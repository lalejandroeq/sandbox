import re
from bs_craping import Soup
from config import get_json_object


my_url = "https://movistar.cr/tv"
json_file = "configuration_files/words.json"

# Testing json read
json_object = get_json_object(json_file)

# Testing soup functionality
soup = Soup(my_url)
soup_text = str(soup.text)
p_canales = json_object['Cable']['Canales']
p_word = 'price'
pattern = re.compile(p_canales)
matches = pattern.finditer(soup_text)

for match in matches:
    print(match.group(0))
