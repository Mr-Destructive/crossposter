import re


def replace_line(file_name, line_num, text):
    with open(file_name, "r+") as f:
        lines = f.readlines()
        lines[line_num] = text
        f.truncate(0)
        f.seek(0)
        f.writelines(lines)


def hard_to_soft_wraps(content):
    # pre= re.findall(r'\n---\n(.*?)\n```.*$', content, re.DOTALL)
    # mid = re.findall(r'\n```\n(.*?)\n```(.*?)',content, re.DOTALL)
    # post = re.findall(r'\n```\n\n(.*$)', content, re.DOTALL)

    # get all fenced code block
    fences = re.findall(r"\n```.*?```\n", content, re.DOTALL)

    # get the frontmatter data
    frontmatter = re.findall(r"---.*?---\n", content, re.DOTALL)

    for fence in fences:
        # set the new line character as some value //r to identify later
        content = content.replace(fence, fence.replace("\n", "\\r"))
    for attrib in frontmatter:
        content = content.replace(attrib, attrib.replace("\n", "\\r"))

    # Replace the new paragraph as a special character \\r
    content = content.replace("\n\n", "\\r\\r")

    # Replace the new heading with the special character
    content = content.replace("\n#", "\\r\\r")

    # Split the text for iterating over the contents
    content = re.split("\\r\\r", content)
    for w in content:
        # replace the newline character which is a hard wrap into a whitespace
        # then replace the special character with new line character
        content = w.replace("\n", " ").replace("\\r", "\n")

    # returned soft wrapped content
    return content
