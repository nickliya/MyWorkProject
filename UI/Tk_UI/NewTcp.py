# /usr/bin/python
# coding=utf-8
# creat by 15025463191 2017/06/04
# version:20171017
from Tkinter import *
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
root.title('otu设备模拟器 version:2017.11.22')

root.columnconfigure(0, weight=1)
root.columnconfigure(2, weight=1)
root.columnconfigure(4, weight=1)
root.rowconfigure(0, weight=1)

framentry_otu = Frame(root)
framentry_bt = Frame(root)
frame_qr = Frame(root)
framentry_otu.grid(row=0, column=0, sticky=S + W + N + E)
framentry_bt.grid(row=0, column=2, sticky=S + W + N + E)
frame_qr.grid(row=0, column=4, sticky=S + W + N + E)
Label(root, bg='#87CEEB').grid(row=0, column=1, rowspan=7, sticky=S + N)
Label(root, bg='#87CEEB').grid(row=0, column=3, rowspan=7, sticky=S + N)

# framentry_otu
framentry_otu.columnconfigure(1, weight=1)
framentry_otu.rowconfigure(4, weight=1)
framentry_otu.rowconfigure(6, weight=1)

Label(framentry_otu, text="端口").grid(row=0, sticky=W)
Label(framentry_otu, text="IP:").grid(row=0, column=1, sticky=W)
Label(framentry_otu, text="主机_IMEI").grid(row=1, sticky=W)
Label(framentry_otu, text="蓝牙_IMEI").grid(row=2, sticky=W)
entry_otu = Entry(framentry_otu)
entry_bt = Entry(framentry_otu)
entry_port = Entry(framentry_otu, width=4)
entry_ip = Entry(framentry_otu, width=16)
entry_otu.grid(row=1, column=1, sticky=W + S + N + E)
entry_bt.grid(row=2, column=1, sticky=W + S + N + E)
entry_port.grid(row=0, column=0, sticky=S + N + E)
entry_ip.grid(row=0, column=1, sticky=E)

frame1_l1 = Label(framentry_otu, text='自定义输入界面:')
frame1_l1.grid(row=3, columnspan=2, sticky=W)
frame1_l2 = Label(framentry_otu, text='接收界面:')
frame1_l2.grid(row=5, columnspan=2, sticky=W)

t1 = Text(framentry_otu, width=34, height=4)
t1.grid(row=4, column=0, columnspan=3, sticky=W + S + E + N)
t2 = Text(framentry_otu, width=34, height=13)
t2.grid(row=6, column=0, columnspan=3, sticky=W + S + E + N)

# framentry_bt
framentry_bt.columnconfigure(0, weight=1)
framentry_bt.columnconfigure(1, weight=1)
framentry_bt.rowconfigure(0, weight=1)
framentry_bt.rowconfigure(1, weight=1)
framentry_bt.rowconfigure(2, weight=1)
framentry_bt.rowconfigure(3, weight=1)
framentry_bt.rowconfigure(4, weight=1)
framentry_bt.rowconfigure(5, weight=1)
framentry_bt.rowconfigure(6, weight=1)
framentry_bt.rowconfigure(7, weight=1)
framentry_bt.rowconfigure(8, weight=1)
# framentry_bt.rowconfigure(9, weight=1)

frame2_l1 = Label(framentry_bt, text='不使用了请离线\n需挂机保持连接请\n勾选心跳')
frame2_l1.grid(row=11, column=0, columnspan=2, sticky=N + S + E + W)

# frame_qr
frame_qr.columnconfigure(0, weight=1)
frame_qr.columnconfigure(1, weight=1)
frame_qr.columnconfigure(2, weight=1)
frame_qr.rowconfigure(3, weight=1)
# frame3.rowconfigure(1, weight=1)
Label(frame_qr, text='转换内容').grid(row=0, column=0, sticky=E + W)
Label(frame_qr, text='请检查空格，空格也会作为内容一部分转成二维码').grid(row=2, column=0, columnspan=3, sticky=E + W)
qrcodecontent = Entry(frame_qr)
qrcodecontent.grid(row=0, column=1, columnspan=2, sticky=E + W)

