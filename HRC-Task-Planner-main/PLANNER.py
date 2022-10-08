import streamlit as st
import PlannerModule as pm
import time

def is_valid(n,d,t):
    if n == '' or d == '' or t == []:
        error = 'Please fill in all fields'
        return False, error
    else:
        return True, ''


pm.header()
job_name,job_description,job_type  =  pm.input_job()
print(job_name,job_description,job_type)

valid, error = is_valid(job_name,job_description,job_type)
if valid:
    plan = pm.Plan(job_name,job_description,job_type)
    pm.display_loading("Generating plan...")
    plan.render()
else:
    st.error(error)