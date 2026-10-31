import json
from pathlib import Path
import tomllib
import unittest

ROOT = Path(__file__).resolve().parents[1]

class ProjectConfigurationTest(unittest.TestCase):
    def test_wokwi_chip_definitions_match_files(self):
        with (ROOT / "wokwi.toml").open("rb") as stream:
            config = tomllib.load(stream)
        self.assertEqual(config["wokwi"]["rfc2217ServerPort"], 4000)
        for chip in config["chip"]:
            binary = ROOT / chip["binary"]
            self.assertTrue(binary.is_file())
            with binary.with_suffix(".json").open(encoding="utf-8") as stream:
                self.assertTrue(json.load(stream)["pins"])

if __name__ == "__main__":
    unittest.main()
