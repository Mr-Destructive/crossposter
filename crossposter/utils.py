
def replace_line(file_name, line_num, text):
    with open(file_name, "r+") as f:
        lines = f.readlines()
        lines[line_num] = text
        f.truncate(0)
        f.seek(0)
        f.writelines(lines)
