import unittest

from jarvis.config import load_config


class ConfigTests(unittest.TestCase):
    def test_cloud_and_shell_are_disabled(self):
        config = load_config()
        self.assertFalse(config["privacy"]["allow_cloud_fallback"])
        self.assertFalse(config["privacy"]["allow_arbitrary_shell_commands"])

    def test_default_model_is_local(self):
        config = load_config()
        self.assertEqual(config["ai"]["base_url"], "http://127.0.0.1:11434")
        self.assertTrue(config["ai"]["model"])


if __name__ == "__main__":
    unittest.main()
