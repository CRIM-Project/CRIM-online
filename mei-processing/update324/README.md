# Updating MEI 3 to 4

## Installation

It's recommended to set up a local environment, activate it, and install requirements

Example (your preferred tools may vary):
```sh
$ python -m venv .env
$ source .env/bin/activate
$ pip install -r requirements.txt
```

## Step 1 - conversion with MEIGarage

Run `convert_all.py` to update all files in `../../crim/static/mei/MEI_3.0/`. These will be placed in `./output` by default.

The conversion relies on MEIGarage, an online MEI conversion service, so you will need an active connection.

## Step 2 - adding metadata

MEI v3 files don't have much metadata in the MEI header. The CSV files in `./data` contain new metadata to be added to the MEI v4 files.

To add these metadata, run `add_metadata.py`. The script will update files in `./output`. 

You are now ready to place the MEI v4 files in `./output` where they are needed.