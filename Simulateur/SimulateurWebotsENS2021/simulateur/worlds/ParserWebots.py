import re

NewWorld = open("empty2.wbt","w")
Test =[]
f=open("empty.wbt","r")
for line in f:
    for car in line:
        if car=='{':
            line = line[:-2]
            line.replace(" ", "")
            Test.append(line)#print(line)

print(Test)
