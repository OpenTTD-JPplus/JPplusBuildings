# Bank Building
bank_building_all_colours =     {   "black" :       2,
                                    "midgrey" :     1
                                    }

# Fukuda
fukuda_all_colours =            {   "grey" :        2,
                                    "midgrey" :     1
                                    }

# Harada
harada_all_colours =            {   "white" :       1, 
                                    "grey":         1, 
                                    "mauve" :       1, 
                                    "brown1" :      1, 
                                    "brown2" :      1, 
                                    "red_brown" :   1, 
                                    "black" :       1  
                                    }
# Hayashi
hayashi_all_colours =           {   "white" :       1, 
                                    "grey":         1, 
                                    "mauve" :       1, 
                                    "brown1" :      1, 
                                    "brown2" :      1, 
                                    "red_brown" :   1, 
                                    "black" :       1  
                                }

# Hirano
hirano_all_colours =            {   "white" :       1 , 
                                    "grey" :        2, 
                                    "mauve" :       1, 
                                    "brown1" :      2, 
                                    "brown2" :      2, 
                                    "dark_green" :  1, 
                                    "peach" :       1, 
                                    "pink" :        1, 
                                    "light_blue" :  1, 
                                    "dark_blue" :   1
                                    }

hirano_old_colours =            {   "white" :       1, 
                                    "grey" :        2, 
                                    "mauve" :       1, 
                                    "brown1" :      2, 
                                    "brown2" :      2
                                    }
                        
# Hirata
hirata_all_colours =            {   "white" :       1 , 
                                    "grey" :        2, 
                                    "mauve" :       1, 
                                    "brown1" :      2, 
                                    "brown2" :      2, 
                                    "dark_green" :  1, 
                                    "peach" :       1, 
                                    "pink" :        1, 
                                    "light_blue" :  1, 
                                    "dark_blue" :   1
                                    }

hirata_old_colours =            {   "white" :       1, 
                                    "grey" :        2, 
                                    "mauve" :       1, 
                                    "brown1" :      2, 
                                    "brown2" :      2
                                    }

buildings_dict = {
	"bank_building" : {
		"construction_state" : "construction_state",
        "colours" : bank_building_all_colours,
        "old_colours" : False,
        "levels" : {"sky"},
        "heights" : {    
            "c" : ["sky"]
        },
        "variants" : {    
            "x" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        }
        }
    },
    
    
    "fukuda" : {
		"construction_state" : "construction_state",
        "colours" : fukuda_all_colours,
        "old_colours" : False,
        "levels" : {"6L", "8L"},
        "heights" : {    
            "m" : ["6L"],
            "l" : ["8L"]
        },
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
        "heights" : {    
            "m" : ["6L"],
            "l" : ["8L"]
        },
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
        "heights" : {    
            "s" : ["3L","4L"],
            "m" : ["5L","6L"]
        },
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
        "end_of_old_era" : 1959,
        "levels" : {"3L", "4L", "5L", "6L"},
        "heights" : {    
            "s" : ["3L","4L"],
            "m" : ["5L","6L"]
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
	},
    "hirata" : {
		"construction_state" : "construction_state",
        "colours" : hirata_all_colours,
        "old_colours" : hirata_old_colours,
        "end_of_old_era" : 1959,
        "levels" : {"3L", "4L", "5L", "6L"},
        "heights" : {    
            "s" : ["3L","4L"],
            "m" : ["5L","6L"]
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
	},
}