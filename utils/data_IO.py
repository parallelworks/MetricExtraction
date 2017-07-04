import sys
import re
import os
import tarfile


def xstr(s):
    return '' if s is None else str(s)


def removeLeadSpacesFromStrList(strList):
    for iLine, line in enumerate(strList):
        strList[iLine] = strList[iLine].lstrip()
    return strList


def removeTrailingCharFromStrList(strList, char2strip):
    for iLine, line in enumerate(strList):
        strList[iLine] = strList[iLine].rstrip().rstrip(char2strip) + '\n'
    return strList


def textStartsWithExactMath(text, flag_str, delimiter):
    if delimiter is None:
        delimiter = '\\b'
    if re.match(flag_str+delimiter, text):
        return True
    else:
        return False


def str2bool(v):
    return v.lower() in ("yes", "true", "t", "1")


def read_ints_from_file_pointer(file_pointer, flag_str, num_data,
                                delimiter=None, startIndex=0):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if textStartsWithExactMath(line, flag_str, delimiter):
            line = line[len(flag_str + xstr(delimiter)):]  # Remove flag from the beginning of line
            for i_data in range(num_data):
                data.append(int(line.split(delimiter)[i_data+startIndex]))
    if len(data) < num_data:
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_floats_from_file_pointer(file_pointer, flag_str, num_data,
                                  delimiter=None, startIndex=0):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if textStartsWithExactMath(line, flag_str, delimiter):
            line = line[len(flag_str + xstr(delimiter)):]  # Remove flag from the beginning of line
            for i_data in range(num_data):
                data.append(float(line.split(delimiter)[i_data + startIndex]))
    if len(data) < num_data:
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_float_from_file_pointer(file_pointer, flag_str, delimiter=None,
                                 startIndex=0):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if textStartsWithExactMath(line, flag_str, delimiter):
            line = line[len(flag_str + xstr(delimiter)):]  # Remove flag from the beginning of line
            data = float(line.split(delimiter)[startIndex])
    if not isinstance(data, float):
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_int_from_file_pointer(file_pointer, flag_str, delimiter=None,
                                 startIndex=0):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if textStartsWithExactMath(line, flag_str, delimiter):
            line = line[len(flag_str + xstr(delimiter)):]  # Remove flag from the beginning of line
            data = int(line.split(delimiter)[startIndex])
    if not isinstance(data, int):
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_int_from_strList(strList, flag_str, delimiter=None, startIndexInLine=0,
                          startLine=0):
    data = []
    for line in strList[startLine:]:
        if textStartsWithExactMath(line, flag_str, delimiter):
            line = line[len(flag_str + xstr(delimiter)):]  # Remove flag from the beginning of line
            data = int(line.split(delimiter)[startIndexInLine])
            break
    if not isinstance(data, int):
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_str_from_strList(strList, flag_str, delimiter=None,
                          startIndex=0, index2start=0):
    data = []
    for line in strList[index2start:]:
        if textStartsWithExactMath(line, flag_str, delimiter):
            line = line[len(flag_str + xstr(delimiter)):]  # Remove flag from the beginning of line
            data = line.split(delimiter)[startIndex]
            data = data.rstrip()
            break
    if not isinstance(data, str):
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def open_file(file_name, open_mode="r"):
    if open_mode == "w":
        if not os.path.exists(os.path.dirname(file_name)):
            os.makedirs(os.path.dirname(file_name))
    try:
        file_pointer = open(file_name, open_mode)
        return file_pointer
    except IOError:
        print("Error: cannot open file", file_name)
        sys.exit(1)


def tarDirectory(output_filename, source_dir, compressMode="w"):
    with tarfile.open(output_filename, compressMode) as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

