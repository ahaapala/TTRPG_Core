# TTRPG_Core

## Table of Contents
+ [About](#about)
+ [Getting Started](#getting_started)
+ [Usage](#usage)

## About <a name = "about"></a>

This library is the current core of code for exploring Table Top Role Playing Game systems programatically.  It mimics dice, dice pools, and full systems (e.g. D&D, CoC, etc...).  I want to be able to perform statistical analysis and emulate various aspects of a TTRPG.  This will allow me to better learn, master, run, and design them.  This logic is meant to be utilized by other libraries which will provide interfaces, enrichment, and interconnectivity.  Usecases include: slack/chat bot, web-applications, and machine learning.

## Getting Started <a name = "getting_started"></a>
* Make sure you're using python3
* Clone the code
* Create a virtualenv and install the [requirements](requirements.txt) 
* Execute the [run_script.py](run_script.py).  Check out the [usage](#usage)

### Prerequisites

* Python 3 (although I'm not doing anything so specific that wouldn't be portable to 2.x)
* See [requirements.txt](requirements.txt) You probably want to install them into a virtualenv or similar

```
$ virtualenv --python=python3 _venv
Already using interpreter /usr/bin/python3
Using base prefix '/usr'
New python executable in /home/ahaapala/_venv/bin/python3
Also creating executable in /home/ahaapala/_venv/bin/python
Installing setuptools, pkg_resources, pip, wheel...done.
$ source _venv/bin/activate
(_venv)$ pip install -r requirements.txt
```

### Installing

If all the prereq's install w/o issue you should be good to run and develop the code.


## Usage <a name = "usage"></a>

run_script.py has usage info.  It currently is ...

```
(_venv)$ ./run_script.py --help
usage: run_script.py [-h] [-d D_NOTE | -s SYSTEM] [-v] [-t] [-g] [--name NAME]
                     [--notes NOTES]

Runner for dice system tools

optional arguments:
  -h, --help            show this help message and exit
  -d D_NOTE, --dice-pool D_NOTE
                        Roll some dice, e.g. 3d12
  -s SYSTEM, --system SYSTEM
                        Specify what ttrpg system to use
  --name NAME           Name used as an id in various parts of the code
  --notes NOTES         Misc notes about what you are trying to do

Misc:
  Miscellaneous

  -v, --verbose         Print debugging information
  -t, --test            Run the test block
  -g, --graph           Graph the results of the operation
```
