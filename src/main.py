import sys

def main():
    args = sys.argv[1:]

    if len(args) > 0:
        if args[0] == "config":
            #run config options (add account, edit account, delete account)
            pass
        else:
            print("Invalid argument.")
    else:
        #load up input CSVs into accounts. If there are any new accounts, prompt for format.
        pass
main()