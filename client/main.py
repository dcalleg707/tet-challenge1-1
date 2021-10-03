
import time
import os
import requests
import constants

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

def elemental_commands(cmd, args):
    # Manual
    if cmd == "man":
        if args:
            print(f'No manual entry for {args[0]}')
        else:
            print('What manual page do you want?\tTry \'man man\'')
    
    # Change Directory
    elif cmd == "cd":
        try:
            if args:
                if args[0] == "--help" or args[0] == '-h':
                    print('Usage: cd [dir]\nChange the shell working directory.\n')
                else:
                    directory = args if len(args) > 1 else args[0] 
                    os.chdir(directory)

        except FileNotFoundError as e:
            print(f'cd: {args[0]}: No such file or directory')
        except TypeError as e:
            print('cd: too many arguments')
    
    # List files
    elif cmd == "ls":
        params = [s for s in args if s[0] == "-"]
        no_params = [s for s in args if s[0] != "-"]
        args = no_params if len(params) != len(args) else []
        
        hidden = False
        if "-a" in params: hidden = True
        if "--help" in params:
            print('Usage: ls [OPTION]... [FILE]...\nList information about the FILEs (the current directory by default).\n\nMandatory arguments to long options are mandatory for short options too.\n\t-a                  do not ignore entries starting with .\n')
            return

        if len(args) > 1:
            for elem in args:
                try:
                    dirs = os.listdir(elem)
                    print(f'{elem}:')
                    for d in dirs:
                        if d[0] != "." or hidden:
                            print(d, end='  ')
                    print('\n')
                
                except FileNotFoundError as e:
                    print(f'ls: cannot access \'{elem}\': No such file or directory')
        else:
            dirs = os.listdir()
            for d in dirs:
                if d[0] != "." or hidden:
                    print(d, end='  ')
            print('')

    # Clear
    elif cmd == "clear":
        print_title()
    
    return cmd == "man" or cmd == "cd" or cmd == "ls" or cmd == "clear"

def command_checker(cmd, args):
    if not elemental_commands(cmd, args):
        if cmd == "upload":
            to_upload(args)
        elif cmd == "list-files":
            to_list_files()
        elif cmd == "download":
            print('DOWNLOAD')
        else:
            print(f'{cmd}: command not found')

def main():
    print('***********************************')
    user_input = ""

    os.system('clear')
    print_title()
    try:
        while True:
            pwd = '[' + os.getcwd().replace("\\\\", "/") + ']'
            shell_input = " ".join(input(pwd + ' # ').split())
            user_input = []
            start = 0
            inQuotes = False
            for i in range(len(shell_input)):
                if shell_input[i] == '"' or shell_input[i] == "'":
                    inQuotes = not inQuotes

                if (shell_input[i] == ' ' or i == len(shell_input) - 1) and not inQuotes:
                    end = i + 1 if i == len(shell_input) - 1 else i
                    user_input.append(shell_input[start:end])
                    start = i + 1
                    inQuotes = False
            
            command = user_input[0]
            args = user_input[1:] if len(user_input) > 1 else []

            #print(f'<<TEST STRING: COMMAND: {command}; args {args}>>')
            command_checker(command, args)
            
    except KeyboardInterrupt:
        print('\n\nBye!\n')

def test_connection(url, port):
    try:
        requests.get(url+':'+port+"/ping")
    except ConnectionRefusedError:
        os.system('clear')
        print('Connection refused! Please contact the administrator')
        time.sleep(3)
        raise ConnectionRefusedError

def to_list_files():
    try:
        test_connection(constants.HERMES_URL, constants.HERMES_PORT)
        r = requests.get(constants.HERMES_URL+':'+constants.HERMES_PORT+'/')
        print(str(r.json()))
    except:
        return

def to_upload(args):
    if args:
        for f_name in args:
            f_name = f_name.replace("'", "")
            try:
                print_progress_bar(0, 4, prefix = 'Progress:', suffix = 'Zipping...')
                os.system(f'gzip -k "{f_name}"')
                
                print_progress_bar(1, 4, prefix = 'Progress:', suffix = 'Partitioning...')
                os.system(f'split -n 3 "{f_name}.gz"')
                
                print_progress_bar(2, 4, prefix = 'Progress:', suffix = 'Storing...')
                # TODO: Code to send xaa, xab, xac
                
                print_progress_bar(3, 4, prefix = 'Progress:', suffix = 'Cleaning...')
                os.system(f'rm *.gz xaa xab xac')

                print_progress_bar(4, 4, prefix = 'Progress:', suffix = 'Complete!')
                print()
            except FileNotFoundError:
                print(f'upload: {f_name}: No such file or directory')
    else:
        print('Usage: upload [path/to/file>...]')

def print_progress_bar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 50, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    clean = ' ' * 70
    print(f'\rclean', end = printEnd)
    print(f'\r{prefix} [{bar}] {percent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

if __name__ == '__main__':
    main()
