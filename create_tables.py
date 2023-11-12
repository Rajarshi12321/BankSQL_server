import mysql.connector as m
import os
from dotenv import load_dotenv

load_dotenv()

PASSWORD = os.getenv("PASSWORD")


db = m.connect(host='localhost', user='root',
               passwd=PASSWORD)
cur = db.cursor()
cr = """create database bank_of_kv;

use bank_of_kv;

create table account(
Acc_No_ int Primary key,
Name varchar(25),
Father_Name varchar(25),
Mother_Name varchar(25),
DOB date,
Balance int
);
create table deposit(
Acc_No_  int,
Name varchar(25),
Date date,
Amount int,
Transaction_ID varchar(30),
foreign key (Acc_No_) references Account(Acc_No_)
);

create table Withdrawl(
Acc_No_  int,
Name varchar(25),
Date date,
Amount int,
Transaction_ID varchar(30),
foreign key (Acc_No_) references Account(Acc_No_)
);

create table Transfer(
acc_no_reciever int,
reciever_name varchar(25),
acc_no_sender int,
sender_name  varchar(25),
Amount int(12),
Date date,
Transaction_ID varchar(30),
foreign key (acc_no_reciever) references Account(Acc_No_),
foreign key (acc_no_sender) references Account(Acc_No_)
);

create table id(
Transaction_ID varchar(30),
Acc_No_ int
);"""
cur.execute(cr, multi=True)
db.commit()
