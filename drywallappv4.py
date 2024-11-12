import streamlit as st
import pandas as pd

# Main function for the Streamlit application
def main():
    st.title("Drywall Project Cost Estimator")
    st.write("Enter the details of your drywall project below to get an estimated cost.")

    # User Inputs
    price_per_sheet = st.number_input("Enter the price per drywall sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    num_of_sheets = st.number_input("Enter the number of drywall sheets:", min_value=0, step=1)
    num_of_cuts = st.number_input("Enter the number of cuts required:", min_value=0, step=1)
    hours_of_labor = st.number_input("Enter the hours of labor required:", min_value=0.0, format="%.2f", step=0.5)
    labor_rate = st.number_input("Enter the hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)

    # Default values for project summary
    total_material_cost = 0.00
    total_labor_cost = 0.00
    total_cost = 0.00

    # Display initial project summary with default values
    st.subheader("Project Summary")
    st.markdown(f"**Total Material Cost:** ${total_material_cost:.2f}")
    st.markdown(f"**Total Labor Cost:** ${total_labor_cost:.2f}")
    st.markdown(f"**Estimated Total Project Cost:** ${total_cost:.2f}")

    # Button to calculate the cost
    if st.button("Calculate Total Cost"):
        # Calculate costs
        total_material_cost = price_per_sheet * num_of_sheets
        total_labor_cost = hours_of_labor * labor_rate
        total_cost = total_material_cost + total_labor_cost

        # Display updated project summary after calculation
        st.subheader("Updated Project Summary")
        st.markdown(f"**Total Material Cost:** ${total_material_cost:.2f}")
        st.markdown(f"**Total Labor Cost:** ${total_labor_cost:.2f}")
        st.markdown(f"**Estimated Total Project Cost:** ${total_cost:.2f}")

        # Create a DataFrame to store user inputs and calculated values
        input_summary = pd.DataFrame({
            "Parameter": [
                "Price per Drywall Sheet ($)", 
                "Number of Drywall Sheets",
                "Number of Cuts Required",
                "Hours of Labor Required",
                "Hourly Labor Rate ($)",
                "Total Material Cost ($)",
                "Total Labor Cost ($)",
                "Estimated Total Project Cost ($)"
            ],
            "Value": [
                round(price_per_sheet, 2),
                num_of_sheets,
                num_of_cuts,
                round(hours_of_labor, 2),
                round(labor_rate, 2),
                round(total_material_cost, 2),
                round(total_labor_cost, 2),
                round(total_cost, 2)
            ]
        })

        # Display full project summary including input values
        st.subheader("Detailed Project Summary and User Input Data")
        st.dataframe(input_summary, width=600)

        # Option to download the full summary as a CSV file
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="drywall_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
