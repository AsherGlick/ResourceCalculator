from typing import List, Dict
import subprocess
import re

from pylib.producer import Producer, SingleFile
from pylib.producer.producer import GenericProducer


def js_rollup_producer(
    target_file: str,
    destination_file: str,
) -> List[GenericProducer]:

    def rollup_typescript(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
        subprocess.run(["./node_modules/.bin/rollup", input_files["file"], "--file", destination_file, "--format", "iife"])
        return [destination_file]

    return [
        Producer(
            name="Rollup Javascript Modules " + target_file,
            input_path_patterns={
                "file": "^" + re.escape(target_file) + "$",
            },
            function=rollup_typescript
        )
    ]
