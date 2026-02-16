# Eevee Clues - screens
# Main menu, investigation board, picks, accusation, review clues.

init:
    style game_panel_text:
        color gui.game_panel_text
        outlines [(2, "#000000")]
        font gui.interface_text_font
    style game_action_button:
        background Solid(gui.game_button_bg_idle)
        hover_background Solid(gui.game_button_bg_hover)
        padding (24, 12)
        xalign 0.5
    style game_action_button_text:
        color gui.game_panel_text
        hover_color "#ffffff"
        size 20
    style game_back_button:
        background Solid(gui.game_button_back_bg)
        hover_background Solid(gui.game_button_bg_idle)
        padding (20, 10)
    style game_back_button_text:
        color gui.game_panel_text
        hover_color "#ffffff"
        size 18
    style game_guess_button:
        background Solid("#d4af37")
        hover_background Solid("#e8c547")
        padding (24, 12)
        xminimum 220
        xalign 0.5
    style game_guess_button_text:
        color "#1a1a1a"
        hover_color "#000000"
        size 20
screen investigation():
    add Solid("#000000")
    add Transform("board_bg", fit="contain", xalign=0.5, yalign=0.5)
    $ panel_w = min(900, int(config.screen_width * 0.95))
    $ panel_h = min(620, int(config.screen_height * 0.85))
    $ clue_h = min(200, int(config.screen_height * 0.28))
    $ clue_inner_w = panel_w - 84
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        xsize panel_w
        ysize panel_h
        padding (30, 30)
        vbox:
            spacing 18
            $ actions_left = max_actions - used_actions
            text "Investigation - Actions left: [actions_left]" style "game_panel_text" size 26
            hbox:
                spacing 30
                vbox:
                    spacing 8
                    text "Eevee and Eeveelutions:" style "game_panel_text" size 20
                    text "Eevee, " + ", ".join(store.EEVEELUTIONS) style "game_panel_text" size 16
                vbox:
                    spacing 5
                    text "Stones: (?)" style "game_panel_text" size 20
            null height 8
            text "Clue log:" style "game_panel_text" size 20
            frame:
                background Solid("#0f0f0fcc")
                padding (12, 12)
                xsize clue_inner_w
                ysize clue_h
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xsize clue_inner_w - 24
                    ysize clue_h - 24
                    vbox:
                        xsize clue_inner_w - 24
                        for i, c in enumerate(gathered_clues):
                            $ _num = i + 1
                            text "[_num]. [c]" style "game_panel_text" size 16 color "#ffffff" xmaximum clue_inner_w - 24
            null height 15
            vbox:
                spacing 12
                xalign 0.5
                if used_actions < max_actions:
                    textbutton "Talk to an Eeveelution" action Call("action_talk") style "game_action_button"
                    textbutton "Investigate a Location" action Call("action_location") style "game_action_button"
                textbutton "Make a Guess" action Return("guess") style "game_guess_button"

screen pick_difficulty():
    modal True
    add Solid(gui.game_modal_overlay)
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        vbox:
            align (0.5, 0.5)
            spacing 20
            text "Choose difficulty" style "game_panel_text" size 30 xalign 0.5
            text "Easy: 6 actions, 8-10 clues\nNormal: 5 actions, 5-7 clues\nHard: 3 actions, 3-5 clues" style "game_panel_text" size 18 xalign 0.5
            null height 10
            textbutton "How to play" action Show("how_to_play") style "game_action_button" xalign 0.5
            textbutton "Easy" action [SetVariable("difficulty", "easy"), Return()] style "game_action_button" xalign 0.5
            textbutton "Normal" action [SetVariable("difficulty", "normal"), Return()] style "game_action_button" xalign 0.5
            textbutton "Hard" action [SetVariable("difficulty", "hard"), Return()] style "game_action_button" xalign 0.5

