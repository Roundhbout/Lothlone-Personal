
# Milestone 6 - Refactoring Report

**Team members: Benjamin Palmer, Zachary Kelley**

**Github team/repo: Lothlone**


## Plan

- Restructure top-level gamestate design (remove levelstate class and merge fields into gamestate)  [DONE]
- Utils to create game objects from json (pretty much done)                                         [DONE]
- Create Tile.py class (& implement it)                                                             [DONE]
- Change connected_rooms dict (in hallway.py) to just be two separate arguments                     [DONE]
- Fix imports                                                                                       [DONE]
- Other stuff not handled in milestone 5                                                            [INCOMPLETE]



## Changes

We refactored `gamestate` to have a `level` class instead of a `levelstate`, and moved `adversaries` to the `gamestate` level (instead of `levelstate`). `objects` now reside within the `level`, as this was the design set forth by the Milestone 4 testing task.

We had already created utils (in `testUtils`) to translate the testing JSON format to our data structure in milestone 5, but with the changes we implemented here we had to do some rewriting of that.

We create a `tile` class that stores relevant information about individual tiles in the level grid, and implemented that across our code.

We refactored hallway to have two arguments/fields for `start_room` and `end_room` (the Room objects the hallway connects) instead of storing them in a dict.

We fixed the import issues. We changed imports within /src/Game to be relative imports, and imports within /tests to be absolute imports. We had to modify `PYTHONPATH` in each test harness.


## Future Work

While we've implemented Tile, we don't utilize it to the full potential. We ought to go and rewrite checks/tests that utilize tile to make our code more effective.

We need to write more unit tests/refactor old tests.
- More `gamestate` tests
- More `hallway` tests
- Fix rendering tests

More helper methods for getting players, adversaries, and objects (given an ID).

Helper method to check if a tile has an object on it.

Ensuring consistent naming convention. We started with camelCase and moved to underscores following python conventions, and we also have some bad name choices.

A script that runs through all our unit tests, and a script that automatically runs our testing task tests (right now we get the output on the command line and compare with the corresponding out.json file).

Maybe using a module to better render our levels beyond ASCII.

Maybe a make script that zips the test harness and relevant files for submission.

## Conclusion

The changes made today should help set us up for future testing tasks and hopefully implementation tasks too. The tile class should help us quickly get information about the game from a given coordinate, as well as standardizing appearances.

The directory layout specified by the assignments has created a massive headache for us since Python doesn't cleanly handle imports across different directories.