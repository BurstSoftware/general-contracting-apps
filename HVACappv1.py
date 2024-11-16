import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Electrical and HVAC Project Cost Estimator")
    st.write("Enter the details of your electrical or HVAC project below to get an estimated cost.")

    # Select Contractor Type
    st.subheader("Select Contractor Type")
    contractor_type = st.selectbox(
        "Choose the Trade:",
        ["General Electrician", "Low Voltage Electrician", "Lineworker", 
         "HVAC Technician", "Sheet Metal Worker", "Boilermaker"]
    )

    # Project Basics
    st.subheader("Project Basics")
    project_type = st.selectbox(
        "Select Project Type:",
        ["New Installation", "Renovation", "Service Upgrade", "Repair"]
    )

    service_size = st.selectbox(
        "Service Size (Amps/Capacity):",
        ["100A", "200A", "400A", "600A", "1 Ton HVAC", "2 Ton HVAC", "5 Ton HVAC"]
    )

    # General Material Inputs (Applicable to All Trades)
    st.subheader("Materials")
    wire_cost = st.number_input("Cost of Wire per Foot ($):", min_value=0.0, format="%.2f", step=0.1)
    wire_length = st.number_input("Total Wire Length Needed (Feet):", min_value=0, step=1)

    num_outlets = st.number_input("Number of Outlets/Switches:", min_value=0, step=1)
    cost_per_outlet = st.number_input("Cost per Outlet/Switch ($):", min_value=0.0, format="%.2f", step=0.5)

    num_fixtures = st.number_input("Number of Light Fixtures:", min_value=0, step=1)
    cost_per_fixture = st.number_input("Cost per Light Fixture ($):", min_value=0.0, format="%.2f", step=0.5)

    panel_cost = st.number_input("Electrical Panel/Unit Cost ($):", min_value=0.0, format="%.2f", step=10.0)

    # Additional Fields Based on Contractor Type
    if contractor_type == "Low Voltage Electrician":
        st.subheader("Low Voltage Systems")
        alarm_system_cost = st.number_input("Cost of Alarm System ($):", min_value=0.0, format="%.2f", step=10.0)
        network_wiring_cost = st.number_input("Cost of Network Wiring ($):", min_value=0.0, format="%.2f", step=10.0)

    elif contractor_type == "Lineworker":
        st.subheader("Lineworker Specific Inputs")
        pole_install_cost = st.number_input("Cost of Pole Installation ($):", min_value=0.0, format="%.2f", step=50.0)
        transformer_cost = st.number_input("Transformer Cost ($):", min_value=0.0, format="%.2f", step=50.0)

    elif contractor_type == "HVAC Technician":
        st.subheader("HVAC System Inputs")
        hvac_unit_cost = st.number_input("Cost of HVAC Unit ($):", min_value=0.0, format="%.2f", step=50.0)
        duct_install_cost = st.number_input("Duct Installation Cost ($):", min_value=0.0, format="%.2f", step=50.0)

    elif contractor_type == "Sheet Metal Worker":
        st.subheader("Sheet Metal Work")
        duct_fabrication_cost = st.number_input("Cost of Duct Fabrication ($):", min_value=0.0, format="%.2f", step=50.0)
        duct_installation_cost = st.number_input("Cost of Duct Installation ($):", min_value=0.0, format="%.2f", step=50.0)

    elif contractor_type == "Boilermaker":
        st.subheader("Boiler Installation")
        boiler_cost = st.number_input("Cost of Boiler Unit ($):", min_value=0.0, format="%.2f", step=100.0)
        tank_installation_cost = st.number_input("Tank Installation Cost ($):", min_value=0.0, format="%.2f", step=100.0)

    # Additional Materials
    st.subheader("Additional Materials")
    conduit_cost = st.number_input("Cost of Conduit and Fittings ($):", min_value=0.0, format="%.2f", step=0.5)
    junction_boxes = st.number_input("Cost of Junction Boxes ($):", min_value=0.0, format="%.2f", step=0.5)
    misc_materials = st.number_input("Cost of Miscellaneous Materials (connectors, fasteners, etc.) ($):", min_value=0.0, format="%.2f", step=0.5)

    # Labor Inputs
    st.subheader("Labor")
    num_technicians = st.number_input("Number of Technicians:", min_value=1, step=1)
    hours_per_technician = st.number_input("Hours per Technician:", min_value=0.0, format="%.2f", step=0.5)
    hourly_rate = st.number_input("Hourly Rate per Technician ($):", min_value=0.0, format="%.2f", step=0.5)

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
        elif contractor_type == "HVAC Technician":
            total_materials += hvac_unit_cost + duct_install_cost
        elif contractor_type == "Sheet Metal Worker":
            total_materials += duct_fabrication_cost + duct_installation_cost
        elif contractor_type == "Boilermaker":
            total_materials += boiler_cost + tank_installation_cost

        # Calculate labor costs
        total_labor_hours = num_technicians * hours_per_technician
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

        # Display total cost
        st.subheader("Total Estimated Project Cost")
        st.write(f"**Total Project Cost: ${total_cost:,.2f}**")

if __name__ == "__main__":
    main()
