"""Push-to-talk laptop audio for the Wokwi Cece bench, not physical I2S."""
import argparse
from array import array
import audioop
import json
import queue
import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk

import serial
import sounddevice as sd
from vosk import KaldiRecognizer, Model, SetLogLevel

def record(model, device, seconds, whisper=False, device_name=None):
    # Refresh PortAudio's inventory: Windows can renumber devices while the
    # application is open, for example when switching remote audio sessions.
    if device_name:
        sd._terminate()
        sd._initialize()
        for index, candidate in enumerate(sd.query_devices()):
            label = (candidate["name"].replace("\r", " ").replace("\n", " ") +
                     " (" + sd.query_hostapis(candidate["hostapi"])["name"] + ")")
            if candidate["max_input_channels"] > 0 and label == device_name:
                device = index
                break
        else:
            raise RuntimeError("The selected microphone is no longer available; reopen Cece and select it again.")
    info = sd.query_devices(device, "input")
    rate = int(info["default_samplerate"])
    try:
        sd.check_input_settings(device=device, channels=1, samplerate=rate, dtype="int16")
        channels = 1
    except sd.PortAudioError:
        channels = int(info["max_input_channels"])
    frames = queue.Queue()
    def callback(indata, frame_count, timing, status):
        frames.put(bytes(indata))
    recognizer = None if whisper else KaldiRecognizer(model, 16000)
    state = None
    segments = []
    audio_chunks = []
    peak = 0
    with sd.RawInputStream(samplerate=rate, blocksize=4000, dtype="int16",
                           channels=channels, device=device, callback=callback):
        deadline = time.monotonic() + seconds
        while time.monotonic() < deadline:
            try:
                block = frames.get(timeout=0.5)
            except queue.Empty:
                continue
            if channels > 1:
                raw = array("h")
                raw.frombytes(block)
                candidates = [raw[i::channels] for i in range(channels)]
                chosen = max(candidates, key=lambda ch: max(map(abs, ch), default=0))
                block = chosen.tobytes()
            peak = max(peak, audioop.max(block, 2))
            block_peak = audioop.max(block, 2)
            if block_peak:
                block = audioop.mul(block, 2, min(8.0, max(1.0, 6000.0 / block_peak)))
            if rate != 16000:
                block, state = audioop.ratecv(block, 2, 1, rate, 16000, state)
            if whisper:
                audio_chunks.append(block)
            elif recognizer.AcceptWaveform(block):
                segments.append(json.loads(recognizer.Result()).get("text", ""))
    if whisper:
        import numpy as np
        audio = np.frombuffer(b"".join(audio_chunks), dtype="<i2").astype(np.float32) / 32768
        parts, _ = model.transcribe(audio, language="en", beam_size=5, vad_filter=False,
                                    condition_on_previous_text=False)
        return " ".join(part.text.strip() for part in parts).strip(), peak
    segments.append(json.loads(recognizer.FinalResult()).get("text", ""))
    return " ".join(x for x in segments if x).strip(), peak

def ask_esp(text):
    # The existing C3 serial parser accepts at most 96 chars per line.
    safe = " ".join(text.split())[:43]
    if not safe:
        raise ValueError("No speech was recognized.")
    with serial.serial_for_url("rfc2217://127.0.0.1:4000",
                               baudrate=115200, timeout=1) as port:
        time.sleep(0.5)
        port.reset_input_buffer()
        port.write(b"wifi Wokwi-GUEST -\n")
        deadline = time.monotonic() + 30
        connected = False
        while time.monotonic() < deadline:
            port.write(b"status\n")
            until = time.monotonic() + 2
            while time.monotonic() < until:
                line = port.readline().decode("utf-8", "replace").strip()
                if line.startswith("WiFi connected IP:"):
                    connected = True
                    break
            if connected:
                break
        if not connected:
            raise RuntimeError("The simulated ESP32 could not connect to Wokwi Wi-Fi.")
        port.write(("ask http://host.wokwi.internal:8768/ask " + safe + "\n").encode())
        deadline = time.monotonic() + 80
        while time.monotonic() < deadline:
            line = port.readline().decode("utf-8", "replace").strip()
            if line.startswith("LLM: "):
                return line[5:]
            if line.startswith(("Bridge request failed:", "Usage: connect WiFi")):
                raise RuntimeError(line)
        raise TimeoutError("No response from the simulated ESP32.")

