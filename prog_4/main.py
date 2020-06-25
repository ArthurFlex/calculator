import os
import Authorization as Auto
import Account as Acc
import Notes
import Security

pathway_old=os.getcwd()
pathway_new=os.path.join(pathway_old,'Lab_4_Files') 
try:
    if not os.path.isdir(pathway_new):
        os.mkdir(pathway_new)
except OSError:
    print ("Создать директорию %s не удалось" %pathway_new )

flag=True
login=''
while flag:
    try:
        flag_5=True
        while flag_5:
            try:
                command=int(input("Действия пользователя:\n\t"
                                  "1) Авторизация\n\t"
                                  "2) Создание аккаунта\n\t"
                                  "3) Выход из программы\n"
                                  ))
                if command==1:
                    print("Авторизация\n")
                    login=Auto.sys_file_reader(pathway_new)
                    if login=='':
                        print("Ошибка авторизации,возврат в главное меню\n")
                    elif login!='':
                        print("Авторизация успешно выполнена\n")
                        print("Аккаунт: %s"% login)
                        flag_2=True
                        while flag_2:
                            try:
                                command=int(input("Действия пользователя:\n\t"
                                                  "1) Работа с заметками\n\t"
                                                  "2) Удаление аккаунта\n\t"
                                                  "3) Смена пользователя\n"
                                                  ))
                                if command==1:
                                    print("Работа с заметками\n")
                                    Notes.user_info(os.path.join(pathway_new,login),login)  
                                    flag_3=True
                                    while flag_3:
                                        try:
                                            command=int(input("Действия пользователя:\n\t"
                                                              "1) Создание новых заметок\n\t"
                                                              "2) Редактирование старых заметок\n\t"
                                                              "3) Удаление заметок\n\t"
                                                              "4)Выход в меню управления аккаунтом\n"
                                                              ))
                                            pathway=os.path.join(pathway_new,login)
                                            if command==1:
                                                print("Создание новых заметок")
                                                Notes.making_notes(pathway,login)
                                            elif command==2:
                                                Notes.changing_notes(pathway,login)
                                            elif command==3:
                                                Notes.del_notes(pathway,login)
                                            elif command==4:
                                                flag_3=False
                                        except ValueError:
                                            print("Ошибка ввода 5")
                                elif command==2:
                                    print("Удаление аккаунта")
                                    Acc.DelAcc(pathway_new,login)
                                    flag_2=False
                                elif command==3:
                                    print("Смена пользователя")
                                    login=''
                                    print("Выход из аккаунта")
                                    flag_2=False
                                else:
                                    print("Ошибка ввода 4")
                            except ValueError:
                                print("Ошибка ввода 3")
                            except FileNotFoundError:
                                print("Файл не найден")
                elif command==2:
                    print("Создание аккаунта")
                    Acc.MakingAcc(pathway_new)
                elif command==3:
                    flag=False
                    break
                else:
                    print("Ошибка ввода 2")
            except ValueError:
                print("Ошибка ввода 1")
    except ValueError:
        Security.sys_files_encode(os.path.join(pathway_new,"config_acc.conf"))
        print("Локальная ошибка")
    except FileNotFoundError:
        print("Файл не найден")
    except BaseException:
         print("Ошибка")
         Flag=False
         break
