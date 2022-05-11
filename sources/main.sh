#!/usr/bin/env bash

dbname="DB_little"
width="1920"
height="1080"
imNum="10"
sunAngles=( "25" "-175" )
towns=( "town01" "town02" "town03" "town04" "town05" "town06" "town07" "town10HD" )
traffic="15"

for (( i = 0; i < ${#towns[@]}; i++ )); do
  for (( j = 0; j < ${#sunAngles[@]}; j++ )); do
    firstTry=1
    while [[ $? != 0 || $firstTry = 1 ]]; do
      gnome-terminal -- /opt/carla-simulator/CarlaUE4.sh -opengl -RenderOffScreen
      sleep 2
      firstTry=0
      python3 simulation.py --dbname $dbname --town ${towns[i]} --dimension $width $height --imNum $imNum --traffic $traffic --angle ${sunAngles[j]}
    done
    carlaPID=$(pgrep -f CarlaUE4-Linux-)
    kill -9 $carlaPID
  done
done

python3 extra/evaluation_DB.py --dbname $dbname
python3 extra/video_maker.py --dbname $dbname --fps 5
