from os.path import (
    join,
    exists
)
from pathlib import (
    Path
)
from os import (
    getcwd,
)


class Configuration:
    
    def __init__(self, full_path_):
        self.pathEngine = Path()
        self.full_path = full_path_
        self.path_config_file = join(self.full_path, "src", "documents", "config.txt")        


    # Function for get data from Config_File
    def getFileConfig(self): 
    
        status_file = self.checkIfExist()
        
        match status_file:
            case True:
                try:
                    file_readed = open(self.path_config_file, "r").read()
                except [ FileNotFoundError, FileExistsError ]:
                    print("Error leyendo el archivo de configuración")
            case False:
                with open(self.path_config_file, 'w') as file:
                    file.write("")
                    file.close()
            
    def checkIfExist(self):

        if exists(self.path_config_file):
            return True
        else:
            return False       
        
if __name__ == "__main__":
    class_config = Configuration(getcwd())
    class_config.checkIfExist()