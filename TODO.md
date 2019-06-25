### TODO

---

- [ ] run_script.py - Needs more work.  Currently can't handle mixed-dice pools (e.g. 3d4+6d10 ) in param list
- [ ] ttrpg_core/die.py - Might want to add some logic to manage roll "memory" so it doesn't get unmanagable over time
- [ ] ttrpg_core/utilities.py - Thinking of putting the split results into a dictionary or list
- [ ] ttrpg_core/utilities.py - Make the pattern matching/split more robustly. Currently case-sensitive
- [ ] tests/test_die.py - Test for multiple rolls (among many other test cases)
- [ ] tests/test_rpg_system.py - TestCoC7th - need testing for bonus/penalty dice
- [ ] tests/test_utilities.py - Need to write uses cases for 
	- [ ] Iterations of malformed dice formats
	- [ ] Expand supported formats
- [ ] rpg_system.py - Build out additional systems
	- [ ] Shadow Run
	- [ ] GURPS
	- [ ] Cee-lo
	- [ ] Previous Versions of existing systems
- [ ] Refactor dice-pool into it's own file
- [ ] After refactoring a bit noticed tests only work when current path is in the python path

