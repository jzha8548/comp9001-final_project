"""Battle simulation logic for SpiritForge."""

import random

from config import TYPE_CHART, VALID_ELEMENTS
from models import BattleResult, BalanceReport


class BattleSimulator:
    """Simulates one or many creature battles.

    The simulator is separated from the menu so the battle logic can be reused
    and tested more easily.
    """

    def __init__(self, skills, max_turns=50):
        self.skills = skills
        self.max_turns = int(max_turns)
        if self.max_turns <= 0:
            raise ValueError("max_turns must be greater than 0.")

    def get_type_multiplier(self, attacking_element, defending_element):
        """Return type effectiveness multiplier using a 2D list chart."""
        attack = attacking_element.strip().lower()
        defend = defending_element.strip().lower()
        if attack not in VALID_ELEMENTS:
            raise ValueError(f"Invalid attacking element: {attacking_element}")
        if defend not in VALID_ELEMENTS:
            raise ValueError(f"Invalid defending element: {defending_element}")

        attack_index = VALID_ELEMENTS.index(attack)
        defend_index = VALID_ELEMENTS.index(defend)
        return TYPE_CHART[attack_index][defend_index]

    def get_effectiveness_text(self, multiplier):
        """Return battle text for a type multiplier."""
        if multiplier > 1:
            return "It was super effective!"
        if multiplier < 1:
            return "It was not very effective."
        return "It had normal effectiveness."

    def calculate_damage(self, attacker, defender, skill):
        """Calculate final damage from attacker to defender using a skill."""
        base_damage = max(1, attacker.attack + skill.power - defender.defense)
        multiplier = self.get_type_multiplier(skill.element, defender.element)
        final_damage = int(base_damage * multiplier)
        return max(1, final_damage)

    def choose_skill(self, attacker, defender):
        """Choose the best available skill by expected damage.

        Expected damage considers skill power, type multiplier, and accuracy.
        This creates a simple AI suitable for automated balance testing.
        """
        available_skills = []
        for skill_name in attacker.skill_names:
            if skill_name in self.skills:
                available_skills.append(self.skills[skill_name])

        if len(available_skills) == 0:
            raise ValueError(f"{attacker.name} has no valid skills in the skill database.")

        best_skill = available_skills[0]
        best_score = -1
        for skill in available_skills:
            damage = self.calculate_damage(attacker, defender, skill)
            expected_score = damage * (skill.accuracy / 100)
            if expected_score > best_score:
                best_score = expected_score
                best_skill = skill
        return best_skill

    def skill_hits(self, skill):
        """Return True if a skill hits based on its accuracy."""
        roll = random.randint(1, 100)
        return roll <= skill.accuracy

    def perform_attack(self, attacker, defender, battle_log):
        """Perform one attack and add readable messages to the battle log."""
        skill = self.choose_skill(attacker, defender)
        battle_log.append(f"{attacker.name} used {skill.name}.")

        if not self.skill_hits(skill):
            battle_log.append(f"{skill.name} missed!")
            return

        multiplier = self.get_type_multiplier(skill.element, defender.element)
        damage = self.calculate_damage(attacker, defender, skill)
        defender.take_damage(damage)

        battle_log.append(self.get_effectiveness_text(multiplier))
        battle_log.append(
            f"{defender.name} took {damage} damage. "
            f"HP: {defender.hp_bar_text()}"
        )

    def get_turn_order(self, player, enemy):
        """Return a list of attacker/defender pairs for one turn."""
        if player.speed >= enemy.speed:
            return [(player, enemy), (enemy, player)]
        return [(enemy, player), (player, enemy)]

    def run_one_battle(self, player_creature, enemy_creature, show_log=True):
        """Run one battle and return a BattleResult object."""
        player = player_creature.clone()
        enemy = enemy_creature.clone()
        player.reset_hp()
        enemy.reset_hp()

        battle_log = []
        if show_log:
            first_attacker = self.get_turn_order(player, enemy)[0][0]
            battle_log.append("=== Battle Start ===")
            battle_log.append(f"{player.name} vs {enemy.name}")
            battle_log.append(
                f"Turn order is decided by speed. First attacker: {first_attacker.name}."
            )
            battle_log.append(f"{player.name} HP: {player.hp_bar_text()}")
            battle_log.append(f"{enemy.name} HP: {enemy.hp_bar_text()}")
            battle_log.append("")

        turns = 0
        while player.is_alive() and enemy.is_alive() and turns < self.max_turns:
            turns += 1
            if show_log:
                battle_log.append(f"Turn {turns}:")

            turn_order = self.get_turn_order(player, enemy)
            for attacker, defender in turn_order:
                if not attacker.is_alive() or not defender.is_alive():
                    continue
                self.perform_attack(attacker, defender, battle_log)
                if not defender.is_alive():
                    battle_log.append(f"{defender.name} fainted!")
                    break

            if show_log:
                battle_log.append(f"Status: {player.name} {player.hp_bar_text()} | {enemy.name} {enemy.hp_bar_text()}")
                battle_log.append("")

            if not player.is_alive() or not enemy.is_alive():
                break

        # If max_turns is reached, decide the winner by HP percentage.
        if player.is_alive() and enemy.is_alive():
            player_ratio = player.current_hp / player.max_hp
            enemy_ratio = enemy.current_hp / enemy.max_hp
            player_won = player_ratio >= enemy_ratio
            battle_log.append("Turn limit reached. Winner decided by remaining HP ratio.")
        else:
            player_won = player.is_alive()

        result = BattleResult(
            player.name,
            enemy.name,
            player_won,
            turns,
            player.current_hp,
            enemy.current_hp,
            battle_log,
        )
        return result

    def run_many_battles(self, player_creature, enemy_creature, simulations):
        """Run multiple battles and return a BalanceReport."""
        simulations = int(simulations)
        if simulations <= 0:
            raise ValueError("Number of simulations must be greater than 0.")

        player_wins = 0
        enemy_wins = 0
        total_turns = 0
        total_player_remaining_hp = 0
        total_enemy_remaining_hp = 0

        for _ in range(simulations):
            result = self.run_one_battle(player_creature, enemy_creature, show_log=False)
            if result.player_won:
                player_wins += 1
            else:
                enemy_wins += 1
            total_turns += result.turns
            total_player_remaining_hp += result.player_remaining_hp
            total_enemy_remaining_hp += result.enemy_remaining_hp

        average_turns = total_turns / simulations
        average_player_remaining_hp = total_player_remaining_hp / simulations
        average_enemy_remaining_hp = total_enemy_remaining_hp / simulations

        return BalanceReport(
            player_creature.name,
            enemy_creature.name,
            simulations,
            player_wins,
            enemy_wins,
            average_turns,
            average_player_remaining_hp,
            average_enemy_remaining_hp,
        )
