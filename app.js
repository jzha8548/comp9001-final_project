const VALID_ELEMENTS = ["fire", "water", "grass", "electric", "rock"];

// Multi-dimensional list: row = attacking type, column = defending type.
const TYPE_CHART = [
  [1.0, 0.5, 2.0, 1.0, 0.5],
  [2.0, 1.0, 0.5, 1.0, 1.0],
  [0.5, 2.0, 1.0, 1.0, 2.0],
  [1.0, 2.0, 0.5, 1.0, 0.5],
  [2.0, 1.0, 1.0, 2.0, 1.0],
];

const FALLBACK_CREATURE_TEXT = `# name,element,hp,attack,defense,speed,skill1|skill2
Flarefox,fire,80,24,10,18,Ember|Flame Claw
Aquari,water,90,20,14,12,Aqua Shot|Bubble Guard
Leafling,grass,75,22,12,20,Leaf Blade|Vine Hit
Voltbat,electric,70,26,8,25,Spark|Thunder Bite
Stonehorn,rock,110,18,22,8,Rock Smash|Stone Charge
Sproutrex,grass,95,19,16,10,Vine Hit|Solar Seed
Steamlord,water,100,23,15,11,Aqua Shot|Steam Burst`;

const FALLBACK_SKILL_TEXT = `# name,element,power,accuracy
Ember,fire,18,90
Flame Claw,fire,25,80
Aqua Shot,water,20,90
Bubble Guard,water,14,100
Leaf Blade,grass,22,85
Vine Hit,grass,16,95
Spark,electric,20,90
Thunder Bite,electric,28,75
Rock Smash,rock,24,85
Stone Charge,rock,30,70
Solar Seed,grass,26,80
Steam Burst,water,28,75`;

let creatures = {};
let skills = {};
let latestReportText = "";

class Skill {
  constructor(name, element, power, accuracy) {
    this.name = name.trim();
    this.element = element.trim().toLowerCase();
    this.power = Number(power);
    this.accuracy = Number(accuracy);
    this.validate();
  }

  validate() {
    if (!this.name) throw new Error("Skill name cannot be empty.");
    if (!VALID_ELEMENTS.includes(this.element)) {
      throw new Error(`Skill '${this.name}' has invalid element '${this.element}'.`);
    }
    if (this.power <= 0) throw new Error(`Skill '${this.name}' power must be greater than 0.`);
    if (this.accuracy < 1 || this.accuracy > 100) {
      throw new Error(`Skill '${this.name}' accuracy must be between 1 and 100.`);
    }
  }
}

class Creature {
  constructor(name, element, hp, attack, defense, speed, skillNames) {
    this.name = name.trim();
    this.element = element.trim().toLowerCase();
    this.maxHp = Number(hp);
    this.currentHp = Number(hp);
    this.attack = Number(attack);
    this.defense = Number(defense);
    this.speed = Number(speed);
    this.skillNames = skillNames.map((name) => name.trim()).filter(Boolean);
    this.validate();
  }

  validate() {
    if (!this.name) throw new Error("Creature name cannot be empty.");
    if (!VALID_ELEMENTS.includes(this.element)) {
      throw new Error(`Creature '${this.name}' has invalid element '${this.element}'.`);
    }
    if (this.maxHp <= 0) throw new Error(`Creature '${this.name}' HP must be greater than 0.`);
    if (this.attack < 0) throw new Error(`Creature '${this.name}' attack cannot be negative.`);
    if (this.defense < 0) throw new Error(`Creature '${this.name}' defense cannot be negative.`);
    if (this.speed < 0) throw new Error(`Creature '${this.name}' speed cannot be negative.`);
    if (this.skillNames.length === 0) throw new Error(`Creature '${this.name}' must have at least one skill.`);
  }

  clone() {
    return new Creature(this.name, this.element, this.maxHp, this.attack, this.defense, this.speed, [...this.skillNames]);
  }

  resetHp() {
    this.currentHp = this.maxHp;
  }

  takeDamage(amount) {
    if (amount < 0) throw new Error("Damage amount cannot be negative.");
    this.currentHp = Math.max(0, this.currentHp - Math.floor(amount));
  }

  isAlive() {
    return this.currentHp > 0;
  }
}

