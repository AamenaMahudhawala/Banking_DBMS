# IMPORTING REQUIRED MODULES
import mysql.connector as sql
from datetime import date, timedelta
import random
import csv

# DECOR FUNCTION
def decor(msg):
    print(f"\n---✧ {msg} ✧---\n")

# CONNECTING TO MYSQL    
mydb = sql.connect(host="hostname", user="username", database="databasename")
mycursor = mydb.cursor(buffered=True)

Login, OG_CODE = "Fail", "None"

# WELCOME MESSAGE
decor("DIAMOND BANK WELCOMES YOU")

def valid_phone(phone):
    return phone.isnumeric() and len(phone) == 10

#INPUT USER INFORMATION
def input_account_info():
    first_name = input("Enter First Name: ").strip()
    last_name = input("Enter Last Name: ").strip()
    phone = input("Enter mobile number: ").strip()

    if not (first_name.isalpha() and last_name.isalpha() and valid_phone(phone)):
        decor("Error: Invalid input")
        return None

    return first_name,last_name,phone

#ADDING A NEW ACCOUNT
def create_account():
    decor("--- Create New Account ---")
    info = input_account_info()
    if not info:
        return

    first_name, last_name, phone = info
    ident_type = input("1:Passport No \n2:Aadhaar No\nChoose identification type: ")
    ident_no = input("Enter identification number: ")
    identification = f"{'PNo' if ident_type == '1' else 'ANo'}: {ident_no}"

    current_amt = float(input("Enter deposit amount: "))
    while current_amt < 1000:
        decor("Amount cannot be less than Rs 1000")
        current_amt = float(input("Enter deposit amount: "))

    account_type = input("Enter account type (SA: Savings Account / FD: Fixed Deposit): ")
    code = f"{account_type}{first_name[0]}{last_name[1]}{random.randint(1000000000, 9999999999)}"

    if account_type == "FD":
        SA_code = input("Enter your Savings Account Number: ")
        mycursor.execute(f"SELECT * FROM Accounts WHERE CODE = '{SA_code}' AND STATUS = 'OPEN'")
        if mycursor.rowcount == 0:
            decor("You must have an Open Savings Account before opening a Fixed Deposit Account")
            return

        tenure = float(input("Enter investment tenure in months: "))
        interest_rate = float(input("Enter interest rate (0.5%-5%): "))
        maturity_date = date.today() + timedelta(days=tenure*30)

        query = (f"INSERT INTO Accounts (CODE, FIRSTNAME, LASTNAME, PHONENO, IDENTIFICATION, CURRENTAMT, TYPE, TENURE, INTEREST_RATE, "
                 f"ACCOUNT_CREATED_ON, MATURITY_DATE, STATUS) "
                 f"VALUES ('{code}', '{first_name}', '{last_name}', '{phone}', '{identification}', {current_amt}, '{account_type}', "
                 f"{tenure}, {interest_rate}, '{date.today()}', '{maturity_date}', 'OPEN')")
    else:
        query = (f"INSERT INTO Accounts (CODE, FIRSTNAME, LASTNAME, PHONENO, IDENTIFICATION, CURRENTAMT, TYPE, ACCOUNT_CREATED_ON, STATUS) "
                 f"VALUES ('{code}', '{first_name}', '{last_name}', '{phone}', '{identification}', {current_amt}, '{account_type}', '{date.today()}', 'OPEN')")

    mycursor.execute(query)
    mydb.commit()

    new_password = input("Enter New Password: ")
    mycursor.execute(f"INSERT INTO AccountsandPassword (Code, PASSWORD, STATUS) VALUES ('{code}', '{new_password}', 'OPEN')")
    mydb.commit()

    decor(f"Your Account Number is {code}")
    decor("New Account has been created")
#LOGGING IN
def login():
    decor("Login")
    for _ in range(3):
        code = input("Enter Account Number: ")
        password = input("Enter Password: ")
        mycursor.execute(f"SELECT * FROM AccountsandPassword WHERE Code = '{code}' AND PASSWORD = '{password}' AND STATUS = 'OPEN'")
        if mycursor.rowcount > 0:
            decor("Login Successful")
            return code
        else:
            print("Invalid AccountCode/Password")
    return None

#CHECKING BALANCE
def check_balance(code):
    mycursor.execute(f"SELECT CURRENTAMT FROM Accounts WHERE CODE = '{code}'")
    balance = mycursor.fetchone()[0]
    decor(f"Balance is ₹{balance}")

