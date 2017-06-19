import argparse
import os
from pylint import epylint as lint


class Main(object):
    """Main class of module

    This class includes the main routine of module.

    Attributes:
        None
    """
    def __init__(self, target_path=None):
        """Initializer of the class

        This method finds a root of the project which includes this script,
        sets the target directory/file for pylint and commandline parser.
        Project root is the nearest successor directory of this script
        which contains the `.git` directory.

        Args:
            target_path (Optional[str, None]): Target directory/path for pylint.
                It will be interpreted from project root.
        """
        root = os.getcwd()
        while ".git" not in os.listdir(root):
            root = os.path.dirname(root)
            if root == os.path.abspath(os.sep):
                raise SystemError("It seems script is not running in git project")
        self._project_root = root
        self._target_path = target_path

        self._parser = argparse.ArgumentParser(description="Pylint runner")
        self._parser.add_argument(
            "-t", "--target", dest="target_path",
            help="Target directory or file from project root.\
            For example, if `app/main.py` is given, file of\
            (project_root)/app/main.py is tested"
        )

    def run(self):
        """Main routine of module

        This method simply runs pylint for every target directory/file

        Args:
            None
        """
        if __name__ == "__main__":
            args = self._parser.parse_args()
            self._target_path = args.target_path
        pylint_options = " --rcfile=" + self._project_root + os.sep + "pylintrc " +\
                "--msg-template='{C}: {line:3d},{column:2d}: {category} ({msg_id}, \
{obj}) {msg} ({symbol})'"

        if self._target_path is None:
            self._target_path = "."
        lint.py_run(self._project_root + os.sep + self._target_path + pylint_options)

if __name__ == "__main__":
    Main().run()
