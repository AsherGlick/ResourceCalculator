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
