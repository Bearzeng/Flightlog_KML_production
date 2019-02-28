"""_________________________________________________________________________

Scripte takes Reigal output CSV file and produces KML ad text file of flight lines

Inset into same folder as RIEGL flight log report, change file name below to required CSV and run script.
This will produce a text file and a KML of the flight line data, including line number and altitude.

Paul Vidler 16/11/2018


_________________________________________________________________________"""


import csv
import simplekml
import os
import subprocess


def take_deg(arg1):
    var1 = arg1.replace("deg", "")
    var2 = float(var1)
    return var2

class FlightLine:

    def __init__(self, description, flight_num,
                 start_lat, start_long, end_lat, end_long, altitude):

        self.description = description
        self.flight_num = flight_num
        self.start_lat = start_lat
        self.start_long = start_long
        self.end_lat = end_lat
        self.end_long = end_long
        self.altitude = altitude

    def show_all(self):

        print("Flight line number: {}".format(self.flight_num))
        print("Description: {}".format(self.description))
        print("Start latitude: {}".format(self.start_lat))
        print("Start longitude: {}".format(self.start_long))
        print("End latitude: {}".format(self.end_lat))
        print("End longitude: {}".format(self.end_long))
        print("Altitude: {}".format(self.altitude))

    def make_dict(self):

        {"Description" : self.description, "Flight line number": self.flight_num,
         "Start longitude" : self.start_long, "Start latitude" : self.start_lat,
         "End latitude" : self.end_lat, "End longitude" : self.end_long, "Altitude" : self.altitude }

    def make_txtprint(self):
        txt = ''
        txt = txt + '\nFlightnum={0}'.format(self.flight_num)
        txt = txt + '\nDescription={0}'.format(self.description)
        txt = txt + '\n{0} {1} {2} '.format(self.start_long, self.start_lat, float(self.altitude.replace('m', "")))
        txt = txt + '\n{0} {1} {2}\n '.format(self.end_long, self.end_lat, float(self.altitude.replace('m', "")))
        return txt

    def make_kml(self, altitude, description, start_lat, start_long, end_lat, end_long):

        ls = kml.newlinestring(name=self.description)
        ls.coords = [(self.start_long,self.start_lat, self.altitude), (self.end_long,self.end_lat, self.altitude)]
        ls.style.linestyle.width = 5
        ls.style.linestyle.color = simplekml.Color.blue
        ls.altitudemode = simplekml.AltitudeMode.relativetoground






counter = 1


# Get CWD and finds file with .CSV extension to be open
file_list = os.listdir()
cur_dir = os.getcwd()
csv1 = []
flight_name = ''

for file in file_list:
    if file.endswith(".csv"):
        csv1.append(file)



csv2 = csv1[0]


# Checks for one than one CSV file in directory. Exits if found.
if len(csv1) > 1:
	print("More than one CSV file detected. Please ensure only one CSV is in the directory")
	print(csv1)
	os.system("pause")
	exit()

flight_name = (csv1[0])
flight_name = flight_name[:-4]


os.system("pause")


# open and read csv file
with open(csv2, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # create list to add class instance values
    flightlines = []

    #create KML file
    kml = simplekml.Kml()

    # loop through and find all start and end tags and write to a CSV
    for line in csv_reader:
        if "|START|" in line:
            # create list "start_key" of header
            start_key = [(next(csv_reader))]
            # create list "start_value" of values
            start_value = [(next(csv_reader))]
            #print(start_key)
            #print(start_value)
        elif "|END|" in line:
            # create list "end_value" of values
            end_key = [(next(csv_reader))]
            end_value = [(next(csv_reader))]
            # new list variables to get out of nested list
            new_start_value = start_value[-1]
            new_end_value = end_value[-1]
            line = FlightLine(new_start_value[1], counter, take_deg(new_start_value[3]), take_deg(new_start_value[4]),
                              take_deg(new_end_value[3]), take_deg(new_end_value[4]), new_end_value[5])

            #line.show_all()
            # add coords/line to kml file
            line.make_kml(line.altitude, line.description, line.start_long, line.start_lat, line.end_long, line.end_lat)
            counter += 1
            flightlines.append(line)

    # Save KML file under flight name

    #save KML file
    kml.save(flight_name + ".kml")

    #open a text file and save lines in "flightlines[]"
    text_file = open(flight_name + "_output.txt", "a")

    for line in flightlines:
        text_file.write(line.make_txtprint())


    #close the files
    text_file.close()
