# /usr/bin/python
# coding=utf-8
# creat by 15025463191 2017/06/04

from tkinter import *
import socket
import threading
import time
from PIL import Image, ImageTk
import qrcode
import base64
import pymssql
import os

isexisted = os.path.exists('D:\Tcptemp')
if not isexisted:
    os.makedirs('D:\Tcptemp')
else:
    pass

threads = []
root = Tk()
root.title('TCP测试定制 version:2017.7.11')

root.columnconfigure(1, weight=1)
root.rowconfigure(4, weight=1)
root.rowconfigure(6, weight=1)

Label(root, text="端口").grid(row=0, sticky=W)
Label(root, text="IP:").grid(row=0, column=1, sticky=W)
Label(root, text="主机_IMEI").grid(row=1, sticky=W)
Label(root, text="蓝牙_IMEI").grid(row=2, sticky=W)
Label(root, bg='#87CEEB').grid(row=0, column=3, rowspan=7, sticky=S+N)
Label(root, bg='#87CEEB').grid(row=0, column=6, rowspan=7, sticky=S+N)
Label(root, text='不使用了请\n离线，长时\n间挂机请勾\n选心跳').grid(row=6, column=4, columnspan=2, sticky=S)
Label(root, text='内容').grid(row=0, column=7, sticky=W)
Label(root, text='请检查空格，空格也会作为内容一部分转成二维码').grid(row=2, column=7, columnspan=3, sticky=W)

l = Label(root, text='二维码装填区域')
l.grid(row=3, column=7, rowspan=4, columnspan=3)

e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root, width=32)
e4 = Entry(root, width=4)
e5 = Entry(root, width=16)

data = open('D:\Tcptemp\data.txt', "a+")
historyinfo = data.read()  # 读取缓存文件data
historyinfolist = historyinfo.split(",")

e1.insert(END, historyinfolist[0])
data.close()
if len(historyinfolist) == 3:
    e4.insert(END, historyinfolist[2])
if len(historyinfolist) == 2 or len(historyinfolist) == 3:
    e5.insert(END, historyinfolist[1])

e1.grid(row=1, column=1, sticky=W+S+N+E)
e2.grid(row=2, column=1, sticky=W+S+N+E)
e3.grid(row=0, column=7, columnspan=3, sticky=E)
e4.grid(row=0, column=0, sticky=S+N+E)
e5.grid(row=0, column=1, sticky=E)

protocol = {
    "引擎": "(1*12|7|302,1,11,1)",
    "门锁": "(1*33|7|305,2,2222|)",
    "电压": "(1*88|7|316,1,1,4B0,4F0|)",
    "温度": "(1*33|7|30B,1,E0|)",
    "GSM": "(1*74|7|30f,14,333e,331a,GSM850_EGSM_DCS_PCS_MODE|)",
    "星数": "(1*33|7|30C,1,1,1,D,1|)",
    "设防": "(1*a7|7|308,1,1|)",
    "速度": "(1*88|7|31a,1,1,50|)",
    "车窗": "(1*88|7|317,1,11111|)",
    "车门": "(1*33|7|304,1,11111|)",
    "OBD诊断": "(1*fa|7|30e,1,2,1,3333,1,0,2|)",
    "ACC": "(1*12|7|301,2,1111)",
    "余油": "(1*e7|5|614,3,7#b312,1,32,3C#|)",
    "余电": "(1*ed|5|614,3,7#b313,1,32,3C#|)",
}

r_blank = r'\d*\d'


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
        IMEI_NUM[0]) + '|102,460079241205511|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
    # IMEI_NUM[0]) + '|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
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


b1 = Button(root, text='上线', command=sx)
b2 = Button(root, text='绑定', command=Btbd)
b3 = Button(root, text='能力', command=fz)
b4 = Button(root, text='设防')
b5 = Button(root, text='发送', command=send)
b6 = Button(root, text='清空', command=qk1)
b7 = Button(root, text='清空', command=qk2)
b8 = Button(root, text='引擎')
b9 = Button(root, text='门锁')
b10 = Button(root, text='速度')
b11 = Button(root, text='温度')
b12 = Button(root, text='GSM')
b13 = Button(root, text='星数')
b14 = Button(root, text='位置', command=sbwz)
b15 = Button(root, text='电压')
b16 = Button(root, text='车窗')
b17 = Button(root, text='车门')
b18 = Button(root, text='生成普通二维码', command=createrqimg)
b19 = Button(root, text='生成展车二维码', command=createrqimg2)
b20 = Button(root, text='清除二维码', command=qc)
b21 = Button(root, text='默认', command=mr)
b22 = Button(root, text='OBD')
b23 = Button(root, text='ACC')
b24 = Button(root, text='余油')
b25 = Button(root, text='余电')

b4.bind("<Button-1>", showpic)
b8.bind("<Button-1>", showpic)
b9.bind("<Button-1>", showpic)
b10.bind("<Button-1>", showpic)
b11.bind("<Button-1>", showpic)
b12.bind("<Button-1>", showpic)
b13.bind("<Button-1>", showpic)
b15.bind("<Button-1>", showpic)
b16.bind("<Button-1>", showpic)
b17.bind("<Button-1>", showpic)
b22.bind("<Button-1>", showpic)
b23.bind("<Button-1>", showpic)
b24.bind("<Button-1>", showpic)
b25.bind("<Button-1>", showpic)

b1.grid(row=1, column=2)
b2.grid(row=2, column=2)
b3.grid(row=3, column=4)
b4.grid(row=3, column=5)
b5.grid(row=3, column=2)
b6.grid(row=3, column=1, sticky=E)
b7.grid(row=5, column=2)
b8.grid(row=0, column=4)
b9.grid(row=0, column=5)
b10.grid(row=1, column=4)
b11.grid(row=1, column=5)
b12.grid(row=2, column=4)
b13.grid(row=2, column=5)
b14.grid(row=4, column=4, sticky=S)
b15.grid(row=4, column=4, sticky=N)
b16.grid(row=4, column=5, sticky=N)
b17.grid(row=4, column=5, sticky=S)
b18.grid(row=1, column=7, sticky=W)
b19.grid(row=1, column=8, sticky=W)
b20.grid(row=1, column=9, sticky=W)
b21.grid(row=0, column=2)
b22.grid(row=6, column=4,sticky=N)
b23.grid(row=5, column=4)
b24.grid(row=5, column=5)
b25.grid(row=6, column=5, sticky=N)

l1 = Label(root, text='自定义输入界面:')
l1.grid(row=3, columnspan=2, sticky=W)
l2 = Label(root, text='接收界面:')
l2.grid(row=5, columnspan=2, sticky=W)

t1 = Text(root, width=34, height=4)
t1.grid(row=4, column=0, columnspan=3, sticky=W+S+E+N)
t2 = Text(root, width=34, height=13)
t2.grid(row=6, column=0, columnspan=3, sticky=W+S+E+N)

v = IntVar()
c1 = Checkbutton(root, text='心跳挂机', variable=v, command=xt, state=DISABLED)
c1.grid(row=6, column=4, columnspan=2)
mainloop()
