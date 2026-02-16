# Eevee Clues – Testing

## Automated tests (required before deploy)

Run from the **project root** (parent of `game/`):

```bash
renpy "path/to/Eevee Clues" test
```

Or from the Ren'Py launcher: **Run Testcases** (refresh the launcher after adding the first test file).

- **Pass criteria:** All testcases must pass. Fix any failure before packaging or release.
- **On failure:** Run with `--print_details` (if supported) or check the console for the assertion and test name.
- **CI:** Use the same command; non-zero exit code indicates test failure.

Test file: `game/test_eevee_clues.rpy` (Data + Logic layer). Names: `Data_*`, `Logic_RandomCase_*`, `Logic_GetClueForAction_*`, `Logic_WinCondition_*`.

## Manual checklist

See [TEST_CHECKLIST.md](TEST_CHECKLIST.md) for scenarios M1–M26 and the Back-at-0-actions edge (M17a). Run at least one full pass per difficulty and the key flows before deploy.

## Portrait and mobile

The game is configured for **portrait** orientation and mobile. Before release:

- Resize the game window to a portrait aspect (e.g. 1080×1920 or 720×1280), or run on an Android emulator/device, and verify: layout fits, clue log and modals scroll, buttons are usable.
- When building an APK (Ren'Py launcher → Distribute), set orientation to portrait in the Android build options so the app locks to portrait on device.
