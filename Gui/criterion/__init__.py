from tkinter import*
from tkinter import ttk
import pandas as pd
from tkinter import filedialog,messagebox
import numpy as np
global actions,result
actions = []
result = pd.DataFrame(columns =["Task","Index","Assigned_to", "reason"])
    
def proceed(task, safety):
    global unsafe_locations,repair, inspect,for_human,robot_can,safe_locations,unsafe_tasks,safe_tasks, result

    safety = pd.read_excel(safety, engine = "openpyxl")
    task = pd.read_excel(task, engine = "openpyxl")


    task = task.set_index("type")

    safety = safety.set_index("type")
    
    
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
            # print(x)
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
            # print(x)
            safe_tasks.append(x)

    for x in safety.loc["unsafe_locations"]:
        if x is not np.nan:
#             print(x)
            unsafe_locations.append(x)

    

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
    # print(to_be_removed)
    for i in to_be_removed:
        del(task_list[i])
    # second_criteria(actions_dict)

def pre_second_criteria(task_list):
    condition = False
    for h,i in task_list.items():
        if ("VISUAL INSPECTION" in i and "OUTER SHELL" in i) or ("ULTRASONIC INSPECTION" in i and"OUTER SHELL" in i):
            condition = True
    return condition

def second_criteria(task_list,height_human,height_tank ):
    to_be_removed = []
    
    for h,i in task_list.items():
        if ("VISUAL INSPECTION" in i and "OUTER SHELL" in i) or ("ULTRASONIC INSPECTION" in i and
                                                                       "OUTER SHELL" in i):
#                 colaborative.update({h:i})
                to_be_removed.append(h)
                print(to_be_removed)
                string = "FROM "+ height_human + " DOWN, ASSIGNED TO HUMAN " + " FROM " + height_tank + " TO " +  height_human + " ASSIGNED TO HUMAN "
                values = [i, h, "HUMAN AND ROBOT", string]

                result.loc[len(result)] = values
                
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

def fourth_criteria(task_list, res):
    to_be_removed = []
   
    for  vals,tasks in zip(res,task_list.items()):
        if vals == "1":
#             colaborative.update({tasks[0]:task[1]})
            to_be_removed.append(tasks[0])
            # print(tasks[1])
            values = [tasks[1],tasks[0], "HUMAN AND ROBOT", "COLLABORATIVE"]
            result.loc[len(result)] = values
    print(to_be_removed)
    for i in to_be_removed:
        del(task_list[i])
        
        
    
    
def fifth_criteria(task_list,opt,bet):
    to_be_removed = []
    print("Function four *********************************************************************************")
    
    for i,j in zip(opt, task_list.items()):
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

        robot_cost = float(bet[0])*task_complexity + float(bet[1]) * (float(i[1])/60) + float(bet[2])*o_c

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

    
    

def sixth_criteria(task_list):
    global repair_task, inspection_task
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
def get_result(resultt, name_task):
    resultt.set_index("Index", inplace =True)
    resultt.sort_index(axis = 0, inplace = True)
    if name_task == "REPAIR": 
        repair_result = resultt
        return repair_result, " "
    if name_task=="INSPECTION":
        inspection_result = resultt
        return " ", inspection_result
    if name_task=="INSPECTION+REPAIR":  
        num_inspect = [x for x in range(len(inspect))]
        inspection_result = resultt.loc[result.index.isin(num_inspect)]
        num_repair = [x for x in range(len(inspect), len(actions)+1)]
        repair_result = resultt.loc[result.index.isin(num_repair)]
        return repair_result, inspection_result



    # display_result(result,response)
    

def download_repair(result):
    result.to_csv("repair_result.csv")
    

def download_inspect(result):
    result.to_csv("inspect_result.csv")