import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Flooring Installation Cost Estimator")
    st.write("Enter the details of your flooring project below to get an estimated cost.")

    # Room Dimensions
    st.subheader("Room Dimensions")
    room_length = st.number_input("Enter room length (feet):", min_value=0.0, format="%.2f", step=0.5)
    room_width = st.number_input("Enter room width (feet):", min_value=0.0, format="%.2f", step=0.5)
    
    # Flooring Material Details
    st.subheader("Flooring Material Details")
    flooring_type = st.selectbox(
        "Select flooring type:",
        ["Hardwood", "Laminate", "Vinyl", "Tile", "Carpet"]
    )
    price_per_sqft = st.number_input("Enter the price per square foot of flooring ($):", min_value=0.0, format="%.2f", step=0.5)
    
    # Additional Materials
    st.subheader("Additional Materials")
    underlayment_cost_sqft = st.number_input("Enter underlayment cost per square foot ($):", min_value=0.0, format="%.2f", step=0.1)
    trim_molding_length = st.number_input("Enter total length of trim/molding needed (feet):", min_value=0.0, step=1.0)
    trim_cost_per_foot = st.number_input("Enter cost of trim/molding per foot ($):", min_value=0.0, format="%.2f", step=0.5)
    adhesive_cost = st.number_input("Enter total cost of adhesive/mortar (if needed) ($):", min_value=0.0, format="%.2f", step=1.0)
    
    # Labor Details
    st.subheader("Labor Details")
    hours_of_labor = st.number_input("Enter estimated hours of labor:", min_value=0.0, format="%.2f", step=0.5)
    labor_rate = st.number_input("Enter hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)
    
    # Additional Costs
    st.subheader("Additional Costs")
    floor_prep_cost = st.number_input("Enter floor preparation costs (leveling, removal of old flooring, etc.) ($):", min_value=0.0, format="%.2f", step=10.0)
    waste_factor = st.slider("Select waste factor (%)", min_value=5, max_value=20, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate total square footage with waste factor
        total_sqft = room_length * room_width
        effective_sqft = total_sqft * (1 + waste_factor / 100)
        
        # Calculate costs
        flooring_material_cost = effective_sqft * price_per_sqft
        underlayment_cost = total_sqft * underlayment_cost_sqft
        trim_cost = trim_molding_length * trim_cost_per_foot
        labor_cost = hours_of_labor * labor_rate
        
        # Calculate total installation materials cost
        total_installation_materials = (
            underlayment_cost +
            trim_cost +
            adhesive_cost +
            floor_prep_cost
        )
        
        # Calculate total project cost
        total_cost = (
            flooring_material_cost +
            total_installation_materials +
            labor_cost
        )

        # Create summary DataFrame
        input_summary = pd.DataFrame({
            "Parameter": [
                "Room Length (feet)",
                "Room Width (feet)",
                "Total Square Footage",
                "Effective Square Footage (with waste)",
                "Flooring Type",
                "Price per Square Foot ($)",
                "Underlayment Cost per Square Foot ($)",
                "Trim/Molding Length (feet)",
                "Trim/Molding Cost per Foot ($)",
                "Adhesive/Mortar Cost ($)",
                "Hours of Labor",
                "Hourly Labor Rate ($)",
                "Floor Preparation Cost ($)",
                "Waste Factor (%)",
                "Total Flooring Material Cost ($)",
                "Total Underlayment Cost ($)",
                "Total Trim/Molding Cost ($)",
                "Total Installation Materials Cost ($)",
                "Total Labor Cost ($)",
                "Estimated Total Project Cost ($)"
            ],
            "Value": [
                round(room_length, 2),
                round(room_width, 2),
                round(total_sqft, 2),
                round(effective_sqft, 2),
                flooring_type,
                round(price_per_sqft, 2),
                round(underlayment_cost_sqft, 2),
                round(trim_molding_length, 2),
                round(trim_cost_per_foot, 2),
                round(adhesive_cost, 2),
                round(hours_of_labor, 2),
                round(labor_rate, 2),
                round(floor_prep_cost, 2),
                waste_factor,
                round(flooring_material_cost, 2),
                round(underlayment_cost, 2),
                round(trim_cost, 2),
                round(total_installation_materials, 2),
                round(labor_cost, 2),
                round(total_cost, 2)
            ]
        })

        # Display project summary
        st.subheader("Project Summary and Detailed Cost Breakdown")
        st.dataframe(input_summary, width=600)

        # Download option
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="comprehensive_flooring_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
