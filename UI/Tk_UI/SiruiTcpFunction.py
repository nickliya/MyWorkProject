# /usr/bin/python
# coding=utf-8
# creat by 15025463191 2017/08/26


import socket
import threading
import time
from PIL import Image, ImageTk
import qrcode
import base64
import pymssql


def createrqimg():
    createQRcode()
    Img_tk('D:\Tcptemp\qrcode.jpg')
    l.configure(image=tkimg)


def createrqimg2():
    createCarQRcode()
    Img_tk('D:\Tcptemp\qrcode.jpg')
    l.configure(image=tkimg)


def Btbd():
    u"""蓝牙绑定"""
    Bt_IMEI = e2.get()
    conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
    cur = conn.cursor()
    sql = "SELECT mac FROM [sirui].[dbo].[Terminal] where IMEI=\'" + Bt_IMEI + "\';"
    cur.execute(sql)
    info = cur.fetchall()
    mac = str(info)[4:-4]
    cur.close()
    conn.close()
    s.send('(1*f5|7|315,8_btu.CC2640.0_0113.release.0_BT_M_B1b.0.00_mac' + str(mac) + '_300,|)')


def sx():
    u"""上线"""
    global pd
    pd = 0
    otu_IMEI = e1.get()
    tcpadress = e5.get()
    tcpport = e4.get()
    IMEI_NUM = re.findall(r_blank, otu_IMEI)
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcpadress, int(tcpport)))
    s.send('(1*7c|a3|106,201|101,' + str(
        IMEI_NUM[0]) + '|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
    data = open('D:\Tcptemp\data.txt', "wb")  # 生成缓存文件data
    data.write(otu_IMEI+","+tcpadress+","+tcpport)  # IMEI保存到缓存文件data
    data.close()

    def xc():
        while 1:
            tcpreceive = s.recv(1024)
            x = tcpreceive[7:10]  # 检测是否为控制协议
            if x == '511' or x == '512' or x == '513' or x == '514' or x == '515' or x == '516' or x == '517' or x == '518' or x == '519' \
                    or x == '51A' or x == '51B' or x == '51C':
                t2.insert(END, tcpreceive)
                t2.update()
                protocol_dic = {
                    "511": "上锁", "512": "解锁", "513": "寻车", "514": "静音", "515": "点火",
                    "516": "熄火", "517": "关门窗", "518": "开门窗", "519": "关天窗", "51A": "开天窗",
                    "51B": "通油", "51C": "断油",
                }
                r = r'\(\*..\|7\|\d\d\w,\w*?,\d\|\)'
                datainfo = re.findall(r, tcpreceive)
                str_data = str(datainfo[0])
                print('recv:' + protocol_dic[str_data[7:10]] + str_data)
                a = str_data[0] + '1' + str_data[1:5] + '8' + str_data[6:]
                s.send(a)
                print('send:' + a)
                b = a[0:6] + '7|4' + a[9:12] + '1,1|)'
                s.send(b)
                print(b)
            else:
                # print "received data:", tcpreceive
                t2.insert(END, tcpreceive)
                t2.update()
                # if not tcpreceive:
            if pd == 1:
                break

    thrd1 = threading.Thread(target=xc)
    threads.append(thrd1)
    thrd1.setDaemon(True)
    thrd1.start()
    b1['text'] = '离线'
    b1['command'] = lx
    c1['state'] = NORMAL


def lx():
    u"""离线"""
    global pd
    pd = 1
    s.shutdown(2)
    s.close()
    b1['text'] = '上线'
    b1['command'] = sx
    c1['state'] = DISABLED


def fz():
    u"""能力赋值"""
    s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')


def send():
    u"""发送"""
    send_message = t1.get('0.0', END)
    s.send(send_message)


def qk1():
    u"""清空"""
    t1.delete('0.0', END)


def qk2():
    u"""清空"""
    t2.delete('0.0', END)


def qc():
    u"""清除"""
    l.configure(image='')


def showpic(event):
    info = event.widget['text'].encode('utf-8')
    pro = (protocol[info])
    t1.insert(END, pro)
    t1.update()


def sbwz():
    u"""设备位置"""
    import time
    import datetime

    def hextime():
        now_stamp = time.time()
        local_time = datetime.datetime.fromtimestamp(now_stamp)

        def local2utc(local_st):
            time_struct = time.mktime(local_st.timetuple())
            utc_st = datetime.datetime.utcfromtimestamp(time_struct)
            return utc_st

        utc_tran = local2utc(local_time)
        nowtime = utc_tran.strftime('%Y%m%d%H%M%S')
        month = utc_tran.strftime('%m')
        day = utc_tran.strftime('%d')
        hour = utc_tran.strftime('%H')
        minute = utc_tran.strftime('%M')
        newminute = int(minute) - 3
        second = utc_tran.strftime('%S')
        m = '%x' % int(month)
        d = '%x' % int(day)
        H = '%x' % int(hour)
        M = '%x' % newminute
        S = '%x' % int(second)
        strhextime = str(m) + ',' + str(d) + ',' + str(H) + ',' + str(M) + ',' + str(S)
        # time.sleep(3)
        return strhextime

    timeinfo = '(1*b2|7|30d,11,' + hextime() + ',E,10629.7228,N,2937.1144,0,10,c,1,1,-1,79|)'
    t1.insert(END, timeinfo)
    t1.update()


def xt():
    u"""心跳"""

    def xc2():
        while v.get() == 1:
            s.send('()')
            time.sleep(30)
            if v.get() == 0:
                break

    thrd2 = threading.Thread(target=xc2)
    threads.append(thrd2)
    thrd2.setDaemon(True)
    thrd2.start()


def createQRcode():
    u"""生成二维码"""
    qr = qrcode.QRCode(
        version=4,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
        box_size=10,  # 每个格子的像素大小
        border=2,  # 边框的格子宽度大小
    )
    qr.add_data(e3.get())
    qr.make(fit=True)
    img = qr.make_image()
    img.save('D:\Tcptemp\qrcode.jpg')


def createCarQRcode():
    u"""生成展车二维码"""
    Bt_IMEI = e3.get()
    conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
    cur = conn.cursor()
    sql = "SELECT ClientType FROM [sirui].[dbo].[Terminal]where IMEI=\'" + Bt_IMEI + "\';"
    cur.execute(sql)
    info = cur.fetchall()
    clientType = str(info)[2:-3]
    if clientType == '16':
        sql = "SELECT randomID FROM [sirui].[dbo].[Bluetooth] where mac=\'" + Bt_IMEI + "\';"
        cur.execute(sql)
        info = cur.fetchall()
        randomID = str(info)[4:-4]
        c = Bt_IMEI + '_' + randomID + '_0_copyright@sirui ChungKing'
    else:
        c = Bt_IMEI + '_' + Bt_IMEI[-6:] + Bt_IMEI[-2:] + '_0_copyright@sirui ChungKing'
    print c
    c_info = base64.b64encode(c)
    code = 'exhibition_' + c_info
    print code
    qr = qrcode.QRCode(
        version=4,  # 生成二维码尺寸的大小 1-40  1:21*21（21+(n-1)*4）
        error_correction=qrcode.constants.ERROR_CORRECT_M,  # L:7% M:15% Q:25% H:30%
        box_size=10,  # 每个格子的像素大小
        border=2,  # 边框的格子宽度大小
    )
    qr.add_data(code)
    qr.make(fit=True)
    img = qr.make_image()
    img.save('D:\Tcptemp\qrcode.jpg')


def Img_tk(url):
    u'二维码转Tk二维码图片'
    im = Image.open(url)
    newimg = im.resize((250, 250), Image.ANTIALIAS)  # 缩放图片
    global tkimg
    tkimg = ImageTk.PhotoImage(newimg)


def mr():
    e4.delete(0, END)
    e5.delete(0, END)
    e4.insert(END, 2103)
    e5.insert(END, '192.168.6.52')
