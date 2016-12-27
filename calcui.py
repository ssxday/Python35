# -*- coding:utf-8 -*-
import tkinter,math
class MyButton:
    def __init__(self,root):
        btn = tkinter.Button(root,
                             width=8,
                             height=8,
                             bg='red',
                             fg='green',
                             text='55555555',
                             )
        btn.pack()
    pass

class MyLabel:
    pass

class MyMessage:
    pass

root = tkinter.Tk(screenName='myscreen',
                  className='myCalculator',
                  )
# cvs = tkinter.Canvas(root,
#                      width=400,
#                      height=660)
# cvs.pack()

MyButton(root)



root.mainloop()
