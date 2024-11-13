import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Set page configuration
st.set_page_config(page_title="Project Punch List", layout="wide")

# Initialize session state for storing tasks
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

def save_tasks():
    """Save tasks to a JSON file"""
    with open('tasks.json', 'w') as f:
        json.dump(st.session_state.tasks, f)

def load_tasks():
    """Load tasks from JSON file if it exists"""
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            st.session_state.tasks = json.load(f)

# Load existing tasks when the app starts
if 'tasks_loaded' not in st.session_state:
    load_tasks()
    st.session_state.tasks_loaded = True

# Main title
st.title("Project Punch List Manager")

# File upload section
with st.expander("Upload CSV File", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.success("File uploaded successfully!")
            
            # Display the uploaded data in a table
            st.subheader("Uploaded Data")
            st.dataframe(df, use_container_width=True)
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Task management section
with st.expander("Add New Task", expanded=True):
    col1, col2 = st.columns(2)
    
    with col1:
        # Task selection from CSV headers if data is uploaded
        if st.session_state.uploaded_data is not None:
            task_options = list(st.session_state.uploaded_data.columns)
            selected_task = st.selectbox("Select Task", task_options)
        else:
            selected_task = st.text_input("Enter Task Name")
        
        # Status selection
        status_options = ["Not Started", "In Progress", "Completed", "Blocked"]
        selected_status = st.selectbox("Select Status", status_options)
    
    with col2:
        # Time tracking
        hours = st.number_input("Hours", min_value=0, max_value=23, value=0)
        minutes = st.selectbox("Minutes", [0, 15, 30, 45])
        
        # Add task button
        if st.button("Add Task"):
            if selected_task:
                new_task = {
                    "id": len(st.session_state.tasks),
                    "name": selected_task,
                    "status": selected_status,
                    "time": f"{hours}h {minutes}m",
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.tasks.append(new_task)
                save_tasks()
                st.success("Task added successfully!")

# Display tasks
if st.session_state.tasks:
    st.subheader("Task List")
    
    # Filter options
    filter_status = st.multiselect(
        "Filter by Status",
        status_options,
        default=status_options
    )
    
    # Create a DataFrame from tasks for easier filtering and display
    tasks_df = pd.DataFrame(st.session_state.tasks)
    filtered_tasks = tasks_df[tasks_df['status'].isin(filter_status)]
    
    # Display each task as a card
    for _, task in filtered_tasks.iterrows():
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
            
            with col1:
                st.markdown(f"**{task['name']}**")
                st.caption(f"Added: {task['timestamp']}")
            
            with col2:
                status_color = {
                    "Not Started": "gray",
                    "In Progress": "blue",
                    "Completed": "green",
                    "Blocked": "red"
                }
                st.markdown(
                    f"<span style='color: {status_color[task['status']]};'>"
                    f"●</span> {task['status']}",
                    unsafe_allow_html=True
                )
            
            with col3:
                st.write(f"⏱️ {task['time']}")
            
            with col4:
                if st.button("Delete", key=f"delete_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                    save_tasks()
                    st.rerun()
        
        st.divider()

# Summary statistics
if st.session_state.tasks:
    st.subheader("Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_tasks = len(st.session_state.tasks)
        st.metric("Total Tasks", total_tasks)
    
    with col2:
        completed_tasks = len([t for t in st.session_state.tasks if t['status'] == 'Completed'])
        st.metric("Completed Tasks", completed_tasks)
    
    with col3:
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")

# Clear all tasks button
if st.session_state.tasks:
    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        save_tasks()
        st.rerun()
