from urllib.request import urlopen
import json
import time

with open('airline_list.json', 'r') as lots_of_airlines:
    airline_list = json.load(lots_of_airlines)

organized_airline = {}

for airline in airline_list:
    if airline['country'] == 'United States' or airline['country'] == 'Mexico':
        if airline['icao'] != '':
            organized_airline[airline['icao']] = airline['name']
# print(organized_airline)

url = "http://adsb.sirver.co:2222/tar1090/data/aircraft.json"

airplane = {}
loop_count = 0
primary_key = 'Hex'

while loop_count < 20:
    first_response = urlopen(url)
    second_response = first_response.read()
    json_data = json.loads(second_response)

    for data in json_data['aircraft']:
        if {'flight', 'hex', 'alt_baro', 'lat', 'lon', 'gs'} <= data.keys():
            # print(data['flight'], data['hex'])
            spaced_flight_number = str(data['flight'])
            flight_number = spaced_flight_number.replace(' ', '')

            airline_name = 'Unknown'
            potential_icao = flight_number[0:3]
            if potential_icao in organized_airline:
                airline_name = organized_airline[potential_icao]

            hex = data['hex']
            altitude = data['alt_baro']
            latitude = data['lat']
            longitude = data['lon']
            ground_speed = data['gs']

            airplane[hex] = {'Name': airline_name, 'Flight': flight_number, 'Altitude': altitude, 'Latitude': latitude, 'Longitude': longitude, 'Ground Speed': ground_speed}

            # for witch in airplane:
            #     if witch[primary_key] == dict[primary_key]:
            #         print(f'Value exists: {dict}')
            #     else:
            #         airplane.append(dict)
    loop_count += 1
    time.sleep(5)
            # print(hex)
            # airplane.append(flight_number)

# print(airplane)

# print(airplane[list(airplane.keys())[1]])

# create json object from the stored adsb list
json_object = json.dumps(airplane, indent=1)

# create the json file from the object
with open("flights.json", "w") as outfile:
   outfile.write(json_object)

def countoccurrences(store, value):
    try:
        store[value] = store[value] + 1
    except KeyError as e:
        store[value] = 1
    return

store = {}
for hex in airplane:
    a = airplane[hex]['Name']
    countoccurrences(store, a)

# print(store)

storted = sorted(store.items(), key=lambda x:x[1])
airlines_seen = dict(storted)
print(airlines_seen)

# dict = {'Southwest': Southwest, 'Delta': Delta, 'Frontier': Frontier, 'American': American, 'Other': Other}
# airlines.append(dict)
#
# print(airlines)
# # print(f'Southwest:{Southwest} \nAmerican:{American} \nDelta:{American} \nOther:{Other} \nFrontier:{Frontier}')
#
another_json_object = json.dumps(airlines_seen, indent=1)

# create the json file from the object
with open('airlines.json', 'w') as outfile:
    outfile.write(another_json_object)