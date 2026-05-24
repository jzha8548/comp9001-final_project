"""Terminal UI helper functions for SpiritForge.

This module keeps visual output separate from battle logic. It does not use any
external libraries, so the project remains easy to run on an examiner's machine.
"""

from config import TYPE_CHART, VALID_ELEMENTS


LINE_WIDTH = 72


def print_header(title):
    """Print a clear section header."""
    print("\n" + "=" * LINE_WIDTH)
    print(title)
    print("=" * LINE_WIDTH)


def print_subheader(title):
    """Print a smaller section header."""
    print("\n" + "-" * LINE_WIDTH)
    print(title)
    print("-" * LINE_WIDTH)


def hp_bar(current_hp, max_hp, width=20):
    """Return an ASCII HP bar such as [####------] 20/50."""
    current_hp = max(0, int(current_hp))
    max_hp = max(1, int(max_hp))
    filled = round((current_hp / max_hp) * width)
    filled = max(0, min(width, filled))
    empty = width - filled
    return "[" + "#" * filled + "-" * empty + f"] {current_hp}/{max_hp}"


def print_quick_start():
    """Show a beginner-friendly workflow for first-time users."""
    print_header("Quick Start Guide")
    print("SpiritForge is a balance testing tool, not a manual fighting game.")
    print("You act as the game designer: choose two creatures and let the")
    print("simulator judge whether the encounter is too easy, too hard, or balanced.")
    print("\nRecommended first run:")
    print("  1  Load creature database")
    print("  2  Load skill database")
    print("  3  View all creatures")
    print("  5  Simulate one battle")
    print("  6  Run balance test, e.g. 30 simulations")
    print("  8  Run system tests")
    print("  9  Save latest report")
    print("\nGood demo matchup:")
    print("  Player: Flarefox")
    print("  Enemy:  Leafling")
    print("\nInput tip:")
    print("  When choosing a creature, you can type its number OR its exact name.")


def print_type_chart():
    """Display the 2D type effectiveness chart in a readable table."""
    print_header("Type Effectiveness Chart")
    print("Rows are attacking elements. Columns are defending elements.")
    print("2.0 = super effective, 0.5 = not very effective, 1.0 = normal")
    print("")

    header = "Attack \\ Def".ljust(14)
    for element in VALID_ELEMENTS:
        header += element[:8].rjust(10)
    print(header)
    print("-" * (14 + 10 * len(VALID_ELEMENTS)))

    for row_index, attack_element in enumerate(VALID_ELEMENTS):
        row = attack_element.ljust(14)
        for multiplier in TYPE_CHART[row_index]:
            row += f"{multiplier:.1f}".rjust(10)
        print(row)


def print_loaded_summary(creatures, skills):
    """Show database status below the menu."""
    creature_status = f"{len(creatures)} creatures" if creatures else "not loaded"
    skill_status = f"{len(skills)} skills" if skills else "not loaded"
    print(f"Database status: Creatures = {creature_status} | Skills = {skill_status}")


def print_creature_list(creatures):
    """Print numbered creature names for easier selection."""
    names = list(creatures.keys())
    for index, name in enumerate(names, start=1):
        creature = creatures[name]
        print(
            f"{index:>2}. {creature.name:<12} "
            f"Type: {creature.element:<8} "
            f"HP:{creature.max_hp:<4} ATK:{creature.attack:<3} "
            f"DEF:{creature.defense:<3} SPD:{creature.speed:<3}"
        )


def print_matchup_preview(player, enemy, simulator):
    """Print useful information before a battle starts."""
    print_header("Matchup Preview")
    print(f"Player: {player.name} ({player.element})")
    print(f"Enemy:  {enemy.name} ({enemy.element})")
    print("")
    print(f"{player.name} HP: {hp_bar(player.max_hp, player.max_hp)}")
    print(f"{enemy.name} HP: {hp_bar(enemy.max_hp, enemy.max_hp)}")
    print("")

    if player.speed > enemy.speed:
        print(f"Speed advantage: {player.name} moves first ({player.speed} > {enemy.speed}).")
    elif enemy.speed > player.speed:
        print(f"Speed advantage: {enemy.name} moves first ({enemy.speed} > {player.speed}).")
    else:
        print(f"Speed tie: player moves first because speeds are equal ({player.speed}).")

    print_subheader("Player skill preview")
    for skill_name in player.skill_names:
        if skill_name in simulator.skills:
            skill = simulator.skills[skill_name]
            multiplier = simulator.get_type_multiplier(skill.element, enemy.element)
            damage = simulator.calculate_damage(player, enemy, skill)
            print(
                f"{skill.name:<15} Type:{skill.element:<8} "
                f"Power:{skill.power:<3} Acc:{skill.accuracy:>3}% "
                f"Multiplier:x{multiplier:<3} Expected damage:{damage}"
            )

    print_subheader("Enemy skill preview")
    for skill_name in enemy.skill_names:
        if skill_name in simulator.skills:
            skill = simulator.skills[skill_name]
            multiplier = simulator.get_type_multiplier(skill.element, player.element)
            damage = simulator.calculate_damage(enemy, player, skill)
            print(
                f"{skill.name:<15} Type:{skill.element:<8} "
                f"Power:{skill.power:<3} Acc:{skill.accuracy:>3}% "
                f"Multiplier:x{multiplier:<3} Expected damage:{damage}"
            )


def format_report_summary(report_text):
    """Add a visual wrapper around report text."""
    return "\n" + "=" * LINE_WIDTH + "\n" + report_text + "\n" + "=" * LINE_WIDTH
