# coding=utf-8
import xxtea

text = b"gfdgfd"

key = hex(1)

encrypt_data = xxtea.encrypt(text, key)
decrypt_data = xxtea.decrypt(encrypt_data, key)

print encrypt_data
print decrypt_data
print type(decrypt_data)