screen how_to_play():
    modal True
    add Solid(gui.game_modal_overlay)
    $ ht_w = min(720, int(config.screen_width * 0.95))
    $ ht_h = min(560, int(config.screen_height * 0.85))
    $ vp_h = min(400, int(config.screen_height * 0.5))
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        xsize ht_w
        ysize ht_h
        vbox:
            spacing 15
            text "How to play" style "game_panel_text" size 26 xalign 0.5
            null height 5
            frame:
                background Solid("#0f0f0fcc")
                padding (12, 12)
                xsize ht_w - 60
                ysize vp_h
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xsize ht_w - 84
                    ysize vp_h - 24
                    vbox:
                        xsize ht_w - 84
                        text "[store.how_to_play_content]" size 18 text_align 0.0 color "#ffffff" xmaximum ht_w - 84
            null height 10
            textbutton "Back" action Hide("how_to_play") style "game_back_button" xalign 0.5

screen main_menu():
    tag menu
    add Solid("#000000")
    add Transform("menu_bg", fit="contain", xalign=0.5, yalign=0.5)
    vbox:
        align (0.5, 0.5)
        spacing 24
        text "Eevee Clues" style "game_panel_text" size 44 xalign 0.5
        text "The Evolution Stone Mystery" style "game_panel_text" size 22 xalign 0.5
        null height 24
        textbutton "New Game" action Start() style "game_action_button" xalign 0.5
        textbutton "Preferences" action ShowMenu("preferences") style "game_action_button" xalign 0.5
        textbutton "Quit" action Quit(confirm=False) style "game_action_button" xalign 0.5

screen game_menu():
    tag menu
    add Solid("#000000")
    add Transform("menu_bg", fit="contain", xalign=0.5, yalign=0.5)
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        vbox:
            align (0.5, 0.5)
            spacing 18
            text "Menu" style "game_panel_text" size 30 xalign 0.5
            null height 8
            textbutton "Return" action Return() style "game_action_button" xalign 0.5
            textbutton "Preferences" action ShowMenu("preferences") style "game_action_button" xalign 0.5
            textbutton "Save Game" action ShowMenu("save") style "game_action_button" xalign 0.5
            textbutton "Load Game" action ShowMenu("load") style "game_action_button" xalign 0.5
            textbutton "Main Menu" action MainMenu() style "game_action_button" xalign 0.5
            textbutton "Quit" action Quit(confirm=True) style "game_back_button" xalign 0.5

screen pick_evolution_talk():
    modal True
    add Solid(gui.game_modal_overlay)
    $ evo_w = min(900, int(config.screen_width * 0.95))
    frame:
        background Solid("#000000")
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        xsize evo_w
        vbox:
            align (0.5, 0.5)
            spacing 18
            text "Talk to which Eeveelution?" style "game_panel_text" size 26 xalign 0.5
            null height 8
            grid 2 4:
                spacing 16
                xalign 0.5
                for evo in store.EEVEELUTIONS:
                    vbox:
                        spacing 8
                        xalign 0.5
                        add Transform(store.EVOLUTION_TO_PORTRAIT.get(evo, "portrait_eevee"), size=(80, 80)) xalign 0.5
                        textbutton evo action Return(evo) style "game_action_button" xminimum 120
            null height 12
            textbutton "Back" action Return(None) style "game_back_button" xalign 0.5

screen pick_location():
    modal True
    add Solid(gui.game_modal_overlay)
    $ loc_w = min(900, int(config.screen_width * 0.95))
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        xsize loc_w
        vbox:
            align (0.5, 0.5)
            spacing 18
            text "Investigate which location?" style "game_panel_text" size 26 xalign 0.5
            null height 8
            grid 2 4:
                spacing 16
                xalign 0.5
                for loc in store.LOCATIONS:
                    $ _stone = store.LOCATION_TO_STONE.get(loc)
                    vbox:
                        spacing 8
                        xalign 0.5
                        add Transform(store.STONE_TO_IMAGE.get(_stone, "icon_unknown"), size=(80, 80)) xalign 0.5
                        textbutton loc action Return(loc) style "game_action_button" xminimum 120
            null height 12
            textbutton "Back" action Return(None) style "game_back_button" xalign 0.5

