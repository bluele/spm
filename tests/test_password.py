#-*- coding:utf-8 -*-
__author__ = 'bluele'

if __name__ == '__main__':
    from libs.manager import PasswordManager
    from libs.utils import sha256
    import unittest

    class TestPassword(unittest.TestCase):
        def setUp(self):
            self.password = 'password'
            self.password_hash = sha256(self.password)

        def testDoubleHash(self):
            pm = PasswordManager()
            PasswordManager.to_hash("password")
            self.assertEqual(
                PasswordManager.to_double_hash("password"),
                PasswordManager.to_double_hash("password")
            )
            self.assertEqual(
                PasswordManager.to_double_hash("password"),
                PasswordManager.to_hash(PasswordManager.to_hash("password"))
            )
            self.assertNotEqual(
                PasswordManager.to_hash("password"),
                PasswordManager.to_double_hash("password"),
            )

    unittest.main()