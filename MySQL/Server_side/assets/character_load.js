// assets/character_load.js
import { apiRequest } from "./api.js";
import { saveCharacter } from "./character_save.js";

function getCharacterIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("character_id");
}

// ------------------------------
// FIGHTER HELPERS
// ------------------------------
function getFighterProficiency(level) {
    if (level >= 17) return 6;
    if (level >= 13) return 5;
    if (level >= 9)  return 4;
    if (level >= 5)  return 3;
    return 2;
}

function getFighterActionSurgeUses(level) {
    if (level >= 17) return 2;
    if (level >= 2)  return 1;
    return 0;
}

function getFighterExtraAttacks(level) {
    if (level >= 20) return 4;
    if (level >= 11) return 3;
    if (level >= 5)  return 2;
    return 1;
}

function getFighterIndomitableUses(level) {
    if (level >= 17) return 3;
    if (level >= 13) return 2;
    if (level >= 9)  return 1;
    return 0;
}

// ------------------------------
// SKILL AUTO-CALCULATION (GLOBAL)
// ------------------------------
const SKILL_ABILITY_MAP = {
    Acrobatics: "Dex",
    Animal: "Wis",
    Arcana: "Int",
    Athletics: "Str",
    Deception: "Cha",
    History: "Int",
    Insight: "Wis",
    Intimidation: "Cha",
    Investigation: "Int",
    Medicine: "Wis",
    Nature: "Int",
    Perception: "Wis",
    Performance: "Cha",
    Persuasion: "Cha",
    Religion: "Int",
    Sleight: "Dex",
    Stealth: "Dex",
    Survival: "Wis"
};

function getAbilityMod(abilityId) {
    const el = document.getElementById(`ab${abilityId}`);
    const score = el ? parseInt(el.value) || 10 : 10;
    return Math.floor((score - 10) / 2);
}

function updateSkill(skillId) {
    const ability = SKILL_ABILITY_MAP[skillId];
    const mod = getAbilityMod(ability);

    const profEl = document.getElementById(`prof${skillId}`);
    const expEl  = document.getElementById(`exp${skillId}`);

    const prof = profEl ? profEl.checked : false;
    const exp  = expEl ? expEl.checked : false;

    const profBonus = parseInt(document.getElementById("combatProfBonus")?.value) || 0;

    let total = mod;
    if (prof) total += profBonus;
    if (exp)  total += profBonus;

    const skillEl = document.getElementById(`skill${skillId}`);
    if (skillEl) skillEl.value = total;
}

function updateAllSkills() {
    Object.keys(SKILL_ABILITY_MAP).forEach(updateSkill);
}

// ------------------------------
// ABILITY MOD DISPLAY
// ------------------------------
function updateAbilityMods() {
    ["Str","Dex","Con","Int","Wis","Cha"].forEach(ab => {
        const mod = getAbilityMod(ab);
        const modEl = document.getElementById(`ab${ab}Mod`);
        if (modEl) {
            modEl.textContent = (mod >= 0 ? `+${mod}` : `${mod}`);
        }
    });
}

// ------------------------------
// CON → HP ADJUSTMENT
// ------------------------------
function updateHPFromConChange() {
    const level = window.CURRENT_CHARACTER_LEVEL || 1;
    const newConMod = getAbilityMod("Con");
    const oldConMod = window.LAST_CON_MOD ?? newConMod;
    const delta = newConMod - oldConMod;

    if (delta === 0) return;

    const maxHpEl = document.getElementById("combatMaxHP");
    const hpEl    = document.getElementById("combatHP");
    if (!maxHpEl || !hpEl) return;

    const currentMax = parseInt(maxHpEl.value) || 0;
    const currentHP  = parseInt(hpEl.value) || 0;

    const change = delta * level;

    maxHpEl.value = currentMax + change;
    hpEl.value    = currentHP + change;

    window.LAST_CON_MOD = newConMod;
}

