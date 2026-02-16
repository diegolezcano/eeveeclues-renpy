# Eevee Clues – Manual test checklist

Pre-deploy: run at least one full pass per difficulty, then sample Back/edge cases. Automated tests: `renpy . test` or launcher "Run Testcases".

---

## Startup and main menu

| #   | Scenario                | Steps                    | Expected                                                            |
| --- | ----------------------- | ------------------------ | ------------------------------------------------------------------- |
| M1  | Launch game             | Open via Ren'Py launcher | Main menu shows (or direct to pick_difficulty if start skips menu). |
| M2  | Main menu – New Game    | Click "New Game"         | Difficulty screen appears.                                          |
| M3  | Main menu – Preferences | Click "Preferences"      | Preferences screen; return to main menu.                            |
| M4  | Main menu – Quit        | Click "Quit"             | Game exits (or returns to launcher).                                |

---

## Difficulty and new game

| #   | Scenario | Steps                               | Expected                           |
| --- | -------- | ----------------------------------- | ---------------------------------- |
| M5  | Easy     | Pick Easy, proceed to investigation | "Actions left: 6"; clue pool 8–10. |
| M6  | Normal   | Pick Normal, proceed                | "Actions left: 5"; clue pool 5–7.  |
| M7  | Hard     | Pick Hard, proceed                  | "Actions left: 3"; clue pool 3–5.  |

---

## Investigation screen

| #   | Scenario                         | Steps                                                          | Expected                                                                            |
| --- | -------------------------------- | -------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| M8  | Actions left display             | Enter investigation (any difficulty)                           | Header shows "Investigation - Actions left: N" with correct N.                      |
| M9  | Talk – get clue                  | Talk to an Eeveelution (e.g. Vaporeon)                         | Dialogue scene with portrait; clue text; clue added to log; actions left decrement. |
| M10 | Talk – no matching clue         | Talk to same Eeveelution until no character clue left for them | "Nothing new here."; actions left unchanged.                                        |
| M11 | Investigate – get clue          | Investigate a location (e.g. the lake)                         | Dialogue with location image; env/elimination clue; log updated; actions decrement. |
| M12 | Investigate – no matching clue  | Investigate location until no env/elim clue for that stone     | "Nothing new here."; actions unchanged.                                             |
| M13 | Review clues – empty            | Review before any action                                       | "Your clues:" list empty; Back works.                                               |
| M14 | Review clues – with clues       | Gather 1+ clues, then Review                                   | List shows numbered clues; Back returns to investigation.                           |
| M15 | Make a Guess (no out of actions)| Click "Make a Guess" with actions left                         | Accusation evolution screen.                                                        |
| M16 | Out of actions                  | Use all actions (Talk/Investigate until N=0)                   | Message "You've used all your actions..."; then accusation.                         |

---

## Accusation flow

| #   | Scenario                  | Steps                                         | Expected                                                                     |
| --- | ------------------------- | --------------------------------------------- | ---------------------------------------------------------------------------- |
| M17 | Back from evolution       | Accusation evolution → Back                   | Return to investigation; if no actions left, immediately back to accusation.  |
| M17a| Back at 0 actions (edge)  | Use all actions, go to accusation, Back       | Re-enter accusation (no softlock).                                           |
| M18 | Back from stone           | Pick evolution, then accusation stone → Back  | Return to investigation (same as M17).                                       |
| M19 | Full accusation – wrong   | Pick wrong Eeveelution and/or wrong stone     | Result screen: "Wrong guess!" and correct culprit/stone revealed.             |
| M20 | Full accusation – correct | Pick correct Eeveelution and correct stone    | Result screen: "Case solved!" and victory message.                            |

---

## Result and replay

| #   | Scenario          | Steps                            | Expected                                                                            |
| --- | ----------------- | -------------------------------- | ----------------------------------------------------------------------------------- |
| M21 | Play again        | After result, click "Play again" | Jump to new_game: new random case, empty clues, reset actions.                     |
| M22 | Quit after result | After result, click "Quit"       | Return to main menu (or launcher).                                                  |

---

## Portrait / mobile (smoke)

| #   | Scenario              | Steps                                              | Expected                                                                 |
| --- | --------------------- | -------------------------------------------------- | ------------------------------------------------------------------------ |
| M22a| Portrait layout       | Run in portrait window (e.g. 720×1280) or on device | Panels fit; clue log and modals scroll; no horizontal overflow.          |
| M22b| Mobile-sized window   | Resize to narrow width (e.g. 400×800)             | Buttons stack; all screens usable; touch-sized targets on small variant.  |

---

## UI and assets (smoke)

| #   | Scenario                   | Steps                         | Expected                                                     |
| --- | -------------------------- | ----------------------------- | ------------------------------------------------------------ |
| M23 | All screens display        | Visit each screen once        | No missing images or script errors; text readable on panels. |
| M24 | All 8 Eeveelutions in pick | Open "Talk to an Eeveelution" | All 8 listed; each selectable.                               |
| M25 | All 8 locations in pick    | Open "Investigate a Location" | All 8 locations listed; each selectable.                     |
| M26 | All 8 stones in accusation | Reach accusation stone screen | All 8 stones listed; each selectable.                        |

---

## LOCATIONS order (spot-check)

First location in "Investigate a Location" should correspond to Water Stone (e.g. "the lake"). Match order to `STONE_TO_LOCATION` in data.rpy.

---

Note: If the game skips main menu (start → pick_difficulty), M1–M4 use "Launch" = difficulty screen.
