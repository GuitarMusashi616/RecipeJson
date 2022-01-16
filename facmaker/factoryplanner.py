import networkx as nx

from facmaker.facmaker import FacMaker
from facmaker.factory import Factory
from facmaker.parser import Parser
from facmaker.stockpile import Stockpile


class FactoryPlanner:
    def __init__(self):
        self.resources = Stockpile()
        self.todo_stack = []
        self.factory_options = []

    def add_resource(self, res_str):
        for item, amount in Parser.res_list_into_dict(res_str).items():
            self.resources.add(item, amount)

    def add_recipe(self, recipe_str):
        left_side, right_side = Parser.recipe_str_into_dicts(recipe_str)
        self.factory_options.append(Factory(left_side, right_side))

    def find_recipe_for(self, res_name):
        for fac in self.factory_options:
            if res_name in fac.prod:
                return fac

    def blueprint_for(self, res_names, layout=nx.planar_layout):
        """Trying to make it so only resource name you want to maximize is required to create the factory plan"""
        target_recipes = [self.find_recipe_for(res_name.strip()) for res_name in res_names.split(',')]
        self.graph(target_recipes, layout)

    def target_output(self, res_str):
        res_dict = Parser.res_list_into_dict(res_str)
        fake_fac = Factory(res_dict, {})
        self.graph([fake_fac])

    def graph(self, target_recipes, layout=nx.planar_layout):
        fm = FacMaker(self.resources, target_recipes, self.factory_options)
        fm.construct(layout, True)
        fm.print_outputs()

