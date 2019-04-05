import os
from colorama import init, Fore, Back, Style

init(autoreset=True)

LOCALS = {
    "eng": {
        "hint": "Enter \"help\" for functions description.",
        "help": "displays info about functions",
        "clear": "clears the console",
        "exit": "closes the app",
        "args_error": "Enter the required number of arguments.",
        "error": "Error",
        "unknown_command": "Unknown command."
    },
    "ukr": {
        "hint": "Введіть \"help\" для опису всіх функцій.",
        "help": "відображає інформацію про всі функції",
        "clear": "очищає консоль",
        "exit": "закриває вікно",
        "args_error": "введіть потрібну кількість елементів.",
        "error": "Помилка:",
        "unknown_command": "Невідома команда."
    }
}

class Method:
    """Оболочка для функции используемой в приложении.

    Имеет описание, саму функцию, и может быть inline,
    то есть принимать в себя аргументы.
    """
    def __init__(self, descr, function, inline=False):
        self.descr = descr
        self.function = function
        self.inline = inline

class ConsoleApp:
    def __init__(
        self,
        title: str = "ConsoleApp",
        subTitle: str = None,
        printHead: bool = True,
        printMethods: bool = False,
        width: int = 45,
        maxMethodLen: int = 9,
        onStart = None,
        onExit = None,
        lang = "eng",
        **kwargs
    ):
        self.__title = title
        self.__subTitle = subTitle
        self.__printHead = printHead
        self.__printMethods = printMethods
        if width < 40:
            self.__width = 40
        else:
            self.__width = width
        if maxMethodLen < 5:
            self.__maxMethodLen = 6
        else:
            self.__maxMethodLen = maxMethodLen + 1
        self.__onStart = onStart
        self.__onExit = onExit
        if LOCALS.get(lang) is None:
            self.__lang = "eng"
        else:
            self.__lang = lang
        self.__methods = kwargs

    def changeSubTitle(self, newSub: str):
        self.__subTitle = newSub
        self.__clear()

    def __printLine(self):
        print("─" * self.__width)

    def __helpMethod(self):
        for title, method in self.__methods.items():
            print("{0:>{2}} - {1}".format(title, method.descr, self.__maxMethodLen))
        print("{0:>{2}} - {1}".format("help", LOCALS[self.__lang]["help"], self.__maxMethodLen))
        print("{0:>{2}} - {1}".format("clear", LOCALS[self.__lang]["clear"], self.__maxMethodLen))
        print("{0:>{2}} - {1}".format("exit", LOCALS[self.__lang]["exit"], self.__maxMethodLen))

    def __printMethodsFunc(self):
        if not self.__printHead:
            self.__printLine()

        methods = list(self.__methods.keys())
        methods.extend(["help", "clear", "exit"])
        for index, method in enumerate(methods):
            if not (index + 1) % (self.__width // self.__maxMethodLen) or index == len(methods) - 1:
                print(f"{method:<{self.__maxMethodLen}}")
            else:
                print(f"{method:<{self.__maxMethodLen}}", end="")

        self.__printLine()

    def __printHeadFunc(self):
        print(Fore.CYAN + f"{self.__title:^{self.__width}}")
        if self.__subTitle:
            print(Fore.GREEN + f"{self.__subTitle:^{self.__width}}")
            
        hint = LOCALS[self.__lang]["hint"]
        print(f"{hint:^{self.__width}}")
        self.__printLine()

    def __clear(self):
        os.system("cls")
        if self.__printHead:
            self.__printHeadFunc()
        if self.__printMethods:
            self.__printMethodsFunc()

    def run(self):
        os.system(f"mode con cols={self.__width} lines={self.__width//2}")

        if self.__printHead:
            self.__printHeadFunc()
        if self.__printMethods:
            self.__printMethodsFunc()
        if self.__onStart:
            try:
                self.__onStart()
            except Exception as exc:
                print(Fore.RED + LOCALS[self.__lang]["error"], exc)

        while True:
            userInput = str(input(">"))
            userInput = userInput.split()

            try:
                command = userInput[0]
            except IndexError as exc:
                command = ""

            method = self.__methods.get(command)
            if method is not None:
                self.__printLine()
                if not method.inline:
                    try:
                        method.function()
                    except Exception as exc:
                        print(Fore.RED + LOCALS[self.__lang]["error"], exc)
                else:
                    try:
                        method.function(userInput[1:])
                    except IndexError as exc:
                        print(Fore.YELLOW + LOCALS[self.__lang]["args_error"])
                    except Exception as exc:
                        print(Fore.RED + LOCALS[self.__lang]["error"], exc)
                self.__printLine()
            elif command == "exit":
                if self.__onExit:
                    try:
                        self.__onExit()
                    except Exception as exc:
                        print(Fore.RED + LOCALS[self.__lang]["error"], exc)
                break
            elif command == "help":
                self.__printLine()
                self.__helpMethod()
                self.__printLine()
            elif command == "clear":
                self.__clear()
            else:
                print(LOCALS[self.__lang]["unknown_command"])