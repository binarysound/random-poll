import argparse
import sys
import os
import subprocess
from enum import Enum, auto

from tests import test_pylint


class EnvParser(object):
    """Parser class for .env file

    This class has function `parse`, which parses the .env file
    and returns a dictionary containing configuration values.

    Attributes:
        None
    """
    def __init__(self):
        """__init__ method

        Initializer of the class

        Args:
            None
        """
        pass

    @staticmethod
    def parse(env_file):
        """Parsing function

        Parse the given .env file and return the dictionary

        Args:
            env_file (str): relative path to .env file

        Returns:
            (dict): Dictionary from parsing result
        """
        env = {}
        with open(env_file, "r") as f:
            for line in f:
                if line[0] == "#":
                    continue  # This is comment line
                parsed = line.strip().split("=")
                if len(parsed) != 2:
                    raise RuntimeError("Ill-formed .env file")
                env[parsed[0]] = parsed[1]
        return env


class AppManager(object):
    """The class which parses the command and run commands

    This class processes the main routine of this manage.py.
    parse_and_run() parses the given arguments and executes
    the appropriate routine for given arguments

    Attributes:
        AVAILABLE_SUBCOMMANDS ([str]): list of available subcommands
            for manage.py
    """
    AVAILABLE_SUBCOMMANDS = ["run", "test"]

    def __init__(self):
        """__init__ method

        Initializer of the class. This function initializes
        parser for manage.py

        Args:
            None
        """
        self._parser = argparse.ArgumentParser(
            description="Manage the random-poll app",
            usage="""manage.py <subcommand> [<args>]

Available subcommands are:
run         Run the Flask web server
test        Test the module (see manage.py test -h)
                """)
        self._parser.add_argument("subcommand", help="Subcommand to run")

    def parse_and_run(self):
        """Function for parsing and running subcommands

        This function parses the given argument and run
        appropriate function according to given subcommand.
        If subcommand is not available, it raises `ValueError`

        Args:
            None
        """
        args = self._parser.parse_args(sys.argv[1:2])
        if args.subcommand not in AppManager.AVAILABLE_SUBCOMMANDS:
            raise ValueError("Unrecognized subcommand")
        getattr(self, args.subcommand)()

    def print_help(self):
        """Function for printing help message of manage.py

        Args:
            None
        """
        self._parser.print_help()

    # Functions for running subcommands
    @staticmethod
    def run():
        """Function called when `run` subcommand is given

        This function runs the flask web server (app/main.py) in
        unbuffered output mode.

        Args:
            None
        """
        parser = argparse.ArgumentParser(
            description="Run the Flask web server",
            usage="manage.py run [<args>]"
        )
        args = parser.parse_args(sys.argv[2:])
        env = EnvParser.parse(".env")

        os.chdir("./app/")
        subprocess.call(["python", "-u", "main.py", "--db-password", env["DB_PASSWORD"]])

    @staticmethod
    def test():
        """Function called when `test` subcommand is given

        This functions runs the module in `tests/` according to
        the given options.

        Args:
            None
        """
        class Args(Enum):
            """An enum class representing argument is given or not"""
            NOT_GIVEN = auto()

        parser = argparse.ArgumentParser(
            description="Run the test",
            usage="manage.py test [<args>]"
        )
        parser.add_argument(
            "-l", "--lint", nargs="?", metavar="FILE", default=Args.NOT_GIVEN,
            help="Run pylint for given file. If file is not given,\
            every file in project will be tested."
        )
        args = parser.parse_args(sys.argv[2:])

        if args.lint != Args.NOT_GIVEN:
            test_pylint.Main(args.lint).run()
        else:
            pass  # Run test_full.py


if __name__ == "__main__":
    manager = AppManager()
    try:
        manager.parse_and_run()
    except ValueError as e:
        print(e)
        manager.print_help()
