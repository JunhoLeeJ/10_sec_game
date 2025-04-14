from cryptography.fernet import Fernet
import keyring
input_file = "data.txt"
output_file = "encrypted_data.txt"

# 키 생성
key = Fernet.generate_key()
keyring.set_password('10_sec_game', 'encryption_key', key.decode())
fernet = Fernet(key)

# 암호화
with open(input_file, "r") as f:
    data = f.read()
with open(output_file, "wb") as f:
    f.write(fernet.encrypt(data.encode()))
