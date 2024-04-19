import pyttsx3 as ttx

from pandas import (
    read_excel
)

from os.path import (
    join
)

def getDataExcel():
    path_file_excel = join("D:/","Programacion", "Repositorios_Git","Shedule_Wallpaper","src", "documents", "Horario.xlsx")
    workbook = read_excel(path_file_excel)
    values = workbook.values
    list_horarios = []
    for v in values:
        list_horarios.append(v[0])
    print(list_horarios)
    
getDataExcel()