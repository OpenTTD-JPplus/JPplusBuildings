#!/bin/bash
python jpplusbuildings.py
python nml_patcher.py -f "JPplusBuildings.pnml" -o "JPplusBuildings.nml" -b 1 -v 1
nmlc JPplusBuildings.nml -o JPplusBuildings.grf -c -t src/custom_tags.txt -l src/lang
python move_grf.py
