import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Main function for the Streamlit application
def main():
    st.title("Comprehensive Drywall Project Cost Estimator")
    st.write("Enter the details of your drywall project below to get an estimated cost.")

    # User Inputs
    price_per_sheet = st.number_input("Enter the price per drywall sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    num_of_sheets = st.number_input("Enter the number of drywall sheets:", min_value=0, step=1)
    num_of_cuts = st.number_input("Enter the number of cuts required:", min_value=0, step=1)
    hours_of_labor = st.number_input("Enter the hours of labor required:", min_value=0.0, format="%.2f", step=0.5)
    labor_rate = st.number_input("Enter the hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)

    # New Inputs for Additional Costs
    screw_cost = st.number_input("Enter the cost of screws/nails per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    tape_mud_cost = st.number_input("Enter the cost of joint compound (mud) per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    drywall_tape_cost = st.number_input("Enter the cost of drywall tape per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    primer_paint_cost = st.number_input("Enter the cost of primer and paint per sheet ($):", min_value=0.0, format="%.2f", step=0.5)
    floor_prep_cost = st.number_input("Enter the cost of floor/room prep materials (e.g., drop cloths, tape) ($):", min_value=0.0, format="%.2f", step=0.5)
    waste_factor = st.slider("Select the waste factor (%)", min_value=0, max_value=20, value=10, step=1)

    # Button to calculate the cost
    if st.button("Calculate Total Cost"):
        # Calculate the effective number of sheets accounting for waste
        effective_num_of_sheets = num_of_sheets * (1 + waste_factor / 100)

        # Calculate material costs
        total_material_cost = price_per_sheet * effective_num_of_sheets
        total_screw_cost = screw_cost * effective_num_of_sheets
        total_tape_mud_cost = tape_mud_cost * effective_num_of_sheets
        total_drywall_tape_cost = drywall_tape_cost * effective_num_of_sheets
        total_paint_cost = primer_paint_cost * effective_num_of_sheets

        # Total installation costs (includes all additional materials)
        total_installation_materials = (total_screw_cost +
                                        total_tape_mud_cost +
                                        total_drywall_tape_cost +
                                        total_paint_cost +
                                        floor_prep_cost)

        # Calculate labor costs
        total_labor_cost = hours_of_labor * labor_rate

        # Calculate the total project cost
        total_cost = total_material_cost + total_installation_materials + total_labor_cost

        # Phase-wise Costs
        drywall_phase_cost = total_material_cost + total_screw_cost
        taping_mudding_phase_cost = total_tape_mud_cost + total_drywall_tape_cost
        priming_painting_phase_cost = total_paint_cost
        prep_material_cost = floor_prep_cost

        # Dashboard section
        st.subheader("Project Cost Breakdown")
        cost_breakdown = {
            "Drywall Installation": drywall_phase_cost,
            "Taping/Mudding": taping_mudding_phase_cost,
            "Priming/Painting": priming_painting_phase_cost,
            "Preparation Materials": prep_material_cost,
            "Labor Costs": total_labor_cost
        }

        # Display as DataFrame
        cost_df = pd.DataFrame(cost_breakdown.items(), columns=["Phase", "Cost ($)"])
        st.dataframe(cost_df)

        # Bar Chart
        st.subheader("Cost Breakdown by Phase")
        fig, ax = plt.subplots()
        ax.bar(cost_breakdown.keys(), cost_breakdown.values(), color=["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#64B5CD"])
        ax.set_xlabel("Project Phases")
        ax.set_ylabel("Cost ($)")
        ax.set_title("Estimated Cost by Project Phase")
        st.pyplot(fig)

        # Pie Chart
        st.subheader("Cost Distribution")
        fig2, ax2 = plt.subplots()
        ax2.pie(cost_breakdown.values(), labels=cost_breakdown.keys(), autopct='%1.1f%%', colors=["#4C72B0", "#55A868", "#C44E52", "#8172B2", "#64B5CD"], startangle=90)
        ax2.axis('equal')
        st.pyplot(fig2)

        # Summary Table
        st.subheader("Detailed Cost Summary")
        input_summary = pd.DataFrame({
            "Parameter": [
                "Price per Drywall Sheet ($)",
                "Number of Drywall Sheets (with waste factor)",
                "Total Material Cost ($)",
                "Total Screw/Nail Cost ($)",
                "Total Joint Compound Cost ($)",
                "Total Drywall Tape Cost ($)",
                "Total Primer and Paint Cost ($)",
                "Total Floor/Room Prep Cost ($)",
                "Total Labor Cost ($)",
                "Estimated Total Project Cost ($)"
            ],
            "Value": [
                round(price_per_sheet, 2),
                round(effective_num_of_sheets, 2),
                round(total_material_cost, 2),
                round(total_screw_cost, 2),
                round(total_tape_mud_cost, 2),
                round(total_drywall_tape_cost, 2),
                round(total_paint_cost, 2),
                round(floor_prep_cost, 2),
                round(total_labor_cost, 2),
                round(total_cost, 2)
            ]
        })
        
        # Display summary
        st.dataframe(input_summary)

        # Option to download the full summary as a CSV file
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="comprehensive_drywall_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
