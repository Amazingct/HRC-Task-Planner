from tkinter import*
from tkinter import ttk
import pandas as pd
from tkinter import filedialog,messagebox
import numpy as np

def default_file():
    global task
    task = pd.read_excel("safety.xlsx")
    safety = pd.read_excel("tasks.xlsx")
    proceed()

def openTasks():
    global task
    filename = filedialog.askopenfilename(title = "Select a file")
    task = pd.read_excel(filename)
    task.set_index("type", inplace = True)
    messagebox.showinfo("message", "Upload Successful")
    
#     print(task)
def openSafety():
    global safety
    filename = filedialog.askopenfilename(title = "Select a file")
    safety = pd.read_excel(filename)
    messagebox.showinfo("message", "Upload Successful")
    safety.set_index("type", inplace = True)
    
    
def proceed():
    global unsafe_locations,repair, inspect,for_human,robot_can,safe_locations,unsafe_tasks,safe_tasks, result
    repair = []
    inspect = []
    for_human = []
    robot_can = []
    safe_tasks = []
    unsafe_tasks = []
    unsafe_locations = []
    safe_locations = []
    for x in task.loc["repair"]:
        if x is not np.nan:
            print(x)
            repair.append(x)
    
    for x in task.loc["inspect"]:
        if x is not np.nan:
#             print(x)
            inspect.append(x)
    
    for x in task.loc["for_human"]:
        if x is not np.nan:
#             print(x)
            for_human.append(x)
    for x in task.loc["robot_can"]:
        if x is not np.nan:
#             print(x)
            robot_can.append(x)
    for x in safety.loc["safe_locations"]:
        if x is not np.nan:
#             print(x)
            safe_locations.append(x)
            
    for x in safety.loc["unsafe_tasks"]:
        if x is not np.nan:
#             print(x)
            unsafe_tasks.append(x)
    
    for x in safety.loc["safe_tasks"]:
        if x is not np.nan:
            print(x)
            safe_tasks.append(x)

    for x in safety.loc["unsafe_locations"]:
        if x is not np.nan:
#             print(x)
            unsafe_locations.append(x)

    homepage()
def homepage():
    global root,result,actions
    root = Toplevel()
    root.geometry("1900x1500")
    actions = []
    safe = {}
    robot_task = {}
    result = pd.DataFrame(columns =["Task","Index","Assigned_to", "reason"])
    
#     for thing in range(100):
#         Button(second_frame,text=f'Button{thing }Yo' ).pack()

    

    def get_response():
        global index,actions_dict,response
        response = clicked.get()

        actions_dict = {}

        index = 2
        if response == "INSPECTION":
            label = [None]*100
            label[1] = Label(root, text = "Task to performed")
            label[1].grid(row = 1, column = 0 ,sticky=W)
            for i in inspect:
                    label[index] = Label(root, text = i)
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    actions.append(i)

    #         create_button()

    #                 actions.append(i)
        elif response == "REPAIR":
            index = 2
            label = [None]*100
            label[1] = Label(root, text = "Task to performed")
            label[1].grid(row = 1, column = 0 ,sticky=W)
            for i in repair:
                    label[index] = Label(root, text = i)
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    actions.append(i)
    #         create_button()
        elif response == "INSPECTION+REPAIR":
            index = 2
            label = [None]*100
            label[1] = Label(root, text = "Task to performed")
            label[1].grid(row = 1, column = 0 ,sticky=W)
            for i in inspect:
                    label[index] = Label(root, text = i)
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    actions.append(i)
            for i in repair:
                    label[index] = Label(root, text = i)
                    label[index].grid(row = index, column = 0 ,sticky=W)
                    index = index + 1
                    actions.append(i)
    #         create_button()
        keys = [x for x in range(len(actions))]
        actions_dict = dict(zip(keys,actions))

        first_criteria(actions_dict)

    # Create object

    label = Label(root, text= "Select Job to be performed")


    label.grid(row = 0, column = 0, padx = 350)


    options = ["INSPECTION","REPAIR", "INSPECTION+REPAIR"]

    clicked = StringVar()

    clicked.set("INSPECTION" )

    drop = OptionMenu( root , clicked , *options )
    drop.config(width = 20)
    drop.grid(row = 0, column = 1)


    button = Button( root , text = "submit" , command = get_response )

    button.grid(row = 0, column = 2,sticky=W)
    print(clicked.get())

