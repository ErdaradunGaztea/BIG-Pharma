#!/bin/bash

su big_pharmaceuta
hadoop fs -mkdir /user/big_pharmaceuta/youtube
hadoop fs -mkdir /user/big_pharmaceuta/genius
exit

su nifi 
mkdir /home/nifi/project
exit
