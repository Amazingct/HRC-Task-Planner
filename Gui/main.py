import inspect
from tkinter import*
from tkinter import ttk
from tkinter import filedialog,messagebox
import numpy as np
import pandas as pd
import criterion as cr
global task, safety

# task = []
# safety = []

def openTasks():
    global task
    task = filedialog.askopenfilename(title = "Select a file")
    messagebox.showinfo("message", "Upload Successful")


def openSafety():
    global safety
    safety = filedialog.askopenfilename(title = "Select a file")
    messagebox.showinfo("message", "Upload Successful")


def default_file():
    global task, safety
    safety="safety.xlsx"
    task = "tasks.xlsx"
    
    cr.proceed(task,safety)

    
def alert(name):
    if name == "inspect":
        messagebox.showinfo("message", "download successful as inspect_result.csv")
    elif name == "repair":
        messagebox.showinfo("message", "download successful as repair_result.csv")

def clear_window(win):
    for widget in win.winfo_children():
        widget.destroy()

def homepage():
    def get_response():
        global index,actions_dict,response
        response = clicked.get()

        actions_dict = {}

        index = 23
        if response == "INSPECTION":
            label = [None]*100
            label[1] = Label(second_frame, text = "Task to performed")
            label[1].grid(row = 1, column = 0 ,sticky=W)
            for i in cr.inspect:
                    label[index] = Label(second_frame, text = str(index -1)+ ' '+i, wraplength=450, justify="left")
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    cr.actions.append(i)
            keys = [x for x in range(len(cr.actions))]
            actions_dict = dict(zip(keys,cr.actions))
            print(len(actions_dict))
            height_tank_s = Button(second_frame, text = "Proceed", command = lambda:[cr.first_criteria(actions_dict),second_proceed()]) #, command = get_val
            height_tank_s.grid(row =index, column = 1, pady = 4, padx = 2, sticky=W)
            print(len(actions_dict))


   
        elif response == "REPAIR":
            index = 2
            label = [None]*100
            label[1] = Label(second_frame, text = "Task to performed")
            label[1].grid(row = 1, column = 0 ,sticky=W)
            for i in cr.repair:
                    label[index] = Label(second_frame, text = str(index -1)+ ' '+i, wraplength=450, justify="left" )
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    cr.actions.append(i)
            keys = [x for x in range(len(cr.actions))]
            actions_dict = dict(zip(keys,cr.actions))
            print(len(actions_dict))
            height_tank_s = Button(second_frame, text = "Proceed", command = lambda:[cr.first_criteria(actions_dict),second_proceed()]) #, command = get_val
            height_tank_s.grid(row =index, column = 1, pady = 4, padx = 2, sticky=W)
            print(len(actions_dict))
        elif response == "INSPECTION+REPAIR":
            index = 2
            label = [None]*100
            label[1] = Label(second_frame, text = "Task to performed")
            label[1].grid(row = 1, column = 0 ,sticky=W)
            for i in cr.inspect:
                    label[index] = Label(second_frame, text = str(index -1)+ ' '+i, wraplength=450, justify="left")
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    cr.actions.append(i)
            for i in cr.repair:
                    label[index] = Label(second_frame, text = str(index -1)+ ' '+i, wraplength=450, justify="left")
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    cr.actions.append(i)
            keys = [x for x in range(len(cr.actions))]
            actions_dict = dict(zip(keys,cr.actions))
            print(len(actions_dict))
            height_tank_s = Button(second_frame, text = "Proceed", command = lambda:[cr.first_criteria(actions_dict),second_proceed()]) 
            height_tank_s.grid(row =index, column = 1, pady = 4, padx = 2, sticky=W)
            print(len(actions_dict))

    
    label = Label(second_frame, text= "Select Job to be performed")


    label.grid(row = 0, column = 0, padx = 50)


    options = ["INSPECTION","REPAIR", "INSPECTION+REPAIR"]

    clicked = StringVar()

    clicked.set("INSPECTION" )

    drop = OptionMenu(second_frame , clicked , *options )
    drop.config(width = 20)
    drop.grid(row = 0, column = 1)


    button = Button(second_frame , text = "submit"  , command = lambda :[clear_window(second_frame),get_response()]) #

    button.grid(row = 0, column = 2,sticky=W)
    print(clicked.get())

def second_proceed():
    def get_val():
        print(len(actions_dict))
        
        global height_human , height_tank
        
        height_human = height_human_e.get()
        height_tank  = height_tank_e.get()
        print(height_human, height_tank)
        cr.second_criteria(actions_dict,height_human,height_tank )
        print(cr.result)
        # third_criteria(actions_dict)
        
    clear_window(second_frame)
    result = cr.pre_second_criteria(actions_dict)
    print(result)
    if result == True:
        height_human_l = Label(second_frame, text = "Enter height of human")
        height_human_l.grid(row =1, column = 1, pady = 4)
        height_human_e = Entry(second_frame)
        height_human_e.grid(row =1, column = 2, pady = 4)
