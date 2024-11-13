import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Set page configuration
st.set_page_config(page_title="Project Punch List", layout="wide")

# Initialize session state for tasks and configuration settings
if 'tasks' not in st.session_state:
    st.session_state.tasks = []

if 'uploaded_data' not in st.session_state:
    st.session_state.uploaded_data = None

if 'selected_column' not in st.session_state:
    st.session_state.selected_column = None

if 'task_names' not in st.session_state:
    st.session_state.task_names = []

def save_tasks():
    """Save tasks to a JSON file."""
    with open('tasks.json', 'w') as f:
        json.dump(st.session_state.tasks, f)

def load_tasks():
    """Load tasks from JSON file if it exists."""
    if os.path.exists('tasks.json'):
        with open('tasks.json', 'r') as f:
            st.session_state.tasks = json.load(f)

# Load existing tasks at the start of the app
if 'tasks_loaded' not in st.session_state:
    load_tasks()
    st.session_state.tasks_loaded = True

# Main title
st.title("Project Punch List Manager")

# File upload and configuration section
with st.expander("Upload CSV File and Configure Tasks", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state.uploaded_data = df
            st.success("File uploaded successfully!")

            # Column selection for task identification
            selected_column = st.selectbox(
                "Select the column to use for task identification",
                options=df.columns,
                key="column_selector"
            )
            st.session_state.selected_column = selected_column
            st.session_state.task_names = df[selected_column].unique().tolist()

            # Create a DataFrame with selection checkboxes
            df['Select'] = False
            edited_df = st.data_editor(
                df,
                hide_index=True,
                use_container_width=True,
                key="task_selector"
            )

            # Create tasks from selected rows
            if st.button("Create Tasks from Selected Records"):
                selected_rows = edited_df[edited_df['Select']]
                for idx, row in selected_rows.iterrows():
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

# Task Management Section
if st.session_state.tasks:
    st.subheader("Manage Tasks")

    # Filter and sorting options
    filter_status = st.multiselect(
        "Filter by Status",
        ["Not Started", "In Progress", "Completed", "Blocked"],
        default=["Not Started", "In Progress", "Completed", "Blocked"]
    )
    sort_by = st.selectbox(
        "Sort Tasks By",
        ["Timestamp", "Task Name", "Status"]
    )

    # Create DataFrame from tasks for easier manipulation
    tasks_df = pd.DataFrame(st.session_state.tasks)
    filtered_tasks = tasks_df[tasks_df['status'].isin(filter_status)]

    # Sorting the tasks based on user selection
    if sort_by == "Task Name":
        filtered_tasks = filtered_tasks.sort_values(by="task_name")
    elif sort_by == "Status":
        filtered_tasks = filtered_tasks.sort_values(by="status")
    else:
        filtered_tasks = filtered_tasks.sort_values(by="timestamp")

    # Display each task as an editable card
    for idx, task in filtered_tasks.iterrows():
        with st.container():
            st.divider()
            # Task details in a structured layout
            col1, col2, col3, col4, col5, col6, delete_col = st.columns([2, 1.5, 1, 1, 1, 1, 0.5])

            # Task Name Dropdown
            with col1:
                st.markdown(f"**Parameter:** {task['parameter']} | **Value:** {task['value']}")
                task_name = st.selectbox(
                    "Task Name",
                    st.session_state.task_names,
                    index=st.session_state.task_names.index(task['task_name']),
                    key=f"task_name_{task['id']}"
                )
                if task_name != task['task_name']:
                    st.session_state.tasks[idx]['task_name'] = task_name
                    save_tasks()

            # Status Dropdown
            with col2:
                new_status = st.selectbox(
                    "Status",
                    ["Not Started", "In Progress", "Completed", "Blocked"],
                    index=["Not Started", "In Progress", "Completed", "Blocked"].index(task['status']),
                    key=f"status_{task['id']}"
                )
                if new_status != task['status']:
                    st.session_state.tasks[idx]['status'] = new_status
                    save_tasks()

            # Time Inputs
            planned_hours = st.number_input(
                "Planned Hours",
                min_value=0,
                max_value=23,
                value=task['planned_hours'],
                key=f"ph_{task['id']}"
            )
            planned_minutes = st.selectbox(
                "Planned Minutes",
                [0, 15, 30, 45],
                index=[0, 15, 30, 45].index(task['planned_minutes']),
                key=f"pm_{task['id']}"
            )
            actual_hours = st.number_input(
                "Actual Hours",
                min_value=0,
                max_value=23,
                value=task['actual_hours'],
                key=f"ah_{task['id']}"
            )
            actual_minutes = st.selectbox(
                "Actual Minutes",
                [0, 15, 30, 45],
                index=[0, 15, 30, 45].index(task['actual_minutes']),
                key=f"am_{task['id']}"
            )

            # Save updates
            if st.button("Update", key=f"update_{task['id']}"):
                st.session_state.tasks[idx]['planned_hours'] = planned_hours
                st.session_state.tasks[idx]['planned_minutes'] = planned_minutes
                st.session_state.tasks[idx]['actual_hours'] = actual_hours
                st.session_state.tasks[idx]['actual_minutes'] = actual_minutes
                save_tasks()
                st.success(f"Task {task['id']} updated!")

            # Delete Task
            if st.button("Delete", key=f"delete_{task['id']}"):
                st.session_state.tasks = [t for t in st.session_state.tasks if t['id'] != task['id']]
                save_tasks()
                st.experimental_rerun()

    # Summary Section
    st.subheader("Summary")
    total_tasks = len(st.session_state.tasks)
    completed_tasks = len([t for t in st.session_state.tasks if t['status'] == "Completed"])
    planned_hours = sum(t['planned_hours'] + t['planned_minutes'] / 60 for t in st.session_state.tasks)
    actual_hours = sum(t['actual_hours'] + t['actual_minutes'] / 60 for t in st.session_state.tasks)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Tasks", total_tasks)
    col2.metric("Completed Tasks", completed_tasks)
    col3.metric("Completion Rate", f"{(completed_tasks / total_tasks * 100):.1f}%" if total_tasks else "0%")
    col4.metric("Actual vs Planned Hours", f"{actual_hours:.1f} / {planned_hours:.1f}")

# Clear all tasks button
if st.button("Clear All Tasks"):
    st.session_state.tasks = []
    save_tasks()
    st.experimental_rerun()
