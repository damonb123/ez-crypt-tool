"""
EzCryptTool Example Python Usage Code
"""
import os
import logging

# Import EzCrypt
from ez_crypt_tool.ez_crypt_tool import EzCryptTool

"""
NOTICE
  This example uses the backed in test key.  This is an EXAMPLE key, its in the project under conf/.ezcrypt.key.
  DO NOT REUSE THIS KEY: Its a example and can be used by others to decyrpt your informaiton.
  GENERATE YOUR A NEW KEY BEFORE TRYING TO USE IT
"""

def example_application():
    log_into_db_dummy("dummy","fenc:gAAAAABjk4vdeenLsvEp_WXKCD_pw2a0oNaSI11l-5WLIdAJH4X579N8GOyYHefEPeR03yJymwoViqba9jBWucKHc4ffoev7Eyyn3O7wx3LmyUqRznut8Cw=")


def log_into_db_dummy(user, password):
    ezc = EzCryptTool.get_instance()
    clear_text_pw = ezc.decrypt(password)
    print(f"Encrypted: {password}")
    print(f"Decrypted: {clear_text_pw}")

    # Now use to log into actually database, or any other needing encryption

if __name__ == "__main__":

    # Initialize the EzCryptTool
    EzCryptTool.get_instance().init()

    # Call main fo applications
    example_application()