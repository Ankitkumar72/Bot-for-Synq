# Local Competitive Programming Setup

Use this folder like a simple online compiler.

## Files
- `practice.py`: write your solution here.
- `inputs.txt`: put the stdin input here.
- `output.txt`: generated output after each run.
- `expected.txt` (optional): expected output for PASS/FAIL check.
- `run_judge.py`: runs one test cycle (input -> output + optional PASS/FAIL). Supports both CP and LeetCode-style files.
- `watch_cp.py`: auto-runs whenever tracked files are saved.

## One-time run
Run the judge once:
```powershell
python run_judge.py practice.py
```

## Auto-run watch mode
Start watch mode once:
```powershell
python watch_cp.py practice.py
```
Then every save of that code file, `inputs.txt`, or `expected.txt` will auto-run and refresh `output.txt`.

Stop watch mode with `Ctrl+C`.

## VS Code
- `F5` with `CP: Watch Mode (auto-run on save)` for continuous runs on the current open file.
- `F5` with `CP: Fast Run (inputs.txt -> output.txt)` for one quick run on the current open file.

## Typical workflow
1. Write/modify your code in `practice.py`.
2. Put test input in `inputs.txt`.
3. Put expected output in `expected.txt` (optional).
4. Start watch mode once (or use fast run).
5. Check `output.txt` and terminal PASS/FAIL message.

## LeetCode Style Support
If your file uses `class Solution` without printing, `run_judge.py` will auto-try LeetCode mode when stdout is empty.

Input formats supported in `inputs.txt`:
- Single method argument: one Python literal, e.g. `[1, 2, 3]` or `"abc"`.
- Multiple arguments: one line with space-separated values, e.g. `35 10`.
- Multiple arguments as literal list/tuple, e.g. `[35, 10]` or `(35, 10)`.
- Multiple methods in `Solution`: first line can select method:
  - `method: commonFactors`