class BalanceReport {
  constructor(playerName, enemyName, simulations, playerWins, enemyWins, averageTurns, averagePlayerHp, averageEnemyHp) {
    this.playerName = playerName;
    this.enemyName = enemyName;
    this.simulations = simulations;
    this.playerWins = playerWins;
    this.enemyWins = enemyWins;
    this.averageTurns = averageTurns;
    this.averagePlayerHp = averagePlayerHp;
    this.averageEnemyHp = averageEnemyHp;
  }

  playerWinRate() {
    return this.simulations === 0 ? 0 : (this.playerWins / this.simulations) * 100;
  }

  rating() {
    const rate = this.playerWinRate();
    if (rate < 35) return "Too hard for the player";
    if (rate < 45) return "Slightly hard";
    if (rate <= 60) return "Balanced";
    if (rate <= 75) return "Slightly easy";
    return "Too easy for the player";
  }

  suggestions() {
    const rate = this.playerWinRate();
    const suggestions = [];

    if (rate > 75) {
      suggestions.push("Enemy may need higher HP, attack, or defense.");
      suggestions.push("Player skills may be too efficient for this matchup.");
    } else if (rate < 35) {
      suggestions.push("Enemy may be too strong for the player creature.");
      suggestions.push("Consider improving player HP, defense, or skill power.");
    } else if (rate > 60) {
      suggestions.push("Encounter is playable but may feel easy.");
      suggestions.push("Slightly increase enemy stats if this is a boss battle.");
    } else if (rate < 45) {
      suggestions.push("Encounter is playable but may feel punishing.");
      suggestions.push("Slightly reduce enemy damage or defense.");
    } else {
      suggestions.push("Win rate is within the balanced target range.");
    }

    if (this.averageTurns <= 2) {
      suggestions.push("Battle ends very quickly; consider increasing HP or lowering damage.");
    } else if (this.averageTurns >= 10) {
      suggestions.push("Battle may feel too slow; consider increasing damage or reducing defense.");
    }

    if (this.averagePlayerHp <= 3 && rate >= 45) {
      suggestions.push("Player wins are very close; this could create high tension.");
    }

    return suggestions;
  }

  toText() {
    return [
      "=== SpiritForge Balance Report ===",
      `Player Creature: ${this.playerName}`,
      `Enemy Creature: ${this.enemyName}`,
      `Simulations: ${this.simulations}`,
      "",
      `Player Wins: ${this.playerWins}`,
      `Enemy Wins: ${this.enemyWins}`,
      `Player Win Rate: ${this.playerWinRate().toFixed(2)}%`,
      `Average Battle Length: ${this.averageTurns.toFixed(2)} turns`,
      `Average Player Remaining HP: ${this.averagePlayerHp.toFixed(2)}`,
      `Average Enemy Remaining HP: ${this.averageEnemyHp.toFixed(2)}`,
      "",
      `Balance Rating: ${this.rating()}`,
      "",
      "Design Suggestions:",
      ...this.suggestions().map((item) => `- ${item}`),
    ].join("\n");
  }
}

class BattleSimulator {
  constructor(skillMap, maxTurns = 50) {
    this.skills = skillMap;
    this.maxTurns = maxTurns;
    if (this.maxTurns <= 0) throw new Error("maxTurns must be greater than 0.");
  }

  getTypeMultiplier(attackingElement, defendingElement) {
    const attack = attackingElement.trim().toLowerCase();
    const defend = defendingElement.trim().toLowerCase();
    if (!VALID_ELEMENTS.includes(attack)) throw new Error(`Invalid attacking element: ${attackingElement}`);
    if (!VALID_ELEMENTS.includes(defend)) throw new Error(`Invalid defending element: ${defendingElement}`);
    return TYPE_CHART[VALID_ELEMENTS.indexOf(attack)][VALID_ELEMENTS.indexOf(defend)];
  }

  effectivenessText(multiplier) {
    if (multiplier > 1) return "It was super effective!";
    if (multiplier < 1) return "It was not very effective.";
    return "It had normal effectiveness.";
  }

