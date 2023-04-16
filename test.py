coloursdict = {
"white": "+0",
"grey": "+1",
"brown1": "+2",
"brown2": "+3",
"mauve": "+4"
}

#building_name = "yanagi"
#colours = ["white", "grey", "mauve"]
#variants= ["a", "b"]
#levels = ["5L", "6L", "7L", "8L"]

'''
yanagi = {
  "colours"  : {
    "white"  : "+0",
    "grey"   : "+1",
	"mauve"  : "+4",
	"brown1" : "+2"
  },
  "levels" : {
    "5L" : "5L",
    "6L" : "6L",
	"7L" : "7L",
	"8L" : "8L"
  },
  "variants" : {
    "a" : {
		"xoffset" : "0",
		"yoffset" : "0"
	},
    "b" : {
		"xoffset" : "0",
		"yoffset" : "0"
	}
  }
}
'''

# Prints the colour code
# print(yanagi["colours"]["grey"])

# Prints
'''
yanagi_colours = yanagi["colours"].keys()

for i in yanagi_colours:
	print(i)
'''


'''
for x,y in yanagi["colours"].items():
	print(x,y)
'''

variants = {
    "a" : {
		"xoffset" : "2",
		"yoffset" : "0"
	},
    "b" : {
		"xoffset" : "0",
		"yoffset" : "0"
	}
  }

variant_names = list(variants.keys())

#print(variants["a"]["xoffset"])


for i in variants:
	xoff = variants[i]["xoffset"]
	yoff = variants[i]["yoffset"]
	print(xoff)
	print(yoff)


