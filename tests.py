"""Simple built-in tests for SpiritForge.

This avoids external testing libraries, so the program remains easy to run on
an examiner's machine. The tests check important battle logic.
"""

from models import Creature, Skill
from simulator import BattleSimulator


def _record_result(results, test_name, passed, message=""):
    """Add one formatted test result to the results list."""
    if passed:
        results.append(f"[PASS] {test_name}")
    else:
        results.append(f"[FAIL] {test_name}: {message}")


def run_all_tests():
    """Run simple system tests and return a readable summary string."""
    results = []
    passed_count = 0
    total_count = 0

    # Test data with 100% accuracy to avoid random failures.
    test_skills = {
        "Test Flame": Skill("Test Flame", "fire", 10, 100),
        "Test Water": Skill("Test Water", "water", 10, 100),
    }
    simulator = BattleSimulator(test_skills)

    # Test 1: Type chart, fire attacks grass.
    total_count += 1
    try:
        passed = simulator.get_type_multiplier("fire", "grass") == 2.0
        _record_result(results, "Fire vs Grass multiplier should be 2.0", passed)
        if passed:
            passed_count += 1
    except Exception as error:
        _record_result(results, "Fire vs Grass multiplier should be 2.0", False, str(error))

    # Test 2: Type chart, fire attacks water.
    total_count += 1
    try:
        passed = simulator.get_type_multiplier("fire", "water") == 0.5
        _record_result(results, "Fire vs Water multiplier should be 0.5", passed)
        if passed:
            passed_count += 1
    except Exception as error:
        _record_result(results, "Fire vs Water multiplier should be 0.5", False, str(error))

    # Test 3: Damage calculation should apply type multiplier.
    total_count += 1
    try:
        attacker = Creature("Attacker", "fire", 100, 10, 5, 10, ["Test Flame"])
        defender = Creature("Defender", "grass", 100, 10, 5, 10, ["Test Water"])
        damage = simulator.calculate_damage(attacker, defender, test_skills["Test Flame"])
        # base = 10 + 10 - 5 = 15, fire vs grass = x2, final = 30
        passed = damage == 30
        _record_result(results, "Damage calculation should include type multiplier", passed)
        if passed:
            passed_count += 1
    except Exception as error:
        _record_result(results, "Damage calculation should include type multiplier", False, str(error))

    # Test 4: Damage should never be below 1.
    total_count += 1
    try:
        weak = Creature("Weak", "fire", 100, 0, 0, 10, ["Test Flame"])
        tank = Creature("Tank", "water", 100, 0, 999, 10, ["Test Water"])
        damage = simulator.calculate_damage(weak, tank, test_skills["Test Flame"])
        passed = damage >= 1
        _record_result(results, "Damage should never be below 1", passed)
        if passed:
            passed_count += 1
    except Exception as error:
        _record_result(results, "Damage should never be below 1", False, str(error))

    # Test 5: Invalid skill accuracy should raise ValueError.
    total_count += 1
    try:
        Skill("Bad Accuracy", "fire", 10, 150)
        _record_result(results, "Invalid skill accuracy should raise ValueError", False, "No error raised")
    except ValueError:
        _record_result(results, "Invalid skill accuracy should raise ValueError", True)
        passed_count += 1
    except Exception as error:
        _record_result(results, "Invalid skill accuracy should raise ValueError", False, str(error))

    # Test 6: Invalid creature HP should raise ValueError.
    total_count += 1
    try:
        Creature("Bad HP", "fire", 0, 10, 10, 10, ["Test Flame"])
        _record_result(results, "Invalid creature HP should raise ValueError", False, "No error raised")
    except ValueError:
        _record_result(results, "Invalid creature HP should raise ValueError", True)
        passed_count += 1
    except Exception as error:
        _record_result(results, "Invalid creature HP should raise ValueError", False, str(error))

    # Test 7: A strong creature should win a simple battle.
    total_count += 1
    try:
        strong = Creature("Strong", "fire", 100, 30, 10, 20, ["Test Flame"])
        weak_enemy = Creature("Weak Enemy", "grass", 30, 5, 5, 1, ["Test Water"])
        result = simulator.run_one_battle(strong, weak_enemy, show_log=False)
        passed = result.player_won
        _record_result(results, "Strong creature should win simple battle", passed)
        if passed:
            passed_count += 1
    except Exception as error:
        _record_result(results, "Strong creature should win simple battle", False, str(error))

    summary = []
    summary.append("=== Running SpiritForge System Tests ===")
    summary.extend(results)
    summary.append("")
    summary.append(f"{passed_count}/{total_count} tests passed.")
    return "\n".join(summary)
