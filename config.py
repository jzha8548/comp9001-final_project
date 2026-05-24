"""Configuration values for SpiritForge.

This file keeps the battle type chart and default file names in one place.
The TYPE_CHART is a multi-dimensional list: rows are attacking elements,
columns are defending elements.
"""

# The order of this list matters because TYPE_CHART uses the same order for
# both row labels and column labels.
VALID_ELEMENTS = ["fire", "water", "grass", "electric", "rock"]

# Multi-dimensional list for type effectiveness.
# Columns:      fire  water grass electric rock
TYPE_CHART = [
    [1.0,  0.5,  2.0,  1.0,     0.5],  # fire attacks
    [2.0,  1.0,  0.5,  1.0,     1.0],  # water attacks
    [0.5,  2.0,  1.0,  1.0,     2.0],  # grass attacks
    [1.0,  2.0,  0.5,  1.0,     0.5],  # electric attacks
    [2.0,  1.0,  1.0,  2.0,     1.0],  # rock attacks
]

DEFAULT_CREATURE_FILE = "creatures.txt"
DEFAULT_SKILL_FILE = "skills.txt"
DEFAULT_REPORT_FILE = "balance_report.txt"
DEFAULT_HISTORY_FILE = "battle_history.txt"