#                 height_human_s = Button(root, text = "Enter")
#                 height_human_s.grid(row =1, column = 3, pady = 4, padx = 2)
        height_tank_l = Label(second_frame, text = "Enter height of Robot")
        height_tank_l.grid(row =2, column = 1, pady = 4)
        height_tank_e = Entry(second_frame)
        height_tank_e.grid(row =2, column = 2, pady = 4)
        height_tank_s = Button(second_frame, text = "Enter", command = lambda:[get_val(), third_proceed() ]) #
        height_tank_s.grid(row =3, column = 1, pady = 4, padx = 2, sticky=W)
    elif result == False:
        third_proceed()
    
    print(len(actions_dict))
def third_proceed():
    clear_window(second_frame)
    cr.third_criteria(actions_dict)
    fourth_proceed()
def fourth_proceed():
    def get_values():
        global res
        res = []
        for i in clicked:
            res.append(i.get()) 
        print(res)

    label = [None]*100
    entry = [None]*100
    drop = [None]*100
    index = 2
    clicked = []
    values = []
    label[1] = Label(second_frame, text = "For Each task enter Enter 1 for, Collaborative task and 0 for otherwise")
    label[1].grid(row = 1, column = 1, sticky=W)
    for i in range(len(actions_dict)):
        var = StringVar(second_frame, "1")
        clicked.append(var)
        
    clicked =clicked[0:len(actions_dict)]
    val = {"Collaborative " : "1","Not Collaborative " : "2"}
    l = 0
    for i in actions_dict.items():
        label[index ] = Label(second_frame, text = i[1],  wraplength=450, justify="left")
#         label[index ].config(width = 80)
        label[index].grid(row = index, column = 1, sticky=W)
        j = 2
        for (text, value) in val.items():
            Radiobutton(second_frame, text = text, variable = clicked[l],
                value = value).grid(row = index, column=j)
            j = j+1
        l= l+1
            
        index = index +1

    button = Button(second_frame, text = "submit", command = lambda:[get_values(), cr.fourth_criteria(actions_dict, res), fifth_proceed() ])
    button.grid(row = index, column = 1)

def fifth_proceed():
    clear_window(second_frame)
    def get_values():
        global ress
        ress = []
        for i,j,k in zip(human_times,robot_times,choice):
            ress.append([i.get(), j.get(), k.get()])
        print(ress)
    label = [None]*100
    human_time = [None]*100
    human_times = []
    robot_time = [None]*100
    robot_times = []
    operating_cost = [None]*100
    operating_costs = []
    index = 2
    
    label[0] = Label( second_frame, text = "For each task enter time for human, time of robot and operating cost")
    label[0].grid(row = 0, column = 0)
    
    label[1] = Label(second_frame, text = "Task")
    label[1].grid(row = 1, column = 0)
    
    label[2] = Label(second_frame, text = "Time for human")
    label[2].grid(row = 1, column = 1, padx = 5)
    
    label[2] = Label(second_frame, text = "Time for robot")
    label[2].grid(row = 1, column = 2, padx = 5)
    
    label[2] = Label(second_frame, text = "Level Operating Cost")
    label[2].grid(row = 1, column = 3, padx = 5)
    costs = ["HIGH", "LOW", "MID"]
    choice = []
    for i in range(len(actions_dict)):
        var = StringVar(second_frame, "1")
        choice.append(var)
    
    
    l = 0
    for i in actions_dict.items():
        label[index] = Label(second_frame, text = i[1], wraplength=450, justify="left")
        label[index].grid(row = index, column = 0, sticky = W)
        human_time[index] = Entry(second_frame, width = 10)
        human_times.append(human_time[index] )
        human_time[index].grid(row = index, column = 1 )
        robot_time[index] = Entry(second_frame, width = 10)
        robot_times.append(robot_time[index] )
        robot_time[index].grid(row = index, column = 2 )
        choice[l].set("HIGH")
        operating_cost[index] = OptionMenu(second_frame, choice[l], *costs)
        operating_cost[index].config(width = 5)
        operating_costs.append(operating_cost[index] )
        operating_cost[index].grid(row = index, column = 3 )

        index = index +1
        l = l + 1
        
    Button(second_frame, text = "submit", command =lambda: [get_values(), cr.fifth_criteria(actions_dict,ress), sixth_proceed()]).grid(row = index, column = 2)
      

def sixth_proceed():
    global final_repair, final_inspect
    clear_window(second_frame)
    cr.sixth_criteria(actions_dict)
    final_repair, final_inspect = cr.get_result(cr.result,response)
    print(cr.result)
    display_result(response)


