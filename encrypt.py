from cryptography.fernet import Fernet

# 원본 파일명 (당신이 정한 TXT_FILE_NAME)
input_file = "data.txt"
# 암호화된 파일명 (당신이 정한 ENCRYPTED_FILE_NAME)
output_file = "encrypted_data.txt"

# 키 생성 (임시, 게임에선 keyring 사용)
key = Fernet.generate_key()
fernet = Fernet(key)

# 암호화
with open(input_file, "r") as f:
    data = f.read()
with open(output_file, "wb") as f:
    f.write(fernet.encrypt(data.encode()))

print(f"Encrypted {input_file} to {output_file}")
print("Note: This key is temporary. Game will use keyring.")