def speak(text):
    command = ("Add-Type -AssemblyName System.Speech; "
               "$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; "
               "$s.Speak([Console]::In.ReadToEnd())")
    subprocess.run(["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", command],
                   input=text, text=True, encoding="utf-8", check=True,
                   creationflags=subprocess.CREATE_NO_WINDOW)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument("--device", type=int, default=None)
    parser.add_argument("--seconds", type=int, default=5)
    parser.add_argument("--whisper-model", default=None)
    args = parser.parse_args()
    SetLogLevel(-1)
    if args.whisper_model:
        from faster_whisper import WhisperModel
        model = WhisperModel(args.whisper_model, device="cpu", compute_type="int8")
    else:
        model = Model(args.model)
    root = tk.Tk()
    root.title("Cece - laptop voice prototype")
    root.geometry("640x320")
    status = tk.StringVar(value="Ready. Click Listen, then speak for five seconds.")
    heard = tk.StringVar(value="")
    answer = tk.StringVar(value="")
    ttk.Label(root, text="Cece", font=("Segoe UI", 20, "bold")).pack(pady=8)
    devices = [(i, info["name"].replace("\r", " ").replace("\n", " ") +
               " (" + sd.query_hostapis(info["hostapi"])["name"] + ")")
               for i, info in enumerate(sd.query_devices()) if info["max_input_channels"] > 0]
    names = [f"{i}: {name}" for i, name in devices]
    choice = ttk.Combobox(root, values=names, state="readonly", width=70)
    choice.pack(pady=4)
    requested = next((i for i, (idx, _) in enumerate(devices) if idx == args.device), None)
    preferred = next((i for i, (_, name) in enumerate(devices)
                      if "microphone array" in name.lower() and "wdm-ks" in name.lower()), None)
    default = next((i for i, (idx, _) in enumerate(devices) if idx == sd.default.device[0]), 0)
    selected = requested if requested is not None else (preferred if preferred is not None else default)
    if names:
        choice.current(selected)
    ttk.Label(root, textvariable=status, wraplength=520).pack(pady=4)
    ttk.Label(root, textvariable=heard, wraplength=520).pack(pady=4)
    ttk.Label(root, textvariable=answer, wraplength=520).pack(pady=4)
    button = ttk.Button(root, text="Listen")
    button.pack(pady=12)
    def update(var, value):
        root.after(0, var.set, value)
    def work(device, device_name):
        try:
            update(status, "Listening now...")
            text, peak = record(model, device, args.seconds, bool(args.whisper_model), device_name)
            update(heard, "You: " + (text or "(nothing recognized)") + f"   [mic level: {peak}]")
            if not text:
                raise ValueError("I did not recognize speech. Check the microphone level and try again.")
            update(status, "Sending to the simulated ESP32...")
            response = ask_esp(text)
            update(answer, "Cece: " + response)
            update(status, "Speaking through the laptop speaker...")
            speak(response)
            update(status, "Ready. Click Listen to speak again.")
        except Exception as exc:
            update(status, "Error: " + str(exc))
        finally:
            root.after(0, lambda: button.config(state="normal"))
    def listen():
        index = choice.current()
        if index < 0:
            status.set("Choose a microphone first.")
            return
        button.config(state="disabled")
        threading.Thread(target=work, args=devices[index], daemon=True).start()
    button.config(command=listen)
    root.mainloop()

if __name__ == "__main__":
    main()
