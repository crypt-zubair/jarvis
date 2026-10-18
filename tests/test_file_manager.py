import tempfile
import unittest
from pathlib import Path

from jarvis.desktop.file_manager import FileManager


class FileManagerTests(unittest.TestCase):
    def test_delete_requires_confirmation(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "note.txt"
            target.write_text("keep me", encoding="utf-8")
            with self.assertRaises(PermissionError):
                FileManager().delete_file(target)
            self.assertTrue(target.exists())

    def test_read_text(self):
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder) / "note.txt"
            target.write_text("hello", encoding="utf-8")
            self.assertEqual(FileManager().read_text(target), "hello")


if __name__ == "__main__":
    unittest.main()
