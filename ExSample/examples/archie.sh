# --------------------------------------------------------------------------
# This is an example for running the offline query on the Archie dataset.
# 1. Download data from: 
#   https://drive.google.com/drive/folders/1riFVI6QZGf8X6lyFphyRighAYMDTAH4Z
# 2. Modify the following arguments to the path in your enviroment.
# Learn more in the README.md file.
# --------------------------------------------------------------------------

python ExSample/examples/offline_query.py \
    -v ../datasets/archie-day/2018-04-10 \
    -c ../datasets/blazeit/filtered/archie-day/archie-day-2018-04-10.csv \
    -o bicycle -n 16 -l 3000