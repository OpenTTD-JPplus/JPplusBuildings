#!/bin/bash
python nml_patcher.py -f "JPplusHouses.pnml" -o "JPplusHouses.nml" -b 1 -v 1
nmlc JPplusHouses.nml -o JPplusHouses.grf -c -t src/custom_tags.txt -l src/lang
python move_grf.py
