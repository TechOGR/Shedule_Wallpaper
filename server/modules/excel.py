from pandas import read_excel as re
from os.path import join


class Horario:

    def __init__(self, full_path_project, filename="Horario.xlsx"):
        self.full_main_path = full_path_project
        self.path_file_exel = join(self.full_main_path, "data", "documents", filename)
        self.setHorarios()

    def HeadTable(self):
        page = re(self.path_file_exel)
        columns = page.columns.tolist()
        return columns

    def RowsValues(self):
        page = re(self.path_file_exel)
        row_values = page.values.tolist()
        return row_values

    def setHorarios(self):
        self.horarios = {
            "head_table": self.HeadTable(),
            "rows_values": self.RowsValues()
        }

    def getHorario(self):
        return self.horarios
