"""
    EZ Crypt Tool

"""

# Python imports
import os
import logging

# Un-REM to debug in Visual Sudio Code, the root of project must come first in syspath, or cant find modules when running
#import sys, os; sys.path.insert(0, os.path.abspath('.'))

# Cryptogrophy
from cryptography.fernet import Fernet
import cryptography.exceptions

# pylint: disable=f-string-without-interpolation
# pylint: disable=line-too-long

class EzCryptTool():
    """
    Encrypt/Decrypt tool for Python.

    Returns:
        None
    """
    # Class variables
    __EZ_CRYPT_INST = None
    KEY_ENV_NAME="EZCRYPT_KEY"
    DEFAULT_KEY_FILE="~/.ezcrypt/.ezcrypt.key"
    KEY_FILES = [".ezcrypt.key", './conf/.ezcrypt.key', DEFAULT_KEY_FILE]
    CRYPT_PREFIX = "fenc:"
    __NOT_INITIALIZED = f"ez_crypt_tool is NOT intialized!  Key must be set or loaded from keyfile!"

    # pylint: disable=too-many-instance-attributes

    def __init__(self, key=None, key_file=None):
        self.__key = None
        self.__key_file = None
        self.__cipher_suite = None
        if key is not None:
            logging.info("Init using passed key")
            self.__set_key(key)
        if key_file is not None:
            logging.info(f"Init using passed key_file: {key_file}")
            self.__set_key_file(key_file)
        try:
            key_env = os.environ.get(EzCryptTool.KEY_ENV_NAME)
            if key_env is not None:
                logging.info(f"Init using env variable: {EzCryptTool.KEY_ENV_NAME}!")
                self.__set_key(key_env)
        # pylint: disable=bare-except
        except:
            pass

    def init(self, key=None, key_file=None):
        '''Loads crypt system from params or file if no other options are available'''
        if key is not None:
            logging.info("Init using passed key")
            self.__set_key(key)
        if key_file is not None:
            logging.info(f"Init using passed key_file: {key_file}")
            self.__set_key_file(key_file)
        try:
            key_env = os.environ.get(EzCryptTool.KEY_ENV_NAME)
            if key_env is not None:
                logging.info(f"Init using env variable: {EzCryptTool.KEY_ENV_NAME}!")
                self.__set_key(key_env)
        # pylint: disable=bare-except
        except:
            pass

        if self.is_initialized() is False:
            self.find_load_keyfile()

        return self

