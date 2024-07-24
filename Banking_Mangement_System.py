'''
Created on Feb 2, 2022

@author: aamena1

'''
#IMPORTING REQUIRED MODULES
import mysql.connector as sql
from datetime import date,timedelta
import random 

import csv 


#DECOR FUNCTION 
def decor(X):
    print()
    print('X')
    print()
    

     
    
#CONNECTING TO MYSQL    
mydb=sql.connect(host="hostname",user="username",database="database_name")
mycursor=mydb.cursor(buffered=True)



Login = "Fail"  
OG_CODE = "None"
Tenure = None

#WELCOME MESSAGE
decor("---✧DIAMOND BANK WELCOMES YOU✧---")

while True:
    
    print('1:Add a new account\
\n2:Login to a existing account \n3:Exit')
    print()
    x = int(input())
    
    #ADDING A NEW ACCOUNT
    if x == 1:
        decor("---✧---")
        #INPUT USER INFORMATION
        First_Name = input("Enter First Name: ")
        Last_Name = input("Enter Last Name: ")
        Phone_No = input("Enter mobile number: ")
        
        First_Name = First_Name.strip()
        Last_Name = Last_Name.strip()
        Phone_No = Phone_No.strip()
        
        if (First_Name.isalpha()!= True) or (Last_Name.isalpha()!= True) or (Phone_No.isnumeric()!= True) or (int(len(Phone_No)) != 10):
            print(int(len(Phone_No)))
            decor('---✧Error✧---')
            continue
        
        
        print("FOR INDENTIFICATION \n1:Passport.No \n2:Aadhaar No")
        print()
        method = int(input())
        print()
        if method == 1:
            indentification = input("Enter passport.no: ")
            Identification = 'PNo: '+ indentification
            
        elif method == 2:
            indentification = input("Enter Aadhaar No: ")
            Identification = 'ANo: '+ indentification
        else:
            print('---✧Error✧---')
            continue
        
        
        
        Current_Amount = float(input("Enter deposit amount: "))
        while Current_Amount<1000:
            #SETTING A MINIMUM DEPOSIT AMOUNT
            decor("---You cannot enter a amount less than Rs1000---")
            
            Current_Amount = float(input("Enter deposit amount: "))
        
        decor("---✧---")
        #TYPES OF ACCOUNTS OFFERED
        print("Currently Our Bank Offers Two Types of Accounts:\nSA:Savings Account \nFD:Fixed Deposit Account")
        Type = input("Enter the type of account you wish to have: ")  
        
        Status = "OPEN"
        x = str(random.randint(1000000000,9999999999))
        code = Type+First_Name[0]+Last_Name[1]+x 
       
        if Type == 'FD':
            
            
            SA_Code = input("Enter your Savings Account Number:")
            st = ("Select * from Accounts where CODE = '{}' AND STATUS = 'OPEN'").format(SA_Code)
            mycursor.execute(st)
            data = mycursor.fetchall()
            count = mycursor.rowcount
            #CHECKING FOR A SAVINGS ACCOUNT
            if count == 0:
                
                print("You must have a Open Savings Account before opening a Fixed Deposit Account")
                decor("---✧---")
                continue
            else:
                
                #INFO NEEDED TO CREATE A FD ACCOUNT            
                Tenure = float(input("Enter investment tenure in months: "))
                print("Available rate range 0.5%-5%")
                interest_rate = float(input("Enter Interest rate: "))
                while 0.5<=interest_rate>=5 :
                    print("Available rate range 0.5%-5%")
                    interest_rate = float(input("Enter Interest rate: "))
                current_date = date.today()
                maturity_date = current_date + timedelta(Tenure*30)
                #STORING USERS INFORMATION INTO A TABLE
                st = "INSERT INTO Accounts(CODE,FIRSTNAME,LASTNAME,PHONENO,IDENTIFICATION,CURRENTAMT,TYPE,TENURE,INTEREST_RATE,ACCOUNT_CREATED_ON,MATURITY_DATE,STATUS) VALUES('{}','{}','{}','{}','{}',{},'{}',{},{},'{}','{}','{}')".format(code,First_Name,Last_Name,Phone_No,Identification,Current_Amount,Type,Tenure,interest_rate,current_date,maturity_date,Status) 
                mycursor.execute(st)
                mydb.commit()
            
        elif Type == 'SA':
            #STORING USERS INFORMATION INTO A TABLE
            current_date = date.today()
            st = "INSERT INTO Accounts(CODE,FIRSTNAME,LASTNAME,PHONENO,IDENTIFICATION,CURRENTAMT,TYPE,ACCOUNT_CREATED_ON,STATUS) VALUES('{}','{}','{}','{}','{}',{},'{}','{}','{}')".format(code,First_Name,Last_Name,Phone_No,Identification,Current_Amount,Type,current_date,Status) 
            mycursor.execute(st)
            mydb.commit()
        else:
            decor('---✧Error✧---')
            continue
        
                          
        New_Password = input("Enter New Password: ")
        
        decor("---✧---")
        print(f"---Your Account Number is {code}---")
        
        
        #STORING USERS INFORMATION INTO A TABLE
        new_st = ("INSERT INTO AccountsandPassword(Code,PASSWORD,STATUS) VALUES('{}','{}','{}')").format(code,New_Password,Status) 
        mycursor.execute(new_st)
        mydb.commit()
        print("---✧New Account has been created✧---")
        decor("---✧---")    
        #STORING ACCOUNT NUMBER
        OG_CODE = code
          
        
    #LOGGING INTO A ACCOUNT
    elif x ==2:
        decor("---✧---")
        #3 TRIES TO FILL IN LOGIN INFORMATION 
        Try = 3
        while Try>0:
            print("No.of tries left: ",Try)
            Code = input("Enter Account Number: ")
            Password = input("Enter Password: ")
            
            #CHECKING IF ACCOUNT NUMBER AND PASSWORD MATCH
            st = ("Select * from AccountsandPassword where Code = '{}' AND PASSWORD = '{}' AND STATUS = 'OPEN'").format(Code,Password)
            mycursor.execute(st)
            data = mycursor.fetchall()
            count = mycursor.rowcount
            if count == 0:
                print()
                print("Invalid AccountCode/Password or This Account has been Closed")
                Try -=1
            else:
                break    
    
        if Try>=1:
            Login = "Successful" 
            
            #STORING ACCOUNT NUMBER
            OG_CODE = Code
            decor("---✧Login Successful✧---")
            mycursor.reset()
    
        else:
            decor("---Login Fail---")
        #AFTER LOGIN IS SUCCESSFUL
        
        while Login == "Successful":
            
            
            print('1:Checking your Balance \n2:Deposit money into account\
\n3:Withdraw money from an account \n4:Transfer money from account \n5:Log Out \n6:Close Account')
            y = int(input())
            
            
            if y == 1:
                decor("---✧---") 
                new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                mycursor.execute(new_st)
                data = mycursor.fetchall()
                
                print(f"---✧BALANCE IS ₹{data[0][0]}✧---")
                decor("---✧---")
            
            #DEPOSITING MONEY
            elif y == 2:
                decor("---✧---")
                amount = float(input("Enter the amount you wish to deposit: "))
                st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT + {} WHERE CODE = '{}'").format(amount,OG_CODE)
                
                mycursor.execute(st)
                mydb.commit()
                new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                mycursor.execute(new_st)
                data = mycursor.fetchall()
                
                decor("---✧---")
            
                print(f"---✧CURRENT BALANCE UPDATED✧---\n\n₹{amount} DEPOSITED \nNEW BALANCE IS ₹{data[0][0]}")
                decor("---✧---")
                mydb.commit()
            
            #WITHDRAWING MONEY    
            elif y == 3:
                decor("---✧---")
                
                #STORING INITIAL BALANCE
                new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                mycursor.execute(new_st)
                temp = mycursor.fetchall()
                
                #CHECKING IF ACCOUNT IS A SAVINGS ACCOUNT OR A FD ACCOUNT
                if OG_CODE[0:2] == 'SA':
                    amount = float(input("Enter the amount you wish to withdraw: "))
                    st = ("UPDATE Accounts SET CURRENTAMT = IF (CURRENTAMT-{}>500,CURRENTAMT - {},CURRENTAMT) WHERE CODE = '{}'").format(amount,amount,OG_CODE)
                    mycursor.execute(st)
                    mydb.commit()
                    new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                    mycursor.execute(new_st)
                    data = mycursor.fetchall()
                
                    #WITHRDRAWAL IS ALLOWED ONLY IF LEFTOVER BALANCE IS OVER Rs500 
                    if temp == data:
                        print("AMOUNT CANNOT BE WITHDRAWN AS BALANCE FALLS BELOW ₹500")
                    else:    
                        print(f"---✧CURRENT BALANCE UPDATED✧---\n\n₹{amount} WITHDRAWN \nNEW BALANCE IS ₹{data[0][0]}")
                
                    decor("---✧---")
                
                elif OG_CODE[0:2] == 'FD':
                    new_st = ("SELECT MATURITY_DATE FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                    mycursor.execute(new_st)
                    temp = mycursor.fetchall()
                    store = temp[0][0]
                    st = ("SELECT ACCOUNT_CREATED_ON FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                    mycursor.execute(st)
                    xtemp = mycursor.fetchall()
                    store_st = xtemp[0][0]
                    i = ("SELECT INTEREST_RATE FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                    mycursor.execute(i)
                    itemp = mycursor.fetchall()
                    interest_st = itemp[0][0]
                    
                    #INCASE OF FD ACCOUNT MATURED
                    if store == date.today():
                        
                        mycursor.execute("SELECT TENURE FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                        K = mycursor.fetchall()
                        T = float(K[0][0])
                        mycursor.execute("UPDATE Accounts SET CURRENTAMT = CURRENTAMT + (CURRENTAMT*{}*{})/(100*12) WHERE CODE = '{}'").format(T,interest_st,OG_CODE)
                        print("---✧YOUR FD HAS MATURED✧---")
                        new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                        mycursor.execute(new_st)
                        data = mycursor.fetchall()
                
                        decor("---✧---")
                        print(f"---✧FD BALANCE IS ₹{data[0][0]}✧---")
                        ans = input("Type OK to transfer your money into your savings account: ")
                        if ans == 'OK':
                            sa = input("Enter Savings Account Number: ")
                            st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT + {} WHERE CODE = '{}'").format(data[0][0],sa)
                            mycursor.execute(st)
                            mydb.commit()
                            st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT - CURRENTAMT WHERE CODE = '{}'").format(OG_CODE)
                            mycursor.execute(st)
                            mydb.commit()
                            print(f"---✧AMOUNT TRANSFERRED IS ₹{data[0][0]}✧---")
                            decor("---✧---")
                            mydb.commit()
                            Status = "MATURED-CLOSED"
                            st = ("UPDATE FROM Accounts SET STATUS = '{}' WHERE CODE ='{}'").format(Status,OG_CODE)
                            ST = ("UPDATE FROM AccountsandPassword SET STATUS = '{}' WHERE CODE ='{}'").format(Status,OG_CODE)
                            mycursor.execute(st)
                            mydb.commit()
                        
                    #INCASE OF ACCOUNT NOT YET MATURED
                    else:
                        #CONFORMATION STATEMENT
                        print("YOUR FD IS NOT YET MATURED,DO U STILL WISH TO WITHDRAW THE MONEY?")
                        new = input("Yes/No: ")
                        if new == "Yes":
                            a = ("SELECT DATEDIFF('{}','{}')".format(date.today(),store_st))
                            mycursor.execute(a)
                            b = mycursor.fetchall()
                            c = b[0][0]
                            mycursor.execute("UPDATE Accounts SET CURRENTAMT = CURRENTAMT + (CURRENTAMT*{}*{})/(100*12) WHERE CODE = '{}'".format(c,interest_st-0.5,OG_CODE))
                            new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                            mycursor.execute(new_st)
                            data = mycursor.fetchall()
                
                            decor("---✧---")
                            print(f"---✧FD BALANCE IS ₹{data[0][0]}✧---")
                            ans = input("Type OK to transfer your money into your savings account: ")
                            if ans == 'OK':
                                #TRANSFERING THE MONEY TO SA ACCOUNT
                                sa = input("Enter Savings Account Number: ")
                                st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT + {} WHERE CODE = '{}'").format(data[0][0],sa)
                                mycursor.execute(st)
                                mydb.commit()
                                st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT - CURRENTAMT WHERE CODE = '{}'").format(OG_CODE)
                                mycursor.execute(st)
                                mydb.commit()
                                print(f"---✧AMOUNT TRANSFERRED IS ₹{data[0][0]}✧---")
                                decor("---✧---")
                                mydb.commit()
                                
                                Status = "IMMATURE-CLOSED"
                                st = ("UPDATE Accounts SET STATUS = '{}' WHERE CODE ='{}'").format(Status,OG_CODE)
                                ST = ("UPDATE AccountsandPassword SET STATUS = '{}' WHERE Code ='{}'").format(Status,OG_CODE)
                                mycursor.execute(st)
                                mydb.commit()
                                mycursor.execute(ST)
                                mydb.commit()
                                continue
                            
                            else:
                                decor("---✧---")
                                continue    
                         
            
            #TRANSFERING MONEY BETWEEN ACCOUNTS    
            elif y == 4:
                if OG_CODE[0:2] == 'FD':
                    print("You cannot transfer directly from a FD Account")
                    break
                decor("---✧---")
                other_code = input("Enter the Payee's account number: ")
                Status = 'OPEN'
                #CHECKING IF ACCOUNT EXISTS
                check_st = ("SELECT * FROM Accounts WHERE CODE = '{}' AND STATUS = '{}'").format(other_code,Status)
                mycursor.execute(check_st)
                data = mycursor.fetchall()
                if count == 0:
                    print("Account does not exist or Has been closed")
                    break
                
                      
                
                amount = float(input("Enter amount to be transfered: "))  
                
                #STORING INITIAL BALANCE  
                new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                mycursor.execute(new_st)
                temp = mycursor.fetchall()
                   
                st = ("UPDATE Accounts SET CURRENTAMT = IF (CURRENTAMT-{}>500,CURRENTAMT - {},CURRENTAMT) WHERE CODE = '{}'").format(amount,amount,OG_CODE)
                mycursor.execute(st)
                mydb.commit()
                new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                mycursor.execute(new_st)
                data = mycursor.fetchall()
                
                #TRANSFER WILL TAKE PLACE ONLY IF LEFTOVER BALANCE IS ABOVE Rs500
                if temp == data:
                    print("AMOUNT CANNOT BE TRANSFERRED AS BALANCE FALLS BELOW ₹500")
                else:
                    st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT + {} WHERE CODE ='{}'").format(amount,other_code)
                    mycursor.execute(st)
                    mydb.commit()    
                    print(f"---✧CURRENT BALANCE UPDATED✧---\n\n₹{amount} TRANSFERRED TO ACCOUNT NUMBER: {other_code} \nNEW BALANCE IS ₹{data[0][0]}")
                
                decor("---✧---")
                
                mydb.commit()
            
            #LOGGING OUT OF AN ACCOUNT    
            elif y == 5:
                print("---✧YOU HAVE LOGGED OUT✧---")
                print()
                Login = "False"
            
            #CLOSING A ACCOUNT          
            elif y == 6 :
                decor("---✧---")
                #CONFORMATION
                #RETURNING ANY REMAINING BALANCE
                cash_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                mycursor.execute(cash_st)
                
                
                ask=input("Are you sure you wish to close your account? yes/no: ") 
                if ask == 'yes':
                    decor("---✧---")
                    #EXTRA SECURITY STEP
                    password = input("Please re-enter your password: ")
                    nst = ("Select * from AccountsandPassword where Code = '{}' AND PASSWORD = '{}' AND STATUS = 'OPEN'").format(OG_CODE,password)
                    mycursor.execute(nst)
                    data = mycursor.fetchall()
                    count = mycursor.rowcount
                    
                    #LOG OUT IF PASSWORD IS INVALID
                    if count == 0:
                        print("---Invalid Password---")
                        print("---YOU WILL BE LOGGED OUT---")
                        print()
                        Login = "False"
                    
                    #CLOSING AN ACCOUNT    
                    else:
                        new_st = ("SELECT CURRENTAMT FROM Accounts WHERE CODE = '{}'").format(OG_CODE)
                        mycursor.execute(new_st)
                        data = mycursor.fetchall()
                        st = ("UPDATE Accounts SET CURRENTAMT = CURRENTAMT - CURRENTAMT WHERE CODE = '{}'").format(OG_CODE)
                        mycursor.execute(st)
                        mydb.commit()
                        
                        print(f"---✧AMOUNT RETURNED IS ₹{data[0][0]}✧---")
                        decor("---✧---")
                        cash_st = ()
                        Status = "CLOSED"
                        st = ("UPDATE Accounts SET STATUS = '{}' WHERE CODE = '{}'").format(Status,OG_CODE)
                        new_st = ("UPDATE AccountsandPassword SET STATUS = '{}' WHERE Code = '{}'").format(Status,OG_CODE)
                        mycursor.execute(new_st)
                        mydb.commit()
                        mycursor.execute(st)
                        
                        mydb.commit()
                        print("---✧YOUR ACCOUNT IS SUCCESFULLY CLOSED✧---")
                        print()
                        Login = "False"
                
                else:
                    print("---✧CLOSING OF ACCOUNT UNSUCCESSFUL✧---")
                    print()
    
    
    
    
    else:
        #DATA BACKUP
        decor("---✧---")
        st = ("SELECT * FROM Accounts")
        mycursor.execute(st)
        data = mycursor.fetchall()
        other = ("SELECT * FROM AccountsandPassword")
        mycursor.execute(other)
        otherdata = mycursor.fetchall()
        with open("BANKING MANAGEMENT SYSTEM.csv",'w',newline = '') as backupfiles:
            writer = csv.writer(backupfiles,delimiter = '|')
            writer.writerow("Accounts")
            writer.writerows(data)
            writer.writerow(" ")  
            writer.writerow("AccountsandPassword")
            writer.writerows(otherdata)  
        
        #FAREWELL MESSAGE    
        exit("---✧THANK YOU FOR USING DIAMOND BANK✧--- \n---✧Exiting✧---")  

     

mydb.close()

