// ------------------------------
// LOAD OVERVIEW
// ------------------------------
function loadOverview(char) {
    if (!char) return;

    document.getElementById("ovName").value        = char.Name ?? "";
    document.getElementById("ovPlayerName").value  = char.PlayerName ?? "";
    document.getElementById("ovGender").value      = char.Gender ?? "";

    document.getElementById("ovRace").value        = char.RaceName ?? "";
    document.getElementById("ovClass").value       = char.ClassName ?? "";
    document.getElementById("ovBackground").value  = char.BackgroundName ?? "";

    const ovSubclass = document.getElementById("ovSubclass");
    if (ovSubclass) {
        ovSubclass.value = char.SubclassName ?? "No subclass selected";
    }

    document.getElementById("ovLevel").value       = char.Level ?? 1;
    document.getElementById("ovAlignment").value   = char.AlignmentID ?? "";
    document.getElementById("ovXP").value          = char.Experience ?? 0;
}

// ------------------------------
// LOAD ABILITIES
// ------------------------------
function loadAbilities(ab) {
    if (!ab) return;

    document.getElementById("abStr").value = ab.StrScore ?? 10;
    document.getElementById("abDex").value = ab.DexScore ?? 10;
    document.getElementById("abCon").value = ab.ConScore ?? 10;
    document.getElementById("abInt").value = ab.IntScore ?? 10;
    document.getElementById("abWis").value = ab.WisScore ?? 10;
    document.getElementById("abCha").value = ab.ChaScore ?? 10;

    updateAbilityMods();
    window.LAST_CON_MOD = getAbilityMod("Con");
}

// ------------------------------
// LOAD COMBAT
// ------------------------------
function loadCombat(c) {
    if (!c) return;

    window.CURRENT_HIT_DICE_TYPE = c.HitDiceType;

    document.getElementById("combatAC").value      = c.ArmorClass ?? 10;
    document.getElementById("combatHP").value      = c.CurrentHP ?? 0;
    document.getElementById("combatMaxHP").value   = c.MaxHP ?? 0;
    document.getElementById("combatTempHP").value  = c.TempHP ?? 0;
    document.getElementById("combatInit").value    = c.Initiative ?? 0;
    document.getElementById("combatSpeed").value   = c.Speed ?? 30;

    const speedClimbEl = document.getElementById("combatSpeedClimb");
    if (speedClimbEl) speedClimbEl.value = c.SpeedClimb ?? 0;

    const speedSwimEl = document.getElementById("combatSpeedSwim");
    if (speedSwimEl) speedSwimEl.value = c.SpeedSwim ?? 0;

    const speedFlyEl = document.getElementById("combatSpeedFly");
    if (speedFlyEl) speedFlyEl.value = c.SpeedFly ?? 0;

    document.getElementById("combatHitDice").value          = c.HitDiceTotal ?? 1;
    document.getElementById("combatHitDiceRemaining").value = c.HitDiceRemaining ?? 1;

    let profBonus = c.ProficiencyBonus ?? 0;
    if (window.CURRENT_CLASS_NAME === "Fighter") {
        profBonus = getFighterProficiency(window.CURRENT_CHARACTER_LEVEL);
    }
    document.getElementById("combatProfBonus").value = profBonus;

    const passivePerceptionEl = document.getElementById("combatPassivePerception");
    if (passivePerceptionEl) passivePerceptionEl.value = c.PassivePerception ?? 0;

    const passiveInvestigationEl = document.getElementById("combatPassiveInvestigation");
    if (passiveInvestigationEl) passiveInvestigationEl.value = c.PassiveInvestigation ?? 0;

    const passiveInsightEl = document.getElementById("combatPassiveInsight");
    if (passiveInsightEl) passiveInsightEl.value = c.PassiveInsight ?? 0;

    document.getElementById("deathSuccess1").checked = !!c.DeathSuccess1;
    document.getElementById("deathSuccess2").checked = !!c.DeathSuccess2;
    document.getElementById("deathSuccess3").checked = !!c.DeathSuccess3;

    document.getElementById("deathFail1").checked = !!c.DeathFail1;
    document.getElementById("deathFail2").checked = !!c.DeathFail2;
    document.getElementById("deathFail3").checked = !!c.DeathFail3;

    document.getElementById("combatResistances").value     = c.Resistances ?? "";
    document.getElementById("combatImmunities").value      = c.Immunities ?? "";
    document.getElementById("combatVulnerabilities").value = c.Vulnerabilities ?? "";
    document.getElementById("combatConditions").value      = c.Conditions ?? "";

    const moneyEl = document.getElementById("combatMoney");
    if (moneyEl) moneyEl.value = c.Money ?? 0;

    if (window.CURRENT_CLASS_NAME === "Fighter") {
        const asEl  = document.getElementById("combatActionSurge");
        const eaEl  = document.getElementById("combatExtraAttack");
        const indEl = document.getElementById("combatIndomitable");

        if (asEl)  asEl.value  = getFighterActionSurgeUses(window.CURRENT_CHARACTER_LEVEL);
        if (eaEl)  eaEl.value  = getFighterExtraAttacks(window.CURRENT_CHARACTER_LEVEL);
        if (indEl) indEl.value = getFighterIndomitableUses(window.CURRENT_CHARACTER_LEVEL);
    }

    updateCritRange();
}

