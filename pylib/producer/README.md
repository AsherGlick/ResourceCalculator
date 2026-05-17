The Producer library is pretty complicated. The Most complex part being the scheduler.



Build Log
===
In order to make configuration easier the producer library uses a build log that stores a history of all the build actions from the previous run of the program. This primarily serves as a way to allow us to skip steps that have already been built previously. But also lets us cull files from previous runs that are not part of current or future runs.



Initial Updates
---

Initial updates take care of several things, most importantly deletion of actions that have been previously completed without change.

File State                      | Build Log Link | Assumed Action Event
--------------------------------|----------------|-----------
Newer Outputs                   | Strong         | Nothing, Skip Processing
Newer Inputs or missing Outputs | Strong         | Add,    Delete Build Log
Newer Outputs                   | Weak           | Change, Delete build Log
Newer Inputs or missing Outputs | Weak           | Change, Delete Build log
Newer Outputs                   | None[^1]       | Remove, Delete Build Log
Newer Inputs or missing Outputs | None[^1]       | Remove, Delete Build Log


Inline Updates
---

Other events happen during runtime execution of the producer actions.

Action Event | Build Log Link | Result
-------------|----------------|--------
Add          | Strong         | Delete Build Log
Remove       | Strong         | Delete Build Log
Change       | Strong         | Delete Build Log
Nothing      | Strong         | Skip Processing
Add          | Weak           | Delete Build Log
Remove       | Weak           | Already Deleted
Change       | Weak           | Already Deleted / Delete
Nothing      | Weak           | Already Deleted
Add          | None           | Nothing
Remove       | None           | Nothing
Change       | None           | Nothing
Nothing      | None           | Nothing

Action Event | Build Log Link | Result
-------------|----------------|--------
Add          | Strong         | Delete Build Log
Add          | Weak           | Delete Build Log
Add          | None           | Nothing
Change       | Strong         | Delete Build Log
Change       | Weak           | Already Deleted / Delete Build Log
Change       | None           | Nothing
Remove       | Strong         | Delete Build Log
Remove       | Weak           | Already Deleted
Remove       | None           | Nothing
Nothing      | Strong         | Skip Processing 
Nothing      | Weak           | Already Deleted
Nothing      | None           | Nothing





How Producers Work
================================================================================
Each producer is defined with three key components.
1) Its unique name
2) A set of regexes that match to input files
3) A function that gets called with each set of files that matches the regexes


Unique Name
--------------------------------------------------------------------------------
A unique name is required for a producer becuase it is stored in the buildlog
to identify if that producer's job had been previously completed or if it needs
to be rerun.

The unique name can be anything, and does not need to be statically defined.

Regex Set
--------------------------------------------------------------------------------
Regexes are the bread and butter of the producer library. They allow each
producer to be incredibly flexible when it comes to identifying their input
files. See the "Regexes" section for more info about how they are constructed.

Function
--------------------------------------------------------------------------------
A producer function gets two pieces of information, the input files, the regex
groups that were captures when matching those input filenames. They are then
required to emit a list which contains all of the files they created. If the
list is incomplete then the producer library will not trigger subsequent builds
on those output files properly.

```python
def example_function(input_files: SingleFile, groups: Dict[str, str]) -> List[str]:
```

Regexes
================================================================================

Single Match Regexes
--------------------------------------------------------------------------------
When a regex is supposed to match only one file then a single match regex is
the right thing to use. A good example of this is a producer that gzips all of
the html, css, and javascript files.

```python
Producer(
    name="Compress HTTP Files",
    input_path_patterns={
        "file": r"^output/.*\.(?:html|js|css)$"
    },
    function=gz_compress_function,
)
```

If we had
```
index.html
index.css
index.js
external_library.js
```

This producer will match each file and call `gz_compress_function()` once on
each file.





Multi Match Regexes
--------------------------------------------------------------------------------
```python
Producer(
    name="Pack Image",
    input_path_patterns={
        "files": [r"^items/.*$"],
    },
    function=pack_function,
)
```


Complex Matches
--------------------------------------------------------------------------------
Regex matches can have named match groups. These named match groups can bundle
together different files to allow for specific combinations of files to be run
together.


Gen2 of the producer lib
================================================================================
The constraints we have are:
1: We want to make sure we know what files we need.
	This will be done the same way we currently do things. With producers that have regexs.


```python
Producer(
    input_path_patterns={
        "file": r"^(?P<fullpath>resource_lists/(?P<calculator_dir>{calculator_dir_regex})/plugins/.+/.+)$".format(
            calculator_dir_regex=calculator_dir_regex
        ),
    },
    function=producer_copyfile,
)
```

There are two types of input path patterns the normal pattern and the array pattern


can we make that syntax any nicer? For typechecking I mean.

also is categories really all that interesting right now? It might have been when we were thinking about "skip" categories but now that just seems like we should make a second producer that gets swapped in satically when the arguments are called



Producers will also no longer need to handle a specific "output file datatype" anymore as all producer functions will be List[str] return types
```python
class Producer(Generic[InputFileDatatype, OutputFileDatatype]):
class Producer(Generic[InputFileDatatype]):
```

```python
def image_pack_function(input_files: MultiFile, output_files: ImagePackOutputFiles) -> None:
def image_pack_function(input_files: MultiFile) -> List[str]:
```



```python
Producer(
    input_path_patterns=SingleFile(
        file=r"^(?P<fullpath>resource_lists/(?P<calculator_dir>{calculator_dir_regex})/plugins/.+/.+)$".format(
            calculator_dir_regex=calculator_dir_regex
        ),
    ),
    function=producer_copyfile,
)
```


Only Require Input Files
--------------------------------------------------------------------------------
To achive this we will instead have a buildlog of "these output files were created by those input files using this producer"


* Warning/error when two different producers create the same file


When looking to see if a producer should re-trigger its job. It looks at all of the input files. Then queries the buildlog to see when the last time this producer was run with those files, and also what files it outputted.

If this producer has:
	* not been run before
	* any of the previous run's output files are missing
	* has last been run before the most recent updated date of any input files (tbd)
	* has an input file with a more recent last-update date then any of the previous run's output files
Then the producer will be run. Otherwise it will not be run.


Delete files not created in this producer run
--------------------------------------------------------------------------------
Because we have a record of each input and output file we can query all the existing output fies from the previous run to see which ones were not created or skipped by the current run. Skips would cascade so every producer that consumed files from a skipped process would be inlcuded in the output of the next build as well.


Dont rebuild files when they are not needed
--------------------------------------------------------------------------------
Again the build log will handle this by checking the previous run's build against this run's build.
