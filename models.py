"""Core data models for SpiritForge.

The project uses classes to keep creature, skill, and report data organised.
No external libraries are required.
"""

from config import VALID_ELEMENTS


class Skill:
    """A battle skill used by a creature.

    Attributes:
        name: Skill name shown to the user.
        element: Skill element, such as fire or water.
        power: Base skill power used in damage calculation.
        accuracy: Hit chance from 1 to 100.
    """

    def __init__(self, name, element, power, accuracy):
        self.name = name.strip()
        self.element = element.strip().lower()
        self.power = int(power)
        self.accuracy = int(accuracy)
        self._validate()

    def _validate(self):
        """Validate skill data and raise ValueError for invalid values."""
        if self.name == "":
            raise ValueError("Skill name cannot be empty.")
        if self.element not in VALID_ELEMENTS:
            raise ValueError(
                f"Skill '{self.name}' has invalid element '{self.element}'."
            )
        if self.power <= 0:
            raise ValueError(f"Skill '{self.name}' power must be greater than 0.")
        if self.accuracy < 1 or self.accuracy > 100:
            raise ValueError(
                f"Skill '{self.name}' accuracy must be between 1 and 100."
            )

    def __str__(self):
        return (
            f"{self.name} ({self.element}) - "
            f"Power: {self.power}, Accuracy: {self.accuracy}%"
        )


class Creature:
    """A creature used in battle simulation.

    Attributes:
        name: Creature name.
        element: Creature element.
        max_hp: Maximum HP.
        current_hp: Current HP during battle.
        attack: Attack stat.
        defense: Defense stat.
        speed: Speed stat. Higher speed acts first.
        skill_names: Names of skills this creature can use.
    """

    def __init__(self, name, element, hp, attack, defense, speed, skill_names):
        self.name = name.strip()
        self.element = element.strip().lower()
        self.max_hp = int(hp)
        self.current_hp = int(hp)
        self.attack = int(attack)
        self.defense = int(defense)
        self.speed = int(speed)
        self.skill_names = [skill.strip() for skill in skill_names if skill.strip()]
        self._validate()

    def _validate(self):
        """Validate creature data and raise ValueError for invalid values."""
        if self.name == "":
            raise ValueError("Creature name cannot be empty.")
        if self.element not in VALID_ELEMENTS:
            raise ValueError(
                f"Creature '{self.name}' has invalid element '{self.element}'."
            )
        if self.max_hp <= 0:
            raise ValueError(f"Creature '{self.name}' HP must be greater than 0.")
        if self.attack < 0:
            raise ValueError(f"Creature '{self.name}' attack cannot be negative.")
        if self.defense < 0:
            raise ValueError(f"Creature '{self.name}' defense cannot be negative.")
        if self.speed < 0:
            raise ValueError(f"Creature '{self.name}' speed cannot be negative.")
        if len(self.skill_names) == 0:
            raise ValueError(f"Creature '{self.name}' must have at least one skill.")

    def reset_hp(self):
        """Restore creature HP to full before a new battle."""
        self.current_hp = self.max_hp

    def clone(self):
        """Return a new copy so simulations do not damage the original object."""
        return Creature(
            self.name,
            self.element,
            self.max_hp,
            self.attack,
            self.defense,
            self.speed,
            list(self.skill_names),
        )

    def take_damage(self, amount):
        """Reduce HP by damage amount. HP will not go below 0."""
        amount = int(amount)
        if amount < 0:
            raise ValueError("Damage amount cannot be negative.")
        self.current_hp = max(0, self.current_hp - amount)

    def is_alive(self):
        """Return True if the creature still has HP."""
        return self.current_hp > 0

    def hp_bar_text(self):
        """Return a simple visual HP bar for battle logs."""
        width = 20
        filled = round((self.current_hp / self.max_hp) * width)
        filled = max(0, min(width, filled))
        empty = width - filled
        return "[" + "#" * filled + "-" * empty + f"] {self.current_hp}/{self.max_hp}"

    def __str__(self):
        skills = ", ".join(self.skill_names)
        return (
            f"{self.name} ({self.element}) - HP: {self.max_hp}, "
            f"ATK: {self.attack}, DEF: {self.defense}, SPD: {self.speed}, "
            f"Skills: {skills}"
        )


