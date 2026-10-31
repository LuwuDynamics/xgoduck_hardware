"""Cece's prototype text bridge. Voice and walking are not implemented here."""
import argparse
import json
import os
import re
import subprocess
import threading
from pathlib import Path
import urllib.error
import urllib.parse
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

motion_lock = threading.Lock()

def json_request(url, *, payload=None, headers=None, timeout=30):
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(url, data=data, headers=headers or {},
                                     method="GET" if data is None else "POST")
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)

def weather_description(code, daytime):
    if code == 0: return "sunny" if daytime else "clear"
    if code in (1, 2): return "partly cloudy"
    if code == 3: return "cloudy"
    if code in (45, 48): return "foggy"
    if code in (51, 53, 55, 56, 57): return "drizzly"
    if code in (61, 63, 65, 66, 67, 80, 81, 82): return "rainy"
    if code in (71, 73, 75, 77, 85, 86): return "snowy"
    if code in (95, 96, 99): return "stormy"
    return "unknown"

def get_weather(city, latitude, longitude):
    params = urllib.parse.urlencode({"latitude": latitude, "longitude": longitude,
        "current": "temperature_2m,weather_code,is_day", "timezone": "auto"})
    result = json_request("https://api.open-meteo.com/v1/forecast?" + params)
    current = result["current"]
    description = weather_description(int(current["weather_code"]), bool(current["is_day"]))
    return f"In {city}, it is {description} and {round(current['temperature_2m'])} degrees Celsius."

def openai_answer(prompt, model, key):
    if not key:
        raise ValueError("OPENAI_API_KEY is not configured on this computer")
    data = json_request("https://api.openai.com/v1/responses", payload={
        "model": model, "reasoning": {"effort": "none"},
        "instructions": "You are Cece, a small friendly robot. Answer briefly. "
                        "Do not claim to move, see, hear, or know current weather.",
        "input": prompt, "max_output_tokens": 120, "store": False,
    }, headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
       timeout=60)
    parts = [part.get("text", "") for item in data.get("output", [])
             if item.get("type") == "message" for part in item.get("content", [])
             if part.get("type") == "output_text"]
    answer = " ".join(parts).strip()
    if not answer:
        raise ValueError("OpenAI returned no text")
    return answer

def ollama_answer(prompt, model):
    data = json_request("http://127.0.0.1:11434/api/generate", payload={
        "model": model, "stream": False, "prompt": prompt, "think": False,
        "options": {"num_predict": 80, "num_ctx": 1024}},
        headers={"Content-Type": "application/json"}, timeout=60)
    return data["response"].strip()

def atbots_answer(prompt, model):
    # AtBots handles consent, credential storage, refresh and profile locking.
    from atbots.config import ProviderConfig
    from atbots.providers.authenticated import AuthenticatedProvider
    row = ProviderConfig(name="cece", kind="chatgpt", model=model,
                         egress_class="remote", auth_profile="default")
    provider = AuthenticatedProvider(row, capability_refs=[], retries=0)
    result = provider.complete(system="You are Cece, a small friendly robot. Answer briefly. "
                               "Do not claim to move, see, hear, or know current weather.",
                               prompt=prompt)
    return result.text.strip()

def reply(prompt, config):
    # Keep motor commands away from model text: walking is not yet calibrated.
    if re.search(r"\b(?:walk|move|step|forward|backward)\b", prompt, re.I):
        if getattr(config, "sim_motion", False):
            if re.search(r"\b(?:backward|backwards|back|left|right)\b", prompt, re.I):
                return "Only the forward test gait is available in simulation."
            if not motion_lock.acquire(blocking=False):
                return "The simulated gait is already running."
            try:
                sim_dir = Path(__file__).resolve().parents[3] / "ros2_sim"
                subprocess.run(["wsl", "-d", "Ubuntu", "--", "bash", "-c",
                    "source /opt/ros/jazzy/setup.bash && /usr/bin/python3 walk_controller.py"],
                    cwd=sim_dir, check=True, timeout=40, capture_output=True)
                return "I sent two step commands in the simulator."
            finally:
                motion_lock.release()
        return "I cannot walk yet. My motors need calibration and a tested gait."
    if re.search(r"\b(?:weather|temperature|forecast)\b", prompt, re.I):
        return get_weather(config.city, config.latitude, config.longitude)
    if config.provider == "openai":
        return openai_answer(prompt, config.model, os.environ.get("OPENAI_API_KEY"))
    if config.provider == "atbots":
        return atbots_answer(prompt, config.model)
    return ollama_answer(prompt, config.model)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/ask":
            self.send_error(404)
            return
        try:
            size = int(self.headers.get("Content-Length", "0"))
            if size < 1 or size > 800:
                self.send_error(413)
                return
            prompt = self.rfile.read(size).decode("utf-8").strip()
            if not prompt or len(prompt) > 200:
                self.send_error(400)
                return
            response = reply(prompt, self.server.config).encode("utf-8")[:1000]
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", str(len(response)))
            self.end_headers()
            self.wfile.write(response)
        except Exception as exc:
            self.send_error(502, "Cece service unavailable")
            # Never log request headers or the API key.
            print("Cece service error:", type(exc).__name__, flush=True)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--listen", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--provider", choices=("atbots", "openai", "ollama"), default="atbots")
    parser.add_argument("--model", default=None)
    parser.add_argument("--city", default="Sydney")
    parser.add_argument("--latitude", type=float, default=-33.8688)
    parser.add_argument("--longitude", type=float, default=151.2093)
    parser.add_argument("--sim-motion", action="store_true",
                        help="Enable experimental Gazebo gait; never drives physical servos")
    args = parser.parse_args()
    if args.model is None:
        args.model = "qwen3:1.7b" if args.provider == "ollama" else "gpt-6-luna"
    server = ThreadingHTTPServer((args.listen, args.port), Handler)
    server.config = args
    print(f"Cece bridge on {args.listen}:{args.port}; {args.provider} {args.model}", flush=True)
    server.serve_forever()

if __name__ == "__main__":
    main()