  calculateDamage(attacker, defender, skill) {
    const baseDamage = Math.max(1, attacker.attack + skill.power - defender.defense);
    const multiplier = this.getTypeMultiplier(skill.element, defender.element);
    return Math.max(1, Math.floor(baseDamage * multiplier));
  }

  chooseSkill(attacker, defender) {
    const availableSkills = attacker.skillNames
      .filter((skillName) => this.skills[skillName])
      .map((skillName) => this.skills[skillName]);

    if (availableSkills.length === 0) {
      throw new Error(`${attacker.name} has no valid skills in the skill database.`);
    }

    let bestSkill = availableSkills[0];
    let bestScore = -1;
    for (const skill of availableSkills) {
      const damage = this.calculateDamage(attacker, defender, skill);
      const expectedScore = damage * (skill.accuracy / 100);
      if (expectedScore > bestScore) {
        bestScore = expectedScore;
        bestSkill = skill;
      }
    }
    return bestSkill;
  }

  skillHits(skill) {
    const roll = Math.floor(Math.random() * 100) + 1;
    return roll <= skill.accuracy;
  }

  getTurnOrder(player, enemy) {
    if (player.speed >= enemy.speed) return [[player, enemy], [enemy, player]];
    return [[enemy, player], [player, enemy]];
  }

  performAttack(attacker, defender, battleLog) {
    const skill = this.chooseSkill(attacker, defender);
    battleLog.push(`${attacker.name} used ${skill.name}.`);

    if (!this.skillHits(skill)) {
      battleLog.push(`${skill.name} missed!`);
      return;
    }

    const multiplier = this.getTypeMultiplier(skill.element, defender.element);
    const damage = this.calculateDamage(attacker, defender, skill);
    defender.takeDamage(damage);

    battleLog.push(this.effectivenessText(multiplier));
    battleLog.push(`${defender.name} took ${damage} damage. HP: ${defender.currentHp}/${defender.maxHp}`);
  }

  runOneBattle(playerCreature, enemyCreature, showLog = true) {
    const player = playerCreature.clone();
    const enemy = enemyCreature.clone();
    player.resetHp();
    enemy.resetHp();
    const battleLog = [];

    if (showLog) {
      const firstAttacker = this.getTurnOrder(player, enemy)[0][0];
      battleLog.push("=== Battle Start ===");
      battleLog.push(`${player.name} vs ${enemy.name}`);
      battleLog.push(`Turn order is decided by speed. First attacker: ${firstAttacker.name}.`);
      battleLog.push(`${player.name} HP: ${player.currentHp}/${player.maxHp}`);
      battleLog.push(`${enemy.name} HP: ${enemy.currentHp}/${enemy.maxHp}`);
      battleLog.push("");
    }

    let turns = 0;
    while (player.isAlive() && enemy.isAlive() && turns < this.maxTurns) {
      turns += 1;
      if (showLog) battleLog.push(`Turn ${turns}:`);

      const turnOrder = this.getTurnOrder(player, enemy);
      for (const [attacker, defender] of turnOrder) {
        if (!attacker.isAlive() || !defender.isAlive()) continue;
        this.performAttack(attacker, defender, battleLog);
        if (!defender.isAlive()) {
          battleLog.push(`${defender.name} fainted!`);
          break;
        }
      }

      if (showLog) {
        battleLog.push(`Status: ${player.name} ${player.currentHp}/${player.maxHp} | ${enemy.name} ${enemy.currentHp}/${enemy.maxHp}`);
        battleLog.push("");
      }

      if (!player.isAlive() || !enemy.isAlive()) break;
    }

    let playerWon;
    if (player.isAlive() && enemy.isAlive()) {
      const playerRatio = player.currentHp / player.maxHp;
      const enemyRatio = enemy.currentHp / enemy.maxHp;
      playerWon = playerRatio >= enemyRatio;
      battleLog.push("Turn limit reached. Winner decided by remaining HP ratio.");
    } else {
      playerWon = player.isAlive();
    }

    return {
      playerName: player.name,
      enemyName: enemy.name,
      playerWon,
      turns,
      playerRemainingHp: player.currentHp,
      enemyRemainingHp: enemy.currentHp,
      battleLog,
      winnerName: playerWon ? player.name : enemy.name,
    };
  }

