import codecs

# KIMURA

# Files which should be first, in order
merged_pnml_path = "src/houses/apartments/kimura/kimura_3L.pnml"
kimura = ["kimura_a", "kimura_b", "kimura_s", "kimura_e", "kimura_w", "kimura_n" , "kimura_z"]

# Create an empty list where all the PNML code will be placed
sections = []

# Function for copying code from .nml files
def append_code(file):
    filename = "src/houses/apartments/kimura/{}.pnml"
    stuff = codecs.open(filename.format(file),'r','utf8')
    print("Merging", filename.format(file))
    sections.append(stuff.read())
    stuff.close()

# Append header stuff which should always be first
for i in kimura:
    append_code(i)

# Write the content of 'sections' into a file and save it
processed_pnml_file = codecs.open(merged_pnml_path,'w','utf8')
processed_pnml_file.write('\n'.join(sections))
processed_pnml_file.close()
