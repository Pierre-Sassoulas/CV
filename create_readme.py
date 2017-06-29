# -*- coding: utf-8 -*-

import argparse

def read_latex(file_):
    """ Return the content of a latex file without the command. """
    with open(file_) as f:
        document = ""
        while True:
            line = f.readline()
            if not line:
                break
            for letter in line:
                if letter in [" ", "\t"]:
                    continue
                if letter == "%":
                    break
                else:
                    document += line
                    break
        f.close()
    #  Replacing all \t and \n and shit by space
    document = " ".join(document.split())
    # Removing all space before {
    final_result = document.replace(" {", "{")
    while final_result != final_result.replace(" {", "{"):
        final_result = final_result.replace(" {", "{")
    return final_result

def get_content_between_bracket(text):
    open_bracket = 0
    content = ""
    for letter in text:
        if letter == "{":
            open_bracket += 1
        elif letter == "}":
            if open_bracket == 0:
                content += letter
                break
            else:
                open_bracket -= 1
        content += letter
    return content

def get_command_content(text, command):
    content = []
    for i, part in enumerate(text.split("\%s{" % command)):
        if i != 0:
            part = " ".join(part.split())
            cleaned_part = "{"
            closing_bracket = False
            opening_bracket = 1
            #  print part
            for letter in part:
                # print "Letter %s, opening bracket %s, closing bracket %s" % (letter, opening_bracket, closing_bracket)
                if letter == "{":
                    opening_bracket += 1
                    closing_bracket = False
                elif letter == '}':
                    opening_bracket -= 1
                    if opening_bracket == 0:
                        closing_bracket = True
                elif letter == " ":
                    pass
                elif letter != '{' and closing_bracket:
                    #  print "Letter {} is not an opening bracket".format(letter)
                    break
                cleaned_part += letter
            # print i, command, "cleaned part :", cleaned_part
            content.append(cleaned_part)
    return content

def get_command_as_list(text, command):
    result = []
    raw_list = get_command_content(text, command)
    for raw_command in raw_list:
        command_list = []
        current = ""
        openning_bracket = 0
        for letter in raw_command:
            if letter == "{":
                if openning_bracket != 0:
                    current += "{"
                openning_bracket += 1
            elif letter == "}":
                openning_bracket -= 1
                if openning_bracket == 0:
                    command_list.append(current)
                    current = ""
                else:
                    current += letter
            else:
                current += letter
        if len(command_list) == 1:
            command_list = command_list[0]
        result.append(command_list)
    return result

def latex_to_md(text):
    #  re.sub("\\textbf{[\-\w ()'\\{}]*}", "** **", text)
    text = text.replace("\\textbf{", "__").replace("}", "__")
    text = text.replace("\\newline{__", ",")
    text = text.replace("\\Rating{100__", ":star:")
    text = text.replace("\\LaTeX{__", "LaTeX")

    return text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("cvfile", help="The name of your CV's LaTeX file")
    args = parser.parse_args()
    readme = open("readme.md", 'w')
    document = read_latex(args.cvfile)
    head, body = document.split("begin{document}")
    first_name = get_command_as_list(head, "firstname")[0]
    last_name = get_command_as_list(head, "familyname")[0]
    title = get_command_as_list(head, "title")[0]
    mail = get_command_as_list(head, "email")[0]
    readme.write("# À PROPOS DE MOI\n")
    readme.write("""
%s %s, %s

## Pour me contacter

%s

""" % (first_name, last_name, latex_to_md(title), mail))
    for section in get_command_as_list(body, "section"):
        readme.write("\n# {}\n".format(section))
        print "Treating", section
        section_content = body.split("section{%s}" % section)[1]
        section_content = section_content.split("\\section")[0]
        cventry = get_command_as_list(section_content, "cventry")
        cvline = get_command_as_list(section_content, "cvline")
        cvlanguage = get_command_as_list(section_content, "cvlanguage")
	cvcomputer = get_command_as_list(section_content, "cvcomputer")
        if cventry:
            for line in cventry:
                md_line = """
## %s

**%s** : %s, %s

%s

""" % (line[1], latex_to_md(line[0]), line[2], line[3], line[5])
                readme.write(md_line)
        if cvline:
            for line in cvline:
                md_line = """
## %s

%s

""" % (latex_to_md(line[0]), latex_to_md(line[1]))
                readme.write(md_line)
        if cvlanguage:
            for language in cvlanguage:
                md_line = """
## %s

%s
""" % (language[0], language[1])
                readme.write(md_line)
        if cvcomputer:
            for computer in cvcomputer:
                md_line = """
## %s

%s

## %s

%s
""" % (latex_to_md(computer[0]), latex_to_md(computer[1]),
       latex_to_md(computer[2]), latex_to_md(computer[3]))
                readme.write(md_line)
    readme.close()
