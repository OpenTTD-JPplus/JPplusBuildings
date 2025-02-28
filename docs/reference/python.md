Extracting a substring
https://www.computerhope.com/issues/ch001721.htm

Code to export to JSON with lists all on one line

# Function to join lists into a single line
def repl_func(match):
    return " ".join(match.group().split())

with open('lib/buildings.json', 'w', encoding='utf8') as json_file:
    # Use json.dumps to get the JSON data as a string
    output = json.dumps(buildings, ensure_ascii=False, indent=4)

    # Apply regex to modify lists to be on the same line
    output2 = re.sub(r"(?<=\[)[^\[\]]+(?=\])", repl_func, output)

    # Write the final modified output to the file
    json_file.write(output2)