#DEPOSITING MONEY
def deposit_money(code):
    amount = float(input("Enter the amount to deposit: "))
    mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = CURRENTAMT + {amount} WHERE CODE = '{code}'")
    mydb.commit()
    check_balance(code)

#WITHDRAWING MONEY    
def withdraw_money(code):
    mycursor.execute(f"SELECT * FROM Accounts WHERE CODE = '{code}'")
    account_details = mycursor.fetchone()

    current_amt, account_type, maturity_date, interest_rate, tenure = account_details[5], account_details[6], account_details[10], account_details[8], account_details[7]

    amount = float(input("Enter the amount to withdraw: "))

    if account_type == 'SA':
        # Withdraw money from a savings account, but balance must not go below Rs 500
        mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = IF(CURRENTAMT - {amount} > 500, CURRENTAMT - {amount}, CURRENTAMT) WHERE CODE = '{code}'")
        mydb.commit()
        check_balance(code)
    elif account_type == 'FD':
        # Withdraw money from a Fixed Deposit account with interest calculation if matured
        current_date = date.today()
        if current_date >= maturity_date:
            #FD has matured, calculate the interest and allow withdrawal
            total_months = tenure
            interest_amt = current_amt * (interest_rate / 100) * (total_months / 12)
            final_amt = current_amt + interest_amt
            decor(f"FD Maturity Date reached. Withdrawing ₹{final_amt} including interest ₹{interest_amt}")
            mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = 0, STATUS = 'CLOSED' WHERE CODE = '{code}'")
        else:
            # FD not matured, allow withdrawal only if customer accepts the penalty
            print("FD not matured yet. A penalty will apply for early withdrawal.")
            penalty_amt = current_amt * 0.01  # Assume 1% penalty
            proceed = input(f"Early withdrawal penalty is ₹{penalty_amt}. Do you wish to proceed? (yes/no): ").lower()
            if proceed == "yes":
                final_amt = current_amt - penalty_amt
                decor(f"Withdrawing ₹{final_amt} after ₹{penalty_amt} penalty")
                mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = 0, STATUS = 'CLOSED' WHERE CODE = '{code}'")
        mydb.commit()
        check_balance(code)
#TRANSFERING MONEY BETWEEN ACCOUNTS    
def transfer_money(code):
    if code[:2] == 'FD':
        print("You cannot transfer directly from a FD Account")
        return
    recipient = input("Enter the recipient's account number: ")
    amount = float(input("Enter the amount to transfer: "))
    mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = CURRENTAMT - {amount} WHERE CODE = '{code}'")
    mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = CURRENTAMT + {amount} WHERE CODE = '{recipient}'")
    mydb.commit()
    decor(f"₹{amount} transferred to {recipient}")

def close_account(code):
    ask = input("Are you sure you want to close your account? (yes/no): ").lower()
    if ask == 'yes':
        mycursor.execute(f"UPDATE Accounts SET CURRENTAMT = 0, STATUS = 'CLOSED' WHERE CODE = '{code}'")
        mydb.commit()
        decor("Account Closed")

def backup_data():
    with open("BANKING_MANAGEMENT_SYSTEM.csv", 'w', newline='') as backup_file:
        writer = csv.writer(backup_file, delimiter='|')
        writer.writerow(["Accounts"])
        mycursor.execute("SELECT * FROM Accounts")
        writer.writerows(mycursor.fetchall())
        writer.writerow(["AccountsandPassword"])
        mycursor.execute("SELECT * FROM AccountsandPassword")
        writer.writerows(mycursor.fetchall())
    decor("Data backed up successfully")

# MAIN LOOP
while True:
    print("1: Add a new account\n2: Login to an existing account\n3: Exit")
    choice = int(input())

    if choice == 1:
        create_account()
    elif choice == 2:
        user_code = login()
        if user_code:
            while True:
                print("1: Check Balance\n2: Deposit Money\n3: Withdraw Money\n4: Transfer Money\n5: Log Out\n6: Close Account")
                action = int(input())
                if action == 1:
                    check_balance(user_code)
                elif action == 2:
                    deposit_money(user_code)
                elif action == 3:
                    withdraw_money(user_code)
                elif action == 4:
                    transfer_money(user_code)
                elif action == 5:
                    decor("You have logged out")
                    break
                elif action == 6:
                    close_account(user_code)
                    break
    elif choice == 3:
        backup_data()
        decor("Thank you for using Diamond Bank")
        break

mydb.close()
