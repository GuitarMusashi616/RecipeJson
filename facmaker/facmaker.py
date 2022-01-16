import networkx as nx

from facmaker.facgraph import FacGraph
from facmaker.factory import Factory
from facmaker.stockpile import Stockpile


class FacMaker:
    def __init__(self, resources, todo_stack, factory_options):
        self.resources = Stockpile(resources)
        self.buildings = Stockpile()
        self.todo_stack = todo_stack
        self.factory_options = Factory.fac_list_to_dict(factory_options)

    @staticmethod
    def find_least_fulfilled(req, res):
        """given requirements and available resources find the least fulfilled required item"""
        least_fulfilled = (1, None)
        for item in req:
            try:
                percent_fulfilled = res[item] / req[item]
            except KeyError:
                percent_fulfilled = 0

            if percent_fulfilled < least_fulfilled[0]:
                least_fulfilled = (percent_fulfilled, item)
        return least_fulfilled

    def graph(self, pos_func=nx.spectral_layout):
        fg = FacGraph(pos_func)
        for building, num in self.buildings.items():
            fg.add(building, num)
        print(list(nx.topological_sort(fg.G)))
        fg.show()

    def report(self):
        for building, amount in self.buildings.items():
            print(f"{amount} {building}")

    def print_outputs(self):
        for item, amount in self.resources.items():
            if 0 < amount < 5000:
                print(f"{amount}x {item}")

    def construct(self, pos_func=nx.planar_layout, verbose=False):
        """
        attempt to make all factories in the todo stack,
        if materials are not available to make factory, add a prerequisite factory to the stack and repeat
        """
        while self.todo_stack:
            # print(f"\nNew Round: {[next(iter(x.prod)) for x in self.todo_stack]}")
            constr_goal = self.todo_stack[-1]
            _, least_fulfilled_item = self.find_least_fulfilled(constr_goal.req, self.resources)
            if least_fulfilled_item is None:
                building = self.todo_stack.pop()
                self.buildings.add(building, 1)
                self.resources -= building.req
                self.resources += building.prod
                # print(f"Building {building}, Stockpile: {self.resources}")
            else:
                if least_fulfilled_item not in self.factory_options:
                    # print("Out of Materials")
                    break
                self.todo_stack.append(self.factory_options[least_fulfilled_item])
                # print(f"Least Fulfilled is {least_fulfilled_item} so now constructing {self.factory_options[least_fulfilled_item]}")
        if verbose:
            self.report()
        self.graph(pos_func)