safe = {}
robot_task = {}
def first_criteria(task_list):
    to_be_removed =[]
       #SAFE
    for h,i in task_list.items(): 
        for x in safe_tasks:
            if x in i:
                for j in safe_locations:
                    if j in i:
                        safe.update({h:i})
#                         print(i)
#Unsafe1
    for  h,i in task_list.items(): 
        for x in safe_tasks:
            if x in i:
                for j in unsafe_locations :
                    if j in i and h not in to_be_removed:
                        print(i)
                        robot_task.update({h:i})
                        to_be_removed.append(h)
                        values = [i,h, "ROBOT", "UNSAFE"]
                        result.loc[len(result)] = values
#                         task_list.remove(i)
#Unsafe2
    for  h,i in task_list.items(): 
        for x in unsafe_tasks:
            if x in str(i):
                for j in safe_locations :
                    if j in  str(i) and i not in robot_task:
                        print(i)
                        robot_task.update({h:i})
                        to_be_removed.append(h)
                        values = [i,h, "ROBOT", "UNSAFE"]
                        result.loc[len(result)] = values
#                         task_list.remove(i)
#Unsafe3
    for  h,i in task_list.items(): 
        for x in unsafe_tasks:
            if x in i:
                for j in unsafe_locations :
                    if j in i and i not in robot_task:
                        print(i)
                        robot_task.update({h:i})
                        to_be_removed.append(h)
                        values = [i,h ,"ROBOT", "UNSAFE"]
                        result.loc[len(result)] = values
#                         task_list.remove(i)
    print(to_be_removed)
    for i in to_be_removed:
        del(task_list[i])
    second_criteria(actions_dict)


def second_criteria(task_list):
    def get_val():
        global height_human , height_tank
        
        height_human = height_human_e.get()
        height_tank  = height_tank_e.get()
        print(height_human, height_tank)
        third_criteria(actions_dict)
        
    
    to_be_removed = []
    condition = False
    
    for h,i in task_list.items():
        if ("VISUAL INSPECTION" in i and "OUTER SHELL" in i) or ("ULTRASONIC INSPECTION" in i and
                                                                       "OUTER SHELL" in i):
                height_human_l = Label(root, text = "Enter height of human")
                height_human_l.grid(row =1, column = 1, pady = 4)
                height_human_e = Entry(root)
                height_human_e.grid(row =1, column = 2, pady = 4)
#                 height_human_s = Button(root, text = "Enter")
#                 height_human_s.grid(row =1, column = 3, pady = 4, padx = 2)
                height_tank_l = Label(root, text = "Enter height of human")
                height_tank_l.grid(row =2, column = 1, pady = 4)
                height_tank_e = Entry(root)
                height_tank_e.grid(row =2, column = 2, pady = 4)
                height_tank_s = Button(root, text = "Enter", command = get_val)
                height_tank_s.grid(row =3, column = 1, pady = 4, padx = 2, sticky=W)

#                 colaborative.update({h:i})
                to_be_removed.append(h)
                print(to_be_removed)
                string = "FROM "+ height_human + " DOWN, ASSIGNED TO HUMAN " + " FROM " + height_tank + " TO " +  str(height_human) + " ASSIGNED TO HUMAN "
                values = [i, h, "HUMAN AND ROBOT", string]
                condition = True
                result.loc[len(result)] = values

    if condition == False:
        third_criteria(actions_dict)
                
    print(to_be_removed)
    for i in to_be_removed:
        del(task_list[i])

def third_criteria(task_list):
    to_be_removed = []
    for h,i in task_list.items():
        for x in for_human:
            if x in i and h not in to_be_removed:
                to_be_removed.append(h)
                values = [i, h, "HUMAN", "MANDATORY FOR HUMAN"]
                result.loc[len(result)] = values
    print(to_be_removed)
    for i in to_be_removed:
        del(task_list[i])
    fourth_criteria(actions_dict)

