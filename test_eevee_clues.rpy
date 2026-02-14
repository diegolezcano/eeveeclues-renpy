# Eevee Clues - automated testcases (Data + Logic)
# Run: renpy . test  or launcher "Run Testcases"
# Bounds: easy (6, 8-10), normal (5, 5-7), hard (3, 3-5)

# -----------------------------------------------------------------------------
# Data layer
# -----------------------------------------------------------------------------

testcase Data_Constants_EEVEELUTIONSLength8:
    description "EEVEELUTIONS has exactly 8 entries."
    assert eval(len(store.EEVEELUTIONS) == 8)

testcase Data_Constants_STONESLength8:
    description "STONES has exactly 8 entries."
    assert eval(len(store.STONES) == 8)

testcase Data_EvolutionByStone_OneEntryPerStone:
    description "EVOLUTION_BY_STONE has one entry per stone."
    assert eval(len(store.EVOLUTION_BY_STONE) == len(store.STONES))

testcase Data_EvolutionByStone_ValuesInEEVEELUTIONS:
    description "Every EVOLUTION_BY_STONE value is in EEVEELUTIONS."
    $ _all_valid = all(store.EVOLUTION_BY_STONE[s] in store.EEVEELUTIONS for s in store.STONES)
    assert eval(_all_valid)

# -----------------------------------------------------------------------------
# Logic layer - random_case
# -----------------------------------------------------------------------------

testcase Logic_RandomCase_ValidCulpritAndStone:
    description "After random_case(), culprit is in EEVEELUTIONS and stolen_stone is in STONES."
    parameter difficulty = ["easy", "normal", "hard"]
    $ store.difficulty = difficulty
    $ random_case()
    assert eval(store.culprit in store.EEVEELUTIONS)
    assert eval(store.stolen_stone in store.STONES)

testcase Logic_RandomCase_ClueCountInRange:
    description "After random_case(), clue count is within difficulty bounds (easy 8-10, normal 5-7, hard 3-5)."
    parameter difficulty = ["easy", "normal", "hard"]
    $ store.difficulty = difficulty
    $ random_case()
    $ _bounds = {"easy": (8, 10), "normal": (5, 7), "hard": (3, 5)}
    $ _low, _high = _bounds[difficulty]
    assert eval(_low <= len(store.clues) <= _high)

testcase Logic_RandomCase_MaxActionsMatchesDifficulty:
    description "After random_case(), max_actions is 6 for easy, 5 for normal, 3 for hard."
    parameter difficulty = ["easy", "normal", "hard"]
    $ store.difficulty = difficulty
    $ random_case()
    $ _expected = {"easy": 6, "normal": 5, "hard": 3}
    assert eval(store.max_actions == _expected[difficulty])

testcase Logic_RandomCase_UsedClueIndicesEmpty:
    description "Right after random_case(), used_clue_indices is empty."
    $ store.difficulty = "normal"
    $ random_case()
    assert eval(len(store.used_clue_indices) == 0)

# -----------------------------------------------------------------------------
# Logic layer - get_clue_for_action
# -----------------------------------------------------------------------------

testcase Logic_GetClueForAction_Talk_ReturnsClueWhenAvailable:
    description "get_clue_for_action('talk', culprit) returns a clue when one exists for that evolution."
    $ store.difficulty = "normal"
    $ random_case()
    $ _txt = get_clue_for_action("talk", store.culprit)
    assert eval(_txt != "Nothing new here.")

testcase Logic_GetClueForAction_Talk_ReturnsNothingWhenExhausted:
    description "After exhausting character clues for one evolution, same target returns Nothing new here."
    $ store.difficulty = "easy"
    $ random_case()
    $ _evo = store.EEVEELUTIONS[0]
    $ _ = get_clue_for_action("talk", _evo)
    $ _again = get_clue_for_action("talk", _evo)
    $ _more = get_clue_for_action("talk", _evo)
    $ _final = get_clue_for_action("talk", _evo)
    $ _yet = get_clue_for_action("talk", _evo)
    assert eval(_yet == "Nothing new here.")

testcase Logic_GetClueForAction_Location_ReturnsClueWhenAvailable:
    description "When pool has env/elim clue for stolen_stone location, get_clue_for_action returns it."
    $ store.difficulty = "normal"
    $ random_case()
    $ _loc = store.LOCATIONS[store.STONES.index(store.stolen_stone)]
    $ _txt = get_clue_for_action("location", _loc)
    $ _has_loc_clue = any(e.get("category") in ("environment", "elimination") and e.get("stone") == store.stolen_stone for e in store.clues)
    assert eval((not _has_loc_clue) or (_txt != "Nothing new here."))

testcase Logic_GetClueForAction_InvalidTarget_Talk_ReturnsNothing:
    description "get_clue_for_action('talk', invalid_evolution) returns Nothing new here. and does not crash."
    $ store.difficulty = "normal"
    $ random_case()
    $ _txt = get_clue_for_action("talk", "UnknownEvo")
    assert eval(_txt == "Nothing new here.")

testcase Logic_GetClueForAction_InvalidTarget_Location_ReturnsNothing:
    description "get_clue_for_action('location', unknown_location) returns Nothing new here. and does not crash."
    $ store.difficulty = "normal"
    $ random_case()
    $ _txt = get_clue_for_action("location", "unknown location")
    assert eval(_txt == "Nothing new here.")

