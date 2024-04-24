import pyttsx3 as ttx

import datetime

from pandas import (
    read_excel
)

from os.path import (
    join
)

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

def getDataExcel():
    path_file_excel = join("D:/","Programacion", "Repositorios_Git","Shedule_Wallpaper","src", "documents", "Horario.xlsx")
    workbook = read_excel(path_file_excel)
    values = workbook.columns
    list_horarios = []
    for v in values:
        list_horarios.append(v)
    # print(list_horarios)
    
    hour, minute = calendar()
    
    for h in list_horarios:
        if h[0:2] == str(hour):
            print(f"Son las {hour} y te toca estudiar algo")
        else:
            continue
    
# sayIntro()
    
getDataExcel()
calendar()
setDaysDateFromExel()