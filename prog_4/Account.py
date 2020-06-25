import os
import shutil
import Security

def write_new_acc(login:str,new_password:str,pathway:str):
        try:
            Security.sys_files_decode(pathway)
        except FileNotFoundError:
            pass
        with open(pathway,'a',encoding='utf-8') as config_acc:
            line=''
            password_new=Security.pass_hash(new_password)
            line=line+str(login)+' '+str(password_new)+'\n'
            config_acc.write(line)
        Security.sys_files_encode(pathway)
    

def MakingAcc(sys_file_path:str):
    login_list=list()
    pathway=os.path.join(sys_file_path,"config_acc.conf")
    try:
        Security.sys_files_decode(pathway)
        with open(pathway,'r',encoding='utf-8') as config_acc:
            for line in config_acc:
                line.replace("\n","")
                line_list=line.split()
                login_list.append(line_list[0])
    except FileNotFoundError:
        print("Другие аккаунты отсутсвуют. \n")
    flag=True
    i=0
    while flag:
        try:
            login=input("Введите ваш логин:")
            if len(login)<1:
                print("Слишком маленькая длина логина.Пожалуйста, введите другой логин.")
            elif len(login)>100:
                print("Слишком большая длина логина.Пожалуйста, введите другой логин.")
            elif login_list.count(login)>0:
                print("Этот логин уже занят.Пожалуйста, введите другой логин.")
            elif len(login)>1 or len(login)==1 and login_list.count(login)<1:
                print("Логин принят.Далее...")
                flag=False
        except BaseException:
            print("Проблемы с логином")
            i+=1
            if i==3:
                flag=False
                Security.sys_files_encode(pathway)
                break
    try:
        Security.sys_files_encode(pathway)
    except FileNotFoundError:
        pass
    flag=True
    while flag:
        try:
            new_password=input("Пожалуйста, придумайте пароль ")
            if len(new_password)<=1:
                print("Слишком простой пароль.Пожалуйста, придумайте другой.")
            elif len(new_password)>30:
                print("Пароль слишком большой.Пожалуйста, придумайте другой.")
            elif len(new_password)>1:
                write_new_acc(login,new_password,pathway)
                print("Аккаунт был успешно создан.")
                try:
                    if not os.path.isdir(os.path.join(sys_file_path,login)): 
                        os.mkdir(os.path.join(sys_file_path,login))
                except OSError:
                    print ("Создать директорию %s не удалось" %sys_file_path )
                try:
                    if not os.path.isdir(os.path.join(sys_file_path,login,"Notes")): 
                        os.mkdir(os.path.join(sys_file_path,login,"Notes"))
                except OSError:
                    print ("Создать директорию %s не удалось" %sys_file_path )
                try:
                    if not os.path.isdir(os.path.join(sys_file_path,login,"Keys")): 
                        os.mkdir(os.path.join(sys_file_path,login,"Keys"))
                except OSError:
                    print ("Создать директорию %s не удалось" %sys_file_path )
                Security.gen_keys(login,os.path.join(sys_file_path,login,"Keys")) 
                flag=False
        except ValueError:
            Security.sys_files_encode(pathway)
            print("Проблемы с паролем.")
            i+=1
            if i==3:
                flag=False
                break
           

def DelAcc(sys_file_path:str,login:str):
    pathway=os.path.join(sys_file_path,"config_acc.conf")
    Login_dict=dict()
    flag=True
    while flag:
        try:
            Security.sys_files_decode(pathway)
            with open(pathway,"r",encoding='utf-8') as config_file:
                for line in config_file:
                    time_list=line.split(' ',1)
                    Login_dict[time_list[0]]=time_list[1]
            with open(pathway,"w",encoding='utf-8') as config_file:
                for key in Login_dict:
                    line=''
                    if key!=login:
                        line=line+key+" "+Login_dict[key]
                        config_file.write(line)
            Security.sys_files_encode(pathway)
            pathway=os.path.join(sys_file_path,login)
            shutil.rmtree(pathway)
            print("Аккаунт успешно удален.")
            flag=False
        except FileNotFoundError:
            print("Файл или директория не найдены.Невозможно удалить.")
            Security.sys_files_encode(pathway)