  runManyBattles(playerCreature, enemyCreature, simulations) {
    if (simulations <= 0) throw new Error("Number of simulations must be greater than 0.");

    let playerWins = 0;
    let enemyWins = 0;
    let totalTurns = 0;
    let totalPlayerHp = 0;
    let totalEnemyHp = 0;

    for (let i = 0; i < simulations; i += 1) {
      const result = this.runOneBattle(playerCreature, enemyCreature, false);
      if (result.playerWon) playerWins += 1;
      else enemyWins += 1;
      totalTurns += result.turns;
      totalPlayerHp += result.playerRemainingHp;
      totalEnemyHp += result.enemyRemainingHp;
    }

    return new BalanceReport(
      playerCreature.name,
      enemyCreature.name,
      simulations,
      playerWins,
      enemyWins,
      totalTurns / simulations,
      totalPlayerHp / simulations,
      totalEnemyHp / simulations,
    );
  }
}

function parseCreatures(text) {
  const result = {};
  const warnings = [];
  text.split(/\r?\n/).forEach((line, index) => {
    const clean = line.trim();
    if (!clean || clean.startsWith("#")) return;
    const parts = clean.split(",");
    if (parts.length !== 7) {
      warnings.push(`Line ${index + 1}: expected 7 fields.`);
      return;
    }
    try {
      const [name, element, hp, attack, defense, speed, skillsText] = parts;
      result[name.trim()] = new Creature(name, element, hp, attack, defense, speed, skillsText.split("|"));
    } catch (error) {
      warnings.push(`Line ${index + 1}: ${error.message}`);
    }
  });
  return { result, warnings };
}

function parseSkills(text) {
  const result = {};
  const warnings = [];
  text.split(/\r?\n/).forEach((line, index) => {
    const clean = line.trim();
    if (!clean || clean.startsWith("#")) return;
    const parts = clean.split(",");
    if (parts.length !== 4) {
      warnings.push(`Line ${index + 1}: expected 4 fields.`);
      return;
    }
    try {
      const [name, element, power, accuracy] = parts;
      result[name.trim()] = new Skill(name, element, power, accuracy);
    } catch (error) {
      warnings.push(`Line ${index + 1}: ${error.message}`);
    }
  });
  return { result, warnings };
}

async function fetchText(path, fallback) {
  try {
    const response = await fetch(path);
    if (!response.ok) throw new Error(`Could not load ${path}`);
    return await response.text();
  } catch (error) {
    console.warn(`${path} could not be fetched. Using embedded fallback data.`, error);
    return fallback;
  }
}

async function loadData() {
  const creatureText = await fetchText("data/creatures.txt", FALLBACK_CREATURE_TEXT);
  const skillText = await fetchText("data/skills.txt", FALLBACK_SKILL_TEXT);
  const creatureData = parseCreatures(creatureText);
  const skillData = parseSkills(skillText);
  creatures = creatureData.result;
  skills = skillData.result;
  populateSelectors();
  renderDatabaseTables();
  renderTypeChart();
  setDataStatus(creatureData.warnings, skillData.warnings);
}

function setDataStatus(creatureWarnings = [], skillWarnings = []) {
  const status = document.getElementById("dataStatus");
  const warningText = [...creatureWarnings, ...skillWarnings];
  status.innerHTML = `${Object.keys(creatures).length} creatures loaded<br>${Object.keys(skills).length} skills loaded` +
    (warningText.length ? `<br><br><strong>Warnings:</strong><br>${warningText.map(escapeHtml).join("<br>")}` : "");
}

function populateSelectors() {
  const playerSelect = document.getElementById("playerSelect");
  const enemySelect = document.getElementById("enemySelect");
  const names = Object.keys(creatures);
  playerSelect.innerHTML = names.map((name) => `<option value="${escapeAttr(name)}">${escapeHtml(name)}</option>`).join("");
  enemySelect.innerHTML = names.map((name) => `<option value="${escapeAttr(name)}">${escapeHtml(name)}</option>`).join("");
  playerSelect.value = names.includes("Flarefox") ? "Flarefox" : names[0];
  enemySelect.value = names.includes("Leafling") ? "Leafling" : names[1] || names[0];
}

