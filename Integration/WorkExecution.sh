#!/bin/bash

BROADCAST_DAEMON="/home/brian/workspace/Critter/BroadcastDaemon.py"
SUT="/home/brian/workspace/Critter/WorkerMain.py Worker1"
TEST="/home/brian/workspace/Critter/Integration/WorkExecution.py"

python $BROADCAST_DAEMON &
BROADCAST_DAEMON_PID=$!

python $SUT &
SUT_PID=$!

python $TEST
echo $?

kill -9 $SUT_PID
kill -9 $BROADCAST_DAEMON_PID
