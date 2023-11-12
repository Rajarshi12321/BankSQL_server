# =========================Main File============================#
import Bank as b
print('----Disclaimer----\nPlease Enter Your Account Details Carefully\nFormat Of Date is:yyyy-mm-dd')
ch = input('----WELCOME TO THE BANK OF KV----\n1.Create Account\n2.Deposit\
        \n3.Withdrawl\n4.Transfer\n5.Statement\n6.History\n7.Exit\nEnter Your Choice:')
while ch != '7':
    if ch == '1':
        b.create_acc()
    elif ch == '2':
        acc_no = int(input('Enter your account number:'))
        name = input('Enter Your Name:')
        deposit = int(input('Enter amount to deposit:'))
        transaction_id = b.TID()
        b.deposit(acc_no, name, deposit, transaction_id)
    elif ch == '3':
        acc_no = int(input('Enter your account number:'))
        name = input('Enter Your Name:')
        withdraw = int(input('Enter amount to withdraw:'))
        transaction_id = b.TID()
        b.withdraw(acc_no, name, withdraw, transaction_id)
    elif ch == '4':
        acc_no_reciever = int(input('Enter account number of reciever:'))
        reciever_name = input("Enter Reciever's Name:")
        acc_no_sender = int(input('Enter account number of sender:'))
        sender_name = input("Enter Sender's Name:")
        transfer_amount = int(input('Enter amount to transfer:'))
        transaction_id = b.TID()
        b.transfer(
            acc_no_reciever,
            reciever_name,
            acc_no_sender,
            sender_name,
            transfer_amount, transaction_id)
    elif ch == '5':
        acc_no = int(input('Enter your account number:'))
        b.stmnt(acc_no)
    elif ch == '6':
        acc_no = int(input('Enter your account number:'))
        start_date = input('Enter Starting Date (YYYY-MM-DD) :')
        end_date = input('Enter Ending Date (YYYY-MM-DD) :')
        limit = int(input('How may transactions do you want to see:'))
        b.history(acc_no, start_date, end_date, limit)
    else:
        print('Invalid Input')
    ch = input('----WELCOME TO THE BANK OF KV----\n1.Create Account\n2.Deposit\
        \n3.Withdrawl\n4.Transfer\n5.Statement\n6.History\n7.Exit\nEnter Your Choice:')
print('Thank you for using our Bank\n We serve the best')
