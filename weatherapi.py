import requests
import matplotlib.pyplot as plt
import json
url = "http://api.openweathermap.org/data/2.5/onecall"
tokken = "2cce50cfca08d716b19f19de207fcca8"
all_datas = {}
city_lat_lon = {'tehran':[35.68,51.42], 'esfahan':[32.6539,51.6660], 'mashhad':[36.2605,59.6168]}

def make_query_for_lat_lon(lat, lon):
    return {"lat":lat, "lon":lon,"appid":tokken,"exclude":"daily, minutely", "units":"metric"}


class weather_situation(object):
    def __init__(self, response):
        self.__dict__ = json.loads(response)
        self.make_data_to_plot()
    def make_data_to_plot(self):
        for key, val in self.__dict__['current'].items():
            if key=='weather':
                    continue
            if key not in all_datas:
                all_datas[key] = [val]
            else:
                all_datas[key].append(val)
        for i in self.__dict__['hourly']:
            for key, val in i.items():
                if key=='weather' or key=='visibility' or key=='clouds':
                    continue
                if key not in all_datas:
                    all_datas[key] = [val]
                else:
                    all_datas[key].append(val)
    def time_zone(self):
        return self.__dict__['timezone']
if __name__ == "__main__":
    while(1):
        print("we can only find city name included: tehran, esfahan, mashhad. for rest of city enter lat and lon of them")
        state = input("if you want weather by city name enter 1 and if you want weather by lat & lon enter 2 and for exit enter e:")
        if state == 'e':
            break
        if state == '1':
            city_name = input("enter city name:")
            lat, lon = city_lat_lon[city_name]
            query_string = make_query_for_lat_lon(lat, lon)
        else:
            lat, lon = input("enter lat and lon:").split()
            query_string = make_query_for_lat_lon(lat, lon)

        response = requests.request("GET", url, params=query_string)
        data = weather_situation(response.text)

        parameter_to_plot = ['humidity', 'feels_like', 'temp']
        for i in parameter_to_plot:
            plt.plot(all_datas[i],'ro' )
            plt.plot(all_datas[i] )
            plt.xlabel('next hours')
            plt.ylabel(i)
            plt.title('time zone:'+data.time_zone())
            plt.show()

        all_datas.clear()


