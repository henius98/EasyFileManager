import unittest
import os
import shutil
from easy_file_manager.processor import process_files

class TestProcessor(unittest.TestCase):
    def setUp(self):
        self.test_dir = "test_data"
        os.makedirs(self.test_dir, exist_ok=True)
        with open(os.path.join(self.test_dir, "test_en.srt"), "w") as f:
            f.write("test")

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_rename(self):
        process_files(self.test_dir, suffix="_en.srt", action='r')
        self.assertTrue(os.path.exists(os.path.join(self.test_dir, "test.srt")))
        self.assertFalse(os.path.exists(os.path.join(self.test_dir, "test_en.srt")))

if __name__ == "__main__":
    unittest.main()
