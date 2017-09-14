#/usr/bin/python
#coding=utf-8
#creat by 15025463191 2017/07/03

from tkinter import *
from tkinter import ttk
import requests
import time
import os
import pickle
import pymssql
import random
import string

isexisted=os.path.exists('D:\Interfacetemp')
if not isexisted:
    os.makedirs('D:\Interfacetemp')
else:pass

isexisted=os.path.exists('D:\Interfacetemp\data.txt')
if not isexisted:
    data=open('D:\Interfacetemp\data.txt',"wb")
    history_dic={
    'input1':'',
    'input2':'',
    'customerUserName':'',
    'customerPhone':''
}

    pickle.dump(history_dic,data,True)
    data.close()
else:pass

s = requests.Session()
def get():
    r=s.get('http://'+e1.get()+e2.get(),params=createPayload())
    t1.insert(END,r.text)

def qk1():
    u'清空'
    t1.delete('0.0',END)

def createPayload():
    a=e3.get()
    b=e4.get()
    keys=a.split(',')
    values=b.split(',')
    payload=dict(zip(keys,values))
    return payload

def go():
    # if combox.get()==u'思锐注册':
    #     payload={
    #         'vehicleMode':100,
    #         'imei':E1.get(),
    #         'customerUserName':E2.get(),
    #         'customerPhone':E2.get(),
    #         'customerPassword':'Wg123456',
    #         'withEncrypt':0
    #     }
    #     interface='/basic/customer/register'
    # else:pass
    payload=t2.get('0.0',END)
    payload_list=payload.split('\n')
    payload_dic={}
    lenth=len(payload_list)-1
    for i in range(lenth):
        pload_split=payload_list[i].split(':')
        payload_dic[pload_split[0]]=pload_split[1]

    if e1.get()=='':
        t1.insert(END,'请输入域名')
    else:
        r=s.get('http://'+e1.get()+e2.get(),params=payload_dic)
        print r.cookies
        t1.insert(END,r.text)

def srzc():
    u'思锐注册'
    t2.delete('0.0',END)
    payload="" \
        "imei:\n" \
        "customerUserName:"+e5.get()+"\n" \
        "customerPhone:"+e8.get()+"\n" \
        "customerPassword:123456\n" \
        "vehicleMode:100\n" \
        "withEncrypt:0"
    t2.insert(END,payload)
    e2.delete('0',END)
    e2.insert(END,'/basic/customer/register')

    #缓存
    data=open('D:\Interfacetemp\data.txt',"rb")
    history_dic=pickle.load(data)
    data.close()
    history_dic['customerUserName']=e5.get()
    history_dic['customerPhone']=e8.get()
    data=open('D:\Interfacetemp\data.txt',"wb")
    pickle.dump(history_dic,data,True)
    data.close()

def sbbd():
    u'设备绑定'
    t2.delete('0.0',END)

    customername=e5.get()
    conn=pymssql.connect(host='192.168.6.51',user='sa',password='test2017')
    cur=conn.cursor()
    cur.execute("SELECT CustomerID FROM [sirui].[dbo].[Customer]where UserName=\'"+customername+"\';")
    info = cur.fetchall()
    customerID = str(info)[2:-3]
    cur.execute("SELECT VehicleID FROM [sirui].[dbo].[Vehicle]where CustomerID=\'"+customerID+"\';")
    info = cur.fetchall()
    VehicleID = str(info)[2:-3]

    if v1.get()==1:
        app='sr'
        version='5.1.0'
    elif v2.get()==1 and v1.get()==0:
        app='miz'
        version='1.21'
    else:
        app=''
        version=''
    payload="" \
        "imei:\n" \
        "version:"+version+"\n" \
        "app:"+app+"\n" \
        "vehicleID:"+VehicleID+"\n" \
        "input1:"+e6.get()+"\n" \
        "input2:"+e7.get()
    t2.insert(END,payload)
    e2.delete('0',END)
    e2.insert(END,'/basic/car/changeDevice')

    #缓存
    data=open('D:\Interfacetemp\data.txt',"rb")
    history_dic=pickle.load(data)
    data.close()
    history_dic['customerUserName']=e5.get()
    history_dic['input1']=e6.get()
    history_dic['input2']=e7.get()
    data=open('D:\Interfacetemp\data.txt',"wb")
    pickle.dump(history_dic,data,True)
    data.close()

