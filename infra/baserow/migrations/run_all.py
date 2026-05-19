"""Run all Baserow migrations in order. Idempotent."""
import sys, importlib.util, pathlib

HERE = pathlib.Path(__file__).parent


def import_module_from_path(name: str, path: pathlib.Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


def main():
    sys.path.insert(0, str(HERE))  # so each migration can `from _api import ...`
    migrations = sorted(p for p in HERE.glob("[0-9][0-9]_*.py") if p.is_file())
    for path in migrations:
        print(f"--- {path.name} ---")
        mod = import_module_from_path(path.stem, path)
        mod.run()
    print("\nAll migrations complete.")


if __name__ == "__main__":
    main()