def fourth_criteria(task_list):
    def get_values():
        global res
        res = []
        for i in clicked:
            res.append(i.get()) 
        for  vals,tasks in zip(res,task_list.items()):
            if vals == "1":
    #             colaborative.update({tasks[0]:task[1]})
                to_be_removed.append(tasks[0])
                print(tasks[1])
                values = [tasks[1],tasks[0], "HUMAN AND ROBOT", "COLLABORATIVE"]
                result.loc[len(result)] = values
        print(to_be_removed)
        for i in to_be_removed:
            del(task_list[i])
        fifth_criteria(actions_dict)
        
        
    to_be_removed = []
    master = Toplevel()
    master.geometry("1900x1500")
    label = [None]*100
    entry = [None]*100
    drop = [None]*100
    index = 2
    clicked = []
    values = []
    label[1] = Label(master, text = "For Each task enter Enter 1 for, Collaborative task and 0 for otherwise")
    label[1].grid(row = 1, column = 1, sticky=W)
    for i in range(len(task_list)):
        var = StringVar(master, "1")
        clicked.append(var)
        
    clicked =clicked[0:len(task_list)]
    val = {"Collaborative " : "1","Not Collaborative " : "2"}
    l = 0
    for i in task_list.items():
        label[index ] = Label(master, text = i[1])
#         label[index ].config(width = 80)
        label[index].grid(row = index, column = 1, sticky=W)
        j = 2
        for (text, value) in val.items():
            Radiobutton(master, text = text, variable = clicked[l],
                value = value).grid(row = index, column=j)
            j = j+1
        l= l+1
            
        index = index +1
  

    

        
    button = Button(master, text = "submit", command = get_values)
    button.grid(row = index, column = 1)
        
def fifth_criteria(task_list):
    print("Function four *********************************************************************************")
    global ress
    ress = []
    def get_values():
        for i,j,k in zip(human_times,robot_times,choice):
            ress.append([i.get(), j.get(), k.get()])
        for i,j in zip(ress, task_list.items()):
            if i[2] == "HIGH" :
                o_c = 1

            elif i[2] == "MID":
                o_c = 0.5

            elif i[2] == "LOW":
                o_c = 0

            if j[1] in robot_can:
                task_complexity = 0
            else:
                task_complexity = float("inf")

            robot_cost = 0.1*task_complexity + 0.3 * (float(i[1])/60) + 0.6*o_c

            print(robot_cost)

            human_cost = 0.1*task_complexity + 0.3 * (float(i[0])/60) + 0.6*o_c

            print(human_cost)

            if human_cost >  robot_cost:
    #             robot_task.update({h:i})
                to_be_removed.append(j[0])
                values = [j[1],j[0], "ROBOT", "LOWER COST FUNCTION"]
                result.loc[len(result)] = values
            elif human_cost < robot_cost:
    #             human_task.update({h:i})
                to_be_removed.append(j[0])
                values = [j[1],j[0], "HUMAN", "LOWER COST FUNCTION"]
                result.loc[len(result)] = values
        print(to_be_removed)
        for i in to_be_removed:
            del(task_list[i])
        sixth_criteria(task_list)
    win = Toplevel()
    win.geometry("1900x1500")
    to_be_removed = []
    label = [None]*100
    human_time = [None]*100
    human_times = []
    robot_time = [None]*100
    robot_times = []
    operating_cost = [None]*100
    operating_costs = []
    index = 2
    
    label[0] = Label( win, text = "For each task enter time for human, time of robot and operating cost")
    label[0].grid(row = 0, column = 0)
    
    label[1] = Label(win, text = "Task")
    label[1].grid(row = 1, column = 0)
    
    label[2] = Label(win, text = "Time for human")
    label[2].grid(row = 1, column = 1, padx = 5)
    
    label[2] = Label(win, text = "Time for robot")
    label[2].grid(row = 1, column = 2, padx = 5)
    
    label[2] = Label(win, text = "Level Operating Cost")
    label[2].grid(row = 1, column = 3, padx = 5)
    costs = ["HIGH", "LOW", "MID"]
    choice = []
    for i in range(len(task_list)):
        var = StringVar(win, "1")
        choice.append(var)
    
    
    l = 0
    for i in task_list.items():
        label[index] = Label(win, text = i[1])
        label[index].grid(row = index, column = 0, sticky = W)
        human_time[index] = Entry(win)
        human_times.append(human_time[index] )
        human_time[index].grid(row = index, column = 1 )
        robot_time[index] = Entry(win)
        robot_times.append(robot_time[index] )
        robot_time[index].grid(row = index, column = 2 )
        choice[l].set("HIGH")
        operating_cost[index] = OptionMenu(win, choice[l], *costs)
        operating_cost[index].config(width = 10)
        operating_costs.append(operating_cost[index] )
        operating_cost[index].grid(row = index, column = 3 )

        index = index +1
        l = l + 1
        
    Button(win, text = "submit", command = get_values).grid(row = index, column = 2)

