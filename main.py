def main_m():
    function = int(input("Welcome to KLCCC automated system\n1: Sign up\n2: Login\n3: Exit\n"))
    while function < 1 or function > 3: #validate the option
        function = int(input("Invalid option\n\n1: Sign up\n2: Login\n3: Exit\n"))
    return function
main_m()