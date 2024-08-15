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
    # Collect and validate user input
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
            print("Passwords don't match, please try again!")
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
        if user[5] in ['inventory','superuser']:
            print("9. Inventory Staff Menu")
        print("10. Exit")

        choice = input("Enter your choice: ")

        if choice == '10':
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
        elif choice == '9' and user[5] in ['inventory','superuser']:
            inventory_menu(user[0],user[5])
        else:
            print("Invalid choice. Please try again!")

def login_sys(username, password):
    users = read_users()

    for user in users:
        if user[0] == username and user[1] == password:
            if user[6] == 'True':
                print(f"Login successful. Welcome {user[0]} ({user[5]})")
                if user[5] in ['superuser', 'admin', 'inventory']:  # Call user_menu for superuser, admin, and inventory
                    user_menu(user)  # Call user_menu with user details
                elif user[5] == 'customer':
                    customer_menu(user[0],user[5],read_threshold())
            else:
                print(f"User {username} is not approved yet. Please contact admin to approve...") #
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
                    # Skipping invalid user entry
                    pass
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
    phone_num = input("Enter phone number for new user: ")
    role = input("Enter role for new user (customer/admin/inventory/superuser): ").lower()
    ic_passport = input("Enter IC or passport for new user:")
    city = input("Enter city for new user:")
    approved = 'True'
    sign_up(username, password, phone_num, ic_passport, city, role)
    print("User added.")

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



#HENG WEI JIE #TP075936
#Customer Management

CUSTOMER_PURCHASE_LIST = 'customer_purchase.txt'

def read_orders():
    orders = []
    try:
        with open(CUSTOMER_PURCHASE_LIST, 'r') as file:
            for line in file:
                order = line.strip().split(',')
                if len(order) == 6:
                    try:
                        order_type = order[0]
                        brand = order[1]
                        item_name = order[2]
                        quantity = int(order[3])
                        price = float(order[4])
                        paid = order[5] == 'True'
                        status = order[6]

                        order = (order_type, brand, item_name, quantity, price, paid, status)
                        orders.append(order)
                    except ValueError as e:
                        print(f"Error processing line: {line}. Error: {e}")
                else:
                    print(f"Invalid line format: {line}")
    except FileNotFoundError:
        print(f"File '{CUSTOMER_PURCHASE_LIST}' not found.")
    except IOError as e:
        print(f"Error reading file: {e}")
    return orders


def write_customer_list(orders):
    with open(CUSTOMER_PURCHASE_LIST, 'w') as file:
        for order in orders:
            order_type, brand, item_name, quantity, price, paid, status = order
            paid_str = 'True' if paid else 'False'
            file.write(f"{order_type},{brand},{item_name},{price},{quantity},{paid_str},{status}\n")


def customer_menu(name, role, lowstock_threshold):
    while True:
        print("\nCustomer Menu")
        print("1. Purchase Order")
        print("2. Service/Repair Order")
        print("3. Modify Order")
        print("4. Make Payment")
        print("5. Inquire Order Status")
        print("6. Cancel Order")
        print("7. Reports")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            place_order(name, role, lowstock_threshold)
        elif choice == '2':
            place_service_order()
        elif choice == '3':
            modify_order()
        elif choice == '4':
            make_payment()
        elif choice == '5':
            inquire_order_status()
        elif choice == '6':
            cancel_order()
        elif choice == '7':
            generate_reports()
        elif choice == '8':
            print("Logging out.")
            break
        else:
            print("Invalid choice. Please try again.")


