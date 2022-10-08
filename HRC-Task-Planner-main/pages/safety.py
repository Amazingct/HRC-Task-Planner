import streamlit as st
import PlannerModule as pm



pm.header()
t = pm.Safety()
t.change()
t.render()
pm.footer()