import urllib.request

with urllib.request.urlopen("https://docs.google.com/document/d/1x7pn2XZp6UxVUD9oOkuweInUKa66KrcmvGt-ISNxJLE/edit#") as fp:
    contents = fp.read().decode("utf-8")
    
tag_to_match = 'ulnk_url":"'
p = 0

urls_list = []
while True:
    p = contents.find(tag_to_match, p)
    if p == -1:
        break

    # skip past the starting tag

    p += len(tag_to_match)

    # find the next quotation mark after this
    # and extract the contents between the quotes

    q = contents.find('edit', p)
    url = contents[p:q]
    urls_list.append(url)
    
    # Resume search after this chunk
    p = q
    
del urls_list[0] # the first one is the formatting guide
del urls_list[-2:] # the last two are special episodes
