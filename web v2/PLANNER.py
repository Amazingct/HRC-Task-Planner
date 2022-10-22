import streamlit as st
import PlannerModule as pm
import time

def is_valid(n,d,t):
    if n == '' or d == '' or t == []:
        error = 'Please fill in all fields'
        return False, error
    else:
        return True, ''

"st.session_state objects", st.session_state

pm.header()
job_name,job_description,job_type, tank_h, human_h  =  pm.input_job()
print(job_name,job_description,job_type)

valid, error = is_valid(job_name,job_description,job_type)
if valid:
    
    plan = pm.Plan(job_name,job_description,job_type,"","",tank_h,human_h) #name, description, type tasks , safety, tank_height, human_height
    pm.display_loading("Starting plan...")
    plan.plan_now()
else:
    st.error(error)