import operator as op
import csv


class RelationalMagic:
    """
    Class for handling table (matrix) structures, applying relational-like methods
        :Example:
            sample_matrix = [["a", "b", "c", "d"],
                             ["1", "0", "2", 8],
                             ["1", "0", "2", 6],
                             ["1", "0", "2", 4],
                             ["1", "0", "2", 2]]

            magic = RelationalMagic(sample_matrix)
            magic.filter_data(3, "4", "=")
            magic.print_relational
                ["1", "0", "2", 4]

    """
    def __init__(self, matrix):
        self.__relational_matrix = matrix
        self.__relational_matrix_copy = self.__relational_matrix.copy()
        self.__operations_dict = {"=": op.eq,
                                  "!=": op.ne,
                                  "<": op.lt,
                                  "<=": op.le,
                                  ">": op.gt,
                                  ">=": op.ge}

    # *****Private methods*****
    @staticmethod
    def assign_rank(rank, row):
        row.append(rank)
        return row

    # *****Public methods*****
    def get_relational(self):
        return self.__relational_matrix

    def print_relational(self, print_limit=100):
        for row in self.__relational_matrix[:print_limit]:
            print(row)

    def add_rank(self):
        self.__relational_matrix = [self.assign_rank(x, y) for x, y in enumerate(self.__relational_matrix)]

    def select_columns(self, col_list):
        if len(col_list) == 1:
            self.__relational_matrix = [row[col_list[0]] for row in self.__relational_matrix]
        else:
            self.__relational_matrix = [list(op.itemgetter(*col_list)(row)) for row in self.__relational_matrix]

    def select_distinct_column(self, col_value):
        seen = set()
        seen_add = seen.add
        self.__relational_matrix = [row[col_value[0]] for row in self.__relational_matrix
                                    if not (row[col_value[0]] in seen or seen_add(row[col_value[0]]))]

    def limit_rows(self, row_s_index, row_e_index):
        self.__relational_matrix = self.__relational_matrix[row_s_index:row_e_index]

    def filter_data(self, column_index, filter_value, operator_input):
        try:
            self.__relational_matrix = [row for row in self.__relational_matrix
                                        if self.__operations_dict[operator_input](row[column_index], filter_value)]
        except IndexError:
            raise Exception("Column does not exist: error found while filtering column {}"
                            .format(column_index))

        except TypeError:
            raise Exception("Can't compare string and integer: error found while filtering column {}"
                            .format(column_index))

    def runtime_rollback(self):
        self.__relational_matrix = self.__relational_matrix_copy

    def export_to_csv(self,
                      file_name="Processed_Magic",
                      folder="C:/Users/Ale/Documents/Python Projects/Crawling/Sandbox_Folder"):
        file_name_format = file_name + '.csv'
        file_path = '/'.join([folder, file_name_format])
        print(file_path)
        with open(file_path, 'w+', encoding="utf-8", newline='') as f:
            writer = csv.writer(f)
            writer.writerows(self.__relational_matrix)
