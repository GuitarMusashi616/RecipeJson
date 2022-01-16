from facmaker.stockpile import Stockpile


class Factory:
    collection = []

    def __init__(self, req, prod):
        self._req = Stockpile(req)
        self._prod = Stockpile(prod)
        self.collection.append(self)

    def __repr__(self):
        return f"{self.req} -> {self.prod}"

    @property
    def req(self):
        return self._req

    @property
    def prod(self):
        return self._prod

    @staticmethod
    def fac_list_to_dict(fac_ls):
        """Returns a dict of name:facmaker for use in the FacMaker"""
        if type(fac_ls) is dict:
            return fac_ls
        return {next(iter(x.prod)): x for x in fac_ls}
