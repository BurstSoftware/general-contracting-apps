import streamlit as st
import pandas as pd

def main():
    st.title("Comprehensive Painting Cost Estimator")
    st.write("Enter the details of your painting project below to get an estimated cost.")

    # Room Dimensions
    st.subheader("Room Dimensions")
    room_length = st.number_input("Enter room length (feet):", min_value=0.0, format="%.2f", step=0.5)
    room_width = st.number_input("Enter room width (feet):", min_value=0.0, format="%.2f", step=0.5)
    ceiling_height = st.number_input("Enter ceiling height (feet):", min_value=0.0, format="%.2f", step=0.5)
    
    # Deductions
    st.subheader("Area Deductions")
    window_count = st.number_input("Number of windows:", min_value=0, step=1)
    avg_window_size = st.number_input("Average window size (square feet):", min_value=0.0, format="%.2f", step=0.5)
    door_count = st.number_input("Number of doors:", min_value=0, step=1)
    avg_door_size = st.number_input("Average door size (square feet):", min_value=0.0, format="%.2f", step=0.5)
    
    # Paint Details
    st.subheader("Paint Details")
    paint_type = st.selectbox(
        "Select paint type:",
        ["Economy Latex", "Premium Latex", "Oil-based", "Specialty Paint", "Eco-friendly"]
    )
    paint_finish = st.selectbox(
        "Select paint finish:",
        ["Flat", "Eggshell", "Satin", "Semi-gloss", "Gloss"]
    )
    paint_price_per_gallon = st.number_input("Enter paint price per gallon ($):", min_value=0.0, format="%.2f", step=0.5)
    coverage_per_gallon = st.number_input("Paint coverage per gallon (sq ft):", min_value=0.0, value=400.0, format="%.2f", step=10.0)
    
    # Surface Preparation
    st.subheader("Surface Preparation")
    needs_primer = st.checkbox("Requires primer")
    if needs_primer:
        primer_price_per_gallon = st.number_input("Primer price per gallon ($):", min_value=0.0, format="%.2f", step=0.5)
        primer_coverage = st.number_input("Primer coverage per gallon (sq ft):", min_value=0.0, value=300.0, format="%.2f", step=10.0)
    
    surface_prep_options = st.multiselect(
        "Select required surface preparation:",
        ["Cleaning", "Sanding", "Patching", "Caulking", "Wallpaper Removal"]
    )
    prep_cost = st.number_input("Enter total surface preparation costs ($):", min_value=0.0, format="%.2f", step=10.0)
    
    # Materials and Tools
    st.subheader("Additional Materials")
    materials_list = st.multiselect(
        "Select required materials:",
        ["Drop Cloths", "Painters Tape", "Brushes", "Rollers", "Paint Trays", "Sandpaper", "Spackling", "Caulk"]
    )
    materials_cost = st.number_input("Enter total cost of additional materials ($):", min_value=0.0, format="%.2f", step=5.0)
    
    # Labor Details
    st.subheader("Labor Details")
    labor_type = st.radio("Select labor type:", ["DIY", "Professional"])
    if labor_type == "Professional":
        hours_of_labor = st.number_input("Enter estimated hours of labor:", min_value=0.0, format="%.2f", step=0.5)
        labor_rate = st.number_input("Enter hourly labor rate ($):", min_value=0.0, format="%.2f", step=0.5)
    
    # Calculations
    if st.button("Calculate Total Cost"):
        # Calculate wall area
        total_wall_area = 2 * (room_length + room_width) * ceiling_height
        ceiling_area = room_length * room_width
        
        # Deduct windows and doors
        total_deductions = (window_count * avg_window_size) + (door_count * avg_door_size)
        paintable_area = total_wall_area - total_deductions
        
        if st.checkbox("Include ceiling"):
            paintable_area += ceiling_area
        
        # Calculate paint needed
        coats = 2  # Assuming two coats as standard
        total_paint_gallons = (paintable_area * coats) / coverage_per_gallon
        paint_cost = total_paint_gallons * paint_price_per_gallon
        
        # Calculate primer if needed
        primer_cost = 0
        if needs_primer:
            primer_gallons = paintable_area / primer_coverage
            primer_cost = primer_gallons * primer_price_per_gallon
        
        # Calculate labor cost
        labor_cost = 0
        if labor_type == "Professional":
            labor_cost = hours_of_labor * labor_rate
        
        # Calculate total project cost
        total_cost = paint_cost + primer_cost + prep_cost + materials_cost + labor_cost

        # Create summary DataFrame
        input_summary = pd.DataFrame({
            "Parameter": [
                "Total Wall Area (sq ft)",
                "Ceiling Area (sq ft)",
                "Total Paintable Area (sq ft)",
                "Paint Type",
                "Paint Finish",
                "Number of Coats",
                "Total Paint Needed (gallons)",
                "Paint Cost ($)",
                "Primer Cost ($)",
                "Surface Preparation Cost ($)",
                "Additional Materials Cost ($)",
                "Labor Cost ($)",
                "Total Project Cost ($)"
            ],
            "Value": [
                round(total_wall_area, 2),
                round(ceiling_area, 2),
                round(paintable_area, 2),
                paint_type,
                paint_finish,
                coats,
                round(total_paint_gallons, 2),
                round(paint_cost, 2),
                round(primer_cost, 2),
                round(prep_cost, 2),
                round(materials_cost, 2),
                round(labor_cost, 2),
                round(total_cost, 2)
            ]
        })

        # Display project summary
        st.subheader("Project Summary and Detailed Cost Breakdown")
        st.dataframe(input_summary, width=600)

        # Download option
        csv_output = input_summary.to_csv(index=False)
        st.download_button(
            label="Download Project Summary as CSV",
            data=csv_output,
            file_name="comprehensive_painting_project_summary.csv",
            mime="text/csv"
        )

if __name__ == "__main__":
    main()
