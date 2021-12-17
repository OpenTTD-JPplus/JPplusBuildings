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
    "population",
    "historical_district",
    "functions",  
    "sprite_templates",
    ]

# Houses
houses = [  
    ### RESIDENTIAL | Class 0 | make sure all the IDs added into the population adder function!! ###
    
    ### Townhouses ###
    "townhouses_01",            # ID 06
    "townhouses_02",            # ID 05
    ### Houses ###
    "naganuma_house",           # ID 26
    "nishikawa_house",          # ID 26
    #"houses_old",              # ID 108
    "takamaro_01",              # ID 52
    "takamaro_02",              # ID 53
    "takamaro_03",              # ID 54
    "takamaro_04",              # ID 55
    #"old_houses",              # ID 24
    #"cottages",                # ID 25
    #"townhouses_old",          # ID 109
    ### Small Apartments ###
    "small_apartments_01",      # ID 02
    "small_apartments_02",      # ID 44
    "small_apartments_03",      # ID 45
    "small_apartments_04",      # ID 46
    ### Apartments ###
    "apartments_01",            # ID 27
    "apartments_02",            # ID 30
    "apartments_04",            # ID 56
    
    ### SHOPS AND OFFICES | Class 2 ###
    
    ### Shops ###
    "shops_01",                 # ID 48
    "shops_02",                 # ID 47
    "petrol_station_01",        # ID 50-51
    "restaurant_01",            # ID 64
    ### Offices ###
    "offices_01",               # ID 36
    "offices_02",               # ID 37
    "offices_03",               # ID 49
    "offices_04",               # ID 58
    "offices_05",               # ID 59
    ### Skyscrapers ###         
    "skyscraper_01",            # ID 76-77
    "skyscraper_02",            # ID 78
    "skyscraper_03",            # ID 79
    "skyscraper_04",            # ID 80
    ### LANDMARKS ###
    "temple_01",                # ID 66-69
    "shiro_01",                 # ID 70-73
    "stadium_01",               # ID 60-63

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
houses.sort()
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
