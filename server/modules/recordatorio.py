import pyttsx3 as ttx

import datetime

from pandas import (
    read_excel
)

from os.path import (
    join
)
from os import environ

from threading import Thread
from time import sleep

def sayIntro():
    bot_audio = ttx.init()
    bot_audio.setProperty('rate', 160)
    bot_audio.setProperty('volume', 1)
    bot_audio.setProperty('voice', 0)
    
    texto = "Bienvenido al centro de aquí mismo, Gracias por usar esta tareca"
    
    bot_audio.say(texto, "Esto")
    bot_audio.runAndWait()

def calendar():
    
    current_date_hour = datetime.datetime.now()

    # print(current_date_hour.hour)
    # print(current_date_hour.minute)
    
    return (current_date_hour.hour, current_date_hour.minute)
    

def setDaysDateFromExel():
    path_file_excel = join("D:/","Programacion", "Repositorios_Git","Shedule_Wallpaper","src", "documents", "Horario.xlsx")
    workbook = read_excel(path_file_excel)
    days_hours = workbook.columns
    values = workbook.values
    days = {}
    asign = []
    for i in range(1, len(days_hours)):
        for j in range(len(values)):
            asign.append(values[j][i])
        
    counter = 0
    for t in range(1, len(days_hours)):
        lista = []
        for i in range(1, 12):
            lista.append(asign[counter])
            counter+=1
        days[days_hours[t]] = lista
    print(days['Monday'])
        
    # print(days)

def get_currentDay():
    today = datetime.datetime.today()
    name_today = today.strftime("%A")
    
    if name_today == 'Monday':
        day = ["Lunes",1]
        return day
    elif name_today == 'Tuesday':
        return 2
    elif name_today == 'Wednesday':
        return 3
    elif name_today == 'Thursday':
        return 4
    elif name_today == 'Friday':
        return 5
    elif name_today == 'Saturday':
        return 6
    elif name_today == 'Sunday':
        return 7
    
def getDataExcel():
    path_file_excel = join("D:/","Programacion", "Repositorios_Git","Shedule_Wallpaper","src", "documents", "Horario.xlsx")
    workbook = read_excel(path_file_excel)
    columns = workbook.columns
    values = workbook.values
    
    days_of_week = list(columns[1:])
    
    num_day = get_currentDay()
    print(f"Today is: {num_day[0]}")

    # Getting subjects of current day    
    subjects_days = []
    for i in range(0, len(values)):
        subjects_days.append(values[i][num_day[1]])
    
    # print(days_of_week, subjects_days)
    
    
    list_horarios = []
    for v in values:
        list_horarios.append(v[0])
    # print(list_horarios)
    
    dict_hour_subjects = {}
    for i in range(0, len(list_horarios)):
        dict_hour_subjects[list_horarios[i]] = subjects_days[i]
    print(dict_hour_subjects)
    
    hour, minute = calendar()
    print(hour, minute)

    for hours in list_horarios:
        hours_range = hours.strip()
        if hours_range.startswith(str(hour)):
            print("Sepalo")
            
    def checking_next_subject():
        while True:
            count = 0
            sleep(10)
            for hours in list_horarios:
                count += 1
                hours_range = hours.strip()
                if hours_range.startswith(str(hour)):
                    say_depends_cheduler(hours_range, subjects_days[count -1], num_day[0])
                    
    hilo = Thread(target=checking_next_subject)
    hilo.daemon = True
    hilo.run()


def say_depends_cheduler(hour_, subjects_, day_):
    
    audio = ttx.init()
    audio.setProperty("rate", 130)
    audio.setProperty("volume", 1)
    audio.setProperty("voice", 0)
    username = environ["USERNAME"]
    print(username)
    text = f"""
    Hola de nuevo idiota, estúpido, pájaro de mal ajuero, 
    ya no se como decirte, en fin, {username}, 
    estoy aquí nuevamente para decirte que hoy es {day_}
    y tienes {subjects_} ahora desde las {str(hour_)}"""
    
    audio.say(text)
    audio.runAndWait()

# sayIntro()
getDataExcel()
# calendar()
# setDaysDateFromExel()