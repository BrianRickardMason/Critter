#!/bin/bash

BROADCAST_DAEMON="/home/brian/workspace/Critter/BroadcastDaemon.py"
SUT="/home/brian/workspace/Critter/CribrarianMain.py Cribrarian1"
TEST="/home/brian/workspace/Critter/Integration/LoadWorkDetails.py"

python $BROADCAST_DAEMON &
BROADCAST_DAEMON_PID=$!

python $SUT &
SUT_PID=$!

sleep 1

python $TEST
echo $?

kill -9 $SUT_PID
kill -9 $BROADCAST_DAEMON_PID