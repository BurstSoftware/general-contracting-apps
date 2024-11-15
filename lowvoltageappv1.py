import streamlit as st
import pandas as pd

def main():
    st.title("Low Voltage Project Cost Estimator")
    st.write("Enter the details of your low voltage project below to get an estimated cost.")

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["Network Cabling", "Security Cameras", "Access Control", "Audio/Visual", 
         "Intercom Systems", "Fire Alarm", "Structured Cabling"]
    )
    
    building_type = st.selectbox(
        "Building Type:",
        ["Commercial Office", "Educational", "Healthcare", "Industrial", 
         "Retail", "Residential", "Data Center"]
    )

    total_square_footage = st.number_input("Total Square Footage:", min_value=0, step=100)

    # Cable and Equipment Inputs
    st.subheader("Cables and Equipment")
    
    # Dynamic cable selection based on project type
    cable_types = {
        "Network Cabling": ["Cat5e", "Cat6", "Cat6a", "Fiber Optic"],
        "Security Cameras": ["Coaxial", "Cat6", "Fiber Optic"],
        "Access Control": ["22/4 Stranded", "22/6 Stranded", "18/4 Stranded"],
        "Audio/Visual": ["Speaker Wire", "HDMI", "Control Cable"],
        "Intercom Systems": ["22/2 Stranded", "Cat5e", "Coaxial"],
        "Fire Alarm": ["16/2 FPLR", "14/2 FPLR", "18/2 FPLR"],
        "Structured Cabling": ["Cat5e", "Cat6", "Cat6a", "Fiber Optic"]
    }
    
    cable_type = st.selectbox(
        "Cable Type:",
        cable_types[project_type]
    )
    
    cable_length = st.number_input("Total Cable Length Needed (Feet):", min_value=0, step=50)
    cost_per_foot = st.number_input("Cost per Foot ($):", min_value=0.0, format="%.2f", step=0.1)

    # Equipment counts based on project type
    st.subheader("Equipment and Terminations")
    
    if project_type == "Network Cabling":
        num_drops = st.number_input("Number of Network Drops:", min_value=0, step=1)
        num_patches = st.number_input("Number of Patch Panels:", min_value=0, step=1)
        num_racks = st.number_input("Number of Equipment Racks:", min_value=0, step=1)
    elif project_type == "Security Cameras":
        num_cameras = st.number_input("Number of Cameras:", min_value=0, step=1)
        num_nvr = st.number_input("Number of NVR/DVR Units:", min_value=0, step=1)
        num_monitors = st.number_input("Number of Monitors:", min_value=0, step=1)
    elif project_type == "Access Control":
        num_doors = st.number_input("Number of Doors:", min_value=0, step=1)
        num_readers = st.number_input("Number of Card Readers:", min_value=0, step=1)
        num_controllers = st.number_input("Number of Controllers:", min_value=0, step=1)
    
    # Common equipment costs
    equipment_cost = st.number_input("Total Equipment Cost ($):", min_value=0.0, format="%.2f", step=10.0)
    connector_cost = st.number_input("Total Connector/Termination Cost ($):", min_value=0.0, format="%.2f", step=0.5)
    
    # Additional Materials
    st.subheader("Additional Materials")
    mounting_hardware = st.number_input("Mounting Hardware Cost ($):", min_value=0.0, format="%.2f", step=0.5)
    cable_management = st.number_input("Cable Management Materials ($):", min_value=0.0, format="%.2f", step=0.5)
    misc_materials = st.number_input("Miscellaneous Materials ($):", min_value=0.0, format="%.2f", step=0.5)

    # Labor Inputs
    st.subheader("Labor")
    num_technicians = st.number_input("Number of Technicians:", min_value=1, step=1)
    hours_per_tech = st.number_input("Hours per Technician:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Hourly Rate per Technician ($):", min_value=0.0, format="%.2f", step=0.5)

    # Testing and Certification
    st.subheader("Testing and Certification")
    testing_hours = st.number_input("Testing Hours:", min_value=0.0, format="%.2f", step=0.5)
    certification_cost = st.number_input("Certification Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Permits and Insurance
    st.subheader("Permits and Insurance")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    insurance_cost = st.number_input("Insurance Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs
        total_cable_cost = cable_length * cost_per_foot
        total_materials = (total_cable_cost + equipment_cost + connector_cost + 
                         mounting_hardware + cable_management + misc_materials)

        # Calculate labor costs
        total_labor_hours = num_technicians * hours_per_tech
        total_labor_cost = total_labor_hours * hourly_rate

        # Calculate testing costs
        testing_cost = testing_hours * hourly_rate + certification_cost

        # Calculate permit and insurance costs
        total_permit_insurance = permit_cost + insurance_cost

        # Calculate subtotal
        subtotal = total_materials + total_labor_cost + testing_cost + total_permit_insurance

        # Calculate markup and contingency
        markup_amount = subtotal * (markup_percentage / 100)
        contingency_amount = subtotal * (contingency / 100)

        # Calculate final total
        total_cost = subtotal + markup_amount + contingency_amount

        # Create summary DataFrame
        summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Building Type",
                "Total Square Footage",
                "Cable Type",
                "Total Cable Length (Feet)",
                "Number of Technicians",
                "Total Labor Hours",
                "Cable Cost ($)",
                "Equipment Cost ($)",
                "Connector/Termination Cost ($)",
                "Mounting Hardware ($)",
                "Cable Management ($)",
                "Miscellaneous Materials ($)",
                "Total Materials Cost ($)",
                "Labor Cost ($)",
                "Testing and Certification ($)",
                "Permits and Insurance ($)",
                "Subtotal ($)",
                f"Markup ({markup_percentage}%) ($)",
                f"Contingency ({contingency}%) ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                project_type,
                building_type,
                total_square_footage,
                cable_type,
                cable_length,
                num_technicians,
                total_labor_hours,
                round(total_cable_cost, 2),
                round(equipment_cost, 2),
                round(connector_cost, 2),
                round(mounting_hardware, 2),
                round(cable_management, 2),
                round(misc_materials, 2),
                round(total_materials, 2),
                round(total_labor_cost, 2),
                round(testing_cost, 2),
                round(total_permit_insurance, 2),
                round(subtotal, 2),
                round(markup_amount, 2),
                round(contingency_amount, 2),
                round(total_cost, 2)
            ]
        })

        # Display project summary
        st.subheader("Project Summary and Cost Breakdown")
        st.dataframe(summary, width=600)

        # Download option
        csv_output = summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="low_voltage_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
