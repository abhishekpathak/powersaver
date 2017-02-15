import unittest
import activityregisters


class TestSabnzbdActivityRegister(unittest.TestCase):
    def test_is_active(self):
        sab_register_1 = activityregisters.SabnzbdActivityRegister([])
        sab_register_2 = activityregisters.SabnzbdActivityRegister(
            ["demo job", "another job"])
        self.assertFalse(sab_register_1.is_active())
        self.assertTrue(sab_register_2.is_active())


class TestSambaActivityRegister(unittest.TestCase):
    def test_is_active(self):
        smb_register_1 = activityregisters.SabnzbdActivityRegister([])
        smb_register_2 = activityregisters.SabnzbdActivityRegister(
            ["demo job", "another job"])
        self.assertFalse(smb_register_1.is_active())
        self.assertTrue(smb_register_2.is_active())
