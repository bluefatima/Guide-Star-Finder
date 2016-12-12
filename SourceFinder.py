
from PyAstronomy import pyasl
import csv
from astroquery.simbad import Simbad
from astropy import coordinates
import astropy.units as u
from astropy.coordinates import SkyCoord
from astropy.table import Table
from Guide_Star_Functions import angnorm, J2000, locsidtime, airmass2alt

##Read in TGAS data to query
data = []    
for i in range(16):
    if i < 10:
        filename = "TGAS/TgasSource_000-000-00" + str(i) +".csv"
    else: 
        filename = "TGAS/TgasSource_000-000-0" + str(i) +".csv"
    f = open(filename, 'r')
    reader = csv.reader(f)
    for row in reader:
        if 'ra' not in row:
            data.append([row[1], row[6], row[8], row[12], row[14], row[53]])

##Reads in variables from input file

with open('input.txt', 'r') as f:
    read_data = f.read()
a = read_data.split("\n")
LAT = float((a[2].split("= ")[1].split(" ")[0]))
LON = float((a[3].split("= ")[1].split(" ")[0]))
TimeZone = float((a[4].split("= ")[1].split(" ")[0]))
year = float((a[8].split("= ")[1].split(" ")[0]))
month = float((a[9].split("= ")[1].split(" ")[0]))
day = float((a[10].split("= ")[1].split(" ")[0]))
loc_hour = float((a[11].split("= ")[1].split(" ")[0]))
loc_minute = float((a[12].split("= ")[1].split(" ")[0]))
max_X = float((a[16].split("= ")[1].split(" ")[0]))
max_g_mag = float((a[17].split("= ")[1].split(" ")[0]))
output_file_name = ((a[19].split("= ")[1].split(" ")[0]))

##########################################################


#Calculates RA, Dec, and search radius for location/time/airmass 
UT_hour = loc_hour - TimeZone
if UT_hour >=24:
    UT_hour -= 24
    day += 1    
d = J2000(year, month, day, UT_hour, loc_minute)
UT = UT_hour + (loc_minute / 60)
LST = locsidtime(d, LON, UT)
z = airmass2alt(max_X) 

#Queries TGAS for stars that fit above parameters
search = []
for star in data:
    if ((float(star[1])-LST)**2 + (float(star[2])-LAT)**2) < z and float(star[5])<max_g_mag:
        search.append(star)
        
#Query Simbad for magnitudes and spectral data, organizes it with TGAS data
final_list = [] 
labels = ["ID", "RA", "Dec", "RA_pm", "Dec_pm", "B_mag", "V_mag", "g_mag", "Spec_Type"]

for i in range(len(search)):
    sexa = pyasl.coordsDegToSexa(float(search[i][1]), float(search[i][2])) #convert to sexagesimal
    c = SkyCoord(sexa, unit=(u.hourangle, u.deg))
    r = 5 * u.arcsecond
    customSimbad = Simbad()
    customSimbad.add_votable_fields('sptype', 'flux(B)', 'flux(V)')
    customSimbad.remove_votable_fields('coordinates')
    result_table = customSimbad.query_region(c, radius=r)
    
    main_id = (result_table[0]['MAIN_ID']).decode("utf-8")
    sp_type = (result_table[0]['SP_TYPE']).decode("utf-8")
    B_mag   = (result_table[0]['FLUX_B'])
    V_mag   = (result_table[0]['FLUX_V'])

    a = search[i][1:]  ##Arrange simbad and gaia data in a list for output
    a.insert(0, main_id)
    a.insert(5, str(B_mag))
    a.insert(6, str(V_mag))
    a.append(sp_type)
    a[1] = (sexa.split("  ")[0])
    a[2] = (sexa.split("  ")[1])

    final_list.append(a)
    
#Writes TGAS and Simbad data to a .txt file     
f = open(output_file_name, 'w')
f.writelines(["     ".join(labels), "\n"])
for line in final_list:
    text_line = "     ".join(line)
    f.writelines([text_line, "\n"])
f.close()

print(output_file_name, " created.  Number of sources:", len(search) )