// ------------------------------
// LOAD SAVING THROWS
// ------------------------------
function loadSavingThrows(st) {
    if (!st) return;

    const map = {
        Str: "saveStr",
        Dex: "saveDex",
        Con: "saveCon",
        Int: "saveInt",
        Wis: "saveWis",
        Cha: "saveCha",
    };

    for (const key in map) {
        document.getElementById(map[key]).value = st[key + "Value"] ?? 0;
    }
}

// ------------------------------
// LOAD SKILLS
// ------------------------------
function loadSkills(sk) {
    if (!sk) return;

    const map = {
        Acrobatics:        "skillAcrobatics",
        AnimalHandling:    "skillAnimal",
        Arcana:            "skillArcana",
        Athletics:         "skillAthletics",
        Deception:         "skillDeception",
        History:           "skillHistory",
        Insight:           "skillInsight",
        Intimidation:      "skillIntimidation",
        Investigation:     "skillInvestigation",
        Medicine:          "skillMedicine",
        Nature:            "skillNature",
        Perception:        "skillPerception",
        Performance:       "skillPerformance",
        Persuasion:        "skillPersuasion",
        Religion:          "skillReligion",
        SleightOfHand:     "skillSleight",
        Stealth:           "skillStealth",
        Survival:          "skillSurvival"
    };

    for (const key in map) {
        document.getElementById(map[key]).value = sk[key + "Value"] ?? 0;
    }
}

// ------------------------------
// LOAD INVENTORY
// ------------------------------
function loadInventory(inv) {
    if (!inv) return;

    document.getElementById("invCP").value = inv.CP ?? 0;
    document.getElementById("invSP").value = inv.SP ?? 0;
    document.getElementById("invEP").value = inv.EP ?? 0;
    document.getElementById("invGP").value = inv.GP ?? 0;
    document.getElementById("invPP").value = inv.PP ?? 0;

    document.getElementById("invArmor").value   = inv.Armor ?? "";
    document.getElementById("invWeapons").value = inv.Weapons ?? "";
    document.getElementById("invTools").value   = inv.Tools ?? "";
    document.getElementById("invMisc").value    = inv.MiscItems ?? "";
}

