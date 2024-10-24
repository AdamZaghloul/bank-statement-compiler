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
    account_default_factors = []

    categories = []

    output_format = []
    output_columns = []

    print(f"Preparing output for {datetime.date(year, month, 1).strftime('%B')} {year}")

    copy_input_files()

    output_format = get_output_format()
    if len(output_format) == 0:
        return
    
    account_IDs, account_names, account_orders, account_default_factors = get_accounts()
    if len(account_IDs) == 0:
        return

    categories = get_categories()

    output_columns = process_input_files(output_columns, output_format, account_IDs, account_names, account_orders, month, year, categories, account_default_factors)

    print_output_file(output_format, output_columns)

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
    account_default_factors = []

    with open('config/accounts.csv', newline='\n') as csvfile:
        accounts = csv.reader(csvfile, delimiter=',', quotechar='|')
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
            account_default_factors.append(int(row[3]))
            if account_default_factors[-1] == 0:
                account_default_factors[-1] = 1
    
    if len(account_IDs) != len(account_names) or len(account_names) != len(account_orders) or len(account_IDs) == 0 or len(account_names) == 0 or len(account_orders) == 0:
        print("ERROR: No accounts found in accounts.csv config file.")
        return 0,0,0
    
    return account_IDs, account_names, account_orders, account_default_factors

def get_categories():
    categories = []

    with open('config/categories.csv', newline='\n') as csvfile:
        cats = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in cats:
            inner_cat = []
            inner_cat.append(row[0])
            inner_cat.append(row[1])
            inner_cat.append(row[2])
            inner_cat.append(row[3])
            categories.append(inner_cat)
    
    return categories

def process_input_files(output_columns, output_format, account_IDs, account_names, account_orders, month, year, categories, account_default_factors):
    for filename in os.listdir("input"):
            file_path = os.path.join("input/", filename)
            try:
                if os.path.isfile(file_path) and filename[-4:] == ".csv":
                    output_columns = process_single_input_file(file_path, output_columns, output_format, account_IDs, account_names, account_orders, month, year, categories, account_default_factors)
                else:
                    print(f"WARNING: Skipped non-CSV file or directory {file_path}")
            except Exception as e:
                print('WARNING: Failed to process %s. Reason: %s' % (file_path, e))
    
    return output_columns
        
def process_single_input_file(file_path, output_columns, output_format, account_IDs, account_names, account_orders, month, year, categories, account_default_factors):
    account = None
    account_dict = {}
    
    with open(file_path, newline='\n') as csvfile:
        rows = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in rows:
            if account is None:
                for col in row:
                    for i in range(0, len(account_IDs)):
                        if account_IDs[i] in col:
                            account = i
                            for k in range(0,len(account_orders[account])):
                                account_dict[account_orders[account][k]] = k
            
            if account is not None:
                new_row = {}

                #check if date and unique ID are valid using account_dict indices
                if account_IDs[account] in row[account_dict["U"]] and int(row[account_dict["D"]][4:6]) == month and int(row[account_dict["D"]][0:4]) == year:
                    #set new_row based on account_dict indices
                    for i in range(0, len(output_format)-1):
                        if output_format[i] in account_dict:
                            if output_format[i] == "D":
                                new_row[output_format[i]] = datetime.date(int(row[account_dict[output_format[i]]][0:4]), int(row[account_dict[output_format[i]]][4:6]), int(row[account_dict[output_format[i]]][6:])).isoformat()
                            elif output_format[i] == "A":
                                new_row[output_format[i]] = float(row[account_dict[output_format[i]]]) * account_default_factors[account]
                            else:
                                new_row[output_format[i]] = row[account_dict[output_format[i]]]
                    new_row["C"], new_row["S"], new_row["F"] = find_row_category(new_row["I"], categories)
                    new_row["T"] = account_names[account]
                    
                    if new_row["C"] != "DELETE":
                        output_columns.append(new_row)
    if account is None:
        print(f"WARNING: Could not identify account in file: {file_path}. File not processed.")
    
    return output_columns

def find_row_category(description, categories):
    if description == "":
        return "", "", ""

    for i in range(0, len(categories)-1):
        if categories[i][0] in description:
            return categories[i][1], categories[i][2], categories[i][3]
    
    return "", "", ""

def print_output_file(output_format, output_columns):
    output_list = []

    file = open("config/copy_output_to.txt", "r")
    directory = file.readline()
    file.close()

    for row in output_columns:

        temp_row = []

        for col in output_format:
            temp_row.append(row[col])
        
        output_list.append(temp_row)

    if os.path.isfile("output/output.csv") or os.path.islink("output/output.csv"):
        os.unlink("output/output.csv")
    with open('output/output.csv', 'w', newline='') as csvfile:
        output_file = csv.writer(csvfile, delimiter=',',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
        
        for row in output_list:
            output_file.writerow(row)


    if directory != "":
        
        if os.path.isfile(f"{directory}/output.csv") or os.path.islink(f"{directory}/output.csv"):
            os.unlink(f"{directory}/output.csv")

        shutil.copyfile("output/output.csv", f"{directory}/output.csv")

        print(f"Output ready at {directory}/output.csv")
    else:
        print("Output ready at output/output.csv")

main()