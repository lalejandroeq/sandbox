import xlrd as xl
from re import findall as re_findall


class ExcelOperations:

    def __init__(self, excel_path, encoding="UTF-8"):
        self.encoding = encoding
        self.__excel_path = excel_path
        self.__excel = self.__open_excel()
        self.__current_sheet = self.__excel.sheet_by_index(0)

    ##################
    # Private Methods
    ##################

    def __open_excel(self):
        return xl.open_workbook(self.__excel_path, encoding_override=self.encoding)

    #############################################
    # Methods are mainly used for find_table()

    def __get_cell_value(self, row, col):
        return self.__current_sheet.cell(row, col).value

    def __get_table_corners(self):
        max_row, max_col = self.__current_sheet.nrows, self.__current_sheet.ncols
        return max_row, max_col

    def __get_col_list(self, current_row, start_col, max_col):
        col_list = [self.__get_cell_value(current_row, current_col) for current_col in range(start_col, max_col)]
        return col_list

    #############################################

    @staticmethod
    def __std_coordinate(xl_coordinate):
        letters = re_findall("[a-zA-Z]", xl_coordinate.lower())
        row_index = int(''.join(re_findall("[0-9]", xl_coordinate.lower()))) - 1
        loop_counter, col_index, alphabet_loop, ord_conversion = 0, 0, 25, 96
        for letter in letters:
            carry_value = alphabet_loop * loop_counter
            col_index += ord(letter) - ord_conversion + carry_value
            loop_counter += 1
        col_index -= 1
        return row_index, col_index

    ##################
    # Public Methods
    ##################

    def get_current_sheet_name(self):
        return self.__current_sheet.name

    def move_to_sheet(self, sheet_name):
        self.__current_sheet = self.__excel.sheet_by_name(sheet_name)

    def find_table(self, start_row=0, start_col=0, max_row=True, max_col=True, header=True):
        if max_row and max_col:
            max_row, max_col = self.__get_table_corners()
        else:
            max_row, max_col = max_row, max_col
        row_list = [self.__get_col_list(row, start_col, max_col) for row in range(start_row, max_row)]
        if header:
            headers, table = row_list[0], row_list[1:]
        else:
            headers, table = None, row_list
        return headers, table

    def get_cell_value(self, excel_cell):
        row, col = self.__std_coordinate(excel_cell)
        try:
            return self.__current_sheet.cell(row, col).value
        except IndexError:
            return None

    def smart_find_table(self):
        # Search for a table, being blank cell agnostic
        pass
