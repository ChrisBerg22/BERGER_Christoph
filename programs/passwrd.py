# creates a secure password

import string # module for strings
import secrets

alphabet = string.ascii_letters + string.digits + string.punctuation

passwd = ""

for i in range(30):
    passwd += secrets.choice(alphabet)

print(passwd)
