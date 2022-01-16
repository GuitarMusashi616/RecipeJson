class Parser:
    @staticmethod
    def split_into_num_str(string):
        """Takes a string like '60 Copper Ingot' and returns (60, 'Copper Ingot')"""
        for i in range(1, len(string) + 1):
            try:
                int(string[:i])
            except ValueError:
                return int(string[:i - 1]), string[i - 1:]

    @staticmethod
    def split(string, symbol):
        """splits the string on symbol, each split is stripped of whitespace"""
        return [x.strip() for x in string.split(symbol)]

    @classmethod
    def res_list_into_dict(cls, ls):
        """Takes a list like ['60 Copper Ingot', '120 Iron Ingot'] and returns a dict {60:'Copper Ingot', 120:'Iron Ingot'}"""
        if type(ls) is not list:
            ls = cls.split(ls, ',')

        dic = {}
        for num_item in ls:
            num, item = cls.split_into_num_str(num_item)
            dic[item] = num

        return dic

    @classmethod
    def recipe_str_into_dicts(cls, string):
        return [cls.res_list_into_dict(x) for x in cls.split(string, '->')]