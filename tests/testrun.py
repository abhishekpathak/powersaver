import unittest
from unittest.mock import MagicMock
import run


class TestRun(unittest.TestCase):
    def setUp(self):
        self.activityinspector = MagicMock(name = "activity inspector")
        self.samba_activity_register = MagicMock(name = "samba activity "
                                                        "register")
        self.sabnz_activity_register = MagicMock(name = "sabnzbd activity "
                                                        "register")
        self.activityinspector.inspect_samba.return_value = \
            self.samba_activity_register
        self.activityinspector.inspect_sabnzbd.return_value = \
            self.sabnz_activity_register

    def test_check_server_active_samba_active(self):
        self.samba_activity_register.is_active.return_value = True
        self.sabnz_activity_register.is_active.return_value = False
        expected = True
        actual = run.check_server_active(self.activityinspector)
        self.assertEquals(expected, actual)
        self.samba_activity_register.is_active.assert_called_once_with()

    def test_check_server_active_both_inactive(self):
        self.samba_activity_register.is_active.return_value = False
        self.sabnz_activity_register.is_active.return_value = False
        expected = False
        actual = run.check_server_active(self.activityinspector)
        self.assertEquals(expected, actual)
        self.samba_activity_register.is_active.assert_called_once_with()
        self.sabnz_activity_register.is_active.assert_called_once_with()
