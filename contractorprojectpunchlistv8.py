import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# Constants
STATUS_OPTIONS = ["Not Started", "In Progress", "Completed", "Blocked"]
TIME_INTERVALS = [0, 15, 30, 45]
COLUMN_WIDTHS = [1, 3, 1, 0.5, 0.5, 0.5, 0.5, 0.6]
HEADERS = ["ID", "Task Name", "Status", "Plan Hrs", "Plan Min", "Act Hrs", "Act Min", "Delete"]

# Page Configuration
st.set_page_config(page_title="Project Punch List", layout="wide")

# Initialize session state
def init_session_state():
    """Initialize all session state variables"""
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

def load_tasks():
    """Load tasks from JSON file"""
    if os.path.exists('tasks.json'):
        try:
            with open('tasks.json', 'r') as f:
                st.session_state['tasks'] = json.load(f)
        except Exception as e:
            st.error(f"Failed to load tasks: {e}")

def save_tasks():
    """Save tasks to JSON file"""
    try:
        with open('tasks.json', 'w') as f:
            json.dump(st.session_state['tasks'], f)
    except Exception as e:
        st.error(f"Failed to save tasks: {e}")

def update_task_field(task_id, field, value):
    """Update a single field in the task state"""
    if task_id < len(st.session_state['tasks']):
        st.session_state['tasks'][task_id][field] = value
        save_tasks()

def delete_task(task_id):
    """Delete a task and update state"""
    task_dict = next((task for task in st.session_state['tasks'] if task['id'] == task_id), None)
    if task_dict:
        st.session_state['tasks'].remove(task_dict)
        save_tasks()

def apply_custom_styles():
    """Apply custom CSS styles"""
    st.markdown("""
        <style>
        .stNumberInput > label, .stSelectbox > label {
            display: none;
        }
        .stSelectbox, .stNumberInput {
            margin-top: -10px;
        }
        div[data-testid="column"] {
            padding: 3px 3px;
        }
        button[kind="primary"] {
            width: 100%;
            margin-top: 1px;
        }
        .compact-input {
            min-width: 60px !important;
        }
        .stDataFrame {
            margin-top: 20px;
        }
        </style>
    """, unsafe_allow_html=True)

def handle_file_upload():
    """Handle CSV file upload and processing"""
    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.session_state['uploaded_data'] = df
            st.success("File uploaded successfully!")

            # Column selection
            st.subheader("Select Task Column")
            selected_column = st.selectbox(
                "Choose the column to use for task identification",
                options=df.columns,
                key="column_selector"
            )
            st.session_state['selected_column'] = selected_column
            st.session_state['task_names'] = df[selected_column].unique().tolist()

            # Data selection interface
            st.subheader("Select Records for Tasks")
            selection_df = df.copy()
            selection_df.insert(0, "Select", False)
            
            edited_df = st.data_editor(
                selection_df,
                hide_index=True,
                use_container_width=True,
                key="task_selector"
            )

            if st.button("Create Tasks from Selected Records"):
                create_tasks_from_selection(edited_df, selected_column)

        except Exception as e:
            st.error(f"Error reading file: {e}")

def create_tasks_from_selection(edited_df, selected_column):
    """Create new tasks from selected records"""
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

def render_task_management():
    """Render the task management interface"""
    if not st.session_state['tasks']:
        return

    st.subheader("Manage Tasks")

    # Status filter
    filter_status = st.multiselect(
        "Filter by Status",
        STATUS_OPTIONS,
        default=STATUS_OPTIONS
    )

    # Create filtered DataFrame
    tasks_df = pd.DataFrame(st.session_state['tasks'])
    filtered_tasks = tasks_df[tasks_df['status'].isin(filter_status)]

    # Render headers
    header_cols = st.columns(COLUMN_WIDTHS)
    for col, header in zip(header_cols, HEADERS):
        col.markdown(f"**{header}**")

    # Render tasks
    for idx, task in filtered_tasks.iterrows():
        st.divider()
        task_id = task['id']
        cols = st.columns(COLUMN_WIDTHS)

        # ID Column
        cols[0].text(task_id)

        # Task Name
        with cols[1]:
            task_name = st.selectbox(
                "",
                options=st.session_state['task_names'],
                index=st.session_state['task_names'].index(task['task_name']),
                key=f"task_name_{task_id}"
            )
            update_task_field(task_id, 'task_name', task_name)

        # Status
        with cols[2]:
            new_status = st.selectbox(
                "",
                STATUS_OPTIONS,
                index=STATUS_OPTIONS.index(task['status']),
                key=f"status_{task_id}"
            )
            update_task_field(task_id, 'status', new_status)

        # Time inputs
        time_fields = [
            ('planned_hours', 23),
            ('planned_minutes', TIME_INTERVALS),
            ('actual_hours', 23),
            ('actual_minutes', TIME_INTERVALS)
        ]

        for idx, (field, max_val) in enumerate(time_fields):
            col_idx = idx + 3
            if isinstance(max_val, list):
                new_val = cols[col_idx].selectbox(
                    "",
                    max_val,
                    index=max_val.index(task[field]),
                    key=f"{field}_{task_id}",
                    label_visibility="hidden"
                )
            else:
                new_val = cols[col_idx].number_input(
                    "",
                    min_value=0,
                    max_value=max_val,
                    value=task[field],
                    key=f"{field}_{task_id}",
                    label_visibility="hidden"
                )
            update_task_field(task_id, field, new_val)

        # Delete button
        if cols[7].button("Delete", key=f"delete_{task_id}", use_container_width=True, help="Delete this task"):
            delete_task(task_id)

def render_summary():
    """Render the summary section"""
    st.subheader("Summary")
    total_tasks = len(st.session_state['tasks'])
    completed_tasks = len([t for t in st.session_state['tasks'] if t['status'] == 'Completed'])
    planned_total = sum(t['planned_hours'] + t['planned_minutes'] / 60 for t in st.session_state['tasks'])
    actual_total = sum(t['actual_hours'] + t['actual_minutes'] / 60 for t in st.session_state['tasks'])

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Tasks", total_tasks)
    with col2:
        st.metric("Completed Tasks", completed_tasks)
    with col3:
        st.metric("Actual vs Planned", f"{actual_total:.1f}h / {planned_total:.1f}h")

def main():
    """Main application function"""
    # Initialize
    init_session_state()
    if not st.session_state['tasks_loaded']:
        load_tasks()
        st.session_state['tasks_loaded'] = True

    # Apply custom styles
    apply_custom_styles()

    # Page title
    st.title("Project Punch List Manager")

    # File upload section
    with st.expander("Upload CSV File and Configure Tasks", expanded=True):
        handle_file_upload()

    # Task management section
    render_task_management()

    # Summary section
    render_summary()

if __name__ == "__main__":
    main()
