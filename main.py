User_details = 'User_details.txt'
ORDER_STATUS_FILE = 'Order_status.txt'
SYSTEM_USAGE_FILE = 'System_usage.txt'
def main_menu():
    while True:
        print("Welcome to KLCCC System")
        print("1. Sign Up")
        print("2. Login")
        print("3. Approve User")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            #Loop until a valid username is provided
            while True:
                username = input("Enter username: ")
                if len(username.strip("")) > 0:
                    break
                else:
                    print("Provide a valid username")

            # Loop until passwords match
            while True:
                password = input("Enter password: ")
                if not password:
                    print("Provide a valid password")
                    continue
                elif len(password) < 8:
                    print("Password too short, must be at least 8 characters")
                    continue
                password1 = input("Re-enter your password: ")
                if password != password1:
                    print("Passwords don't match, please try again")
                else:
                    break
            role = input("Enter role (customer/admin/staff): ").lower()
            sign_up(username, password, role)
            break
        elif choice == '2':
            username = input("Enter username: ")
            password = input("Enter password: ")
            login_sys(username, password)
            break
        elif choice == '3':
            super_user = input("Enter your role: ").lower()
            username = input("Enter username to approve: ")
            approve_user(super_user, username)
            break
        elif choice == '4':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again!\n")
def time():
    from datetime import datetime
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d %H:%M:%S')
    return date_string

def user_menu(user):
    while True:
        print(f"User Menu - {user[0]} ({user[2]})")
        print("1. Check Customer Order Status")
        if user[2] in ['superuser', 'admin']:
            print("2. Verify New Customers")
            print("3. Reports")
        if user[2] == 'superuser':
            print("4. Add Users")
            print("5. Modify User Personal Details")
            print("6. Disable User Access")
            print("7. Inquiry of User’s system usage")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '8':
            print("Exiting the system.")
            break
        elif choice == '1':
            check_order_status()
        elif choice == '2' and user[2] in ['superuser', 'admin']:
            verify_new_customer(user[2])
        elif choice == '3' and user[2] in ['superuser', 'admin']:
            generate_reports()
        elif choice == '4' and user[2] == 'superuser':
            add_user()
        elif choice == '5' and user[2] == 'superuser':
            modify_user_details()
        elif choice == '6' and user[2] == 'superuser':
            disable_user_access()
        elif choice == '7' and user[2] == 'superuser':
            inquiry_sys_usage()
        else:
            print("Invalid choice. Please try again!")

def login_sys(username, password):
    users = read_users()
    for user in users:
        if user[0] == username and user[1] == password:
            if user[3] == 'True':
                print(f"Login successful. Welcome {user[0]} ({user[2]})")
            else:
                print(f"User {username} is not approved yet.")
            return
    print("Invalid username or password.")

# approval process
def approve_user(super_user, username):
    users = read_users()
    if super_user not in ['superuser','admin']:
        print("Only superuser and admin can approve.")
        return

    for user in users:
        if user[0] == username:
            user[3] = 'True'
            write_users(users)
            print(f"User {username} approved successfully.")
            return
    print(f"User {username} not found.")
# Function to read users from file
def read_users():
    users = []
    with open(User_details, 'r') as file:
        for line in file:
            users.append(line.strip().split(','))
    return users
def read_pending():
    users = []
    with open(Pending_approve, 'r') as file:
        for line in file:
            users.append(line.strip().split(','))
    return users
# Function to write users to file
def write_users(users):
    users.append(time())
    with open(User_details, 'w') as file:
        for user in users:
            file.write(','.join(user) + '\n')


# Function to sign up a new user
def sign_up(username, password, role):
    users = read_users()
    for user in users:
        if user[0] == username:
            print("Username already exists.")
            return

    #approved = 'False'
    #if role == 'customer':
        #approved = 'False'
    #elif role == 'admin':
        #approved = 'False'
    #elif role == 'superuser':
        #approved = 'True'  # Superuser will be approved

    users.append([username, password])
    write_users(users)
    print(f"User {username} signed up successfully. Awaiting approval.")

# Check customer order status
def check_order_status():
    print("Checking customer order status...")
    try:
        with open(ORDER_STATUS_FILE, 'r') as file:
            orders = file.readlines()
            for order in orders:
                print(order.strip())
    except FileNotFoundError:
        print("No order status found.")

# Verify new customer
def verify_new_customer(role):
    print("Verifying new customers...")
    if role not in ['superuser', 'admin']:
        print("Only superuser and admin can verify new customers.")
        return

    users = read_users()
    pending_users = [user for user in users if user[3] == 'False']
    if not pending_users:
        print("No new customers to verify.")
        return

    for user in pending_users:
        print(f"Pending user: {user[0]} ({user[2]})")

    username = input("Enter username to approve: ")
    approve_user(role, username)

# Generate reports
def generate_reports():
    print("Generating reports...")
    try:
        users = read_users()
        for user in users:
            print(f"Username: {user[0]}, Role: {user[2]}, Active: {user[3]}")
    except FileNotFoundError:
        print("No user data found.")

# Add user for user_menu()
def add_user():
    print("Adding user...")
    username = input("Enter username for new user: ")
    password = input("Enter password for new user: ")
    role = input("Enter role for new user (customer/admin/superuser): ").lower()
    sign_up(username, password, role)

# Modify user details
def modify_user_details():
    print("Modifying user personal details...")
    username = input("Enter the username of the user to modify: ")
    users = read_users()
    for user in users:
        if user[0] == username:
            new_username = input("Enter new username: ")
            new_password = input("Enter new password: ")
            new_role = input("Enter new role: ").lower()
            user[0] = new_username
            user[1] = new_password
            user[2] = new_role
            write_users(users)
            print("User details updated successfully.")
            return
    print("User not found.")

# Disable user access
def disable_user_access():
    print("Disabling user access...")
    username = input("Enter the username of the user to disable: ")
    users = read_users()
    for user in users:
        if user[0] == username:
            user[3] = 'False'
            write_users(users)
            print("User access disabled successfully.")
            return
    print("User not found.")

# Inquiry of User's System Usage
def inquiry_sys_usage():
    print("Inquiring user's system usage...")
    try:
        with open(SYSTEM_USAGE_FILE, 'r') as file:
            usage_records = file.readlines()
            for record in usage_records:
                print(record.strip())
    except FileNotFoundError:
        print("No system usage details found.")

if __name__ == "__main__":
    main_menu()
#Inventory Management
#def inventory_login():
#    while True:
#        print("1:Purchase \n2:Stock check \n3:Check purchase order status \n4:Purchase Cart \n5:Report \n6:EXIT ")
#        inventory_func = int(input("Enter the choice"))
#        if inventory_func == 1:
#           Call part list func
#        elif inventory_func == 2:
#           Call func
#        elif inventory_func == 3 :
#           Call func
#        elif inventory_func == 4 :
#           Call func
#        elif inventory_func == 5 :
#           Call func
#        elif inventory_func == 6:
#           print("Exiting...")
#           break
#        else:
#           print("Invalid")


#if __name__ == "__main__":
#    main_menu()