function getSelectedCreatures() {
  const playerName = document.getElementById("playerSelect").value;
  const enemyName = document.getElementById("enemySelect").value;
  if (!creatures[playerName] || !creatures[enemyName]) throw new Error("Please select valid creatures.");
  return [creatures[playerName], creatures[enemyName]];
}

function getSimulationCount() {
  const raw = Number(document.getElementById("simulationCount").value);
  if (!Number.isInteger(raw) || raw <= 0) throw new Error("Please enter a positive whole number of simulations.");
  return raw;
}

function getSimulator() {
  return new BattleSimulator(skills);
}

function renderDatabaseTables() {
  const creatureRows = Object.values(creatures).map((c) => `
    <tr>
      <td><strong>${escapeHtml(c.name)}</strong><br><span class="badge">${escapeHtml(c.element)}</span></td>
      <td>${c.maxHp}</td><td>${c.attack}</td><td>${c.defense}</td><td>${c.speed}</td>
      <td>${c.skillNames.map(escapeHtml).join(", ")}</td>
    </tr>`).join("");

  document.getElementById("creatureTable").innerHTML = `
    <div class="table-wrap"><table class="table">
      <thead><tr><th>Name</th><th>HP</th><th>ATK</th><th>DEF</th><th>SPD</th><th>Skills</th></tr></thead>
      <tbody>${creatureRows}</tbody>
    </table></div>`;

  const skillRows = Object.values(skills).map((s) => `
    <tr>
      <td><strong>${escapeHtml(s.name)}</strong><br><span class="badge">${escapeHtml(s.element)}</span></td>
      <td>${s.power}</td>
      <td>${s.accuracy}%</td>
    </tr>`).join("");

  document.getElementById("skillTable").innerHTML = `
    <div class="table-wrap"><table class="table">
      <thead><tr><th>Name</th><th>Power</th><th>Accuracy</th></tr></thead>
      <tbody>${skillRows}</tbody>
    </table></div>`;
}

function renderTypeChart() {
  const header = VALID_ELEMENTS.map((type) => `<th>${escapeHtml(type)}</th>`).join("");
  const rows = TYPE_CHART.map((row, rowIndex) => {
    const cells = row.map((value) => `<td class="${multiplierClass(value)}">${value.toFixed(1)}×</td>`).join("");
    return `<tr><th>${escapeHtml(VALID_ELEMENTS[rowIndex])}</th>${cells}</tr>`;
  }).join("");

  document.getElementById("typeChart").innerHTML = `
    <p class="muted">Rows are attacking types. Columns are defending types.</p>
    <div class="table-wrap"><table class="table">
      <thead><tr><th>Attack ↓ / Defend →</th>${header}</tr></thead>
      <tbody>${rows}</tbody>
    </table></div>`;
}

function renderCreatureCard(creature, label) {
  return `
    <div class="creature-card">
      <h4>${escapeHtml(label)}: ${escapeHtml(creature.name)}</h4>
      <span class="badge">${escapeHtml(creature.element)}</span>
      <div class="stat-grid">
        <div class="stat"><span>HP</span><strong>${creature.maxHp}</strong></div>
        <div class="stat"><span>ATK</span><strong>${creature.attack}</strong></div>
        <div class="stat"><span>DEF</span><strong>${creature.defense}</strong></div>
        <div class="stat"><span>SPD</span><strong>${creature.speed}</strong></div>
      </div>
      <p class="muted">Skills: ${creature.skillNames.map(escapeHtml).join(", ")}</p>
    </div>`;
}

function skillPreviewRows(attacker, defender, simulator) {
  return attacker.skillNames
    .filter((name) => skills[name])
    .map((name) => {
      const skill = skills[name];
      const multiplier = simulator.getTypeMultiplier(skill.element, defender.element);
      const damage = simulator.calculateDamage(attacker, defender, skill);
      const expected = damage * (skill.accuracy / 100);
      return `
        <tr>
          <td><strong>${escapeHtml(skill.name)}</strong><br><span class="badge">${escapeHtml(skill.element)}</span></td>
          <td>${skill.power}</td>
          <td>${skill.accuracy}%</td>
          <td class="${multiplierClass(multiplier)}">${multiplier.toFixed(1)}×</td>
          <td>${damage}</td>
          <td>${expected.toFixed(1)}</td>
        </tr>`;
    }).join("");
}

