import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Electrical Project Cost Estimator")
    st.write("Enter the details of your electrical project below to get an estimated cost.")

    # Select Contractor Type
    st.subheader("Select Contractor Type")
    contractor_type = st.selectbox(
        "Choose the Trade:",
        ["General Electrician", "Low Voltage Electrician", "Lineworker"]
    )

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["New Installation", "Renovation", "Service Upgrade", "Repair"]
    )

    service_size = st.selectbox(
        "Service Size (Amps):",
        ["100A", "200A", "400A", "600A"]
    )

    # General Material Inputs (Applicable to All Trades)
    st.subheader("Materials")
    wire_cost = st.number_input("Cost of Wire per Foot ($):", min_value=0.0, format="%.2f", step=0.1)
    wire_length = st.number_input("Total Wire Length Needed (Feet):", min_value=0, step=1)

    num_outlets = st.number_input("Number of Outlets/Switches:", min_value=0, step=1)
    cost_per_outlet = st.number_input("Cost per Outlet/Switch ($):", min_value=0.0, format="%.2f", step=0.5)

    num_fixtures = st.number_input("Number of Light Fixtures:", min_value=0, step=1)
    cost_per_fixture = st.number_input("Cost per Light Fixture ($):", min_value=0.0, format="%.2f", step=0.5)

    panel_cost = st.number_input("Electrical Panel Cost ($):", min_value=0.0, format="%.2f", step=10.0)

    # Additional Fields Based on Contractor Type
    if contractor_type == "Low Voltage Electrician":
        st.subheader("Low Voltage Systems")
        alarm_system_cost = st.number_input("Cost of Alarm System ($):", min_value=0.0, format="%.2f", step=10.0)
        network_wiring_cost = st.number_input("Cost of Network Wiring ($):", min_value=0.0, format="%.2f", step=10.0)

    elif contractor_type == "Lineworker":
        st.subheader("Lineworker Specific Inputs")
        pole_install_cost = st.number_input("Cost of Pole Installation ($):", min_value=0.0, format="%.2f", step=50.0)
        transformer_cost = st.number_input("Transformer Cost ($):", min_value=0.0, format="%.2f", step=50.0)

    # Additional Materials
    st.subheader("Additional Materials")
    conduit_cost = st.number_input("Cost of Conduit and Fittings ($):", min_value=0.0, format="%.2f", step=0.5)
    junction_boxes = st.number_input("Cost of Junction Boxes ($):", min_value=0.0, format="%.2f", step=0.5)
    misc_materials = st.number_input("Cost of Miscellaneous Materials (connectors, fasteners, etc.) ($):", min_value=0.0, format="%.2f", step=0.5)

    # Labor Inputs
    st.subheader("Labor")
    num_electricians = st.number_input("Number of Electricians:", min_value=1, step=1)
    hours_per_electrician = st.number_input("Hours per Electrician:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Hourly Rate per Electrician ($):", min_value=0.0, format="%.2f", step=0.5)

    # Permits and Inspections
    st.subheader("Permits and Inspections")
    permit_cost = st.number_input("Permit Costs ($):", min_value=0.0, format="%.2f", step=10.0)
    inspection_cost = st.number_input("Inspection Costs ($):", min_value=0.0, format="%.2f", step=10.0)

    # Markup and Contingency
    markup_percentage = st.slider("Markup Percentage (%):", min_value=0, max_value=50, value=20, step=1)
    contingency = st.slider("Contingency Percentage (%):", min_value=0, max_value=30, value=10, step=1)

    if st.button("Calculate Total Cost"):
        # Calculate material costs
        total_wire_cost = wire_cost * wire_length
        total_outlet_cost = num_outlets * cost_per_outlet
        total_fixture_cost = num_fixtures * cost_per_fixture
        total_materials = (total_wire_cost + total_outlet_cost + total_fixture_cost + 
                         panel_cost + conduit_cost + junction_boxes + misc_materials)

        # Include trade-specific costs
        if contractor_type == "Low Voltage Electrician":
            total_materials += alarm_system_cost + network_wiring_cost
        elif contractor_type == "Lineworker":
            total_materials += pole_install_cost + transformer_cost

        # Calculate labor costs
        total_labor_hours = num_electricians * hours_per_electrician
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
                "Service Size",
                "Total Wire Length (Feet)",
                "Number of Outlets/Switches",
                "Number of Light Fixtures",
                "Number of Electricians",
                "Total Labor Hours",
                "Wire Cost ($)",
                "Outlet/Switch Cost ($)",
                "Fixture Cost ($)",
                "Panel Cost ($)",
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
                service_size,
                wire_length,
                num_outlets,
                num_fixtures,
                num_electricians,
                total_labor_hours,
                round(total_wire_cost, 2),
                round(total_outlet_cost, 2),
                round(total_fixture_cost, 2),
                round(panel_cost, 2),
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
            file_name="electrical_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
