# Fukuda
fukuda_all_colours = {  "grey" :        "1",
                        "midgrey" :     "1"
                        }

# Harada
harada_all_colours = {  "white" :       "1", 
                        "grey":         "1", 
                        "mauve" :       "1", 
                        "brown1" :      "1", 
                        "brown2" :      "1", 
                        "red_brown" :   "1", 
                        "black" :       "1"  
                        }
# Hayashi
hayashi_all_colours = { "white" :       "1", 
                        "grey":         "1", 
                        "mauve" :       "1", 
                        "brown1" :      "1", 
                        "brown2" :      "1", 
                        "red_brown" :   "1", 
                        "black" :       "1"  
                        }

# Hirano
hirano_all_colours = {  "white" :       "1" , 
                        "grey" :        "1", 
                        "mauve" :       "1", 
                        "brown1" :      "1", 
                        "brown2" :      "1", 
                        "dark_green" :  "1", 
                        "peach" :       "1", 
                        "pink" :        "1", 
                        "light_blue" :  "1", 
                        "dark_blue" :   "1"
                        }

hirano_old_colours = {  "white" :       "1", 
                        "grey" :        "1", 
                        "mauve" :       "1", 
                        "brown1" :      "1", 
                        "brown2" :      "1"
                        }

buildings_dict = {
	"fukuda" : {
		"construction_state" : "construction_state",
        "colours" : fukuda_all_colours,
        "old_colours" : False,
        "levels" : {"6L", "8L"},
        "variants" : {    
            "x" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        }
        }
    },
	"harada" : {
		"construction_state" : "construction_state",
        "colours" : harada_all_colours,
        "old_colours" : False,
        "levels" : {"6L", "8L"},
        "variants" : {    
            "x" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        }
        }
	},
    "hayashi" : {
		"construction_state" : "3",
        "colours" : hayashi_all_colours,
        "old_colours" : False,
        "levels" : {"3L", "4L", "5L", "6L"},
        "variants" : {    
            "x" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        }
        }
	},
    "hirano" : {
		"construction_state" : "3",
        "colours" : hirano_all_colours,
        "old_colours" : hirano_old_colours,
        "levels" : {"3L", "4L", "5L", "6L"},
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
	},
}
