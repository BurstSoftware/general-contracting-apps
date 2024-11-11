# drywallappv1.py

def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def get_int_input(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer value.")

def main():
    print("=== Drywall Project Cost Estimator ===")

    # Get user inputs
    price_per_sheet = get_float_input("Enter the price per drywall sheet ($): ")
    num_of_sheets = get_int_input("Enter the number of drywall sheets: ")
    num_of_cuts = get_int_input("Enter the number of cuts required: ")
    hours_of_labor = get_float_input("Enter the hours of labor required: ")
    labor_rate = get_float_input("Enter the hourly labor rate ($): ")

    # Calculate costs
    total_material_cost = price_per_sheet * num_of_sheets
    total_labor_cost = hours_of_labor * labor_rate
    total_cost = total_material_cost + total_labor_cost

    # Display the tool checklist
    tools_needed = ["Utility Knife", "Tape Measure", "Drywall Saw", "T-Square", "Drywall Screws", "Screwdriver/Drill"]
    print("\nRecommended Tools for the Job:")
    for tool in tools_needed:
        print(f"- {tool}")

    # Display results
    print("\n=== Project Summary ===")
    print(f"Total Material Cost: ${total_material_cost:.2f}")
    print(f"Total Labor Cost: ${total_labor_cost:.2f}")
    print(f"Estimated Total Project Cost: ${total_cost:.2f}")

if __name__ == "__main__":
    main()
