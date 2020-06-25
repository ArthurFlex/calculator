import os
import Security


def sys_file_reader(sys_file_path:str):
    users_dict=dict()
    pathway=os.path.join(sys_file_path,"config_acc.conf")
    try:
        Security.sys_files_decode(pathway)
    except FileNotFoundError:
        print("Аккаунт ещё не создан.")

    with open(pathway,'r',encoding='utf-8') as account_file:
       for line in account_file:
           line.replace("\n","")
           line_list=line.split()
           users_dict[line_list[0]]=line_list[1]
    flag=True
    i=0
    while flag:
        login=input("Пожалуйста, введите логин. \n")
        if login in users_dict:
            hashed_password=users_dict[login]
            flag=False
        else:
            print("Пользователь с этим логином не найден. \n")
            i+=1
            if i==3:
                print("Слишком много ошибок.Возврат в главное меню.")
                Security.sys_files_encode(pathway)
                flag=False
                return ''
    i=0    
    flag=True
    while flag:
        password=input("Пожалуйста, введите пароль: \n")
        if Security.pass_check(hashed_password, password):
            flag=False
            Security.sys_files_encode(pathway)
            return login 
        else:
            print('Извините, но пароли не совпадают')
            i+=1
            if i==3:
                print("Слишком много ошибок.Возврат в главное меню.")
                Security.sys_files_encode(pathway)
                flag=False
                return '' 
 