#!/usr/bin
protoName=$1
./protoc -I=../../proto --java_out=../../src/main/java/ $1