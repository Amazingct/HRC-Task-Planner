
import streamlit as st
import time, json
import pandas as pd
import os
import matplotlib.pyplot as plt
import criterion as cr
import threading as th

rtasks =  os.path.join(os.path.dirname(__file__),'configurations', 'tasks.json')
rsafety = os.path.join(os.path.dirname(__file__),'configurations', 'safety.json')
ready = False
job_name = ""
job_description = ""
job_type = []
plan_container = st.empty()

def collect_4th_criteria_input(actions):
    print("THIS-->", len(actions))
    for i,a in enumerate(actions):
            act_row = st.columns(2)
            act_row[0].write(str(i)+"."+a)
            act_row[1].radio("Select", ["Collaborative", "Non-Collaborative"], key="4th_c_input_"+str(i))


def extract_4th_input(state, n_actions):
    values = [0]*n_actions
    for key, value in state.items():
        if "4th_c" in key:
            index = int(key.split("_")[3])
            print("index", index)
            values[index] = 1 if value=="Collaborative" else 0
    return values
            


def collect_5th_criteria_input():
    pass

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
    def __init__(self, name, description,job_type, tasks , safety, tank_height, human_height):
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
        self.jobNumber = 0
        self.currentPlan = None
        self.render_container = st.empty()
        self.tank_height = tank_height
        self.human_height = human_height

        if len(self.job_type) == 2:
            self.jobNumber = "3"
        elif len(self.job_type) == 1:
            if self.job_type[0] == "REPAIR":
                self.jobNumber = "2"
            elif self.job_type[0] == "INSPECTION":
                self.jobNumber = "1"
    
    def plan_now(self):
        print("jobNumber",self.jobNumber)
        # Empty Container to hold UI for collecting user input
        placeholder = st.empty()
        cr.collect_data("safety.xlsx", "tasks.xlsx", self.jobNumber, placeholder)
       
        # First Criteria
        cr.first_criteria()
        cr.second_criteria(self.tank_height, self.human_height)
        cr.third_criteria()
       # print(cr.task_list)

        # 4th `  Criteria`
        collect_4th_criteria_input(list(cr.task_list.values()))
        fcvals = extract_4th_input(st.session_state, len(list(cr.task_list.values())))
        fcvals = [0]*len(list(cr.task_list.values()))
        cr.fourth_criteria(fcvals)

        # 5th Criteria
        collect_5th_criteria_input
        time_h=[12]*len(list(cr.task_list.values()))
        time_r=[25]*len(list(cr.task_list.values()))
        cost = [2]*len(list(cr.task_list.values()))
        cr.fifth_criteria(time_h, time_r, cost)

        # 6th Criteria
        cr.sixth_criteria()
        print(cr.result)
        self.render()
        
       
    def render(self):
        with self.render_container.container():
            # get details
            self.currentPlan = cr.result
            self.n_assigned_to_robot =  len(self.currentPlan[self.currentPlan["Assigned_to"]=="ROBOT"])
            self.n_assigned_to_human =  len(self.currentPlan[self.currentPlan["Assigned_to"]=="HUMAN"])
            self.n_assigned_to_human_and_robot = len(self.currentPlan[self.currentPlan["Assigned_to"]=="HUMAN AND ROBOT"])
            print("robot:",self.n_assigned_to_robot)
            print("human:",self.n_assigned_to_human)
            tab = st.columns(6)
            #job name
            tab[0].title(self.name)
            #job type
            if len(self.job_type) == 1:
                tab[1].write(self.job_type[0])
            else:
                tab[1].write(self.job_type[0]  + " AND " + self.job_type[1])
            #plan description
            tab[2].metric("Robot", self.n_assigned_to_robot,)
            tab[3].metric("Human", self.n_assigned_to_human)
            tab[4].metric("Human & Robot", self.n_assigned_to_human_and_robot)
            tab[5].metric("Total Tasks", self.n_assigned_to_robot + self.n_assigned_to_human+self.n_assigned_to_human_and_robot)

            cols = st.columns(2)
            self.stage = ["INSPECT", "REPAIR"] if len(self.job_type) == 2 else self.job_type
            
            cols[0].write("""## CURRENT PLAN""")
            cols[0].write(self.currentPlan)
            cols[0].write("""---""")

            with cols[1] as col:
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

            #download = st.columns(2)
            
            #results = cr.result_sorting(self.currentPlan, self.jobNumber)
            # for i in results:
            #      self.currentPlan[i].to_excel(index=False,excel_writer=os.path.join(os.path.dirname(__file__),'configurations', "{}.xlsx").format(self.stage[i]))
            #      download[i].download_button(file_name="{}.xlsx".format(self.stage[i]), label="Download {}".format(self.stage[i]), data=open(os.path.join(os.path.dirname(__file__),'configurations', "{}.xlsx").format(self.stage[i]), 'rb').read(), mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        
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
        human_height = cols[0].slider("HUMAN HEIGHT(Meters)", 0,100)
        date = cols[0].date_input("DATE")
        job_time = cols[0].time_input("TIME")

        job_description = cols[1].text_area("TASK DESCRIPTION", height=410)
        submit_button = st.form_submit_button(label='Submit',)

    return job_name, job_description, job_type, tank_height, human_height


