import streamlit as st
import pandas as pd

# Main function for the Streamlit application
def main():
    st.title("Enhanced Drywall Project Cost Estimator")
    st.write("Enter the details of your drywall project below to get an estimated cost.")

    # User Inputs
    price_per_sheet = st.number_input("Enter the price per drywall sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    num_of_sheets = st.number_input("Enter the number of drywall sheets:", min_value=0, step=1)
    num_of_cuts = st.number_input("Enter the number of cuts required:", min_value=0, step=1)
    hours_of_labor = st.number_input("Enter the hours of labor required:", min_value=0.0, format="%.2f", step=0.5)
    labor_rate = st.number_input("Enter the hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)

    # New Inputs for Additional Costs
    screw_cost = st.number_input("Enter the cost of screws/nails per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    tape_mud_cost = st.number_input("Enter the cost of tape and mud per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    primer_paint_cost = st.number_input("Enter the cost of primer and paint per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    waste_factor = st.slider("Select the waste factor (%)", min_value=0, max_value=20, value=10, step=1)

    # Button to calculate the cost
    if st.button("Calculate Total Cost"):
        # Calculate the waste factor
        effective_num_of_sheets = num_of_sheets * (1 + waste_factor / 100)

        # Calculate material costs
        total_material_cost = price_per_sheet * effective_num_of_sheets
        total_screw_cost = screw_cost * effective_num_of_sheets
        total_tape_mud_cost = tape_mud_cost * effective_num_of_sheets
        total_paint_cost = primer_paint_cost * effective_num_of_sheets

        # Total installation costs
        total_installation_materials = total_screw_cost + total_tape_mud_cost + total_paint_cost

        # Calculate labor costs
        total_labor_cost = hours_of_labor * labor_rate

        # Calculate the total project cost
        total_cost = total_material_cost + total_installation_materials + total_labor_cost

        # Create a DataFrame to store user inputs and calculated values
        input_summary = pd.DataFrame({
            "Parameter": [
                "Price per Drywall Sheet ($)",
                "Number of Drywall Sheets (with waste factor)",
                "Number of Cuts Required",
                "Hours of Labor Required",
                "Hourly Labor Rate ($)",
                "Cost of Screws/Nails per Sheet ($)",
                "Cost of Tape and Mud per Sheet ($)",
                "Cost of Primer and Paint per Sheet ($)",
                "Waste Factor (%)",
                "Total Material Cost ($)",
                "Total Screw/Nail Cost ($)",
                "Total Tape and Mud Cost ($)",
                "Total Primer and Paint Cost ($)",
                "Total Installation Material Cost ($)",
                "Total Labor Cost ($)",
                "Estimated Total Project Cost ($)"
            ],
            "Value": [
                round(price_per_sheet, 2),
                round(effective_num_of_sheets, 2),
                num_of_cuts,
                round(hours_of_labor, 2),
                round(labor_rate, 2),
                round(screw_cost, 2),
                round(tape_mud_cost, 2),
                round(primer_paint_cost, 2),
                waste_factor,
                round(total_material_cost, 2),
                round(total_screw_cost, 2),
                round(total_tape_mud_cost, 2),
                round(total_paint_cost, 2),
                round(total_installation_materials, 2),
                round(total_labor_cost, 2),
                round(total_cost, 2)
            ]
        })

        # Display project summary including input values
        st.subheader("Project Summary and Detailed Cost Breakdown")
        st.dataframe(input_summary, width=600)

        # Option to download the full summary as a CSV file
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="enhanced_drywall_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
