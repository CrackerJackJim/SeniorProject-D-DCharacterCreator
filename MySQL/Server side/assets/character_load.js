// assets/character_load.js
import { apiRequest } from "./api.js";

function getCharacterIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("character_id");
}

// ------------------------------
// LOAD OVERVIEW
// ------------------------------
function loadOverview(char) {
    if (!char) return;

    document.getElementById("ovName").value        = char.Name ?? "";
    document.getElementById("ovPlayerName").value  = char.PlayerName ?? "";
    document.getElementById("ovGender").value      = char.Gender ?? "";

    // These now show names, not IDs
    document.getElementById("ovRace").value        = char.RaceName ?? "";
    document.getElementById("ovClass").value       = char.ClassName ?? "";
    document.getElementById("ovBackground").value  = char.BackgroundName ?? "";

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
}

// ------------------------------
// LOAD COMBAT
// ------------------------------
function loadCombat(c) {
    if (!c) return;

    document.getElementById("combatAC").value      = c.ArmorClass ?? 0;
    document.getElementById("combatHP").value      = c.HP ?? 0;
    document.getElementById("combatTempHP").value  = (c.TempHP ?? c.MaxHP ?? 0);

    document.getElementById("combatInit").value    = c.Initiative ?? 0;

    document.getElementById("combatSpeed").value        = c.Speed ?? "";
    document.getElementById("combatSpeedClimb").value   = c.SpeedClimb ?? "";
    document.getElementById("combatSpeedSwim").value    = c.SpeedSwim ?? "";
    document.getElementById("combatSpeedFly").value     = c.SpeedFly ?? "";

    document.getElementById("combatHitDice").value          = c.HitDiceTotal ?? "";
    document.getElementById("combatHitDiceRemaining").value = c.HitDiceRemaining ?? "";

    document.getElementById("combatPassivePerception").value    = c.PassivePerception ?? 0;
    document.getElementById("combatPassiveInvestigation").value = c.PassiveInvestigation ?? 0;
    document.getElementById("combatPassiveInsight").value       = c.PassiveInsight ?? 0;

    document.getElementById("combatProfBonus").value = c.ProficiencyBonus ?? 0;

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
    if (moneyEl) {
        moneyEl.value = c.Money ?? 0;
    }
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
        const base = map[key];
        document.getElementById(base).value = st[key + "Value"] ?? 0;
    }
}

// ------------------------------
// LOAD SKILLS
// ------------------------------
function loadSkills(sk) {
    console.log("Skills object from backend:", sk);
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
        const base = map[key];
        document.getElementById(base).value = sk[key + "Value"] ?? 0;
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

    document.getElementById("inventoryArmor").value  = inv.Armor ?? "";
    document.getElementById("inventoryWeapons").value= inv.Weapons ?? "";
    document.getElementById("inventoryTools").value  = inv.Tools ?? "";
    document.getElementById("inventoryMisc").value   = inv.MiscItems ?? "";
}

// ------------------------------
// LOAD SPELLS
// ------------------------------
function loadSpells(sp) {
    if (!sp) return;

    document.getElementById("spellAbility").value = sp.SpellcastingAbility ?? "";
    document.getElementById("spellSaveDC").value = sp.SpellSaveDC ?? 0;
    document.getElementById("spellAttackBonus").value = sp.SpellAttackBonus ?? 0;

    document.getElementById("spell1Total").value = sp.L1SlotsTotal ?? 0;
    document.getElementById("spell1Remaining").value = sp.L1SlotsRemaining ?? 0;

    document.getElementById("spell2Total").value = sp.L2SlotsTotal ?? 0;
    document.getElementById("spell2Remaining").value = sp.L2SlotsRemaining ?? 0;

    document.getElementById("spell3Total").value = sp.L3SlotsTotal ?? 0;
    document.getElementById("spell3Remaining").value = sp.L3SlotsRemaining ?? 0;

    document.getElementById("spell4Total").value = sp.L4SlotsTotal ?? 0;
    document.getElementById("spell4Remaining").value = sp.L4SlotsRemaining ?? 0;

    document.getElementById("spell5Total").value = sp.L5SlotsTotal ?? 0;
    document.getElementById("spell5Remaining").value = sp.L5SlotsRemaining ?? 0;

    document.getElementById("spell6Total").value = sp.L6SlotsTotal ?? 0;
    document.getElementById("spell6Remaining").value = sp.L6SlotsRemaining ?? 0;

    document.getElementById("spell7Total").value = sp.L7SlotsTotal ?? 0;
    document.getElementById("spell7Remaining").value = sp.L7SlotsRemaining ?? 0;

    document.getElementById("spell8Total").value = sp.L8SlotsTotal ?? 0;
    document.getElementById("spell8Remaining").value = sp.L8SlotsRemaining ?? 0;

    document.getElementById("spell9Total").value = sp.L9SlotsTotal ?? 0;
    document.getElementById("spell9Remaining").value = sp.L9SlotsRemaining ?? 0;

    document.getElementById("spellKnown").value = sp.KnownSpells ?? "";
    document.getElementById("spellPrepared").value = sp.PreparedSpells ?? "";
}

function loadTraits(t) {
    if (!t) return;

    document.getElementById("featsNotes").value = t.Feats ?? "";
    document.getElementById("raceFeatures").value = t.RaceFeatures ?? "";
    document.getElementById("classFeatures").value = t.ClassFeatures ?? "";
    document.getElementById("backgroundFeatures").value = t.BackgroundFeatures ?? "";
    document.getElementById("proficienciesLanguages").value = t.ProficienciesLanguages ?? "";
    document.getElementById("personalityTraits").value = t.PersonalityTraits ?? "";
    document.getElementById("ideals").value = t.Ideals ?? "";
    document.getElementById("bonds").value = t.Bonds ?? "";
    document.getElementById("flaws").value = t.Flaws ?? "";
    document.getElementById("backstory").value = t.Backstory ?? "";
}

// ------------------------------
// MAIN LOAD FUNCTION
// ------------------------------
export async function loadCharacterSheet() {
    const charId = getCharacterIdFromURL();
    if (!charId) return;

    const sheet = await apiRequest(`/characters/${charId}/sheet`);

    loadOverview(sheet.character);
    loadAbilities(sheet.abilityscores);
    loadCombat(sheet.combatstats);
    loadSavingThrows(sheet.savingthrows);
    loadSkills(sheet.skills);
    loadInventory(sheet.inventory);
    loadSpells(sheet.spells);
    loadTraits(sheet.traits);

    document.getElementById("sheetWrapper").classList.remove("hidden");

    const creator = document.querySelector(".creator-panel");
    if (creator) creator.classList.add("hidden");
}

document.addEventListener("DOMContentLoaded", loadCharacterSheet);