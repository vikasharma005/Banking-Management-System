import mysql.connector
import pandas as pd
import csv
from datetime import date
from prettytable import PrettyTable

def clear():
  for _ in range(5):
     print()

def customer_record():
  conn = mysql.connector.connect(
      host='localhost', database='Banking', user='root', password='root')
  cursor = conn.cursor()
  sql ="select * from customers;"
  print('Customer Records')
  df = pd.read_sql(sql, conn)
  df.to_csv('C:/Users/Admin/Desktop/IP Project/customers.csv', index=False)
  #conn.close()
  df = pd.read_csv('C:/Users/Admin/Desktop/IP Project/customers.csv')
  print(df.to_string())
  cursor.execute(sql)
  
  wait = input('\n\n\n Press any key to continue....')

def account_status(account_no):
  conn = mysql.connector.connect(
      host='localhost', database='Banking', user='root', password='root')
  cursor = conn.cursor()
  sql ="select status,balance from customers where account_no ='"+account_no+"'"
  result = cursor.execute(sql)
  result = cursor.fetchone()
  conn.close()
  return result

def deposit_amount():
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    clear()
    account_no = input('Enter Account No :')
    amount = input('Enter amount :')
    today = date.today()
    result = account_status(account_no)
    if result [0]== 'active':
      sql1 ="update customers set balance = balance+"+amount + ' where account_no = '+account_no+' and status="active";'
      sql2 = 'insert into transactions(amount,type,account_no,date_of_transaction) values(' + amount +',"deposit",'+account_no+',"'+str(today)+'");'
      sql3 = 'COMMIT;'
      cursor.execute(sql2)
      cursor.execute(sql1)
      cursor.execute(sql3)
      print('\n\namount deposited')

    else:
      print('\n\nClosed or Suspended Account....')
    
    wait= input('\n\n\n Press any key to continue....')
    conn.close()


def withdraw_amount():
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    clear()
    account_no = input('Enter Account No :')
    amount = input('Enter amount :')
    today = date.today()
    result = account_status(account_no)
    if result[0] == 'active' and int(result[1])>=int(amount):
      sql1 = "update customers set balance = balance-" + \
          amount + ' where account_no = '+account_no+' and status="active";'
      sql2 = 'insert into transactions(amount,type,account_no,date_of_transaction) values(' + \
          amount + ',"withdraw",'+account_no+',"'+str(today)+'");'

      sql3 = 'COMMIT;'
      cursor.execute(sql2)
      cursor.execute(sql1)
      cursor.execute(sql3)
      #print(sql1)
      #print(sql2)
      print('\n\namount Withdrawn')

    else:
      print('\n\nClosed or Suspended Account.Or Insufficient amount')

    wait = input('\n\n\n Press any key to continue....')
    conn.close()

def transaction_menu():
    while True:
      clear()
      print(' Trasaction Menu')
      print("\n1.  Deposit Amount")
      print('\n2.  WithDraw Amount')
      print('\n3.  Back to Main Menu')
      print('\n\n')
      choice = int(input('Enter your choice ...: '))
      if choice == 1:
        deposit_amount()
      if choice == 2:
        withdraw_amount()
      if choice == 3:
        break

