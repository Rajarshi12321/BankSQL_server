import mysql.connector as m
import os
from dotenv import load_dotenv
from datetime import date
import random as r
import string as s

load_dotenv()

PASSWORD = os.getenv("PASSWORD")

db = m.connect(host='localhost', user='root', passwd=PASSWORD,
               database='bank_of_kv')
cur = db.cursor()


def create_acc():
    try:

        cr = "insert into account(Acc_No_,Name,Father_name,mother_name,dob,balance) values(%s,%s,%s,%s,%s,%s)"
        accountID = AID()
        name = input('Enter Your Name:')
        Fname = input("Enter Your Father's Name:")
        Mname = input("Enter Your Mother's Name:")
        DOB = input("Enter Your D.O.B (YYYY-MM-DD):")
        amount = int(input("Enter Your Opening Amount:"))
        val = (accountID, name, Fname, Mname, DOB, amount)
        cur.execute(cr, val)
        print('Your Account No.:', accountID,
              '\nYour Name:', name, '\nBalance:', amount)
        db.commit()
    except:
        print('Please check the details you have entered')


def deposit(acc_no, name, amount, TID):
    try:

        statement = "update Account set balance=balance+%s where Acc_No_=%s and Name=%s"
        cur.execute(statement, (amount, acc_no, name))
        statement = "insert into deposit values ('%s','%s','%s','%s','%s')"
        cur.execute(statement % (acc_no, name, date.today(), amount, TID))
        statement = "select balance from account where Acc_No_=%s and Name='%s'"
        cur.execute(statement % (acc_no, name))
        fetched = cur.fetchone()
        balance = int(fetched[0])
        print('Your Account No.:', acc_no, '\nYour current balance is',
              balance, '\nTransaction ID:', TID)
        db.commit()
    except:
        print('This account is invalid \nPlease check the details you have entered')


def withdraw(acc_no, name, amount, TID):
    try:
        statement = "select balance from account where Acc_No_=%s and Name='%s'"
        cur.execute(statement % (acc_no, name))
        fetched = cur.fetchone()
        balance = int(fetched[0])
        if balance > amount:
            statement = "insert into withdrawl values (%s,%s,%s,%s,%s)"
            cur.execute(statement, (acc_no, name, date.today(), amount, TID))
            statement = "update Account set balance=balance-%s where Acc_No_=%s and Name=%s"
            cur.execute(statement, (amount, acc_no, name))
            statement = "select balance from account where Acc_No_=%s and Name='%s'"
            cur.execute(statement % (acc_no, name))
            fetchbalance = cur.fetchone()
            c = int(fetchbalance[0])
            print('Your Account No.:', acc_no, '\nYour current balance is',
                  c, '\nTransactionID:', TID)
            db.commit()
        else:
            print('Your account has insufficient balance.')
    except:
        print('This account is invalid \nPlease check the details you have entered')


def transfer(acc_no_reciever, reciever_name, acc_no_sender, sender_name, amount, TID):
    try:
        statement = "select balance from account where Acc_No_=%s"
        cur.execute(statement % (acc_no_sender))
        fetched = cur.fetchone()
        print(fetched)
        balance = int(fetched[0])
        if balance > amount:
            statement = "update account set balance=balance-%s where Acc_No_=%s and Name=%s"
            cur.execute(statement, (amount, acc_no_sender, sender_name))
            statement = "update account set balance=balance+%s where Acc_No_=%s and Name=%s"
            cur.execute(statement, (amount, acc_no_reciever, reciever_name))
            statement = "select balance from account where Acc_No_=%s and Name='%s'"
            cur.execute(statement % (acc_no_sender, sender_name))
            a = cur.fetchone()
            print('Your Account No.:', acc_no_sender, '\nYour current balance is',
                  balance-amount, '\nTransaction ID:', TID)
            s = "insert into transfer values (%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(s, (acc_no_reciever, reciever_name, acc_no_sender,
                        sender_name, amount, date.today(), TID))
        else:
            print('Your account has insufficient balance.')
        db.commit()
    except:
        print('This account is invalid \nPlease check the details you have entered')