def display_result(name_task):
    
    index = 2
    Label(second_frame, text = "Task").grid(row =1, column = 0)
    Label(second_frame, text = "Assigned_to").grid(row =1, column = 1)
    Label(second_frame, text = "Reason").grid(row =1, column = 2)
    if name_task ==  "INSPECTION":
        Label(second_frame, text= response+" TASKS").grid(row=0, column=0, sticky=W)
        for i,j,k in zip(final_inspect["Task"], final_inspect["reason"],final_inspect["Assigned_to"]):
            Label(second_frame, text = i, wraplength=450, justify="left").grid(row=index, column=0, sticky=W)
            Label(second_frame, text = j,wraplength=300, justify="left").grid(row=index, column=1, sticky=W)
            Label(second_frame, text = k).grid(row=index, column=2, sticky=W)
            index = index + 1
    
        button = Button(second_frame, text="Download result", command= lambda:[cr.download_inspect(final_inspect),alert("inspect")]).grid(row = 3, column =4)
    if name_task == "REPAIR":
        Label(second_frame, text= response+" TASKS").grid(row=0, column=0, sticky=W)
        for i,j,k in zip(final_repair["Task"], final_repair["reason"],final_repair["Assigned_to"]):
            Label(second_frame, text = i, wraplength=450, justify="left").grid(row=index, column=0, sticky=W)
            Label(second_frame, text = j,wraplength=300, justify="left").grid(row=index, column=1, sticky=W)
            Label(second_frame, text = k).grid(row=index, column=2, sticky=W)
            index = index + 1
            
        button = Button(second_frame, text="Download result", command= lambda:[cr.download_repair(final_repair),alert("inspect")]).grid(row = 3, column =4)  
            
    if name_task == "INSPECTION+REPAIR":
        
        Label(second_frame, text="INSPECTION TASKS").grid(row=0, column=0, sticky=W)
        for i,j,k in zip(final_inspect["Task"], final_inspect["reason"],final_inspect["Assigned_to"]):
            Label(second_frame, text = i, wraplength=450, justify="left").grid(row=index, column=0, sticky=W, padx= 10)
            Label(second_frame, text = j,wraplength=300, justify="left").grid(row=index, column=1, sticky=W, padx= 10)
            Label(second_frame, text = k).grid(row=index, column=2, sticky=W, padx= 10)
            index = index + 1
        button = Button(second_frame, text="Download result2", command = lambda:[cr.download_inspect(final_inspect),alert("inspect")]).grid(row = 3, column =4)
        
        
        Label(second_frame, text = "Task").grid(row =index+1, column = 0)
        Label(second_frame, text = "Assigned_to").grid(row =index+1, column = 1)
        Label(second_frame, text = "Reason").grid(row =index+1, column = 2)
        Label(second_frame, text="REPAIR TASKS").grid(row=index, column=1, sticky=W)
        col = index +2
        for i,j,k in zip(final_repair["Task"], final_repair["reason"],final_repair["Assigned_to"]):
            Label(second_frame, text = i, wraplength=450, justify="left").grid(row=col, column=0, sticky=W,padx= 10)
            Label(second_frame, text = j,wraplength=300, justify="left").grid(row=col, column=1, sticky=W, padx= 10)
            Label(second_frame, text = k).grid(row=col, column=2, sticky=W, padx= 10)
            col = col + 1
        button = Button(second_frame, text="Download result1", command= lambda:[cr.download_repair(final_repair),alert("repair")]).grid(row = 4, column =4)

root = Tk()

root.geometry('1000x800')

main_frame = Frame(root)

main_frame.pack(fill =BOTH, expand = 1)

my_canvas = Canvas(main_frame)

my_canvas.pack(side=LEFT, fill = BOTH, expand =1)

my_scrollbar = ttk.Scrollbar(main_frame, orient =VERTICAL, command = my_canvas.yview)
x_my_scrollbar = ttk.Scrollbar(main_frame, orient =HORIZONTAL, command = my_canvas.xview)
my_scrollbar.pack(side=RIGHT, fill = Y)
x_my_scrollbar.pack(side=BOTTOM, fill = Y)

my_canvas.configure(yscrollcommand = my_scrollbar.set)
my_canvas.configure(xscrollcommand = x_my_scrollbar.set)
my_canvas.bind("<Configure>",lambda e:my_canvas.configure(scrollregion =my_canvas.bbox("all") ) )

second_frame = Frame(my_canvas)

my_canvas.create_window((0,0), window = second_frame, anchor ="nw")
i =0
Button(second_frame, text= "Upload Tasks file", command = openTasks).pack()
Button(second_frame, text= "Upload Safety file", command = openSafety).pack()
Button(second_frame, text = "Proceed", command = lambda: [cr.proceed(task, safety),clear_window(second_frame), homepage()]).pack(pady=5)
Button(second_frame, text ="Skip", command=lambda :[default_file(),clear_window(second_frame), homepage()]).pack(pady=5)


root.mainloop()