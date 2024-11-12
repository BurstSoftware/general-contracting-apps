import streamlit as st
import pandas as pd

# Main function for the Streamlit application
def main():
    st.title("Comprehensive Drywall Project Cost Estimator")
    st.write("Enter the details of your drywall project below to get an estimated cost.")

    # User Inputs
    price_per_sheet = st.number_input("Enter the price per drywall sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    num_of_sheets = st.number_input("Enter the number of drywall sheets:", min_value=0, step=1)
    num_of_cuts = st.number_input("Enter the number of cuts required:", min_value=0, step=1)
    hours_of_labor = st.number_input("Enter the hours of labor required:", min_value=0.0, format="%.2f", step=0.5)
    labor_rate = st.number_input("Enter the hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)

    # New Inputs for Additional Costs
    screw_cost = st.number_input("Enter the cost of screws/nails per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    tape_mud_cost = st.number_input("Enter the cost of joint compound (mud) per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    drywall_tape_cost = st.number_input("Enter the cost of drywall tape per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    primer_paint_cost = st.number_input("Enter the cost of primer and paint per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    floor_prep_cost = st.number_input("Enter the cost of floor/room prep materials ($):", min_value=0.0, format="%.2f", step=0.5)
    waste_factor = st.slider("Select the waste factor (%)", min_value=0, max_value=20, value=10, step=1)

    # Button to calculate the cost
    if st.button("Calculate Total Cost"):
        effective_num_of_sheets = num_of_sheets * (1 + waste_factor / 100)

        # Calculate costs
        total_material_cost = price_per_sheet * effective_num_of_sheets
        total_screw_cost = screw_cost * effective_num_of_sheets
        total_tape_mud_cost = tape_mud_cost * effective_num_of_sheets
        total_drywall_tape_cost = drywall_tape_cost * effective_num_of_sheets
        total_paint_cost = primer_paint_cost * effective_num_of_sheets
        total_installation_materials = (total_screw_cost + total_tape_mud_cost + 
                                        total_drywall_tape_cost + total_paint_cost + floor_prep_cost)
        total_labor_cost = hours_of_labor * labor_rate
        total_cost = total_material_cost + total_installation_materials + total_labor_cost

        # Display Cost Summary
        st.subheader("Estimated Total Project Cost: ${:.2f}".format(total_cost))

    # Punch List Section
    st.subheader("Project Punch List")
    
    # Initialize punch list DataFrame
    punch_list_columns = ["Task", "Phase", "Assigned Worker", "Status"]
    default_punch_list = pd.DataFrame(columns=punch_list_columns)
    
    # File Upload for Punch List
    uploaded_file = st.file_uploader("Upload a CSV Punch List", type="csv")
    if uploaded_file:
        default_punch_list = pd.read_csv(uploaded_file)

    # Input fields for punch list entries
    task = st.text_input("Task Description")
    phase = st.selectbox("Project Phase", 
                         ["Drywall Installation", "Taping/Mudding", 
                          "Priming/Painting", "Preparation", "Final Inspection"])
    assigned_worker = st.text_input("Assigned Worker")
    status = st.selectbox("Status", ["Pending", "In Progress", "Completed"])

    # Add task button
    if st.button("Add Task"):
        new_task = {
            "Task": task,
            "Phase": phase,
            "Assigned Worker": assigned_worker,
            "Status": status
        }
        default_punch_list = default_punch_list.append(new_task, ignore_index=True)
        st.success(f"Task '{task}' added to the punch list!")

    # Display the punch list
    st.dataframe(default_punch_list)

    # Allow users to download the punch list
    if not default_punch_list.empty:
        csv_punch_list = default_punch_list.to_csv(index=False)
        st.download_button(
            label="Download Punch List as CSV",
            data=csv_punch_list,
            file_name="project_punch_list.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
