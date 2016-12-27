# -*- coding:utf-8 -*-
import tkinter
help(tkinter.Canvas.create_image)
root = tkinter.Tk('screenname', 'mybase', 'my_window')
# 菜单
mnu = tkinter.Menu(root)
submn = tkinter.Menu(mnu, tearoff=0)
submn.add_command(label='Open')
submn.add_command(label='Save')
submn.add_command(label='Close')
mnu.add_cascade(label='File', menu=submn)

submn = tkinter.Menu(mnu, tearoff=0)
submn.add_command(label='Copy')
submn.add_command(label='Cut')
submn.add_command(label='Paste')
mnu.add_cascade(label='Edit', menu=submn)

root.config(menu=mnu)
# 弹出式菜单 pop-up-menu
popup = tkinter.Menu(root,tearoff=0)
popup.add_command(label='strip')
popup.add_command(label='rub')
popup.add_separator()
popup.add_command(label='fuck')

def ppmenu(event):
    popup.post(event.x_root, event.y_root)

# root.bind('<Button-1>',ppmenu)
myimg = tkinter.PhotoImage(file='./overall/PoweredByMacOSX.gif')

# 标签
label = tkinter.Label(root,
                      text='我去年买了\n个表',
                      anchor=tkinter.NW,
                      width=200,
                      height=50,  # 上下都各有一个height
                      bg='green',
                      fg='white',
                      justify=tkinter.LEFT,
                      image=myimg  # 有了图，字就没有了
                      )
label.pack()
# 按钮
button1 = tkinter.Button(root,
                         text='buttonone',
                         anchor=tkinter.E,  # 无效
                         width=20,
                         height=1,  # 无效,成了上下间距
                         )
button1.pack()

button2 = tkinter.Button(root,
                         text='buttontwo',
                         background='blue',  # 无效
                         font='times',
                         foreground='yellow',  # 无效
                         )
button2.pack()
# 文本框
entry1 = tkinter.Entry(root,
                       bg='red',
                       fg='white',
                       show='$',
                       # state=tkinter.DISABLED
                       )
entry1.pack()

entry2 = tkinter.Entry(root,
                       selectbackground='#cbc',
                       selectforeground='red',
                       width=10,
                       font='helvetica'
                       )
entry2.pack()

# 单选框与多选框 variable参数是关键
r = tkinter.StringVar()
r.set('2')
rdbtn = tkinter.Radiobutton(root,
                            text='单选1',
                            variable=r,
                            value='1',
                            indicatoron=0,  # OS X无效
                            )
rdbtn.pack()
rdbtn = tkinter.Radiobutton(root,
                            text='单选2',
                            variable=r,
                            value='2',
                            indicatoron=0,  # 无效
                            )
rdbtn.pack()
rdbtn = tkinter.Radiobutton(root,
                            text='单选3',
                            variable=r,
                            value='3',
                            indicatoron=0,  # 无效
                            )
rdbtn.pack()

c = tkinter.IntVar()
c.set(1)
chkbn = tkinter.Checkbutton(root,
                            variable=c,
                            onvalue=1,
                            offvalue=5,
                            text='多选框',
                            indicatoron="0",  # 无效
                            )
chkbn.pack()

# 文本框
txtx = tkinter.Text(root,
                    width=20,
                    height=5,  # 有，但是不准
                    selectbackground='red',
                    selectforeground='green',
                    font='helvetica'
                    )
txtx.pack()

# 画布Canvas
cvs = tkinter.Canvas(root,
                     width=300,
                     height=400,
                     bg='#ccc',
                     )
# cvs.create_image(50,50,image=myimg)
cvs.create_text(150,20,
                text='hello, asshole',
                fill='red',  # Canvas中创建文字的颜色用fill
                )

cvs.create_polygon(70,50,150,50,
                   200,100,150,150,
                   70,150,40,100,
                   fill='yellow')
cvs.create_oval(70,200,150,300,
                fill='white')
cvs.create_line(70,200,150,300)
# cvs.create_line(70,300,200,400)
cvs.create_arc(50,300,250,500,
               start=30,
               extent=60,
               fill='pink'
               )
cvs.pack()

# 对话框
import tkinter.messagebox
tkinter.messagebox.showerror('这是title','myquestion')
# import tkinter.colorchooser
# mycolor = tkinter.colorchooser.askcolor()
# import tkinter.filedialog
# url = tkinter.filedialog.askopenfiles()
# print(mycolor)
# 滑块
scl = tkinter.Scale(root)
# scl.pack()
# 滚动条
scrb = tkinter.Scrollbar(root)
# scrb.pack()
# 列表框
libox = tkinter.Listbox(root)
# libox.pack()




root.mainloop()
# 输出单选，复选的variable
print(r.get())
print(c.get())