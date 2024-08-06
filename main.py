from datetime import datetime

User_details = 'User_details.txt'
ORDER_STATUS_FILE = 'Order_status.txt'
SYSTEM_USAGE_FILE = 'System_usage.txt'
def main_menu():
    while True:
        print("Welcome to KLCCC System")
        print("1. Sign Up")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            sign_up_process()
        elif choice == '2':
            login_process()
        elif choice == '3':
            print("Exiting the system.")
            break
        else:
            print("Invalid choice. Please try again!\n")
def sign_up_process():
    # Loop until a valid username is provided
    while True:
        username = input("Enter username: ")
        if len(username.strip()) > 0:
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
    while True:
        phone_num = input("Enter phone number: ").strip()
        if phone_num.isdigit() and 10 <= len(phone_num) <= 12:
            break
        else:
            print("Provide a valid phone number (10-12 digits).")
    while True:
        ic_passport = input("Enter IC/Passport number: ").strip()
        if ic_passport.isdigit() and 12 <= len(ic_passport) <= 15:
            break
        else:
            print("Provide a valid IC/Passport number (12-15 digits).")
    while True:
        city = input("Enter city of domicile: ").strip()
        if len(city) > 0:
            break
        else:
            print("Provide a valid city of domicile.")
    while True:
        role = input("Enter role (customer/admin/inventory/superuser): ").lower().strip()
        valid_roles = ['customer', 'admin', 'superuser','inventory']
        if role.isdigit():
            print("Role cannot be a number. Please enter a valid role.")
        elif role in valid_roles:
            print(f"Role '{role}' is valid.")
            break
        else:
            print("Invalid role. Please enter 'customer', 'admin', or 'superuser'.")

    sign_up(username, password, phone_num, ic_passport, city, role)
    print("Signed up successfully. Awaiting approval process...")

def login_process():
    username = input("Enter username: ")
    password = input("Enter password: ")
    login_sys(username, password)

def approve_user_process():
    super_user = input("Enter your role: ").lower()
    username = input("Enter username to approve: ")
    approve_user(super_user, username)
def time():
    now = datetime.now()
    date_string = now.strftime('%Y-%m-%d %H:%M:%S')
    return date_string

#User Management
#CHAI TIAN CHENG
#TP075051
def user_menu(user):
    while True:
        print(f"User Menu - {user[0]} ({user[2]})")
        print("1. Check Customer Order Status")
        if user[5] in ['superuser', 'admin']:
            print("2. Verify New Customers")
            print("3. Reports")
        if user[5] == 'superuser':
            print("4. Add Users")
            print("5. Modify User Personal Details")
            print("6. Disable User Access")
            print("7. Inquiry of User’s system usage")
            print("8. Approve User")
        print("9. Exit")

        choice = input("Enter your choice: ")

        if choice == '9':
            print("Exiting the system.")
            break
        elif choice == '1':
            check_order_status()
        elif choice == '2' and user[5] in ['superuser', 'admin']:
            verify_new_customer(user[5])
        elif choice == '3' and user[5] in ['superuser', 'admin']:
            generate_reports()
        elif choice == '4' and user[5] == 'superuser':
            add_user()
        elif choice == '5' and user[5] == 'superuser':
            modify_user_details()
        elif choice == '6' and user[5] == 'superuser':
            disable_user_access()
        elif choice == '7' and user[5] == 'superuser':
            inquiry_sys_usage()
        elif choice == '8' and user[5] == 'superuser':
            approve_user_process()
        else:
            print("Invalid choice. Please try again!")

def login_sys(username, password):
    users = read_users()
    print("Loaded users for debugging:")
    for user in users:
        print(user)  # Print each user for debugging

    for user in users:
        if user[0] == username and user[1] == password:
            if user[6] == 'True':
                print(f"Login successful. Welcome {user[0]} ({user[5]})")
                print(f"Role: {user[5]}") #For debugging
                if user[5] == 'superuser':
                    user_menu(user)  # Call user_menu with user details
                elif user[5] == 'inventory':
                    inventory_menu(user[0],user[5])
            else:
                print(f"User {username} is not approved yet. Please contact admin to approve...")
            return
    print("Invalid username or password.")
