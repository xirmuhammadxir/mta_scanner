# — coding: utf-8 —
import platform
import os
import subprocess
import datetime
import shlex


def data():
    print("System information: ")
    print('System :', platform.system())  # Отображение названия системы / ОС
    print('Distribution :', platform.platform())  # Показать название ОС, версию и кодовое имя
    print(platform.architecture())  # Показать архитектуру машины
    print('Node :', platform.node())  # Показать имя компьютера в сети
    print('Machine :', platform.machine())  # Показать тип машины
    print('Processor :', platform.processor())  # Показать имя процессора
    print('Version :', platform.version())  # Показать версию системы
    print('Platform :', platform.platform())  # Показать базовую платформу
    print('Release :', platform.release())  # Показать информацию о выпуске системы


def installed():
    dpkg_list = shlex.split("dpkg-query -Wf '${Installed-Size}\t${Package}\n'")
    process = subprocess.Popen(dpkg_list, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("List installed application: ")
    print(output.decode('UTF-8'))

    
def check():
    check_diff = shlex.split("diff backup_1.txt backup_2.txt")
    process = subprocess.Popen(check_diff, stdout=subprocess.PIPE)
    output, error = process.communicate()
    print("List of changes: ")
    print(output.decode('UTF-8'))
    
    
def change(input_file, output_file):
    with open(input_file, 'r') as in_file, open(output_file, 'w') as out_file:
        for line in in_file:
            out_file.write(line)
        os.remove(input_file)

        
def last_time():
    if os.path.exists("backup_1.txt"):
        with open('backup_1.txt') as f:
            last_time = f.readline()
    else:
        last_time="Сканирование ни разу не проводилось"
    return last_time

def new_scan():
    if os.path.exists("backup_1.txt"): #Если есть предыдущий скан
        sys.stdout = open("backup_2.txt", "w") #Запись в временный файл
        print(datetime.datetime.now().strftime('%Y-%m-%d__%H:%M:%S')) #Первая строчка - время
        data() #Сведения о системе
        installed() #Установленные пакеты
        sys.stdout.close()

        sys.stdout = open("differents.txt", "w")
        check() #Сравнение временного файла и последнего сканирования. Запись различия в файл different.txt
        sys.stdout.close()

        if not os.path.exists("Backups"): #Проверка на существование директории для резервного хранения
            os.mkdir(os.getcwd()+"/Backups/") #Создание директории для резервного хранения
        cwd = os.getcwd()+"/Backups/"
        change("backup_1.txt", cwd + datetime.datetime.now().strftime('%Y-%m-%d__%H:%M:%S')) #Копирование предыдущего скана в резервное хранилище
        change("backup_2.txt", "backup_1.txt") #Копирование временного файла в основной

    else:# Если предыдущего скана нет
        sys.stdout = open("backup_1.txt", "w")
        print(datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')) #Запись в новый файл
        data()
        installed()
        sys.stdout.close()

        sys.stdout = open("differents.txt", "w")
        print("Не найдено последних проверок")
        sys.stdout.close()
    
    
def open_scan():
    new_scan() #Сканирование
    filepath = os.getcwd()+"/backup_1.txt" #Адрес файла
    txt_edit.delete("1.0", tk.END) #Очистить поле
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text) #Запись из файла
    window.title(f"MTA Scanner - {filepath}")
    last_scan_2 = tk.Label(fr_buttons, text=last_time())
    last_scan_2.grid(row=7, column=0, sticky="ew", padx=5)
    
    
def open_diff():
    filepath = os.getcwd()+"/differents.txt" #Адрес файла
    txt_edit.delete("1.0", tk.END) #Очистить поле
    with open(filepath, "r") as input_file:
        text = input_file.read()
        txt_edit.insert(tk.END, text) #Запись из файла
    window.title(f"MTA Scanner - {filepath}")
