"""File input/output functions for SpiritForge.

This module demonstrates File I/O in a meaningful way:
- creature and skill values are loaded from text files
- balance reports are saved to text files
- battle history can be appended for later review
"""

from datetime import datetime

from models import Creature, Skill


def load_skills(filename):
    """Load skills from a text file.

    Expected line format:
        name,element,power,accuracy

    Returns:
        skills: dictionary mapping skill name to Skill object
        warnings: list of skipped-line warning messages
    """
    skills = {}
    warnings = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if line == "" or line.startswith("#"):
                    continue

                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 4:
                    warnings.append(
                        f"Skipped skills line {line_number}: expected 4 fields."
                    )
                    continue

                name, element, power, accuracy = parts
                try:
                    skill = Skill(name, element, int(power), int(accuracy))
                except ValueError as error:
                    warnings.append(f"Skipped skills line {line_number}: {error}")
                    continue

                skills[skill.name] = skill
    except FileNotFoundError:
        raise FileNotFoundError(f"Skill file not found: {filename}")

    if len(skills) == 0:
        raise ValueError("No valid skills were loaded.")

    return skills, warnings


def load_creatures(filename):
    """Load creatures from a text file.

    Expected line format:
        name,element,hp,attack,defense,speed,skill1|skill2

    Returns:
        creatures: dictionary mapping creature name to Creature object
        warnings: list of skipped-line warning messages
    """
    creatures = {}
    warnings = []

    try:
        with open(filename, "r", encoding="utf-8") as file:
            for line_number, raw_line in enumerate(file, start=1):
                line = raw_line.strip()
                if line == "" or line.startswith("#"):
                    continue

                parts = [part.strip() for part in line.split(",")]
                if len(parts) != 7:
                    warnings.append(
                        f"Skipped creatures line {line_number}: expected 7 fields."
                    )
                    continue

                name, element, hp, attack, defense, speed, skills_text = parts
                skill_names = [skill.strip() for skill in skills_text.split("|")]

                try:
                    creature = Creature(
                        name,
                        element,
                        int(hp),
                        int(attack),
                        int(defense),
                        int(speed),
                        skill_names,
                    )
                except ValueError as error:
                    warnings.append(f"Skipped creatures line {line_number}: {error}")
                    continue

                creatures[creature.name] = creature
    except FileNotFoundError:
        raise FileNotFoundError(f"Creature file not found: {filename}")

    if len(creatures) == 0:
        raise ValueError("No valid creatures were loaded.")

    return creatures, warnings


def validate_creature_skills(creatures, skills):
    """Return warnings for creature skills missing from the skill database."""
    warnings = []
    for creature in creatures.values():
        for skill_name in creature.skill_names:
            if skill_name not in skills:
                warnings.append(
                    f"Warning: {creature.name} uses '{skill_name}', "
                    "but that skill is not in skills.txt."
                )
    return warnings


def save_report(report_text, filename):
    """Save the latest report to a text file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(report_text)
        file.write("\n")


def append_history(report_text, filename):
    """Append a short timestamped report entry to battle history."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(filename, "a", encoding="utf-8") as file:
        file.write("\n" + "=" * 60 + "\n")
        file.write(f"Saved at: {timestamp}\n")
        file.write(report_text)
        file.write("\n")
