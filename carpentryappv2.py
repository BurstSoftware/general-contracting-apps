import streamlit as st
import pandas as pd

def main():
    st.title("Carpentry Project Cost Estimator")
    st.write("Estimate costs for various carpentry projects with trade-specific details.")

    # Project Type
    st.subheader("Project Type")
    project_type = st.selectbox(
        "Select type of carpentry project:",
        ["Rough Carpentry", "Finish Carpentry", "Framing"]
    )

    # Subcategories based on Project Type
    if project_type == "Rough Carpentry":
        st.write("Rough Carpentry covers framework, structural work, and formwork.")
        sub_project = st.selectbox(
            "Select specific rough carpentry task:",
            ["Structural Framing", "Formwork", "Decking"]
        )
        
    elif project_type == "Finish Carpentry":
        st.write("Finish Carpentry includes trim work, molding, cabinetry, and detailed woodwork.")
        sub_project = st.selectbox(
            "Select specific finish carpentry task:",
            ["Trim and Molding", "Cabinet Installation", "Custom Shelving"]
        )

    else:
        st.write("Framing involves building the structure's skeleton using wood or metal studs.")
        sub_project = st.selectbox(
            "Select specific framing task:",
            ["Wall Framing", "Roof Framing", "Floor Framing"]
        )

    # Dimensions
    st.subheader("Project Dimensions and Requirements")
    length = st.number_input("Enter length of project area/item (feet):", min_value=0.0, format="%.2f", step=0.5)
    width = st.number_input("Enter width of project area/item (feet):", min_value=0.0, format="%.2f", step=0.5)
    height = st.number_input("Enter height of project area/item (feet):", min_value=0.0, format="%.2f", step=0.5)

    # Material Selection
    st.subheader("Material Details")
    material_type = st.selectbox(
        "Select primary material type:",
        ["Wood", "Metal", "Composite"]
    )
    if material_type == "Wood":
        wood_type = st.selectbox(
            "Select type of wood:",
            ["Pine", "Oak", "Maple", "Walnut", "Plywood"]
        )
        material_price_per_sqft = st.number_input("Enter the price per square foot of wood ($):", min_value=0.0, format="%.2f", step=0.5)
    elif material_type == "Metal":
        metal_type = st.selectbox(
            "Select type of metal:",
            ["Steel Studs", "Aluminum", "Galvanized Steel"]
        )
        material_price_per_sqft = st.number_input("Enter the price per square foot of metal ($):", min_value=0.0, format="%.2f", step=0.5)
    else:
        composite_price = st.number_input("Enter the price per square foot of composite material ($):", min_value=0.0, format="%.2f", step=0.5)

    # Additional Materials
    st.subheader("Additional Materials")
    fasteners_cost = st.number_input("Enter total cost of fasteners (screws, nails) ($):", min_value=0.0, format="%.2f", step=0.5)
    adhesive_cost = st.number_input("Enter total cost of adhesive ($):", min_value=0.0, format="%.2f", step=0.5)
    finish_cost = st.number_input("Enter total cost of finishes (paint, stain, varnish) ($):", min_value=0.0, format="%.2f", step=0.5)

    # Labor Details
    st.subheader("Labor Details")
    estimated_hours = st.number_input("Enter estimated hours of labor:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Enter hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)

    # Additional Costs
    st.subheader("Additional Costs")
    preparation_cost = st.number_input("Enter preparation costs (sanding, cutting, setup) ($):", min_value=0.0, format="%.2f", step=5.0)
    waste_factor = st.slider("Select waste factor (%)", min_value=5, max_value=20, value=10, step=1)

    # Calculate Total Cost
    if st.button("Calculate Total Cost"):
        area_sqft = length * width
        effective_area_sqft = area_sqft * (1 + waste_factor / 100)

        # Calculate material cost
        material_cost = effective_area_sqft * material_price_per_sqft
        total_materials_cost = material_cost + fasteners_cost + adhesive_cost + finish_cost

        # Calculate labor cost
        labor_cost = estimated_hours * hourly_rate
        total_project_cost = total_materials_cost + labor_cost + preparation_cost

        # Summary DataFrame
        input_summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Sub Project Type",
                "Length (feet)",
                "Width (feet)",
                "Height (feet)",
                "Material Type",
                "Material Cost per Sqft ($)",
                "Total Area (sqft)",
                "Effective Area with Waste (sqft)",
                "Fasteners Cost ($)",
                "Adhesive Cost ($)",
                "Finish Cost ($)",
                "Estimated Hours of Labor",
                "Hourly Labor Rate ($)",
                "Preparation Cost ($)",
                "Waste Factor (%)",
                "Total Material Cost ($)",
                "Total Labor Cost ($)",
                "Estimated Total Project Cost ($)"
            ],
            "Value": [
                project_type,
                sub_project,
                round(length, 2),
                round(width, 2),
                round(height, 2),
                material_type,
                round(material_price_per_sqft, 2),
                round(area_sqft, 2),
                round(effective_area_sqft, 2),
                round(fasteners_cost, 2),
                round(adhesive_cost, 2),
                round(finish_cost, 2),
                round(estimated_hours, 2),
                round(hourly_rate, 2),
                round(preparation_cost, 2),
                waste_factor,
                round(material_cost, 2),
                round(labor_cost, 2),
                round(total_project_cost, 2)
            ]
        })

        # Display project summary
        st.subheader("Project Summary and Detailed Cost Breakdown")
        st.dataframe(input_summary, width=800)

        # Download option
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="contractor_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
