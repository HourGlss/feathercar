import struct
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES, PKCS1_OAEP
import os

def create_struct(num1, num2, num3, num4):
    # Define the struct format string
    struct_format = "B B b b"

    # Pack the numbers into a byte string
    packed_data = struct.pack(struct_format, num1, num2, num3, num4)

    return packed_data

from_device = 8
msg_number = 31
steering = -100
throttle = 100

# CREATE DATA
data = create_struct(from_device, msg_number, steering, throttle)
print(data.hex())

# CREATE RSA KEYS
if not os.path.exists('private.pem') or not os.path.exists("public.pem"):
    key = RSA.generate(1024)
    private_key = key.export_key()
    file_out = open("private.pem", "wb")
    file_out.write(private_key)
    file_out.close()

    public_key = key.publickey().export_key()
    file_out = open("public.pem", "wb")
    file_out.write(public_key)
    file_out.close()

# ENCRYPT DATA WITH RECEIVER'S PUBLIC KEY
file_out_for_data = open("encrypted_data.bin", "wb")
recipient_key = RSA.import_key(open("public.pem").read())
session_key = get_random_bytes(16)

# Encrypt the session key with the public RSA key
cipher_rsa = PKCS1_OAEP.new(recipient_key)
enc_session_key = cipher_rsa.encrypt(session_key)

# Encrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX)
ciphertext, tag = cipher_aes.encrypt_and_digest(data)
[file_out_for_data.write(x) for x in (enc_session_key, cipher_aes.nonce, tag, ciphertext)]
file_out_for_data.close()

# GET DATA TO DECRYPT
file_in = open("encrypted_data.bin", "rb")

# GET PRIVATE KEY
private_key = RSA.import_key(open("private.pem").read())

# LOAD THE ENCRYPTED DATA INTO FIELDS
enc_session_key, nonce, tag, ciphertext = \
    [file_in.read(x) for x in (private_key.size_in_bytes(), 16, 16, -1)]
file_in.close()
print(f"{ciphertext.hex()}{nonce.hex()}{tag.hex()}{enc_session_key.hex()}")
# Decrypt the session key with the private RSA key
cipher_rsa = PKCS1_OAEP.new(private_key)
session_key = cipher_rsa.decrypt(enc_session_key)

# Decrypt the data with the AES session key
cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
data = cipher_aes.decrypt_and_verify(ciphertext, tag)
print(data.hex())