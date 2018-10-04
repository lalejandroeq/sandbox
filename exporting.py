import csv


def export_soup(file_name, matrix_content, folder="ouput_box"):
    file_name_format = file_name + '.csv'
    file_path = '/'.join([folder, file_name_format])
    print(file_path)
    with open(file_path, 'w+', encoding="utf-8", newline='') as f:
        writer = csv.writer(f)
        writer.writerows(matrix_content)
