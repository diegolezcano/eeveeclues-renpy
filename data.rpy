# Eevee Clues - data and game logic
# All constants and helper functions in one init python block.

init python:
    import time
    import renpy.store as store

    # Constants and mapping
    EEVEELUTIONS = [
        "Vaporeon", "Jolteon", "Flareon", "Espeon",
        "Umbreon", "Leafeon", "Glaceon", "Sylveon"
    ]
    STONES = [
        "Water Stone", "Thunder Stone", "Fire Stone", "Sun Stone",
        "Moon Stone", "Leaf Stone", "Ice Stone", "Shiny Stone"
    ]
    EVOLUTION_BY_STONE = {
        "Water Stone": "Vaporeon",
        "Thunder Stone": "Jolteon",
        "Fire Stone": "Flareon",
        "Sun Stone": "Espeon",
        "Moon Stone": "Umbreon",
        "Leaf Stone": "Leafeon",
        "Ice Stone": "Glaceon",
        "Shiny Stone": "Sylveon",
    }
    STONE_TO_LOCATION = {
        "Water Stone": "the lake",
        "Thunder Stone": "the power plant",
        "Fire Stone": "the volcano",
        "Sun Stone": "the sunny meadow",
        "Moon Stone": "the city at night",
        "Leaf Stone": "the forest",
        "Ice Stone": "the mountain",
        "Shiny Stone": "the fairy garden",
    }
    LOCATION_TO_STONE = {loc: stone for stone, loc in STONE_TO_LOCATION.items()}

    # Character clue templates (4-6 per evolution)
    CHARACTER_CLUES = {
        "Vaporeon": [
            "I love the water. So calm...",
            "Something shiny by the lake caught my eye.",
            "I didn't need a Fire Stone.",
            "The lake is where I feel most at home.",
            "Water types stick together, you know.",
            "I was near the water earlier.",
        ],
        "Jolteon": [
            "The power plant is so full of energy!",
            "I prefer lightning over flames.",
            "I didn't need a Water Stone.",
            "Electricity was in the air today.",
            "I can't stay away from the power plant.",
            "Sparky and quick—that's me.",
        ],
        "Flareon": [
            "It's always warm near the volcano.",
            "Fire is the best!",
            "I didn't need an Ice Stone.",
            "The volcano path is my favorite walk.",
            "Things got a little heated recently.",
            "I like it where it's warm.",
        ],
        "Espeon": [
            "The sunny meadow is perfect for reading the future.",
            "Sunlight makes me stronger.",
            "I didn't need a Moon Stone.",
            "I was in the meadow when the sun was high.",
            "The sun brings out my power.",
            "Daylight and psychics go together.",
        ],
        "Umbreon": [
            "I like the city when the moon is out.",
            "The night is full of secrets.",
            "I didn't need a Sun Stone.",
            "I prefer the city at night.",
            "The moon was bright last night.",
            "Darkness and the moon—my favorite.",
        ],
        "Leafeon": [
            "The forest is my home.",
            "Plants and leaves everywhere!",
            "I didn't need a Thunder Stone.",
            "I was in the forest all morning.",
            "The trees know everything.",
            "Green and growing—that's the forest.",
        ],
        "Glaceon": [
            "The mountain peak is so cold and clear.",
            "Ice keeps everything pure.",
            "I didn't need a Leaf Stone.",
            "The mountain is where I belong.",
            "Frost and ice don't bother me.",
            "I was up on the mountain earlier.",
        ],
        "Sylveon": [
            "The fairy garden is magical.",
            "Friendship and bonds mean everything.",
            "I didn't need a Fire Stone.",
            "The fairy garden sparkles so nicely.",
            "I love visiting the garden.",
            "Something shiny belongs in the garden.",
        ],
    }

    # Location clue templates (2-3 per stone)
    LOCATION_CLUES = {
        "Water Stone": [
            "Footprints led toward the lake.",
            "Something glinted near the water.",
            "Wet paw prints by the shore.",
        ],
        "Thunder Stone": [
            "Lights flickered at the power plant.",
            "Static in the air...",
            "The plant hummed with energy.",
        ],
        "Fire Stone": [
            "Smoke rose from the volcano path.",
            "It was warm near the lava.",
            "Soot and heat along the trail.",
        ],
        "Sun Stone": [
            "The meadow was extra bright today.",
            "Sunbeams touched the grass.",
            "Warm light lingered in the meadow.",
        ],
        "Moon Stone": [
            "The city was quiet under the moon.",
            "Shadows moved at night.",
            "Moonlight lit the streets.",
        ],
        "Leaf Stone": [
            "Leaves were disturbed in the forest.",
            "The trees whispered.",
            "Fresh trampled leaves on the path.",
        ],
        "Ice Stone": [
            "The mountain path had fresh frost.",
            "Something cold passed by.",
            "Ice crystals on the rocks.",
        ],
        "Shiny Stone": [
            "Sparkles in the fairy garden.",
            "Something precious was here.",
            "A gleam among the flowers.",
        ],
    }

    def _clue_count_for_difficulty(difficulty):
        if difficulty == "easy":
            return (8, 10)
        if difficulty == "hard":
            return (3, 5)
        return (5, 7)  # normal

    def _max_actions_for_difficulty(difficulty):
        if difficulty == "easy":
            return 6
        if difficulty == "hard":
            return 3
        return 5  # normal

    def random_case():
        """Pick one stone and culprit, generate clues. Sets store state."""
        renpy.random.seed(int(time.time() * 1000))
        diff = getattr(store, "difficulty", "normal")
        store.stolen_stone = renpy.random.choice(STONES)
        store.culprit = renpy.random.choice(EEVEELUTIONS)
        store.clues = generate_clues(store.culprit, store.stolen_stone, diff)
        store.clue_index = 0
        store.used_clue_indices = set()
        store.max_actions = _max_actions_for_difficulty(diff)

    def generate_clues(culprit, stolen_stone, difficulty):
        """Build shuffled pool of clue dicts; never contradict guilty pair. Guarantees at least one talk clue for culprit and one location clue for stolen_stone so the player can always discover something."""
        pool = []
        low, high = _clue_count_for_difficulty(difficulty)
        count = renpy.random.randint(low, high)

        # Character clues: one theme hint for culprit, elimination for non-culprits
        culprit_options = []
        for evo in EEVEELUTIONS:
            templates = list(CHARACTER_CLUES.get(evo, []))
            renpy.random.shuffle(templates)
            for t in templates[:4]:  # up to 4 per evolution
                if "didn't need" in t and (stolen_stone in t or any(s in t and EVOLUTION_BY_STONE.get(s) == evo for s in STONES)):
                    continue  # never imply stolen stone or this evolution's canonical stone was not needed
                entry = {"text": t, "category": "character", "evolution": evo}
                pool.append(entry)
                if evo == culprit:
                    culprit_options.append(entry)

        # Environment: one hint for stolen_stone location
        loc_templates = list(LOCATION_CLUES.get(stolen_stone, []))
        renpy.random.shuffle(loc_templates)
        loc_entries = [{"text": t, "category": "environment", "stone": stolen_stone} for t in loc_templates[:3]]
        pool.extend(loc_entries)

        # Elimination: "It was not the X Stone" for stones != stolen_stone
        for stone in STONES:
            if stone == stolen_stone:
                continue
            pool.append({"text": "It was not the " + stone + ".", "category": "elimination", "stone": stone})

        # Guaranteed: at least one clue reachable by talking to culprit, one by investigating stolen_stone location
        guaranteed = []
        if culprit_options:
            guaranteed.append(renpy.random.choice(culprit_options))
        if loc_entries:
            guaranteed.append(renpy.random.choice(loc_entries))
        # Remove guaranteed from pool so we don't duplicate, then take the rest randomly
        for g in guaranteed:
            if g in pool:
                pool.remove(g)
        renpy.random.shuffle(pool)
        need = max(0, count - len(guaranteed))
        return guaranteed + pool[:need]

    def get_clue_for_action(action_type, target):
        """Return a clue matching action_type and target; mark it used. Talk: character+evolution; location: environment/elimination+stone for LOCATION_TO_STONE[target]."""
        clues = getattr(store, "clues", [])
        used = getattr(store, "used_clue_indices", set())
        if action_type == "talk":
            for i, entry in enumerate(clues):
                if i in used:
                    continue
                if entry.get("category") == "character" and entry.get("evolution") == target:
                    store.used_clue_indices = used | {i}
                    return entry.get("text", "Nothing new here.")
        elif action_type == "location":
            stone = LOCATION_TO_STONE.get(target)
            if stone is not None:
                for i, entry in enumerate(clues):
                    if i in used:
                        continue
                    if entry.get("category") in ("environment", "elimination") and entry.get("stone") == stone:
                        store.used_clue_indices = used | {i}
                        return entry.get("text", "Nothing new here.")
        return "Nothing new here."

    # Image name mappings for script/screens (image_prompts.md)
    EVOLUTION_TO_PORTRAIT = {
        "Vaporeon": "portrait_vaporeon", "Jolteon": "portrait_jolteon",
        "Flareon": "portrait_flareon", "Espeon": "portrait_espeon",
        "Umbreon": "portrait_umbreon", "Leafeon": "portrait_leafeon",
        "Glaceon": "portrait_glaceon", "Sylveon": "portrait_sylveon",
    }
    LOCATION_TO_IMAGE = {
        "the lake": "loc_lake", "the power plant": "loc_power_plant",
        "the volcano": "loc_volcano", "the sunny meadow": "loc_meadow",
        "the city at night": "loc_city_night", "the forest": "loc_forest",
        "the mountain": "loc_mountain", "the fairy garden": "loc_fairy_garden",
    }
    STONE_TO_IMAGE = {
        "Water Stone": "icon_water_stone", "Thunder Stone": "icon_thunder_stone",
        "Fire Stone": "icon_fire_stone", "Sun Stone": "icon_sun_stone",
        "Moon Stone": "icon_moon_stone", "Leaf Stone": "icon_leaf_stone",
        "Ice Stone": "icon_ice_stone", "Shiny Stone": "icon_shiny_stone",
    }

    store.EEVEELUTIONS = EEVEELUTIONS
    store.STONES = STONES
    store.LOCATIONS = [STONE_TO_LOCATION[s] for s in STONES]
    store.EVOLUTION_BY_STONE = EVOLUTION_BY_STONE
    store.EVOLUTION_TO_PORTRAIT = EVOLUTION_TO_PORTRAIT
    store.LOCATION_TO_IMAGE = LOCATION_TO_IMAGE
    store.LOCATION_TO_STONE = LOCATION_TO_STONE
    store.STONE_TO_IMAGE = STONE_TO_IMAGE
