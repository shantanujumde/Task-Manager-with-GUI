from tkinter import *
from tkcalendar import Calendar, DateEntry
from functools import partial  
from datetime import datetime
from threading import Timer
#notification
def notification(name,duration):
    import time
    Label(root, text=f'Upcoming Event: {name},\nTime Remaining(s): {duration}').grid(row=4 ,pady=30 ,column=0)
    t = Timer(duration, playSound)
    t.start() 
    
def playSound():
    from playsound import playsound
    from win10toast import ToastNotifier
    playsound('[location]\\src\\1.wav')
    toaster = ToastNotifier()
    toaster.show_toast("Task Manager","Its Time to Do Your Work",icon_path="[location]\\src\\icon.ico",
    duration=10)
    import time
    while toaster.notification_active():
        time.sleep(0.1)


#time Calculator
def timeCalculator(date,time):
    dt = date.split('/')
    tm = time.split(':')
    remTime = datetime(2020, int(dt[1]), int(dt[0]), int(tm[0]), int(tm[1]), 0)
    notify = remTime - datetime.now()
    return notify.total_seconds()

#Add Tasks
def addTask(name,date,time):
    name=name.get()
    date=date.get()
    time=time.get()
    f = open('[location]\\tasks\\task.txt','a')
    try:
        timeCalculator(date,time)
        if '/' not in date and ':' not in time:
            print('Invalid Format')
            Label(root,text= "(!) Invalid Entry" ,justify=RIGHT,bg='white',fg='#fc0324').grid(row=3, column=4)
        else:
            dt=date.split('/')
            dt[0] = int(dt[0])
            dt[1] = int(dt[1])
            tm=time.split(':')
            tm[0] = int(tm[0])
            tm[1] = int(tm[1])
            
            if dt[0]>0 and dt[0]<=31 and dt[1]>0 and dt[1]<=12 and tm[0]>0 and tm[0]<=24 and tm[1]>0 and tm[1]<=59 and timeCalculator(date,time)>0:
                f.write(f'{name}\n')
                f.write(f'{date}\n')
                f.write(f'{time}\n^_^')
                f.close()
                print('\nEntry Added')
                showTask()
            elif timeCalculator(date,time)<0:
                Label(root,text= "(!) Time Already Passed" ,justify=RIGHT,bg='white',fg='#fc0324').grid(row=3, column=4)
            else:
                print('Invalid Format')
                Label(root,text= "(!) Invalid Entry" ,justify=RIGHT,bg='white',fg='#fc0324').grid(row=3, column=4)
    except:
        Label(root,text= "(!) Invalid Entry" ,justify=RIGHT,bg='white',fg='#fc0324').grid(row=3, column=4)

#delete task
def deltContent(val):
    print(val)
    f = open('[location]\\tasks\\task.txt','r')
    tmp = f.read()
    lst=tmp.split('^_^')
    print('\nlst\n',lst)
    lst.remove('')
    f.close()
    f = open('[location]\\tasks\\task.txt','w')
    for i in range(len(lst)):
        if lst[i]==val:
            lst[i]=''
        else:
            f.write(lst[i]+'^_^')

    showTask()


root = Tk()
timeImg = PhotoImage(file="[location]\\src\\backG.png")
Label(root, image=timeImg).place(x=0, y=0, relwidth=1, relheight=1)


root.title('Task Manager')
root.geometry("1200x500+200+200")

root.iconbitmap('D:\\Aabhyas\\Python\\OOP with python\\TASKMANAGER\\src\\icon.ico')
mb = Menu(root)
root.config(menu=mb)
tm = Menu(mb)
mb.add_cascade(label='Taks',menu=tm)  #Taks
mb.add_cascade(label='Edit',menu=tm)  #Edit



# Add
name = StringVar()
date = StringVar()
time = StringVar()

#placeholder for e1
def on_clicke1(event):
    e1.configure(state=NORMAL)
    e1.delete(0, END)
    e1.unbind('<Button-1>', on_click_id1)
def on_clicke2(event):
    e2.configure(state=NORMAL)
    e2.delete(0, END)
    e2.unbind('<Button-1>', on_click_id2)
def on_clicke3(event):
    e3.configure(state=NORMAL)
    e3.delete(0, END)
    e3.unbind('<Button-1>', on_click_id3)

Label(root, text="Event Name").grid(row=1)
e1=Entry(root,textvariable = name)
e1.insert(0, 'Enter Name')
e1.grid(row=1,column=1)
e1.configure(state=DISABLED)
on_click_id1 = e1.bind('<Button-1>', on_clicke1)

