from consts import VERSION
from interpreter import interpreter

def main():
    print_welcome_message()
    interpreter()
        

def print_usage():
    print("+---------------------------------+")
    print("  help: Print help message.")
    print("  quit: Quit this application.") 
    print("+---------------------------------+")

def print_welcome_message():
    """
    AA from https://patorjk.com/software/taag/
    Font: Rectangles
    """
    print(" _____ _____ ____  _____    _____ __    _____ ")
    print("|_   _|     |    \|     |  |     |  |  |     |")
    print("  | | |  |  |  |  |  |  |  |   --|  |__|-   -|")
    print("  |_| |_____|____/|_____|  |_____|_____|_____|")
    print("  version: {}".format(VERSION))
    print_usage()                              

if __name__ == '__main__':
    main()
