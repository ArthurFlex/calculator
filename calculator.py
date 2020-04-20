print ("hello,user")
flag=True
while flag: 
    val_1=int(input("input val_1:"))
    val_2=int(input("input val_2:"))
    command=input("input command:")
    if command=="+":
        print(val_1,"+",val_2,"=",val_1+val_2)
    elif command=="-":
        print(val_1,"-",val_2,"=",val_1-val_2)
    elif command=="*":
        print (val_1,"*",val_2,"=",val_1*val_2)     
    elif command=="/":
        print(val_1,"/",val_2,"=",val_1/val_2)
    else:
        print("введен неверный символ!")    
   
    for i in range(1,4):
        command=input("Do you want to continue?(Y/N):")
        if command=="N":
            flag=False
            break 
        elif command=="Y":
            flag=True
            break 
        if i==3:
            print ("Команда введена неверно 3 раза!Выполняю выход из программы...")
            flag=False
        else:
            print ("Введена неправильная команда!")
print ("goodbye")       
    
     