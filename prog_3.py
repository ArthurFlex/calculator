from abc import ABC, abstractmethod
import random

class MainClass(ABC):

    @abstractmethod
    def gen_key(self, **kwargs):
        pass
   
    @abstractmethod
    def ciphering(self, **kwargs):
        pass

    @abstractmethod
    def deciphering(self, **kwargs):
        pass

   


    def _made_file(self, file):
        flag = True
        while flag:
            try:
                path = input(f"Введите путь для создания файла {file}: ")
                if path.endswith(f".{file}"):
                    flag=False
                    break
                else:
                    print("Неправильный тип файла")
            except Exception:
                print("Ошибка в пути файла")
        return path        
        

    def _file_path(self, file):
        flag = True
        while flag:
            path=input(f"Введите путь к файлу {file} : ")
            try:
                if path.endswith(f".{file}"):
                    flag = False
                    break
                else:
                    print("Неверный тип файла")
            except Exception:
                print("Ошибка в пути файла")
        return path         

       
    def _open_text_file(self):
        flag = True
        while flag:
            try:
                path = self._file_path('txt')
                with open(path, "r", encoding="utf-8") as text_file:
                    text_list = []
                    for line in text_file:
                        text_list.extend(list(line))
                    if len(text_list)!=0:
                        flag = False
                        break
                    else:
                        print("Пустой файл")
            except Exception:
                print("Ошибка")
        return text_list

    def _open_alph(self):
        flag = True
        while flag:
            try:
                alph_list0 = []
                path = self._file_path('alph')
                with open(path, "r", encoding="utf-8") as alph_file:
                    alph_list1 = []
                    for line in alph_file:
                        alph_str = line.rstrip('\n')
                        if len(alph_str) == 1 and line[0] != '\n':
                            alph_list1.append(alph_str)
                        elif len(alph_str) != 1:
                            str0 = alph_str.split()
                            alph_str = ''.join(str0)
                            if len(alph_str) == 1:
                                alph_list1.append(alph_str)
                    for z in alph_list1:
                        if z not in alph_list0:
                            alph_list0.append(z)
                    if len(alph_list0) == 0:
                        print("В файле с алфавитом значения не подходят или отсутствуют")            
                flag = False
                break
            except Exception:
                print("Ошибка")
        return alph_list0    

    def _open_cipher_text(self, crypt):
        flag = True
        while flag:
            try:
                path = self._file_path('encrypt')
                with open(path, "r", encoding="utf-8") as cipher_file:
                    cipher_list = []
                    for line in cipher_file:
                        key_str = line.rstrip('\n')
                        cipher_list.append(key_str)
                    if cipher_list[0] == crypt:
                        cipher_list.clear()
                        str0 = list(line)
                        cipher_list.extend(str0)
                        if len(cipher_list) != 0:
                            flag = False
                            break
                        else:
                            print("Ошибка:пустой файл")
                    else:
                        print("Файл шифрованного текста для другого метода")        
            except Exception:
                print("Ошибка")
        return path

    
        
    def _open_key(self, crypt):
        flag = True
        while flag:
            try:
                path = self._file_path('key')
                with open(path, "r", encoding="utf-8") as key_file:
                    key_list = []
                    for line in key_file:
                        key_str = line.rstrip('\n')
                        key_list.append(key_str)
                    if key_list[0] == crypt:
                        if len(key_list) != 0:
                            flag = False
                            break
                        else:
                            print("Пустой файл")
                    else:
                        print("Ключ для другого метода")    
                    
            except Exception:
                print("Ошибка")
        return path

   


