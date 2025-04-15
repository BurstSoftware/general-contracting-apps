import streamlit as st
import pandas as pd

def main():
    st.title("Concrete Restoration Project Pricing Tool")
    st.write("Enter the details of your concrete restoration project to estimate the total cost.")

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["Residential", "Commercial", "Industrial", "Municipal"]
    )

    restoration_service = st.selectbox(
        "Type of Concrete Restoration Service:",
        [
            "Concrete Resurfacing", "Crack Repair", "Spall Repair", "Concrete Leveling",
            "Joint Repair and Sealing", "Surface Grinding and Polishing", "Concrete Overlay",
            "Waterproofing and Sealing", "Reinforcement Corrosion Repair", "Structural Strengthening",
            "Concrete Staining and Coloring", "Pothole and Surface Patching", "Epoxy Flooring",
            "Removal and Replacement"
        ]
    )

    # Project Scope Inputs
    st.subheader("Project Scope")
    area_sqft = st.number_input("Area to Restore (Square Feet):", min_value=0, step=10)
    concrete_volume = st.number_input("Volume of Concrete Needed (Cubic Yards):", min_value=0.0, format="%.2f", step=0.1)

    # Material Inputs
    st.subheader("Materials")
    overlay_cost_per_sqft = st.number_input("Cost per Sqft of Overlay/Resurfacing Material ($):", min_value=0.0, format="%.2f", step=0.1)
    concrete_cost_per_cubic_yard = st.number_input("Cost per Cubic Yard of Concrete ($):", min_value=0.0, format="%.2f", step=10.0)
    sealant_cost = st.number_input("Cost of Sealant/Waterproofing Materials ($):", min_value=0.0, format="%.2f", step=5.0)
    repair_materials_cost = st.number_input("Cost of Repair Materials (Epoxy, Patches, etc.) ($):", min_value=0.0, format="%.2f", step=5.0)
    reinforcement_cost = st.number_input("Cost of Reinforcement Materials (Rebar, Carbon Fiber) ($):", min_value=0.0, format="%.2f", step=10.0)
    misc_materials_cost = st.number_input("Cost of Miscellaneous Materials (Gravel, Formwork, etc.) ($):", min_value=0.0, format="%.2f", step=5.0)

    # Labor Inputs
    st.subheader("Labor")
    num_workers = st.number_input("Number of Workers:", min_value=1, step=1)
    hours_per_worker = st.number_input("Hours per Worker:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate_worker = st.number_input("Hourly Rate per Worker ($):", min_value=0.0, format="%.2f", step=1.0)

    # Equipment Costs
    st.subheader("Equipment")
    equipment_rental_cost = st.number_input("Equipment Rental Costs (Grinders, Mixers, etc.) ($):", min_value=0.0, format="%.2f", step=10.0)

    # Permits and Inspections
    st.subheader("Permits and Inspections")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    inspection_cost = st.number_input("Inspection Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=15, step=1)
    contingency_percentage = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs
        total_overlay_cost = area_sqft * overlay_cost_per_sqft
        total_concrete_cost = concrete_volume * concrete_cost_per_cubic_yard
        total_material_cost = (total_overlay_cost + total_concrete_cost + sealant_cost + 
                              repair_materials_cost + reinforcement_cost + misc_materials_cost)

        # Calculate labor costs
        total_labor_hours = num_workers * hours_per_worker
        total_labor_cost = total_labor_hours * hourly_rate_worker

        # Calculate equipment, permits, and inspection costs
        total_additional_costs = equipment_rental_cost + permit_cost + inspection_cost

        # Calculate subtotal
        subtotal = total_material_cost + total_labor_cost + total_additional_costs

        # Calculate markup and contingency
        markup_amount = subtotal * (markup_percentage / 100)
        contingency_amount = subtotal * (contingency_percentage / 100)

        # Calculate final total
        total_cost = subtotal + markup_amount + contingency_amount

        # Create summary DataFrame
        summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Restoration Service",
                "Area to Restore (Sqft)",
                "Concrete Volume (Cubic Yards)",
                "Number of Workers",
                "Total Labor Hours",
                "Material Costs ($)",
                "Labor Costs ($)",
                "Equipment Costs ($)",
                "Permits and Inspections ($)",
                "Subtotal ($)",
                f"Markup ({markup_percentage}%) ($)",
                f"Contingency ({contingency_percentage}%) ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                project_type,
                restoration_service,
                area_sqft,
                concrete_volume,
                num_workers,
                total_labor_hours,
                round(total_material_cost, 2),
                round(total_labor_cost, 2),
                round(equipment_rental_cost, 2),
                round(permit_cost + inspection_cost, 2),
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
            file_name="concrete_restoration_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
