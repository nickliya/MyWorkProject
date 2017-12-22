# -*- coding:utf8 -*-
import os
import base64

# images_path是需要加密的图片的绝对路径
encrypt_key = 95


def encrypt(images_path):
    f = open(images_path, 'rb')
    filedata = f.read()
    filesize = f.tell()
    f.close()

    file_byte_array = bytearray(filedata)
    encrypt_file_byte_array = bytearray(0)

    for byte in file_byte_array:
        encrypt_bype = byte ^ encrypt_key
        encrypt_file_byte_array.append(encrypt_bype)

    info = base64.b64encode(encrypt_file_byte_array)
    os.remove(images_path)
    f2 = open(images_path, 'wb')
    f2.write(info)
    f2.close()


def decrypt(images_path):
    f = open(images_path, 'rb')
    filedata = f.read()
    filesize = f.tell()
    f.close()

    info = base64.b64decode(filedata)
    file_byte_array = bytearray(info)

    decrypt_file_byte_array = bytearray(0)
    for byte in file_byte_array:
        decrypt_bype = byte ^ encrypt_key
        decrypt_file_byte_array.append(decrypt_bype)

    os.remove(images_path)
    f2 = open(images_path, 'wb')
    f2.write(decrypt_file_byte_array)
    f2.close()


path = 'C:\\Users\\YangQ\\Desktop\\bg'
for dirpath, dirnames, filenames in os.walk(path):
    for file in filenames:
        fullpath = os.path.join(dirpath, file)
        encrypt(fullpath)

# encrypt("bgdhjdnr_n.png")
# decrypt("bgdhjdnr_n.png")
