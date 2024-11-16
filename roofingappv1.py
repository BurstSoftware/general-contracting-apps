import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Roofing Project Cost Estimator")
    st.write("Enter the details of your roofing project below to get an estimated cost.")

    # Project Basics
    st.subheader("Project Basics")
    roofing_type = st.selectbox(
        "Select Roofing Trade:",
        ["Shingler", "Flat Roofer", "Metal Roofer"]
    )

    roof_area = st.number_input("Total Roof Area (Square Feet):", min_value=0, step=10)

    # Material Inputs
    st.subheader("Materials")

    if roofing_type == "Shingler":
        shingle_cost = st.number_input("Cost per Bundle of Shingles ($):", min_value=0.0, format="%.2f", step=1.0)
        bundles_needed = st.number_input("Number of Bundles Needed:", min_value=0, step=1)
        underlayment_cost = st.number_input("Cost of Underlayment per Roll ($):", min_value=0.0, format="%.2f", step=1.0)
        rolls_needed = st.number_input("Number of Rolls Needed:", min_value=0, step=1)

    elif roofing_type == "Flat Roofer":
        flat_material_cost = st.number_input("Cost per Square Foot of Flat Roofing Material ($):", min_value=0.0, format="%.2f", step=0.1)
        insulation_cost = st.number_input("Cost of Insulation per Square Foot ($):", min_value=0.0, format="%.2f", step=0.1)
        sealant_cost = st.number_input("Total Cost of Sealant and Adhesives ($):", min_value=0.0, format="%.2f", step=10.0)

    elif roofing_type == "Metal Roofer":
        metal_panel_cost = st.number_input("Cost per Metal Panel ($):", min_value=0.0, format="%.2f", step=1.0)
        panels_needed = st.number_input("Number of Metal Panels Needed:", min_value=0, step=1)
        flashing_cost = st.number_input("Total Cost of Flashing Materials ($):", min_value=0.0, format="%.2f", step=10.0)

    # Additional Materials
    st.subheader("Additional Materials")
    fasteners_cost = st.number_input("Cost of Fasteners ($):", min_value=0.0, format="%.2f", step=1.0)
    disposal_cost = st.number_input("Cost of Disposal (Dumpster, Haul Away) ($):", min_value=0.0, format="%.2f", step=10.0)

    # Labor Inputs
    st.subheader("Labor")
    num_workers = st.number_input("Number of Workers:", min_value=1, step=1)
    labor_hours = st.number_input("Total Labor Hours:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Hourly Rate per Worker ($):", min_value=0.0, format="%.2f", step=0.5)

    # Permits and Inspections
    st.subheader("Permits and Inspections")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    inspection_cost = st.number_input("Inspection Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs based on roofing type
        total_materials = 0
        if roofing_type == "Shingler":
            total_shingle_cost = shingle_cost * bundles_needed
            total_underlayment_cost = underlayment_cost * rolls_needed
            total_materials = total_shingle_cost + total_underlayment_cost

        elif roofing_type == "Flat Roofer":
            total_flat_material_cost = flat_material_cost * roof_area
            total_insulation_cost = insulation_cost * roof_area
            total_materials = total_flat_material_cost + total_insulation_cost + sealant_cost

        elif roofing_type == "Metal Roofer":
            total_metal_cost = metal_panel_cost * panels_needed
            total_materials = total_metal_cost + flashing_cost

        # Add additional material costs
        total_materials += fasteners_cost + disposal_cost

        # Calculate labor costs
        total_labor_cost = labor_hours * hourly_rate * num_workers

        # Calculate permit and inspection costs
        total_permit_inspect = permit_cost + inspection_cost

        # Calculate subtotal
        subtotal = total_materials + total_labor_cost + total_permit_inspect

        # Calculate markup and contingency
        markup_amount = subtotal * (markup_percentage / 100)
        contingency_amount = subtotal * (contingency / 100)

        # Calculate final total
        total_cost = subtotal + markup_amount + contingency_amount

        # Create summary DataFrame
        summary = pd.DataFrame({
            "Parameter": [
                "Roofing Type",
                "Roof Area (Sq Ft)",
                "Number of Workers",
                "Total Labor Hours",
                "Material Cost ($)",
                "Labor Cost ($)",
                "Permits and Inspections ($)",
                "Subtotal ($)",
                f"Markup ({markup_percentage}%) ($)",
                f"Contingency ({contingency}%) ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                roofing_type,
                roof_area,
                num_workers,
                labor_hours,
                round(total_materials, 2),
                round(total_labor_cost, 2),
                round(total_permit_inspect, 2),
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
            file_name="roofing_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
