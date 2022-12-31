#!/bin/bash
python nml_patcher.py -f "JPplusHousesCommercial.pnml" -o "JPplusHousesCommercial.nml" -b 1 -v 1
nmlc JPplusHousesCommercial.nml -o JPplusHousesCommercial.grf -c -t src/custom_tags_commercial.txt -l src/lang
python move_grf_commercial.py
