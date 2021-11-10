#################################
####### SET UP FILES HERE #######
#################################

# Name of NewGRF, as it appears in file names
newgrf_name = "JPplusBuildings"

# Files which should be first, in order (header, cargotable, etc)
header_stuff = [
    "header", 
    "graphics", 
    "functions",  
    "waste",
    "sprite_templates",
    ]

# Houses
houses = [  
    ### Class 0 - RESIDENTIAL - are all the IDs added into the population adder function? ###
    
    ### Townhouses ###
    "townhouses_01",            # ID 06
    "townhouses_02",            # ID 06
    ### Houses ###
    "naganuma_house",           # ID 26
    "nishikawa_house",          # ID 26
    #"houses_old",              # ID 108
    #"old_houses",              # ID 24
    #"cottages",                # ID 25
    #"townhouses_old",          # ID 109
    ### Small Apartments ###
    "small_apartments_01",      # ID 02
    "small_apartments_02",      # ID 02
    ### Apartments ###
    "apartments_01",            # ID 27
    "apartments_02",            # ID 27
    
    ### SHOPS AND OFFICES ###
    
    ### Shops ###
    #"shops_01"                  # ID 33
    ### Offices ###
    ]

# Files to place in alphabetical order below
unordered_stuff = [
    "residential", 
    "commercial", 
    "landmarks", 
    "tropic", 
    #"arctic"
    ]

# Items that have to appear after the graphic
post_graphics_stuff = [
    "switches"
]

commercial = [    
    ### SHOPS AND OFFICES ###
    
    ### Shops ###
    "shops_01"                  # ID 33
    ### Offices ###
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

# Append post graphics stuff which should always be first
for i in post_graphics_stuff:
    append_code(i)

# Sort the unordered list for readability in the printout, then append to the list
unordered_stuff.sort()
for i in unordered_stuff:
    append_code(i)

# Sort the unordered list for readability in the printout, then append to the list
commercial.sort()
for i in commercial:
    append_houses(i)

merged_nml_path = "src/merged/" + newgrf_name + ".nml"
grf_name = newgrf_name + ".grf"

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
