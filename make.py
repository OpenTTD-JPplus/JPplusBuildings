#################################
####### SET UP FILES HERE #######
#################################

# Name of NewGRF, as it appears in file names
newgrf_name = "JPplusBuildings"

# Files which should be first, in order (header, cargotable, etc)
header_stuff = [
    "header",
    "cargotable",
    "HouseGap",
    "clustering",
    "population",
    "functions",  
    "sprite_templates",
    ]

# Houses
houses = [  
    ### RESIDENTIAL | Class 0 | make sure all the IDs added into the population adder function!! ###
    
    ### Townhouses ###
    "townhouses/townhouses_01",             # ID 06
    "townhouses/townhouses_02",             # ID 05
    ### Houses ###
    "houses/naganuma_house",                # ID 26
    "houses/nishikawa_house",               # ID 26
    ### Old Houses ###              
    #"houses_old/takamaro/takamaro_01",      # ID 52
    #"houses_old/takamaro/takamaro_02",      # ID 53
    #"houses_old/takamaro/takamaro_03",      # ID 54
    #"houses_old/takamaro/takamaro_04",      # ID 55
    "houses_old/dense_wooden",                  # ID 13
    "houses_old/wooden_townhouses_01",          # ID 01
    "houses_old/wooden_townhouses_02",          # ID 03
    "houses_old/wooden_townhouses_03",          # ID 04
    "houses_old/historical_zone_01",            # ID 00
    #"old_houses",              
    #"cottages",                
    #"townhouses_old",          
    ### Small Apartments ###
    "small_apartments/small_apartments_01",      # ID 02
    "small_apartments/small_apartments_02",      # ID 44
    "small_apartments/small_apartments_03",      # ID 45
    "small_apartments/small_apartments_04",      # ID 46
    ### Apartments ###
    "apartments/apartments_01",            # ID 27
    "apartments/apartments_02",            # ID 30
    "apartments/apartments_03",            # ID 31
    "apartments/apartments_04",            # ID 56
    "apartments/apartments_05",            # ID 32
    
    ### SHOPS AND OFFICES | Class 2 ###
    
    ### Shops ###
    "shops/shops_01",                       # ID 48
    "shops/shops_02",                       # ID 47
    "shops/petrol_station_01",              # ID 50-51
    "shops/restaurant_01",                  # ID 64
    "shops/shops_small_01",                 # ID 7
    ### Offices ###
    "offices/offices_01",                   # ID 36
    "offices/offices_02",                   # ID 37
    "offices/offices_03",                   # ID 49
    "offices/offices_04",                   # ID 58
    "offices/offices_05",                   # ID 59
    ### Skyscrapers ###         
    "skyscrapers/skyscraper_01",            # ID 76-77
    "skyscrapers/skyscraper_02",            # ID 78
    "skyscrapers/skyscraper_03",            # ID 79
    "skyscrapers/skyscraper_04",            # ID 80
    "skyscrapers/skyscraper_05",            # ID 81
    "skyscrapers/skyscraper_06",            # ID 82
    "skyscrapers/skyscraper_07",            # ID 83
    "skyscrapers/skyscraper_08",            # ID 84

    ### LANDMARKS ###
    "landmarks/temple_01",                  # ID 66-69
    "landmarks/temple_02",                  # ID 09-12
    "landmarks/shiro_01",                   # ID 70-73
    "landmarks/stadium_01",                 # ID 60-63
    "landmarks/hospital_01",                # ID 40-43

    ]

# Do you want to copy the completed NewGRF to your OpenTTD folder? (True/False)
copy_bool = True

# What is the path of your OpenTTD folder?
openttd_path = "/home/john/.local/share/openttd/newgrf"

#################################
# NO NEED TO CHANGE STUFF BELOW #
#################################

# Thanks to Andythenorth for much of this code

import codecs
import subprocess
import shutil

# Get the version number from the custom tags file to use in the filename
with open("src/custom_tags.txt") as v:
    lines = v.read() 
    first = lines.split('\n', 1)[0]
version = first.split(":")[1]

# Create an empty list where all the NML code will be placed
sections = []

# Function for copying code from .nml files in src folder
def append_code(file):
    filename = "src/{}.nml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    print("Merging", filename.format(file))
    sections.append(stuff.read())
    stuff.close()

# Function for copying houses code from the .nml files from houses folder
def append_houses(file):
    filename = "src/houses/{}.nml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    print("Merging", filename.format(file))
    sections.append(stuff.read())
    stuff.close()    

# Append header stuff which should always be first
for i in header_stuff:
    append_code(i)

# Sort the unordered list for readability in the printout, then append to the list
#houses.sort()
for i in houses:
    append_houses(i)

merged_nml_path = "src/merged/" + newgrf_name + "_v" + version +".nml"
grf_name = newgrf_name + "_v" + version + ".grf"

# Write the content of 'sections' into a file and save it
processed_nml_file = codecs.open(merged_nml_path,'w','utf8')
processed_nml_file.write('\n'.join(sections))
processed_nml_file.close()

print("#### nmlc ####")

# Run 
nmlc = subprocess.run(["nmlc", "-c", "-t", "src/custom_tags.txt", "-l", "src/lang", "--grf", grf_name, merged_nml_path], stdout = subprocess.PIPE, stderr = subprocess.PIPE, text=True)
print(nmlc.stdout)
print(nmlc.stderr)

if copy_bool == True:
    print("Copying NewGRF to OpenTTD folder")
    shutil.copy(grf_name, openttd_path )
else:
    print("Complete. Did not copy.")
