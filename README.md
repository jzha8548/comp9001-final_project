# SpiritForge: Creature Battle Balance Simulator

![SpiritForge representative image](assets/spiritforge_padlet_image.png)

SpiritForge is a terminal-based Python tool for testing battle balance in creature-collection RPGs. It is designed for student game designers and indie developers who want to check whether a battle encounter is too easy, too hard, or balanced before real playtesting.

The program loads original creature and skill data from text files, simulates turn-based battles, runs automated balance tests, and generates a report with win rate, average battle length, remaining HP, balance rating, and design suggestions.

## Why this project exists

In creature-collection RPGs, battle balance is difficult to judge by intuition alone. A boss may be too strong, a starter creature may defeat enemies too easily, or a type matchup may be too one-sided. SpiritForge helps designers test these situations quickly through simulation.

## Main features

- Load creature data from `creatures.txt`
- Load skill data from `skills.txt`
- View creatures and skills in readable terminal tables
- Choose creatures by number or by name
- Preview matchup details before battle
- Display HP bars during battle logs
- Simulate one battle
- Run multiple automated simulations
- Generate a balance report
- Save report output to text files
- View a 2D type effectiveness chart
- Run built-in system tests

## Advanced Python concepts used

### 1. File I/O

The program reads creature and skill data from external text files and saves generated reports. This means designers can change game values without editing the Python source code.

Files used:

- `creatures.txt`
- `skills.txt`
- `balance_report.txt` generated after saving
- `battle_history.txt` generated after saving

### 2. Multi-dimensional list

The type effectiveness chart in `config.py` is implemented as a two-dimensional list. Rows represent attacking elements, and columns represent defending elements.

### 3. Testing

The project includes a built-in testing mode that checks type multipliers, damage calculation, validation, and simple battle logic.

### 4. Exception handling and control flow

The program uses `try-except`, `raise`, `return`, `break`, and `continue` to handle invalid input, missing files, invalid data, menu control, and battle endings.

## How to run

1. Download or clone this repository.
2. Open a terminal in the project folder.
3. Run:

```bash
python main.py
```

If your computer uses Python 3 as `python3`, run:

```bash
python3 main.py
```

No external Python libraries are required.

## Recommended demo flow

After running `python main.py`, try:

```text
12
```

This runs the guided demo: `Flarefox` vs `Leafling`.

Or use the full manual flow:

```text
1   Load creature database
2   Load skill database
3   View all creatures
5   Simulate one battle
6   Run balance test
8   Run system tests
9   Save latest report
10  Exit
```

Recommended battle test:

```text
Player: Flarefox
Enemy: Leafling
Simulations: 30
```

## Project file structure

```text
main.py              Main menu and user interaction
models.py            Skill, Creature, BattleResult, BalanceReport classes
simulator.py         Battle simulation and damage logic
data_manager.py      File loading and saving functions
tests.py             Built-in system tests
config.py            Type chart and default file names
ui_helpers.py        Terminal UI helper functions
creatures.txt        Creature database
skills.txt           Skill database
README.md            Project explanation
.gitignore           Files to ignore in GitHub
assets/              Representative image for README / Padlet
```

## Example pitch

SpiritForge is not just a creature battle game. It is a game design tool that helps designers make better balance decisions before playtesting.


## AI Appendix

### AI Use Appendix

AI tools were used as a support tool during the development, documentation, and presentation preparation of this project. The assistance was mainly used for improving clarity, wording, structure, user-facing communication, and implementation guidance based on my project requirements.

Specifically, AI assistance was used in the following areas:

### 1. Representative Poster / UI Image

AI assistance was used to refine the visual concept and wording of the representative project image for the Padlet post. The image was designed to communicate the core idea of SpiritForge as a creature battle balance simulator, including elements such as battle testing, win rate, balance rating, and design feedback. The final image and wording were reviewed and selected by me.

### 2. Terminal UI Guidance

AI assistance was used to improve the clarity of the terminal-based user interface guidance. This included refining menu labels, quick-start instructions, guided demo wording, matchup preview text, HP bar display, and explanatory messages to make the program easier for users and examiners to understand.

### 3. README Polishing

AI assistance was used to polish the README file, including the project description, feature explanation, running instructions, file structure explanation, advanced concept summary, and presentation of the project as a game design balance testing tool. The purpose was to make the documentation clearer and easier to follow.

### 4. Creature Names and Initial Stat Values

AI assistance was used to generate and refine original creature names and initial creature stat values based on my design requirements. These included values such as HP, attack, defense, speed, element type, and skill allocation. The values were designed to support simple balance testing scenarios, such as showing when a matchup is too easy, too hard, or relatively balanced. I reviewed the generated values and used them as part of the final creature database.

### 5. Skill Data and Type Effectiveness Design

AI assistance was used to help generate original skill names, skill power values, accuracy values, and a simplified type effectiveness chart based on my requirements. The type chart was designed as a multi-dimensional list to support battle calculations between different creature elements such as fire, water, grass, electric, and rock. I reviewed the chart and used it to demonstrate how type advantage affects damage calculation and battle balance.

### 6. Code Structure and Implementation Guidance

AI assistance was used to help structure the Python project into separate files and modules, including the main menu system, data models, battle simulator logic, file input/output handling, UI helper functions, and built-in system tests. The implementation was developed according to my project idea and requirements, and I reviewed how the main logic works, including creature loading, skill loading, turn order, damage calculation, type effectiveness, balance testing, and report generation.

### 7. Project Explanation and Presentation Wording

AI assistance was also used to help refine how the project is explained in a concise and professional way, especially the distinction between a normal creature battle game and a game design balance testing tool. This helped me prepare clearer wording for the Padlet post, README, and project presentation.

All final project decisions, submitted files, code execution, and project understanding were reviewed by me. I tested the program locally, checked that the terminal interface works, and ensured that I can explain the main logic, including creature data loading, skill damage calculation, turn order, type effectiveness, balance testing, system testing, and report generation.

AI was used to support development, communication, documentation, and presentation polish. It was not used as a replacement for my understanding of the submitted project.
