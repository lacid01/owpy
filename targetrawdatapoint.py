from dbhelper import getCityTable
import pandas as pd



class datapointtarget:
    """
    Speichert die Orte in die in EnEffCo geschrieben werden soll
    """

    @staticmethod
    def get_cities():
        ctytable = pd.DataFrame.from_records(getCityTable())
        ctytable.columns = ['FKID','ID','Name','lat','lon','Zeige in Visu']
        return ctytable