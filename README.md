# Re-numbering tool for table_of_content.txt

## About

A python script to replace Arabic numbers at the end of each line in a text file.
When it finds a sign of the form "old_number->new_number", for instance 1->11, at the end of a line, it replaces the sign with new_number(11) and remembers the difference d:=new_number-old_number(10=11-1).
It then adds d to each number that appears after the sign.
The value of d is updated when it finds a new sign.

## Sample

The first of the following text is an input for the script, and the second is the output.

```txt
# input /sample/sample1.txt
CHAPTER I
Hilbert Spaces
§1. Elementary Properties and Examples 1->11
§2. Orthogonality 
§3. The Riesz Representation Theorem 10
§4. Orthonormal Sets of Vectors and Bases 20->23
§5. Isomorphic Hilbert Spaces and the Fourier Transform for the Circle 30
§6. The Direct Sum of Hilbert Spaces 40
```

```txt
# output /sample/sample1_renumbered.txt
CHAPTER I
Hilbert Spaces
§1. Elementary Properties and Examples 11
§2. Orthogonality 
§3. The Riesz Representation Theorem 20
§4. Orthonormal Sets of Vectors and Bases 23
§5. Isomorphic Hilbert Spaces and the Fourier Transform for the Circle 33
§6. The Direct Sum of Hilbert Spaces 43
```

[sample folder](/sample) contains these text files.

## Usage

### Command

Simply run the following.

```bash
python ./scr/renumbering.py ./sample/sample1.txt
```

It has some options, for instance, `-d` for specifying output directory, `-o` for overwriting input file, `-m` for pointing out lines with no page numbers in the output.
For detail, see help.

```bash
python ./scr/renumbering.py --help
```

### Rule about `->`

There can be spaces around `->`.

```txt:
# ok
sample 1 -> 4
sample 1->4
sample 1-> 4
sample 1 ->4
sample -3  ->  4
```

There must be space before mapping description.

```txt: ng
# ng
sample1 -> 4
```

Mapping symbol must be exactly `->`.

```txt: ng
# ng
sample 1 --> 4
sample 1 ->> 4
sample 1 >> 4
```

Re-numbering zone can be limited by placing a trivial mapping `x -> x`:

```txt:before
# before
§1. Elementary Properties and Examples 1->8
§2. Orthogonality 
§3. The Riesz Representation Theorem 10
§4. Orthonormal Sets of Vectors and Bases 20->20
§5. Isomorphic Hilbert Spaces and the Fourier Transform for the Circle 30
§6. The Direct Sum of Hilbert Spaces 40
```

The above example re-numbers the first 3 lines only.

```txt:after
# after
§1. Elementary Properties and Examples 8
§2. Orthogonality 
§3. The Riesz Representation Theorem 17
§4. Orthonormal Sets of Vectors and Bases 20
§5. Isomorphic Hilbert Spaces and the Fourier Transform for the Circle 30
§6. The Direct Sum of Hilbert Spaces 40
```

## Install

- Tested Environment
  - Windows 10 + WSL2 + Ubuntu 20.04
  - python 3.10.5 (pyenv 2.3.2) + poetry (1.1.11)

Follow a typical routine of setting up a virtual environment by pyenv + poetry.

```bash
git clone https://github.com/Shena4746/re-numbering-py.git
cd ./re-numbering-py
pyenv local 3.10.5
```

The last line fails if you have not downloaded python 3.10.5. Run the following to download it, and try the previous pyenv command again.

```bash
pyenv install 3.10.5
```

Locate the python interpreter at {project-top}/.venv. Then let poetry perform a local installation of dependency.

```bash
python3 -m venv .venv
poetry install
```

Make sure that poetry uses the intended python interpreter.

```bash
poetry run which python
poetry run python --version
```