class BattleResult:
    """Result from one simulated battle."""

    def __init__(
        self,
        player_name,
        enemy_name,
        player_won,
        turns,
        player_remaining_hp,
        enemy_remaining_hp,
        battle_log,
    ):
        self.player_name = player_name
        self.enemy_name = enemy_name
        self.player_won = bool(player_won)
        self.turns = int(turns)
        self.player_remaining_hp = int(player_remaining_hp)
        self.enemy_remaining_hp = int(enemy_remaining_hp)
        self.battle_log = list(battle_log)

    def winner_name(self):
        """Return the winner's name."""
        if self.player_won:
            return self.player_name
        return self.enemy_name

    def to_text(self):
        """Return a readable text report for one battle."""
        lines = []
        lines.append("=== Single Battle Report ===")
        lines.append(f"Player Creature: {self.player_name}")
        lines.append(f"Enemy Creature: {self.enemy_name}")
        lines.append(f"Winner: {self.winner_name()}")
        lines.append(f"Battle Length: {self.turns} turns")
        lines.append(f"Player Remaining HP: {self.player_remaining_hp}")
        lines.append(f"Enemy Remaining HP: {self.enemy_remaining_hp}")
        lines.append("")
        lines.append("Battle Log:")
        lines.extend(self.battle_log)
        return "\n".join(lines)


class BalanceReport:
    """Summary report from multiple battle simulations."""

    def __init__(
        self,
        player_name,
        enemy_name,
        simulations,
        player_wins,
        enemy_wins,
        average_turns,
        average_player_remaining_hp,
        average_enemy_remaining_hp,
    ):
        self.player_name = player_name
        self.enemy_name = enemy_name
        self.simulations = int(simulations)
        self.player_wins = int(player_wins)
        self.enemy_wins = int(enemy_wins)
        self.average_turns = float(average_turns)
        self.average_player_remaining_hp = float(average_player_remaining_hp)
        self.average_enemy_remaining_hp = float(average_enemy_remaining_hp)

    def player_win_rate(self):
        """Return the player's win rate as a percentage."""
        if self.simulations == 0:
            return 0.0
        return (self.player_wins / self.simulations) * 100

    def rating(self):
        """Return a balance rating based on player win rate."""
        rate = self.player_win_rate()
        if rate < 35:
            return "Too hard for the player"
        if rate < 45:
            return "Slightly hard"
        if rate <= 60:
            return "Balanced"
        if rate <= 75:
            return "Slightly easy"
        return "Too easy for the player"

    def suggestions(self):
        """Return design suggestions based on simulation results."""
        rate = self.player_win_rate()
        suggestions = []

        if rate > 75:
            suggestions.append("Enemy may need higher HP, attack, or defense.")
            suggestions.append("Player skills may be too efficient for this matchup.")
        elif rate < 35:
            suggestions.append("Enemy may be too strong for the player creature.")
            suggestions.append("Consider improving player HP, defense, or skill power.")
        elif rate > 60:
            suggestions.append("Encounter is playable but may feel easy.")
            suggestions.append("Slightly increase enemy stats if this is a boss battle.")
        elif rate < 45:
            suggestions.append("Encounter is playable but may feel punishing.")
            suggestions.append("Slightly reduce enemy damage or defense.")
        else:
            suggestions.append("Win rate is within the balanced target range.")

        if self.average_turns <= 2:
            suggestions.append("Battle ends very quickly; consider increasing HP or lowering damage.")
        elif self.average_turns >= 10:
            suggestions.append("Battle may feel too slow; consider increasing damage or reducing defense.")

        if self.average_player_remaining_hp <= 3 and rate >= 45:
            suggestions.append("Player wins are very close; this could create high tension.")

        return suggestions

    def to_text(self):
        """Return the full report as readable text."""
        lines = []
        lines.append("=== SpiritForge Balance Report ===")
        lines.append(f"Player Creature: {self.player_name}")
        lines.append(f"Enemy Creature: {self.enemy_name}")
        lines.append(f"Simulations: {self.simulations}")
        lines.append("")
        lines.append(f"Player Wins: {self.player_wins}")
        lines.append(f"Enemy Wins: {self.enemy_wins}")
        lines.append(f"Player Win Rate: {self.player_win_rate():.2f}%")
        lines.append(f"Average Battle Length: {self.average_turns:.2f} turns")
        lines.append(
            f"Average Player Remaining HP: {self.average_player_remaining_hp:.2f}"
        )
        lines.append(
            f"Average Enemy Remaining HP: {self.average_enemy_remaining_hp:.2f}"
        )
        lines.append("")
        lines.append("Balance Rating:")
        lines.append(self.rating())
        lines.append("")
        lines.append("Design Suggestions:")
        for suggestion in self.suggestions():
            lines.append(f"- {suggestion}")
        return "\n".join(lines)
