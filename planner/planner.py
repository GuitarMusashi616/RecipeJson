from planner.prompt import Prompt
from planner.search import Search


class Planner:
    def __init__(self):
        self.raw_materials = set()
        self.unique_items = set()
        self.unique_tags = set()
        self.target_recipe = None
        self.target_amount = 1
        self.item_to_recipe = {}
        self.tag_to_item = {}

    def prompt_link_recipe(self, display_name):
        self.target_recipe = self.ask_which_recipe(display_name)
        self.add_new_ingredients(self.target_recipe)

    @staticmethod
    def ask_which_recipe(name, skip_solo_recipes=True, skip_non_crafting=True):
        print(f"which recipe for {name}")
        func = Search.search_item
        if any(x.isupper() for x in name):
            func = Search.search_display_name
        options = func(name, False)

        if skip_non_crafting:
            options = [x for x in options if x['type'] == 'crafting']

        if skip_solo_recipes and len(options) == 1 and options[0]['type'] == 'crafting':
            print(f"picked {options[0]['ingredients']}")
            return options[0]

        for i, option in enumerate(options):
            print(f"{i}) {option['type']} {option['ingredients']}")

        return Prompt.pick_choice("\npick a recipe: ", options)

    @staticmethod
    def ask_which_item(tag, skip_solo_tags=True):
        print(f"which item for {tag}?")
        options = Search.search_tag(tag, False)
        if skip_solo_tags and len(options) == 1:
            print(f"picked {options[0]}")
            return options[0]

        for i,option in enumerate(options):
            print(f"{i}) {option}")
        return Prompt.pick_choice("\npick a tag: ", options)

    def ask_if_raw(self, unique_item):
        if Prompt.get_yes_no(f"\ncount {unique_item} as a raw material (y/n)? "):
            self.raw_materials.add(unique_item)
        else:
            recipe = self.ask_which_recipe(unique_item)
            self.item_to_recipe[unique_item] = recipe
            self.add_new_ingredients(recipe)

    # def ask_about_tag(self, unique_tag):
    #     item = self.ask_which_item(unique_tag)
    #     self.tag_to_item[unique_tag] = item
    #     self.add_new_ingredient(item)

    def add_new_ingredients(self, recipe):
        for ing in recipe['ingredients']:
            if len(ing) > 1:
                print(f"more than 1 ing {ing}")
            elif len(ing) == 1:
                self.add_new_ingredient(ing)

    def add_new_ingredient(self, ing):
        if 'item' in ing:
            item = ing['item']
            if item not in self.item_to_recipe and item not in self.raw_materials:
                self.unique_items.add(item)
        elif 'tag' in ing:
            tag = ing['tag']
            if tag not in self.tag_to_item:
                self.unique_tags.add(tag)
        else:
            print(f"could not add {ing}")

    def plan(self, display_name):
        # get which recipe from display name
        # add each ing to list
        # prompt about each unique ing with multiple options

        self.prompt_link_recipe(display_name)

        while self.unique_items or self.unique_tags:
            if self.unique_items:
                item = self.unique_items.pop()
                self.ask_if_raw(item)
            else:
                tag = self.unique_tags.pop()
                item = self.ask_which_item(tag)
                self.tag_to_item[tag] = item
                self.ask_if_raw(item)

    def __repr__(self):
        return f"{self.raw_materials}\n{self.target_amount}x {self.target_recipe}\n\n{self.unique_items}\n{self.unique_tags}\n\n{self.item_to_recipe}"
