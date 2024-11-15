import streamlit as st
import pandas as pd

def main():
    st.title("Landscaping Project Cost Estimator")
    st.write("Enter the details of your landscaping project below to get an estimated cost.")

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["Lawn Installation", "Garden Design", "Hardscaping", "Irrigation System", 
         "Tree Services", "Landscape Lighting", "Maintenance"]
    )
    
    property_type = st.selectbox(
        "Property Type:",
        ["Residential", "Commercial", "Municipal", "Educational", 
         "Industrial", "Resort/Hotel"]
    )

    total_square_footage = st.number_input("Total Project Area (Square Feet):", min_value=0, step=100)

    # Materials selection based on project type
    st.subheader("Materials")
    
    materials_types = {
        "Lawn Installation": ["Sod", "Grass Seed", "Topsoil", "Fertilizer"],
        "Garden Design": ["Plants", "Mulch", "Decorative Stone", "Soil Amendment"],
        "Hardscaping": ["Pavers", "Natural Stone", "Gravel", "Concrete"],
        "Irrigation System": ["PVC Pipes", "Sprinkler Heads", "Controllers", "Valves"],
        "Tree Services": ["Trees", "Support Stakes", "Mulch", "Soil Amendment"],
        "Landscape Lighting": ["LED Fixtures", "Wiring", "Transformers", "Controls"],
        "Maintenance": ["Fertilizer", "Mulch", "Replacement Plants", "Pest Control"]
    }
    
    material_type = st.selectbox(
        "Primary Material Type:",
        materials_types[project_type]
    )
    
    # Material quantities and costs
    material_quantity = st.number_input("Material Quantity (Units/Square Feet):", min_value=0, step=10)
    cost_per_unit = st.number_input("Cost per Unit ($):", min_value=0.0, format="%.2f", step=0.1)

    # Equipment and supplies based on project type
    st.subheader("Equipment and Supplies")
    
    if project_type == "Lawn Installation":
        soil_prep_sqft = st.number_input("Square Feet Requiring Soil Preparation:", min_value=0, step=100)
        irrigation_needs = st.number_input("Temporary Irrigation Equipment Cost ($):", min_value=0.0, step=10.0)
        grading_equipment = st.number_input("Grading Equipment Cost ($):", min_value=0.0, step=10.0)
    elif project_type == "Hardscaping":
        base_material_tons = st.number_input("Base Material Required (Tons):", min_value=0.0, step=0.5)
        equipment_rental = st.number_input("Equipment Rental Cost ($):", min_value=0.0, step=10.0)
        tools_cost = st.number_input("Specialized Tools Cost ($):", min_value=0.0, step=10.0)
    elif project_type == "Irrigation System":
        pipe_length = st.number_input("Total Pipe Length (Feet):", min_value=0, step=50)
        num_heads = st.number_input("Number of Sprinkler Heads:", min_value=0, step=1)
        control_units = st.number_input("Number of Control Units:", min_value=0, step=1)
    
    # Additional Materials
    st.subheader("Additional Materials")
    soil_amendments = st.number_input("Soil Amendments Cost ($):", min_value=0.0, format="%.2f", step=10.0)
    drainage_materials = st.number_input("Drainage Materials Cost ($):", min_value=0.0, format="%.2f", step=10.0)
    misc_supplies = st.number_input("Miscellaneous Supplies ($):", min_value=0.0, format="%.2f", step=10.0)

    # Labor Inputs
    st.subheader("Labor")
    num_workers = st.number_input("Number of Workers:", min_value=1, step=1)
    hours_per_worker = st.number_input("Hours per Worker:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Hourly Rate per Worker ($):", min_value=0.0, format="%.2f", step=0.5)

    # Equipment
    st.subheader("Equipment")
    equipment_hours = st.number_input("Heavy Equipment Hours:", min_value=0.0, format="%.2f", step=0.5)
    equipment_rate = st.number_input("Equipment Rate per Hour ($):", min_value=0.0, format="%.2f", step=10.0)

    # Permits and Insurance
    st.subheader("Permits and Insurance")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    insurance_cost = st.number_input("Insurance Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs
        total_material_cost = material_quantity * cost_per_unit
        total_materials = (total_material_cost + soil_amendments + 
                         drainage_materials + misc_supplies)

        # Calculate labor costs
        total_labor_hours = num_workers * hours_per_worker
        total_labor_cost = total_labor_hours * hourly_rate

        # Calculate equipment costs
        total_equipment_cost = equipment_hours * equipment_rate

        # Calculate permit and insurance costs
        total_permit_insurance = permit_cost + insurance_cost

        # Calculate subtotal
        subtotal = total_materials + total_labor_cost + total_equipment_cost + total_permit_insurance

        # Calculate markup and contingency
        markup_amount = subtotal * (markup_percentage / 100)
        contingency_amount = subtotal * (contingency / 100)

        # Calculate final total
        total_cost = subtotal + markup_amount + contingency_amount

        # Create summary DataFrame
        summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Property Type",
                "Total Project Area (sq ft)",
                "Material Type",
                "Material Quantity",
                "Number of Workers",
                "Total Labor Hours",
                "Equipment Hours",
                "Material Cost ($)",
                "Soil Amendments ($)",
                "Drainage Materials ($)",
                "Miscellaneous Supplies ($)",
                "Total Materials Cost ($)",
                "Labor Cost ($)",
                "Equipment Cost ($)",
                "Permits and Insurance ($)",
                "Subtotal ($)",
                f"Markup ({markup_percentage}%) ($)",
                f"Contingency ({contingency}%) ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                project_type,
                property_type,
                total_square_footage,
                material_type,
                material_quantity,
                num_workers,
                total_labor_hours,
                equipment_hours,
                round(total_material_cost, 2),
                round(soil_amendments, 2),
                round(drainage_materials, 2),
                round(misc_supplies, 2),
                round(total_materials, 2),
                round(total_labor_cost, 2),
                round(total_equipment_cost, 2),
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
            file_name="landscaping_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
