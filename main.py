
from tkinter import *
from datetime import datetime
from tkinter import ttk
import socket
import pyodbc
import datetime

window = Tk()
window.title("PACKAGE")
window.geometry('1000x444')
global list
list=[]
global boardlist
boardlist = []
global cnt
cnt=0
global str1
def checksn(sn):

    server = '192.168.3.233'
    database = 'cultraview'
    username = 'sa'
    password = 'Ctv@123'
    cnxn = pyodbc.connect(
        'DRIVER={SQL Server};SERVER=' + server + ';DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
    cursor = cnxn.cursor()
    cursor1 = cnxn.cursor()
    requestString2 = """SELECT RESULT FROM [cultraview].[dbo].[TEST_PASS_2021_ss] WHERE [PCB_SN] = 'gg'"""
    requestString3 = """SELECT RESULT FROM [cultraview].[dbo].[TEST_PASS_2021_ss] WHERE [PCB_SN] = 'gg'"""
    requestString2 = requestString2.replace("gg", str(sn))
    requestString3 = requestString3.replace("gg", str(sn))
    datenow = datetime.datetime.now()
    now = datenow.month
    now2 = int(now) - 1
    now = str(now)
    if len(now) == 1:
        now = '0' + now
    now2 = str(now2)
    if len(now2) == 1:
        now2 = '0' + now2
    # print(now, now2)
    if len(now2) == 1:
        now2 = '0' + now2
    requestString2 = requestString2.replace("ss", str(now))
    requestString3 = requestString3.replace("ss", str(now2))
    cursor.execute(requestString2)
    row = cursor.fetchall()

    cursor1.execute(requestString3)
    row1 = cursor1.fetchall()
    # print(now, now2)
    if len(row) == 1 or len(row1) == 1:
        return True
    else:
        return False
def entr1(event):
    qtyboard()
    txt0.focus()
    txt0.bind('<Return>', entr2)

def entr2(event):
    boardname()
    txt.focus()
    txt.bind('<Return>', entr3)
def entr3(event):
    init()
    txt1.focus()
    txt1.bind('<Return>', entr4)
def entr4(event):
    boards()
    txt1.focus()
    txt1.delete(0, END)

def boardname():
    global boardn
    boardn = format(txt0.get())
    lbl0.configure(text=boardn, font='Times 25')
    txt.focus()

def init():
    global operator
    operator = format(txt.get())
    txt1.focus()
    numberbox = open("Z:/SMT/package/numbox.txt")
    box = numberbox.readline()
    box = int(box)
    lbl.configure(text=operator, font='Times 25')
    lbl2.configure(text=box, font='Times 25')

def qtyboard():
    global qtyb
    qtyb = format(qtyboardtxt.get())
    qtyb=int(qtyb)
    qtylbl.configure(text=qtyb, font='Times 25')

def reset():
    boardlist.clear()
    lbl1.configure(text=len(boardlist), font='Times 25')
    window["bg"] = "gray93"
    txt1.delete(0, END)
    txt1.focus()
    lbl5.configure(text="", font='Times 25', bg="red", fg='black')

def boards():
    if (format(txt1.get()) in boardlist)==True:
        window["bg"] = "purple"
    else:
        if format(txt1.get()) == "reset":
            reset()
        if len(boardlist) > qtyb:
            window["bg"] = "blue"
        if len(boardlist) == qtyb-1:
            window["bg"] = "yellow"
            lbl5.configure(text="КОРОБКА ЗАПОЛНЕНА!!!", font='Times 25', bg="Black", fg='red')
        if format(txt1.get()) == "closebox":
            lbl5.configure(text="", font='Times 25', bg="Black", fg='red')
            str1 = ' '
            for i in range(len(boardlist)):
                str1=str1+" "+boardlist[i]
                # print(str1)
                tistamp = str(datetime.datetime.now())
                f = open("Z:/SMT/package/pack.txt", "a")
                numberbox = open("Z:/SMT/package/numbox.txt")
                box = numberbox.readline()
                f.write(boardlist[i]+' '+operator+' '+tistamp+' '+box+'\n')
            numberbox = open("Z:/SMT/package/numbox.txt")
            box = numberbox.readline()
            box = int(box)
            f = open('Z:/SMT/package/numbox.txt', 'w')
            f.close()
            boxstr2=str(box)
            box += 1
            boxstr = str(box)
            f = open('Z:/SMT/package/numbox.txt', 'w')
            f.write(boxstr)
            f.close()
            lbl2.configure(text=box, font='Times 25')
            lbl1.configure(text=len(boardlist), font='Times 25')
            txt1.delete(0, END)
            compBK1 = """^XA^FO^FS^FO100,0^A0N,55,50^FD User:operator ^FS^FO  100,100^A0N,55,50^FD BoxNo:strbox ^FS^FO^FS^FO  100,145^A0N,55,50^FD Date:time ^FS^FO ^FS^FO  100,190^A0N,55,50^FD QTY:kol ^FS^FO^FS^FO 100,50^A0N,55,50^FD Model:strboard ^FS^FO^FO120,250^BQN,4,4^FDsss^FS^ ^XZ"""
            compBK1 = compBK1.replace("operator", operator[0:9])
            # compBK1 = compBK1.replace("tistamp", tistamp[0:6])
            compBK1 = compBK1.replace("strbox", boxstr2)
            compBK1 = compBK1.replace("strboard", boardn)
            tistamp = str(datetime.datetime.now())
            compBK1 = compBK1.replace("time", tistamp[0:16])
            compBK1 = compBK1.replace("kol", str(len(boardlist)))

            compBK1 = compBK1.replace("sss", str1)
            mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            host = "192.168.0.159"
            port = 9100
            str1=" "
            boardlist.clear()
            window["bg"] = "gray93"
            try:
                mysocket.connect((host, port))  # connecting to host
                mysocket.send(compBK1.encode())  # using bytes
                mysocket.close()  # closing connection
            except:
                print("Error with the connection")
        else:

            if checksn(format(txt1.get())) == True:
                if len(boardlist)!=qtyb-1:
                    window["bg"] = "gray93"
                if len(boardlist)>=qtyb:
                    window["bg"] = "blue"
                    lbl5.configure(text="КОРОБКА ПЕРЕПОЛНЕНА!!!", font='Times 25', bg="red", fg='black')
                boardlist.append(format(txt1.get()))
                lbl1.configure(text=len(boardlist), font='Times 25')
                txt1.delete(0, END)
                txt1.focus()
            else:
                window["bg"] = "red"
                txt1.delete(0, END)
                txt1.focus()


qtylbl = Label(window, font='Times 25', text="КОЛИЧЕСТВО В КОРОБКЕ")
qtylbl.grid(column=3, row=0)
lbl0 = Label(window, font='Times 25', text="МОДЕЛЬ ПЛАТЫ")
lbl0.grid(column=3, row=1)
lbl = Label(window, font='Times 25', text="УПАКОВЩИК")
lbl.grid(column=3, row=2)
lbl1 = Label(window, font='Times 25', text="СЕРИЙНИК ПЛАТЫ")
lbl1.grid(column=3, row=3)
lbl2 = Label(window, font='Times 25', text="НОМЕР КОРОБКИ")
lbl2.grid(column=1, row=4)
lbl5 = Label(window, font='Times 25', text="")
lbl5.grid(column=1, row=5)

qtyboardtxt = Entry(window, font='Times 25', width=20)
qtyboardtxt.grid(column=1, row=0)
txt0 = Entry(window, font='Times 25', width=20)
txt0.grid(column=1, row=1)
txt = Entry(window, font='Times 25', width=20)
txt.grid(column=1, row=2)
qtyboardtxt.focus()
qtyboardtxt.bind('<Return>', entr1)
txt1 = Entry(window, font='Times 25', width=20)
txt1.grid(column=1, row=3)

qtybtn = Button(window, text="go",font='Times 25', command=qtyboard)
qtybtn.grid(column=2, row=0)
btn0 = Button(window, text="go",font='Times 25', command=boardname)
btn0.grid(column=2, row=1)
btn = Button(window, text="go",font='Times 25', command=init)
btn.grid(column=2, row=2)
btn1 = Button(window, text="go",font='Times 25', command=boards)
btn1.grid(column=2, row=3)
btn1 = Button(window, text="reset",font='Times 25', command=reset)
btn1.grid(column=5, row=7)


window.mainloop()
