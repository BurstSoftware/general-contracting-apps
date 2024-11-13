import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Set page configuration
st.set_page_config(page_title="Project Punch List", layout="wide")

# Initialize session state for storing tasks and settings
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None

if 'task_names' not in st.session_state:
    st.session_state.task_names = []

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

# File upload and column selection section
with st.expander("Upload CSV File and Configure Tasks", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.success("File uploaded successfully!")
            
            # Column selection for task identification
            st.subheader("Select Task Column")
            selected_column = st.selectbox(
                "Choose the column to use for task identification",
                options=df.columns,
                key="column_selector"
            )
            st.session_state.selected_column = selected_column
            
            # Store unique task names from the selected column
            st.session_state.task_names = df[selected_column].unique().tolist()
            
            # Display the uploaded data with selectable rows
            st.subheader("Select Records for Tasks")
            
            # Create a new DataFrame with selection checkboxes
            selection_df = df.copy()
            selection_df.insert(0, "Select", False)
            
            # Display editable dataframe
            edited_df = st.data_editor(
                selection_df,
                hide_index=True,
                use_container_width=True,
                key="task_selector"
            )
            
            # Button to create tasks from selected rows
            if st.button("Create Tasks from Selected Records"):
                selected_rows = edited_df[edited_df["Select"]]
                
                for idx, row in selected_rows.iterrows():
                    # Create a new task for each selected row
                    new_task = {
                        "id": len(st.session_state.tasks),
                        "parameter": selected_column,
                        "value": str(row[selected_column]),
                        "task_name": str(row[selected_column]),
                        "status": "Not Started",
                        "planned_hours": 0,
                        "planned_minutes": 0,
                        "actual_hours": 0,
                        "actual_minutes": 0,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    }
                    st.session_state.tasks.append(new_task)
                save_tasks()
                st.success(f"Created {len(selected_rows)} new tasks!")
                
        except Exception as e:
            st.error(f"Error reading file: {str(e)}")

# Task management section
if st.session_state.tasks:
    st.subheader("Manage Tasks")
    
    # Filter options in a single row
    status_options = ["Not Started", "In Progress", "Completed", "Blocked"]
    filter_status = st.multiselect(
        "Filter by Status",
        status_options,
        default=status_options
    )
    
    # Create a DataFrame from tasks for easier filtering and display
    tasks_df = pd.DataFrame(st.session_state.tasks)
    filtered_tasks = tasks_df[tasks_df['status'].isin(filter_status)]
    
    # Display each task as an editable card with compact layout
    for idx, task in filtered_tasks.iterrows():
        with st.container():
            st.divider()
            
            # Task details row with compact columns
            details_col1, details_col2, details_col3, details_col4, details_col5, details_col6 = st.columns([1.5, 1, 0.75, 0.75, 0.75, 0.75])
            
            with details_col1:
                st.markdown(f"**Parameter:** {task['parameter']}")
                st.markdown(f"**Value:** {task['value']}")
                
                # Task name dropdown
                task_name = st.selectbox(
                    "Task Name",
                    options=st.session_state.task_names,
                    index=st.session_state.task_names.index(task['task_name']) if task['task_name'] in st.session_state.task_names else 0,
                    key=f"task_name_{task['id']}"
                )
                if task_name != task['task_name']:
                    st.session_state.tasks[idx]['task_name'] = task_name
                    save_tasks()
                
                st.caption(f"Added: {task['timestamp']}")
            
            with details_col2:
                st.markdown("**Status**")
                new_status = st.selectbox(
                    "",
                    status_options,
                    index=status_options.index(task['status']),
                    key=f"status_{task['id']}",
                    label_visibility="collapsed"
                )
                if new_status != task['status']:
                    st.session_state.tasks[idx]['status'] = new_status
                    save_tasks()
            
            with details_col3:
                st.markdown("**Planned Hours**")
                planned_hours = st.number_input(
                    "",
                    min_value=0,
                    max_value=23,
                    value=task['planned_hours'],
                    key=f"ph_{task['id']}",
                    label_visibility="collapsed"
                )
            
            with details_col4:
                st.markdown("**Planned Min**")
                planned_minutes = st.selectbox(
                    "",
                    [0, 15, 30, 45],
                    index=[0, 15, 30, 45].index(task['planned_minutes']),
                    key=f"pm_{task['id']}",
                    label_visibility="collapsed"
                )
            
            with details_col5:
                st.markdown("**Actual Hours**")
                actual_hours = st.number_input(
                    "",
                    min_value=0,
                    max_value=23,
                    value=task['actual_hours'],
                    key=f"ah_{task['id']}",
                    label_visibility="collapsed"
                )
            
            with details_col6:
                st.markdown("**Actual Min**")
                actual_minutes = st.selectbox(
                    "",
                    [0, 15, 30, 45],
                    index=[0, 15, 30, 45].index(task['actual_minutes']),
                    key=f"am_{task['id']}",
                    label_visibility="collapsed"
                )
            
            # Add delete button in a separate column
            delete_col = st.columns([5.5, 0.5])[1]
            with delete_col:
                if st.button("Delete", key=f"delete_{task['id']}"):
                    st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                    save_tasks()
                    st.rerun()
            
            # Update times if changed
            if (planned_hours != task['planned_hours'] or 
                planned_minutes != task['planned_minutes'] or
                actual_hours != task['actual_hours'] or 
                actual_minutes != task['actual_minutes']):
                st.session_state.tasks[idx]['planned_hours'] = planned_hours
                st.session_state.tasks[idx]['planned_minutes'] = planned_minutes
                st.session_state.tasks[idx]['actual_hours'] = actual_hours
                st.session_state.tasks[idx]['actual_minutes'] = actual_minutes
                save_tasks()

    # Summary statistics
    st.subheader("Summary")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_tasks = len(st.session_state.tasks)
        st.metric("Total Tasks", total_tasks)
    
    with col2:
        completed_tasks = len([t for t in st.session_state.tasks if t['status'] == 'Completed'])
        st.metric("Completed Tasks", completed_tasks)
    
    with col3:
        completion_rate = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        st.metric("Completion Rate", f"{completion_rate:.1f}%")
    
    with col4:
        total_planned_hours = sum(
            t['planned_hours'] + t['planned_minutes']/60 
            for t in st.session_state.tasks
        )
        total_actual_hours = sum(
            t['actual_hours'] + t['actual_minutes']/60 
            for t in st.session_state.tasks
        )
        st.metric(
            "Actual vs Planned Hours",
            f"{total_actual_hours:.1f}h / {total_planned_hours:.1f}h"
        )

    # Clear all tasks button
    if st.button("Clear All Tasks"):
        st.session_state.tasks = []
        save_tasks()
        st.rerun()
