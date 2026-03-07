import os
import json


basePath = 'D:\\file\\historyDownloads\\program\\'

def readEnumerate(fileName):
    with open(os.path.join(basePath, fileName), 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            cleaned_line = line.strip()
            if cleaned_line:
                print(f"第 {line_num} 行：{cleaned_line}")


def readLine(fileName):
    with open(os.path.join(basePath, fileName), 'r', encoding='utf-8') as file:
        while True:
            line = file.readline()
            print(line)
            if(not line):
                break

def readLines(fileName):
    with open(os.path.join(basePath, fileName), 'r', encoding='utf-8') as file:
        lines = file.readlines()
        print(lines)

def readLines(fileName):
    with open(os.path.join(basePath, fileName), 'r', encoding='utf-8') as file:
        txt = json.load(file)
        print(txt)

readEnumerate('array.txt')
readLine('array.txt')
readLines('array.txt')