def place_order(name, role, lowstock_threshold):
    # Display the current inventory to the customer
    inventory_list = read_inventory(name, role)
    display_inventory(inventory_list, name, role, lowstock_threshold)

    # Allow the customer to input their order
    while True:
        item_index = input("Enter item number to order (or 'exit' to cancel): ")
        if item_index.lower() == 'exit':
            return None
        elif item_index.isnumeric():
            item_index = int(item_index) - 1
            if 0 <= item_index < len(inventory_list):
                item = inventory_list[item_index]
                break
            else:
                print("Invalid item number.")
        else:
            print("Invalid input.")

    # Ask for the quantity of the item they wish to order
    while True:
        quantity = input("Enter quantity: ")
        if quantity.isnumeric() and int(quantity) > 0:
            quantity = int(quantity)
            if quantity <= item[2]:
                break
            else:
                print("Insufficient stock available for this item.")
        else:
            print("Invalid quantity.")

    # Calculate the total price
    total_price = item[3] * quantity

    # Create an order list: [order_type, brand, item_name, quantity, price, paid, status]
    order = ['Preorder', item[1], item[0], quantity, item[3], False, 'Pending']

    # Add the order to the list of orders
    orders = read_orders()  # Read current orders
    orders.append(order)    # Add new order
    write_customer_list(orders)  # Write all orders back to the file

    print(f"Order placed successfully! You ordered {quantity}x {item[1]} for a total of RM{total_price:.2f}.")

def place_service_order(inventory_list, display_inventory):
    orders = read_orders()  # Read current orders
    if not orders:
        print("No orders available to repair.")
        return

    item = input("Enter the item you want to repair: ").lower()

    # Check if the item exists and has a paid order
    paid_orders = [order for order in orders if order[2].lower() == item and order[5] and order[0] == 'Preorder']

    if not paid_orders:
        print(f"No paid orders found for item '{item}'. Please ensure the item has a paid order before placing a service/repair order.")
        return

    # Calculate repair cost and time
    item_details = next((i for i in inventory_list if i[0].lower() == item), None)
    if item_details:
        total_price = item_details[3] * 0.2  # Assume repair cost is 20% of the item price
        repair_time = item_details[4]  # Assume the repair time is the fifth element
        print(f"Total Price for repair: RM{total_price:.2f}")
        print(f"Estimated repair time: {repair_time} days")

        # Create the repair order
        new_order = ('Repair', item, 1, total_price, False, 'Pending')
        orders.append(new_order)
        write_customer_list(orders)
        print("Service/Repair Order placed successfully!")
    else:
        print(f"Item '{item}' not found in inventory.")

def modify_order(inventory_list, display_inventory):
    orders = read_orders()  # Read current orders
    if not orders:
        print("No orders available to modify.")
        return

    for i, order in enumerate(orders):
        print(f"Order {i + 1}: {order}")

    try:
        order_number = int(input("Enter the order number to modify: ")) - 1
        order = orders[order_number]
    except (ValueError, IndexError):
        print("Invalid order number.")
        return

    if order[5]:  # Check if the order is paid
        print("Cannot modify a paid order.")
        return

    display_inventory(inventory_list)  # Display the inventory to allow selection

    while True:
        item = input("Enter the new item: ").lower()
        if any(i[0].lower() == item for i in inventory_list):
            break
        else:
            print("Item not found. Please enter a valid item.")

    item_details = next((i for i in inventory_list if i[0].lower() == item), None)
    if item_details:
        if order[0] == 'Preorder':
            while True:
                try:
                    quantity = int(input(f"Enter the new quantity of {item}: "))
                    if 0 < quantity <= item_details[2]:
                        break
                    else:
                        print(f"Invalid quantity. Please enter a number between 1 and {item_details[2]}.")
                except ValueError:
                    print("Please enter a valid number.")
            total_price = item_details[3] * quantity
        else:
            quantity = 1
            total_price = item_details[3] * 0.2

        new_order = ('Preorder', item, quantity, total_price, False, 'Pending')
        orders[order_number] = new_order
        write_customer_list(orders)
        print("Order modified successfully!")
    else:
        print(f"Item '{item}' not found in inventory.")


def make_payment():
    orders = read_orders()  # Read current orders
    if not orders:
        print("No orders available to make payment.")
        return

    for i, order in enumerate(orders):
        print(f"Order {i + 1}: {order}")

    try:
        order_number = int(input("Enter the order number to make payment: ")) - 1
        order = orders[order_number]
    except (ValueError, IndexError):
        print("Invalid order number.")
        return

    if order[5]:  # Check if the order is already paid
        print("Order is already paid.")
        return

    while True:
        try:
            payment = float(input(f"Enter the payment amount for the order (RM{order[3]}): "))
            if payment == order[3]:
                orders[order_number] = (order[0], order[1], order[2], order[3], True, 'Paid')
                write_customer_list(orders)
                print("Payment successful!")
                break
            else:
                print(f"Payment must be exactly RM{order[3]:.2f}. Please try again.")
        except ValueError:
            print("Please enter a valid amount.")


