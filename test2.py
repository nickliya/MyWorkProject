from gmpy2 import is_prime
from os import urandom
import base64


def bytes_to_num(b):
    return int(b.encode('hex'), 16)


def num_to_bytes(n):
    b = hex(n)[2:-1]
    if len(b) % 2 == 1:
        b = '0' + b
    else:
        b = b

    return b.decode('hex')


def get_a_prime(l):
    random_seed = urandom(l)

    num = bytes_to_num(random_seed)

    while True:
        if is_prime(num):
            break
        num += 1
    return num


def encrypt(s, e, n):
    p = bytes_to_num(s)
    p = pow(p, e, n)
    return num_to_bytes(p).encode('hex')


def separate(n):
    p = n % 4
    t = (p * p) % 4
    return t == 1


# f = open('flag.txt', 'r')
# flag = f.read()
flag = "QCTF{}"

msg1 = ""
msg2 = ""
for i in range(len(flag)):
    if separate(i):
        msg2 += flag[i]
    else:
        msg1 += flag[i]

p1 = get_a_prime(128)
p2 = get_a_prime(128)
p3 = get_a_prime(128)
n1 = p1 * p2
n2 = p1 * p3
e = 0x1001
c1 = encrypt(msg1, e, n1)
c2 = encrypt(msg2, e, n2)
# print(c1)
# print(c2)

e1 = 0x1001
e2 = 0x101
p4 = get_a_prime(128)
p5 = get_a_prime(128)
n3 = p4 * p5
c1 = num_to_bytes(pow(n1, e1, n3)).encode('hex')
c2 = num_to_bytes(pow(n1, e2, n3)).encode('hex')
# print(c1)
# print(c2)
#
# print(base64.b64encode(num_to_bytes(n2)))
# print(base64.b64encode(num_to_bytes(n3)))

n2dec = "S2FcVBqWJlGtO3bJytsmNV+x2Qls/syILAf0Dv/p/g2nmXZc9atSV0EQ9cpBIOTY2AwDbzZYXvyr3GX/AaxxIPyCHkZmmJWgKthrQyVL3h7WQ1pp6t1v8uFcqKro5iwKdjf9nYSj16ofM1t7e4C26/HRVNCCF/IIEZ4vVYcWWEtfoDcTIAM1GJhd5Dt0aYdxFVWB8WQTSo0tDdGQhmcxvObQMVB4rO8YxM8cicDwbMJG0JwxW2mlrnIVlwG0fQcpbrR2PNx7SQFS+TqM9Fd/qtrqr15qjbZ9BZVnF6laLaISMhRPSo6+DIJjNDmDbxtvEoMSNbFIdqnPTdMuJtim4Q=="
n3dec = "GOQ14Y8W+mQGofmutmHpmFrj6TuAbZJ7KBF2fhWzALaVhKN0DIh4D6eu3QxMzvUuI1l7X7nbWOXudTKTkVf/kWp73gg53vi5HztZppBFSgzJTfPheAz/kvKo8KI9k96HNw6yslgfGAEFOmx2y1JojLaCTaJZBaaBuVMQIfXNh/R9tBJl9oPxdqWzGwfmoKzci88iK7ZjhuQLuwS7o/Pc2u4ORau7TFR5v1JkqrJOdNT1vrAdmO1NdbaZV/DReiHFlKEcptI2ve/vLKO7oYRwCReutux3wNi2wcTni98oRSavWGBI95zievUu96qEGgyv+K+rN7ZmFJFflax+vXtAiQ=="

print base64.b64decode(n2dec).encode("hex")
print base64.b64decode(n3dec).encode("hex")

c1hex = "11574caaea9fd80017ee2986de85b4939d2e43bd5edf5f84e280198004628303fc0c46030926d701194fd8b6b61fdad9fb996291742dcc181d7a21af22f9834caf7650637e458c616ec725a1396ea1920e78ea1ed70d9a35a2390744943a134c8a8101383386e94db4ff4e809d226cffc84bfa2847a3f4fe08ee9df4bf7a40ebf16a347fe90f09016b8b9d2dfb281b536da1fc4442c7b47f84204b3eed6186f4deab1f71ead8edd8c42fe3d93972c220d8c4eb9aab52600ed168ce51064c49b152e34c6fb83de63a635d421c9664fc78f7388de3d1dde7cd3180951c876f20dcede08280ec6ac284b120615e9e141dac68399035bb71eac8cd2bb866b3a6e007"
c2hex = "0230d7a40a416d8c056c314b7d641bffb1dd007917ba0b215f58f6b68f8285067136aa0f0ce37db354cf61d22af84c8be4160963fcbfb9814f31875b458bfea9cb8aa064e5692894f2cde421b16ee2fba30d0b5d5acd8270af65c5bfdd656733b7170b48583a909560c5811cae775499b813efeb9bbb6a8e9da35bd54c0c6d047d6c28a6442cf69522b02c1609774fd4c19e1841989526f70896227138d0fc8bf3ad4ff92466aafc79dbc2b0b68cde3a810d805fba9db05267b33a39f26ccc06c34de1a6a90a5521f01a1e8e0e1387f6ed51b3970409b7562896dfdbf487337d787e6629d474a73e86dbb934446628dad06a8bc6bded821b9a2361f2f1055d12"