#метод перестановки
class TranspositionMethod(MainClass):

    def gen_key(self, **kwargs):
        flag = True
        error=0
        while flag:
            try:
                len_key = 0
                while len_key < 2:
                    len_key = int(input("Введите длину ключа: "))
                    if len_key < 2:
                        print("Ключ слишком короткий ")    
                key_list = [x for x in range(1, len_key+1)]
                random.shuffle(key_list)
                key_filepath = self._made_file('key')
                with open(key_filepath,'x',encoding='utf-8') as key_file:
                    key_file.write('шифр перестановки\n')
                    i=0
                    str0=''
                    while i < len(key_list):                   
                        str0 = str0 + str(key_list[i]) + ' '
                        i+=1 
                    key_file.write(str0)
                    flag == False
                    print("Ключ был успешно сохранен.")
                    break
            except ValueError:
                print("Недопустимый символ")
                error+=1
                if error > 2:
                    print("Совершены 3 ошибки ввода!Выполняю выход из программы...!")
                    flag = False
                    break
            except Exception:
                print("Ошибка") 

    def __read_key(self):
        key_filename = self._open_key('шифр перестановки')
        with open(key_filename,'r', encoding='utf-8') as key_file:
            i=0
            for line in key_file:
                if i < 1:
                    i+=1
                    pass
                elif i==1:
                    line=line.rstrip(' ')
                    key_list = line.split(' ')    
        return key_list   

    def ciphering(self, **kwargs):
        text_list = self._open_text_file()
        key_list = self.__read_key()
        len_key = len(key_list)
        while len(text_list)%len_key != 0:
            text_list.append(random.choice(text_list))
        len_text = len(text_list)
        
        flag = True
        while flag:
            try:
                cipher_path = self._made_file('encrypt')
                with open(cipher_path,'x', encoding='utf-8') as cipher_file:
                    cipher_file.write('шифр перестановки\n')
                    str0=''
                    k=0
                    p=0
                    block_lict=[None]*len_key
                    for i in range(len_text):
                        x=0
                        flag1 = True
                        while flag1:
                            if int(key_list[x]) == k%len_key + 1:
                                block_lict.pop(x)
                                block_lict.insert(x, text_list[i])
                                k+=1
                                flag1 = False
                                break
                            else:
                                x+=1
                        p+=1
                        if p == len_key:
                            for z in range(len_key):
                                str0 = str0 + f'{block_lict[z]}'
                            block_lict = [None]*len_key
                            p=0
                    cipher_file.write(str0)
                    print("Текст был успешно преобразован!")
                    flag = False
                    break
            except Exception:
                print("Ошибка")  

    def deciphering(self, **kwargs):
        key_list = self.__read_key()
        len_key = len(key_list)
        cipher_list = self.__read_cipher(len_key)
        len_cipher = len(cipher_list)
        flag1 = True
        while flag1:
            try:
                decipher_path = self._made_file('txt')
                with open(decipher_path,'x', encoding='utf-8') as decipher_file:
                    str0=''
                    k=0
                    p=0
                    block_lict = [None]*len_key
                    for i in range(len_cipher):
                        x=0
                        flag = True
                        while flag:
                            for x in range(len_key):
                                if (x+1) == int(key_list[k]):
                                    block_lict.pop(x)
                                    block_lict.insert(x, cipher_list[i])
                                    k = (k + 1)%len_key
                                    flag = False
                                    break
                                else:
                                    x+=1
                        p+=1
                        if p == len_key:
                            for z in range(len_key):
                                str0 = str0 + f'{block_lict[z]}'
                            block_lict = [None]*len_key
                            p=0
                    decipher_file.write(str0)
                    print("Текст был успешно преобразован!")
                    flag1 = False
                    break
            except Exception:
                print("Ошибка") 

    def __read_cipher(self, len_key):
        cipher_file = open(self._open_cipher_text('шифр перестановки'),'r', encoding='utf-8' )
        cipher_list = []
        i=0
        for line in cipher_file:
            if i < 1:
                i+=1
            else:
                cipher_list.extend(list(line))
        return cipher_list            

                              

    

    
