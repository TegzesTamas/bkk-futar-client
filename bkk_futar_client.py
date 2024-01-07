#!/usr/bin/env python3

from ast import List
from time import localtime, mktime, strftime
import requests
import pprint

from bkk_futar_client.consts import apikey, stopId


def arrivalMinutes(apikey: str = apikey, stopId: str = stopId, maxDepartures: int = 10, minsBefore: int = 0, minsAfter: int = 90, debug: bool = False) -> list[float]:

    request_url :str = f'https://futar.bkk.hu/api/query/v1/ws/otp/api/where/arrivals-and-departures-for-stop.json?key={apikey}&version=3&includeReferences=false&stopId={stopId}&onlyDepartures=true&limit={maxDepartures}&minutesBefore={minsBefore}&minutesAfter={minsAfter}'

    if (debug):
        print(f'Requesting from: {request_url}')
    response = requests.get(request_url)
    if (debug):
        print(f'status: {response.status_code}')

    json = response.json()
    stopTimes = json['data']['entry']['stopTimes']
    currentTimePython = mktime(localtime())
    if (debug):
        print()
        print('--- JSON ---')
        print()
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(json)
        print()
        print('------------')
        print()

    minutes : list[float] = [((stopTime['departureTime'] - currentTimePython)/60) for stopTime in stopTimes]
    
    if (debug):
        print('Arrival minutes')
        for minute in minutes:
            print(f"{minute} mins")
    return minutes


if __name__ == "__main__":
    print()
    print()
    print("---------------------------------------------------------------------")
    print(strftime('%Y-%m-%d %H:%M:%S'))
    print()
    print()
    arrivalMinutes(apikey, stopId, 5, 1, 60, True)
    print("---------------------------------------------------------------------")
    print()
