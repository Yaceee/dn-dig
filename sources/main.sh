#!/usr/bin/env bash

dbname="DB_vignette20000"
width="400"
height="400"
imNum="625"
day="25"
night="-175"
traffic="15"

python3 simulation.py --dbname $dbname --dimension $width $height --imNum $imNum --traffic $traffic --angle $day
python3 simulation.py --dbname $dbname --dimension $width $height --imNum $imNum --traffic $traffic --angle $night

python3 extra/evaluation_DB.py --dbname $dbname
