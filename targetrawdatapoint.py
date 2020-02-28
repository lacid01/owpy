from dbhelper import getCityTable
import pandas as pd


def get_cities():
        ctytable = pd.DataFrame.from_records(getCityTable())
        ctytable.columns = ['FKID','ID','Name','lat','lon','Zeige in Visu']
        return ctytable