def inquire_order_status():
    orders = read_orders()  # Read current orders
    if not orders:
        print("No orders found.")
        return

    print("Current Orders:")
    for order in orders:
        print(order)

def cancel_order():
    orders = read_orders()  # Read current orders
    if not orders:
        print("No orders available to cancel.")
        return

    for i, order in enumerate(orders):
        print(f"Order {i + 1}: {order}")

    try:
        order_number = int(input("Enter the order number to cancel: ")) - 1
        order = orders[order_number]
    except (ValueError, IndexError):
        print("Invalid order number.")
        return

    if order[5]:  # Check if the order is paid
        print("Cannot cancel a paid order. Money is non-refundable.")
        return

    # Remove the order from the in-memory list
    orders.pop(order_number)

    # Write the remaining orders back to the file
    write_customer_list(orders)
    print("Order cancelled successfully.")

def generate_reports():
    orders = read_orders()  # Read current orders
    if not orders:
        print("No orders found.")
        return

    print("\nReports:")
    for i, order in enumerate(orders):
        print(f"Order {i + 1}: {order}")




#LOH JIAN FENG #TP076480
#Inventory Management
def inventory_menu(name, role):
    lowstock_threshold = read_threshold()
    inventory_log(name,role,"Log in","User logged in")
    while True:
        print("\nInventory Menu")
        print("1:Purchase \n2:Stock check/update \n3:Check purchase order status \n4:Modify,Cancel or Mark as received purchase order \n5:Change Low stock threshold \n6:Report(Inventory Log) \n7:EXIT ")
        inventory_func = int(input("Enter the choice"))
        if inventory_func == 1:
            purchase_inventory(name, role,lowstock_threshold)
        elif inventory_func == 2:
           display_inventory(read_inventory(name, role),name, role,lowstock_threshold)
           update_inventory(name, role)
        elif inventory_func == 3 :
            display_purchase_order(name,role,read_purchase_list(name,role))
        elif inventory_func == 4 :
            if role == 'inventory':
                modify_cancel_received_order(name,role,read_purchase_list(name,role))
            else:
                print("Only Inventory staff can modify the purchase order")
        elif inventory_func == 5 :
            save_threshold(change_threshold(name,role,lowstock_threshold))
        elif inventory_func == 6:
            log_menu(name, role)
        elif inventory_func == 7:
           print("Exiting...")
           return
        else:
           print("Invalid")
