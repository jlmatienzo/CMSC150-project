# CMSC 150 Project

Final Project for the course **CMSC150: Numerical and Symbolic Computation**

A generic solver that performs **Quadratic Spline Interpolation** and
**Polynomial Regression** on a given CSV file input, and solves a specific
**Minimization Problem** on shipping costs of goods

## Getting Started

.You can acquire the code from the GitHub [repository](https://www.github.com/jonlowi/CMSC150-project)
and download it as a zip file or you can clone it by typing the command below
```
git clone https://github.com/jonlowi/CMSC150-project
```

### Prerequisites

The program is written in `Python3` and uses `PyQt5` Library to implement the
user interface

Most Linux distributions come with Python pre installed. Check version of Python in your system
```
python3 --version
```
Upgrade to the latest vesion of Python using the command below
```
sudo apt-get update
sudo apt-get -y upgrade
```

PyQt library contains Python bindings for the Qt cross platform UI and
application toolkit

Check if PyQt5 is installed in your system
```
pip3 show PyQt5
```
If it is not yet in the system install it by typing
```
pip3 install PyQt5
```

## Running the Program

Navigate to the root folder of the project then run
```
python3 main.py
```

The CSV file input are required to follow the format
```
<x1>,<y1>
<x2>,<y2>
<x3>,<y3>
.
.
.
<xn>,<yn>
```

## Author
* **John Louie Matienzo** - CMSC150 Section B-3L