# approval process
def approve_user(super_user, username):
    users = read_users()
    if super_user not in ['superuser', 'admin']:
        print("Only superuser and admin can approve.")
        return

    for user in users:
        if user[0] == username:
            user[6] = 'True'
            write_users(users)
            print(f"User {username} approved successfully.")
            return
    print(f"User {username} not found.")
# Function to read users from file
def  read_users():
    users = []
    try:
        with open(User_details, 'r') as file:
            for line in file:
                user = line.strip().split(',')
                if len(user) == 8:  # Ensure there are exactly 8 fields
                    users.append(user)
                else:
                    print(f"Skipping invalid user entry: {line.strip()}")
    except FileNotFoundError:
        print("User details file not found.")
    return users
# Function to write users to file
def write_users(users):
    with open(User_details, 'w') as file:
        for user in users:
            file.write(','.join(user) + '\n')


# Function to sign up a new user
def sign_up(username, password, phone_num, ic_passport, city,role):
    users = read_users()
    for user in users:
        if user[0] == username:
            print("Username already exists.")
            return

    approved = 'False'
    if role == 'superuser':
        approved = 'True'  # Superuser will be approved immediately

    users.append([username, password, phone_num, ic_passport, city,role, approved,time()])
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
    pending_users = [user for user in users if user[6] == 'False']
    if not pending_users:
        print("No new customers to verify.")
        return

    for user in pending_users:
        print(f"Pending user: {user[0]} ({user[2]})")

    username = input("Enter username to approve: ")
    approve_user(role, username)

# Generate reports
# Generate reports
def generate_reports():
    print("Generating reports...")
    try:
        users = read_users()
        for user in users:
            print(f"Username: {user[0]}, Role: {user[5]}, Active: {user[6]}, Datetime: {user[7]}")
        write_log("generate_reports", "Generate user reports", "Success", "System", time())
    except FileNotFoundError:
        print("No user data found.")
        write_log("generate_reports", "Generate user reports", "Failure", "System", time())

# Function to write log
def write_log(function, activity, status, user, datetime):
    with open("log.txt", "a") as logFile:
        logFile.write(f"{function},{activity},{status},{user},{datetime}\n")

# Add user for user_menu()
def add_user():
    print("Adding user...")
    username = input("Enter username for new user: ")
    password = input("Enter password for new user: ")
    role = input("Enter role for new user (customer/admin/inventory/superuser): ").lower()
    sign_up(username, password, role)

# Modify user details
def modify_user_details():
    print("Modifying user personal details...")
    username = input("Enter the username of the user to modify: ")
    users = read_users()
    for user in users:
        if user[0] == username:
            user[2] = input(f"Enter new phone number for {username} (current: {user[2]}): ")
            user[3] = input(f"Enter new IC/Passport number for {username} (current: {user[3]}): ")
            user[4] = input(f"Enter new city for {username} (current: {user[4]}): ")
            write_users(users)
            print(f"Details for {username} updated successfully.")
            return
    print(f"User {username} not found.")

# Disable user access
def disable_user_access():
    print("Disabling user access...")
    username = input("Enter the username to disable: ")
    users = read_users()
    for user in users:
        if user[0] == username:
            user[6] = 'False'
            write_users(users)
            print(f"Access for {username} disabled successfully.")
            return
    print(f"User {username} not found.")

# Inquiry of User's System Usage
def inquiry_sys_usage():
    print("Inquiring user's system usage...")
    try:
        with open(SYSTEM_USAGE_FILE, 'r') as file:
            usage = file.readlines()
            for entry in usage:
                print(entry.strip())
    except FileNotFoundError:
        print("No system usage data found.")

#Inventory Management #LOH JIAN FENG #TP076480
def inventory_menu(name, role):
    inventory_log(name,role,"Log in","User logged in")
    while True:
        print("\nInventory Menu")
        print("1:Purchase \n2:Stock check \n3:Check purchase order status \n4:Purchase Cart \n5:Report \n6:EXIT ")
        inventory_func = int(input("Enter the choice"))
        if inventory_func == 1:
            purchase_inventory(name, role)
        elif inventory_func == 2:
           display_inventory(read_inventory(name, role),name, role)
           update_inventory(name, role)
        elif inventory_func == 3 :
            continue
        elif inventory_func == 4 :
            continue
        elif inventory_func == 5 :
            continue
        elif inventory_func == 6:
           print("Exiting...")
           break
        else:
           print("Invalid")
