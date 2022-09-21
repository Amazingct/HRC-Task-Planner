from ast import Index
from traceback import print_tb
import streamlit as st
import time, json
import pandas as pd
import os
import numpy as np
import matplotlib.pyplot as plt

rtasks =  os.path.join(os.path.dirname(__file__),'configurations', 'tasks.json')
rsafety = os.path.join(os.path.dirname(__file__),'configurations', 'safety.json')
ready = False
job_name = ""
job_description = ""
job_type = []
plan_container = st.empty()

def header():
    st.write(
    
    
    """

    # ![logo] HRC TASK PLANNER
    [Github](https://github.com/Amazingct/HRC-Task-Planner)

    ---
     
    [logo]: https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 2"
    """
)


def footer():
    st.write(
    """
    ---
    """
)

def excel_to_json(df):
    keys = df["type"].to_list()
    df = df.to_json('convert.json', indent=4, orient='records')
    with open('convert.json', 'r') as f:
        data = json.load(f)
    print("keys", keys)
    new_json = dict(zip(keys, [[]]*len(keys)))
    print("new_json", new_json)

    l = []


    all = []
    for i,row_dict in enumerate(data):
        l = []
        for n in range(len(row_dict.keys())):   
            try:
                t = data[i][str(n)]
                if type(t) == type("gg"):
                    l.append(t)
            except Exception as e:
                print("ERROR:",e)
        all.append(l)
    for i in range(len(keys)):
        new_json[keys[i]] = all[i]
    return new_json

