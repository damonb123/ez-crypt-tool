"""
EZ Crypt Tool

"""
# pylint: disable=logging-fstring-interpolation
# pylint: disable=line-too-long
# pylint: disable=too-many-locals
# pylint: disable=too-many-statements

# Python imports
import os
import sys
import getopt

# Rich Imports
# pylint: disable=redefined-builtin
from rich import print

# Fernet imports
from cryptography.fernet import InvalidToken

# ez_crypt_tool Imports
from ez_crypt_tool.ez_crypt_tool import EzCryptTool
from ez_crypt_tool.module_info import ModuleInfo

ez_crypt_tool_mod_info = ModuleInfo(__file__)
def print_mod_info():
    '''Prints the module information'''
    print(mod_info)
def mod_info():
    '''Gets the module information'''
    # pylint: disable=anomalous-backslash-in-string
    return f"[cyan bold]\[{ez_crypt_tool_mod_info.package_name()}/{ez_crypt_tool_mod_info.version()}][/cyan bold]"

HELP_TEXT = f"""
{mod_info()}
This application generates a Fernet key that needs to be retained and stored in [dark_goldenrod]KEY_FILES[/dark_goldenrod].
[bold red]IMPORTANT[/bold red]: Do not loose this key, any encrypted items will be lost and unable to be decrypted[red]![/red]

[dark_goldenrod]USE:[/dark_goldenrod]
[cyan bold]{ez_crypt_tool_mod_info.package_name()}[/cyan bold] [bold yellow]--genkey[/bold yellow] | [bold yellow]--genkeyfile[/bold yellow] | [bold yellow]--encrypt[/bold yellow] <password> | [bold yellow]--decrypt[/bold yellow] <encrypted_pwd>

[bold yellow]--genkey[/bold yellow]: Generates a key, that can be used for encryption and decryption.
[bold yellow]--genkeyfile[/bold yellow]: Will generate a key and put it in the [bold yellow]DEFAULT_KEY_FILE[/bold yellow]: {EzCryptTool.DEFAULT_KEY_FILE}.
  NOTE: Will NOT overrite the key file if it exist.

[bold yellow]--keyfile[/bold yellow]: Is supplied, will be used for Fernet key.
[bold yellow]--encrypt[/bold yellow]: Uses the key in the [dark_goldenrod]KEY_FILES[/dark_goldenrod] to encrypt a clear text string.
[bold yellow]--decrypt[/bold yellow]: Uses the key in the [dark_goldenrod]KEY_FILES[/dark_goldenrod] to decrypt a cipher string.
    Checks to see if string has 'fenc:' in front of it. If so, its removed, then decrypted.

[dark_goldenrod]KEY_FILES:[/dark_goldenrod] {EzCryptTool.KEY_FILES}
[dark_goldenrod]ENV:[/dark_goldenrod] Environment can be used, skipping key file.  Example: export {EzCryptTool.KEY_ENV_NAME}=<key>
"""



# pylint: disable=too-many-branches
def main():
    '''Main for application'''
    # Get system arguments for executable
    argv = sys.argv[1:]


    try:
        # pylint: disable=unused-variable
        opts, args = getopt.getopt(argv,"hskgfed",["status", "genkey", "genkeyfile", "keyfile=", "encrypt=", "decrypt="])
    except getopt.GetoptError:
        print( HELP_TEXT )
        sys.exit(2)

    # Params
    crypt = EzCryptTool()

    try:
        if len(opts) == 0:
            print( HELP_TEXT )
            sys.exit()

        for opt, arg in opts:
            if opt == '-h':
                print( HELP_TEXT )
                sys.exit()

            elif opt in ("-s", "--status"):
                keyfile = None
                if crypt.is_initialized() is False:
                    try:
                        keyfile = crypt.find_load_keyfile()
                    except Exception as ex:
                        print(ex)
                        sys.exit()
                else:
                    keyfile = crypt.get_key_file()

                kfile_full = os.path.expanduser(keyfile)
                if os.path.exists(kfile_full) is False:
                    print("Keyfile not found.")
                else:
                    print(f"keyfile={keyfile}")

            elif opt in ("-k", "--keyfile"):
                keyfile = str(arg).strip()
                crypt.set_key_file(keyfile)

            elif opt in ("-g", "--genkey"):
                fernet_key = EzCryptTool.gen_key()
                print(fernet_key)

            elif opt in ("-f", "--genkeyfile"):
                try:
                    EzCryptTool.gen_key_file()
                except Exception as ex:
                    print(ex)

            elif opt in ("-e", "--encrypt"):
                if crypt.is_initialized() is False:
                    try:
                        keyfile = crypt.find_load_keyfile()
                    except Exception as ex:
                        print(ex)
                        sys.exit()
                ciphered_text = crypt.encrypt(arg)
                print(f"Encrypted:{ciphered_text}")

            elif opt in ("-d", "--decrypt"):
                if crypt.is_initialized() is False:
                    try:
                        keyfile = crypt.find_load_keyfile()
                    except Exception as ex:
                        print(ex)
                        sys.exit()
                clear_text = crypt.decrypt(arg)
                print(f"Decrypted:{clear_text}")

    except InvalidToken:
        print("InvalidToken to decrypt this ciphered text!")

    except Exception as ex:
        raise ex


if __name__ == "__main__":
    main()
