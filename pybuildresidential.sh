#!/bin/bash
python nml_patcher.py -f "JPplusHousesResidential.pnml" -o "JPplusHousesResidential.nml" -b 1 -v 1
nmlc JPplusHousesResidential.nml -o JPplusHousesResidential.grf -c -t src/custom_tags_residential.txt -l src/lang
python move_grf_residential.py
