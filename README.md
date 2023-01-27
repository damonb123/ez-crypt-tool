![Made with Python][7]

[![license][5]][6]
[![Python Supported Version][1]][2]
[![PyPi Package][3]][4]

[1]: https://img.shields.io/badge/python-3.11%3E-blue
[2]: https://www.python.org/downloads/release/python-3111/
[3]: https://img.shields.io/pypi/v/pip.svg
[4]: https://pypi.org/project/pip/
[5]: https://img.shields.io/badge/License-Apache_2.0-blue.svg
[6]: http://www.apache.org/licenses/LICENSE-2.0
[7]: https://forthebadge.com/images/badges/made-with-python.svg
[8]: https://forthebadge.com/images/badges/powered-by-coffee.svg
[9]: https://www.peets.com/products/big-bang

# EZ Crypt Tool for Python

Create and used encryption keys to encrypt any sensitive information used for your application.  Can be used by command line, in environment variables, within Python code as a module.  Simplies the process and makes it easy to kep sensative information safe.

## Operations

___

### Install

```sh
pip install ez-crypt-tool
```

### USE

```sh
ez_crypt_tool -h

This application generates a Fernet key that needs to be retained and stored in KEY_FILES.
IMPORTANT: Do not loose this key, any encrypted items will be lost and unable to be decrypted!

USE:
ez_crypt_tool --genkey | --genkeyfile | --genkeyfile <path/file.key> | --keyfile <path/file.key> | --encrypt <password> | --decrypt <encrypted_pwd>

--genkey: Generates a key, that can be used for encryption and decryption.
--genkeyfile: With no parameter will generate a key and put it in the DEFAULT_KEY_FILE: ~/ezcrypt/.ezcrypt.key.
    Pass a key file path and name to
    NOTE: Will NOT overrite the key file if it exist.

--keyfile: To supply a custome key file.
--encrypt: Uses the key in the KEY_FILES to encrypt a clear text string.
--decrypt: Uses the key in the KEY_FILES to decrypt a cipher string.
    NOTE: Use 'fenc:' in front of encrypted key, to indicate an encrypted value. If present, 'fenc:' is removed, then decrypted.

KEY_FILES: ['.ezcrypt.key', './conf/.ezcrypt.key', '~/ezcrypt/.ezcrypt.key']
ENV: Environment can be used, skipping key file.  Example: export EZCRYPT_KEY=<key>
```

### Step 1:  Generate Key

```sh
ez_crypt_tool --genkey
NQYiJixqOhkFWOESyttUvP4ChIcNehpTiyXMGA0eifA=
```

### Step 2:  Place key in file

Place the key into the ezcrypt.key file, then put the file in one of the 3 locations listed above in KEY_FILES.

### Step 3: Use command to encrypt password

```sh
ez_crypt_tool --encrypt mypassword
Encrypted:gAAAAABi6DbHCEwLiKHIrolX_oUGA9k-3RjB08-5VW0-lg4FdvGgsiwe1HriMkhLfWRFnMJsbJRvmpULEHbu2Q_EQbFDWaPBxA==
```

### Step 4: Store encrypted password

Place encrypted password in configuration file that can be retrieved by the application.

See example under ./sandbox directory.

### Notes

A prefix of "fenc:<key>" can be prepended to key, to denote encrypted string.  Not required.

### NOTICE

* This project uses an example example test key.</span>
* The key file [.ezcrypt.key] is in the conf directory.
* Its only for this example and can be used by others to decyrpt your informaiton.
* !!! DO NOT REUSE THE INCLUDED KEY !!!
* GENERATE A NEW KEY BEFORE USING EzCryptTool in your environment.

## Prerequisites  (IMPORTANT)

* Python 3.8.x or greater

* PIP 20.x or greater
* virtualenv 20.14.x or greater

## Code Examples

___

```python
    Example code here
```

## Info and History

___

### History

* Initial upload

### TODO

* [X] Add generate encryption file
* [X] Add code examples in readme

### Author

* [damonb123@outlook.com](https://github.com/damonb123)

### License

Copyright © 2023, [damonb123](https://github.com/damonb123).
Released under the [APACHE-2.0](LICENSE).

[![Powers by Coffee][8]][9]