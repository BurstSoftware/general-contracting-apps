import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Masonry Project Cost Estimator")
    st.write("Enter the details of your masonry project below to get an estimated cost.")

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["New Construction", "Repair", "Renovation", "Restoration"]
    )

    masonry_type = st.selectbox(
        "Type of Masonry Work:",
        ["Bricklaying", "Stone Masonry", "Concrete Finishing", "Cement Masonry"]
    )

    # Material Inputs
    st.subheader("Materials")
    
    # Bricklaying Materials
    num_bricks = st.number_input("Number of Bricks Needed:", min_value=0, step=1)
    cost_per_brick = st.number_input("Cost per Brick ($):", min_value=0.0, format="%.2f", step=0.1)

    # Stone Masonry Materials
    stone_area = st.number_input("Total Area of Stone Masonry (Square Feet):", min_value=0, step=1)
    cost_per_sqft_stone = st.number_input("Cost per Square Foot of Stone ($):", min_value=0.0, format="%.2f", step=0.1)

    # Concrete Finishing and Cement Masonry Materials
    concrete_volume = st.number_input("Volume of Concrete Needed (Cubic Yards):", min_value=0.0, format="%.2f", step=0.1)
    cost_per_cubic_yard = st.number_input("Cost per Cubic Yard of Concrete ($):", min_value=0.0, format="%.2f", step=10.0)

    rebar_cost = st.number_input("Cost of Rebar and Reinforcement Materials ($):", min_value=0.0, format="%.2f", step=10.0)
    mortar_cost = st.number_input("Cost of Mortar/Cement ($):", min_value=0.0, format="%.2f", step=10.0)

    # Additional Materials
    st.subheader("Additional Materials")
    formwork_cost = st.number_input("Cost of Formwork and Temporary Structures ($):", min_value=0.0, format="%.2f", step=10.0)
    gravel_base_cost = st.number_input("Cost of Gravel Base Preparation ($):", min_value=0.0, format="%.2f", step=10.0)
    misc_materials = st.number_input("Cost of Miscellaneous Materials (e.g., nails, fasteners) ($):", min_value=0.0, format="%.2f", step=5.0)

    # Labor Inputs
    st.subheader("Labor")
    num_masons = st.number_input("Number of Masons:", min_value=1, step=1)
    hours_per_mason = st.number_input("Hours per Mason:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate_mason = st.number_input("Hourly Rate per Mason ($):", min_value=0.0, format="%.2f", step=1.0)

    num_helpers = st.number_input("Number of Helpers:", min_value=0, step=1)
    hours_per_helper = st.number_input("Hours per Helper:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate_helper = st.number_input("Hourly Rate per Helper ($):", min_value=0.0, format="%.2f", step=0.5)

    # Permits and Inspections
    st.subheader("Permits and Inspections")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    inspection_cost = st.number_input("Inspection Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs
        total_brick_cost = num_bricks * cost_per_brick
        total_stone_cost = stone_area * cost_per_sqft_stone
        total_concrete_cost = concrete_volume * cost_per_cubic_yard
        total_masonry_materials = (total_brick_cost + total_stone_cost + 
                                   total_concrete_cost + rebar_cost + mortar_cost +
                                   formwork_cost + gravel_base_cost + misc_materials)

        # Calculate labor costs
        total_mason_hours = num_masons * hours_per_mason
        total_mason_cost = total_mason_hours * hourly_rate_mason

        total_helper_hours = num_helpers * hours_per_helper
        total_helper_cost = total_helper_hours * hourly_rate_helper

        total_labor_cost = total_mason_cost + total_helper_cost

        # Calculate permit and inspection costs
        total_permit_inspect = permit_cost + inspection_cost

        # Calculate subtotal
        subtotal = total_masonry_materials + total_labor_cost + total_permit_inspect

        # Calculate markup and contingency
        markup_amount = subtotal * (markup_percentage / 100)
        contingency_amount = subtotal * (contingency / 100)

        # Calculate final total
        total_cost = subtotal + markup_amount + contingency_amount

        # Create summary DataFrame
        summary = pd.DataFrame({
            "Parameter": [
                "Project Type",
                "Masonry Type",
                "Total Number of Bricks",
                "Stone Area (Sqft)",
                "Concrete Volume (Cubic Yards)",
                "Number of Masons",
                "Number of Helpers",
                "Total Mason Hours",
                "Total Helper Hours",
                "Material Costs ($)",
                "Labor Costs ($)",
                "Permits and Inspections ($)",
                "Subtotal ($)",
                f"Markup ({markup_percentage}%) ($)",
                f"Contingency ({contingency}%) ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                project_type,
                masonry_type,
                num_bricks,
                stone_area,
                concrete_volume,
                num_masons,
                num_helpers,
                total_mason_hours,
                total_helper_hours,
                round(total_masonry_materials, 2),
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
            file_name="masonry_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
