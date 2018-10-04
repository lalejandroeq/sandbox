import re
from bs_craping import Soup


my_url = "https://movistar.cr/tv"

# Testing soup functionality
soup = Soup(my_url)
soup_text = str(soup.text)
p_canales = r'\d+\scanales*'
p_word = 'price'
pattern = re.compile(p_word)
matches = pattern.finditer(soup_text)

for match in matches:
    print(match.group(0))
