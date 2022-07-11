from typing import List, Callable, Any, Set, Generic

from .producer import InputFileDatatype, OutputFileDatatype


################################################################################
# Creator
#
# This is a static pairing of input files to output files. These are
# constructed and managed fully behind the scenes and should not be implemented
# by users directly. Producers are in charge of constructing them and Studios
# are in charge of managing them after their creation.
################################################################################
class Creator(Generic[InputFileDatatype, OutputFileDatatype]):
    ############################################################################
    #
    ############################################################################
    def __init__(
        self,
        input_paths: InputFileDatatype,
        output_paths: OutputFileDatatype,
        function: Callable[[InputFileDatatype, OutputFileDatatype], None],
        categories: List[str],
    ):
        self.input_paths: InputFileDatatype = input_paths
        self.output_paths: OutputFileDatatype = output_paths
        self.function: Callable[[InputFileDatatype, OutputFileDatatype], None] = function
        self.categories: List[str] = categories

        # Pre-cache the input files in a set for very fast file lookups.
        self._input_paths_set: Set[str] = set(self.flat_input_paths())

    ############################################################################
    #
    ############################################################################
    def __repr__(self) -> str:
        return "Creator(input_paths={}, output_paths={}, function={}, categories={})".format(
            str(self.input_paths),
            str(self.output_paths),
            str(self.function),
            str(self.categories)
        )

    ############################################################################
    #
    ############################################################################
    def flat_input_paths(self) -> List[str]:
        flat_input_paths: List[str] = []
        for input_path in self.input_paths.values():  # type:ignore # Typed Dict is secretly a dict but technically not
            if isinstance(input_path, str):
                flat_input_paths.append(input_path)

            elif isinstance(input_path, list) and all([isinstance(x, str) for x in input_path]):
                for sub_input_path in input_path:
                    flat_input_paths.append(sub_input_path)

            else:
                raise TypeError("Expected either a string or a list of strings but got", input_path)

        return flat_input_paths

    ############################################################################
    #
    ############################################################################
    def flat_output_paths(self) -> List[str]:
        flat_output_paths: List[str] = []
        for output_path in self.output_paths.values():  # type:ignore # Typed Dict is secretly a dict but technically not
            if isinstance(output_path, str):
                flat_output_paths.append(output_path)

            elif isinstance(output_path, list) and all([isinstance(x, str) for x in output_path]):
                for sub_output_path in output_path:
                    flat_output_paths.append(sub_output_path)

            else:
                raise TypeError("Expected either a string but got", output_path)

        return flat_output_paths

    ############################################################################
    #
    ############################################################################
    def has_input(self, input_path: str) -> bool:
        return input_path in self._input_paths_set

    ############################################################################
    #
    ############################################################################
    def run(self) -> None:
        self.function(self.input_paths, self.output_paths)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Creator):
            raise TypeError("'<' not supported between instances of 'Creator' and {}".format(type(other)))

        self_paths = [sorted(self.flat_output_paths()), sorted(self.flat_input_paths())]
        other_paths = [sorted(other.flat_output_paths()), sorted(other.flat_input_paths())]

        return self_paths < other_paths

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Creator):
            return False

        if self.input_paths != other.input_paths:
            return False

        if self.output_paths != other.output_paths:
            return False

        if self.function != other.function:
            return False

        if self.categories != other.categories:
            return False

        return True
