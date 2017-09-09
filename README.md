# lm
I/O management for Experiments in Machine Learning

## Installation
```bash
python setup.py install
```

## Usage
lm uses SQLite3 for managing executed experiments and administrative metadata. To init your Machine Learning system, you simply run

```bash
python -m lm init
```

This command creates the directory and init the database in `./.lm/`.

Then, you can execute experiments under the control of lm, which automatically creates an unique directory for stdout and stderr (the default is in `./logs/[number].exp/`) for the execution. At the same time, the execution metadata (e.g., running time, started and ended time, user environment, ...) are collected and are going to be inserted to the database.

```bash
python -m lm run './myscript'
```

`ls` command displays all the managed data for experiments in the database.

```bash
python -m lm ls
```

## Note
To obtain the log directory that lm created for the execution from your programs, you can use a shell environment variable, namely `LM_LOGS_PATH`.

