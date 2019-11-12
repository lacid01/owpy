
class datapointtarget:
    """
    Speichert die Orte in die in EnEffCo geschrieben werden soll
    """

    @staticmethod
    def get_sbrg():
        body =	{
            "ID": "sbrg",
            "lat": 52.482626,
            "lon": 13.357410,
            "temperature": "4b6d3ae2-054a-4fe7-bf44-43b66105e1d4",
            "humidity": "657014cf-e0cd-42db-a90d-ea2844563e1c",
            "pressure": "bc4a90b7-bcda-4e55-863a-5ff922075537",
            "windspeed": "691d4e72-e21b-4979-96fd-c9c1ef3342a9",
            "winddegree": "66095594-7126-4d44-ae93-dd130b4bcf79"
            }
        return body

        
    @staticmethod
    def get_nb():
        body =	{
            "ID": "nb",
            "lat": 55.057659,
            "lon": 9.744552,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

        
    @staticmethod
    def get_osl():
        body =	{
            "ID": "osl",
            "lat": 59.918443,
            "lon": 10.767229,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

        
    @staticmethod
    def get_ntwrpn():
        body =	{
            "ID": "ntwrpn",
            "lat": 51.209683,
            "lon": 4.411001,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

        
    @staticmethod
    def get_stckhlm():
        body =	{
            "ID": "stckhlm",
            "lat": 59.33364,
            "lon": 18.048404,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

        
    @staticmethod
    def get_wkfhr():
        body =	{
            "ID": "wkfhr",
            "lat": 54.694487,
            "lon": 8.571797,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

    

        
    @staticmethod
    def get_sndrbrg():
        body =	{
            "ID": "sndbrg",
            "lat": 54.924556,
            "lon": 9.781041,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body
        
    @staticmethod
    def get_sttl():
        body =	{
            "ID": "sttl",
            "lat": 47.600357,
            "lon": -122.323153,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

    @staticmethod
    def get_bsslke():
        body =	{
            "ID": "bsslke",
            "lat": 37.336777,
            "lon": -119.578894,
            "temperature": "Mustang",
            "humidity": "Mustang",
            "pressure": "Mustang",
            "windspeed": "Mustang",
            "winddegree": "Mustang"
            }
        return body

    @staticmethod
    def get_cities():
        cts = [
            datapointtarget.get_sbrg(),
            datapointtarget.get_nb(),
            datapointtarget.get_ntwrpn(),
            datapointtarget.get_osl(),
            datapointtarget.get_sndrbrg(),
            datapointtarget.get_stckhlm(),
            datapointtarget.get_wkfhr(),
            datapointtarget.get_sttl(),
            datapointtarget.get_bsslke()
        ]
        return cts