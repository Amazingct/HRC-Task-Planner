from asyncio import tasks
import streamlit as st
import time, json
import pandas as pd
rtasks =  r"E:\Projects\HRC Task Planner\configurations\tasks.json"
rsafety = r"E:\Projects\HRC Task Planner\configurations\safety.json"
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

class Tasks:
    def __init__(self,filename=rtasks):
        self.file = filename
        with open(self.file) as f:
            self.tasks = json.load(f)
        
    def file_is_valid(self,uploaded_file):
        error = ''
        if uploaded_file is not None:
            try:
                json.loads(uploaded_file.getvalue().decode("utf-8"))
                return True, error
            except:
                return False, 'Please upload a valid JSON file'
        else:
            return False, ''
    
    def change(self):
        uploaded_file = st.file_uploader("Choose a JSON file")
        valid, error = self.file_is_valid(uploaded_file)
        if valid:
            display_loading("Loading Tasks...")
            self.tasks =json.loads(uploaded_file.getvalue().decode("utf-8"))
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
            st.error("Wrong formaat of Tasks JSON file")

        

class Safety:
    def __init__(self,filename=rsafety):
        self.file = filename
        with open(self.file) as f:
            self.tasks = json.load(f)
        

    
    def file_is_valid(self,uploaded_file):
            error = ''
            if uploaded_file is not None:
                try:
                    json.loads(uploaded_file.getvalue().decode("utf-8"))
                    return True, error
                except:
                    return False, 'Please upload a valid JSON file'
            else:
                return False, ''
        
    def change(self):
        uploaded_file = st.file_uploader("Choose a JSON file")
        valid, error = self.file_is_valid(uploaded_file)
        if valid:
            display_loading("Loading Safety...")
            self.tasks =json.loads(uploaded_file.getvalue().decode("utf-8"))
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
            st.error("Wrong formaat of Safety JSON file")

       

class Plan:
    def __init__(self, name= "", description ="", job_type = [], tasks =rtasks , safety=rsafety):
        self.name = name
        self.description = description
        self.tasks = tasks
        self.safety = safety
        self.job_type = job_type
        self.n_assigned_to_robot = 4
        self.n_assigned_to_human = 6

    



    def render(self):
        tab = st.columns(4)

        tab[0].title(self.name)
        tab[1].metric("Assigned to Robot", self.n_assigned_to_robot,)
        tab[2].metric("Assigned to Human", self.n_assigned_to_human)
        tab[3].markdown(self.description)

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


