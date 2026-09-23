# ZEPHON Ukrainian audit: status and resume guide

Last updated 23.09.2026. Game version 1.3.21. Pass 1 is paused after wave 3.

## Where things stand

- Pass 1 has 18 of 70 batches done: B01 to B15 and the catch-up batches R01 to R03 are scanned, triaged, applied, validated and committed.
- 52 batches are left, B16 to B67. At 6 batches per wave that is 9 more waves (wave 4 to wave 12).
- The next wave is wave 4: B16, B17, B18, B19, B20, B21, all Diplomacy.xml.
- Batches B16 to B67 were last rebuilt on 16.09.2026, after the 1.3.21 sync, and are still current. Wave 3 only changed entries inside B10 to B15.
- Every applied fix is synced to the live mod folder and to the local Workshop copy. The Steam Workshop item has not been re-published.
- The address to the player is only partly converted. It is «ви» in the Actions.xml flavor texts, B07 to B09 and the first half of Diplomacy.xml (B10 to B15), but the rest of Diplomacy, Quests, Factions and the later flavor files still say «ти» until their waves run. Re-publishing before the audit ends ships that mix.

## Wave plan for the rest of pass 1

- Wave 4: B16 to B21 (Diplomacy.xml)
- Wave 5: B22 to B27 (end of Diplomacy.xml, Effects.xml, Factions.xml, start of Features.xml)
- Wave 6: B28 to B33 (Features.xml, GUI.xml, Items.xml, Messages.xml, Modifiers.xml, Notifications.xml, Objectives.xml, Overlay.xml, start of Quests.xml)
- Wave 7: B34 to B39 (Quests.xml)
- Wave 8: B40 to B45 (Quests.xml)
- Wave 9: B46 to B51 (end of Quests.xml, Regions.xml, start of Settings.xml)
- Wave 10: B52 to B57 (Settings.xml, Tips.xml, Titles.xml, Traits.xml)
- Wave 11: B58 to B63 (Traits.xml, Units.xml, Upgrades.xml)
- Wave 12: B64 to B67 (Upgrades.xml, Weapons.xml, WorldParameters.xml)

`pass1/LEDGER.md` has the exact file list and size of every batch.

## What was applied (1,289 fix operations)

- Script sweep: 648 raw hits in `pass1/sweep.json`, of which 140 confirmed fixes are in `pass1/findings/SWEEP.json`. They were applied as part of wave 1.
- Wave 1: B01 to B06 (AI.xml, Actions.xml, Attributes.xml, start of Branches.xml). 288 fixes including the sweep. Full list in `pass1/wave1.md`.
- Bleed rename: `pass1/findings/BLEED.json` (44 entries, Теча to Кровотеча) and `pass1/findings/BLEED2.json` (11 entries, Bleedwalker and the Russian spelling Течь).
- Wave 2: R01 to R03 (catch-up «ви» and participle pass over the Actions.xml flavor texts that wave 1 had already scanned) and B07 to B09 (Branches.xml, Buildings.xml, Cities.xml, Colors.xml, Controls.xml, Credits.xml, first Diplomacy.xml lines). 116 fixes, 54 of them «ви» rewrites. Full list in `pass1/wave2.md`.
- PlatinumScion city names: `pass1/findings/PSCITIES.json`, 21 names retranslated because the Ukrainian came from an old English list.
- Wave 3: B10 to B15 (Diplomacy.xml, from the general hints through the first HonorableAristocrat lines). 806 fixes, 739 of them «ви» rewrites, 25 high. 13 of the agents' wordings were changed in triage and none were dropped. Impersonal «ти» that means anyone, not the player, stays («ніколи не знаєш», «на все підеш»). Full list in `pass1/wave3.md`.
- Puns: `pass1/findings/PUNS.json`, 3 Emulated Mind lines where English or Latin letters were glued into Ukrainian words («заDOOMили», «DOOM.ати», «>pagu>»).

