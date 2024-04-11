import os
from optparse import Option


class Console(object):
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError("Implement this method")

    def clear(self):
        os.system('cls' if os.name == 'nt' else 'clear')


class Application(object):

    def __init__(self, start: Console):
        self._console: Console = start
        self._is_running = False

    def set_console(self, console: Console):
        self._console = console

    def stop(self):
        self._is_running = False

    def run(self):
        self._is_running = True
        while self._is_running:
            self._console = self._console.run()


class Menu(Console):
    def __init__(self, title):
        super().__init__()
        self._title = title
        self._options = []
        self._width = 50

    def __iter__(self):
        return iter(self._options)

    def get_options(self) -> list:
        return self._options

    def add_option(self, option: Option):
        self._options.append(option)

    def remove_option(self, option: Option):
        self._options.remove(option)

    def show(self):
        print("#" * self._width)
        left = "# "
        right = "#"
        space = " " * (self._width - len(left) - len(self._title) - len(right))
        print(f"{left}{self._title}{space}{right}")
        print("#" * self._width)
        for i, option in enumerate(self, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("#" * self._width)

    def run(self) -> Console:
        self.clear()
        self.show()
        return self._navigation(self.make_choice())

    def make_choice(self) -> int:
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            self.show()
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigation(self, choice: int):
        raise NotImplementedError("Implement this method")


class MenuOption(object):
    def __init__(self, title):
        self._title = title

    def get_title(self) -> str:
        return self._title

    def __str__(self):
        return self._title

    def __len__(self):
        return len(self._title)