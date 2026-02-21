from winotify import (
    Notification,
    audio
)
from pandas import read_excel as re
import datetime
from os.path import (
    join
)
from os import (
    system
)

class Horario:
    
    def __init__(self, full_path_project, filename="Horario.xlsx") -> None:
        self.full_main_path = full_path_project
        self.path_file_exel = join(self.full_main_path, "src", "documents", filename)
        self.setHorarios()
    
    def HeadTable(self):
        path_exel = self.path_file_exel
        page = re(path_exel)
        columns = page.columns.tolist()
        
        return columns

    def RowsValues(self):
        path_exel = self.path_file_exel
        page = re(path_exel)
        row_values = page.values.tolist()
        
        return row_values
    
    def setHorarios(self):
        self.horarios = {
            "head_table": self.HeadTable(),
            "rows_values": self.RowsValues()
        }
    
    def getHorario(self):
        return self.horarios
        
    def knowHours(self):
        day_month = datetime.datetime.now()
        
        minutes = day_month.minute
        system(f"msg * {self.horarios}")
        if minutes == 6:
            # self.createNotification(f"Es hora de estudiar: {self.horarios["8:00 - 9:00"]}")
            pass

    def createNotification(self,_mensaje):
        notification = Notification(
            app_id="Horario",
            title="Aviso que se está Avisando",
            msg=f"{_mensaje}",
            icon="",
            duration='long'
        )
        notification.set_audio(audio.LoopingAlarm, loop=True)
        notification.show()
        
if __name__ == "__main__":
    h = Horario()
    h.knowHours()