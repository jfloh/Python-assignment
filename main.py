def main_m():
    function = int(input("Welcome to KLCCC automated system\n1: Sign up\n2: Login\n3: Exit\n"))
    while function < 1 or function > 3: #validate the option(Only 1-3 can be input)
        function = int(input("Invalid option\n\n1: Sign up\n2: Login\n3: Exit\n"))
    if function == 1:
        #Call sign-up function here
    elif function == 2:
        #Call login function here
    else:
        print("Exit selected")
        quit()
main_m()

def main_menu():
    while True:
        print("Welcome to KLCCC System")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            user_management.sign_up()
        elif choice == '2':
            user_management.login()
        elif choice == '3':
            print("Exiting the system. Goodbye!")
        else:
            print("Invalid choice. Please try again!")
main_menu()