def search_menu():
    conn = mysql.connector.connect(
       host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    while True:
      clear()
      print(' Search Menu')
      print("\n1.  Account No")
      print('\n2.  Aadhar Card')
      print('\n3.  Phone No')
      print('\n4.  Email')
      print('\n5.  Names')
      print('\n6.  Back to Main Menu')
      print('\n\n')
      choice = int(input('Enter your choice ...: '))
      field_name=''
   
      if choice == 1:
        field_name ='account_no'
  
      if choice == 2:
        field_name ='aadhar_no'
   
      if choice == 3:
        field_name = 'phone'
      
      if choice == 4:
        field_name = 'email'

      if choice == 5:
        field_name = 'name'
      
      if choice == 6:
        break
      msg ='Enter '+field_name+': '
      value = input(msg)
      if field_name=='account_no':
        sql = 'select * from customers where '+field_name + ' = '+value+';'
      else:
        sql = 'select * from customers where '+field_name +' like "%'+value+'%";'

      print("\n\n\n")
      print('Search Result for ', field_name, ' ',value)
      print('-'*80)
      df = pd.read_sql(sql, conn)
      print(df.to_string())  
      
      cursor.execute(sql)
      records = cursor.fetchall()
      n = len(records)
      clear()
     
      for record in records:
       
          if(n <= 0):
            print(field_name, ' ', value, ' does not exist')
      wait = input('\n\n\n Press any key to continue....')

    conn.close()
    wait=input('\n\n\n Press any key to continue....')

def daily_report():
   clear()
   
   conn = mysql.connector.connect(
       host='localhost', database='Banking', user='root', password='root')
   today = date.today()
   cursor = conn.cursor()
   sql = 'select transaction_id,date_of_transaction,amount,type,account_no from transactions t  where t.date_of_transaction="'+ str(today)+'";'
   cursor.execute(sql)
   records = cursor.fetchall()
   clear()
   print('Daily Report :',today)
   print('-'*120)
   for record in records:
       print(record[0], record[1], record[2], record[3], record[4])
   print('-'*120)

   conn.close()
   wait = input('\n\n\n Press any key to continue....')


def monthly_report():
   clear()

   conn = mysql.connector.connect(
       host='localhost', database='Banking', user='root', password='root')
   today = date.today()
   cursor = conn.cursor()
   sql = 'select transaction_id,date_of_transaction,amount,type,account_no from transactions t where month(date_of_transaction)="' + \
       str(today).split('-')[1]+'";'
   cursor.execute(sql)
   records = cursor.fetchall()
   clear()
   print(sql)
   print('Monthly Report :', str(today).split(
       '-')[1], '-,', str(today).split('-')[0])
   print('-'*120)
   for record in records:
       print(record[0], record[1], record[2], record[3], record[4])
   print('-'*120)

   conn.close()
   wait = input('\n\n\n Press any key to continue....')

def yearly_report():
   clear()

   conn = mysql.connector.connect(
       host='localhost', database='Banking', user='root', password='root')
   today = date.today()
   cursor = conn.cursor()
   sql = 'select transaction_id,date_of_transaction,amount,type,account_no from transactions t where year(date_of_transaction)="' + \
       str(today).split('-')[1]+'";'
   cursor.execute(sql)
   records = cursor.fetchall()
   clear()
   print(sql)
   print('Yearly Report :', str(today).split(
       '-')[1], '-,', str(today).split('-')[0])
   print('-'*120)
   for record in records:
       print(record[0], record[1], record[2], record[3], record[4])
   print('-'*120)

   conn.close()
   wait = input('\n\n\n Press any key to continue....')

def transaction_details():
    clear()
    account_no = input('Enter account no :')
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    sql1 = 'select transaction_id,date_of_transaction,amount,type from transaction where account_no ='+account_no+';'
    df = pd.read_sql(sql1, conn)
    
    df.to_csv('d:\Banking ManagementSystem\\transaction.csv', index=False)
    #conn.close()
    df = pd.read_csv('d:\Banking ManagementSystem\\transaction.csv')
    print(df)
    cursor.execute(sql1)
    result = cursor.fetchone()

    conn.close()
    wait=input('\n\n\nPress any key to continue.....')

def report_menu():
    while True:
      clear()
      print('                                               Report Menu                                              ')
      print("\n                                       1.  Daily Report                                       ")
      print('\n                                        2.  Monthly Report                                       ')
      print('\n                                        3.  Yearly Report                                       ')
      print('\n                                        4.  Transaction Details                                       ')
      print('\n                                        5.  Customer Records                                       ')
      print('\n                                        6.  Back to Main Menu                                       ')
      print('\n\n')
      choice = int(input('Enter your choice ...: '))
      if choice == 1:
        daily_report()
      if choice == 2:
        monthly_report()
      if choice == 3:
        yearly_report()
      if choice == 4:
        transaction_details()
      if choice == 5:
        customer_record()
      if choice == 6:
        break

def add_account():
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
   
    name = input('Enter Name :')
    address = input('Enter address : ')
    phone = input('Enter Phone no :')
    email = input('Enter Email :')
    aadhar = input('Enter AAdhar no :')
    account_type = input('Account Type (saving/current ) :')
    balance = input('Enter opening balance :')
    cursor.execute("""insert into customers(name,address,phone,email,aadhar_no,account_type,balance,status) values ( %s,%s,%s,%s,%s,%s,%s,"active" )""",(name,address,phone,email,aadhar,account_type,balance))
    print('\n\nNew customer added successfully')
    sql1='select account_no from customers where phone ='+phone+';'
    cursor.execute(sql1)
    print("Your Account Number is :")
    b=cursor.fetchall()
    table = PrettyTable([ 'Account_no'])
    for rec in b:
        table.add_row(rec)
    print(table)
    
    conn.commit ()
    
    
    wait= input('\n\n\n Press any key to continue....')


def modify_account():
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    clear()
    account_no = input('Enter customer Account No :')
    print('                                       Modify screen ')
    print('\n                               1.  Customer Name')
    print('\n                               2.  Customer Address')
    print('\n                               3.  Customer Phone No')
    print('\n                               4.  Customer Email ID')
    choice = int(input('What do you want to change ? '))
    new_data  = input('Enter New value :')
    field_name=''
    if choice == 1:
       field_name ='name'
    if choice == 2:
       field_name = 'address'
    if choice == 3:
       field_name = 'phone'
    if choice == 4:
       field_name = 'email'
    sql ='update customers set ' + field_name + '="'+ new_data +'" where account_no='+account_no+';' 
    #print(sql)
    sql1 = 'COMMIT;'
    cursor.execute(sql)
    cursor.execute(sql1)
    print('\n\nCustomer Information modified..')
    wait = input('\n\n\n Press any key to continue....')

def close_account():
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    clear()
    account_no = input('Enter customer Account No :')
    sql ='update customer set status="close" where account_no ='+account_no+';'
    sql1 = 'COMMIT;'
    cursor.execute(sql)
    cursor.execute(sql1)
    print('\n\nAccount closed')
    wait = input('\n\n\n Press any key to continue....')

def activate_account():
    conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
    cursor = conn.cursor()
    clear()
    account_no = input('Enter customer Account No :')
    sql = 'update customers set status="active" where account_no ='+account_no+';'
    sql1 = 'COMMIT;'
    cursor.execute(sql)
    cursor.execute(sql1)
    print('\n\nAccount Activated')
    wait = input('\n\n\n Press any key to continue....')

def delete_account():
  conn = mysql.connector.connect(
        host='localhost', database='Banking', user='root', password='root')
  cursor = conn.cursor()
  clear()
  account_no = input('Enter customer Account No :')
  sql = 'delete from customers where account_no ='+account_no+';'
  sql1= 'COMMIT;'
  cursor.execute(sql)
  cursor.execute(sql1)
  print('\n\nAccount Deleted')
  wait = input('\n\n\n Press any key to continue....')

def main_menu():
    while True:
      clear()
      print('                                                      Main Menu                                                      ')
      print(" \n                                             1. Add Account                                                      ")
      print('\n                                              2. Modify Account                                            ')
      print('\n                                              3. Close Account                                            ')
      print('\n                                              4. Activate Account                                            ')
      print('\n                                              5. Transaction Menu                                            ')
      print('\n                                              6. Search Menu                                            ')
      print('\n                                              7. Report Menu                                            ')
      print('\n                                              8. Delete Account                                           ')
      print('\n                                              9. Close application                                            ')
      print('\n\n')
      
      choice = int(input('Enter your choice ...: '))
      if choice == 1:
        add_account()
      if choice == 2:
        modify_account()
      if choice == 3:
        close_account()

      if choice == 4:
        activate_account()

      if choice ==5 :
        transaction_menu()
      if choice ==6 :
        search_menu()
      if choice == 7:
        report_menu()
      if choice == 8:
        delete_account()        
      if choice ==9:
        exit()

if __name__ == "__main__":
    main_menu()
