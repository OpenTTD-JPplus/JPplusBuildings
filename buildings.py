# Bank Building
bank_building_all_colours =     {   "black" :       2,
                                    "midgrey" :     1
                                    }

# Farm
farm_all_colours =            {     "black" :       1, 
                                    "brown1":       1, 
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

# Hospital
hospital_all_colours =          {   "light_blue" :  1, 
                                    "grey":         1, 
                                    "dark_blue" :   1, 
                                    "brown1" :      1, 
                                    "brown2" :      1, 
                                    "red_brown" :   1, 
                                    "dark_green" :  1  
                                }

# Pachinko
pachinko_all_colours =          {   "black" :       1,
                                    "midgrey" :     1
                                    }

# Naganuma
naganuma_all_colours =          {   "gold" :        2 , 
                                    "grey" :        3, 
                                    "mauve" :       2, 
                                    "brown1" :      2, 
                                    "brown2" :      2, 
                                    "dark_green" :  1, 
                                    "black" :       2, 
                                    "red_brown" :   2,
                                    "red" :         2, 
                                    "dark_blue" :   1
                                    }

naganuma_old_colours =          {   "black" :       2, 
                                    "grey" :        2, 
                                    "mauve" :       1, 
                                    "brown1" :      2, 
                                    "brown2" :      2,
                                    "red_brown" :   1,
                                    }

# Police Station
police_station_all_colours =    {   "light_blue" :  1, 
                                    "red":          1, 
                                    "dark_blue" :   1, 
                                    "black" :       1 
                                }

# Shiro
shiro_all_colours =             {   "black" :       1, 
                                    "brown1":       1, 
                                    "brown2" :      1, 
                                    "grey" :        1
                                }

# Stadium
stadium_all_colours =          {    "light_blue" :  1, 
                                    "red":          1, 
                                    "dark_blue" :   1, 
                                    "gold" :        1, 
                                    "black" :       1, 
                                    "red_brown" :   1, 
                                    "dark_green" :  1  
                                }

# Temple
temple_all_colours =            {   "black" :       1, 
                                    "brown1":       1, 
                                    "brown2" :      1, 
                                    "grey" :        1, 
                                    "red_brown" :   1, 
                                }

# Tsuno Building
tsuno_building_all_colours =    {   "light_blue" :  1, 
                                    "red":          1, 
                                    "dark_blue" :   1, 
                                    "gold" :        1, 
                                    "black" :       1, 
                                    "red_brown" :   1, 
                                    "dark_green" :  1  
                                }

buildings_dict = {
	"bank_building" : {
        "colours" : bank_building_all_colours,
        "old_colours" : False,
        "levels" : {"x"},
        "heights" : {    
            "c" : ["x"]
        },
        "variants" : {    
            "x" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
	        }
        }
    },
     "farm" : {
        "manual_gfx" : True,
        "manual_switches" : True,
        "colours" : farm_all_colours,
        "old_colours" : False,
        "levels" : {"x"},   
        "heights" : {    
            "h" : ["x"],   
        },
        "variants" : {    
            "north" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "east" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "west" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "south" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        }
        }
	},
    "fukuda" : {
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
		        "yoffset" : "0",
                "construction_state" : "3"
	        }
        }
	},
    "hirano" : {
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
		        "yoffset" : "0",
                "construction_state" : "3"
	        },
	        "b" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "construction_state" : "3"
	        }
        }
	},
    "hirata" : {
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
    "hospital" : {
        "colours" : hospital_all_colours,
        "old_colours" : False,
        "levels" : {"x"},   # x since only one version of this 2X2
        "heights" : {    
            "k" : ["x"],    # k means landmark and 2X2
        },
        "variants" : {    
            "north" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "east" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "west" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "south" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        }
        }
	},
    "naganuma" : {
        "colours" : naganuma_all_colours,
        "old_colours" : naganuma_old_colours,
        "end_of_old_era" : 1959,
        "ground" : "spr_ground_grass",
        "levels" : {"a", "b", "c", "d", "e", "f"},
        "heights" : {    
            "h" : ["a", "b", "c", "d", "e", "f"]
        },
        "variants" : {    
            "x" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
	        }
        }
	},
    "pachinko" : {
        "colours" : pachinko_all_colours,
        "old_colours" : False,
        "levels" : {"x"},
        "heights" : {    
            "k" : ["x"]
        },
        "variants" : {    
            "x" : {
		        "xoffset" : "3",
		        "yoffset" : "-1",
	        }
        }
    },
    "police_station" : {
        "colours" : police_station_all_colours,
        "old_colours" : False,
        "levels" : {"x"},
        "heights" : {    
            "k" : ["x"],
        },
        #"shared_variant_gfx" : True,
        "variants" : {    
            "north" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
	        },
            "east" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
	        },
        }
	},
    "shiro" : {
        "colours" : shiro_all_colours,
        "old_colours" : False,
        "ground" : "spr_ground_shiro",
        "levels" : {"x"},   # x since only one version of this 2X2
        "heights" : {    
            "k" : ["x"],    # k means landmark and 2X2
        },
        "shared_variant_gfx" : True,
        "variants" : {    
            "north" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "hide_sprite":  "1",
                "construction_state" : "3"
	        },
            "east" : {
		        "xoffset" : "-1",
		        "yoffset" : "2",
                "construction_state" : "2"
	        },
            "west" : {
		        "xoffset" : "1",
		        "yoffset" : "0",
                "construction_state" : "0"
	        },
            "south" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "construction_state" : "1"
	        }
        }
	},
    "stadium" : {
        "colours" : stadium_all_colours,
        "old_colours" : False,
        "levels" : {"x"},   # x since only one version of this 2X2
        "heights" : {    
            "k" : ["x"],    # k means landmark and 2X2
        },
        "shared_variant_gfx" : True,
        "variants" : {    
            "north" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "construction_state" : "0"
	        },
            "east" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "construction_state" : "2"
	        },
            "west" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "construction_state" : "1"
	        },
            "south" : {
		        "xoffset" : "0",
		        "yoffset" : "0",
                "construction_state" : "3"
	        }
        }
	},
    "temple" : {
		"construction_state" : "3",
        "colours" : temple_all_colours,
        "old_colours" : False,
        "levels" : {"p", "q"},   
        "heights" : {    
            "k" : ["p", "q"],       # may need to vary the k
        },
        "shared_variant_gfx" : True,
        "variants" : {    
            "north" : {
		        "xoffset" :     "0",
		        "yoffset" :     "0",
                "hide_sprite":  "1",
                "construction_state" : "3"
	        },
            "east" : {
		        "xoffset" :     "1",
		        "yoffset" :     "3",
                "construction_state" : "2"
	        },
            "west" : {
		        "xoffset" :     "1",
		        "yoffset" :     "0",
                "construction_state" : "0"
	        },
            "south" : {
		        "xoffset" :     "0",
		        "yoffset" :     "0",
                "construction_state" : "1"
	        }
        }
	},
    "tsuno_building" : {
        "colours" : tsuno_building_all_colours,
        "old_colours" : False,
        "levels" : {"x"},   
        "heights" : {    
            "c" : ["x"],    
        },
        "variants" : {    
            "north" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
            "east" : {
		        "xoffset" : "0",
		        "yoffset" : "0"
	        },
        },
	},
}