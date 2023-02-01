import re
from html.parser import HTMLParser
from collections import defaultdict


def parse_mutants_from_file(filename):
    with open(filename, "r") as f:
        strr = f.read()
        table = strr.split("<table cellpadding=\"0\" id=\"locs\">")[1].split("</table")[0]
        table.replace("</tr>", "")
        rows = table.split("<tr>")[1:]

        current_stack = 0
        def f():
            return 0
        results = defaultdict(f)
        latest_key = None
        for index, row in enumerate(rows):
            if "{" in row:
                if current_stack == 0:
                    print("open at: " + str(index+1))
                    tmp_row = rows[index-1]
                    tmp_row = tmp_row.split('<')[1:]
                    first_occurance = True
                    output = ""
                    for item in tmp_row:
                        if not item.endswith(">"):
                            if first_occurance:
                                first_occurance = False
                            else:
                                output += item.split(">")[1]
                    print(output)
                    latest_key = output
                if latest_key and "namespace" in latest_key:
                    latest_key = None
                elif latest_key and "class" in latest_key:
                    pass
                else:
                    current_stack +=1
            if "}" in row:
                current_stack -=1
                if current_stack == 0:
                    print("close at: " + str(index+1))

            count = row.count("class=\"mutant")
            if count:
                print(f"{count} mutant(s) at {index+1}")
                results[filename + latest_key.replace("&nbsp;", "")] += count
        return results
if __name__ == '__main__':
    resulst = parse_mutants_from_file('Game.cpp.html')
    print()