
import json
import random
import string 
from pathlib import Path

class Bank:
    database="database.json"
    data=[]
    if Path(database).exists():
     
        
        
     with open(database) as fs:
        data=json.loads(fs.read())

    @classmethod
    def __update(cls):
        with open(cls.database,"w") as fs:
            fs.write(json.dumps(cls.data))

    @classmethod
    def __accountgenerate(cls):
        alpha=random.choices(string.ascii_letters,k=8)
        num=random.choices(string.digits,k=4)

        acc=alpha+num
        random.shuffle(acc)
        return "".join(acc)
    


    def create_user(self):
        info={
            "name":input("tell user name:- "),
            "age":int(input("tell user age :- ")),
            "email":input("tell user email:- "),
            "AccountNo":str(input("enter your account number:- ")),

            "pin":int(input("tell user pin:-- ")),
            "balance":0

        }

        if info['age']<12 or len(str(info["pin"])) !=4:
            print("sorry you are not able to create the account ")
        else:
            Bank.data.append(info)
            Bank.__update()
    
    def deposit_money(self):
        accno=input("tell me your account number:- ")
        pin=int(input("enter your pin "))

        userdata=[i for i in Bank.data if i["AccountNo"]==accno and i['pin']==pin]

        if userdata==False:
            print("sorry no such user exists")
        else:
            amount=int(input("Enter money for Deposit := "))
            userdata[0]['balance']+=amount
            bank.__update()
            print("Ballance deposit succesful ")
            
    def withdraw_money(self):
            accno=str(input("tell me your account number"))
            pin=int(input("enter your pin "))

            userdata=[i for i in Bank.data if i["AccountNo"]==accno and i['pin']==pin]

            if userdata==False:
                print("sorry no such user exists")
            else:
                amount=int(input("Enter your money for withdraw:= "))
                if amount>userdata[0]['balance']:
                    print("insufficient balance")
                else:
                 userdata[0]['balance']-=amount
                 bank.__update()
                 print("Ballance withdraw succesful ")


    def show_details(self):
        accno=input("tell your account number: ")
        pin=int(input("tell me your pin: "))
        userdata=[i for i in Bank.data if i["AccountNo"]==accno and i['pin']==pin]
        if not userdata:
            print("no data found ! ")
        else:
            for i in userdata[0]:
                print(f"{i}--{userdata[0][i]}")

    def update_details(self):
        accno=input("tell your account number: ")
        pin=int(input("tell me your pin: "))
        userdata=[i for i in Bank.data if i["AccountNo"]==accno and i['pin']==pin]

        if userdata==False:
            print("no user found ")
        else:
            print("you cannot change bankbalance ,account number and age ")
            newdata={"name":input("tell your new name or press enter to skip ."),
                     "email":input("tell your email or press enter to skip."),
                     "pin":int(input("tell your pin or press enter to skip."))
                     }
            if newdata["name"]=="":
                newdata["name"]=userdata[0]["name"]
            if newdata["email"]=="":
                newdata["email"]=userdata[0]["email"]
            if newdata["pin"]=="":
                newdata["pin"]=str(userdata[0]["pin"])

            for i in userdata[0]:
                if i in newdata and i !="pin":
                    userdata[0][i]=int(newdata[i])

            Bank.__update()

    def delete_account(self):
         accno=input("tell your account number: ")
         pin=int(input("tell me your pin: "))
         userdata=[i for i in Bank.data if i["AccountNo"]==accno and i['pin']==pin]

         if userdata==False:
             print("no such user found ! ")
         else:
             print("are you sure you want to delete ")
             check=input("press y(yes) or n(no) :")
             if check=="y":
                 index=Bank.data.index(userdata[0])
                 Bank.data.pop(index)

                 Bank.__update()



bank=Bank()
while True:

    print("press 1 for creating an account  ")
    print("press 2 for depositing the money ")
    print("press 3 for withdrawing money  ")
    print("press 4 for details of a user ")
    print("press 5 for updating user details  ")
    print("press 6 for deleting user  ")
    print("press 0 to exit ")

    res=int(input(" enter your response plz: "))

    if res==1:
        bank.create_user()
    elif res==2:
        bank.deposit_money()
    elif res==3:
        bank.withdraw_money()
    elif res==4:
        bank.show_details()
    elif res==5:
        bank.update_details()
    elif res==6:
        bank.delete_account()
    elif res==0:
        break
    else:
        print("invalid input plz try again ")














