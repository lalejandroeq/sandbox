from read_config import get_json_object
import operator as op


class RelationalGen:
    """
    Class will create generator for children to perform operations in one iteration
    Rows iteration could eventually be threaded
    """
    def __init__(self, matrix, header):
        self.__header = header
        self.__relational_matrix = matrix
        self.relational_generator = self.__create_generator()
        self.headers_dict = self.__get_headers()

    # *****Private methods*****
    def __get_headers(self):
        if self.__header:
            headers = next(self.relational_generator)
            headers_dict = {key: index for index, key in enumerate(headers)}
        else:
            headers_dict = None
        return headers_dict

    def __create_generator(self):
        self.__generator = (row for row in self.__relational_matrix)
        return self.__generator


class RelationalOps:
    # Methods will be designed to perform at row level to alter generator on 1 iteration
    def __init__(self, row):
        self.__row = row
        self.__operations_dict = {"=": op.eq,
                                  "!=": op.ne,
                                  "<": op.lt,
                                  "<=": op.le,
                                  ">": op.gt,
                                  ">=": op.ge}

    def __filter_handling(self, column_index, value_to_filter, operator_input):
        try:
            if not self.__operations_dict[operator_input](self.__row[column_index], value_to_filter):
                self.__row = None
        except IndexError:
            raise Exception("Column does not exist: error found while filtering column {}"
                            .format(column_index))
        except TypeError:
            raise Exception("Can't compare string and integer: error found while comparing {} & {}"
                            .format(self.__row[column_index], value_to_filter))
        except KeyError:
            raise Exception("Operation {} not available in list of operations"
                            .format(operator_input))

    def select_columns(self, col_list):
        if len(col_list) == 1:
            self.__row = self.__row[col_list[0]]
        else:
            self.__row = list(op.itemgetter(*col_list)(self.__row))

    def filter_row(self, column_indexes, values_to_filter, operator_inputs):
        counter = 0
        while True:
            if self.__row is None:
                break
            try:
                column_index = column_indexes[counter]
                value_to_filter = values_to_filter[counter]
                operator_input = operator_inputs[counter]
            except IndexError:
                break
            self.__filter_handling(column_index, value_to_filter, operator_input)
            counter += 1

    def get_row(self):
        if self.__row is not None:
            return self.__row
        else:
            pass


# class RelationalQuery(RelationalGen, RelationalOps):
#     def __init__(self, matrix, header):
#         RelationalGen.__init__(self, matrix, header)
#         self.__relational_generator = self.relational_generator
#
#     def execute_query(self):
#         for gen_row in self.__relational_generator:
#             RelationalOps.__init__(gen_row)


# class ReadQuery(RelationalGen):
#
#     def __init__(self, matrix, query_config):
#         RelationalGen.__init__(self, matrix, query_config)
#
#     # *****Public methods*****
#     def private get_select_columns(self, col_list):
#     # *****Public methods*****
#     def execute_query(self):
#         for row in self.relational_generator:
#             try:
#                 self.query["select"]["columns"]


if __name__ == '__main__':
    sample_matrix = [["a", "b", "c", "d"],
                     ["1", "0", "2", 8],
                     ["1", "0", "4", 6],
                     ["1", "0", "2", 6],
                     ["1", "0", "2", 4],
                     ["1", "0", "2", 2]]

    # Queries could eventually be threaded
    query_path = "configuration_files/query.json"
    query = get_json_object(query_path)
    relational_gen = RelationalGen(sample_matrix, header=True)
    relational_generator = relational_gen.relational_generator
    relational_headers = relational_gen.headers_dict
    for in_row in relational_generator:
        if in_row is not None:
            column_selection = query["select"]["columns"]
            filter_param_1 = query["filters"]["column"]
            filter_param_2 = query["filters"]["operation"]
            filter_param_3 = query["filters"]["value"]
            relational_row = RelationalOps(in_row)
            relational_row.select_columns(column_selection)
            relational_row.filter_row(filter_param_1, filter_param_3, filter_param_2)
            processed_row = relational_row.get_row()
            print(processed_row)
