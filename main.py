sp_user="admin,admin123" #Define Super-user username & password
def main_menu():
    while True:
        print("Welcome to KLCCC System")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            #user_management.sign_up()
            signup_sys()
            break
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
    login_pass=input("Enter password: ")
    sp_fields = sp_user.split(",") #Split string to Char
    file = open("User_details.txt","r")
    for i in file:
        user_fields= i.split(",")

    if login_name == sp_fields[0] and login_pass == sp_fields[1]: #Check name and Password
        print("Login Successful")
        print("Welcome Super user ! ")
        #Call function for super-user
    elif login_name == user_fields[0] and login_pass== user_fields[1] :
        print("Login Successful")
    else:
        print("Username or Password incorrect, please try again")
def signup_sys():
    sign_name = input("Enter username: ")
    sign_pass = input("Enter password: ")
    file= open("User_details.txt","a")
    file.write("\n"+sign_name)
    file.write(",")
    file.write(sign_pass)
    file.close()
#Sign up system here
main_menu()