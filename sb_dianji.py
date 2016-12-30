# coding=utf8
'''
'''
import sys
import ttk
import time
import serial
import threading
import Tkinter as Tk
import Tkinter as tk
import tkMessageBox as alert
import serial.tools.list_ports
isOpened = threading.Event()

RBuf = ''
TBuf = '5603200012C000000000A7AA'

root = Tk.Tk()
ComX = Tk.StringVar(root, 'COM1')
dinyaX = Tk.StringVar(root, '0.8V')
Baud = Tk.StringVar(root, "9600")
Dbit = Tk.StringVar(root, '8')
Sbit = Tk.StringVar(root, '1')
Chck = Tk.StringVar(root, 'None')
Open = Tk.StringVar(root, u'打开串口')
sn_str = Tk.StringVar(root, u'')
Portlist = []

COM = serial.Serial()
def key_enter_action(event):
    print('你按下了: ' + event.char)

def main():
    #设置窗口
    root.title(u"爱其电机检测 v1.0.0")
    root.iconbitmap('aiqi.ico')
    root.resizable(False, False)

    #获取可用串口
    getComport()

    #设置菜单
    menubar = Tk.Menu(root)
    about = Tk.Menu(menubar, tearoff=0)
    about.add_command(label=u"关于软件", command=aboutus)
    about.add_command(label=u"退出", command=root.quit)
    menubar.add_cascade(label=u"关于", menu=about)
    root.config(menu=menubar)
    center_window(root, 600, 480) #设置窗口初始位置

    #打开串口操作
    serial = tk.Canvas(root, height=26, width=580)
    serial.pack(side='top', padx=0, pady=0, anchor='c')
    serial.create_window(30, 15, window=ttk.Label(root, text=u'串口号：'))
    serial.create_window(105, 15, window=ttk.Combobox(root, textvariable=ComX, values=Portlist, width=12))
    serial.create_window(202, 15, window=ttk.Label(root, text=u'波特率：'))
    serial.create_window(277, 15, window=ttk.Combobox(root, textvariable=Baud, values=['4800', '9600', '19200'], width=12))
    serial.create_window(387, 15, window=ttk.Button(root, textvariable=Open, width=12, command=lambda: COMOpen(serial)))
    serial.create_oval(450, 7, 466, 23, fill='black', tag='led')
    #serial.create_window(547, 15, window=ttk.Checkbutton(root, text=u'HEX发送', variable=HexO, onvalue=True, offvalue=False))

    # # 设置电压
    # dinya = tk.Canvas(root, height=26, width=580)
    # dinya.pack(side='top', padx=0, pady=20, anchor='c')
    # dinya.create_window(30, 15, window=ttk.Label(root, text=u'电压：'))
    # dinya.create_window(77, 15, window=ttk.Combobox(root, textvariable=dinyaX, values=['0.8V', '12V'], width=4))
    # dinya.create_window(90, 15, window=ttk.Button(root, textvariable=sendCheckMotorMessage, width=12, command=lambda: sendCheckMotorMessage(dinya)))

    # 发送报文内容
    #send = tk.Canvas(root, height=26, width=580)
    #send.pack(side='top', padx=0, pady=0, anchor='c')
    #send.create_window(30, 15, window=ttk.Label(root, text=u'指令：'))
    #send.create_window(191, 15, window=ttk.Entry(root, width=39))
    #send.create_window(387, 15, window=ttk.Button(root, text=u'发送', width=12))
    #send.create_window(472, 15, window=ttk.Button(root, text=u'清除', width=9))
    #send.create_window(547, 15, window=ttk.Checkbutton(root, text=u'HEX显示', variable=HexD, onvalue=True, offvalue=False))

    #扫码
    scan_code = tk.Canvas(root,height = 52,width=580)
    scan_code.pack(side='top', padx=0, pady=0, anchor='c')
    scan_code.create_window(30, 15, window=ttk.Label(root, text=u'电机SN：'))
    scan_code.create_window(191, 15, tag='sn',window=ttk.Entry(root, width=39,textvariable = sn_str))
    scan_code.tag_bind(root,'sn', '<Key>', key_enter_action)



    #设置奇偶校验等参数
    #cnv3 = tk.Canvas(root, height=26, width=580)
    #cnv3.pack(side='top', padx=0, pady=0, anchor='c')
    #cnv3.create_window(30, 15, window=ttk.Label(root, text=u'数据位：'))
    #cnv3.create_window(105, 15,
    #                 window=ttk.Combobox(root, textvariable=Dbit, values=['9', '8', '7', '6', '5'], width=12))
    #cnv3.create_window(202, 15, window=ttk.Label(root, text=u'停止位：'))
    #cnv3.create_window(277, 15, window=ttk.Combobox(root, textvariable=Sbit, values=['1', '2'], width=12))
    #cnv3.create_window(370, 15, window=ttk.Label(root, text=u'校验位：'))
    #cnv3.create_window(445, 15,
    #                   window=ttk.Combobox(root, textvariable=Chck, values=['None', 'Odd', 'Even', 'Mark', 'Space'],
    #                                      width=12))
    #cnv3.create_window(547, 15, window=ttk.Button(root, text=u'扩展', width=9))

    #内容显示窗口
    tips_lable = Tk.Text(root, width=90, border=2)
    tips_lable.pack(side='top', padx=3, pady=1, anchor='c')

    #底部信息
    bottom_tip = tk.Canvas(root, height=26, width=580)
    bottom_tip.pack(side='top', padx=0, pady=0, anchor='c')
    bottom_tip.create_window(450, 7, window=ttk.Label(root, text=u'IQI Technology Co., LTD. | 北京爱其科技有限公司'))

    com_thread = threading.Thread(target=COMTrce)
    com_thread.setDaemon(True)
    com_thread.start()
    root.bind("<<COMRxRdy>>", lambda e: tips_lable.insert("insert", RBuf))

    root.mainloop()

