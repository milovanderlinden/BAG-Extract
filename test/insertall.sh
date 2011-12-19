#!/bin/sh
#
# Test with small pieces of BAG for easy debugging
#
DATA_DIR=$PWD/data
cd ../src
python BAG.py --dbinit
python BAG.py -e $DATA_DIR
cd -

