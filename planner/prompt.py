class Prompt:
    @staticmethod
    def get_int(prompt, not_valid):
        choice = "invalid"
        while type(choice) is str:
            choice = input(prompt)
            assert choice != 'q', "quit"
            try:
                choice = int(choice.strip())
            except ValueError:
                print(not_valid)
        return choice

    @staticmethod
    def get_yes_no(prompt, not_valid="type a y or n"):
        choice = input(prompt)
        assert choice != 'q', "quit"
        while choice not in {'y','n'}:
            print(not_valid)
            choice = input(prompt)
            assert choice != 'q', "quit"

        return choice == 'y'

    @staticmethod
    def pick_choice(prompt, options):
        choice = Prompt.get_int(prompt, f"enter a number between 0 and {len(options) - 1}")
        return options[choice]