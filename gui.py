from tkinter import *
from time import sleep
root = Tk()
root.geometry('350x500')
root.title('test')
f1 = Frame(root)
# f1.place(relx=0.01, rely=0.05, relwidth=0.65, relheight=0.9)
text = Label(root, bg = '#85b4ff',font=('Courier',16), text = 'yeeeeaaaaahhhooooo')
text.place(relx = 0.01, rely=0.01,relwidth = 0.98, relheight=0.05)
lb = Listbox(root)
lb.insert(END,'first element')
lb.place(relx = 0.01, rely=0.065,relwidth = 0.98, relheight=0.74)
f1.place(relx = 0.01, rely=0.08,relwidth = 0.98, relheight=0.9)
msg = Message(f1,bg = '#85b4ff', anchor='w',width = 400, text=f'  hey there adasdf adsf asdasdasdasdaas asdasd!')
msg .place(relx = 0.02,relwidth = 0.98)
for i in range(20):
    ms = Message(f1,bg = '#85b4ff', anchor='w',width = 400, text=f'{i}  hey there adasdf adsf asdasdasdasdaas asdasd!')
    lb.insert(END,ms)
root.mainloop()




