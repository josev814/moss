import os

class AssignmentCollector:
    """
    Class to pull assignments
    """

    __ASSIGNMENTS_DIR = None
    __RESULT_PREFIX = None

    def __init__(self, assignments_dir:str, result_prefix:str|None = None):
        """
        Initializes the Assignments collector

        :param assignments_dir: the path to the assignments directory
        :type assignments_dir: str
        :param result_prefix: the prefix to set for a filename of the results
        :type result_prefix: str
        """
        self.__ASSIGNMENTS_DIR = assignments_dir
        if result_prefix:
            self.__RESULT_PREFIX = result_prefix

    # Step 1: Read files and preprocess code
    def read_files(self, file_paths:list) -> list:
        """
        Reads the contents of the files and returns them in a list

        :param file_paths: The files we're reading
        :type file_paths: list
        :return: list of strings where the strings are the contents of each file
        :rtype: list
        """
        code_snippets = []
        for file_path in file_paths:
            with open(file_path, 'r') as file:
                code = file.read()
                # Preprocess code (remove comments, normalize, etc.)
                code_snippets.append(self.preprocess_code(code))
        return code_snippets


    def preprocess_code(self, code: str) -> str:
        """
        Simple preprocessing to remove comments and normalize whitespace
        This should be improved on

        :param code: The raw contents of the file
        :type code: str
        :return: We return the string as a single line with no comments
        :rtype: str
        """
        clean_lines = []
        comment_block = False
        for line in code.splitlines():
            strip_line = line.strip()
            if len(strip_line) == 0:
                continue
            if strip_line[0] in ['#']:
                continue
            if strip_line.startswith('"""'):
                comment_block = '"""'
                if strip_line.endswith(comment_block):
                    # single line comment
                    comment_block = False
                continue
            if comment_block:
                # Currently in a comment block
                if (strip_line.startswith(comment_block) or strip_line.endswith(comment_block)):
                    # End of comment block
                    comment_block = False
                continue
            clean_lines.append(strip_line)
        return ' '.join(clean_lines)


    def collect_assignments(self) -> list[list[str], str]:
        """
        Collects all assignment files

        :return: Returns a list of the assignments broken down by the assignment dir along with a list of strings of where to save the results to
        :rtype: list[list[str], str]
        """
        file_paths = []
        save_paths = []
        for language_dir in os.scandir(self.__ASSIGNMENTS_DIR):
            if not language_dir.is_dir():
                continue
            for assignment_dir in os.scandir(language_dir.path):
                if not assignment_dir.is_dir():
                    continue
                if self.__RESULT_PREFIX:
                    result_path = os.path.join(assignment_dir.path, self.__RESULT_PREFIX)
                    if not os.path.isdir(result_path):
                        os.mkdir(result_path)
                files_to_compare = []
                for entry in os.scandir(assignment_dir.path):
                    if entry.is_file() and entry.name.endswith('.py'):
                        files_to_compare.append(entry.path)
                if len(files_to_compare) > 0:
                    file_paths.append(
                        files_to_compare
                    )
                    if self.__RESULT_PREFIX:
                        save_paths.append(
                            result_path
                        )
        return file_paths, save_paths