// ------------------------------
// LOAD SPELLS
// ------------------------------
function loadSpells(sp) {
    if (!sp) return;

    document.getElementById("spellAbility").value      = sp.SpellcastingAbility ?? "";
    document.getElementById("spellSaveDC").value       = sp.SpellSaveDC ?? 0;
    document.getElementById("spellAttackBonus").value  = sp.SpellAttackBonus ?? 0;

    document.getElementById("spell1Total").value       = sp.L1SlotsTotal ?? 0;
    document.getElementById("spell1Remaining").value   = sp.L1SlotsRemaining ?? 0;

    document.getElementById("spell2Total").value       = sp.L2SlotsTotal ?? 0;
    document.getElementById("spell2Remaining").value   = sp.L2SlotsRemaining ?? 0;

    document.getElementById("spell3Total").value       = sp.L3SlotsTotal ?? 0;
    document.getElementById("spell3Remaining").value   = sp.L3SlotsRemaining ?? 0;

    document.getElementById("spell4Total").value       = sp.L4SlotsTotal ?? 0;
    document.getElementById("spell4Remaining").value   = sp.L4SlotsRemaining ?? 0;

    document.getElementById("spell5Total").value       = sp.L5SlotsTotal ?? 0;
    document.getElementById("spell5Remaining").value   = sp.L5SlotsRemaining ?? 0;

    document.getElementById("spell6Total").value       = sp.L6SlotsTotal ?? 0;
    document.getElementById("spell6Remaining").value   = sp.L6SlotsRemaining ?? 0;

    document.getElementById("spell7Total").value       = sp.L7SlotsTotal ?? 0;
    document.getElementById("spell7Remaining").value   = sp.L7SlotsRemaining ?? 0;

    document.getElementById("spell8Total").value       = sp.L8SlotsTotal ?? 0;
    document.getElementById("spell8Remaining").value   = sp.L8SlotsRemaining ?? 0;

    document.getElementById("spell9Total").value       = sp.L9SlotsTotal ?? 0;
    document.getElementById("spell9Remaining").value   = sp.L9SlotsRemaining ?? 0;

    document.getElementById("spellKnown").value        = sp.KnownSpells ?? "";
    document.getElementById("spellPrepared").value     = sp.PreparedSpells ?? "";
}

// ------------------------------
// CHAMPION FEATURE PROGRESSION (HELP PANEL ONLY)
// ------------------------------
function getChampionFeaturesByLevel() {
    return [
        {
            level: 3,
            title: "Improved Critical",
            text: "Your weapon attacks score a critical hit on a roll of 19 or 20."
        },
        {
            level: 7,
            title: "Remarkable Athlete",
            text: "Add half your proficiency bonus (rounded up) to STR/DEX/CON checks that don’t already use proficiency. Also increases running long jump distance by your STR modifier."
        },
        {
            level: 10,
            title: "Additional Fighting Style",
            text: "Choose a second option from the Fighting Style class feature (not one you already have)."
        },
        {
            level: 15,
            title: "Superior Critical",
            text: "Your weapon attacks score a critical hit on a roll of 18–20."
        },
        {
            level: 18,
            title: "Survivor",
            text: "At the start of each of your turns, regain hit points equal to 5 + your CON modifier if you have no more than half your hit points left. You don’t gain this benefit if you have 0 HP."
        }
    ];
}

// ------------------------------
// LOAD TRAITS
// ------------------------------
function loadTraits(t) {
    if (!t) return;

    document.getElementById("featsNotes").value             = t.Feats ?? "";
    document.getElementById("raceFeatures").value           = t.RaceFeatures ?? "";
    document.getElementById("classFeatures").value          = t.ClassFeatures ?? "";
    document.getElementById("backgroundFeatures").value     = t.BackgroundFeatures ?? "";
    document.getElementById("proficienciesLanguages").value = t.ProficienciesLanguages ?? "";
    document.getElementById("personalityTraits").value      = t.PersonalityTraits ?? "";
    document.getElementById("ideals").value                 = t.Ideals ?? "";
    document.getElementById("bonds").value                  = t.Bonds ?? "";
    document.getElementById("flaws").value                  = t.Flaws ?? "";
    document.getElementById("backstory").value              = t.Backstory ?? "";
}

