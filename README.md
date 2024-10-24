# bank-statement-compiler
Takes bank statement csv files as inputs and compiles them into a single csv for analysis.

##Setup Instructions

1. Clone repo on environment with python installed
2. Populate config/accounts.csv with information about the different bank accounts in format "account Unique ID, Account Name, Account statement format, Account default Factor" where:
    Account Unique ID - a unique string that shows up in every line of releant data rows of an input statement. I use the last 4 digits of the account.
    Account Name - A name to be printed on the output e.g. "Savings Account"
    Account Statement Format - A string of capital letters indicating the order of columns in the input statement:
        N - Ignore/Not relevant
        U - Unique ID (Required if not present in file name)
        D - Date (Required)
        I - Item Notes/Description (Required)
        A - Amount (Required)
    Account default factor - -1 or 1 depending on how values/amounts are reported in your input statement.
3. Populate config/output_format.txt with your desired order of columns *(All required)*:
    U - Unique ID
    D - Date
    I - Item Notes/Description
    C - Category
    S - Subcategory
    A - Amount
    T - Account
    F - Filter flag
4. Populate config/categories.csv with any automatic categorization rules in format "search string, category, subcategory, filter". See sample data in file where:
    Search string is the string that should appear in any input row's item notes/description
    Category, subcategory, filter are self-explanatory
    NOTE a category of "DELETE" will indicate that the program will ignore rows. I use this to ignore things like internal transfers and plan charges with rebates.
5. Populate copy_input_files_from.txt with the directory you plan to have your input files to be copied to the input/ directory. Useful if you're on WSL and don't want to manually move files. See sample data in file.
6. Populate copy_output_to.txt with the directory you want your output file to be copied from the output/ directory. Useful if you're on WSL and don't want to manually move files. See sample data in file.

##Running Instructions
1. Copy your bank statement csv files to the input/ directory, or the directory from step 5 above if applicable
2. From the project root directory, run "python3 main.py MM YYYY" in your terminal, where:
    MM is the month you're analyzing (01 for Jan, 02 for Feb, etc.)
    YYYY is the year you're analyzing
3. Watch for confirmation message "Output ready at DIRECTORY"
4. Retrieve your output csv from the DIRECTORY mentioned

##Troubleshooting

###Index out of range error
1. Make sure that your input csv files are comma-delimited, not tab or anything else
2. Make sure that your config/accounts.csv file input formats have all of the required characters listed above
3. Make sure that your config/output_format.txt file has all of the required characters listed above

###Output columns in wrong order
Make sure that your config/output_format.txt file has all of the required characters listed above in your desired order.

###Output column data not where expected
Make sure that your config/accounts.csv file input formats have all of the required characters listed above in the correct order for your input file.
