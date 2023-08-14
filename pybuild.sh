#!/bin/bash
python jpplusbuildings.py
python switches_directions.py
python pnml_combiner.py
python items.py
python nml_patcher.py -f "JPplusBuildings.pnml" -o "JPplusBuildings.nml" -b 1 -v 1
nmlc JPplusBuildings.nml -o JPplusBuildings.grf -c -t src/custom_tags.txt -l src/lang
python move_grf.py
