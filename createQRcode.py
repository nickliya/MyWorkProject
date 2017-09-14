#coding=utf-8
#create by 15025463191 2017/07/01

import qrcode
import base64
import pymssql

def make_qr(str,save):
    qr=qrcode.QRCode(
        version=4,  #生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M, #L:7% M:15% Q:25% H:30%
        box_size=10, #每个格子的像素大小
        border=2, #边框的格子宽度大小
    )
    qr.add_data(str)
    qr.make(fit=True)

    img=qr.make_image()
    img.save(save)

Bt_IMEI=raw_input('BT_IMEI：')
conn=pymssql.connect(host='192.168.6.51',user='sa',password='test2017')
cur=conn.cursor()
sql="SELECT randomID FROM [sirui].[dbo].[Bluetooth] where mac=\'"+Bt_IMEI+"\';"
cur.execute(sql)
info = cur.fetchall()
randomID = str(info)[4:-4]
c=Bt_IMEI+'_'+randomID+'_0_copyright@sirui ChungKing'
print c
c1=base64.b64encode(c)
code='exhibition_'+c1
print code
save_path='qrcode.jpg' #生成后的保存文件
make_qr(code,save_path)

