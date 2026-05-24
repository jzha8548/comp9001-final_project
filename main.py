"""SpiritForge: A Creature Battle Balance Simulator.

Run this file with:
    python main.py

This project is designed for COMP9001-style learning outcomes:
- basic Python: variables, input/output, conditionals, containers, loops,
  functions, and classes
- advanced topics: File I/O, multi-dimensional lists, simple testing, and
  robust exception handling

The interface is intentionally terminal-based so it stays easy to run on the
examiner's machine. UI helper functions make the terminal output easier to
understand without requiring external libraries.
"""

import os

from config import (
    DEFAULT_CREATURE_FILE,
    DEFAULT_HISTORY_FILE,
    DEFAULT_REPORT_FILE,
    DEFAULT_SKILL_FILE,
)
from data_manager import (
    append_history,
    load_creatures,
    load_skills,
    save_report,
    validate_creature_skills,
)
from simulator import BattleSimulator
from tests import run_all_tests
from ui_helpers import (
    format_report_summary,
    print_creature_list,
    print_header,
    print_loaded_summary,
    print_matchup_preview,
    print_quick_start,
    print_type_chart,
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def project_path(filename):
    """Return a path inside this project folder."""
    return os.path.join(BASE_DIR, filename)


def print_menu(creatures, skills):
    """Display the main terminal menu."""
    print_header("SpiritForge: Creature Battle Balance Simulator")
    print_loaded_summary(creatures, skills)
    print("")
    print("0. Quick start guide")
    print("1. Load creature database")
    print("2. Load skill database")
    print("3. View all creatures")
    print("4. View all skills")
    print("5. Simulate one battle")
    print("6. Run balance test")
    print("7. View latest report")
    print("8. Run system tests")
    print("9. Save latest report")
    print("10. Exit")
    print("11. View type effectiveness chart")
    print("12. Run guided demo")


def print_warnings(warnings):
    """Print warning messages from file loading or validation."""
    if len(warnings) == 0:
        return
    print("\nWarnings:")
    for warning in warnings:
        print(f"- {warning}")


def require_data(creatures, skills):
    """Check that both creature and skill databases have been loaded."""
    if len(creatures) == 0:
        print("Please load the creature database first by choosing option 1.")
        return False
    if len(skills) == 0:
        print("Please load the skill database first by choosing option 2.")
        return False
    return True


def view_creatures(creatures):
    """Display all loaded creatures in a readable table."""
    if len(creatures) == 0:
        print("No creatures loaded yet. Choose option 1 first.")
        return

    print_header("Loaded Creatures")
    print(f"{'No.':>3} {'Name':<12} {'Type':<10} {'HP':>5} {'ATK':>5} {'DEF':>5} {'SPD':>5}  Skills")
    print("-" * 84)
    for index, creature in enumerate(creatures.values(), start=1):
        skills_text = ", ".join(creature.skill_names)
        print(
            f"{index:>3} {creature.name:<12} {creature.element:<10} "
            f"{creature.max_hp:>5} {creature.attack:>5} "
            f"{creature.defense:>5} {creature.speed:>5}  {skills_text}"
        )
    print("\nTip: In battle setup, you can choose a creature by number or by name.")


def view_skills(skills):
    """Display all loaded skills in a readable table."""
    if len(skills) == 0:
        print("No skills loaded yet. Choose option 2 first.")
        return

    print_header("Loaded Skills")
    print(f"{'No.':>3} {'Name':<15} {'Type':<10} {'Power':>7} {'Accuracy':>10}")
    print("-" * 58)
    for index, skill in enumerate(skills.values(), start=1):
        print(
            f"{index:>3} {skill.name:<15} {skill.element:<10} "
            f"{skill.power:>7} {skill.accuracy:>9}%"
        )


def get_creature_choice(prompt, creatures):
    """Ask the user to select a creature by number or name."""
    print("\nAvailable creatures:")
    print_creature_list(creatures)

    raw_choice = input(prompt).strip()
    if raw_choice == "":
        raise ValueError("Creature choice cannot be empty.")

    names = list(creatures.keys())

    if raw_choice.isdigit():
        number = int(raw_choice)
        if number < 1 or number > len(names):
            raise ValueError(f"Please enter a number between 1 and {len(names)}.")
        return creatures[names[number - 1]]

    lower_lookup = {name.lower(): name for name in names}
    key = raw_choice.lower()
    if key not in lower_lookup:
        raise ValueError(f"Creature '{raw_choice}' was not found. Use a number or exact name.")

    return creatures[lower_lookup[key]]


def get_positive_integer(prompt):
    """Ask for a positive integer and validate the input."""
    raw_value = input(prompt).strip()
    try:
        value = int(raw_value)
    except ValueError:
        raise ValueError("Please enter a valid whole number, such as 30.")

    if value <= 0:
        raise ValueError("The number must be greater than 0.")
    return value


def load_creature_database(creatures, skills):
    """Load creatures from creatures.txt and show warnings."""
    file_path = project_path(DEFAULT_CREATURE_FILE)
    loaded_creatures, warnings = load_creatures(file_path)
    creatures.clear()
    creatures.update(loaded_creatures)

    print(f"Loaded {len(creatures)} creatures from {DEFAULT_CREATURE_FILE}.")
    print_warnings(warnings)
    print("Next step: choose option 2 to load skills, then option 3 to view creatures.")

    if len(skills) > 0:
        skill_warnings = validate_creature_skills(creatures, skills)
        print_warnings(skill_warnings)


def load_skill_database(creatures, skills):
    """Load skills from skills.txt and show warnings."""
    file_path = project_path(DEFAULT_SKILL_FILE)
    loaded_skills, warnings = load_skills(file_path)
    skills.clear()
    skills.update(loaded_skills)

    print(f"Loaded {len(skills)} skills from {DEFAULT_SKILL_FILE}.")
    print_warnings(warnings)
    print("Next step: choose option 5 for one battle or option 6 for balance testing.")

    if len(creatures) > 0:
        skill_warnings = validate_creature_skills(creatures, skills)
        print_warnings(skill_warnings)


def simulate_one_battle(creatures, skills):
    """Let the user choose two creatures and simulate one battle."""
    if not require_data(creatures, skills):
        return None

    print_header("Single Battle Setup")
    player = get_creature_choice("Choose player creature by number or name: ", creatures)
    enemy = get_creature_choice("Choose enemy creature by number or name: ", creatures)

    simulator = BattleSimulator(skills)
    print_matchup_preview(player, enemy, simulator)

    result = simulator.run_one_battle(player, enemy, show_log=True)
    report_text = result.to_text()
    print(format_report_summary(report_text))
    return report_text


def run_balance_test(creatures, skills):
    """Run many simulations and generate a balance report."""
    if not require_data(creatures, skills):
        return None

    print_header("Balance Test Setup")
    player = get_creature_choice("Choose player creature by number or name: ", creatures)
    enemy = get_creature_choice("Choose enemy creature by number or name: ", creatures)
    simulations = get_positive_integer("How many simulations? Recommended: 30 or 50: ")

    simulator = BattleSimulator(skills)
    print_matchup_preview(player, enemy, simulator)
    print(f"\nRunning {simulations} automated simulations...")

    report = simulator.run_many_battles(player, enemy, simulations)
    report_text = report.to_text()
    print(format_report_summary(report_text))
    return report_text


def view_latest_report(latest_report):
    """Display the latest generated report."""
    if latest_report is None:
        print("No report has been generated yet. Choose option 5 or 6 first.")
        return
    print(format_report_summary(latest_report))


def save_latest_report(latest_report):
    """Save the latest report to balance_report.txt and battle_history.txt."""
    if latest_report is None:
        print("No report has been generated yet. Run a battle or balance test first.")
        return

    report_path = project_path(DEFAULT_REPORT_FILE)
    history_path = project_path(DEFAULT_HISTORY_FILE)
    save_report(latest_report, report_path)
    append_history(latest_report, history_path)
    print(f"Latest report saved to {DEFAULT_REPORT_FILE}.")
    print(f"Report also appended to {DEFAULT_HISTORY_FILE}.")


def run_guided_demo(creatures, skills):
    """Load data if needed, then run the recommended Flarefox vs Leafling demo."""
    print_header("Guided Demo: Flarefox vs Leafling")

    if len(creatures) == 0:
        print("Auto-loading creatures for demo...")
        load_creature_database(creatures, skills)
    if len(skills) == 0:
        print("Auto-loading skills for demo...")
        load_skill_database(creatures, skills)

    if "Flarefox" not in creatures or "Leafling" not in creatures:
        raise ValueError("Demo requires Flarefox and Leafling in creatures.txt.")

    player = creatures["Flarefox"]
    enemy = creatures["Leafling"]
    simulator = BattleSimulator(skills)

    print_matchup_preview(player, enemy, simulator)
    print("\nDemo purpose: Fire normally has advantage against Grass, so this matchup")
    print("should often be rated as easy for the player.")
    print("\nRunning 30 automated simulations...")

    report = simulator.run_many_battles(player, enemy, 30)
    report_text = report.to_text()
    print(format_report_summary(report_text))
    return report_text


def main():
    """Main program loop."""
    creatures = {}
    skills = {}
    latest_report = None

    print_quick_start()

    while True:
        print_menu(creatures, skills)
        choice = input("Enter your choice: ").strip()

        try:
            if choice == "0":
                print_quick_start()
            elif choice == "1":
                load_creature_database(creatures, skills)
            elif choice == "2":
                load_skill_database(creatures, skills)
            elif choice == "3":
                view_creatures(creatures)
            elif choice == "4":
                view_skills(skills)
            elif choice == "5":
                new_report = simulate_one_battle(creatures, skills)
                if new_report is not None:
                    latest_report = new_report
            elif choice == "6":
                new_report = run_balance_test(creatures, skills)
                if new_report is not None:
                    latest_report = new_report
            elif choice == "7":
                view_latest_report(latest_report)
            elif choice == "8":
                print("\n" + run_all_tests())
            elif choice == "9":
                save_latest_report(latest_report)
            elif choice == "10":
                print("Thank you for using SpiritForge. Goodbye!")
                break
            elif choice == "11":
                print_type_chart()
            elif choice == "12":
                latest_report = run_guided_demo(creatures, skills)
            else:
                print("Invalid menu choice. Please choose a number from 0 to 12.")
                continue
        except (ValueError, FileNotFoundError) as error:
            print(f"Error: {error}")
            continue


if __name__ == "__main__":
    main()