#Reading inventory in list of list
def read_inventory(name, role):
    # Check the inventory file
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("Inventory file not found.")
        return

    inventory_data = []
    for i, line in enumerate(lines, 1):
        line = line.strip()
        if not line:
            continue

        try:
            columns = line.split(",")
            #Validating the data
            if len(columns) != 3:
                print(f"Warning: Invalid data in line {i}. Skipping.")
                continue
            #Putting item in a list of list
            name, quantity, price = columns
            inventory_data.append((name, int(quantity), float(price)))
        except ValueError:
            print(f"Warning: Invalid data in line {i}. Skipping.")
    inventory_log(name, role, "Read inventory", "Read inventory files")
    return inventory_data

#Display the inventory stock
def display_inventory(inventory_data,name, role):
    if len(inventory_data) != 0 :
        print("Current Inventory:")
        for i, item in enumerate(inventory_data ,1): #Loop until printing all of the item
            print(f"{i}.{item[0]}:Quantity:{item[1]},Price:RM{item[2]:.2f}")
        inventory_log(name, role, "Display", "Displayed inventory items")
    else:
        print("Inventory is empty.")
def purchase_inventory(name, role):
    inventory_list= read_inventory(name, role)
    display_inventory(inventory_list,name, role)
    purchase_list = []
    while True:
        purchase_item = input("""Enter item number to purchase, "new" for a new item, or "exit" to exit: """ )
        if purchase_item.lower() == "exit":
            return None
        if purchase_item.lower() == "new" :
            item_name = input("Enter item name: ")
            quantity = int(input("Enter quantity: "))
            price = float(input("Enter price: "))
            purchase_list.append((item_name, quantity, price,name, role,time()))
            print(f"{item_name} added to purchase order.")
            addmore_option = input("Do you want to add more ? (Y/N)")
            if addmore_option.lower() == 'y':
                continue
            elif addmore_option.lower() == 'n':
                break
            else:
                print("Invalid")
        elif purchase_item.isnumeric():
            index_item = int(purchase_item) - 1
            if 0 <= index_item < len(inventory_list) :
                item = inventory_list[index_item]
                quantity = int(input(f"Enter quantity to purchase for {item[0]} "))
                if quantity > 0 :
                    purchase_list.append((item[0],quantity,item[2],name, role,time()))
                    print(f"{item[0]}added to purchase list.")
                    addmore_option = input("Do you want to add more ? (Y/N)")
                    if addmore_option.lower()=='y' :
                        continue
                    elif addmore_option.lower()== 'n':
                        break
                    else :
                        print("Invalid")

                else :
                    print("Invalid quantity.")
            else :
                print("Invalid item number")
        else :
            print("Invalid input")
    if len(purchase_list) != 0 :
        purchase_summary(purchase_list)
def purchase_summary(purchase_list):
    total_purchase = 0
    for item in purchase_list:
        total = item[1] * item[2]
        purchase_list.append(total)
        print(f"{item[0]}: Quantity:{item[1]},Cost per unit:RM{item[2]:.2f}, Total:RM{item[3]:.2f} ")
    return purchase_list

def update_inventory(name, role): #Function for update inventory
    inventory_list = read_inventory(name, role)
    while True:
        initial_input_1 = input("Do you want to update inventory ?(Y/N) ")
        if initial_input_1.lower() == 'y':
            break
        elif initial_input_1.lower() == 'n':
            return None
        else:
            print("Invalid")
    item_name = input("Enter item name: ")
    for i, item in enumerate(inventory_list):
        if item[0] == item_name:
            new_quantity = int(input("Enter new quantity: "))
            inventory_list[i] = (item[0], new_quantity, item[2])
            print(f"{item_name} quantity updated to {new_quantity}.")
            #save_inventory(inventory_list)
            return
    print("Item not found in inventory.")

#Record inventory activity in log file.
def inventory_log(name,role,activity,details):
    try:
        with open("inventory_log.txt", "a") as inventory_log_file:
            activity_list = f"{name} , {role} , {activity} , {details} , {time()} \n"
            inventory_log_file.write(activity_list)
    except FileNotFoundError:
        print("Log file not found.")
        return
#def save_inventory(inventory_list):

if __name__ == "__main__":
    main_menu()

