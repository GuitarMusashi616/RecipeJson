import json

from IPython.core.display import display


class Search:
    recipes_json = json.load(open("resources/recipes.json"))
    tags_json = json.load(open("resources/tags.json"))

    @classmethod
    def base_search(cls, key, val, verbose=True):
        output = [x for x in cls.recipes_json if x[key] == val]
        if verbose:
            display(output)
        return output

    @classmethod
    def search_display_name(cls, displayName, verbose=True):
        return cls.base_search('outputDisplayName', displayName, verbose)

    @classmethod
    def search_item(cls, name, verbose=True):
        return cls.base_search('outputName', name, verbose)

    @classmethod
    def search_tag(cls, tag, verbose=True):
        assert tag in cls.tags_json, f"{tag} not found"
        if verbose:
            print(cls.tags_json[tag])
        return cls.tags_json[tag]