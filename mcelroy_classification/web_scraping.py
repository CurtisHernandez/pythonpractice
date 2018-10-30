import urllib.request

# get the contents of the web page
URL = "https://docs.google.com/document/d/1DZTzWWcsRm815uoUpXWlxytaLrO8gKjEMhZ7fzV68Vc/edit"
with urllib.request.urlopen(URL) as fp:
    contents = fp.read().decode("utf-8")
    
# how search through the text for the <script> lines
# that I want and print them:
tag_to_match = '"s":"'
p = 0

speakers = {"Justin": [], "Travis": [], "Griffin": []}

def noStageDirections(text):
    while True:
        openbracket = text.find('[')
        closebracket = text.find(']')
        brackettext = text[openbracket:closebracket+1]
        if openbracket == -1 or closebracket == -1:
            break
        else:
            text = text.replace(brackettext,"")
            continue
    return text

while True: # Loop forever
    p = contents.find(tag_to_match, p)
    if p == -1:
        break

    # skip past the starting tag

    p += len(tag_to_match)

    # find the next quotation mark after this
    # and extract the contents between the quotes

    q = contents.find('"', p)
    chunk = contents[p:q]

    # heuristics to remove special characters
    # (See Python Language Reference about raw string literals)

    chunk = chunk.replace(r'''\n''', '\n')          # New line
    chunk = chunk.replace(r'''\t''', ' ')           # Tab
    chunk = chunk.replace(r'''\u000b''', '\n')      # Vertical tab
    chunk = chunk.replace(r'''\u0026''', '&')       # Ampersand
    chunk = chunk.replace(r'''\u0027''', "'")       # Smart apostrophe
    chunk = chunk.replace(chr(0x2013), "-")         # M-dash
    chunk = chunk.replace(chr(0x201c), '"')         # Smart start quote
    chunk = chunk.replace(chr(0x201d), '"')         # Smart end quote
    chunk = chunk.replace(chr(0x2026), '...')       # Ellipsis

#    chunk = noStageDirections(chunk) # get rid of bracketed things

    # split chunk up into lines
    splitchunk = chunk.split(sep='\n')
    for i in splitchunk:
        line = i.strip()
        if line.startswith("Justin: "):
            line = line[len("Justin: "):] # everything after their names
            line = noStageDirections(line)
            speakers['Justin'].append(line)
        elif line.startswith("Travis: "):
            line = line[len("Travis: "):]
            line = noStageDirections(line)
            speakers['Travis'].append(line)
        elif line.startswith("Griffin: "):
            line = line[len("Griffin: "):]
            line = noStageDirections(line)
            speakers['Griffin'].append(line)

    # Resume search after this chunk

    p = q

import pandas as pd
brotherlist = []
gooftextlist = []
for i in list(speakers.keys()):
    for j in speakers[i]:
        if j != "''" and j!= "":
            brotherlist.append(i)
            gooftextlist.append(j)
df = pd.DataFrame(columns=["brother","gooftext"])
df["brother"]=brotherlist
df["gooftext"]=gooftextlist
