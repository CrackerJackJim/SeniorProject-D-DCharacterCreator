// assets/character_save.js
import { apiRequest } from "./api.js";

// ------------------------------
// HELPERS
// ------------------------------
function getText(id) {
    const el = document.getElementById(id);
    return el ? el.value.trim() : "";
}

function getNumber(id) {
    const el = document.getElementById(id);
    if (!el) return 0;

    const raw = el.value;
    if (raw === "" || raw === null || raw === undefined) return 0;

    const num = parseInt(raw, 10);
    return isNaN(num) ? 0 : num;
}

function getCheckbox(id) {
    const el = document.getElementById(id);
    return el ? el.checked : false;
}

function getCharacterIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get("character_id");
}

// ------------------------------
// MAIN SAVE FUNCTION
// ------------------------------
async function saveCharacter() {
    if (document.activeElement) {
        document.activeElement.blur();
    }

    const payload = {
        overview: {
            name: getText("ovName"),
            player_name: getText("ovPlayerName"),
            gender: getText("ovGender"),
            alignment: getNumber("ovAlignment"),
            level: getNumber("ovLevel"),
            xp: getNumber("ovXP"),
        },

        abilities: {
            strength: getNumber("abStr"),
            dexterity: getNumber("abDex"),
            constitution: getNumber("abCon"),
            intelligence: getNumber("abInt"),
            wisdom: getNumber("abWis"),
            charisma: getNumber("abCha"),
        },

        combat: {
            ac: getNumber("combatAC"),
            hp: getNumber("combatHP"),
            temp_hp: getNumber("combatTempHP"),
            initiative: getNumber("combatInit"),

            max_hp: getNumber("combatMaxHP"),

            speed: getNumber("combatSpeed"),
            speed_climb: getNumber("combatSpeedClimb"),
            speed_swim: getNumber("combatSpeedSwim"),
            speed_fly: getNumber("combatSpeedFly"),

            hit_dice_total: getNumber("combatHitDice"),
            hit_dice_remaining: getNumber("combatHitDiceRemaining"),

            passive_perception: getNumber("combatPassivePerception"),
            passive_investigation: getNumber("combatPassiveInvestigation"),
            passive_insight: getNumber("combatPassiveInsight"),

            death_success_1: getCheckbox("deathSuccess1"),
            death_success_2: getCheckbox("deathSuccess2"),
            death_success_3: getCheckbox("deathSuccess3"),

            death_fail_1: getCheckbox("deathFail1"),
            death_fail_2: getCheckbox("deathFail2"),
            death_fail_3: getCheckbox("deathFail3"),

            proficiency_bonus: getNumber("combatProfBonus"),

            resistances: getText("combatResistances"),
            immunities: getText("combatImmunities"),
            vulnerabilities: getText("combatVulnerabilities"),
            conditions: getText("combatConditions"),

            money: getNumber("combatMoney"),
        },

        saving_throws: {
            str: { proficient: getCheckbox("saveStrProf"), value: getNumber("saveStr") },
            dex: { proficient: getCheckbox("saveDexProf"), value: getNumber("saveDex") },
            con: { proficient: getCheckbox("saveConProf"), value: getNumber("saveCon") },
            int: { proficient: getCheckbox("saveIntProf"), value: getNumber("saveInt") },
            wis: { proficient: getCheckbox("saveWisProf"), value: getNumber("saveWis") },
            cha: { proficient: getCheckbox("saveChaProf"), value: getNumber("saveCha") },
        },

        skills: {
            acrobatics: getNumber("skillAcrobatics"),
            animal_handling: getNumber("skillAnimal"),
            arcana: getNumber("skillArcana"),
            athletics: getNumber("skillAthletics"),
            deception: getNumber("skillDeception"),
            history: getNumber("skillHistory"),
            insight: getNumber("skillInsight"),
            intimidation: getNumber("skillIntimidation"),
            investigation: getNumber("skillInvestigation"),
            medicine: getNumber("skillMedicine"),
            nature: getNumber("skillNature"),
            perception: getNumber("skillPerception"),
            performance: getNumber("skillPerformance"),
            persuasion: getNumber("skillPersuasion"),
            religion: getNumber("skillReligion"),
            sleight_of_hand: getNumber("skillSleight"),
            stealth: getNumber("skillStealth"),
            survival: getNumber("skillSurvival"),
        },

        // ------------------------------
        // INVENTORY
        // ------------------------------
        inventory: {
            cp: getNumber("invCP"),
            sp: getNumber("invSP"),
            ep: getNumber("invEP"),
            gp: getNumber("invGP"),
            pp: getNumber("invPP"),

            armor: getText("invArmor"),
            weapons: getText("invWeapons"),
            tools: getText("invTools"),
            misc_items: getText("invMisc"),
        },

        // ------------------------------
        // SPELLS
        // ------------------------------
        spells: {
            ability: getText("spellAbility"),
            save_dc: getNumber("spellSaveDC"),
            attack_bonus: getNumber("spellAttackBonus"),

            l1_total: getNumber("spell1Total"),
            l1_remaining: getNumber("spell1Remaining"),
            l2_total: getNumber("spell2Total"),
            l2_remaining: getNumber("spell2Remaining"),
            l3_total: getNumber("spell3Total"),
            l3_remaining: getNumber("spell3Remaining"),
            l4_total: getNumber("spell4Total"),
            l4_remaining: getNumber("spell4Remaining"),
            l5_total: getNumber("spell5Total"),
            l5_remaining: getNumber("spell5Remaining"),
            l6_total: getNumber("spell6Total"),
            l6_remaining: getNumber("spell6Remaining"),
            l7_total: getNumber("spell7Total"),
            l7_remaining: getNumber("spell7Remaining"),
            l8_total: getNumber("spell8Total"),
            l8_remaining: getNumber("spell8Remaining"),
            l9_total: getNumber("spell9Total"),
            l9_remaining: getNumber("spell9Remaining"),

            known_spells: getText("spellKnown"),
            prepared_spells: getText("spellPrepared")
        },

        traits: {
            feats: getText("featsNotes"),
            race_features: getText("raceFeatures"),
            class_features: getText("classFeatures"),
            background_features: getText("backgroundFeatures"),
            proficiencies_languages: getText("proficienciesLanguages"),
            personality_traits: getText("personalityTraits"),
            ideals: getText("ideals"),
            bonds: getText("bonds"),
            flaws: getText("flaws"),
            backstory: getText("backstory")
        }
    };

    console.log("Saving character payload:", payload);

    try {
        const charId = getCharacterIdFromURL();
        const result = await apiRequest(`/characters/${charId}/update`, "POST", payload);

        console.log("Character saved:", result);
        alert("Character saved successfully!");

    } catch (err) {
        console.error("Error saving character:", err);
        alert("Failed to save character.");
    }
}

// ------------------------------
// ATTACH SAVE BUTTON
// ------------------------------
document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("saveCharacterBtn");
    if (!btn) {
        console.warn("saveCharacterBtn not found in DOM.");
        return;
    }
    btn.addEventListener("click", saveCharacter);
});