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
ez_crypt_tool
```

| Option | Description |
| ------| -----------|
| --genkey   | Generates a key, that can be used for encryption and decryption. |
| --genkeyfile | Will generate a key and put it in the DEFAULT_KEY_FILE: ~/.ezcrypt/.ezcrypt.key.
| --keyfile:    | Is supplied, will be used for Fernet key. |
| --encrypt: | Uses the key in the KEY_FILES to encrypt a clear text string.|
| --decrypt | Uses the key in the KEY_FILES to decrypt a cipher string. |



KEY_FILES: ['.ezcrypt.key', './conf/.ezcrypt.key', '~/.ezcrypt/.ezcrypt.key']
ENV: Environment can be used, skipping key file.  Example: export EZCRYPT_KEY=<key>

### Step 1:  Generate Key or Key File

```console
ez_crypt_tool --genkey
NQYiJixqOhkFWOESyttUvP4ChIcNehpTiyXMGA0eifA=
```

or

```console
ez_crypt_tool --genkeyfile
NQYiJixqOhkFWOESyttUvP4ChIcNehpTiyXMGA0eifA=
```


### Step 2:  Place key in file

Place the key into the ezcrypt.key file, then put the file in one of the 3 locations listed above in KEY_FILES.

### Step 3: Use command to encrypt password

```console
ez_crypt_tool --encrypt mypassword
Encrypted:gAAAAABi6DbHCEwLiKHIrolX_oUGA9k-3RjB08-5VW0-lg4FdvGgsiwe1HriMkhLfWRFnMJsbJRvmpULEHbu2Q_EQbFDWaPBxA==
```

### Step 4: Store encrypted password

Place encrypted password in configuration file that can be retrieved by the application.

See example under ./sandbox directory.

### Notes

* A prefix of "fenc:<key>" can be prepended to key, to denote encrypted string.  Not required.
* This project uses an example example test key.
* The key file [.ezcrypt.key] is in the conf directory.
* Its only for this example and can be used by others to decyrpt your informaiton.

> !!! DO NOT REUSE THE INCLUDED KEY !!!
> GENERATE A NEW KEY BEFORE USING EzCryptTool in your environment

### Prerequisites  (IMPORTANT)

* Python 3.8.x or greater

* PIP 20.x or greater
* virtualenv 20.14.x or greater

## Code Examples

### EzCryptTool Python Code

___

```python
# Import EzCrypt
from ez_crypt_tool.ez_crypt_tool import EzCryptTool

# Initialize the EzCryptTool
ezc = EzCryptTool.get_instance()

# Starting with clear text string
clear_text_pw = "MyCoolPassword"
print(f"Clear Text: {clear_text_pw}")

# Encrypting the string
crypted_password = ezc.encrypt(clear_text_pw)
print(f"Encrypted: {password}")

# decrypting the string
clear_text_pw = ezc.decrypt(crypted_password)
print(f"Decrypted: {clear_text_pw}")

```

### Output

```console
Clear Text: MyCoolPassword
Encrypted: fenc:gAAAAABjk4vdeenLsvEp_WXKCD_pw2a0oNaSI11l-5WLIdAJH4X579N8GOyYHefEPeR03yJymwoViqba9jBWucKHc4ffoev7Eyyn3O7wx3LmyUqRznut8Cw=
Decrypted: MyCoolPassword
```

## Info and History

___

### History

* Initial upload

### TODO

* [X] Add generate encryption file
* [ ] Add code examples in readme

### Author

* [damonb123@outlook.com](https://github.com/damonb123)

### License

Copyright © 2023, [damonb123](https://github.com/damonb123).
Released under the [APACHE-2.0](LICENSE).

[![Powers by Coffee][8]][9]