def tjcl():
    u'添加车辆'
    t2.delete('0.0',END)
    if v1.get()==1:
        app='sr'
        version='5.1.0'
    elif v2.get()==1 and v1.get()==0:
        app='miz'
        version='1.21'
    else:
        app=''
        version=''
    payload="" \
        "imei:\n" \
        "version:"+version+"\n" \
        "app:"+app+"\n" \
        "vehicleModelID:26954\n" \
        "version:5.1.0\n" \
        "input1:"+e6.get()+"\n" \
        "input2:"+e7.get()

    t2.insert(END,payload)
    e2.delete('0',END)
    e2.insert(END,'/basic/customer/bindTerminal')

    #缓存
    data=open('D:\Interfacetemp\data.txt',"rb")
    history_dic=pickle.load(data)
    data.close()
    history_dic['input1']=e6.get()
    history_dic['input2']=e7.get()
    data=open('D:\Interfacetemp\data.txt',"wb")
    pickle.dump(history_dic,data,True)
    data.close()

def mzhzc():
    u'咪智汇注册'
    t2.delete('0.0',END)
    r=s.get('http://'+e1.get()+'/provider/testProvide/sendAuthCode?phone='+e8.get())
    authinfo=r.text
    t1.insert(END,authinfo)
    print r.cookies
    authcode=authinfo[23:27]
    payload="" \
        "customerUserName:"+e5.get()+"\n" \
        "customerPhone:"+e8.get()+"\n" \
        "customerPassword:123456\n" \
        "authcode:"+authcode \

    t2.insert(END,payload)
    e2.delete('0',END)
    e2.insert(END,'/basic/customer/registerCustomer')

    #缓存
    data=open('D:\Interfacetemp\data.txt',"rb")
    history_dic=pickle.load(data)
    data.close()
    history_dic['customerUserName']=e5.get()
    history_dic['customerPhone']=e8.get()
    data=open('D:\Interfacetemp\data.txt',"wb")
    pickle.dump(history_dic,data,True)
    data.close()

root = Tk()
root.title('接口测试定制 version:2017.7.7')

Label(root, text="域名").grid(row=0,sticky=W)
Label(root, text="接口").grid(row=1,sticky=W)
Label(root, text="字段").grid(row=2,sticky=W)
Label(root, text="参数").grid(row=2,column=2,sticky=W)
Label(root, text="响应内容").grid(row=3,columnspan=2,sticky=W)
# Label(root,bg='#87CEEB',width=10,height=1).grid(row=5,columnspan=7,pady=0)
Label(root, text="常用接口测试:").grid(row=5,columnspan=2,sticky=W)
Label(root, text="用户名").grid(row=6,columnspan=2,sticky=W)
Label(root, text="手机号").grid(row=7,columnspan=2,sticky=W)
Label(root, text="input1").grid(row=8,columnspan=2,sticky=W)
Label(root, text="input2").grid(row=9,columnspan=2,sticky=W)
Label(root, text="最终推送的字段和参数值:").grid(row=10,columnspan=2,sticky=W)

e1 = Entry(root,width=56)
e2 = Entry(root,width=56)
e3 = Entry(root,width=25)
e4 = Entry(root,width=25)
e5 = Entry(root,width=54)
e6 = Entry(root,width=54)
e7 = Entry(root,width=54)
e8 = Entry(root,width=54)

