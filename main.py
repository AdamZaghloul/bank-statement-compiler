import sys
import csv
import shutil
import datetime
import os

def main():
    month, year = process_args(sys.argv[1:])

    if month == 0:
        return

    account_IDs = []
    account_names = []
    account_orders = []

    output_format = []
    output_columns = []

    print(f"Preparing output for {datetime.date(year, month, 1).strftime('%B')}, {year}")

    copy_input_files()

    output_format = get_output_format()
    if len(output_format) == 0:
        return
    
    account_IDs, account_names, account_orders = get_accounts()
    if len(account_IDs) == 0:
        return

def process_args(args):
    
    month = 0
    year = 0

    if len(args) > 0 and len(args) <= 2:
        if args[0] == "config":
            #run config options (add account, edit account, delete account)
            pass
        elif args[0].isnumeric() and args[1].isnumeric():
            if int(args[0]) > 0 and int(args[0]) <= 12:
                month = int(args[0])
            else:
                print("Invalid month.")
            year = int(args[1])
        else:
            print("Invalid arguments. Should be './main.sh MM YYYY' with month and year numeric.")
    else:
        print("Invalid arguments. Should be './main.sh MM YYYY' with month and year numeric.")
    
    return month, year

def copy_input_files():
    file = open("config/copy_input_files_from.txt", "r")
    directory = file.readline()
    if directory != "":
        for filename in os.listdir("input"):
            file_path = os.path.join("input/", filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

        #shutil.copytree(directory, 'input')
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    shutil.copyfile(file_path, f"input/{filename}")
            except Exception as e:
                print('Failed to copy %s. Reason: %s' % (file_path, e))
    file.close()

def get_output_format():
    output_format = []
    
    file = open("config/output_format.txt", "r")
    format_string = file.readline()
    for char in format_string:
        output_format.append(char)

    file.close()

    if len(output_format) == 0:
        print("ERROR: No output format found in output_format.txt config file.")

    return output_format

def get_accounts():
    account_IDs = []
    account_names = []
    account_orders = []

    with open('config/accounts.csv', newline='') as csvfile:
        accounts = csv.reader(csvfile, delimiter=' ', quotechar='|')
        if len(accounts) != 0:
            for row in accounts:
                account_IDs.append(row[0])
                account_names.append(row[1])
                temp_list = []
                chars_so_far = ""
                for char in row[2]:
                    if(char in chars_so_far and char.upper() != "N"):
                        print(f"ERROR: Invalid input format for {account_names.pop()} account in accounts.csv config file. All flags are allowed once and only once except for 'N'")
                        return 0,0,0

                    chars_so_far = chars_so_far + char
                    temp_list.append(char)
                
                account_orders.append(temp_list)
    
    if len(account_IDs) != len(account_names) or len(account_names) != len(account_orders) or len(account_IDs) == 0 or len(account_names) == 0 or len(account_orders) == 0:
        print("ERROR: No accounts found in accounts.csv config file.")
        return 0,0,0
    
    return account_IDs, account_names, account_orders

main()