import unittest

from jarvis.safety.permissions import (
    arbitrary_shell_allowed,
    cloud_access_allowed,
    requires_confirmation,
)


class PermissionTests(unittest.TestCase):
    def test_cloud_and_shell_are_disabled(self):
        self.assertFalse(cloud_access_allowed())
        self.assertFalse(arbitrary_shell_allowed())

    def test_destructive_actions_require_confirmation(self):
        self.assertTrue(requires_confirmation("delete_file"))
        self.assertTrue(requires_confirmation("upload"))
        self.assertFalse(requires_confirmation("list_directory"))


if __name__ == "__main__":
    unittest.main()
