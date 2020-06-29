import os
import math
from sys import argv
import multiprocessing as mp
import time
import timeit

def begin(verge: int):
    with mp.Pool(processes=3) as my_pool:
        p1 = my_pool.starmap(Atkin_alg,
                             iterable=[
                                       [verge, 1],
                                       [verge, 2],
                                       [verge, 3]
                                      ],
                             )
        my_pool.close()

def Atkin_alg(verge: int, pr1: int):
    if pr1 == 1:
        path = "Number_1.txt"
        status = "Прекращение первого процесса"
        i=1
    elif pr1 == 2:
        path = "Number_2.txt"
        status = "Прекращение второго процесса"      
        i=2
    elif pr1 == 3:
        path = "Number_3.txt"
        status = "Прекращение третьего процесса"        
        i=3
    resh = [False] * (verge+1)
    
    t=time.time()
    t=int(t)
    for x in range(i, int(math.sqrt(verge)) + 1, 3):
        for y in range(1, int(math.sqrt(verge)) + 1):           
            n = 4 * x ** 2 + y ** 2
            if n <= verge and (n % 12 == 1 or n % 12 == 5):
                resh[n] = not resh[n]
            n = 3 * x ** 2 + y ** 2
            if n <= verge and n % 12 == 7:
                resh[n] = not resh[n]
            n = 3 * x ** 2 - y ** 2
            if x > y and n <= verge and n % 12 == 11:
                resh[n] = not resh[n]
            if int(time.time())-t>6:
                print(x)
                t=time.time()
                t=int(t)           
    with open(path, "w", encoding='utf-7') as file_alg:
        for id, x in enumerate(resh):            
            string = str(x) + '\n'
            file_alg.write(string)
    print(status + '\n')


def file_reader()->list:
    print("чтение первого файла")
    with open('Number_1.txt','r',encoding='utf-8') as file_1:
        first_read = file_1.read()
        list_1 = first_read.split("\n")
    print("чтение второго файла")
    with open('Number_2.txt','r',encoding='utf-8') as file_2:
            first_read = file_2.read()
            list_2 = first_read.split("\n")
    print("чтение третьего файла")
    with open('Number_3.txt','r',encoding='utf-8') as file_3:
        first_read = file_3.read()
        list_3 = first_read.split("\n")
    list_unity=[False]*len(list_3)
    lens=len(list_3)
    for i in range(0,lens):
        if list_1[i]=="False":
            z=False
        else: z=True
        if list_2[i]=="False":
            zx=False
        else: zx=True
        if list_3[i]=="False":
            xz=False
        else: xz=True
        list_unity[i]=(z+zx+xz)%2
    list_fin=[False]*len(list_unity)
    for id,x in enumerate(list_unity):
        if x==1:
            if id%5==0:
                pass
            else:
                list_fin[id]=id
    for x in range(5, int(math.sqrt(len(list_unity)))):
        if list_fin[x]:
            for y in range(x ** 2, verge + 1, x ** 2):
                list_fin[y] = False
    return list_fin


if __name__ == '__main__':
    try:
        if int(argv[1]) > 0:
            pass
        elif int(argv[1]) < 0:
            raise Exception
        elif int(argv[1]) == 0:
            raise Exception
        else:
            raise Exception
        verge = int(argv[1])
        a = timeit.default_timer()
        begin(verge)
        time_list = file_reader()
        while len(time_list)>verge:
            time_list.pop()
        res=list()
        for index,elem in enumerate(time_list):
            if elem is not False:
                res.append(elem)
        res.sort()
        with open("final.txt", "w", encoding='utf-8') as file:
            file.write("2\n3\n5\n")
            for p in res:
                string = ""+str(p)+"\n"
                file.write(string)
        print("Время выполнения алгоритма:", timeit.default_timer()-a, "секунд\n")
    except Exception:
        print("Ошибка ввода")
    except BaseException:
        print("Выход из программы...")
    except FileNotFoundError:
        pass