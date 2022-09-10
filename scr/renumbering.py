from pathlib import Path

import click

from main import _re_numbering, _re_numbering_all

# this file is for turning main.py into command line tool by click package.
# just decorating core functions in main.py


@click.command(help="re-numbering digit number located at the end of each row in a text file.")
@click.argument("path", type=click.Path(exists=True))
@click.option(
    "-d",
    "--dirout",
    type=click.Path(file_okay=False),
    help="directory where output text file is saved. the default uses the same place as the input text file.",
)
@click.option(
    "-p",
    "--pre",
    default="",
    type=str,
    help="prefix for the stem-name of the output text file. the default is ''. see --join option.",
)
@click.option(
    "-s",
    "--suf",
    default="_renumbered",
    type=str,
    help="suffix for the stem-name of the output text file. the default is '_cleaned'. see --join option.",
)
@click.option(
    "-j",
    "--join",
    default="",
    type=str,
    help="the character with which prefix + (text file name) + suffix are combined. e.g., prefix='pre', text file name='sample.txt', suffix='suf', join='_' -> output text file name='pre_sample_suf.txt'",
)
@click.option(
    "-o",
    "--overwrite",
    type=bool,
    is_flag=True,
    help="overwrite input file with output. If enabled, all options for output file name such as --dirout, --pre and --join are ignored.",
)
@click.option(
    "-m", "--missing", type=bool, is_flag=True, help="point out rows with no page number at the end of the process."
)
@click.option(
    "-b", "--blank", type=bool, is_flag=True, help="add blank line at the end of the text if there is not the one."
)
def renumbering(
    path: str | Path, dirout: str | None, pre: str, suf: str, join: str, overwrite: bool, missing: bool, blank: bool
) -> None:
    path = Path(path)
    if path.is_file():
        _re_numbering(
            file=path,
            dir_out=dirout,
            prefix=pre,
            suffix=suf,
            join_with=join,
            overwrite=overwrite,
            missing_page_number=missing,
            add_last_space=blank,
        )
    elif path.is_dir():
        _re_numbering_all(
            dir=path,
            dir_out=dirout,
            prefix=pre,
            suffix=suf,
            join_with=join,
            overwrite=overwrite,
            missing_page_number=missing,
            add_last_space=blank,
        )


if __name__ == "__main__":
    renumbering()
