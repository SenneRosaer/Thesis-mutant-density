import re
from html.parser import HTMLParser
from collections import defaultdict

def extract_output_from_line(line):
    first_occurance = True
    output = ""
    for item in line:
        if not item.endswith(">"):
            if first_occurance:
                first_occurance = False
            else:
                output += item.split(">")[1]
    return output
def parse_mutants_from_file(filename):
    with open(filename, "r") as f:
        strr = f.read()
        table = strr.split("<table cellpadding=\"0\" id=\"locs\">")[1].split("</table")[0]
        table.replace("</tr>", "")
        rows = table.split("<tr>")[1:]

        current_stack = 0
        backup_stack = 0
        def f():
            return 0
        results = defaultdict(f)
        latest_key = None
        latest_key_index = None
        for index, row in enumerate(rows):
            if "{" in row:
                if index > 14500:
                    print()
                if current_stack == 0:
                    print("open at: " + str(index+1))
                    total = ""
                    output = None
                    new_index = index
                    while output != '\n' and output != '*/':
                        tmp_row = rows[new_index]
                        tmp_row = tmp_row.split('<')[1:]
                        output = extract_output_from_line(tmp_row)
                        new_index -= 1
                        if '//' not in output and '///' not in output:
                            total = output + total

                    latest_key_index = int(rows[new_index + 2].split('">')[0].split('loc-')[-1])
                    latest_key = total.replace('\n', '')
                    if latest_key == '':
                        continue
                if latest_key and "namespace" in latest_key:
                    latest_key = None
                    backup_stack += 1
                elif latest_key and "class" in latest_key:
                    backup_stack += 1
                else:
                    current_stack +=1
            if "}" in row:
                if 'nlohmann' in filename:
                    print()
                if current_stack == 0:
                    backup_stack -= 1
                else:
                    current_stack -=1
                if current_stack == 0:
                    print("close at: " + str(index+1))

            count = row.count("class=\"mutant")
            if count:
                print(f"{count} mutant(s) at {index+1}")

                # TODO struct shit is weird with struct in struct etc.
                if 'struct' in latest_key:
                    method = latest_key.split('struct')[1].split('&lt;')[0].replace('&nbsp;', '').replace('{', '')
                else:
                    try:
                        temp_count = 0
                        split_index = None
                        could_break = False
                        for index2, char in enumerate(latest_key[::-1]):
                            if char == '(':
                                temp_count -= 1
                            elif char == ')':
                                temp_count += 1
                                could_break = True

                            if could_break and temp_count == 0:
                                split_index = index2 + 1
                                break
                        split_index = len(latest_key) - split_index
                        test = latest_key[0:split_index]
                        method = test.split('&nbsp;')[-1].replace('{', '')
                    except:
                        method = latest_key.split('(')[0].split("&nbsp;")[-1].replace('{', '')
                if 'nlohmann' in filename:
                    print()
                if '::' in method:
                    method = method.split('::')[-1]
                results[str(latest_key_index) + '//' +filename.split('/')[-1].replace('.html','').replace('__','/')+ '//' + method] += count
                # results[filename.split('/')[-1].replace('.html', '').replace('__', '/') + '//' + latest_key.split('(')[0].split("&nbsp;")[-1].split('::')[-1]] += count

        return results
if __name__ == '__main__':
    resulst = parse_mutants_from_file('Game.cpp.html')
    print()