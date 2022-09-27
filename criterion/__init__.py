from platform import java_ver
import pandas as pd
import numpy as np
import json
actions = []
human = {}
robot = {}
collab = {}
safe = {}
actions_dict  = {}
for_human = []
safe_tasks = []
unsafe_tasks = []
robot_can = []
inspect = []
repair = []
safe_locations = []
unsafe_locations = []


result = pd.DataFrame(columns =["Task","Index","Assigned_to", "reason"])


def capture(question):
    val =input(question+": ")
    return val

def sort_result(unsorted):
    unsorted.set_index("Index", inplace = True)
    sorted = unsorted.sort_values(by=['Index'])
    return sorted


def collect_data(safety, tasks, job_type):
    global actions_dict, safe_tasks, unsafe_tasks, for_human, safe_locations, unsafe_locations, actions

    
    safety = pd.read_excel(safety)
    task = pd.read_excel(tasks)
    safety.set_index("type", inplace = True)
    task.set_index("type", inplace = True)
    safe_tasks = []

    for_human = []
    for x in task.loc["for_human"]:
        if x is not np.nan:
 
            for_human.append(x)

    robot_can = []
    for x in task.loc["robot_can"]:
        if x is not np.nan:

            robot_can.append(x)
    inspect = []
    for x in task.loc["inspect"]:
        if x is not np.nan:

            inspect.append(x)

    repair = []
    for x in task.loc["repair"]:
        if x is not np.nan:
   
            repair.append(x)
    for x in safety.loc["safe_tasks"]:
        if x is not np.nan:

            safe_tasks.append(x)

        safe_locations = []
    for x in safety.loc["safe_locations"]:
        if x is not np.nan:
  
            safe_locations.append(x)

    unsafe_tasks = []
    for x in safety.loc["unsafe_tasks"]:
        if x is not np.nan:

            unsafe_tasks.append(x)


    unsafe_locations = []
    for x in safety.loc["unsafe_locations"]:
        if x is not np.nan:

            unsafe_locations.append(x)

    if job_type == "1":
        for i in inspect:
                actions.append(i)
    elif job_type == "2":
        for i in repair:
                actions.append(i)
    elif job_type == "3":
        for i in inspect:
                actions.append(i)
        for i in repair:
                actions.append(i)

    keys = [x for x in range(len(actions))]
    actions_dict = dict(zip(keys,actions))

def first_criteria(task_list):
    robot_task = {}

    to_be_removed =[]
       #SAFE
    for h,i in task_list.items(): 
        for x in safe_tasks:
            if x in i:
                for j in safe_locations:
                    if j in i:
                        safe.update({h:i})

#Unsafe1
    for  h,i in task_list.items(): 
        for x in safe_tasks:
            if x in i:
                for j in unsafe_locations :
                    if j in i and h not in to_be_removed:
              
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
                    if j in  str(i) and i not in robot:
              
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
                    if j in i and i not in robot:
                 
                        robot_task.update({h:i})
                        to_be_removed.append(h)
                        values = [i,h ,"ROBOT", "UNSAFE"]
                        result.loc[len(result)] = values
#                         task_list.remove(i)

    for i in to_be_removed:
        del(task_list[i])
        

def second_criteria(task_list):
    colaborative = {}
    to_be_removed =[]
    for h,i in task_list.items():
    
        if ("VISUAL INSPECTION" in i and "OUTER SHELL" in i) or ("ULTRASONIC INSPECTION" in i and
                                                                       "OUTER SHELL" in i):
                human_height = capture("Enter human height")
                tank_height = capture("Enter tank height")

                colaborative.update({h:i})
                to_be_removed.append(h)

                string = "FROM "+ str(human_height) + " DOWN, ASSIGNED TO HUMAN " + " FROM " + str(tank_height) + " TO " +  str(human_height) + " ASSIGNED TO HUMAN "
                values = [i, h, "HUMAN AND ROBOT", string]
                result.loc[len(result)] = values

    for i in to_be_removed:
        del(task_list[i])

            