frame3_l1 = Label(frame_qr, text='二维码装填区域')
frame3_l1.grid(row=3, column=0, columnspan=3)

data = open('D:\Tcptemp\data.txt', "a+")
historyinfo = data.read()  # 读取缓存文件data
historyinfolist = historyinfo.split(",")

entry_otu.insert(END, historyinfolist[0])
data.close()
if len(historyinfolist) == 3:
    entry_port.insert(END, historyinfolist[2])
if len(historyinfolist) == 2 or len(historyinfolist) == 3:
    entry_ip.insert(END, historyinfolist[1])

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
    "OBD": "(1*fa|7|30e,1,2,1,3333,1,0,2|)",
    "ACC": "(1*12|7|301,2,1111)",
    "余油614": "(1*ea|5|614,3,7#b312,1,32,32#|)",
    "余电614": "(1*ea|5|614,3,7#b313,1,32,32#|)",
    "余电31F": "(1*88|7|31F,1,32,0,0|)",
    "余油30A": "(1*88|7|30A,1,22|)",
    "总里程614": "(1*ea|5|614,3,7#b311,9C4#|)",
    "总里程313": "(1*10|7|313,1,10,1,552.0.0.0f39202a00,|)",
}

# 变量声明
r_blank = r'\d*\d'  # 识别空格的正则
stopsingle = 0  # 停止信号
tkimg = None  # 图片
s = None  # soket连接


def Btbd():
    u"""蓝牙绑定"""
    Bt_IMEI = entry_bt.get()
    conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
    cur = conn.cursor()
    sql = "SELECT mac FROM [sirui].[dbo].[Terminal] WHERE IMEI=\'" + Bt_IMEI + "\';"
    cur.execute(sql)
    info = cur.fetchall()
    mac = str(info)[4:-4]
    cur.close()
    conn.close()
    s.send('(1*f5|7|315,8_btu.CC2640.0_0113.release.0_BT_M_B1b.0.00_mac' + str(mac) + '_300,|)')


def sx():
    u"""上线"""
    otu_IMEI = entry_otu.get()
    tcpadress = entry_ip.get()
    tcpport = entry_port.get()
    IMEI_NUM = re.findall(r_blank, otu_IMEI)
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcpadress, int(tcpport)))
    # s.send('(1*7c|a3|106,201|101,' + str(
    #     IMEI_NUM[0]) + '|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
    s.send('(1*7c|a3|106,201|101,' + str(
        IMEI_NUM[0]) + '|102,460079241205511|104,otu.ost,01022300|105,a1,18|622,a1c2|)')  # 商用去掉103
    historydata = open('D:\Tcptemp\data.txt', "wb")  # 生成缓存文件data
    historydata.write(otu_IMEI + "," + tcpadress + "," + tcpport)  # IMEI保存到缓存文件data
    historydata.close()

    def xc():
        global stopsingle
        stopsingle = 0
        while 1:
            tcpreceive = s.recv(1024)
            x = tcpreceive[7:10]  # 检测是否为控制协议
            if x == '511' or x == '512' or x == '513' or x == '514' or x == '515' or x == '516' or x == '517' \
                    or x == '518' or x == '519' or x == '51A' or x == '51B' or x == '51C':
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
            elif tcpreceive == "":
                stopsingle = 1
                s.shutdown(2)
                s.close()
                frame1_b2['text'] = '上线'
                frame1_b2['command'] = sx
                frame2_c1['state'] = DISABLED
            else:
                # print "received data:", tcpreceive
                t2.insert(END, tcpreceive)
                t2.update()
                # if not tcpreceive:
            if stopsingle == 1:
                break

    thrd1 = threading.Thread(target=xc)
    threads.append(thrd1)
    thrd1.setDaemon(True)
    thrd1.start()
    frame1_b2['text'] = '离线'
    frame1_b2['command'] = lx
    frame2_c1['state'] = NORMAL