function renderMatchupPreview() {
  const [player, enemy] = getSelectedCreatures();
  const simulator = getSimulator();
  const firstAttacker = simulator.getTurnOrder(player, enemy)[0][0].name;

  document.getElementById("matchupPreview").innerHTML = `
    <div class="card-row">
      ${renderCreatureCard(player, "Player")}
      ${renderCreatureCard(enemy, "Enemy")}
    </div>
    <p><strong>Turn order:</strong> ${escapeHtml(firstAttacker)} moves first because of speed.</p>
    <h4>${escapeHtml(player.name)} skill preview against ${escapeHtml(enemy.name)}</h4>
    ${renderSkillPreviewTable(skillPreviewRows(player, enemy, simulator))}
    <h4>${escapeHtml(enemy.name)} skill preview against ${escapeHtml(player.name)}</h4>
    ${renderSkillPreviewTable(skillPreviewRows(enemy, player, simulator))}`;
}

function renderSkillPreviewTable(rows) {
  return `
    <div class="table-wrap"><table class="table">
      <thead><tr><th>Skill</th><th>Power</th><th>Accuracy</th><th>Type</th><th>Damage</th><th>Expected</th></tr></thead>
      <tbody>${rows}</tbody>
    </table></div>`;
}

function runSingleBattle() {
  renderMatchupPreview();
  const [player, enemy] = getSelectedCreatures();
  const simulator = getSimulator();
  const result = simulator.runOneBattle(player, enemy, true);
  latestReportText = singleBattleText(result);

  document.getElementById("battleLog").classList.remove("empty-state");
  document.getElementById("battleLog").textContent = result.battleLog.join("\n");

  document.getElementById("balanceReport").innerHTML = `
    <div class="rating ${result.playerWon ? "good" : "bad"}">Single battle winner: ${escapeHtml(result.winnerName)}</div>
    <div class="report-highlight">
      <div class="metric"><span>Turns</span><strong>${result.turns}</strong></div>
      <div class="metric"><span>Player HP</span><strong>${result.playerRemainingHp}</strong></div>
      <div class="metric"><span>Enemy HP</span><strong>${result.enemyRemainingHp}</strong></div>
    </div>
    <p class="muted">For more reliable design feedback, run a balance test with multiple simulations.</p>`;
}

function runBalanceTest() {
  renderMatchupPreview();
  const [player, enemy] = getSelectedCreatures();
  const simulations = getSimulationCount();
  const simulator = getSimulator();
  const report = simulator.runManyBattles(player, enemy, simulations);
  latestReportText = report.toText();
  renderBalanceReport(report);
}

function renderBalanceReport(report) {
  const rate = report.playerWinRate();
  const rating = report.rating();
  const ratingClass = rating === "Balanced" ? "good" : (rating.includes("Slightly") ? "warn" : "bad");
  document.getElementById("balanceReport").innerHTML = `
    <div class="rating ${ratingClass}">${escapeHtml(rating)}</div>
    <div class="report-highlight">
      <div class="metric"><span>Win rate</span><strong>${rate.toFixed(1)}%</strong></div>
      <div class="metric"><span>Avg turns</span><strong>${report.averageTurns.toFixed(2)}</strong></div>
      <div class="metric"><span>Avg player HP</span><strong>${report.averagePlayerHp.toFixed(1)}</strong></div>
    </div>
    <div class="hp-bar" aria-label="win rate bar"><div class="hp-fill" style="width: ${Math.min(100, Math.max(0, rate))}%"></div></div>
    <p><strong>Player wins:</strong> ${report.playerWins} / ${report.simulations}</p>
    <p><strong>Enemy wins:</strong> ${report.enemyWins} / ${report.simulations}</p>
    <h4>Design suggestions</h4>
    <ul class="clean">${report.suggestions().map((s) => `<li>${escapeHtml(s)}</li>`).join("")}</ul>`;
}

