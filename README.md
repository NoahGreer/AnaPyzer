# AnaPyzer

## Synopsis

This is Group 2's IT Project for CSD 299 Spring 2018

## Screenshot

![AnaPyZer Screenshot](https://github.com/NoahGreer/AnaPyzer/blob/master/AnaPyzer_screenshot.png)

## Authors

* **Daniel Estes**
* **Michael Langley**
* **Nathan O'Brien**
* **Noah Greer**

See also the list of [contributors](https://github.com/NoahGreer/AnaPyzer/contributors) who participated in this project.

## Prerequisites/Dependencies
	Python 3.6
	MatplotLib

## Installation
The application can be installed by cloning the repository and executing the installation script:
```python
python setup.py install
```
If cloned from github, ip address database files will be included as ips.zip.  Simply unzip this file into the root directory of the AnaPyzer application.  

If the ip address database files have become corrupted/deleted/obsolete, please download a new core ip/country code data csv from https://db-ip.com/db/download/country.  Unzip the gz file into the AnaPyzer root directory, rename the file to ips.csv and run the ipdbbuild script.  This will parse the file and create the ip address database.

The application can then be run by executing:
```python
python anapyzer.py
```
## Technologies/Built With
This project uses tkinter for the GUI and matplotlib to generate graphs

## Tests
Tests are stored in the 'tests' subfolder and can be run by executing the following from the project root directory:
```python
python -m unittest discover tests
```
