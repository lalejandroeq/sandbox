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
        self.current_row = row
        self.__row = self.current_row
        self.__operations_dict = {"=": op.eq,
                                  "!=": op.ne,
                                  "<": op.lt,
                                  "<=": op.le,
                                  ">": op.gt,
                                  ">=": op.ge}

    # *****Private methods*****
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

    # *****Public methods*****
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
        return self.__row


class RelationalQuery(RelationalGen, RelationalOps):
    def __init__(self, matrix, header, query_path):
        RelationalGen.__init__(self, matrix, header)
        self.__relational_generator = self.relational_generator
        self.__query = get_json_object(query_path)
        self.generator_memory = []
        self.distinct_memory = []
        self.query_results = self.__implement_results()

    # *****Private methods*****
    def __store_generator(self):
        if self.get_row() is not None:
            self.generator_memory.extend([self.get_row()])

    def __distinct_generator(self):
        if not any(self.get_row() in x for x in [None, self.distinct_memory]):
            self.distinct_memory.extend([self.get_row()])

    def __try_select(self):
        try:
            column_list = self.__query["select"]["columns"]
            self.select_columns(column_list)
        except IndexError:
            pass

    def __try_filter(self):
        try:
            column_indexes = self.__query["filters"]["column"]
            values_to_filter = self.__query["filters"]["value"]
            operator_inputs = self.__query["filters"]["operation"]
            self.filter_row(column_indexes, values_to_filter, operator_inputs)
        except IndexError:
            pass

    def __get_distinct(self):
        distinct_flag = self.__query["distinct"] == "True"
        return distinct_flag

    def __implement_results(self):
        if self.__get_distinct():
            return self.distinct_memory
        else:
            return self.generator_memory

    # *****Public methods*****
    def execute_query(self):
        for gen_row in self.__relational_generator:
            RelationalOps.__init__(self, gen_row)
            self.__try_select()
            self.__try_filter()
            if not self.__get_distinct():
                self.__store_generator()


if __name__ == '__main__':
    sample_matrix = [["a", "b", "c", "d"],
                     ["1", "0", "2", 8],
                     ["1", "0", "4", 6],
                     ["1", "0", "4", 6],
                     ["1", "0", "2", 6],
                     ["1", "0", "2", 4],
                     ["1", "0", "2", 2]]

    # Queries could eventually be threaded
    query_url = "configuration_files/query.json"
    relational_query = RelationalQuery(sample_matrix, True, query_url)
    relational_query.execute_query()
    results = relational_query.query_results
    print(results)