def lx():
    u"""离线"""
    global stopsingle
    stopsingle = 1
    s.shutdown(2)
    # s.close()
    frame1_b2['text'] = '上线'
    frame1_b2['command'] = sx
    frame2_c1['state'] = DISABLED


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
    frame3_l1.configure(image='')


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
        # nowtime = utc_tran.strftime('%Y%m%d%H%M%S')
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
        Sec = '%x' % int(second)
        strhextime = str(m) + ',' + str(d) + ',' + str(H) + ',' + str(M) + ',' + str(Sec)
        return strhextime

    timeinfo = '(1*b2|7|30d,11,' + hextime() + ',E,10629.7228,N,2937.1144,0,10,c,1,1,-1,79|)'
    t1.insert(END, timeinfo)
    t1.update()


def xt():
    u"""心跳"""

    def xc2():
        while heart_v.get() == 1:
            s.send('()')
            time.sleep(30)
            if heart_v.get() == 0:
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
    qr.add_data(qrcodecontent.get())
    qr.make(fit=True)
    img = qr.make_image()
    img.save('D:\Tcptemp\qrcode.jpg')


def createCarQRcode():
    u"""生成展车二维码"""
    Bt_IMEI = qrcodecontent.get()
    conn = pymssql.connect(host='192.168.6.51', user='sa', password='test2017')
    cur = conn.cursor()
    sql = "SELECT ClientType FROM [sirui].[dbo].[Terminal]WHERE IMEI=\'" + Bt_IMEI + "\';"
    cur.execute(sql)
    info = cur.fetchall()
    clientType = str(info)[2:-3]
    if clientType == '16':
        sql = "SELECT randomID FROM [sirui].[dbo].[Bluetooth] WHERE mac=\'" + Bt_IMEI + "\';"
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
    u"""二维码转Tk二维码图片"""
    im = Image.open(url)
    newimg = im.resize((280, 280), Image.ANTIALIAS)  # 缩放图片
    global tkimg
    tkimg = ImageTk.PhotoImage(newimg)
    return tkimg


def createrqimg():
    createQRcode()
    jin = Img_tk('D:\Tcptemp\qrcode.jpg')
    frame3_l1.configure(image=jin)


def createrqimg2():
    createCarQRcode()
    Img_tk('D:\Tcptemp\qrcode.jpg')
    frame3_l1.configure(image=tkimg)


def mr():
    """默认"""
    entry_port.delete(0, END)
    entry_ip.delete(0, END)
    entry_port.insert(END, 2103)
    entry_ip.insert(END, '192.168.6.52')


# frame1
frame1_b1 = Button(framentry_otu, text='默认', command=mr)
frame1_b2 = Button(framentry_otu, text='上线', command=sx)
frame1_b3 = Button(framentry_otu, text='绑定', command=Btbd)
frame1_b4 = Button(framentry_otu, text='发送', command=send)
frame1_b5 = Button(framentry_otu, text='清空', command=qk1)
frame1_b6 = Button(framentry_otu, text='清空', command=qk2)
frame1_b1.grid(row=0, column=2)
frame1_b2.grid(row=1, column=2)
frame1_b3.grid(row=2, column=2)
frame1_b4.grid(row=3, column=2)
frame1_b5.grid(row=3, column=1, sticky=E)
frame1_b6.grid(row=5, column=2)

