def navigation_menu():
    """
    Displays the navigation menu for the data analysis tool.
    """
    print("Welcome to the Data Analysis Tool!")
    print("Please select an option:")
    print("1. Load Data")
    print("2. Analyze Data")
    print("3. Visualize Data")
    print("4. Export Results")
    print("5. Exit")         
def get_user_choice():
    """
    Prompts the user to select an option from the navigation menu.
    Returns the user's choice as an integer.
    """
    while True:
        try:
            choice = int(input("Enter your choice (1-5): "))
            if choice in range(1, 6):
                return choice
            else:
                print("Invalid choice. Please enter a number between 1 and 5.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
            
