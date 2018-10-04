import re
from bs_craping import Soup
from read_config import get_json_object


my_url = "https://movistar.cr/tv"
json_file = "configuration_files/keywords.json"

# Testing json read
json_object = get_json_object(json_file)

# Testing soup functionality
soup = Soup(my_url)
soup_text = str(soup.get_text())
p_canales = dict(json_object['cable'])
for keywords in p_canales.values():
    for keyword in keywords:
        pattern = re.compile(keyword)
        matches = pattern.finditer(soup_text)
        print(len(list(matches)))
        for match in matches:
            print(match.group(0))
