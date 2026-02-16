# Eevee Clues - main flow
# Default variables and labels: start, new_game, investigation, accusation, result.

image dialogue_bg = "images/dialogue_bg.png"

default difficulty = "normal"
default culprit = None
default stolen_stone = None
default clues = []
default clue_index = 0
default gathered_clues = []
default used_actions = 0
default max_actions = 5
default guess_evolution = None
default guess_stone = None
default accusation_step = 0  # 0 = pick evolution, 1 = pick stone
default result_title = ""
default result_message = ""

default how_to_play_content = """Your goal

Find which Eeveelution stole which Evolution Stone.

Getting clues

Use "Talk to an Eeveelution" and "Investigate a Location". When you get a real clue (not "Nothing new here."), it's added to your Clue log.

Using the Clue log

Open "Review Clues" to read everything you've learned. Combine what characters say with what you found at locations.

Solving the mystery

Character clues often mention a place or say they didn't need a certain stone. Location clues tell you about the stone at that place. One stone was stolen, and one Eeveelution took it—any Eeveelution might have taken any stone. Figure out who took which stone.

Making your guess

When ready, choose "Make a Guess", then pick the Eeveelution and the stone. Get both right to win."""

label start:
    call screen pick_difficulty
    jump new_game

label new_game:
    $ random_case()
    $ gathered_clues = []
    $ used_actions = 0
    play music "audio/mainSong.mp3" loop fadein 1.0
    jump investigation_loop

label investigation_loop:
    scene board_bg
    if used_actions >= max_actions:
        "You've used all your actions. Time to make a guess!"
        jump accusation_phase
    call screen investigation
    if _return == "guess":
        jump accusation_phase
    jump investigation_loop

label action_talk:
    call screen pick_evolution_talk
    $ _chosen = _return
    if _chosen and used_actions < max_actions:
        $ txt = get_clue_for_action("talk", _chosen)
        scene expression Transform("dialogue_bg", size=(config.screen_width, config.screen_height))
        $ _portrait = store.EVOLUTION_TO_PORTRAIT.get(_chosen, "portrait_eevee")
        show expression Transform(_portrait, fit="contain", ysize=int(config.screen_height * 0.45), xalign=0.5, yalign=0.5)
        with Dissolve(0.15)
        "" "[txt]"
        if txt == "Nothing new here.":
            $ renpy.play("audio/sfx_talk_wrong.ogg", channel="sound")
        elif _chosen == culprit:
            $ renpy.play("audio/sfx_talk_culprit.ogg", channel="sound")
        if txt != "Nothing new here.":
            $ gathered_clues.append(txt)
            $ used_actions += 1
    return

label action_location:
    call screen pick_location
    $ _loc = _return
    if _loc and used_actions < max_actions:
        $ txt = get_clue_for_action("location", _loc)
        $ _stone = store.LOCATION_TO_STONE.get(_loc)
        scene expression Transform("dialogue_bg", size=(config.screen_width, config.screen_height))
        show expression store.LOCATION_TO_IMAGE.get(_loc, "loc_lake")
        show expression Transform(store.STONE_TO_IMAGE.get(_stone, "icon_unknown"), size=(128, 128)) at right
        with Dissolve(0.15)
        "" "[txt]"
        if _stone == stolen_stone and txt != "Nothing new here.":
            $ renpy.play("audio/sfx_talk_culprit.ogg", channel="sound")
        if txt != "Nothing new here.":
            $ gathered_clues.append(txt)
            $ used_actions += 1
    return

label action_review:
    call screen review_clues
    return

label accusation_phase:
    stop music
    call screen accusation_evolution
    $ guess_evolution = _return
    if guess_evolution is None:
        jump investigation_loop
    call screen accusation_stone
    $ guess_stone = _return
    if guess_stone is None:
        jump investigation_loop
    jump show_result

label show_result:
    if guess_evolution == culprit and guess_stone == stolen_stone:
        scene result_victory
        $ result_title = "Case solved!"
        $ result_message = "You were right! {color=#e0a366}" + culprit + "{/color} took the {color=#e0a366}" + stolen_stone + "{/color}!"
    else:
        scene result_defeat
        $ result_title = "Wrong guess!"
        $ result_message = "It was actually {color=#e0a366}" + culprit + "{/color} with the {color=#e0a366}" + stolen_stone + "{/color}!"
    call screen result_screen
    if _return == "again":
        jump new_game
    return