#    def __new__(cls, key=None, key_file=None):
#        if not hasattr(cls, 'instance'):
#            cls.instance = super(EzCryptTool, cls).__new__(cls)
#            EzCryptTool.__EZ_CRYPT_INST:EzCryptTool = cls.instance
#            new_key = EzCryptTool.__EZ_CRYPT_INST.gen_key()
#            EzCryptTool.__EZ_CRYPT_INST.set_key(new_key)
#        return cls.instance

    def is_initialized(self):
        """Returns if EzCryptTool is initialized with key or keyfile and ready to work"""
        if self.__cipher_suite is not None:
            return True
        return False

    def find_load_keyfile(self):
        """Finds and loads keyfile"""
        return self.__find_key_file()

    def set_key_file(self, key_file=None):
        """Sets key file for decrypting"""
        if key_file is not None:
            self.__set_key_file(key_file)
        else:
            self.__find_key_file()

    def set_key(self, key:str):
        """Sets key for decrypting"""
        self.__set_key(key)

    def __set_key(self, key:str):
        # Save the key
        self.__key = key

        # Create a new cipher_suite with new key
        self.__cipher_suite = Fernet(bytes(self.__key.encode("UTF8")))

    def __set_key_file(self, key_file:str):
        # Save the key_file name, open and read keyfile
        self.__key_file = key_file

        key = self.__open_key_file(self.__key_file)
        self.__set_key(key)

    def get_key_file(self):
        '''Gets the current keyfile being used'''
        return self.__key_file

    @staticmethod
    def __open_key_file(key_file):
        '''Reads a key file and returns the key.'''
        try:
            full_path = os.path.expanduser(key_file)
            with open(full_path, "r", encoding="utf-8") as keyf:
                key = keyf.read()
        except Exception as ex:
            logging.exception(ex)
            raise Exception(f"Key file [{key_file}] does not exist.  Can NOT continue!") from ex

        # Strip string, clean it up
        key = key.strip()

        return key

    def __find_key_file(self):
        if self.__key_file is not None:
            raise Exception(f"Keyfile already loaded: [{self.__key_file}]")
        kfile_full = None
        for kfile in EzCryptTool.KEY_FILES:
            try:
                kfile_full = os.path.expanduser(kfile)
                if os.path.exists(kfile_full):
                    key = self.__open_key_file(kfile_full)
                    if key is not None:
                        self.__set_key(key)
                        break
            # pylint: disable=broad-except
            except Exception:
                pass

        if self.__key is None:
            raise Exception(f"Could not find a key in one of these keyfiles: [{EzCryptTool.KEY_FILES}]")

        return kfile_full


    def read_key_file(self, key_file=None):
        '''Reads a fernet key from a key file.'''
        # Try to open and read key file
        if key_file is not None:
            self.__key_file = key_file
            key = self.__open_key_file(key_file)
        # Now set the key
        self.__set_key(key)
        return key

    @staticmethod
    def gen_key():
        '''Generates a Fernet key that can be used to encrypt/decrypt values.'''
        return Fernet.generate_key().decode("UTF8")

    @staticmethod
    def gen_key_file():
        '''Generates a new keyfile if it does not exist'''
        key = EzCryptTool.gen_key()
        keyfile = EzCryptTool.get_instance().get_key_file()
        if keyfile is None:
            keyfile = EzCryptTool.DEFAULT_KEY_FILE

        try:
            kfile_full = os.path.expanduser(keyfile)
            kfile_path = os.path.dirname(kfile_full)
            os.makedirs(kfile_path, exist_ok=True)

            if os.path.exists(kfile_full) is False:
                with open(kfile_full, "x", encoding="UTF8") as f_file:
                    f_file.write(key)
                print(f"Wrote new key into keyfile:{kfile_full}")
            else:
                print(f"ERROR: Not writing keyfile:{kfile_full}, it already exist!")
        # pylint: disable=broad-except
        except Exception as ex:
            print(ex)

    def encrypt(self, clear_text:str):
        '''Uses a fernet key encrypt a value.'''

        if self.__cipher_suite is None:
            raise Exception(EzCryptTool.__NOT_INITIALIZED)

        ciphered_text = self.__cipher_suite.encrypt(bytes(clear_text.encode("UTF8"))).decode("UTF8")

        return ciphered_text

    def is_encrypted(self, ciphered_text:str):
        '''Used to check if string is encrypted!'''
        # pylint: disable=broad-except, bare-except
        try:
            decrypt_text = self.decrypt(ciphered_text)

            temp = ciphered_text
            if ciphered_text.startswith(EzCryptTool.CRYPT_PREFIX):
                temp = ciphered_text.replace(EzCryptTool.CRYPT_PREFIX,"")

            if temp != decrypt_text:
                return True

        except:
            pass

        return False

    def decrypt(self, ciphered_text:str):
        '''Uses a fernet key dencrypt a ciphered text.'''

        if self.__cipher_suite is None:
            raise Exception(EzCryptTool.__NOT_INITIALIZED)


        if ciphered_text.startswith(EzCryptTool.CRYPT_PREFIX):
            ciphered_text = ciphered_text.replace(EzCryptTool.CRYPT_PREFIX,"")
        clear_text = ciphered_text

        # pylint: disable=broad-except
        try:
            temp = self.__cipher_suite.decrypt(bytes(ciphered_text.encode("UTF8"))).decode("UTF8")
            clear_text = temp
        except cryptography.exceptions.InvalidTag as ex:
            logging.info(f"{type(ex).__name__}: Ciphered text has invalid tag!")
        except cryptography.exceptions.InvalidSignature as ex:
            logging.info(f"{type(ex).__name__}: Ciphered text has invalid signiture!")
        except cryptography.fernet.InvalidToken as ex:
            logging.info(f"{type(ex).__name__}: Ciphered text was not crypted by same key!")
        except Exception as ex:
            logging.error(f"Exception: {type(ex)}")

        return clear_text

    @staticmethod
    def get_instance(key:str=None,key_file:str=None):
        ''' Simple initialize and load keyfile for ez_crypt_tool using singleton '''
        # Use singleton
        #global __EZ_CRYPT_INST

        crypt = None
        if EzCryptTool.__EZ_CRYPT_INST is None:
            crypt = EzCryptTool(key=key, key_file=key_file)
            EzCryptTool.__EZ_CRYPT_INST = crypt
        else:
            crypt = EzCryptTool.__EZ_CRYPT_INST

        if key is not None:
            crypt.set_key(key)
        elif key_file is not None:
            crypt.set_key_file(key_file)

        return crypt

    @staticmethod
    def s_encrypt(clear_text:str):
        ''' Simple encrypt clear string using singleton'''
        # Use singleton
        crypt = EzCryptTool.get_instance()
        return crypt.encrypt(clear_text)

    @staticmethod
    def s_decrypt(ciphered_text:str):
        ''' Simple decrypt ciphered string using singleton'''
        # Use singleton
        crypt = EzCryptTool.get_instance()
        return crypt.decrypt(ciphered_text)