function runSystemTests() {
  const simulator = getSimulator();
  const tests = [];
  const addTest = (name, fn) => {
    try {
      const passed = fn();
      tests.push({ name, passed, error: "" });
    } catch (error) {
      tests.push({ name, passed: false, error: error.message });
    }
  };

  addTest("Fire attacks Grass should be 2.0", () => simulator.getTypeMultiplier("fire", "grass") === 2.0);
  addTest("Fire attacks Water should be 0.5", () => simulator.getTypeMultiplier("fire", "water") === 0.5);
  addTest("Water attacks Fire should be 2.0", () => simulator.getTypeMultiplier("water", "fire") === 2.0);
  addTest("Damage should never be below 1", () => {
    const weak = new Creature("Weak", "fire", 10, 0, 0, 1, ["Ember"]);
    const tank = new Creature("Tank", "rock", 100, 0, 999, 1, ["Rock Smash"]);
    return simulator.calculateDamage(weak, tank, skills["Ember"]) >= 1;
  });
  addTest("Invalid skill accuracy should throw an error", () => {
    try { new Skill("Broken", "fire", 10, 120); }
    catch { return true; }
    return false;
  });
  addTest("Invalid creature HP should throw an error", () => {
    try { new Creature("Broken", "fire", 0, 10, 10, 10, ["Ember"]); }
    catch { return true; }
    return false;
  });
  addTest("A simple battle should return a valid winner", () => {
    const result = simulator.runOneBattle(creatures["Flarefox"], creatures["Leafling"], false);
    return result.winnerName === "Flarefox" || result.winnerName === "Leafling";
  });

  const passedCount = tests.filter((t) => t.passed).length;
  document.getElementById("testResults").innerHTML = `
    <p><strong>${passedCount}/${tests.length} tests passed.</strong></p>
    <ul class="clean">
      ${tests.map((test) => `<li><span class="${test.passed ? "test-pass" : "test-fail"}">${test.passed ? "PASS" : "FAIL"}</span> ${escapeHtml(test.name)}${test.error ? ` — ${escapeHtml(test.error)}` : ""}</li>`).join("")}
    </ul>`;
}

function runGuidedDemo() {
  document.getElementById("playerSelect").value = "Flarefox";
  document.getElementById("enemySelect").value = "Leafling";
  document.getElementById("simulationCount").value = 30;
  renderMatchupPreview();
  runSingleBattle();
  runBalanceTest();
  runSystemTests();
  document.getElementById("matchupPanel").scrollIntoView({ behavior: "smooth", block: "start" });
}

function downloadLatestReport() {
  if (!latestReportText) {
    alert("No report has been generated yet. Run a single battle or balance test first.");
    return;
  }
  const blob = new Blob([latestReportText], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "spiritforge_balance_report.txt";
  link.click();
  URL.revokeObjectURL(url);
}

function singleBattleText(result) {
  return [
    "=== Single Battle Report ===",
    `Player Creature: ${result.playerName}`,
    `Enemy Creature: ${result.enemyName}`,
    `Winner: ${result.winnerName}`,
    `Battle Length: ${result.turns} turns`,
    `Player Remaining HP: ${result.playerRemainingHp}`,
    `Enemy Remaining HP: ${result.enemyRemainingHp}`,
    "",
    "Battle Log:",
    ...result.battleLog,
  ].join("\n");
}

function multiplierClass(value) {
  if (value > 1) return "multiplier-good";
  if (value < 1) return "multiplier-bad";
  return "multiplier-normal";
}

function escapeHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function escapeAttr(value) {
  return escapeHtml(value).replaceAll("`", "&#096;");
}

function safeAction(fn) {
  try {
    fn();
  } catch (error) {
    alert(error.message);
  }
}

document.getElementById("loadDataBtn").addEventListener("click", () => safeAction(loadData));
document.getElementById("previewBtn").addEventListener("click", () => safeAction(renderMatchupPreview));
document.getElementById("singleBattleBtn").addEventListener("click", () => safeAction(runSingleBattle));
document.getElementById("balanceBtn").addEventListener("click", () => safeAction(runBalanceTest));
document.getElementById("testsBtn").addEventListener("click", () => safeAction(runSystemTests));
document.getElementById("guidedDemoBtn").addEventListener("click", () => safeAction(runGuidedDemo));
document.getElementById("downloadReportBtn").addEventListener("click", () => safeAction(downloadLatestReport));

loadData().then(() => {
  renderTypeChart();
  renderMatchupPreview();
});