# -----------------------------------------------------------------------------
# Logic layer - win condition
# -----------------------------------------------------------------------------

testcase Logic_WinCondition_CorrectPair_True:
    description "When guess_evolution and guess_stone match culprit and stolen_stone, win condition is True."
    $ store.culprit = store.EEVEELUTIONS[0]
    $ store.stolen_stone = store.STONES[0]
    $ store.guess_evolution = store.EEVEELUTIONS[0]
    $ store.guess_stone = store.STONES[0]
    $ _win = (store.guess_evolution == store.culprit and store.guess_stone == store.stolen_stone)
    assert eval(_win)

testcase Logic_WinCondition_WrongEvolution_False:
    description "When guess_evolution is wrong, win condition is False."
    $ store.culprit = store.EEVEELUTIONS[0]
    $ store.stolen_stone = store.STONES[0]
    $ store.guess_evolution = store.EEVEELUTIONS[1]
    $ store.guess_stone = store.STONES[0]
    $ _win = (store.guess_evolution == store.culprit and store.guess_stone == store.stolen_stone)
    assert eval(not _win)

testcase Logic_WinCondition_WrongStone_False:
    description "When guess_stone is wrong, win condition is False."
    $ store.culprit = store.EEVEELUTIONS[0]
    $ store.stolen_stone = store.STONES[0]
    $ store.guess_evolution = store.EEVEELUTIONS[0]
    $ store.guess_stone = store.STONES[1]
    $ _win = (store.guess_evolution == store.culprit and store.guess_stone == store.stolen_stone)
    assert eval(not _win)

# -----------------------------------------------------------------------------
# Logic layer - clue log (gathered_clues)
# -----------------------------------------------------------------------------

testcase Logic_ClueLog_EmptyAfterReset:
    description "After random_case() and reset, gathered_clues is empty."
    $ store.difficulty = "normal"
    $ random_case()
    $ store.gathered_clues = []
    $ store.used_actions = 0
    assert eval(len(store.gathered_clues) == 0)

testcase Logic_ClueLog_TalkCulpritAppendsOne:
    description "Talk to culprit returns a clue; simulating script appends one and uses one action."
    $ store.difficulty = "normal"
    $ random_case()
    $ store.gathered_clues = []
    $ store.used_actions = 0
    $ _txt = get_clue_for_action("talk", store.culprit)
    $ (_txt != "Nothing new here.") and (store.gathered_clues.append(_txt) or (store.__setattr__("used_actions", store.used_actions + 1)))
    assert eval(_txt != "Nothing new here.")
    assert eval(len(store.gathered_clues) == 1)
    assert eval(store.used_actions == 1)

testcase Logic_ClueLog_LocationCrimeAppendsOne:
    description "Investigate crime location returns a clue; simulating script appends one and uses one action."
    $ store.difficulty = "normal"
    $ random_case()
    $ store.gathered_clues = []
    $ store.used_actions = 0
    $ _loc = store.LOCATIONS[store.STONES.index(store.stolen_stone)]
    $ _txt = get_clue_for_action("location", _loc)
    $ (_txt != "Nothing new here.") and (store.gathered_clues.append(_txt) or (store.__setattr__("used_actions", store.used_actions + 1)))
    assert eval(_txt != "Nothing new here.")
    assert eval(len(store.gathered_clues) == 1)
    assert eval(store.used_actions == 1)

testcase Logic_ClueLog_GuaranteedTwoEntries:
    description "After talk-to-culprit and investigate-crime-location, gathered_clues has at least 2 entries."
    $ store.difficulty = "normal"
    $ random_case()
    $ store.gathered_clues = []
    $ store.used_actions = 0
    $ _t1 = get_clue_for_action("talk", store.culprit)
    $ (_t1 != "Nothing new here.") and (store.gathered_clues.append(_t1) or (store.__setattr__("used_actions", store.used_actions + 1)))
    $ _loc = store.LOCATIONS[store.STONES.index(store.stolen_stone)]
    $ _t2 = get_clue_for_action("location", _loc)
    $ (_t2 != "Nothing new here.") and (store.gathered_clues.append(_t2) or (store.__setattr__("used_actions", store.used_actions + 1)))
    assert eval(len(store.gathered_clues) >= 2)
    assert eval(store.used_actions >= 2)

testcase Logic_ClueLog_NothingNewNotAppended:
    description "Wrong target returns Nothing new here.; no append, used_actions stays 0."
    $ store.difficulty = "normal"
    $ random_case()
    $ store.gathered_clues = []
    $ store.used_actions = 0
    $ _txt = get_clue_for_action("talk", "UnknownEvo")
    assert eval(_txt == "Nothing new here.")
    assert eval(len(store.gathered_clues) == 0)
    assert eval(store.used_actions == 0)

# -----------------------------------------------------------------------------
# UI - How to play content in store
# -----------------------------------------------------------------------------

testcase UI_HowToPlayContent_InStore_NonEmpty:
    description "how_to_play_content is in store and contains expected sections for How to play screen."
    assert eval(hasattr(store, "how_to_play_content"))
    assert eval(isinstance(store.how_to_play_content, str))
    assert eval(len(store.how_to_play_content) > 0)
    assert eval("Your goal" in store.how_to_play_content)
    assert eval("Making your guess" in store.how_to_play_content)