screen review_clues():
    modal True
    add Solid(gui.game_modal_overlay)
    $ rv_w = min(640, int(config.screen_width * 0.95))
    $ rv_h = min(480, int(config.screen_height * 0.7))
    $ rv_vp_h = min(320, int(config.screen_height * 0.45))
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        xsize rv_w
        ysize rv_h
        vbox:
            spacing 15
            text "Your clues:" style "game_panel_text" size 26 xalign 0.5
            null height 5
            frame:
                background Solid("#0f0f0fcc")
                padding (12, 12)
                xsize rv_w - 80
                ysize rv_vp_h
                viewport:
                    scrollbars "vertical"
                    mousewheel True
                    draggable True
                    xsize rv_w - 104
                    ysize rv_vp_h - 24
                    vbox:
                        xsize rv_w - 104
                        for i, c in enumerate(gathered_clues):
                            $ _num = i + 1
                            text "[_num]. [c]" style "game_panel_text" size 18 color "#ffffff" xmaximum rv_w - 104
            null height 10
            textbutton "Back" action Return() style "game_back_button" xalign 0.5

screen accusation_evolution():
    modal True
    add Solid(gui.game_modal_overlay)
    $ acc_w = min(560, int(config.screen_width * 0.95))
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        xsize acc_w
        vbox:
            align (0.5, 0.5)
            spacing 15
            text "Who stole the stone? (Choose one Eeveelution)" style "game_panel_text" size 24 xalign 0.5
            null height 5
            viewport:
                scrollbars "vertical"
                mousewheel True
                draggable True
                xsize acc_w - 80
                ysize min(400, int(config.screen_height * 0.5))
                vbox:
                    spacing 10
                    for evo in store.EEVEELUTIONS:
                        hbox:
                            spacing 12
                            xalign 0.5
                            add Transform(store.EVOLUTION_TO_PORTRAIT.get(evo, "portrait_eevee"), size=(64, 64))
                            textbutton evo action Return(evo) style "game_action_button"
            null height 10
            textbutton "Back" action Return(None) style "game_back_button" xalign 0.5

screen accusation_stone():
    modal True
    add Solid(gui.game_modal_overlay)
    $ stone_w = min(560, int(config.screen_width * 0.95))
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 0.5
        padding (40, 40)
        xsize stone_w
        vbox:
            align (0.5, 0.5)
            spacing 15
            text "Which stone was stolen?" style "game_panel_text" size 24 xalign 0.5
            null height 5
            for stone in store.STONES:
                hbox:
                    spacing 12
                    xalign 0.5
                    add Transform(store.STONE_TO_IMAGE.get(stone, "icon_unknown"), size=(64, 64))
                    textbutton stone action Return(stone) style "game_action_button"
            null height 10
            textbutton "Back" action Return(None) style "game_back_button" xalign 0.5

screen result_screen():
    modal True
    add Solid(gui.game_modal_overlay)
    $ res_w = min(560, int(config.screen_width * 0.95))
    frame:
        background Solid(gui.game_panel_bg)
        xalign 0.5
        yalign 1.0
        xsize res_w
        padding (28, 28)
        vbox:
            spacing 14
            text "[result_title]" style "game_panel_text" size 28 xalign 0.5
            null height 4
            text "[result_message]" style "game_panel_text" size 18 xalign 0.5 text_align 0.5
            null height 18
            hbox:
                spacing 20
                xalign 0.5
                textbutton "Play again" action Return("again") style "game_action_button"
                textbutton "Quit" action Return("quit") style "game_back_button"

screen say(who, what):
    window:
        yalign 1.0
        xsize config.screen_width
        background Solid(gui.game_panel_bg)
        padding (48, 32)
        vbox:
            if who:
                text who style "game_panel_text" size gui.name_text_size id "who"
                null height 8
            text what style "game_panel_text" size gui.text_size id "what"