def sixth_criteria(task_list):
    to_be_removed = []
    val = 1
    for  h,i in task_list.items():
        if val == 1:
            to_be_removed.append(h)
            val = 0
            values = [i,h, "ROBOT", "RANDOM SELECTION"]
            result.loc[len(result)] = values
        elif val == 0:
            to_be_removed.append(h)
            values = [i,h, "HUMAN", "RANDOM SELECTION"]
            result.loc[len(result)] = values
            val = 1
    for i in to_be_removed:
        del(task_list[i])
    display_result(result,response)
        
def display_result(resultt, no_task):
    wind = Toplevel()
    wind.geometry("1900x1500")
    resultt.set_index("Index", inplace =True)
    resultt.sort_index(axis = 0, inplace = True)
    index = 2
#     task = [None]*len(result)
#     reason = [None]*len(result)
#     Assigned_to = [None]*len(result)
    Label(wind, text = "Task").grid(row =1, column = 0)
    Label(wind, text = "Assigned_to").grid(row =1, column = 1)
    Label(wind, text = "Reason").grid(row =1, column = 2)
    if no_task ==  "INSPECTION" or no_task == "REPAIR":
        Label(wind, text= response+" TASKS").grid(row=0, column=0, sticky=W)
        for i,j,k in zip(result["Task"], result["reason"],result["Assigned_to"]):
            Label(wind, text = i).grid(row=index, column=0, sticky=W)
            Label(wind, text = j).grid(row=index, column=1, sticky=W)
            Label(wind, text = k).grid(row=index, column=2, sticky=W)
            index = index + 1
            if no_task ==  "REPAIR":
                button = Button(wind, text="Download result", command= lambda:download_repair(resultt)).grid(row = 3, column =4)
            elif no_task ==  "INSPECTION":
                button = Button(wind, text="Download result", command= lambda:download_inspect(resultt)).grid(row = 3, column =4)
                    
            
    if no_task == "INSPECTION+REPAIR":
        num_inspect = [x for x in range(len(inspect))]
        inspect_result = resultt.loc[result.index.isin(num_inspect)]
        Label(wind, text="INSPECTION TASKS").grid(row=0, column=0, sticky=W)
        for i,j,k in zip(inspect_result["Task"], inspect_result["reason"],inspect_result["Assigned_to"]):
            Label(wind, text = i).grid(row=index, column=0, sticky=W, padx= 10)
            Label(wind, text = j).grid(row=index, column=1, sticky=W, padx= 10)
            Label(wind, text = k).grid(row=index, column=2, sticky=W, padx= 10)
            index = index + 1
        button = Button(wind, text="Download result", command = lambda:download_inspect(inspect_result)).grid(row = 3, column =4)
        num_repair = [x for x in range(len(inspect), len(actions)+1)]
        repair_result = resultt.loc[result.index.isin(num_repair)]
        
        
#         index = index +1
        window = Toplevel()
        window.geometry(("1950x1500"))
        Label(window, text = "Task").grid(row =1, column = 0)
        Label(window, text = "Assigned_to").grid(row =1, column = 1)
        Label(window, text = "Reason").grid(row =1, column = 2)
        Label(window, text="REPAIR TASKS").grid(row=0, column=0, sticky=W)
        col = 2
        for i,j,k in zip(repair_result["Task"], repair_result["reason"],repair_result["Assigned_to"]):
            Label(window, text = i).grid(row=col, column=0, sticky=W,padx= 10)
            Label(window, text = j).grid(row=col, column=1, sticky=W, padx= 10)
            Label(window, text = k).grid(row=col, column=2, sticky=W, padx= 10)
            col = col + 1
        button = Button(window, text="Download result", command= lambda:download_repair(repair_result)).grid(row = 3, column =4)

    def download_repair(result):
        result.to_csv("repair_result.csv")
        messagebox.showinfo("message", "download successful as repair_result.csv")
        wind.destroy()


    def download_inspect(result):
        result.to_csv("inspect_result.csv")
        messagebox.showinfo("message", "download successful as inspect_result.csv")
        wind.destroy()
    