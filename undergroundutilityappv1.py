import streamlit as st
import pandas as pd

def main():
    st.title("Underground Utility Locating Cost Estimator")
    st.write("Enter the details of your underground utility locating project to get an estimated cost.")

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["Private Property", "Public Roadway", "Construction Site", "Industrial Area", "Commercial Area"]
    )

    building_type = st.selectbox(
        "Site Type:",
        ["Residential", "Commercial", "Industrial", "Educational", "Agricultural"]
    )

    total_square_footage = st.number_input("Total Site Area (Square Feet):", min_value=0, step=100)

    # Utility and Detection Methods
    st.subheader("Utility Types and Detection Methods")

    # Utility types selection
    utility_types = st.multiselect(
        "Select Utility Types to Locate:",
        ["Gas Lines", "Water Lines", "Sewer Lines", "Electric Cables", "Telecom Cables", "Fiber Optic Cables", "Oil Pipelines"]
    )

    # Detection method based on utility types
    detection_methods = {
        "Gas Lines": ["Electromagnetic", "Ground Penetrating Radar (GPR)", "Acoustic Detection"],
        "Water Lines": ["Electromagnetic", "Acoustic Detection", "GPR"],
        "Sewer Lines": ["GPR", "Electromagnetic", "Acoustic Detection"],
        "Electric Cables": ["Electromagnetic", "Induction Locators"],
        "Telecom Cables": ["Electromagnetic", "GPR"],
        "Fiber Optic Cables": ["Electromagnetic", "GPR"],
        "Oil Pipelines": ["Electromagnetic", "GPR", "Magnetic Locator"]
    }

    selected_detection_methods = set()
    for utility in utility_types:
        methods = detection_methods.get(utility, [])
        selected_method = st.selectbox(f"Detection Method for {utility}:", methods)
        selected_detection_methods.add(selected_method)

    service_depth = st.number_input("Estimated Depth of Utilities (Feet):", min_value=0.0, step=0.5)

    # Cost Inputs
    st.subheader("Cost Estimations")

    # Equipment and Material Costs
    equipment_rental = st.number_input("Equipment Rental Cost per Day ($):", min_value=0.0, format="%.2f", step=10.0)
    num_days_rented = st.number_input("Number of Days for Equipment Rental:", min_value=0, step=1)
    materials_cost = st.number_input("Additional Materials Cost ($):", min_value=0.0, format="%.2f", step=10.0)

    # Labor Inputs
    st.subheader("Labor")
    num_technicians = st.number_input("Number of Technicians:", min_value=1, step=1)
    hours_per_tech = st.number_input("Hours per Technician per Day:", min_value=0.0, format="%.2f", step=0.5)
    num_days_worked = st.number_input("Total Days of Work:", min_value=1, step=1)
    hourly_rate = st.number_input("Hourly Rate per Technician ($):", min_value=0.0, format="%.2f", step=0.5)

    # Permits and Insurance
    st.subheader("Permits and Insurance")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    insurance_cost = st.number_input("Insurance Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material and equipment costs
        total_equipment_cost = equipment_rental * num_days_rented
        total_materials = total_equipment_cost + materials_cost

        # Calculate labor costs
        total_labor_hours = num_technicians * hours_per_tech * num_days_worked
        total_labor_cost = total_labor_hours * hourly_rate

        # Calculate permit and insurance costs
        total_permit_insurance = permit_cost + insurance_cost

        # Calculate subtotal
        subtotal = total_materials + total_labor_cost + total_permit_insurance

        # Calculate markup and contingency
        markup_amount = subtotal * (markup_percentage / 100)
        contingency_amount = subtotal * (contingency / 100)

        # Calculate final total
        total_cost = subtotal + markup_amount + contingency_amount

        # Create summary DataFrame
        summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Site Type",
                "Total Site Area (Square Feet)",
                "Utility Types",
                "Detection Methods",
                "Estimated Depth (Feet)",
                "Equipment Rental Cost ($)",
                "Materials Cost ($)",
                "Number of Technicians",
                "Total Labor Hours",
                "Labor Cost ($)",
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
                ", ".join(utility_types),
                ", ".join(selected_detection_methods),
                service_depth,
                round(total_equipment_cost, 2),
                round(materials_cost, 2),
                num_technicians,
                round(total_labor_hours, 2),
                round(total_labor_cost, 2),
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
            file_name="underground_utility_locating_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
