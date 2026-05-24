SpiritForge: A Creature Battle Balance Simulator
================================================

Project idea
------------
SpiritForge is a terminal-based Python program for game designers. It simulates
turn-based creature battles and helps users test whether a matchup is too easy,
too hard, or balanced.

It is inspired by creature-collection RPGs, but all creature and skill names are
original. It is a balance-testing tool, not a clone of an existing game.

How to run
----------
1. Put all project files in the same folder.
2. Open a terminal in this folder.
3. Run:

   python main.py

No external libraries are needed.

Recommended demo flow
---------------------
1. Choose menu option 1: Load creature database
2. Choose menu option 2: Load skill database
3. Choose menu option 3: View all creatures
4. Choose menu option 5: Simulate one battle
   Example: Flarefox vs Leafling
5. Choose menu option 6: Run balance test
   Example: Flarefox vs Leafling, 30 simulations
6. Choose menu option 8: Run system tests
7. Choose menu option 9: Save latest report

Data files
----------
creatures.txt format:
name,element,hp,attack,defense,speed,skill1|skill2

skills.txt format:
name,element,power,accuracy

Advanced topics included
------------------------
1. File I/O
   - Reads creature data from creatures.txt
   - Reads skill data from skills.txt
   - Saves reports to balance_report.txt
   - Appends saved reports to battle_history.txt

2. Multi-dimensional list
   - Uses a 2D type effectiveness chart in config.py
   - Rows are attacking elements
   - Columns are defending elements
   - The simulator uses this chart to calculate damage multipliers

3. Testing
   - Menu option 8 runs built-in system tests
   - Tests type effectiveness, damage calculation, validation, and simple battle logic

Important design choice
-----------------------
The interface is text-based. This was chosen to keep the project easy to run and
to focus on Python logic, data structures, classes, file handling, and testing.
