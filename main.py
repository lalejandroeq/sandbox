from bs_craping import TagDetails, Soup
from new_relational import RelationalQuery
from exporting import export_matrix


def get_relational_tags(url, parser='lxml', filters_list=None):
    """
    Main method, builds tags relational matrix
    :return: relational matrix [tag name, class name, tag style, text flag, raw_text]
    """
    tags = TagDetails(url, parser=parser, filters_list=filters_list)
    relational_soup = [list(row)for row in zip(tags.get_tag_names(),
                                               tags.get_tag_classes(),
                                               tags.get_tag_styles(),
                                               tags.get_text_flags(),
                                               tags.get_tag_texts())]

    return relational_soup


my_url = "https://movistar.cr/tv"

# # Testing soup functionality
# soup = Soup(my_url)
# soup_text = soup.text
# print(soup_text)

# Testing hidden tags filters
filter_list = ['[style="display: none;"]']
relational_tags = get_relational_tags(my_url, filters_list=filter_list)
print(relational_tags)
query_url = "configuration_files/query.json"
relational_magic = RelationalQuery(relational_tags, query_url)
relational_magic.execute_query()
matrix = relational_magic.query_results
print(matrix)
# export_matrix('matrix_test', matrix)


