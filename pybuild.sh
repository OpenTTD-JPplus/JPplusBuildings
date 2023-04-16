#!/bin/bash
python src/house/apartments/yanagi/yanagi.py
python replicate_directions.py
python combine_directions.py
python replicate_buildings.py
python nml_patcher.py -f "JPplusBuildings.pnml" -o "JPplusBuildings.nml" -b 1 -v 1
nmlc JPplusBuildings.nml -o JPplusBuildings.grf -c -t src/custom_tags.txt -l src/lang
python move_grf.py
