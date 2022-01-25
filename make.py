#################################
####### SET UP FILES HERE #######
#################################

# Name of NewGRF, as it appears in file names
newgrf_name = "JPplusBuildings"

# Files which should be first, in order (header, cargotable, etc)
header_stuff = [
    "header",
    "cargotable",
    "sprite_templates",

    ### Primary Functions (i.e. do not use any other Function)
    "functions/ModernOfficePopCheckV2",
    "functions/CommercialWithinTwoTiles",
    "functions/CommercialWithinOneTile",
    "functions/AcrossAnAvenue",
    "functions/AcrossTracks",
    "functions/CargoServiceChecks",
    "functions/one_liner_functions",

    ### Secondary Functions (i.e. those that use Primary Functions, therefore must appear later)
    "functions/SpriteDirections",
    "functions/HouseGap",
    "functions/SmallApartmentsCheck",
    "functions/ClusterBuildingClass",
    "functions/IfFirstSkyscraper",
    "functions/CommercialCargoes",  
    ]

# HOUSES
houses = [  
    ### RESIDENTIAL | Class 0 ###

    ### Houses ###
    "houses/naganuma_house",                 # ID 19-20
    "houses/nishikawa_house",                # ID 21-22

    ### Old Houses ###              
    "houses_old/wooden_farmhouse_01",        # ID 17
    "houses_old/wooden_house_01",            # ID 18
    "houses_old/dense_wooden",               # ID 13
    "houses_old/wooden_townhouses_01",       # ID 01
    "houses_old/wooden_townhouses_02",       # ID 03
    "houses_old/wooden_townhouses_03",       # ID 04
    "houses_old/wooden_townhouses_04",       # ID 08
    "houses_old/two_wooden_houses_01",       # ID 14
    "houses_old/two_wooden_houses_02",       # ID 15
    "houses_old/two_wooden_houses_03",       # ID 16
    "houses_old/large_wooden_house_01",      # ID 23
    "houses_old/large_wooden_house_02",      # ID 24
    "houses_old/large_wooden_farmhouse_01",  # ID 25
        
    ### TOWNHOUSES | CLASS 1 ###
    "houses/townhouses",                     # ID 05-06

    ### Small Apartments ###
    "small_apartments/small_apartments_01",  # ID 02
    "small_apartments/small_apartments_02",  # ID 44
    "small_apartments/small_apartments_03",  # ID 45
    "small_apartments/small_apartments_04",  # ID 46
    "small_apartments/small_apartments_05",  # ID 35
    "small_apartments/small_apartments_06",  # ID 94

    ### Apartments ###
    "apartments/apartments_01",              # ID 27
    "apartments/apartments_02",              # ID 30
    "apartments/apartments_03",              # ID 31
    "apartments/apartments_04",              # ID 56
    "apartments/apartments_05",              # ID 32
    "apartments/apartments_06",              # ID 33
    "apartments/apartments_07",              # ID 34
    "apartments/apartments_08",              # ID 92
    
    ### SHOPS AND OFFICES | Class 2 ###
    
    ### Shops ###
    "shops/convini_01",                      # ID 95
    "shops/onsen_01",                        # ID 93
    "shops/shotengai_01",                    # ID 00
    "shops/shops_01",                        # ID 48
    "shops/shops_02",                        # ID 47
    "shops/shops_03",                        # ID 65
    "shops/petrol_station_01",               # ID 50-51
    "shops/restaurant_01",                   # ID 64
    "shops/shops_small_01",                  # ID 07
    
    ### Offices ###
    "offices/offices_01",                    # ID 36
    "offices/offices_02",                    # ID 37
    "offices/offices_03",                    # ID 49
    "offices/offices_04",                    # ID 58
    "offices/offices_05",                    # ID 59
    "offices/offices_06",                    # ID 38
    "offices/offices_07",                    # ID 39
    "offices/offices_08",                    # ID 88
    "offices/offices_09",                    # ID 85
    "offices/offices_10",                    # ID 90
    "offices/offices_11",                    # ID 91
    "offices/hotel_01",                      # ID 74-75
    "offices/hotel_02",                      # ID 28-29
    
    ### SKYSCRAPERS | Class 5 ###

    ### Skyscrapers ###         
    "skyscrapers/skyscraper_01",             # ID 76-77
    "skyscrapers/skyscraper_02",             # ID 78
    "skyscrapers/skyscraper_03",             # ID 79
    "skyscrapers/skyscraper_04",             # ID 80
    "skyscrapers/skyscraper_05",             # ID 81
    "skyscrapers/skyscraper_06",             # ID 82
    "skyscrapers/skyscraper_07",             # ID 83
    "skyscrapers/skyscraper_08",             # ID 84
    "skyscrapers/skyscraper_09",             # ID 86
    "skyscrapers/skyscraper_10",             # ID 87
    "skyscrapers/skyscraper_11",             # ID 89

    ### LANDMARKS ###
    "landmarks/temple_01",                   # ID 66-69
    "landmarks/temple_02",                   # ID 09-12
    "landmarks/shiro_01",                    # ID 70-73
    "landmarks/stadium_01",                  # ID 60-63
    "landmarks/hospital_01",                 # ID 40-43

    ### RURAL ###
    "rural/farm_01",                         # ID 52-55

    ]

# Do you want to copy the completed NewGRF to your OpenTTD folder? (True/False)
copy_bool = True

# What is the path of your OpenTTD folder?
openttd_path = "/home/john/.local/share/openttd/newgrf"

#################################
# NO NEED TO CHANGE STUFF BELOW #
#################################

# Thanks to Andythenorth for much of this code, as well as 2TallTyler 

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