#Reading inventory in list of list
def read_inventory(name, role):
    # Check the inventory file
    try:
        with open("inventory.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        inventory_log(name, role, "Read inventory", "Failed to read inventory files")
        print("Inventory file not found.")
        return

    inventory_data = []
    for i, line in enumerate(lines, 1):#Loop through the lines starting from 1
        line = line.strip() #remove whitespace
        if len(line)== 0: #skip empty line
            continue

        try:
            columns = line.split(",")
            #Validating the data
            if len(columns) != 4:
                print(f"Warning: Invalid data in line {i}. Skipping.")
                continue
            #Putting item in a list of list
            brand,item_name, quantity, price = columns
            inventory_data.append([brand,item_name, int(quantity), float(price)])
        except ValueError:
            print(f"Warning: Invalid value in line {i}. Skipping.")
    inventory_log(name, role, "Read inventory", "Read inventory files")
    return inventory_data

#Display the inventory stock
def display_inventory(inventory_data,name, role,lowstock_threshold):
    inventory_log(name, role, "Display inventory", "Displayed inventory items")
    if len(inventory_data) != 0 :
        total_inventory = 0
        print("Current Inventory:")
        for i, item in enumerate(inventory_data ,1): #Loop until printing all of the item
            total_each_inv_item = item[2] * item[3]
            total_inventory = total_each_inv_item + total_inventory
            #Print low stock warning
            low_stock_warning = ""
            if item[2] <= lowstock_threshold :
                low_stock_warning = "LOW STOCK !!!"

            print(f"{i}.Brand: {item[0]}, Item name: {item[1]}, Quantity: {item[2]}, Price: RM{item[3]:.2f} {low_stock_warning}")
        if role in ['superuser','inventory']:
            print(f"Total value of inventory is {total_inventory}")
    else:
        print("Inventory is empty.")
def display_purchase_order(name,role,purchase_file_data):
    inventory_log(name, role, "Display purchase file", "Displayed purchase file items")
    if len(purchase_file_data) != 0:
        print("Current purchase order:")
        for i, item in enumerate(purchase_file_data, 1):
            print(f"{i}.Brand: {item[0]}, Item name:{item[1]}, Quantity:{item[2]}, Price per unit:RM{item[3]:.2f}, Total:{item[4]}, Status:{item[5]}, Ordered by:{item[6]}, Role:{item[7]}")
    else:
        print("Purchase file is empty")
def purchase_inventory(name, role,lowstock_threshold):
    inventory_list= read_inventory(name, role)
    display_inventory(inventory_list,name, role,lowstock_threshold)
    section_purchase_list =[]
    while True:
        purchase_item = input("""Enter item number to purchase, "new" for a new item, or "exit" to exit: """ )
        if purchase_item.lower().strip() == "exit":
            return None
        elif purchase_item.lower().strip() == "new" :
            while True :
                manufacture_brand = input("Enter manufacture brand: ")
                item_name = input("Enter item name: ")
                while True:
                    quantity = input("Enter quantity: ")
                    if quantity.isnumeric()and int(quantity) > 0:
                        quantity = int(quantity) #set quantity to integer
                        break
                    else:
                        print("Invalid quantity")
                while True:
                    try:
                        price = float(input("Enter price per item : "))
                        if price > 0 :
                            break
                        else:
                            print("Price cannot be 0")
                    except ValueError:
                        print("Invalid price format")
                section_purchase_list.append([manufacture_brand,item_name, quantity, price,name,role])
                print(f"{item_name} added to purchase order.")
                while True:
                    addmore_option = input("Do you want to add more ? (Y/N)")
                    if addmore_option.lower().strip() == 'y':
                        break
                    elif addmore_option.lower().strip() == 'n':
                        return purchase_summary(name, role,section_purchase_list)
                    else:
                        print("Invalid input. Please Enter Y or N only")

        elif purchase_item.isnumeric(): #validate
            index_item = int(purchase_item) - 1
            if 0 <= index_item < len(inventory_list) :
                item = inventory_list[index_item]
                while True:
                    quantity = input(f"Enter quantity to purchase for {item[0]} {item[1]} ")
                    if quantity.isnumeric() and int(quantity)> 0  :
                        quantity = int(quantity)
                        break
                    else:
                        print("Invalid quantity")
                section_purchase_list.append([item[0],item[1],quantity,item[3],name, role])
                print(f"{item[0]} {item[1]} added to purchase list.")
                while True:
                    addmore_option = input("Do you want to add more ? (Y/N)")
                    if addmore_option.lower().strip()=='y' :
                        break
                    elif addmore_option.lower().strip()== 'n':
                        return purchase_summary(name, role,section_purchase_list)
                    else :
                        print("Invalid")
    else :
        print("Invalid input")
def purchase_summary(name, role, purchase_list):
    total_purchase = 0
    for i, item in enumerate(purchase_list, 1): # start counting from 1
        total_eachitem = item[2] * item[3]
        total_purchase = total_purchase + total_eachitem
        print(f"{i}, {item[0]} {item[1]}: Quantity:{item[2]},Cost per unit:RM{item[3]:.2f}, Total:RM{total_eachitem} ")
    print(f"The total purchase amount is RM{total_purchase}")
    while True:
        payment_status = input("Pay now?(Y/N):")
        if payment_status.lower().strip() =='y':
            payment_status = "PAID"
            break
        elif payment_status.lower().strip() =='n':
            payment_status = "UNPAID"
            break
        else:
            print("Invalid choice")
        # Update each item in the list with the new details
    for i in range(len(purchase_list)): #loop thru the purchase list, start counting i from 0
        inventory_log(name, role, "Purchase", f"Purchased item{purchase_list[i][0]} {purchase_list[i][0]}")
        total_cost = purchase_list[i][2] * purchase_list[i][3]
        purchase_list[i] = [purchase_list[i][0], purchase_list[i][1], purchase_list[i][2], purchase_list[i][3],total_cost, payment_status, name, role]
    print("Added to purchase list")
    write_purchase_list_in_append(name, role ,purchase_list)
def write_purchase_list_in_append(name, role ,purchase_list):
    try:
        with open("purchase_list.txt", "a") as file:
            for item in purchase_list:
                file.write(f"{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]},{item[6]},{item[7]}\n")
            inventory_log(name, role, "Write in purchase order", "Wrote purchase order file ")
    except FileNotFoundError:
        inventory_log(name, role, "Write in purchase order", "Failed to write purchase order files")
        print("Inventory file not found.")
def modify_cancel_received_order(name,role,purchase_file_data):
    display_purchase_order(name,role,purchase_file_data)
    while True:
        modify_choice = int(input("Enter the item index you want to modify ,cancel or mark as received: "))- 1
        if 0 <= modify_choice < len(purchase_file_data):
            break
        else:
            print("Invalid item index.")

    while True:
        modify_input = input("Enter 'm' to modify a order, 'c' to cancel a order, 'r' as received (type 'exit' to quit):  ")
        if modify_input.lower().strip() == 'm':
            if purchase_file_data[modify_choice][5] == "PAID":
                print("Cannot modify or cancel a paid order.")
                return
            else:
                while True :
                    new_quantity = input("Enter new quantity: ")
                    if new_quantity.isnumeric() and int(new_quantity) >= 0 :
                        new_quantity = int(new_quantity)
                        purchase_file_data[modify_choice][2] = new_quantity #assign new quantity to purchase_file_list[user input index(inner list)][3th element in the inner list]
                        # Recalculate the total cost
                        price_per_item = purchase_file_data[modify_choice][3]#get price per item from purchase_file_list[user input index(inner list)][4th element in the inner list]
                        new_total = new_quantity * price_per_item
                        purchase_file_data[modify_choice][4] = new_total #assign new total to purchase_file_list[user input index(inner list)][5th element in the inner list]
                        print(f"Quantity of {purchase_file_data[modify_choice][0]} {purchase_file_data[modify_choice][1]} is changed to {new_quantity}")
                        inventory_log(name,role,"Modify purchase order",f"Quantity of {purchase_file_data[modify_choice][0]} {purchase_file_data[modify_choice][1]} is changed to {new_quantity}")
                        write_purchase_list(name, role, purchase_file_data)
                        return
                    else:
                        print("Invalid input. Please enter a non-negative number.")

        elif modify_input.lower().strip() == 'c':
            if purchase_file_data[modify_choice][5] == "PAID":
                print("Cannot modify or cancel a paid order.")
                return
            else:
                inventory_log(name, role, "Canceled order", f"Canceled {purchase_file_data[modify_choice][0]} {purchase_file_data[modify_choice][1]} ")
                purchase_file_data.pop(modify_choice) # Delete whole line in the data list
                print("Order has been canceled.")
                write_purchase_list(name, role, purchase_file_data)
                return
        elif modify_input.lower().strip() =='r': # Mark item as received
            if purchase_file_data[modify_choice][5] == "PAID":
                mark_item_received(name, role, purchase_file_data[modify_choice])
                inventory_log(name, role, "Received item", f"Item {purchase_file_data[modify_choice][0]} {purchase_file_data[modify_choice][1]} received")
                purchase_file_data.pop(modify_choice)  # Remove the received item from purchase list
                print("Order has been marked as received and updated in the inventory.")
                write_purchase_list(name, role, purchase_file_data)
                return
            else:
                print("Only paid orders can be marked as received.")
                return
        elif modify_input.lower().strip()=='exit':
            return None
        else:
            print("Invalid input")
def mark_item_received(name, role, item):
    inventory_list = read_inventory(name, role)
    item_found = False

    # Check if the item already exists in the inventory
    for inventory_item in inventory_list:
        if inventory_item[0] == item[0] and inventory_item[1] == item[1]:
            inventory_item[2] += item[2]  # Update quantity
            item_found = True
            break

    if item_found == False: # If item does not exist in inventory, append it as a new item
        inventory_list.append([item[0], item[1], item[2], item[3]])

    # Write the updated inventory back to the file
    write_inventory(inventory_list)
    inventory_log(name, role, "Received Inventory", f"Item {item[1]} received with quantity {item[2]} and added to inventory.")
    print(f"Item {item[1]} has been received and added to inventory.")

def write_purchase_list(name,role,purchase_list):
    try:
        with open("purchase_list.txt", "w") as file:
            for item in purchase_list:
                file.write(f"{item[0]},{item[1]},{item[2]},{item[3]},{item[4]},{item[5]},{item[6]},{item[7]}\n")
            inventory_log(name, role, "Write in purchase order", "Wrote purchase order file ")
    except FileNotFoundError:
        inventory_log(name, role, "Write in purchase order", "Failed to write purchase order files")
        print("Inventory file not found.")
def read_purchase_list(name, role):
    # Check the inventory file
    try:
        with open("purchase_list.txt", "r") as file:
            lines = file.readlines() #read inventory_purchase_file
    except FileNotFoundError:
        inventory_log(name, role, "Read inventory", "Failed to read inventory files")
        print("Inventory file not found.")
        return

    purchase_order_data = []
    for i, line in enumerate(lines, 1):#Loop through the lines starting from 1
        line = line.strip() #remove whitespace
        if len(line)== 0: #skip empty line
            continue

        try:
            columns = line.split(",")
            #Validating the data
            if len(columns) != 8:
                print(f"Warning: Invalid data in line {i}. Skipping.")
                continue
            #Putting item in a list of list
            brand,item_name, quantity, price , total_price,status,name,role= columns #upcak columns to brand,item_name, quantity, price , total_price,status,name,role
            purchase_order_data.append([brand,item_name, int(quantity), float(price),float(total_price),status,name,role])
        except ValueError:
            print(f"Warning: Invalid data in line {i}. Skipping.")
    inventory_log(name, role, "Read purchase order file", "Read purchase order file")
    return purchase_order_data
def update_inventory(name, role): #Function for update inventory
    inventory_list = read_inventory(name, role)
    while True:
        initial_input_1 = input("Do you want to update inventory ?(Y/N) ")
        if initial_input_1.lower().strip() == 'y':
            break
        elif initial_input_1.lower().strip() == 'n':
            return None
        else:
            print("Invalid input")
    while True:
        update_item = input("Enter item index number to update: ")
        if update_item.isnumeric():
            index_item = int(update_item) - 1
            if 0 <= index_item < len(inventory_list):
                break
            else:
                print("Invalid item index number")
        else :
            print("Invalid input")
    item = inventory_list[index_item] #allocate the item line in inventory list using the index_item.
    new_manufacture_brand = input(f"Enter new brand for {item[0]} {item[1]} (or 0 to keep current): ")
    if new_manufacture_brand == '0':
        new_manufacture_brand = item[0]

    new_item_name = input(f"Enter new name for {item[0]} {item[1]} (or 0 to keep current): ")
    if new_item_name == '0':
        new_item_name = item[1]
    while True:
        new_quantity = input(f"Current quantity for {item[0]} {item[1]} is {item[2]}. Enter new quantity(or 0 to keep current): ")
        if new_quantity == '0':
            new_quantity = item[2]
            break
        elif new_quantity.isnumeric() and int(new_quantity) >= 0:
            new_quantity = int(new_quantity)
            break
        else:
            print("Invalid input. Please enter a non-negative number.")
    while True:
        new_price = input(f"Current price per unit for {item[0]} {item[1]} is {item[3]}. Enter new price per unit (or 0 to keep current): ")
        if new_price == '0':
            new_price = item[3]
            break
        try:
            new_price = float(new_price)
            if new_price >= 0:
                break
            else:
                print("Price cannot be negative. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    inventory_list[index_item] = [new_manufacture_brand, new_item_name, new_quantity, new_price]  #Save updated list to the inventory list(allocated by index number(index_item))
    inventory_log(name, role, "Update Inventory", f"Updated Brand: {item[0]} to {new_manufacture_brand}, Item name: {item[1]} to {new_item_name}, Quantity: {item[2]} to {new_quantity}, Price :{item[3]} to {new_price} ")
    print(f"{item[0]} {item[1]} updated. New brand name: {new_manufacture_brand}, New name: {new_item_name} New quantity: {new_quantity}, New price per unit: {new_price}")
    write_inventory(inventory_list)


def write_inventory(inventory_list):
    with open("inventory.txt", "w") as file:
        for item in inventory_list:
            file.write(f"{item[0]},{item[1]},{item[2]},{item[3]}\n")
def change_threshold(name,role,lowstock_threshold):
    print(f"Current low stock threshold: {lowstock_threshold}")
    while True:
        try:
            new_threshold = int(input("Enter new threshold (or 0 to keep current): "))
            if new_threshold < 0:
                print("Threshold must be a non-negative integer.")
            elif new_threshold == 0:
                print(f"Threshold remain the same ")
                inventory_log(name, role, "Change threshold",f"Changed low stock threshold from {lowstock_threshold} to {lowstock_threshold}")
                return lowstock_threshold
            else:
                print(f"New threshold set to {new_threshold}")
                inventory_log(name,role,"Change threshold",f"Changed low stock threshold from {lowstock_threshold} to {new_threshold}")
                return new_threshold
        except ValueError:
            print("Please enter a valid integer.")
def read_threshold():
    try:
        with open("low_stock_threshold.txt","r") as file:
            threshold = int(file.read())
            return threshold
    except FileNotFoundError:
        print("Low Stock threshold file not found.")
        return 0
def save_threshold(threshold):
    with open("low_stock_threshold.txt", "w") as file:
        file.write(str(threshold))
def log_menu(name,role):
    log_data = read_inventory_log(name,role)

    print("Log Menu: ")
    print("1. Display Inventory Log")
    print("2. Delete Inventory Log")
    print("3. Back to Inventory Menu")
    while True:
        choice = input("Enter your choice: ")

        if choice == '1':
            display_inventory_log(name,role,log_data)
            break
        elif choice == '2':
                confirm_delete = input("Are you sure you want to delete the entire log? (y/n): ")
                if confirm_delete.lower().strip() == 'y':
                    delete_inventory_log(name,role)
                break
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please try again.")
#Record inventory activity in log file.
def read_inventory_log(name,role):
    try:
        with open('inventory_log.txt', 'r') as inventory_log_file:
            log_lines = inventory_log_file.read()#read all line
            log_lines =log_lines.strip().split('\n') # Split content into lines
    except FileNotFoundError:
        print("Log file not found")
        return
    log_data = []
    for i, line in enumerate(log_lines,1):
            line = line.strip() #remove whitespace
            if len(line) == 0 : #skip empty lines
                continue
            try:
                components = line.split(",")#split the log components out
                if len(components) != 5: # Check if the line has exactly 5 components
                    print(f"Warning: Invalid data in line {i}. Skipping.")
                    continue
                log_name,log_role,activity,detail,time = components #unpacks components to log_name,log_role,activity,detail,time
                log_data.append([log_name,log_role,activity,detail,time])
            except:
                print(f"Warning: Invalid value in line {i}. Skipping.")
    inventory_log(name,role,"Read Log","Read inventory log file")
    return log_data
def inventory_log(name,role,activity,details):
    try:
        with open("inventory_log.txt", "a") as inventory_log_file:
            activity_list = (f"{name},{role},{activity},{details},{time()} \n")
            inventory_log_file.write(activity_list)
    except FileNotFoundError:
        print("Log file not found")

def display_inventory_log(name,role,log_data):
    inventory_log(name,role,"Display log", "Displayed all log file")
    if len(log_data) > 0 :
        print("Inventory Log Report:")
        for log_item in log_data: #Loop thru the log_line
            print(f"Name: {log_item[0]},Role: {log_item[1]},Activity: {log_item[2]},Detail: {log_item[3]},At: {log_item[4]}")

    else:
        print("The inventory log is empty.")

def delete_inventory_log(name,role):
        with open('inventory_log.txt','w') as inventory_log_file :
            inventory_log_file.write("")
        print("Inventory log has been deleted")
        inventory_log(name,role,"Delete log", "ALL Inventory log deleted")


#def save_inventory(inventory_list):

if __name__ == "__main__":
    main_menu()

