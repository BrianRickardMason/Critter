#!/bin/bash

BROADCAST_DAEMON="/home/brian/workspace/Critter/BroadcastDaemon.py"
SUT="/home/brian/workspace/Critter/BalancerMain.py Balancer1"
TEST="/home/brian/workspace/Critter/Integration/CantExecuteWorkNow.py"

python $BROADCAST_DAEMON &
BROADCAST_DAEMON_PID=$!

sleep 1

python $SUT &
SUT_PID=$!

sleep 1

python $TEST
echo $?

kill -9 $SUT_PID
kill -9 $BROADCAST_DAEMON_PID
