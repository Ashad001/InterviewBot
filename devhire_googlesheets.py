import gspread #for sheets
import re #for string verification such as email and name formats

gc = gspread.service_account(filename='sheetAuth.json') #giving sheet access
wks = gc.open("devhire_Database").sheet1

def validate_email(email):
    pattern = r'^\w+([.-]?\w+)*@\w+([.-]?\w+)*(\.\w{2,3})+$'
    return re.match(pattern, email)

def validate_name(name):
    pattern = r'^[a-zA-Z]+$'
    return re.match(pattern, name)

print("\nWelcome To User Data Entry")

# Prompt for new user or exit
while True:
    choice = input("\nEnter '!' to exit or any other key to enter a new user: ")
    if choice == "!":
        break
    
    while True:
        first_name = input("Enter your first name: ")
        last_name = input("Enter your last name: ")
        email = input("Enter your email: ")
    
        if not (first_name.isalpha() and last_name.isalpha()):
            print("Invalid name format. Please try again.")
            continue
    
        if not validate_email(email):
            print("Invalid email format. Please try again.")
            continue
    
        existing_emails = wks.col_values(3) #to check for a returning user and keeping new users unique
        #ashad this is the method you can use for retrieving data as 3rd coloumn is hardcoded for emails
        if email in existing_emails:
            print("Email already exists in the sheet. Please try again with a different email.")
            continue
    
        break
    
    row = [first_name, last_name, email] #will insert in this order 
    wks.insert_row(row, index=2) #is hardcoded to insert at 2nd row always pushing others one row down
    #first row has titles
    print("User added successfully!")
