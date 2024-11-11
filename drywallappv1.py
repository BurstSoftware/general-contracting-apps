import streamlit as st

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

    # Button to calculate the cost
    if st.button("Calculate Total Cost"):
        # Calculate costs
        total_material_cost = price_per_sheet * num_of_sheets
        total_labor_cost = hours_of_labor * labor_rate
        total_cost = total_material_cost + total_labor_cost

        # Display results
        st.subheader("Project Summary")
        st.write(f"**Total Material Cost:** ${total_material_cost:.2f}")
        st.write(f"**Total Labor Cost:** ${total_labor_cost:.2f}")
        st.write(f"**Estimated Total Project Cost:** ${total_cost:.2f}")

        # Tool checklist
        tools_needed = ["Utility Knife", "Tape Measure", "Drywall Saw", "T-Square", "Drywall Screws", "Screwdriver/Drill"]
        st.subheader("Recommended Tools for the Job")
        for tool in tools_needed:
            st.write(f"- {tool}")

if __name__ == "__main__":
    main()