## Decisions VK made

Every future wave follows these. They are also written into `BRIEF.md` and into the canon of the zephon-localization-update skill.

- Address the player and the reader with lowercase «ви» everywhere: quest narration, characters in quests, Diplomacy leader lines (rude leaders too), faction and flavor texts. «ти» stays only when someone speaks to a person who is not the player.
- Bleed is «Кровотеча» everywhere. Bleedwalker is «Кровотечехід», plural «кровотечеходи».
- Replace every Russian-style active participle in «-ючий» (палаючий, сяючий, вражаючий, існуючий). Flying is «летючий».
- Terms: Reavers «Спустошувачі»; the Voice «Голос», genitive «Голосу»; Vorodai «Вородай»; Dreameater «Сноїд», in prose «сноїдець»; ЗЕФОН genitive «ЗЕФОНа»; tiles in the genitive plural «клітинок»; spelling «проєкт».
- Keep as they are: the capitalised «НЕ-» prefix, and names written out in words where Ukrainian needs a case that a `<string/>` reference can't give.
- No English puns inside Ukrainian words (23.09.2026). The Emulated Mind keeps her glitch style (dots, dashes, caps, digits for letters), but every word must read as Ukrainian. «заDOOMили», «DOOM.ати» and «>pagu>» were rewritten in `pass1/findings/PUNS.json`. Latin copied from the English stays: Swedish words, homo sapiens, brand and code names.
- Workflow: Opus agents for every scan, 6 batches per wave, stop after every wave for VK's approval before applying, a progress line every 30 seconds while agents run.

## Folder map

- `BRIEF.md`: what every scanning agent reads. The three jobs (defects, «ви», participles), what not to report, the term canon and the output format.
- `scripts/build_batches.py`: builds batch files and their ledger lines. `--start N` rebuilds from batch N on, `--exclude FILE` skips the entry ids listed in FILE, `--only FILE` builds only from those ids, `--prefix R` names catch-up batches.
- `scripts/sweep.py`: mechanical whole-corpus checks (Russian letters, russianisms, leftover Latin, quotes, apostrophes, spacing, numbers, capitals, term variants). Writes `<pass>/sweep.json`.
- `scripts/show_findings.py`: triage view of a batch's small fixes. Flags a `find` text that doesn't occur exactly once.
- `scripts/show_diff.py`: triage view of full-entry «ви» rewrites as word diffs. Flags changed markup, quote balance and big length changes.
- `scripts/merge_approved.py`: combines findings files with `decisions.json` into `<pass>/<wave>.json` plus a readable `<wave>.md`.
- `scripts/apply_fixes.py`: writes a fixes file into the Ukrainian XML, keeping the BOM and each file's line endings. `--dry-run` writes nothing.
- `pass1/LEDGER.md`: one line per batch. `[ ]` not scanned, `[~]` scanned and triaged but not applied, `[x]` applied.
- `pass1/decisions.json`: triage decisions per findings file, plus VK's decision log under `_decisions_by_VK`.
- `pass1/batches/`: batch text files. B16 to B67 are waiting to be scanned.
- `pass1/findings/`: one JSON per scanned batch, plus SWEEP, BLEED, BLEED2, PSCITIES and PUNS.
- `pass1/scanned_ids.txt`: every entry id already scanned (B01 to B15). `pass1/catchup_ids.txt`: the ids R01 to R03 covered.
- `pass1/wave1.json` to `pass1/wave3.json`, each with its `.md`: exactly what each wave applied.

## How to run the next wave

Run everything from the repo root: `Desktop/MyCode/zephone`, or `Desktop/MyCoding/zephone` on machines where the folder has that name. In Git Bash set `PYTHONIOENCODING=utf-8` first. Below, `<repo>` means the absolute Windows path of the repo root.

1. **Start clean.** `git pull`, then `git status` should show nothing to commit.