#метод гаммирования
class GammaMethod(MainClass):

    def gen_key(self, **kwargs):
        flag = True
        error=0
        while flag:
            try:
                gamma=0
                while gamma < 2:
                    gamma=int(input("Введите значение гаммы: "))
                    if gamma < 2:
                        print("Слишком маленькое значение гаммы")
                key_list = [i + 1 for i in range(gamma)]
                random.shuffle(key_list)
                key_file = open(self._made_file('key'),'x',encoding='utf-8')
                key_file.write('шифр гаммирования\n')
                i=0
                str0=''
                while i < len(key_list):                   
                    str0 = str0 + str(key_list[i]) + ' '
                    i+=1
                str0 = str0.rstrip(' ')
                key_file.write(str0)
                flag == False
                print("Ключ был успешно сохранен.")
                break
            except ValueError:
                print("Недопустимый символ")
                error+=1
                if error > 2:
                    print("Совершены 3 ошибки ввода!Выполняю выход из программы...!")
                    flag = False
                    break
            except Exception:
                print("Ошибка") 
                
    def __read_key(self):
        key_file = open(self._open_key('шифр гамирования'),'r', encoding='utf-8')
        key_list = []
        i=0
        for line in key_file:
            if i < 1:
                i+=1
            else:
                key_list = line.split(' ')
        return key_list, len(key_list) 
    
    def ciphering(self, **kwargs):
        text_list = self._open_text_file()
        key_list, gamma = self.__read_key()
        alph_list=self._open_alph()
        while len(text_list)%gamma != 0:
            text_list.append(random.choice(text_list))
        len_text = len(text_list)
        len_alph = len(alph_list)
        flag1 = True
        while flag1:
            try:
                with open(self._made_file('encrypt'),'x', encoding='utf-8') as cipher_file:
                    cipher_file.write('шифр гаммирования\n')
                    i=0
                    k=0
                    str0=''
                    while len(str0) != len_text:
                        if k<len_alph:
                            if  text_list[i] == alph_list[k]:
                                key_val = int(key_list[i%gamma])
                                cipher_val = (k+key_val)%len_alph
                                str0 = str0 + f'{alph_list[cipher_val]}'
                                i+=1
                                k=0
                            else:
                                k+=1
                        else:
                            str0 = str0 + text_list[i]
                            i+=1
                            k=0
                    cipher_file.write(str0)
                    print("Текст был успешно преобразован!")
                    flag1 = False
                    break
            except Exception:
                print("Ошибка")       

    def deciphering(self, **kwargs):
        cipher_list = self.__read_cipher()
        key_list, gamma = self.__read_key()
        alph_list = self._open_alph()
        len_cipher = len(cipher_list)
        len_alph = len(alph_list)
        flag1 = True
        while flag1:
            try:
                with open(self._made_file('txt'),'x', encoding='utf-8') as decipher_file:
                    i=0
                    k=0
                    str0=''
                    while len(str0) != len_cipher:
                        if k<len_alph:
                            if  cipher_list[i] == alph_list[k]:
                                key_val = int(key_list[i%gamma])
                                cipher_val = (k - key_val + len_alph)%len_alph
                                str0 = str0 + f'{alph_list[cipher_val]}'
                                i+=1
                                k=0
                            else:
                                k+=1
                        else:
                            str0 = str0 + cipher_list[i]
                            i+=1
                            k=0
                    decipher_file.write(str0)
                    print("Текст был успешно преобразован!")
                    flag1=False
                    break
            except Exception:
                print("Ошибка")

                                   
       
    def __read_cipher(self):
        cipher_file = open(self._open_cipher_text('шифр гаммирования'),'r', encoding='utf-8' )
        cipher_list = []
        i=0
        for line in cipher_file:
            if i < 1:
                i+=1
            else:
                cipher_list.extend(list(line))
        return cipher_list

    

            
#метод замены
class ReplacementMethod(MainClass):

    def gen_key(self, **kwargs):
        flag1 = True
        while flag1:
            key_filepath = self._made_file('key')    
            alph_list = self._open_alph()
            key_list = random.sample(alph_list, len(alph_list))
            try:
                with open(key_filepath, "x", encoding="utf-8") as key_file:
                    key_file.write('шифр замены\n')
                    i=0
                    while i < len(alph_list):
                        str0 = '\n' + alph_list[i] + ':' + key_list[i]
                        key_file.write(str0)
                        i+=1
                    flag1 =False
                    print("Ключ был успешно сохранен.")
                    break 
            except Exception:
                print("Возникла ошибка")

    def __read_key(self):
        key_filename = self._open_key('шифр замены')
        key_dict = {}
        with open(key_filename,'r', encoding='utf-8') as key_file:
            for line in key_file:
                if line[0] != '\n':
                    key_list = line.split(':',1)
                    if len(key_list) == 1:
                        pass
                    elif len(key_list) == 2:
                        key_dict[line[0]] = line[2]
        return key_dict

    def ciphering(self, **kwargs):
        key_dict = self.__read_key()
        text_list = self._open_text_file()
        flag = True
        while flag:
            try:
                cipher_path = self._made_file('encrypt')
                with open(cipher_path,'x', encoding='utf-8') as cipher_file:
                    cipher_file.write('шифр замены\n')
                    str0=''
                    for k in range(len(text_list)):
                        i=0 
                        for key, value in key_dict.items():
                            i+=1   
                            if text_list[k] == key: 
                                str0 = str0 + f'{value}'
                                break
                            elif i == len(key_dict):
                                str0 = str0 + f'{text_list[k]}'
                                break                      
                    cipher_file.write(str0)
                    print("Текст был успешно преобразован!")        
                flag = False
                break
            except Exception:
                print("Возникла ошибка")      

    def deciphering(self, **kwargs):
        key_dict = self.__read_key()
        cipher_list = self.__read_cipher()
        flag = True
        while flag:
            try:
                text_path = self._made_file('txt')
                with open(text_path,'x', encoding='utf-8') as text_file:
                    str0=''
                    for k in range(len(cipher_list)): 
                        i=0
                        for key, value in key_dict.items():
                            i+=1   
                            if cipher_list[k] == value:
                                str0 = str0 + f'{key}'
                                break
                            elif i == len(key_dict):
                                str0 = str0 + f'{cipher_list[k]}'
                                break          
                    text_file.write(str0)
                    print("Текст был успешно преобразован!")        
                flag=False
                break
            except Exception:
                print("Возникла ошибка")

    
    def __read_cipher(self):
        cipher_file = open(self._open_cipher_text('шифр замены'),'r', encoding='utf-8' )
        cipher_list = []
        i=0
        for line in cipher_file:
            if i<1:
                i+=1
            else:
                cipher_list.extend(list(line))
        return cipher_list   



