
def word_to_file(logPath):
    filePath = r'D:\u02\json2Excel\word.txt'
    helf = 42
    waitTxt = []
    with open(filePath, 'r', encoding='utf-8') as file:
        for line_num, line in enumerate(file, 1):
            cleaned_line = line.strip()
            if cleaned_line is None or cleaned_line == '':
                continue
            if(str(cleaned_line).startswith('#') > 0):
                if (len(waitTxt) == 1):
                    writeLog(logPath, waitTxt[0])
                    waitTxt.clear()
                if (len(waitTxt) == 2):
                    writeLog(logPath, waitTxt[0] + ' ' * (helf - calc_string_length_v2(waitTxt[0])) + waitTxt[1])
                    waitTxt.clear()
                writeLog(logPath, '\n' + cleaned_line)
                continue
            if(len(waitTxt) < 2):
                waitTxt.append(cleaned_line)
                continue
            writeLog(logPath, waitTxt[0] + ' ' * (helf - calc_string_length_v2(waitTxt[0])) + waitTxt[1])
            waitTxt.clear()
    for txt in waitTxt:
        writeLog(logPath, txt)

def writeLog(logPath, logTxt):
    with open(logPath, 'a', encoding='utf-8') as f:
        f.write(logTxt + '\n')

def calc_string_length_v2(s):
    return sum(2 if '\u4e00' <= char <= '\u9fff' or char in '/' else 1 for char in s)

if __name__ == '__main__':
    word_to_file(r'D:\u02\json2Excel\word_result.txt')