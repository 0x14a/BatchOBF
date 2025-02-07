import argparse
from pathlib import Path
from typing import Final


class BatchOBF:
    NEW_BYTES: Final[bytes] = b"\xFF\xFE\x0D\x0A"

    def __init__(self, path: str, output: str) -> None:
        self.path = path
        self.output = output

    def __get_file_path(self) -> Path:
        file_path = Path(self.path)
        if not file_path.is_file():
            raise FileNotFoundError(
                f"Input file '{self.path}' does not exist."
            )
        return file_path

    def __batch_file(self, file: Path) -> None:
        if not file.name.lower().endswith(".bat"):
            raise ValueError("Select a valid '.bat' file.")

    def modify_file_bytes(self) -> Path:
        file_path = self.__get_file_path()
        self.__batch_file(file_path)

        new_filename = f"{self.output}_obfuscated.bat"
        new_file = file_path.parent / new_filename

        try:
            original_bytes = file_path.read_bytes()
            new_file.write_bytes(self.NEW_BYTES + original_bytes)
        except Exception as e:
            raise Exception(f"Error obfuscating file: {e}")

        return new_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "BatchOBF is a Python obfuscation tool designed to make batch "
            "files harder to understand for casual users."
        ),
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        help="The file containing the batch code to obfuscate",
        metavar="PATH",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=False,
        help="The file to write the obfuscated code (defaults to [input]_obfuscated.bat)",
        metavar="FILENAME",
    )
    args = parser.parse_args()

    if not args.output:
        args.output = Path(args.input).stem

    try:
        obfuscator = BatchOBF(args.input, args.output)
        output_path = obfuscator.modify_file_bytes()
        print(
            f"Obfuscation completed successfully! File saved at: {output_path}"
        )
    except Exception as error:
        print(f"An error occurred: {error}")
        exit(1)
