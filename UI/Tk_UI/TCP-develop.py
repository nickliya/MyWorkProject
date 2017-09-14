#/usr/bin/python
#coding=utf-8
#creat by 15025463191 2017/06/04

from tkinter import *
import socket
import threading
import pymssql


root = Tk()
root.title('TCP开发定制')
# root.geometry('400x300')
# root.columnconfigure(0, weight=1)
Label(root, text="端口").grid(row=0,sticky=W)
Label(root, text="IP:").grid(row=0,column=1,sticky=W)
Label(root, text="主机_IMEI").grid(row=1)
Label(root, text="蓝牙_IMEI").grid(row=2)
Label(root,bg='#87CEEB',height=20).grid(row=0,column=3,rowspan=7)
e1 = Entry(root)
e2 = Entry(root)
e3 = Entry(root,width=4)
e4 = Entry(root,width=16)

e1.grid(row=1, column=1,sticky=W)
e2.grid(row=2, column=1,sticky=W)
e3.grid(row=0, column=0,sticky=E)
e4.grid(row=0, column=1,sticky=E)

protocol={
    "引擎":"(1*12|7|302,1,11,1)",
    "门锁":"(1*33|7|305,2,2222|)",
    "电压":"(1*88|7|316,1,1,4B0,4F0|)",
    "温度":"(1*33|7|30B,1,E0|)",
    "GSM":"(1*74|7|30f,14,333e,331a,GSM850_EGSM_DCS_PCS_MODE|)",
    "星数":"(1*33|7|30C,1,1,1,D,1|)"
}

def Btbd():
    u'蓝牙绑定'
    Bt_IMEI=e2.get()
    conn=pymssql.connect(host='192.168.6.51',user='sa',password='test2017')
    cur=conn.cursor()
    sql="SELECT mac FROM [sirui].[dbo].[Terminal] where IMEI=\'"+Bt_IMEI+"\';"
    cur.execute(sql)
    info = cur.fetchall()
    mac = str(info)[4:-4]
    cur.close()
    conn.close()
    s.send('(1*f5|7|315,8_btu.CC2640.0_0113.release.0_BT_M_B1b.0.00_mac'+str(mac)+'_300,|)')
    print('ok2')

def sx():
    u'上线'
    global pd
    pd=0
    tcpadress=e4.get()
    tcpport=e3.get()
    otu_IMEI=e1.get()
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((tcpadress,int(tcpport)))
    s.send('(1*7c|a3|106,201|101,'+otu_IMEI+'|102,460079241205511|103,898600D23113837|104,otu.ost,01022300|105,a1,18|622,a1c2|)')
    def xc():
        while 1:
            tcpreceive = s.recv(1024)
            x=tcpreceive[7:10] #检测是否为控制协议
            if x=='511' or x=='512' or x=='513' or x=='514' or x=='515' or x=='516' or x=='517' or x=='518' or x=='519' or \
               x=='51A' or x=='51B' or x=='51C':
                t2.insert(END,tcpreceive)
                t2.update()
                protocol_dic={
                "511":"上锁","512":"解锁","513":"寻车","514":"静音","515":"点火",
                "516":"熄火","517":"关门窗","518":"开门窗","519":"关天窗","51A":"开天窗",
                "51B":"通油","51C":"断油",
                }
                r = r'\(\*..\|7\|\d\d\w,\w*?,1\|\)'
                datainfo = re.findall(r,tcpreceive)
                str_data = str(datainfo[0])
                print('recv:'+protocol_dic[str_data[7:10]]+str_data)
                a = str_data[0]+'1'+str_data[1:5]+'8'+str_data[6:]
                s.send(a)
                print('send:'+a)
                b = a[0:6]+'7|4'+a[9:12]+'1,1|)'
                s.send(b)
                print(b)
            else:
                # print "received data:", tcpreceive
                t2.insert(END,tcpreceive)
                t2.update()
                # if not tcpreceive:
            if pd==1:
                break
    threads = []
    global t
    t = threading.Thread(target=xc)
    threads.append(t)
    t.setDaemon(True)
    t.start()
    b1['text']='离线'
    b1['command']=lx

def lx():
    u'离线'
    global pd
    pd=1
    s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')
    s.close()
    b1['text']='上线'
    b1['command']=sx