2. **Check the batches are current.** Batch files are snapshots of the Ukrainian text. They stay valid as long as nothing touched `ModData/Data/Core/Languages/Ukrainian` since the last audit commit. If something did (a game patch sync, a manual fix), rebuild the remaining batches first:

    ```
    python audit/scripts/build_batches.py pass1 --start 16 --exclude audit/pass1/scanned_ids.txt
    ```

    This rewrites B16 onward and their ledger lines. B01 to B15 stay as they are. New entries from a patch in already-scanned files land in the rebuilt batches, because their ids aren't in `scanned_ids.txt`.

3. **Launch the wave.** One background agent per batch, type `general-purpose`, model `opus`, all six in one message. The prompt for B16 (swap the id for the others):

    ```
    Scan batch B16 of the ZEPHON Ukrainian translation audit. Do all three jobs from the brief.

    1. Read <repo>\audit\BRIEF.md and follow it exactly.
    2. Read the batch: <repo>\audit\pass1\batches\B16.txt
    3. Write your findings to <repo>\audit\pass1\findings\B16.json

    Reply with exactly one line, as the brief says.
    ```

4. **Post progress every 30 seconds.** Start a persistent Monitor with this loop and relay each line to VK:

    ```
    D="<repo>/audit/pass1/findings"
    start=$(date +%s)
    while true; do
      sleep 30
      finished=""; left=""
      for b in B16 B17 B18 B19 B20 B21; do
        if [ -f "$D/$b.json" ]; then finished="$finished $b"; else left="$left $b"; fi
      done
      mins=$(( ($(date +%s) - start) / 60 ))
      if [ -z "$left" ]; then echo "wave 4: all 6 batches done after ${mins} min"; exit 0; fi
      echo "wave 4: done:${finished:- none}, still running:${left}, ${mins} min"
    done
    ```

    The loop only sees findings files. A failed agent still shows as "still running", so watch the agent notifications as well and tell VK when one fails.

5. **If an agent fails** (for example "Can't reach the API server"), resume it with SendMessage to its agent id rather than starting over:

    ```
    Your run stopped on a network error before you wrote the findings file; please continue batch B16 now. Finish the task exactly as your original instructions and BRIEF.md describe, write the findings file, and reply with the one-line summary.
    ```

    An agent stopped by a session limit can't be resumed this way, because it counts as cancelled. Launch its batch again from scratch.

6. **Triage each batch as it lands.**

    ```
    python audit/scripts/show_findings.py pass1 B16
    python audit/scripts/show_diff.py pass1 B16
    ```

    Check every item against the English. Look up the corpus when a term or name is in doubt, because agents sometimes "fix" toward a spelling the rest of the translation doesn't use. Record rejections and changes in `pass1/decisions.json`:

    ```
    "B16": {
      "drop": [3, 7],
      "edit": { "12": { "replace": "corrected text" } },
      "add": [ { "id": "File.xml|Key", "sev": "low", "cat": "typo", "note": "why", "find": "old", "replace": "new" } ]
    }
    ```

    The numbers are the 1-based positions that `show_findings.py` prints. Anything not listed is accepted. Mark the batch `[~]` in `pass1/LEDGER.md`.

7. **Checkpoint with VK.** Merge and dry-run:

    ```
    python audit/scripts/merge_approved.py pass1 wave4 B16 B17 B18 B19 B20 B21
    python audit/scripts/apply_fixes.py audit/pass1/wave4.json --dry-run
    ```

    Every fix must report as applicable. Summarize the counts and the worst findings, point VK at `pass1/wave4.md`, and ask before applying.

