import os
import shutil


def clean_directories() -> None:
    dirs_to_remove = [
        "__pycache__",
        "models/__pycache__",
        "simulation/__pycache__",
        "ui/__pycache__",
        ".mypy_cache",
        ".ruff_cache",
    ]

    for dir_path in dirs_to_remove:
        try:
            if os.path.exists(dir_path):
                shutil.rmtree(dir_path)
        except Exception as e:
            print(f"Error when deleting {dir_path}: {e}")


def clean_files() -> None:
    file_extensions = [".pyc", ".pyo"]
    for root, _, files in os.walk("."):
        for file in files:
            if any(file.endswith(ext) for ext in file_extensions):
                try:
                    os.remove(os.path.join(root, file))
                except Exception as e:
                    print(f"Error when deleting {file}: {e}")


if __name__ == "__main__":
    clean_directories()
    clean_files()