def fz():
    u'能力赋值'
    s.send('(1*67|7|10c,100,100,100,100,100,100,100,100,100,100,100,100,100|)')

def sf():
    u'设防'
    s.send('(1*a7|7|308,1,1|)')

# def gn():
#     u'功能测试'
#     protocol_dic={
#         "511":"上锁","512":"解锁","513":"寻车","514":"静音","515":"点火",
#         "516":"熄火","517":"关门窗","518":"开门窗","51B":"通油","51C":"断油",
#     }
#     time.sleep(1)
#     data = s.recv(1024)
#     r = r'\(\*..\|7\|\d\d\w,\w*?,1\|\)'
#     datainfo = re.findall(r,data)
#     str_data = str(datainfo[0])
#     print('recv:'+protocol_dic[str_data[7:10]]+str_data)
#     a = str_data[0]+'1'+str_data[1:5]+'8'+str_data[6:]
#     s.send(a)
#     print('send:'+a)
#     b = a[0:6]+'7|4'+a[9:12]+'1,1|)'
#     s.send(b)
#     print(b)

def send():
    u'发送'
    send_message=t1.get('0.0',END)
    s.send(send_message)

def qk1():
    u'清空'
    t1.delete('0.0',END)

def qk2():
    u'清空'
    t2.delete('0.0',END)

def showpic(event):
    info=event.widget['text'].encode('utf-8')
    pro=(protocol[info])
    t1.insert(END,pro)
    t1.update()

def sbwz():
    u'设备位置'
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
        newminute = int(minute)-3
        second = utc_tran.strftime('%S')
        m = '%x' %int(month)
        d = '%x' %int(day)
        H = '%x' %int(hour)
        M = '%x' %newminute
        S = '%x' %int(second)
        strhextime = str(m)+','+str(d)+','+str(H)+','+str(M)+','+str(S)
        time.sleep(3)
        return strhextime
    timeinfo='(1*b2|7|30d,11,'+hextime()+',E,10905.6297,N,3415.61818,0,10,c,1,1,-1,79|)'
    t1.insert(END,timeinfo)
    t1.update()

def mr():
    e3.delete(0,END)
    e4.delete(0,END)
    e3.insert(END,2103)
    e4.insert(END,'192.168.6.52')

b1=Button(root,text='上线',command=sx)
b2=Button(root,text='绑定',command=Btbd)
b3=Button(root,text='能力',command=fz)
b4=Button(root,text='设防',command=sf)
b5=Button(root,text='发送',command=send)
b6=Button(root,text='清空',command=qk1)
b7=Button(root,text='清空',command=qk2)
b8=Button(root,text='引擎')
b9=Button(root,text='门锁')
b10=Button(root,text='电压')
b11=Button(root,text='温度')
b12=Button(root,text='GSM')
b13=Button(root,text='星数')
b14=Button(root,text='设备位置',command=sbwz,width=10)
b15=Button(root,text='默认',command=mr)

b8.bind("<Button-1>", showpic)
b9.bind("<Button-1>", showpic)
b10.bind("<Button-1>", showpic)
b11.bind("<Button-1>", showpic)
b12.bind("<Button-1>", showpic)
b13.bind("<Button-1>", showpic)

b1.grid(row=1,column=2)
b2.grid(row=2,column=2)
b3.grid(row=3,column=4)
b4.grid(row=3,column=5)
b5.grid(row=3,column=2)
b6.grid(row=3,column=1,sticky=E)
b7.grid(row=5,column=2)
b8.grid(row=0,column=4)
b9.grid(row=0,column=5)
b10.grid(row=1,column=4)
b11.grid(row=1,column=5)
b12.grid(row=2,column=4)
b13.grid(row=2,column=5)
b14.grid(row=4,column=4,columnspan=2,sticky=N)
b15.grid(row=0,column=2)

l1=Label(root,text='自定义输入界面:')
l1.grid(row=3,columnspan=2,sticky=W)
l2=Label(root,text='接收界面:')
l2.grid(row=5,columnspan=2,sticky=W)

t1=Text(root,width=34,height=5)
t1.grid(row=4,column=0,columnspan=3)
t2=Text(root,width=34,height=10)
t2.grid(row=6,column=0,columnspan=3)

mainloop()