def sendCheckMotorMessage():
    return

def COMOpen(cnv2):
    print sn_str.get()
    return
    if not isOpened.isSet():
        try:
            COM.timeout = 1
            COM.xonxoff = 0
            COM.port = ComX.get()
            COM.parity = Chck.get()[0]
            COM.baudrate = int(Baud.get())
            COM.bytesize = int(Dbit.get())
            COM.stopbits = int(Sbit.get())
            COM.open()
        except Exception:
            #print "COM Open Error!"
            alert.showinfo(title=u'错误', message=u'端口打开失败，请确认端口是否被占用!')
        else:
            isOpened.set()
            Open.set(u'关闭串口')
            cnv2.itemconfig('led', fill='green')
    else:
        COM.close()
        isOpened.clear()
        Open.set(u'打开串口')
        cnv2.itemconfig('led', fill='black')


def COMTrce():
    while True:
        if isOpened.isSet():
            RBuf = COM.read(1)  # read one, with timout
            if RBuf:
                n = COM.inWaiting()
                if n:
                    RBuf = RBuf + COM.read(n)
                    root.event_generate("<<COMRxRdy>>")

            if len(TBuf) != 0:
                COM.write(TBuf)

            time.sleep(0.01)
        time.sleep(0.05)

#设置窗口居中
def center_window(root, width, height):
    screenwidth = root.winfo_screenwidth()
    screenheight = root.winfo_screenheight()
    size = '%dx%d+%d+%d' % (width, height, (screenwidth - width)/2, (screenheight - height)/2)
    #print(size)
    root.geometry(size)

def test():
    alert.showinfo(title=u'提示', message=u'提示!')

def aboutus():
    alert.showinfo(title=u'关于软件', message=u'版本号：V1.0.0\n\n北京爱其科技有限公司')

#获取可用串口
def getComport():
    plist = list(serial.tools.list_ports.comports())
    if len(plist) <= 0:
        alert.showinfo(title=u'错误', message=u'未找到可用串口，请退出程序重试')
    else:
        for index in range(len(plist)):
            Portlist.append(plist[index][0])


if __name__ == '__main__':
    isOpened.clear()
    main()

