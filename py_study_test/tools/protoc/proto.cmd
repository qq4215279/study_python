set protoName=%1
protoc.exe -I=../../proto --java_out=../../src/ %protoName%