// ------------------------------
// MAIN LOAD FUNCTION
// ------------------------------
export async function loadCharacterSheet() {
    const charId = getCharacterIdFromURL();
    if (!charId) return;

    window.CURRENT_CHARACTER_ID = charId;

    const res = await fetch(`http://127.0.0.1:8000/api/characters/${charId}/sheet`, {
        method: "GET",
        cache: "no-store"
    });
    const sheet = await res.json();

    let currentSubclassObj = null;

    if (Array.isArray(sheet.available_subclasses) && sheet.available_subclasses.length > 0) {
        if (sheet.character.SubclassID) {
            currentSubclassObj = sheet.available_subclasses.find(
                s => s.SubclassID === sheet.character.SubclassID
            ) || null;

            sheet.character.SubclassName = currentSubclassObj ? currentSubclassObj.Name : null;
        }
    }

    window.CURRENT_SUBCLASS_NAME   = sheet.character.SubclassName || null;
    window.CURRENT_SUBCLASS_OBJECT = currentSubclassObj;
    window.CURRENT_CHARACTER_LEVEL = sheet.character.Level ?? 1;
    window.CURRENT_CLASS_NAME      = sheet.character.ClassName || null;

    loadOverview(sheet.character);
    loadAbilities(sheet.abilityscores);
    loadCombat(sheet.combatstats);
    loadSavingThrows(sheet.savingthrows);
    loadSkills(sheet.skills);
    loadInventory(sheet.inventory);
    loadSpells(sheet.spells);
    loadTraits(sheet.traits);

    updateAbilityMods();
    updateAllSkills();

    document.getElementById("sheetWrapper").classList.remove("hidden");
    const creator = document.querySelector(".creator-panel");
    if (creator) creator.classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", loadCharacterSheet);

// ------------------------------
// SUBCLASS HELP PANEL
// ------------------------------
let subclassHelpPanel = null;
let isSubclassHelpOpen = false;

document.addEventListener("DOMContentLoaded", () => {
    subclassHelpPanel = document.getElementById("subclassHelpPanel");
});

function getSubclassDescriptionHTML(sc) {
    if (!sc || !sc.Name) return "";

    if (sc.Name === "Champion") {
        const features = getChampionFeaturesByLevel();

        let listHtml = "";
        features.forEach(f => {
            listHtml += `<li><strong>Level ${f.level}: ${f.title}</strong> — ${f.text}</li>`;
        });

        return `
            <h2>Champion</h2>
            <p>A straightforward, durable fighter focused on consistent damage and survivability.</p>
            <ul>${listHtml}</ul>
        `;
    }

    return `
        <h2>${sc.Name}</h2>
        <p>${sc.Description ?? "This subclass grants unique features and abilities as you level up."}</p>
    `;
}

function openSubclassHelpPanel(sc, fromOverview = false) {
    if (!subclassHelpPanel) return;

    const html = getSubclassDescriptionHTML(sc);
    subclassHelpPanel.innerHTML = html;

    subclassHelpPanel.style.right = "-600px";

    if (fromOverview) {
        subclassHelpPanel.style.right = "50px";
    } else {
        subclassHelpPanel.style.right = "500px";
    }

    isSubclassHelpOpen = true;
}

function closeSubclassHelpPanel() {
    if (!subclassHelpPanel) return;
    subclassHelpPanel.style.right = "-600px";
    isSubclassHelpOpen = false;
}

// ------------------------------
// SUBCLASS MENU LOGIC
// ------------------------------
window.SELECTED_SUBCLASS = null;

function loadSubclassOptions(subclasses) {
    const container = document.getElementById("subclassContent");
    if (!container) return;

    container.innerHTML = "";

    if (!subclasses || subclasses.length === 0) {
        container.innerHTML = "<p>No subclasses available.</p>";
        return;
    }

    subclasses.forEach(sc => {
        const id = sc.SubclassID ?? sc.subclassid ?? sc.SubclassId ?? sc.id;

        const div = document.createElement("div");
        div.className = "subclass-option";
        div.dataset.id = id;
        div.innerHTML = `<strong>${sc.Name}</strong><br>${sc.Description ?? ""}`;

        div.addEventListener("click", () => {
            document.querySelectorAll(".subclass-option")
                .forEach(opt => opt.classList.remove("subclass-selected"));

            div.classList.add("subclass-selected");
            window.SELECTED_SUBCLASS = id;

            openSubclassHelpPanel(sc, false);
        });

        container.appendChild(div);
    });
}

function updateCritRange() {
    let range = 20;

    if (window.CURRENT_SUBCLASS_NAME === "Champion") {
        const lvl = window.CURRENT_CHARACTER_LEVEL || 1;

        if (lvl >= 15) {
            range = 18;
        } else if (lvl >= 3) {
            range = 19;
        }
    }

    window.CRIT_RANGE = range;

    const critEl = document.getElementById("combatCritRange");
    if (critEl) {
        critEl.value = `${range}–20`;
    }
}

// ------------------------------
// SKILL PROF / EXPERT WIRING
// ------------------------------
function wireSkill(skillId) {
    const prof = document.getElementById(`prof${skillId}`);
    const exp  = document.getElementById(`exp${skillId}`);

    if (!prof || !exp) return;

    prof.addEventListener("change", () => {
        if (!prof.checked) exp.checked = false;
        updateSkill(skillId);
    });

    exp.addEventListener("change", () => {
        updateSkill(skillId);
    });
}

[
    "Acrobatics",
    "Animal",
    "Arcana",
    "Athletics",
    "Deception",
    "History",
    "Insight",
    "Intimidation",
    "Investigation",
    "Medicine",
    "Nature",
    "Perception",
    "Performance",
    "Persuasion",
    "Religion",
    "Sleight",
    "Stealth",
    "Survival"
].forEach(wireSkill);

function openSubclassPanel() {
    closeSubclassHelpPanel();
    document.getElementById("subclassOverlay").style.display = "block";
    document.getElementById("subclassPanel").style.display = "block";
}

function closeSubclassPanel() {
    document.getElementById("subclassOverlay").style.display = "none";
    document.getElementById("subclassPanel").style.display = "none";
    closeSubclassHelpPanel();
}

document.getElementById("subclassPanel").addEventListener("click", (event) => {
    event.stopPropagation();
});

document.getElementById("confirmSubclassBtn").addEventListener("click", async (event) => {
    event.preventDefault();
    event.stopPropagation();

    if (!window.SELECTED_SUBCLASS) {
        alert("You must choose a subclass.");
        return;
    }

    try {
        await apiRequest(`/characters/${window.CURRENT_CHARACTER_ID}/subclass/select`, "POST", {
            subclass_id: window.SELECTED_SUBCLASS
        });
        updateCritRange();
        closeSubclassPanel();
        location.reload();

    } catch (err) {
        console.error("Error saving subclass:", err);
        alert("Error saving subclass.");
    }
});

// ------------------------------
// LEVEL UP LOGIC
// ------------------------------
function populateHpDropdown(hitDiceType) {
    const hpSelect = document.getElementById("manualHpInput");
    if (!hpSelect) return;

    hpSelect.innerHTML = "";

    for (let i = 1; i <= hitDiceType; i++) {
        const opt = document.createElement("option");
        opt.value = i;
        opt.textContent = i;
        hpSelect.appendChild(opt);
    }
}

function openLevelUpMenu() {
    populateHpDropdown(window.CURRENT_HIT_DICE_TYPE);

    document.getElementById("levelUpOverlay").style.display = "block";
    document.getElementById("levelUpMenu").style.display = "flex";
}

function closeLevelUpMenu() {
    document.getElementById("levelUpOverlay").style.display = "none";
    document.getElementById("levelUpMenu").style.display = "none";
}

// ---------------------------------------------------------
// DOMContentLoaded WIRING
// ---------------------------------------------------------
document.addEventListener("DOMContentLoaded", () => {

    // LEVEL UP BUTTONS
    const levelUpBtn = document.getElementById("levelUpBtn");
    const confirmLevelUpBtn = document.getElementById("confirmLevelUpBtn");
    const cancelLevelUpBtn = document.getElementById("cancelLevelUpBtn");

    if (levelUpBtn) {
        levelUpBtn.addEventListener("click", () => {
            if (isSubclassHelpOpen) closeSubclassHelpPanel();
            openLevelUpMenu();
        });
    }

    if (confirmLevelUpBtn) {
        confirmLevelUpBtn.addEventListener("click", async () => {
            const roll = parseInt(document.getElementById("manualHpInput").value);

            // 1. Save current sheet FIRST (this preserves ability scores)
            await saveCharacter();

            // 2. Apply level-up
            const result = await apiRequest(`/characters/${window.CURRENT_CHARACTER_ID}/level_up`, "POST", {
                manual_roll: roll
            });

            // 3. Update HP locally
            const hpEl    = document.getElementById("combatHP");
            const maxHpEl = document.getElementById("combatMaxHP");

            if (hpEl)    hpEl.value    = result.new_current_hp;
            if (maxHpEl) maxHpEl.value = result.new_max_hp;

            updateCritRange();
            closeLevelUpMenu();

            // 4. Reload AFTER saving + level-up
            location.reload();
        });
    }

    if (cancelLevelUpBtn) {
        cancelLevelUpBtn.addEventListener("click", closeLevelUpMenu);
    }

    // SUBCLASS CHOOSE BUTTON
    const chooseBtn = document.getElementById("chooseSubclassBtn");
    if (chooseBtn) {
        chooseBtn.addEventListener("click", async () => {
            if (isSubclassHelpOpen) closeSubclassHelpPanel();

            const charId = window.CURRENT_CHARACTER_ID;
            if (!charId) {
                alert("No character loaded.");
                return;
            }

            try {
                const sheet = await apiRequest(`/characters/${charId}/sheet`, "GET");
                loadSubclassOptions(sheet.available_subclasses);
                window.SELECTED_SUBCLASS = null;
                openSubclassPanel();
            } catch (err) {
                console.error("Failed to load subclass list:", err);
                alert("Could not load subclass list.");
            }
        });
    }

    // BACK BUTTON IN SUBCLASS MODAL
    const backBtn = document.getElementById("backSubclassBtn");
    if (backBtn) {
        backBtn.addEventListener("click", () => {
            closeSubclassHelpPanel();
            closeSubclassPanel();
        });
    }

    // CLICKABLE SUBCLASS FIELD IN OVERVIEW
    const ovSubclass = document.getElementById("ovSubclass");
    if (ovSubclass) {
        ovSubclass.style.cursor = "pointer";
        ovSubclass.addEventListener("click", () => {
            if (window.CURRENT_SUBCLASS_OBJECT) {
                openSubclassHelpPanel(window.CURRENT_SUBCLASS_OBJECT, true);
            }
        });
    }

    // AUTO‑CLOSE HELP PANEL ON TAB SWITCH
    document.querySelectorAll(".sheet-tab").forEach(tab => {
        tab.addEventListener("click", () => {
            if (isSubclassHelpOpen) closeSubclassHelpPanel();
        });
    });

    // AUTO‑CLOSE WHEN OPENING SETTINGS
    const settingsButton = document.getElementById("settingsButton");
    if (settingsButton) {
        settingsButton.addEventListener("click", () => {
            if (isSubclassHelpOpen) closeSubclassHelpPanel();
        });
    }

    // AUTO‑CLOSE WHEN OPENING FONT MENU
    const openFontMenuBtn = document.getElementById("openFontMenuBtn");
    if (openFontMenuBtn) {
        openFontMenuBtn.addEventListener("click", () => {
            if (isSubclassHelpOpen) closeSubclassHelpPanel();
        });
    }

    ["Str","Dex","Con","Int","Wis","Cha"].forEach(ab => {
        const el = document.getElementById(`ab${ab}`);
        if (el) {
            el.addEventListener("input", () => {

                // Clamp between 1 and 30
                let val = parseInt(el.value) || 1;
                if (val > 30) val = 30;
                if (val < 1)  val = 1;
                el.value = val;

                updateAbilityMods();
                updateAllSkills();

                if (ab === "Con") {
                    updateHPFromConChange();
                }
            });
        }
    });

});