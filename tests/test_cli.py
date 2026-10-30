import tempfile
import unittest
from pathlib import Path

from devlog.cli import add_task, complete_task, load_tasks


class WorkLogTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / "worklog.json"

    def tearDown(self):
        self.temp.cleanup()

    def test_add_and_complete_real_task(self):
        task = add_task(self.path, "Fix CSV export for empty datasets")
        self.assertEqual(task["status"], "open")
        done = complete_task(self.path, task["id"], "Added regression test and fixed empty export.")
        self.assertEqual(done["status"], "done")
        self.assertEqual(load_tasks(self.path)[0]["result"], "Added regression test and fixed empty export.")

    def test_reject_vague_task(self):
        with self.assertRaises(ValueError):
            add_task(self.path, "fix bug")

    def test_reject_duplicate_completion(self):
        task = add_task(self.path, "Improve command line help output")
        complete_task(self.path, task["id"], "Clarified usage examples and option descriptions.")
        with self.assertRaises(ValueError):
            complete_task(self.path, task["id"], "Tried to complete it again.")

    def test_unknown_id(self):
        with self.assertRaises(ValueError):
            complete_task(self.path, 99, "This task does not exist.")

if __name__ == "__main__":
    unittest.main()
