"""
Unit test for ez_crypt_tool
"""
# pylint: disable=missing-module-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=wrong-import-position

# Python Imports
import logging
import unittest
import os

# Un-REM to debug in Visual Sudio Code, the root of project must come first in syspath, or cant find modules when running
#import sys, os; sys.path.insert(0, os.path.abspath('.'))


# Module Imports
from ez_crypt_tool.ez_crypt_tool import EzCryptTool

def make_orderer():
    order = {}

    def ordered(f):
        order[f.__name__] = len(order)
        return f

    def compare(a, b):
        return [1, -1][order[a] < order[b]]

    return ordered, compare

ordered, compare = make_orderer()
unittest.defaultTestLoader.sortTestMethodsUsing = compare

# Change the logging if needing to debug messages
logging.basicConfig(level=logging.ERROR,
                    format='%(asctime)s | %(module)s(%(lineno)d) | %(levelname)s | %(message)s',
                    datefmt='%Y/%m/%d %H:%M:%S')
# Create the EzCryptTool() object first
crypt = EzCryptTool.get_instance()

# Run test
class TestEzCryptTool(unittest.TestCase):
    CRYPT_KEY = None
    CLEAR_TEXT = "MyCoolPassWord"
    CIPHER_TEXT = None

    def __init__(self, *args, **kwargs):
        super(TestEzCryptTool, self).__init__(*args, **kwargs)


    @ordered
    def test_100_genkey(self):
        TestEzCryptTool.CRYPT_KEY = EzCryptTool.gen_key()
        crypt.set_key(TestEzCryptTool.CRYPT_KEY)
        self.assertIsNotNone(TestEzCryptTool.CRYPT_KEY)

    @ordered
    def test_101_encrypt(self):
        TestEzCryptTool.CIPHER_TEXT = crypt.encrypt(TestEzCryptTool.CLEAR_TEXT)
        self.assertIsNotNone(TestEzCryptTool.CIPHER_TEXT)

    @ordered
    def test_102_iscrypt_true(self):
        is_encrypted = crypt.is_encrypted(f"fenc:{TestEzCryptTool.CIPHER_TEXT}")
        self.assertEqual(is_encrypted, True)

    @ordered
    def test_103_iscrypt_false(self):
        is_encrypted = crypt.is_encrypted("fenc:not_encrypt_password")
        self.assertEqual(is_encrypted, False)

    @ordered
    def test_104_iscrypt_false(self):
        enc_test = crypt.decrypt("crappassword")
        self.assertEqual(enc_test, "crappassword")

    @ordered
    def test_105_decrypt(self):
        dec_crypt_test = crypt.decrypt(f"fenc:{TestEzCryptTool.CIPHER_TEXT}")
        self.assertEqual(TestEzCryptTool.CLEAR_TEXT, dec_crypt_test)

    @ordered
    def test_106_s_encrypt(self):
        EzCryptTool.get_instance(key=TestEzCryptTool.CRYPT_KEY)
        TestEzCryptTool.CIPHER_TEXT = EzCryptTool.s_encrypt(TestEzCryptTool.CLEAR_TEXT)
        self.assertIsNotNone(TestEzCryptTool.CIPHER_TEXT)

    @ordered
    def test_107_s_decrypt(self):
        EzCryptTool.get_instance(key=TestEzCryptTool.CRYPT_KEY)
        dec_crypt_test = EzCryptTool.s_decrypt(f"fenc:{TestEzCryptTool.CIPHER_TEXT}")
        self.assertEqual(TestEzCryptTool.CLEAR_TEXT, dec_crypt_test)

if __name__ == "__main__":
    unittest.main()