def third_criteria(task_list):
    human_task = {}
    to_be_removed = []
    for h,i in task_list.items():
        for x in for_human:
            if x in i and h not in to_be_removed:
                to_be_removed.append(h)
                values = [i, h, "HUMAN", "MANDATORY FOR HUMAN"]
                result.loc[len(result)] = values
                human_task.update({h:i})

    for i in to_be_removed:
        del(task_list[i])

def fourth_criteria(task_list):
    to_be_removed = []
    for i in task_list.items():
        print(i)

    val = capture("for each ofthe above task enter a list of values indicating 1 for collaborative and 0 for otherwise [1,2,2,]")
    val = json.loads(val)
    for  vals,tasks in zip(val,task_list.items()):
        if vals == 1:
            # colaborative.update({tasks[0]:task[1]})
            to_be_removed.append(tasks[0])
            print(tasks[1])
            values = [tasks[1],tasks[0], "HUMAN AND ROBOT", "COLLABORATIVE"]
            result.loc[len(result)] = values
    print(to_be_removed)
    for i in to_be_removed:
        del(task_list[i])


def fifth_criteria(task_list):
    print("Function four *********************************************************************************")
    to_be_removed = []
    for i in task_list.items():
        print(i)
    
    
    time_human = capture("for each of the task above enter time it takes for human to complete as a list")
    time_robot = capture("for each of the task above enter time it takes for robot to complete as a list")
    operating_cost = capture("for each of  the task enter  Enter the level of operating cost 3 HIGH, 2 MID, 1 LOW")
    
    
    time_human = json.loads(time_human)
    time_robot = json.loads(time_robot)
    operating_cost = json.loads(operating_cost)
    
    for i,j,k,l in zip(time_human,time_robot,operating_cost,task_list.items()):
        if k == 3 :
            o_c = 1
        
        elif k == 2:
            o_c = 0.5
        
        elif k == 1:
            o_c = 0
        
        if l[1] in robot_can:
            task_complexity = 0
        else:
            task_complexity = float("inf")

        robot_cost = 0.1*task_complexity + 0.3 * (j/60) + 0.6*o_c
        
        print(robot_cost)
        
        human_cost = 0.1*task_complexity + 0.3 * (i/60) + 0.6*o_c
        print(human_cost)
        if human_cost >  robot_cost:
#             robot_task.update({h:i})
            to_be_removed.append(l[0])
            values = [l[1],l[0], "ROBOT", "LOWER COST FUNCTION"]
            result.loc[len(result)] = values
        elif human_cost < robot_cost:
#             human_task.update({h:i})
            to_be_removed.append(l[0])
            values = [l[1],l[0], "HUMAN", "LOWER COST FUNCTION"]
            result.loc[len(result)] = values
    for i in to_be_removed:
        del(task_list[i])

def sixth_criteria(task_list):
    robot_task = {}
    human_task ={}
    to_be_removed = []
    val = 1
    for  h,i in task_list.items():
        if val == 1:
            robot_task.update({h:i})
            to_be_removed.append(h)
            val = 0
            values = [i,h, "ROBOT", "RANDOM SELECTION"]
            result.loc[len(result)] = values
        elif val == 0:
            robot_task.update({h:i})
            to_be_removed.append(h)
            values = [i,h, "HUMAN", "RANDOM SELECTION"]
            result.loc[len(result)] = values
            val = 1
    for i in to_be_removed:
        del(task_list[i])
def result_sorting(resultt, no_task):
    resultt.set_index("Index", inplace =True)
    resultt.sort_index(axis = 0, inplace = True)
    if no_task ==  "1" or no_task == "2":
        return result, " "
    if no_task == "3":
        num_inspect = [x for x in range(len(inspect))]
        inspect_result = resultt.loc[result.index.isin(num_inspect)]
        num_repair = [x for x in range(len(inspect), len(actions)+1)]
        repair_result = resultt.loc[result.index.isin(num_repair)]
        
        return inspect_result, repair_result