Label(root, text="Event Date(DD/MM)").grid(row=2)
e2=Entry(root,textvariable = date)
e2.insert(0, ' Date (DD/MM)')
e2.grid(row=2,column=1)
e2.configure(state=DISABLED)
on_click_id2 = e2.bind('<Button-1>', on_clicke2)

Label(root, text="Event Time(HH:mm)").grid(row=3)
e3=Entry(root,textvariable = time)
e3.insert(0, 'Time(HH:mm),24 hour')
e3.grid(row=3,column=1)
e3.configure(state=DISABLED)
on_click_id3 = e3.bind('<Button-1>', on_clicke3)

add = PhotoImage(file="[location]\\src\\add.png")
add = add.subsample(15,19)
addTask = partial(addTask,name,date,time)
Button(root,image=add,text='Add \nTask',compound="left",command=addTask).grid(row=0, column=3,rowspan=4,padx=20,pady=2)
# Button(root,text='Refresh',compound="left",command=showTask).grid(row=0, column=4,padx=4)


# can.create_rectangle(30,2, 580,50, fill="grey")
#Show Tasks
def showTask():
    frme=Frame(root,width=600, height=400)
    scroll = Scrollbar(frme,orient=VERTICAL)
    w = Canvas(frme, width=600, height=400,bg='#72e87a',yscrollcommand=scroll.set)
    scroll.config(command=w.yview)
    scroll.pack(fill=Y,side=RIGHT)
    frme.grid(row=5,pady=0,column=4)
    w.pack()
    
    f= open('[location]\\tasks\\task.txt','r')
    data = f.read()
    lst = data.split('^_^')
    name=[]
    date=[]
    time=[]
    for i in range(len(lst)-1):
        tmp = lst[i].split("\n")
        name.append(tmp[0])
        date.append(tmp[1])
        time.append(tmp[2])
        tmp.clear()

    rect=0
    ylabel=0
    delt = PhotoImage(file="[location]\\src\\delt.png")
    delt = delt.subsample(7,7)
    
    for i in range(len(name)):
        w.create_rectangle(30,2+rect, 580,50+rect, fill="#adfffb")
        l1=Label(w,text= "Name: "+name[i] ,justify=RIGHT,bg='#adfffb')
        l2=Label(w,text= "Date: "+date[i] ,justify=RIGHT,bg='#adfffb')
        l3=Label(w,text= "Time: "+time[i] ,justify=RIGHT,bg='#adfffb')
        if round(((timeCalculator(date[i],time[i]))/60),2)>0:
            l4=Label(w,text= f"Time Remaining: {round(timeCalculator(date[i],time[i])/3600,2)} hours" ,justify=RIGHT,bg='#adfffb')
        else:
            l4=Label(w,text= f"Task Completed" ,justify=RIGHT,bg='#adfffb')
        b1=Button(w,text='Delete',height=1,command=(lambda: deltContent(f"{name[i]}\n{date[i]}\n{time[i]}\n")))
        w.create_window(80,15+ylabel,window=l1)
        w.create_window(80,35+ylabel,window=l2)
        w.create_window(300,15+ylabel,window=l3)
        w.create_window(300,35+ylabel,window=l4)
        w.create_window(500,20+ylabel,window=b1)
        rect+=50
        ylabel+=50
    
showTask()
Label(root, text='Clock is Ticking',bg='yellow' ,font=("Helvetica", 26)).grid(row=5,padx=50)
# root.create_window(200,0,window=l5)
def upComingEvent():
    f= open('[location]\\tasks\\task.txt','r')
    data = f.read()
    lst = data.split('^_^')
    name=[]
    date=[]
    time=[]
    for i in range(len(lst)-1):
        tmp = lst[i].split("\n")
        name.append(tmp[0])
        date.append(tmp[1])
        time.append(tmp[2])
        tmp.clear()
    rem=[]
    for i in range(len(time)):
        rem.append(timeCalculator(date[i],time[i]))
    try:
        min(i for i in rem if i > 0)
        m = min(i for i in rem if i > 0)
        notification(name[rem.index(m)],rem[rem.index(m)])
    except:
        Label(root, text=f'All tasks are Completed',pady=40,padx=20).grid(row=4, column=0)


#tools Canvas
can = Canvas(root,bg='#00610b', width=600, height=50)
can.grid(row=4,column=4,pady=5)
event=Label(can,text= "Tools: " ,justify=RIGHT)
can.create_window(25,15,window=event)

refresh = PhotoImage(file="[location]\\src\\refresh.png")
ref = refresh.subsample(15,19)
btn1 = Button(can,image=ref,borderwidth=0,compound="left",command=showTask, bg='black')
can.create_window(105,20,window=btn1)
btn2=Button(root,text='Start',borderwidth=0,compound="left",command=upComingEvent,padx=10,pady=4)
can.create_window(180,20,window=btn2)
root.mainloop()
