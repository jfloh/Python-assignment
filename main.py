User_details = 'User_details.txt'
def main_menu():
    while True:
        print("Welcome to KLCCC System")
        print("1. Sign Up")
        print("2. Login")
        print("3. Approve User")
        print("4. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            username = input("Enter username: ")
            password = input("Enter password: ")
            role = input("Enter role (customer/admin/superuser): ").lower()
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


# Function to write users to file
def write_users(users):
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

    approved = 'False'
    if role == 'customer':
        approved = 'False'
    elif role == 'admin':
        approved = 'False'
    elif role == 'superuser':
        approved = 'True'  # Superuser will be approved

    users.append([username, password, role, approved])
    write_users(users)
    print(f"User {username} signed up successfully. Awaiting approval.")

if __name__ == "__main__":
    main_menu()

