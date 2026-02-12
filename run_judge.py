from pathlib import Path
import ast
import importlib.util
import inspect
import subprocess
import sys
from types import ModuleType


BASE_DIR = Path(__file__).resolve().parent
DEFAULT_CODE_FILE = BASE_DIR / "practice.py"
INPUT_FILE = BASE_DIR / "inputs.txt"
OUTPUT_FILE = BASE_DIR / "output.txt"
EXPECTED_FILE = BASE_DIR / "expected.txt"


def normalize(text: str) -> str:
    return text.replace("\r\n", "\n").rstrip("\n")


def resolve_code_file(raw_path: str | None) -> Path:
    if not raw_path:
        return DEFAULT_CODE_FILE

    code_file = Path(raw_path)
    if not code_file.is_absolute():
        code_file = BASE_DIR / code_file
    return code_file


def parse_literal_or_text(value: str):
    text = value.strip()
    if text == "":
        return ""
    try:
        return ast.literal_eval(text)
    except Exception:
        return text


def extract_method_hint(input_data: str) -> tuple[str | None, list[str]]:
    lines = [line.strip() for line in input_data.splitlines() if line.strip()]
    if lines and lines[0].lower().startswith("method:"):
        method_name = lines[0].split(":", 1)[1].strip()
        return method_name or None, lines[1:]
    return None, lines


def parse_leetcode_args(
    lines: list[str], param_names: list[str]
) -> tuple[list | None, str | None]:
    argc = len(param_names)
    if argc == 0:
        return [], None

    if not lines:
        return None, "No input values found for Solution method arguments."

    payload = "\n".join(lines).strip()

    try:
        parsed = ast.literal_eval(payload)
        parsed_ok = True
    except Exception:
        parsed = None
        parsed_ok = False

    if parsed_ok:
        if argc == 1:
            return [parsed], None
        if isinstance(parsed, dict) and all(name in parsed for name in param_names):
            return [parsed[name] for name in param_names], None
        if isinstance(parsed, (list, tuple)) and len(parsed) == argc:
            return list(parsed), None

    if len(lines) == argc:
        return [parse_literal_or_text(line) for line in lines], None

    if len(lines) == 1 and argc > 1:
        tokens = lines[0].replace(",", " ").split()
        if len(tokens) == argc:
            return [parse_literal_or_text(token) for token in tokens], None

    if argc == 1:
        return [[parse_literal_or_text(line) for line in lines]], None

    return None, f"Could not map inputs.txt values to {argc} method arguments."


def load_target_module(target_file: Path) -> ModuleType:
    module_name = f"_cp_target_{target_file.stem}_{abs(hash(str(target_file)))}"
    spec = importlib.util.spec_from_file_location(module_name, str(target_file))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load module from {target_file}")

    module = importlib.util.module_from_spec(spec)
    sys.modules.pop(module_name, None)
    spec.loader.exec_module(module)
    return module


def select_solution_method(
    module: ModuleType, method_hint: str | None
) -> tuple[callable | None, str | None]:
    solution_cls = getattr(module, "Solution", None)
    if solution_cls is None:
        return None, "No Solution class found for LeetCode mode."

    instance = solution_cls()
    methods: list[tuple[str, callable]] = []

    for name, member in solution_cls.__dict__.items():
        if name.startswith("_"):
            continue
        if isinstance(member, (staticmethod, classmethod)) or callable(member):
            bound = getattr(instance, name)
            if callable(bound):
                methods.append((name, bound))

    if not methods:
        return None, "No public method found inside Solution class."

    if method_hint:
        for name, method in methods:
            if name == method_hint:
                return method, None
        return None, f"Method '{method_hint}' not found in Solution class."

    if len(methods) == 1:
        return methods[0][1], None

    method_names = ", ".join(name for name, _ in methods)
    return methods[0][1], (
        f"Multiple Solution methods found ({method_names}). "
        f"Using '{methods[0][0]}'. Add 'method: <name>' as first line in inputs.txt to choose."
    )


def try_leetcode_mode(target_file: Path, input_data: str) -> tuple[str | None, str | None]:
    try:
        module = load_target_module(target_file)
    except Exception as exc:
        return None, f"LeetCode mode import failed: {exc}"

    method_hint, lines = extract_method_hint(input_data)
    method, method_note = select_solution_method(module, method_hint)
    if method is None:
        return None, method_note

    signature = inspect.signature(method)
    param_names = list(signature.parameters.keys())
    args, parse_error = parse_leetcode_args(lines, param_names)
    if args is None:
        return None, parse_error

    try:
        result = method(*args)
    except Exception as exc:
        return None, f"LeetCode mode execution failed: {exc}"

    output = "" if result is None else str(result)
    return output, method_note


def main(code_file: Path | None = None) -> int:
    target_file = code_file or DEFAULT_CODE_FILE

    if not target_file.exists():
        print(f"Missing code file: {target_file}")
        return 1

    if not INPUT_FILE.exists():
        print("Missing inputs.txt")
        return 1

    input_data = INPUT_FILE.read_text(encoding="utf-8")

    run = subprocess.run(
        [sys.executable, str(target_file)],
        input=input_data,
        text=True,
        capture_output=True,
        cwd=BASE_DIR,
    )

    if run.returncode != 0:
        print(f"Runtime Error in {target_file.name}")
        if run.stderr:
            print(run.stderr)
        return run.returncode

    output_text = run.stdout
    execution_mode = "CP (stdin/stdout)"

    if normalize(output_text) == "":
        leetcode_output, leetcode_note = try_leetcode_mode(target_file, input_data)
        if leetcode_output is not None:
            output_text = leetcode_output
            execution_mode = "LeetCode (Solution class)"
        if leetcode_note:
            print(leetcode_note)

    OUTPUT_FILE.write_text(output_text, encoding="utf-8")

    print("Program executed successfully.")
    print(f"Code file: {target_file.name}")
    print(f"Execution mode: {execution_mode}")
    print("Output written to output.txt")

    if EXPECTED_FILE.exists():
        expected = normalize(EXPECTED_FILE.read_text(encoding="utf-8"))
        actual = normalize(output_text)
        if actual == expected:
            print("Test Result: PASS")
            return 0

        print("Test Result: FAIL")
        print("Expected (expected.txt):")
        print(EXPECTED_FILE.read_text(encoding="utf-8"))
        print("Actual (output.txt):")
        print(output_text)
        return 2

    print("Tip: add expected.txt to enable automatic PASS/FAIL checks.")
    return 0


if __name__ == "__main__":
    arg_file = sys.argv[1] if len(sys.argv) > 1 else None
    exit_code = main(resolve_code_file(arg_file))

    # Treat test-case mismatch (exit code 2) as a normal outcome.
    # This avoids noisy SystemExit popups in VS Code debug runs.
    if exit_code == 2:
        pass
    elif sys.gettrace() is None:
        raise SystemExit(exit_code)
