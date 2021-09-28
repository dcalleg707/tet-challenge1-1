
import time
import os
import http.client
#import constants

def print_title():
    os.system('clear')
    print('CDH Team presents...')
    print('''
        _____   _       _          _  ____  
        |  __ \\ (_)     | |        (_)|  _ \\ 
        | |  | | _  ___ | |_  _ __  _ | |_) |
        | |  | || |/ __|| __|| '__|| ||  _ < 
        | |__| || |\__ \| |_ | |   | || |_) |
        |_____/ |_||___/ \\__||_|   |_||____/ 
    ''')

    print('Welcome to DistriB CLI!', end='\n\n')

def main():
    print('***********************************')
    user_input = ""

    os.system('clear')
    print_title()
    try:
        while True:
            pwd = '[' + os.getcwd().replace("\\\\", "/") + ']'
            user_input = input(pwd + ' # ').split()
            command = user_input[0]
            args = user_input[1:] if len(user_input) > 1 else []

            print(f'<<TEST STRING: COMMAND: {command}; args {args}>>')
    
    except KeyboardInterrupt:
        print('\n\nBye!\n')


if __name__ == '__main__':
    main()

# Test connection
# try:
#     conn = http.client.HTTPConnection(constants.TABLE_SERVER, constants.TABLE_PORT)
#     conn.request("GET", "/ping")
# except ConnectionRefusedError:
#     os.system('clear')
#     print('Connection refused! Please contact the administrator')
#     time.sleep(3)
#     continue

# Connection
# try:
#     conn = http.client.HTTPConnection(constants.CONVERT_SERVER, constants.CONVERT_PORT)
#     conn.request("GET", f'/?value={ir}&actualIrType={actual_irt}&newIrType={new_irt}')
#     res = conn.getresponse()
#     # ANSWER
#     answer = res.read().decode(constants.ENCODING_FORMAT)
#     print('\nAnswer')
#     print(f': {answer} % {new_irt}')

#     print('\nPress any key to go back...')
#     input()
# except ConnectionRefusedError:
#     os.system('clear')
#     print('Connection refused! Please contact the administrator')
#     time.sleep(3)
#     continue

# MONTHS
# print_gen_table_header(init_value, ir, months)
# print('\nSet the periods amount to pay (enter \'q\' to quit)')
# data_to_send = input(': ')

# while(not (is_float(data_to_send) or data_to_send == 'q')):
#     print('Please, input an int number')
#     data_to_send = input(': ')
# if (data_to_send == 'q'): continue