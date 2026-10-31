import io
import json
import threading
import unittest
import urllib.error
import urllib.request
from http.server import ThreadingHTTPServer
from types import SimpleNamespace
from unittest.mock import patch
import server

class BridgeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.http = ThreadingHTTPServer(("127.0.0.1", 0), server.Handler)
        cls.http.config = SimpleNamespace(provider="openai", model="test-model",
                                          city="Sydney", latitude=-33.8688, longitude=151.2093)
        cls.worker = threading.Thread(target=cls.http.serve_forever, daemon=True)
        cls.worker.start()
        cls.url = f"http://127.0.0.1:{cls.http.server_port}/ask"

    @classmethod
    def tearDownClass(cls):
        cls.http.shutdown()
        cls.http.server_close()
        cls.worker.join()

    def post(self, text):
        request = urllib.request.Request(self.url, data=text, method="POST")
        return urllib.request.urlopen(request, timeout=3)

    def test_openai_response(self):
        response = {"output": [{"type": "message", "content": [
            {"type": "output_text", "text": "Hello there!"}]}]}
        with patch.dict("os.environ", {"OPENAI_API_KEY": "test-only"}), \
             patch.object(server, "json_request", return_value=response) as mock:
            with self.post(b"Hello") as result:
                self.assertEqual(result.read(), b"Hello there!")
            self.assertEqual(mock.call_args.kwargs["payload"]["model"], "test-model")
            self.assertFalse(mock.call_args.kwargs["payload"]["store"])

    def test_weather_uses_weather_service(self):
        data = {"current": {"temperature_2m": 21.2, "weather_code": 0, "is_day": 1}}
        with patch.object(server, "json_request", return_value=data):
            with self.post(b"What is the weather?") as result:
                self.assertEqual(result.read(), b"In Sydney, it is sunny and 21 degrees Celsius.")

    def test_walk_not_claimed_or_dispatched(self):
        with patch.object(server, "openai_answer") as model:
            with self.post(b"move forward") as result:
                self.assertIn(b"cannot walk", result.read())
            model.assert_not_called()

    def test_atbots_provider_selected(self):
        config = SimpleNamespace(provider="atbots", model="gpt-6-luna")
        with patch.object(server, "atbots_answer", return_value="Hello!") as model:
            self.assertEqual(server.reply("hello", config), "Hello!")
            model.assert_called_once_with("hello", "gpt-6-luna")

    def test_simulation_motion_accepts_requested_count(self):
        config = SimpleNamespace(sim_motion=True)
        with patch.object(server, "start_gait", side_effect=lambda count: server.motion_lock.release()) as run:
            self.assertIn("20 simulated steps", server.reply("move forward twenty steps", config))
            run.assert_called_once_with(20)
            self.assertIn("forward", server.reply("move backwards", config))
            self.assertEqual(run.call_count, 1)
        self.assertEqual(server.requested_steps("move forward 100 steps"), 100)
        self.assertIsNone(server.requested_steps("move forward"))

    def test_stop_signal_only_for_running_simulation(self):
        config = SimpleNamespace(sim_motion=True)
        self.assertEqual(server.reply("stop", config), "The simulated gait is not running.")
        with patch.object(server, "STOP_FILE") as stop:
            server.motion_lock.acquire()
            try:
                self.assertEqual(server.reply("stop", config), "Stopping the simulated gait.")
                stop.touch.assert_called_once()
            finally:
                server.motion_lock.release()

    def test_missing_key_does_not_claim_success(self):
        with patch.dict("os.environ", {}, clear=True):
            with self.assertRaises(urllib.error.HTTPError) as exc:
                self.post(b"hello")
            self.assertEqual(exc.exception.code, 502)

    def test_empty_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as exc:
            self.post(b"")
        self.assertEqual(exc.exception.code, 413)

if __name__ == "__main__":
    unittest.main()
