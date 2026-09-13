from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent
INPUT_DIR = PROJECT_ROOT / "data" / "input"


def main():
    INPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("secretariat automation")
    print("workflow started successfully.")
    print(f"input directory: {INPUT_DIR}")


if __name__ == "__main__":
    main()