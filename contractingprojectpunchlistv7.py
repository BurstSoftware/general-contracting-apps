import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Set page configuration
st.set_page_config(page_title="Project Punch List", layout="wide")

# Initialize session state for storing tasks and settings
if 'tasks' not in st.session_state:
    st.session_state['tasks'] = []

if 'uploaded_data' not in st.session_state:
    st.session_state['uploaded_data'] = None

if 'selected_column' not in st.session_state:
    st.session_state['selected_column'] = None

if 'task_names' not in st.session_state:
    st.session_state['task_names'] = []

if 'tasks_loaded' not in st.session_state:
    st.session_state['tasks_loaded'] = False

# Load tasks from a JSON file if available
def load_tasks():
    if os.path.exists('tasks.json'):
        try:
            with open('tasks.json', 'r') as f:
                st.session_state['tasks'] = json.load(f)
        except Exception as e:
            st.error(f"Failed to load tasks: {e}")

# Save tasks to a JSON file
def save_tasks():
    try:
        with open('tasks.json', 'w') as f:
            json.dump(st.session_state['tasks'], f)
    except Exception as e:
        st.error(f"Failed to save tasks: {e}")

# Initial load of tasks
if not st.session_state['tasks_loaded']:
    load_tasks()
    st.session_state['tasks_loaded'] = True

# Main title
st.title("Project Punch List Manager")

# File upload and column selection section
with st.expander("Upload CSV File and Configure Tasks", expanded=True):
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state['uploaded_data'] = df
            st.success("File uploaded successfully!")

            # Column selection for task identification
            st.subheader("Select Task Column")
            selected_column = st.selectbox(
                "Choose the column to use for task identification",
                options=df.columns,
                key="column_selector"
            )
            st.session_state['selected_column'] = selected_column

            # Store unique task names from the selected column
            st.session_state['task_names'] = df[selected_column].unique().tolist()

            # Display the uploaded data with selectable rows
            st.subheader("Select Records for Tasks")
            selection_df = df.copy()
            selection_df.insert(0, "Select", False)

            # Editable DataFrame for selection
            edited_df = st.data_editor(
                selection_df,
                hide_index=True,
                use_container_width=True,
                key="task_selector"
            )

            # Button to create tasks from selected records
            if st.button("Create Tasks from Selected Records"):
                selected_rows = edited_df[edited_df["Select"]]

                for idx, row in selected_rows.iterrows():
                    new_task = {
                        "id": len(st.session_state['tasks']),
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
                    st.session_state['tasks'].append(new_task)

                save_tasks()
                st.success(f"Created {len(selected_rows)} new tasks!")
                
        except Exception as e:
            st.error(f"Error reading file: {e}")

# Task management section
if st.session_state['tasks']:
    st.subheader("Manage Tasks")

    # Define the available status options
    status_options = ["Not Started", "In Progress", "Completed", "Blocked"]
    filter_status = st.multiselect(
        "Filter by Status",
        status_options,
        default=status_options
    )

    # Create a DataFrame for display
    tasks_df = pd.DataFrame(st.session_state['tasks'])
    filtered_tasks = tasks_df[tasks_df['status'].isin(filter_status)]

    # Custom CSS for better alignment
    st.markdown(
        """
        <style>
        .stNumberInput > label, .stSelectbox > label {
            display: none;
        }
        .stSelectbox, .stNumberInput {
            margin-top: -10px;
        }
        div[data-testid="column"] {
            padding: 5px 10px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Header row for better alignment
    header_cols = st.columns([2, 1, 1, 1, 1, 1, 0.5])
    with header_cols[0]:
        st.markdown("**Task Name**")
    with header_cols[1]:
        st.markdown("**Status**")
    with header_cols[2]:
        st.markdown("**Planned Hours**")
    with header_cols[3]:
        st.markdown("**Planned Minutes**")
    with header_cols[4]:
        st.markdown("**Actual Hours**")
    with header_cols[5]:
        st.markdown("**Actual Minutes**")
    with header_cols[6]:
        st.markdown("**Delete**")

    # Display tasks with aligned inputs
    for idx, task in filtered_tasks.iterrows():
        st.divider()
        with st.container():
            cols = st.columns([2, 1, 1, 1, 1, 1, 0.5])

            # Task Name
            with cols[0]:
                task_name = st.selectbox(
                    "", 
                    options=st.session_state['task_names'],
                    index=st.session_state['task_names'].index(task['task_name']),
                    key=f"task_name_{task['id']}"
                )
                st.session_state['tasks'][task['id']]['task_name'] = task_name

            # Status
            with cols[1]:
                new_status = st.selectbox(
                    "", 
                    status_options,
                    index=status_options.index(task['status']),
                    key=f"status_{task['id']}"
                )
                st.session_state['tasks'][task['id']]['status'] = new_status

            # Planned Hours
            with cols[2]:
                planned_hours = st.number_input("", min_value=0, max_value=23, value=task['planned_hours'], key=f"planned_hours_{task['id']}")
                st.session_state['tasks'][task['id']]['planned_hours'] = planned_hours

            # Planned Minutes
            with cols[3]:
                planned_minutes = st.selectbox("", [0, 15, 30, 45], index=[0, 15, 30, 45].index(task['planned_minutes']), key=f"planned_minutes_{task['id']}")
                st.session_state['tasks'][task['id']]['planned_minutes'] = planned_minutes

            # Actual Hours
            with cols[4]:
                actual_hours = st.number_input("", min_value=0, max_value=23, value=task['actual_hours'], key=f"actual_hours_{task['id']}")
                st.session_state['tasks'][task['id']]['actual_hours'] = actual_hours

            # Actual Minutes
            with cols[5]:
                actual_minutes = st.selectbox("", [0, 15, 30, 45], index=[0, 15, 30, 45].index(task['actual_minutes']), key=f"actual_minutes_{task['id']}")
                st.session_state['tasks'][task['id']]['actual_minutes'] = actual_minutes

            # Delete button
            with cols[6]:
                if st.button("Delete", key=f"delete_{task['id']}"):
                    st.session_state['tasks'].remove(task.to_dict())
                    save_tasks()

    # Summary section
    st.subheader("Summary")
    total_tasks = len(st.session_state['tasks'])
    completed_tasks = len([t for t in st.session_state['tasks'] if t['status'] == 'Completed'])
    planned_total = sum(t['planned_hours'] + t['planned_minutes'] / 60 for t in st.session_state['tasks'])
    actual_total = sum(t['actual_hours'] + t['actual_minutes'] / 60 for t in st.session_state['tasks'])

    st.metric("Total Tasks", total_tasks)
    st.metric("Completed Tasks", completed_tasks)
    st.metric("Actual vs Planned", f"{actual_total:.1f}h / {planned_total:.1f}h")
