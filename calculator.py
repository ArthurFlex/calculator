print ("hello,user")
flag=True
while flag: 
    val_1=float(input("input val_1:"))
    val_2=float(input("input val_2:"))
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
           
    counter = 0
    while True:
        if counter ==3:
            print ("Команда введена неверно 3 раза!Выполняю выход из программы...")
            exit()
        command=input("Do you want to continue?(Y/N):")
        if command.upper() =="N":
            flag=False
            break 
        elif command.upper() =="Y":
            flag=True
            break 
        else:
            counter+=1
            print ("Введена неправильная команда!")
print ("goodbye")       
    
     