move=TranspositionMethod()
gamma=GammaMethod()
replace=ReplacementMethod()



error=0
flag = True
while flag:
    flag2 = True
    try:
        print("Меню:")
        choice = int(input("\n1) Зашифровать\n2) Расшифровать\
            \n3) Сгенерировать ключ\n4) Выход из программы\nВаш выбор: "))
        
        if choice==1: 
            error=0     
            while flag2:
                choice1 = int(input("\nВыберите метод шифровки:\n1) Метод перестановки\
                    \n2) Метод гамирования\n3) Метод замены\n4)Назад в меню\nВаш выбор: "))
                if choice1 != 1 and choice1 != 2 and choice1 != 3 and choice1 != 4:
                    print("Ошибка ввода")
                    error+=1
                    if error > 2:
                        print("Совершены 3 ошибки ввода!Выполняю выход из программы...!")
                        flag = False
                        break
                elif choice1==4:
                    flag2==False
                    break
                if choice1==1:
                    move.ciphering()
                elif choice1==2:
                    gamma.ciphering() 
                elif choice1==3:
                    replace.ciphering()           

        elif choice==2:
            error=0    
            while flag2:
                choice1 = int(input("\nВыберите метод расшифровки:\n1) Метод перестановки\
                    \n2) Метод гамирования\n3) Метод замены\n4)Назад в меню\nВаш выбор: "))
                if choice1 != 1 and choice1 != 2 and choice1 != 3 and choice1 != 4:
                    print("Ошибка ввода")
                    error+=1
                    if error > 2:
                        print("Совершены 3 ошибки ввода!Выполняю выход из программы...!")
                        flag = False
                        break
                elif choice1==4:
                    flag2=False
                    break
                if choice1==1:
                    move.deciphering()
                elif choice1==2:
                    gamma.deciphering()
                elif choice1==3:
                    replace.deciphering()                 
                
        elif choice==3:
            print("Выполняется процедура генерации ключа...") 
            error=0    
            while flag2:
                choice1 = int(input("\nСгенерировать ключ для следующего алгоритма:\n1) Метод перестановки\
                    \n2) Метод гамирования \n3) Метод замены \n4)Назад в меню\nВаш выбор: "))
                if choice1 != 1 and choice1 != 2 and choice1 != 3 and choice1 != 4:
                    print("Ошибка ввода")
                    error+=1
                    if error > 2:
                        print("Совершены 3 ошибки ввода!Выполняю выход из программы...!")
                        flag = False
                        break
                elif choice1==4:
                    flag2==False
                    break     
                if choice1==1:
                    move.gen_key()    
                elif choice1==2:
                    gamma.gen_key()    
                elif choice1==3:
                    replace.gen_key()

        elif choice==4:
            flag==False
            break
        
        else:
            print("Ошибка ввода\n")
            error+=1
            if error > 2:
                print("Совершены 3 ошибки ввода!Выполняю выход из программы...!")
                flag = False
                break
    
    except SyntaxError:
        print("SyntaxError")
    except KeyboardInterrupt:
        pass
    except TypeError:
        print("TypeError")
    except UnboundLocalError:
        print("UnboundLocalError")
    except IndexError:
        print("IndexError")
    except ValueError:
        print("ValueError") 