import os
import time
import Security

def user_info(pathway:str,login:str):
    try:
        list_of_files=os.listdir(os.path.join(pathway,"Notes")) 
        print("Логин - %s\n"% login)
        print("Количество заметок - %s\n"% len(list_of_files))
        print("Ваши заметки:\n")
        for elem in list_of_files:
            list=elem.split(".")
            line=''
            for elem in list:
                if elem!='txt':
                    line=line+elem
            if line=='':
                print("Заметка без имени.")
            elif line!='':
                print(line)
        print('\n')
    except ValueError:
       print("Нет информации об аккаунте")

def making_notes(pathway:str,login:str):
    flag_1=True
    while flag_1:
        flag=True
        while flag:
            try:
                command=str(input("Введите имя для новой заметки с расширением (.txt) "))
                command=command.replace(' ','_')
                list=command.split(".")
                list.reverse()
                if list[0]=='txt':
                    list_forbid=["\\","/",":","*","?","\"","|","<",">"]
                    for ch in command:
                        if list_forbid.count(ch)!=0:
                            print("Неккоректное имя файла- испольюзуются неподходящие символы.")
                            break    
                    flag=False
                else:
                    print('Неправильное расширение файла.')
            except ValueError:
                print("Ошибка ввода.")
        pathway_new=os.path.join(pathway,"Notes",command)
        try:
            with open(pathway_new,'r',encoding='utf-8') as New_Note:
                print("Заметка с этим именем уже была сделана")
        except FileNotFoundError:
            with open(pathway_new,'a',encoding='utf-8') as New_Note:
                print("Открытие файла...")
            os.system(pathway_new) 
            Security.usual_files_encode(pathway,pathway_new)
            flag_1=False
        except OSError:
            print("Пожалуйста, введите правильный путь.")


def changing_notes(pathway:str,login:str):
    flag_1=True
    while flag_1:
        try:
            flag=True
            while flag:
                try:
                    command=str(input("Введите имя вашей заметки с расширением (.txt) "))
                    command=command.replace(' ','_')
                    list=command.split(".")
                    list.reverse()
                    if list[0]=='txt':
                        list_forbid=["\\","/",":","*","?","\"","|","<",">"]
                        for i in command:
                            if list_forbid.count(i)!=0:
                                print("Неккоректное имя файла- испольюзуются неподходящие символы.")
                                break    
                        flag=False
                    else:
                        print('Неправильное расширение файла.')
                except ValueError:
                    print("Ошибка ввода")
            pathway_new=os.path.join(pathway,"Notes",command)
            Security.usual_files_decode(pathway,pathway_new)
            with open(pathway_new,'a',encoding='utf-8') as New_Note:
                print("Открытие файла...")
            os.system(pathway_new)
            Security.usual_files_encode(pathway,pathway_new)
            flag_1=False
        except OSError:
            print("Пожалуйста, введите правильный путь.")


def del_notes(pathway:str,login:str):
    i=0
    flag=True
    command=input("Если Вы действительно хотите удалить заметку, то введите имя этой заметки.\n")
    while flag:
        if i!=0:
            command=input("Введите имя заметки с расширением (.txt)")
        list=command.split('.')
        list.reverse()
        if list[0]=='txt':
            try:
                os.remove(os.path.join(pathway,"Notes",command))
                print("Заметка успешно удалена.")
                flag=False
            except FileNotFoundError:
                print("Заметка не найдена.")
                i+=1
            except OSError:
                print("Указан неправильный путь/Вы использовали некорректные символы.")
                i+=1
        else:
            command=command+'.txt'
            try:
                os.remove(os.path.join(pathway,command))
                print("Заметка успешно удалена.")
                flag=False
            except FileNotFoundError:
                print("Заметка не найдена.")
                i+=1
            except OSError:
                print("Указан неправильный путь/Вы использовали некорректные символы.")
                i+=1