class Tasks:
    def __init__(self,filename=rtasks):
        self.file = filename
        with open(self.file) as f:
            self.tasks = json.load(f)
        
    def file_is_valid(self,uploaded_file):
        error = ''
        if uploaded_file is not None:
            try:
                d = pd.read_excel(uploaded_file)
                return True, error
            except:
                return False, 'Please upload a valid file'
        else:
            return False, ''
    
    def change(self):
        uploaded_file = st.file_uploader("Choose an excel file")
        valid, error = self.file_is_valid(uploaded_file)
        if valid:
            display_loading("Loading Tasks...")
            df = pd.read_excel(uploaded_file)
            self.tasks = excel_to_json(df)
            #print(self.tasks)
            with open(self.file, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        else:
            if error != '':
                st.error(error)





    def render(self):
        try:
            self.repair = pd.DataFrame(self.tasks['repair'], columns=['REPAIR'])
            self.inspect = pd.DataFrame(self.tasks['inspect'], columns=['INSPECT'])
            self.robot_can = pd.DataFrame(self.tasks['robot_can'], columns=['ROBOT CAN'])
            self.for_human = pd.DataFrame(self.tasks['for_human'], columns=['FOR HUMAN'])

            st.write("""
            ## TASKS
            """)
            cols = st.columns(2)
            _cols = st.columns(2)


            cols[0].write(self.repair)
            cols[1].write(self.inspect)
            _cols[0].write(self.robot_can)
            _cols[1].write(self.for_human)

        except:
            st.error("Wrong formaat of Tasks  file")

class Safety:
    def __init__(self,filename=rsafety):
        self.file = filename
        with open(self.file) as f:
            self.tasks = json.load(f)
        

    
    def file_is_valid(self,uploaded_file):
            error = ''
            if uploaded_file is not None:
                try:
                    d = pd.read_excel(uploaded_file)
                    return True, error
                except:
                    return False, 'Please upload a valid file'
            else:
                return False, ''
        
    def change(self):
        uploaded_file = st.file_uploader("Choose an excel file")
        valid, error = self.file_is_valid(uploaded_file)
        if valid:
            df = pd.read_excel(uploaded_file)
            self.tasks = excel_to_json(df)
            #print(self.tasks)
            with open(self.file, 'w') as f:
                json.dump(self.tasks, f, indent=4)
        else:
            if error != '':
                st.error(error)
    
        

    def render(self):
        try:
            self.safe_tasks = pd.DataFrame(self.tasks['safe_tasks'], columns=['SAFE TASK'])
            self.unsafe_tasks = pd.DataFrame(self.tasks['unsafe_tasks'], columns=['UNSAFE TASKS'])
            self.safe_locations = pd.DataFrame(self.tasks['safe_locations'], columns=['SAFE LOCATIONS'])
            self.unsafe_locations = pd.DataFrame(self.tasks['unsafe_locations'], columns=['UNSAFE LOCATIONS'])

            st.write("""
                ## SAFETY
                """)
            cols = st.columns(2)
            _cols = st.columns(2)
            cols[0].write(self.safe_tasks)
            cols[1].write(self.unsafe_tasks)
            _cols[0].write(self.safe_locations)
            _cols[1].write(self.unsafe_locations)

        except:
            st.error("Wrong formaat of Safety  file")
class Plan:
    def __init__(self, name= "", description ="", job_type = [], tasks =rtasks , safety=rsafety):
        self.name = name
        self.description = description
        self.tasks = tasks
        self.safety = safety
        self.job_type = job_type
        self.n_assigned_to_robot = 0
        self.n_assigned_to_human = 0
        self.assignment = None
        self.repairtasks_who = []
        self.repairtasks = []
        self.inspecttasks_who=[]
        self.inspecttasks=[]
        self.robot_can = []
        self.for_human = []
        self.stage = []

    def assign_based_on_within_string(self, task):
        print("task", task)
        print("unsafe_location", self.unsafe_locations)
        

        for ul in self.unsafe_locations:
            if ul in task:
                return "ROBOT", "UNSAFE LOCATION"


        for ul in self.unsafe_tasks:
            if ul in task:
                return "ROBOT", "UNSAFE TASK"


        for ul in self.safe_locations:
            if ul in task:
                return "MAN", "SAFE LOCATION"

        for ul in self.safe_locations:
            if ul in task:
                return "MAN", "SAFE LOCATION"

        return "NONE", "OTHERS(UNKNOWN)"


    def plan_now(self):
        with open(self.tasks, "rb") as f:
            tasks = json.load(f)
            self.repairtasks = tasks["repair"]
            self.inspecttasks = tasks["inspect"]
            self.robot_can=tasks["robot_can"]
            self.for_human=tasks["for_human"]

        with open(self.safety, "rb") as f:
            safety = json.load(f)
            self.safe_tasks = safety["safe_tasks"]
            self.unsafe_tasks = safety["unsafe_tasks"]
            self.safe_locations = safety["safe_locations"]
            self.unsafe_locations = safety["unsafe_locations"]

        #REPAIR TASKS
        for i,task in enumerate(self.repairtasks):
            who, reason = self.assign_based_on_within_string(task)
            # LOCATION
            if who == "MAN":
                self.repairtasks_who.append([task, "MAN", reason])
            elif  who == "ROBOT":
                self.repairtasks_who.append([task, "ROBOT", reason])

            # SAFTY
            elif task in self.safe_tasks:
                self.repairtasks_who.append([task, "MAN", "SAFE TASK"])
            elif  task in self.unsafe_tasks:
                self.repairtasks_who.append([task, "ROBOT", "UNSAFE TASK"])

            # OTHERS
            elif task in self.for_human:
                self.repairtasks_who.append([task, "MAN", "AS IN DATABASE"])
            elif  task in self.robot_can:
                self.repairtasks_who.append([task, "ROBOT", "AS IN DATABASE"])

        
        
            else:
                self.repairtasks_who.append([task, "ROBOT", reason])

        #INSPECT TASKS
        for i,task in enumerate(self.inspecttasks):
            who, reason = self.assign_based_on_within_string(task)
             # LOCATION
            if who == "MAN":
                self.inspecttasks_who.append([task, "MAN", reason])
            elif  who == "ROBOT":
                self.inspecttasks_who.append([task, "ROBOT", reason])
            # SAFTY
            elif task in self.safe_tasks:
                self.inspecttasks_who.append([task, "MAN", "SAFE TASK"])
            elif  task in self.unsafe_tasks:
                self.inspecttasks_who.append([task, "ROBOT", "UNSAFE TASK"])

             # OTHERS
            elif task in self.for_human:
                self.inspecttasks_who.append([task, "MAN", "AS IN DATABASE"])
            elif  task in self.robot_can:
                self.inspecttasks_who.append([task, "ROBOT", "AS IN DATABASE"])


            else:
                self.inspecttasks_who.append([task, "ROBOT", reason])

            
                

           
        # ASSIGNMENT
        self.finalrepair = pd.DataFrame(self.repairtasks_who, columns=["TASKS", "ASSIGNED TO", "REASON"])
        self.finalinspect = pd.DataFrame(self.inspecttasks_who, columns=["TASKS", "ASSIGNED TO", "REASON"])

        if "INSPECTION" in self.job_type and "REPAIR" in self.job_type:
            self.assignment = [self.finalinspect, self.finalrepair]
            self.n_assigned_to_robot =  len(self.finalinspect[self.finalinspect["ASSIGNED TO"]=="ROBOT"]) + len(self.finalrepair[self.finalrepair["ASSIGNED TO"]=="ROBOT"])
            self.n_assigned_to_human = len(self.finalinspect[self.finalinspect["ASSIGNED TO"]=="MAN"]) + len(self.finalrepair[self.finalrepair["ASSIGNED TO"]=="MAN"])

        elif "INSPECTION" in self.job_type:
            self.assignment = [self.finalinspect]
            self.n_assigned_to_robot =  len(self.finalinspect[self.finalinspect["ASSIGNED TO"]=="ROBOT"])
            self.n_assigned_to_human = len(self.finalinspect[self.finalinspect["ASSIGNED TO"]=="MAN"])
        
        elif "REPAIR" in self.job_type:
            self.assignment = [self.finalrepair]
            self.n_assigned_to_robot =  len(self.finalrepair[self.finalrepair["ASSIGNED TO"]=="ROBOT"])
            self.n_assigned_to_human = len(self.finalrepair[self.finalrepair["ASSIGNED TO"]=="MAN"])

     


    def render(self):
        self.plan_now()
        tab = st.columns(5)
        tab[0].title(self.name)
        if len(self.job_type) == 1:
            tab[1].write(self.job_type[0])
        else:
            tab[1].write(self.job_type[0]  + " AND " + self.job_type[1])

        tab[2].metric("Assigned to Robot", self.n_assigned_to_robot,)
        tab[3].metric("Assigned to Human", self.n_assigned_to_human)
        tab[4].metric("Total Tasks", self.n_assigned_to_robot + self.n_assigned_to_human)

        cols = st.columns(3)
        self.stage = ["INSPECT", "REPAIR"] if len(self.job_type) == 2 else self.job_type
        for i, table in enumerate(self.assignment, ):
            cols[i].write("""## {}""".format(self.stage[i]))
            cols[i].write(table)
            cols[i].write("""---""")

        with cols[i+1] as col:
            data = {'ROBOT':self.n_assigned_to_robot, 'HUMAN':self.n_assigned_to_human}
            courses = list(data.keys())
            values = list(data.values())
            
            fig = plt.figure(figsize = (25, 25))
            
            # creating the bar plot
            plt.bar(courses, values, color ='maroon',
                    width = 0.4, edgecolor='black', linewidth=2)
 
            plt.xlabel("TASKS ASSIGNMENT")
            plt.ylabel("NUMBER OF TASK ASSIGNED")
            plt.title("DISTRIBUTION")
            st.pyplot(fig)

        download = st.columns(2)
        for i, table in enumerate(self.stage):
             self.assignment[i].to_excel(index=False,excel_writer=os.path.join(os.path.dirname(__file__),'configurations', "{}.xlsx").format(table.lower()))
             download[i].download_button(file_name="{}.xlsx".format(table.lower()), label="Download {}".format(table.lower()), data=open(os.path.join(os.path.dirname(__file__),'configurations', "{}.xlsx").format(table.lower()), 'rb').read(), mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
       
def display_loading(message):
    progress = st.empty()
    info = st.empty()
    my_bar = progress.progress(0)
    info.info(message)
    t = 3
    for percent_complete in range(t):
        time.sleep(1)
        my_bar.progress(100 * ((percent_complete+1)/t)/100)
    info.success("Done!")
        
def input_job():
    global job_name, job_description, job_type
    with st.form(key='job'):
        cols = st.columns(2)
        job_name = cols[0].text_input("JOB NAME")
        job_type = cols[0].multiselect("JOB TYPE (MULTIPLE SELECTION ALLOWED)", ["INSPECTION", "REPAIR"])
        tank_height = cols[0].slider("TANK HEIGHT(Meters)", 0,100)
        date = cols[0].date_input("DATE")
        job_time = cols[0].time_input("TIME")

        job_description = cols[1].text_area("TASK DESCRIPTION", height=410)
        submit_button = st.form_submit_button(label='Submit',)

    return job_name, job_description, job_type


