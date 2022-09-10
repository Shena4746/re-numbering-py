from pathlib import Path
from typing import Optional, TypeAlias

from rich import print

from Re_Numbering import Re_Numbering
from Text_Lines import Paged_Text_Lines

Save_Result: TypeAlias = tuple[Path, bool]


def save_text(
    text: str,
    dir_out: Path,
    name_out: str,
) -> Save_Result:
    if not dir_out.exists():
        dir_out.mkdir(parents=True)
    text_path: Path = dir_out / name_out
    with open(text_path, mode="w") as tf:
        tf.write(text)
    return text_path, text_path.exists()


def get_new_file_name(file: Path, prefix: str = "", suffix: str = "", join_with: str = "") -> str:
    return f"{join_with.join([prefix,file.stem,suffix])}{file.suffix}"


def point_out_missing_page_number(lines: Paged_Text_Lines):
    missing: list[str] = [
        f"{str(i+1).zfill(3)} | {line.to_text()}" for i, line in enumerate(lines) if line.page_number is None
    ]
    if missing != []:
        out: str = "\n".join(missing)
        print(out)


def add_trailing_space(text: str) -> str:
    return text + "\n" if text.split(sep="\n")[-1] != "" else text


def _re_numbering(
    file: str | Path,
    dir_out: Optional[str | Path],
    prefix: str = "",
    suffix: str = "",
    join_with: str = "",
    overwrite: bool = False,
    missing_page_number: bool = False,
    add_last_space: bool = False,
    support: list[str] = [".txt", ".yaml", "yml"],
) -> Path:
    file = Path(file)
    if not file.is_file():
        raise ValueError(f"{file} is not a file.")
    if file.suffix not in support:
        raise ValueError(f"{file} is not a supported extension.")
    with open(str(file)) as f:
        text: str = f.read()
        re_numberer = Re_Numbering(Paged_Text_Lines(text))
        lines_out: Paged_Text_Lines = re_numberer.re_numbering()
        if missing_page_number:
            point_out_missing_page_number(lines_out)
        # text_out: str = lines_out.to_text()
        text_out: str = add_trailing_space(lines_out.to_text()) if add_last_space else lines_out.to_text()
        # save
        dir_out = file.parent if dir_out is None else Path(dir_out)
        saved_file, success = save_text(
            text=text_out,
            dir_out=file.parent if overwrite else dir_out,
            name_out=file.name
            if overwrite
            else get_new_file_name(file=file, prefix=prefix, suffix=suffix, join_with=join_with),
        )
        if not success:
            raise Exception(f"failed to save {str(saved_file)}.")
        return saved_file


def _re_numbering_all(
    dir: str | Path,
    dir_out: Optional[str | Path],
    prefix: str = "",
    suffix: str = "",
    join_with: str = "",
    overwrite: bool = False,
    missing_page_number: bool = False,
    add_last_space: bool = False,
    support: list[str] = [".txt"],
) -> None:
    dir = Path(dir)
    if not dir.is_dir():
        raise ValueError(f"{dir} is not a directory.")
    for extension in support:
        for file in dir.glob(f"*{extension}"):
            _re_numbering(
                file=file,
                dir_out=dir_out,
                prefix=prefix,
                suffix=suffix,
                join_with=join_with,
                overwrite=overwrite,
                missing_page_number=missing_page_number,
                add_last_space=add_last_space,
                support=support,
            )
