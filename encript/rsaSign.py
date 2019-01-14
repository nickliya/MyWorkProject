# coding=utf-8

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.Hash import SHA


from Crypto.Hash import MD5
import base64


def RSA_sign(data):
    # privateKey = '''MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAOAUZ0MSftk8ZWTw46udqRj1n43wP0YXejb2tf+2cWP6JJtnD6Hu0tCZZoxk6+L5Qh8NAYxmCiydI3p4Qhe021RajRqda6IvHRL9Tp0NO5McXEtT7mkuJZRriGT5s4ZPECzO/k8nePbJ7nWf/dM84JjVNyIlroEnX7wpEW/16M5bAgMBAAECgYEA2wM2NnlCYCNG2xUTAW7Ukt+ntjxmK6TQwB38ntV8GIKp+vYNcnGRvW7hq0EMyUhk1yKIK+ij8x0XSyF1P+R2JTQ4t3bVl1ZtseJbv9Pq90awMXAANg9rFfuIHGeVBez1BHbxellzKr/+e5Szb5c/tcT86QbQEDbC8z2oZK9TgAECQQD/nq3m7yDKr58ABHhKL9gZnpyXu2aFAzWeknlVKF5DI0Aud1rEAIv7J3E/EWaz0Zk+UHxid0NELyxrqBoMWo5bAkEA4Gm3SVsdCt5Ojam7ktka8Q/welZW/FaSZNFYG1Tv3vXZ2OxFOS9FcnrUChcP6YjTXFUj95s9XVcOb8N/Kn7AAQJBAO79E4f7AMSfp9+jTjfGPZvOYIe4LSSlGIeWWJxWrrLEjWgkLRddj4KUoNufUE9E4qqRI4oICTsBg91vgFMWg0sCQHRPdnanqZrLc61KrnRC4ArW9w2BGF56xC9KrT6lPBm0FK+wbYRg8r6N2L5OC6o/h0SQwC6CIEDzcQEOMyekQAECQEl7MgzeVI4pYoufCo17RFznAWNZPVzRAXdJ5nlBJtmUTB+A4f0EN2RciqiRhI6mz3XEW8d4MnMY14JtbNrZkTk='''
    privateKey = '''MIICdwIBADANBgkqhkiG9w0BAQEFAASCAmEwggJdAgEAAoGBAJn8mZMiAZASwLaheskz0VpUJa+32OXXmzQF20DCY7zn7wB9gm+Kqfb05JsTvLxVnAMBKHSJGOA0+3MOIXjOcKlZIiPf7t4R91WeH3cCMrW3Ipt9xDiEBjwsoY4bdEKEA13nCypn35aKrzQvmEMjEMahvk8+FyeyGRJb+TzFFjTZAgMBAAECgYB//sp81VhtNFlBtUoFsm/DYIyO2geNTUEx5ehQlQQogrVUN/9SzfTnVLos+SP5fEOY775713V48DFOeqFx9E8J9h6P47TZ6j1HaTjk13iByetsdlVqqn1TQVmD/rUDLHLPc+9ACjRZS6czSPR78VZDyeMXRrQB4zCVrkg3GyBYPQJBAOu2HwbsS013mzCytJEUR64uNupTa5C7Cv9Z9P2HI3eAhJ5tOBpEEK/g1LALe/axlLT9ggK0KAYO6mQanrIvlO8CQQCnPa7KfEQhzMuexZeRR6p2bR+am5fmNLdPC8S1H/SOANXlhtlbSSA5tBzxzr54iyN3/zy4ulWYUZoNNJO/ZSK3AkBd5oOdwmyNQ+SzFb4RPb8AiLCf0PO9CIZtC20pwrhCVxR9+IytCgiLyElyiGCt+jh/ka5FXXfEUhTWJDSsT4BJAkEAl1E/MmRHPRHQdoKvhbqDKI3Jl5kKUjcGWJX8UClum4F0By4AwhCjALLPsZXvTqAN4ofkx/uIcL38ldApknYOdwJBAL88p7mFa+N5s741xiZ/msvJnD4xA+FxlFoOllZbs+Nx5jcBkYpK2NJTqdTvPC2YFdAjctwNhCk9f8Mc4Sfa1qc='''
    private_keyBytes = base64.b64decode(privateKey)
    priKey = RSA.importKey(private_keyBytes)
    signer = PKCS1_v1_5.new(priKey)
    h = SHA.new(data)
    signature = signer.sign(h)
    signatureBase64 = base64.b64encode(signature)
    return signatureBase64


# a = RSA_sign("commandId=4&companyID=aotu&numberPlate=沪AZU029")
# a = RSA_sign("accelerate=14&collisionAcceleration=159&collisionCheckTime=0.9&collisionContineTime=29&collisionStopTime=290&numberPlate=沪D45865&rollAngSpeed=49&rollAngleChg=49&rollStopTime=9&slowDown=14&turnFastAngSpeedThd=7&turnFastSpeedThd=79&turnLowAngSpeedThd=9&turnLowSpeedThd=19&vibrate=100")
# a = RSA_sign("accelerate=46&collisionAcceleration=260&collisionCheckTime=5&collisionContineTime=101&collisionStopTime=1201&numberPlate=沪D45865&rollAngSpeed=101&rollAngleChg=181&rollStopTime=31&slowDown=51&turnFastAngSpeedThd=101&turnFastSpeedThd=101&turnLowAngSpeedThd=101&turnLowSpeedThd=80&vibrate=150")
# a = RSA_sign("accelerate=40&collisionAcceleration=230&collisionCheckTime=3&collisionContineTime=60&collisionStopTime=800&numberPlate=沪D45865&rollAngSpeed=70&rollAngleChg=88&rollStopTime=20&slowDown=48&turnFastAngSpeedThd=66&turnFastSpeedThd=90&turnLowAngSpeedThd=88&turnLowSpeedThd=60&vibrate=125")

dic = {
    "keyWord": "861477035280435",
    "vibrationAcceleration": "20",
    "collisionAcceleration": "161",
    "collisionDetectionDuration": "3",
    "collisionDuration": "35",
    "collisionStopDuration": "500",
    "flipAngularthreshold": "60",
    "flipChangeThreshold": "100",
    "flipParkingDuration": "20",
    "accelerationThreshold": "30",
    "decelerationThreshold": "35",
    "sharpLowSpeed": "40",
    "sharpLowAngleThreshold": "50",
    "sharpHighThreshold": "90",
    "sharpHighAngleThreshold": "60",
    "product_key": "7a6d2266-4df0-492b-a28a-5e9390f1db47",
    "msgid": "沪B2133"
}
keylist = dic.keys()
keylist.sort()
signMsg = ""
for key in keylist:
    value = dic[key]
    signMsg += (key+"="+str(value)+"&")


a = RSA_sign(signMsg[:-1])
print(a)
b = RSA_sign("accelerationThreshold=30&collisionAcceleration=161&collisionDetectionDuration=3&collisionDuration=35&collisionStopDuration=500&decelerationThreshold=35&flipAngularthreshold=60&flipChangeThreshold=100&flipParkingDuration=20&keyWord=861477035280435&msgid=2a289c2e-a7b8-4ace-86be-2d4d1896ed68&product_key=7a6d2266-4df0-492b-a28a-5e9390f1db47&sharpHighAngleThreshold=60&sharpHighThreshold=90&sharpLowAngleThreshold=50&sharpLowSpeed=40&vibrationAcceleration=20")
print(a)

