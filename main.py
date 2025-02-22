#dependencies
from urllib.request import urlopen
import json
import time

#the dictionary where each plane's data will be added with hex codes as the key
airplane = {}

#url that has an airline .json that updates every couple seconds
url = "http://planes.dirtroads.us:2222"

#opens the .json that contains all known registration details associated with all known hex codes
with open('aircrafts.json', 'r') as g:
    plane_regs = json.load(g)

#.json for just a small subset of airlines that are relevant to this project
with open('limited_airlines.json', 'r') as b:
    airlines_short = json.load(b)

# .json that contains the details of aircrafts and military tag based on the 3 letter aircraft tag in aircrafts.json
with open('types.json', 'r') as h:
    craft_type = json.load(h)


def fetch_and_process_data():
    #open the self hosted .json from antenna
    try:
        open_url = urlopen(url)
        read_url = open_url.read()
        read_json = json.loads(read_url)
    except Exception as e:
        print(f"Error fetching or parsing data: {e}")
        exit()\

    for data in read_json['aircraft']:
        if {'flight', 'hex', 'alt_baro', 'lat', 'lon', 'gs'} <= data.keys():
            spaced_flight_number = str(data['flight'])
            flight_number = spaced_flight_number.replace(' ', '')

            airline_name = 'Other'
            potential_icao = flight_number[0:3]
            if potential_icao in airlines_short:
                airline_name = airlines_short[potential_icao]

            hex_code = data['hex'].upper()
            altitude = data['alt_baro']
            latitude = data['lat']
            longitude = data['lon']
            ground_speed = data['gs']

            tail_number = plane_regs.get(hex_code, ['not found'])[0]
            craft_info = plane_regs.get(hex_code, ['not found','not found','not found'])  # Default to a list with at least two items

            # Check if the list has a second element (the aircraft model)
            if len(craft_info) > 1 and craft_info[1] != 'not found':
                aircraft_model = craft_info[1]  # Assign the model if available
            else:
                aircraft_model = 'unknown'  # If not found or only one element, set to 'unknown'

            detailed_craft = craft_type.get(aircraft_model, ['not found'])[0]

            military = plane_regs.get(hex_code, ['not found','not found','not found'])
            if len(military) > 1 and military[2] != 'not found':
                military_status = military[2]  # Assign the model if available
            else:
                military_status = 'unknown'

            military_tag = 'unknown'
            if military_status == '10':
                military_tag = "Yes"
            else:
                military_tag = "No"

            if tail_number != 'not found':
                airplane[hex_code] = {'Tail Number': tail_number, 'Airline': airline_name, 'Flight': flight_number, 'Altitude': altitude, 'Latitude': latitude,
                             'Longitude': longitude, 'Ground Speed': ground_speed, 'Aircraft Model': detailed_craft, 'Military': military_tag}

    output_file = 'processed_airplane_data.json'
    try:
        with open(output_file, 'w') as outfile:
            json.dump(airplane, outfile, indent=4)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving data: {e}")
while True:
    fetch_and_process_data()
    time.sleep(30)  # Sleep for 15 seconds before running again