from typing import Callable, Generic, Protocol, List, Dict, cast
from dataclasses import dataclass
from .producer import InputFileDatatype


@dataclass
class FunctionCall(Generic[InputFileDatatype]):
    input_paths: InputFileDatatype
    groups: Dict[str, str]
    output_paths: List[str]


class TrackedProducerFunction(Generic[InputFileDatatype], Protocol):
    call_list: List[FunctionCall[InputFileDatatype]]
    def __call__(self, input_files: InputFileDatatype, groups: Dict[str, str]) -> List[str]:
        ...


def tracked_function(
    func: Callable[[InputFileDatatype, Dict[str, str]], List[str]]
) -> TrackedProducerFunction[InputFileDatatype]:

    wrapper: TrackedProducerFunction[InputFileDatatype]

    def _wrapper(input_files: InputFileDatatype, groups: Dict[str, str]) -> List[str]:
        result = func(input_files, groups)
        wrapper.call_list.append(FunctionCall(
            input_paths=input_files,
            groups=groups,
            output_paths=result
        ))
        return result

    wrapper = cast(TrackedProducerFunction[InputFileDatatype], _wrapper)
    wrapper.call_list = []
    return wrapper
