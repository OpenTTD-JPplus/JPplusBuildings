
from lib import functions
from lib import dictionaries
import pprint

buildings_recolouring = functions.Recolouring()
buildings_no_recolouring = functions.NoRecolouring()
colour_dict = dictionaries.ColourDict()
heights_dict = dictionaries.HeightsDict()
num_heights_dict = dictionaries.NumHeightsDict()
colour_weightings_all_dict = dictionaries.ColourWeightingsAllDict()
colour_weightings_old_dict = dictionaries.ColourWeightingsOldDict()
colours_all_weightings = dictionaries.ColoursAllWeightings()
colours_old_weightings = dictionaries.ColoursOldWeightings()
end_point_all = dictionaries.EndPointAll()
end_point_old = dictionaries.EndPointOld()
start_point_all = dictionaries.StartPointAll()
start_point_old = dictionaries.StartPointOld()
random_bits_all_range = dictionaries.RandomBitsAllRange()
random_bits_old_range = dictionaries.RandomBitsOldRange()
random_bits_total_all_dict = dictionaries.RandomBitsTotalAllDict()
random_bits_total_old_dict = dictionaries.RandomBitsTotalOldDict()
items_tab = dictionaries.ItemsTab()


#pprint.pprint(items_tab)
print(buildings_recolouring)