import sys


def read_ints_from_file_pointer(file_pointer, flag_str, num_data):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if line.startswith(flag_str):
            for i_data in range(num_words_in_flag, num_words_in_flag+num_data):
                data.append(int(line.split()[i_data]))
    if len(data) < num_data:
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_floats_from_file_pointer(file_pointer, flag_str, num_data):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if line.startswith(flag_str):
            for i_data in range(num_words_in_flag, num_words_in_flag+num_data):
                data.append(float(line.split()[i_data]))
    if len(data) < num_data:
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_float_from_file_pointer(file_pointer, flag_str):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if line.startswith(flag_str):
            data = float(line.split()[num_words_in_flag])
    if not isinstance(data, float):
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def read_int_from_file_pointer(file_pointer, flag_str):
    data = []
    num_words_in_flag = len(flag_str.split())
    file_pointer.seek(0)
    for line in file_pointer:
        if line.startswith(flag_str):
            data = int(line.split()[num_words_in_flag])
    if not isinstance(data, int):
        print("Error: cannot read ", flag_str, " from input file")
        sys.exit(1)
    return data


def open_file(file_name, open_mode="r"):
    try:
        file_pointer = open(file_name, open_mode)
        return file_pointer
    except IOError:
        print("Error: cannot open input file", file_name)
        sys.exit(1)