e1.insert(END,'192.168.6.52:8080')
e1.grid(row=0,column=1,columnspan=4,sticky=W)
e2.grid(row=1,column=1,columnspan=4,sticky=W)
e3.grid(row=2,column=1,sticky=W)
e4.grid(row=2,column=4,sticky=W)
e5.grid(row=6,column=1,columnspan=4,sticky=E)
e6.grid(row=8,column=1,columnspan=4,sticky=E)
e7.grid(row=9,column=1,columnspan=4,sticky=E)
e8.grid(row=7,column=1,columnspan=4,sticky=E)

t1=Text(root,width=60,height=16)
t2=Text(root,width=60,height=7)
t1.grid(row=4,columnspan=5)
t2.grid(row=11,columnspan=5)

b1=Button(root,text='请求',command=get,bg='#87CEEB',width=7)
b2=Button(root,text='清空',command=qk1,width=8)
b3=Button(root,text='Go!',command=go,bg='#87CEEB',width=10)
# b4=Button(root,text='思锐注册',command=srzc,width=10)
# b5=Button(root,text='绑定更换',command=sbbd,width=10)
# b6=Button(root,text='添加车辆',command=tjcl,width=10)
# b7=Button(root,text='咪智汇注册',command=mzhzc,width=10)
b1.grid(row=3,column=4,sticky=E)
b2.grid(row=3,column=4)
b3.grid(row=10,column=4,sticky=E)
# b4.grid(row=10,column=5,columnspan=2,sticky=N)
# b5.grid(row=10,column=5,columnspan=2)
# b6.grid(row=10,column=5,columnspan=2,sticky=S)
# b7.grid(row=9,column=5)

data=open('D:\Interfacetemp\data.txt',"rb")
history_dic=pickle.load(data) #读取缓存文件data
data.close()

e5.insert(END,history_dic['customerUserName'])
e6.insert(END,history_dic['input1'])
e7.insert(END,history_dic['input2'])
e8.insert(END,history_dic['customerPhone'])

#下拉被注释
# L1=Label(root, text="IMEI")
# L2=Label(root, text="手机")
# L3=Label(root, text="")
# L4=Label(root, text="")
# L1.grid(row=7,sticky=W)
# L2.grid(row=8,sticky=W)
# L3.grid(row=9,sticky=W)
# L4.grid(row=10,sticky=W)
# E1=Entry(root)
# E2=Entry(root)
# E3=Entry(root)
# E4=Entry(root)
# E1.grid(row=7,column=1,sticky=W)
# E2.grid(row=8,column=1,sticky=W)
# E3.grid(row=9,column=1,sticky=W)
# E4.grid(row=10,column=1,sticky=W)
#
def action(*args):
    if combox.get()==u'思锐注册':
        srzc()
    elif combox.get()==u'咪智汇注册':
        mzhzc()
    elif combox.get()==u'绑定更换':
        sbbd()
    elif combox.get()==u'添加车辆':
        tjcl()
    else:pass

combox=ttk.Combobox(root,width=11)
combox['values'] = (u'思锐注册',u'咪智汇注册', u'绑定更换',u'添加车辆')
combox["state"] = "readonly"
# combox.current(0) #设置默认
combox.bind("<<ComboboxSelected>>", action)
combox.grid(row=10,column=3,columnspan=2,sticky=W)

def pbsr():
    if v2.get()==1:
        c1['state']=DISABLED
    else:
        c1['state']=NORMAL
    # elif v2.get()==0:
    #     c1['state']=NORMAL
    # elif v1.get()==1:
    #     c2['state']=DISABLED
    # else:
    #     c2['state']=NORMAL

def pbmiz():
    if v1.get()==1:
        c2['state']=DISABLED
    else:
        c2['state']=NORMAL

v1=IntVar()
v2=IntVar()
c1=Checkbutton(root,text='思锐',command=pbmiz,variable=v1)
c2=Checkbutton(root,text='咪智汇',command=pbsr,variable=v2)
c1.grid(row=5,column=4,sticky=W)
c2.grid(row=5,column=4,sticky=E)

mainloop()