8. **Apply and validate.**

    ```
    python audit/scripts/apply_fixes.py audit/pass1/wave4.json
    python ~/.claude/skills/zephon-localization-update/scripts/Validate-Localization.py
    python ~/.claude/skills/zephon-localization-update/scripts/Find-MixedScript.py
    ```

    Both validators must end with 0 problems. Then mark the batches `[x]` in the ledger and append their ids to `scanned_ids.txt`:

    ```
    python -c "import re; ids=[i for b in ['B16','B17','B18','B19','B20','B21'] for i in re.findall(r'^## (.+)$', open(f'audit/pass1/batches/{b}.txt', encoding='utf-8').read(), re.M)]; open('audit/pass1/scanned_ids.txt', 'a', encoding='utf-8', newline='\n').write('\n'.join(ids) + '\n')"
    ```

9. **Update this file** after every wave: "Where things stand", the wave plan and "What was applied".

## When the audit stops for the day

1. Sync `ModData/Data/Core/Languages/` to the live mod folder and to the Workshop copy, then confirm every language declared in `Languages.xml` has a populated folder in all three places (skill steps 11 and 12).
2. Add a dated status block to `README.md` (Ukrainian).
3. Update this file, then commit and push per the commits skill.

## After B67

1. Rerun the script sweep on the finished text into a new folder, so the first sweep stays on record: `python audit/scripts/sweep.py pass1-final`. Also search for leftovers of VK's decisions: «ти» and «твій» forms addressing the player, «-ючий» participles, «Теча», «Пустошник», «клітин».
2. Start pass 2 with fresh eyes: `python audit/scripts/build_batches.py pass2`, same brief, same wave routine, findings under `pass2/`. VK's goal is to keep scanning until a pass comes back clean.
3. Finish like a normal update: README block, commit and push, sync the live mod and Workshop copy, and draft the Workshop change-log note and description (skill step 13) so VK can re-publish.

## Pitfalls already hit

- Inline Python containing curly quotes (“ ” ‘ ’ „) inside a Bash heredoc breaks Git Bash. Put such scripts in a file and run the file.
- A `cd` inside a Bash call moves the working directory for every later call. Use absolute paths, or `cd` back to the repo root.
- Agent task output files are empty placeholders. Use the findings files to track progress.
- A network outage kills running agents. They report "failed" and resume cleanly with SendMessage.
- A «ви» rewrite replaces the whole entry value. Any other fix for that entry has to be folded into the rewrite, or it no longer matches.
- Term-wide renames (like Теча to Кровотеча) must match whole words and every case form, never a blind substring. Generate them from the current text after the wave's fixes are applied, dry-run, then apply.
- Batch files are snapshots. Rebuild later batches if anything changed their entries.
- The validator's NOTES list (seven `<string/>` gaps, Branches.xml as a mod-only file, the empty Labels.xml) is expected, not a defect. The mixed-script check has no allowed words any more, so any hit it reports is real.
- `Find-MixedScript.py` only sees Latin letters touching Cyrillic ones. A pun split by a dot or a dash («DOOM.ати») slips past it, so read Latin runs in Emulated Mind lines by eye.
- A session limit stops every running agent for good. Wave 3 lost four batches that way twice. Relaunch them; only the tokens they had spent are lost.
- An agent may write short finds for its «ви» rewrites instead of the whole entry. B14 did it for about 50 entries, and `show_diff.py` flags each as "find is not the whole current value". They apply fine while each find is unique, but check the rest of the entry for a «ти» the agent skipped.
- An agent can rewrite its findings file after first saving it (B12's counts changed). Triage a batch only after its agent has reported back.

## Cost and timing

- Wave 3 (Diplomacy) took 9 to 31 minutes per batch, run in parallel, and 110,000 to 300,000 agent tokens per batch (B12 was the outlier at 300,000). That is about 1,000,000 tokens for the wave, not counting the runs lost to session limits.
- The earlier waves took 40 to 60 minutes and roughly 700,000 agent tokens (100,000 to 140,000 per batch).
- Six agents at once can hit the session limit mid-wave. VK chose on 18.09.2026 to keep six anyway: the total cost is the same, and a wave finishes sooner.
