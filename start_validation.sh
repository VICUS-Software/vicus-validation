#!/bin/bash

py="python"

#$py validate_nandrad.py --nandrad-exec /mnt/Daten/99-git/VICUS/VICUS-Master/bin/release/NandradSolver -c="600" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"
#$py validate_nandrad.py --nandrad-exec /mnt/Daten/99-git/VICUS/VICUS-Master/bin/release/NandradSolver -c="600FF" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"
#$py validate_nandrad.py --nandrad-exec /mnt/Daten/99-git/VICUS/VICUS-Master/bin/release/NandradSolver -c="610" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"
#$py validate_nandrad.py --nandrad-exec /mnt/Daten/99-git/VICUS/VICUS-Master/bin/release/NandradSolver -c="910" -v="v1" -w="ZONE SUBSURFACE 1,ZONE SUBSURFACE 2"

source .venv/bin/activate && python run_all_validations.py --nandrad-exec ./bin/nandrad-radiation
