
def replace_line(file_name, line_num, text):
    lines = open(file_name, "r").readlines()
    print(lines)
    lines[line_num] = text
    out = open(file_name, "w")
    out.writelines(lines)
    out.close()
