import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Plumbing Project Cost Estimator")
    st.write("Enter the details of your plumbing project below to get an estimated cost.")

    # Select Contractor Type
    st.subheader("Select Contractor Type")
    contractor_type = st.selectbox(
        "Choose the Trade:",
        ["General Plumber", "Pipefitter", "Steamfitter", "Sprinkler Fitter"]
    )

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["New Installation", "Renovation", "Service Upgrade", "Repair"]
    )

    pipe_material = st.selectbox(
        "Pipe Material:",
        ["PVC", "Copper", "Steel", "PEX"]
    )

    # General Material Inputs (Applicable to All Trades)
    st.subheader("Materials")
    pipe_cost_per_foot = st.number_input("Cost of Pipe per Foot ($):", min_value=0.0, format="%.2f", step=0.1)
    pipe_length = st.number_input("Total Pipe Length Needed (Feet):", min_value=0, step=1)

    num_fixtures = st.number_input("Number of Fixtures (sinks, toilets, etc.):", min_value=0, step=1)
    cost_per_fixture = st.number_input("Cost per Fixture ($):", min_value=0.0, format="%.2f", step=0.5)

    valve_cost = st.number_input("Total Cost of Valves ($):", min_value=0.0, format="%.2f", step=10.0)
    fittings_cost = st.number_input("Total Cost of Fittings (elbows, tees, etc.) ($):", min_value=0.0, format="%.2f", step=10.0)

    # Additional Fields Based on Contractor Type
    if contractor_type == "Pipefitter":
        st.subheader("Pipefitting Specific Inputs")
        insulation_cost = st.number_input("Cost of Pipe Insulation ($):", min_value=0.0, format="%.2f", step=10.0)
        support_bracket_cost = st.number_input("Cost of Support Brackets ($):", min_value=0.0, format="%.2f", step=10.0)

    elif contractor_type == "Steamfitter":
        st.subheader("Steamfitting Specific Inputs")
        steam_trap_cost = st.number_input("Cost of Steam Traps ($):", min_value=0.0, format="%.2f", step=10.0)
        pressure_valve_cost = st.number_input("Cost of Pressure Relief Valves ($):", min_value=0.0, format="%.2f", step=10.0)

    elif contractor_type == "Sprinkler Fitter":
        st.subheader("Sprinkler System Specific Inputs")
        sprinkler_head_cost = st.number_input("Cost per Sprinkler Head ($):", min_value=0.0, format="%.2f", step=1.0)
        num_sprinkler_heads = st.number_input("Number of Sprinkler Heads:", min_value=0, step=1)
        fire_pump_cost = st.number_input("Cost of Fire Pump ($):", min_value=0.0, format="%.2f", step=100.0)

    # Additional Materials
    st.subheader("Additional Materials")
    sealant_cost = st.number_input("Cost of Sealant and Adhesives ($):", min_value=0.0, format="%.2f", step=0.5)
    clamps_and_hangers = st.number_input("Cost of Clamps and Hangers ($):", min_value=0.0, format="%.2f", step=0.5)
    misc_materials = st.number_input("Cost of Miscellaneous Materials (connectors, fasteners, etc.) ($):", min_value=0.0, format="%.2f", step=0.5)

    # Labor Inputs
    st.subheader("Labor")
    num_plumbers = st.number_input("Number of Plumbers:", min_value=1, step=1)
    hours_per_plumber = st.number_input("Hours per Plumber:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Hourly Rate per Plumber ($):", min_value=0.0, format="%.2f", step=0.5)

    # Permits and Inspections
    st.subheader("Permits and Inspections")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    inspection_cost = st.number_input("Inspection Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs
        total_pipe_cost = pipe_cost_per_foot * pipe_length
        total_fixture_cost = num_fixtures * cost_per_fixture
        total_materials = total_pipe_cost + total_fixture_cost + valve_cost + fittings_cost + sealant_cost + clamps_and_hangers + misc_materials

        # Include trade-specific costs
        if contractor_type == "Pipefitter":
            total_materials += insulation_cost + support_bracket_cost
        elif contractor_type == "Steamfitter":
            total_materials += steam_trap_cost + pressure_valve_cost
        elif contractor_type == "Sprinkler Fitter":
            total_materials += (sprinkler_head_cost * num_sprinkler_heads) + fire_pump_cost

        # Calculate labor costs
        total_labor_hours = num_plumbers * hours_per_plumber
        total_labor_cost = total_labor_hours * hourly_rate

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
                "Contractor Type",
                "Project Type",
                "Pipe Material",
                "Total Pipe Length (Feet)",
                "Number of Fixtures",
                "Number of Plumbers",
                "Total Labor Hours",
                "Pipe Cost ($)",
                "Fixture Cost ($)",
                "Valve and Fittings Cost ($)",
                "Total Materials Cost ($)",
                "Labor Cost ($)",
                "Permits and Inspections ($)",
                "Subtotal ($)",
                f"Markup ({markup_percentage}%) ($)",
                f"Contingency ({contingency}%) ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                contractor_type,
                project_type,
                pipe_material,
                pipe_length,
                num_fixtures,
                num_plumbers,
                total_labor_hours,
                round(total_pipe_cost, 2),
                round(total_fixture_cost, 2),
                round(valve_cost + fittings_cost, 2),
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
        st.dataframe(summary, width=700)

        # Download option
        csv_output = summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="plumbing_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
