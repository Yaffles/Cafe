from Database import Database
from datetime import datetime

class SPXCafe(Database):
    """Wrapper class around database for spxcafe"""

    def __init__(self) -> None:
        self.__dbname = "spxcafecopy.db"
        super().__init__(self.__dbname)
    
    def getToday(self):
        return datetime.now().strftime("%Y-%m-%d")