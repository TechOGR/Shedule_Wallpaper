from winshell import recycle_bin
from os.path import (
    join,
    basename,
    abspath
)
from ctypes import (
    windll,
    c_ulong,
    c_ulonglong,
    sizeof,
    byref,
    Structure
)
import math

class RecycleBin:
    
    def __init__(self):
        self.initComponents()
    
    class rb_info(Structure):

        _fields_ = [
            ('cbSize', c_ulong),
            ('i64Size', c_ulonglong),
            ('i64NumItems', c_ulonglong)
        ]
        
    def initComponents(self):
        
        self.shell32 = windll.shell32
        self.query_recycleBin = self.shell32.SHQueryRecycleBinW
        
        self.info = self.rb_info()
        self.info.cbSize = sizeof(self.info)
        
        self.result = self.query_recycleBin(None, byref(self.info))
        
    def getNumFiles(self):
        self.info = self.rb_info()
        self.info.cbSize = sizeof(self.info)
        
        self.result = self.query_recycleBin(None, byref(self.info))
        
        if self.result == 0:
            size = f"{math.floor(self.info.i64Size / (1024 * 1024))}"
            numFiles = self.info.i64NumItems
            if self.info.i64NumItems > 0:
                return (numFiles, size, 'Full');
            else:
                return(numFiles, size, 'Empty')
        else:
            return "Error"
            
    def getPropertiesFile(self):
        
        rb = recycle_bin()
        fullName = []
        names = []
        paths = []
        for deletedFile in rb:
            fullName.append(deletedFile.original_filename())
        
        for item in fullName:
            names.append(basename(item))
            paths.append(abspath(item))
        
        print(names, paths)
        
        return (names, paths)
    
    def emptyTrash(self):
        rb = recycle_bin()
        if self.info.i64NumItems > 0:
            rb.empty(confirm=False)

            return 'Vaciada'
        else:
            return 'Está vacía'
    
    def restoreFile(self, path):
        from winshell import undelete
        try:
            undelete(path)
            return 'Restaurado'
        except Exception as e:
            return f'Error: {str(e)}'
