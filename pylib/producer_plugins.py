from pylib.producer import Producer, SingleFile, producer_copyfile
from typing import List, Tuple, Dict
import os



def plugins_producers() -> List[Producer]:
    return [
        Producer(
            input_path_patterns={
                "file": r"^resource_lists/(?P<calculator_dir>[a-z ]+)/plugins/.+/.+$",
            },
            paths=plugins_paths,
            function=producer_copyfile,
            categories=["editor"]
        )
    ]


def plugins_paths(input_files: SingleFile, categories: Dict[str,str]) -> Tuple[SingleFile, SingleFile]:
    return (
        input_files,
        {
            "file": os.path.join("output",os.path.relpath(input_files["file"], "resource_lists")),
        }
    )
