# import re

# pattern = r'^(\w+\.\w+):\s*\[(\w+(?:,\s*\w+)*)\]$'

# examples = ['hello.py: [get_Access_Token, get_Secret]', 'test.cpp: [hollow_func,get_hard]','regex.py:[pattern,henry]']

# for example in examples:
#     match = re.match(pattern, example)
#     if match:
#         filename = match.group(1)
#         functions = match.group(2).split(', ')
#         print(f"Filename: {filename}, Functions: {functions}")
#     else:
#         print(f"No match for: {example}")

import re

def extract_matches(text):
    pattern = r'[A-Za-z0-9]+\.[A-Za-z]+: \[[^\]]*\]'
    matches = []

    # Find all matches in the text
    for match in re.finditer(pattern, text, re.MULTILINE):
        # filename = match.group(1)
        # functions = match.group(2).split(', ')
        # matches.append({"filename": filename, "functions": functions})
        # matches.append()
        print("Matches inside Regex: ",match)
        print(f'The match is: {match.group(0)!r}')
        matches.append(match.group(0))
        print(matches)

    return matches

if __name__=="__main__":
    # Example usage
    large_text = """
    Some random text here...
    hello.py: [get_Access_Token, get_Secret]
    More text...
    test.cpp: [hollow_func,get_hard]
    Another line...
    """

    result = extract_matches(large_text)
    print(result)

    # for item in result:
    #     print(f"Filename: {item['filename']}, Functions: {item['functions']}")
