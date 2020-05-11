data=dict()
flag=True 
with open(r"C:\Users\User\.vscode\my programms\программы\conf.txt","r") as file:
    for line in file:
        if line[0]!='#' and line[0]!=';' and line[0]!='\n':
            list0=line.split(' ',1)
            x=len(list0)
            if x>1:
                key=list0[0]
                value=list0[1]
                data[key]=value
            if x==1:
                key=list0[0].rstrip('\n')
                value="Значение не задано"
                data[key]=value
while flag:
    try:
        key=input("Введите значение ключа:")  
        print("Ключ:",key,"\n","Значение:",data[key])
    except:
        print("Ключ:", key,"\n","Ошибка ввода ключа")
    while True:
        command=input("Хотите продолжить?(Y/N):")
        if command.upper() =="N":
            flag=False
            break 
        elif command.upper() =="Y":
            flag=True
            break 
        else:
            print ("Введена неправильная команда!")
print("Завершение сеанса")
        