# frame2
frame2_b1 = Button(framentry_bt, text='能力', command=fz, cursor="circle")
frame2_b2 = Button(framentry_bt, text='设防')
frame2_b3 = Button(framentry_bt, text='引擎')
frame2_b4 = Button(framentry_bt, text='门锁')
frame2_b5 = Button(framentry_bt, text='速度')
frame2_b6 = Button(framentry_bt, text='温度')
frame2_b7 = Button(framentry_bt, text='GSM')
frame2_b8 = Button(framentry_bt, text='星数')
frame2_b9 = Button(framentry_bt, text='位置', command=sbwz)
frame2_b10 = Button(framentry_bt, text='电压')
frame2_b11 = Button(framentry_bt, text='车窗')
frame2_b12 = Button(framentry_bt, text='车门')
frame2_b13 = Button(framentry_bt, text='OBD')
frame2_b14 = Button(framentry_bt, text='ACC')
frame2_b15 = Button(framentry_bt, text='余油614')
frame2_b16 = Button(framentry_bt, text='余电614')
frame2_b17 = Button(framentry_bt, text='余油30A')
frame2_b18 = Button(framentry_bt, text='余电31F')
frame2_b19 = Button(framentry_bt, text='总里程614')
frame2_b20 = Button(framentry_bt, text='总里程313')

frame2_b2.bind("<Button-1>", showpic)
frame2_b3.bind("<Button-1>", showpic)
frame2_b4.bind("<Button-1>", showpic)
frame2_b5.bind("<Button-1>", showpic)
frame2_b6.bind("<Button-1>", showpic)
frame2_b7.bind("<Button-1>", showpic)
frame2_b8.bind("<Button-1>", showpic)
frame2_b10.bind("<Button-1>", showpic)
frame2_b11.bind("<Button-1>", showpic)
frame2_b12.bind("<Button-1>", showpic)
frame2_b13.bind("<Button-1>", showpic)
frame2_b14.bind("<Button-1>", showpic)
frame2_b15.bind("<Button-1>", showpic)
frame2_b16.bind("<Button-1>", showpic)
frame2_b17.bind("<Button-1>", showpic)
frame2_b18.bind("<Button-1>", showpic)
frame2_b19.bind("<Button-1>", showpic)
frame2_b20.bind("<Button-1>", showpic)

frame2_b1.grid(row=0, column=0, sticky=N + S + W + E)
frame2_b2.grid(row=0, column=1, sticky=N + S + W + E)
frame2_b3.grid(row=1, column=0, sticky=N + S + W + E)
frame2_b4.grid(row=1, column=1, sticky=N + S + W + E)
frame2_b5.grid(row=2, column=0, sticky=N + S + W + E)
frame2_b6.grid(row=2, column=1, sticky=N + S + W + E)
frame2_b7.grid(row=3, column=0, sticky=N + S + W + E)
frame2_b8.grid(row=3, column=1, sticky=N + S + W + E)
frame2_b9.grid(row=4, column=0, sticky=N + S + W + E)
frame2_b10.grid(row=4, column=1, sticky=N + S + W + E)
frame2_b11.grid(row=5, column=0, sticky=N + S + W + E)
frame2_b12.grid(row=5, column=1, sticky=N + S + W + E)
frame2_b13.grid(row=6, column=0, sticky=N + S + W + E)
frame2_b14.grid(row=6, column=1, sticky=N + S + W + E)
frame2_b15.grid(row=7, column=0, sticky=N + S + W + E)
frame2_b16.grid(row=7, column=1, sticky=N + S + W + E)
frame2_b17.grid(row=8, column=0, sticky=N + S + W + E)
frame2_b18.grid(row=8, column=1, sticky=N + S + W + E)
frame2_b19.grid(row=9, column=0, sticky=N + S + W + E)
frame2_b20.grid(row=9, column=1, sticky=N + S + W + E)

heart_v = IntVar()
frame2_c1 = Checkbutton(framentry_bt, text='心跳挂机', variable=heart_v, command=xt, state=DISABLED)
frame2_c1.grid(row=10, column=0, columnspan=2, sticky=E + W + S)

# frame3
frame3_b1 = Button(frame_qr, text='生成普通二维码', command=createrqimg)
frame3_b2 = Button(frame_qr, text='生成展车二维码', command=createrqimg2)
frame3_b3 = Button(frame_qr, text='清除二维码', width=12, command=qc)
frame3_b1.grid(row=1, column=0, sticky=E + W)
frame3_b2.grid(row=1, column=1, sticky=E + W)
frame3_b3.grid(row=1, column=2, sticky=E + W)

mainloop()