def TID():

    while True:
        l = ''
        for i in range(30):
            g = r.choice(s.ascii_uppercase+s.digits)
            l += g
        statement = "select Transaction_ID from id"
        cur.execute(statement)
        fetchedall = cur.fetchall()
        if l not in fetchedall:
            statement = "insert into id(transaction_id) values('%s')" % (l)
            cur.execute(statement)
            db.commit()
            return l
        else:
            True


def AID():
    while True:
        l = ''
        for i in range(9):
            g = r.choice(s.digits)
            l += g
        statement = "select Acc_No_ from id"
        cur.execute(statement)
        fetchedall = cur.fetchall()
        if l not in fetchedall:
            statement = "insert into id(Acc_No_) values('%s')" % (l)
            cur.execute(statement)
            db.commit()
            return l
        else:
            True
    # db.commit()


def stmnt(acc_no):
    try:

        statement = "select Name,balance from account where Acc_No_=%s"
        cur.execute(statement % (acc_no))
        fetched = cur.fetchone()
        print('Account Number:', acc_no, '\nName:',
              fetched[0], '\nBalance:', fetched[1])
        db.commit()
    except:
        print('This account is invalid \nPlease check the details you have entered')


def history(acc_no, start_date, end_date, limit):
    import datetime

    statement = "create table demo(acc_no_reciever int, reciever_name varchar(20), acc_no_sender int, sender_name Varchar(20),Balance int,    Date date, TID Varchar(30),  transaction_category Varchar(20))"
    cur.execute(statement)

    # Getting deposit data

    statement = "select * from deposit where %s=Acc_No_ and Date between %s and %s"
    cur.execute(statement, (acc_no, start_date, end_date))
    fetchedall = cur.fetchall()
    for i in fetchedall:
        statement = 'insert into demo(acc_no_reciever,reciever_name,Date,Balance,TID, transaction_category) values(%s,%s,%s,%s,%s,%s)'
    cur.execute(statement, (i[0], i[1], i[2], i[3], i[4], 'Credit'))

    # Getting withdrawl data

    statement = "select * from withdrawl where Acc_No_=%s and Date between %s and %s"
    cur.execute(statement, (acc_no, start_date, end_date))
    fetchedall = cur.fetchall()
    for i in fetchedall:
        statement = 'insert into demo(acc_no_sender,sender_name,Date,Balance,TID, transaction_category) values(%s,%s,%s,%s,%s,%s)'
        cur.execute(statement, (i[0], i[1], i[2], i[3], i[4], "Debit"))

    # Getting transfer data

    statement = "select * from transfer where acc_no_reciever=%s or acc_no_sender=%s and Date between %s and %s"
    cur.execute(statement, (acc_no, acc_no, start_date, end_date))
    fetchedall = cur.fetchall()
    for i in fetchedall:
        statement = "insert into demo(acc_no_reciever,reciever_name,acc_no_sender,sender_name,Date,Balance,TID, transaction_category) values(%s,%s,%s,%s,%s,%s,%s,%s) "
        cur.execute(statement, (i[0], i[1], i[2],
                    i[3], i[5], i[4], i[6], 'Transfer'))
    try:
        statement = "select * from demo order by date desc"
        cur.execute(statement)
        fetchedall = cur.fetchall()
        if len(fetchedall) == 0:
            print('This account is invalid \nPlease check the details you have entered')
        elif limit >= len(fetchedall):
            print('ANO(R)', 'NO(R)', 'acc_no_sender', 'sender_name', 'Balacnce',
                  'Date', 'TID', 'DCT', sep='     ')
            for i in fetchedall:
                print(i[0], i[1], i[2], i[3], i[4],
                      i[5], i[6], i[7], '\n')
        else:
            print('ANO(R)', 'NO(R)', 'acc_no_sender', 'sender_name', 'Balacnce',
                  'Date', 'TID', 'DCT', sep='     ')
            for i in range(limit):
                print(fetchedall[i][0], fetchedall[i][1], fetchedall[i][2], fetchedall[i][3], fetchedall[i][4], fetchedall[i]
                      [5].strftime('%Y-%m-%d'), fetchedall[i][6], fetchedall[i][7], '\n')
    except:
        print('This account is invalid \nPlease check the details you have entered')
        db.commit()

    finally:
        statement = 'drop table demo'
        cur.execute(statement)
        db.commit()
