sp_user=['admin','admin123']
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
            login_sys()
            break
            #user_management.login()
        elif choice == '3':
            print("Exiting the system. Goodbye!")
            break
            quit()
        else:
            print("Invalid choice. Please try again!\n")
def login_sys():
    login_name=input("Enter username: ")
    if login_name in sp_user[1]:
        print("Welcome Super user ! ")
#def signup_sys():
#Sign up system here
main_menu()