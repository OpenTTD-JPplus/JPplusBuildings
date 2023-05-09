coloursdict = {
"white": 		"0",
"grey": 		"1",
"brown1": 		"2",
"brown2": 		"3",
"mauve":		"4",
"dark_green":	"5",
"peach":		"6",
"pink":			"7",
"light_blue":	"8",
"dark_blue":	"9",
"light_green":	"10",
"black":		"11",
"gold":			"12",
"red_brown":	"13"
}

building_name = "hayashi"
colours = ["white", "grey", "mauve", "brown1", "brown2", "red_brown", "black"]
levels = ["3L", "4L", "5L", "6L"]
items = {
	"s" : {
		"height1" : "3L",
		"height2" : "4L"
	}, 
	"m" : {
		"height1" : "5L",
		"height2" : "6L"
	}
}
variants = {
    "a" : {
		"xoffset" : "0",
		"yoffset" : "0"
	}
}

for x in variants.keys():
    print(type(x))