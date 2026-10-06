# Plot-study CLI runner

This runner manages storage and session continuity only. The supervisor supplies
the final question, paper corpus, initial prompt, and each subsequent discussion
prompt. It does not prescribe slide count, chapters, claims, or figure choices.

## Execution Settings

Every new session and resumed turn uses `gpt-6-luna`, reasoning effort `high`,
no profile, `--approve-for-me`, and config overrides for `workspace-write` and
network access. The approval option belongs to the parent `exec` command before
`resume`; the explicit `--sandbox` option is omitted to avoid its flag conflict.
There is no token cap, timeout, automatic feedback, or automatic retry.

Use an escalated command invocation (`require_escalated`) when running real
Codex turns. `freeze`, `prepare`, and unit tests do not launch a real model.
The runner does not use `--ephemeral` or `resume --last`.

## Required Order

1. The supervisor approves the current skill version after its final review.
2. Freeze that version once. Source roots are `SKILL.md`, `references/`,
   `scripts/`, `assets/`, and `agents/`; caches and Python bytecode are excluded.
3. The corpus owner finishes the papers and bibliography. The supervisor
   adjusts and confirms the question and initial prompt.
4. Prepare all three workspaces from the same frozen snapshot and final corpus.
5. Launch the three initial turns in parallel using separate run numbers.
6. The supervisor reads each plot and writes its feedback. Resume the matching
   thread explicitly for each discussion round.
7. Preserve all drafts and rounds. Revise the skill only after all three
   discussion processes have finished.

```sh
python3 evaluations/luna-plot-study/runtime/runner.py freeze
python3 evaluations/luna-plot-study/runtime/runner.py prepare --run 1 --corpus evaluations/luna-plot-study/corpus
python3 evaluations/luna-plot-study/runtime/runner.py turn --run 1 --round draft --prompt /path/to/confirmed-initial-prompt.txt
python3 evaluations/luna-plot-study/runtime/runner.py turn --run 1 --round r1 --prompt /path/to/supervisor-r1-prompt.txt
```

Repeat `prepare` and the initial `turn` for run 2 and run 3; separate processes
can execute concurrently. Use a fresh round name for every subsequent turn,
including any environment-recovery turn. Existing snapshots, runs, and round
directories are never overwritten.

## Stored Evidence

- `runtime/snapshot-manifest.json`: source roots and individual file hashes.
- `run-N/workspace/`: copied skill, `corpus/`, local execution instructions,
  and the agent's `outputs/` directory.
- `run-N/input-manifest.json`: hashes for each copied skill/paper input and
  workspace instructions. Inputs are checked before and after every round.
- `run-N/state.json`: exact settings, active state, round names, and conversation
  ID saved as soon as `thread.started` arrives.
- `run-N/rounds/ROUND/`: original `prompt.txt`, `events.jsonl`, `stderr.log`,
  `final.txt`, `execution.json`, and independent `before/` and `after/` copies
  of the output artifacts. These records survive changes to the next draft.

Workspace instructions establish a read-only convention for the supplied skill
and papers and prohibit exploring sibling runs and supervisor records. They do
not establish physical filesystem isolation. The run's `completed` state means
that the CLI exited zero, emitted `turn.completed`, saved a final response, and
preserved input integrity; it does not mean the generated plot passed review.
Individual command failures are recorded separately even when the overall CLI
exits zero. Raw events remain the authoritative record for interpreting tool
outputs, including compound commands that can hide an earlier failure.

If a process crashes, inspect its recorded PID, events, and stderr before
changing its running state or resuming. Preserve the unfinished round and use a
new round name. Record environment repairs and execution-state changes in the
existing runtime/run records; do not send substantive plot guidance as a repair.

Focused checks use a fake CLI and temporary fixture inputs, with no real model
invocation:

```sh
python3 -m unittest discover -s evaluations/luna-plot-study/runtime -p 'test_runner.py' -v
```
