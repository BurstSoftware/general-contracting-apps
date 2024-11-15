import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Carpentry Project Cost Estimator")
    st.write("Enter the details of your carpentry project below to get an estimated cost.")

    # Project Type
    st.subheader("Project Type")
    project_type = st.selectbox(
        "Select type of carpentry project:",
        ["Custom Furniture", "Framing & Trim Work", "Custom Shelving/Built-ins", "General Carpentry Work"]
    )

    # Dimensions
    st.subheader("Project Dimensions and Requirements")
    length = st.number_input("Enter length of project area/item (feet):", min_value=0.0, format="%.2f", step=0.5)
    width = st.number_input("Enter width of project area/item (feet):", min_value=0.0, format="%.2f", step=0.5)
    height = st.number_input("Enter height of project area/item (feet):", min_value=0.0, format="%.2f", step=0.5)

    # Material Selection
    st.subheader("Material Details")
    wood_type = st.selectbox(
        "Select type of wood:",
        ["Pine", "Oak", "Maple", "Walnut", "Plywood"]
    )
    wood_price_per_sqft = st.number_input("Enter the price per square foot of wood ($):", min_value=0.0, format="%.2f", step=0.5)
    
    # Additional Materials
    st.subheader("Additional Materials")
    screws_cost = st.number_input("Enter total cost of screws/nails ($):", min_value=0.0, format="%.2f", step=0.5)
    adhesive_cost = st.number_input("Enter total cost of adhesive/glue ($):", min_value=0.0, format="%.2f", step=0.5)
    stain_varnish_cost = st.number_input("Enter total cost of stain/varnish/paint ($):", min_value=0.0, format="%.2f", step=0.5)

    # Labor Details
    st.subheader("Labor Details")
    estimated_hours = st.number_input("Enter estimated hours of labor:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Enter hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)

    # Additional Costs
    st.subheader("Additional Costs")
    preparation_cost = st.number_input("Enter project preparation costs (sanding, cutting, etc.) ($):", min_value=0.0, format="%.2f", step=5.0)
    waste_factor = st.slider("Select waste factor (%)", min_value=5, max_value=20, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate total square footage and effective square footage with waste
        area_sqft = length * width
        effective_area_sqft = area_sqft * (1 + waste_factor / 100)
        
        # Calculate material costs
        wood_cost = effective_area_sqft * wood_price_per_sqft
        total_materials_cost = wood_cost + screws_cost + adhesive_cost + stain_varnish_cost

        # Calculate labor costs
        labor_cost = estimated_hours * hourly_rate
        
        # Calculate total project cost
        total_project_cost = total_materials_cost + labor_cost + preparation_cost

        # Create summary DataFrame
        input_summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Length (feet)",
                "Width (feet)",
                "Height (feet)",
                "Wood Type",
                "Wood Cost per Sqft ($)",
                "Total Area (sqft)",
                "Effective Area with Waste (sqft)",
                "Screws/Nails Cost ($)",
                "Adhesive/Glue Cost ($)",
                "Stain/Varnish Cost ($)",
                "Estimated Hours of Labor",
                "Hourly Labor Rate ($)",
                "Preparation Cost ($)",
                "Waste Factor (%)",
                "Total Wood Material Cost ($)",
                "Total Additional Materials Cost ($)",
                "Total Labor Cost ($)",
                "Estimated Total Project Cost ($)"
            ],
            "Value": [
                project_type,
                round(length, 2),
                round(width, 2),
                round(height, 2),
                wood_type,
                round(wood_price_per_sqft, 2),
                round(area_sqft, 2),
                round(effective_area_sqft, 2),
                round(screws_cost, 2),
                round(adhesive_cost, 2),
                round(stain_varnish_cost, 2),
                round(estimated_hours, 2),
                round(hourly_rate, 2),
                round(preparation_cost, 2),
                waste_factor,
                round(wood_cost, 2),
                round(total_materials_cost - wood_cost, 2),
                round(labor_cost, 2),
                round(total_project_cost, 2)
            ]
        })

        # Display project summary
        st.subheader("Project Summary and Detailed Cost Breakdown")
        st.dataframe(input_summary, width=700)

        # Download option
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="comprehensive_carpentry_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
