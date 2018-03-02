# Kyiv team - Google HashCode 2018 

## Overview
With this algorithm we're ranked 56th out of about 30 000 teams from all
over Europe:)
The final score is **49,275,031**.

## Authors
Oleh Rybalchenko

Olexandr Yarushevskyi

## Run

Algorithm runner requires the only parameter - problem name. To run, say, 
**b_should_be_easy**: 

> python3 alg_runner.py --file b_should_be_easy

All input files should be in `input` dir, format - `<problem name>.in`.

Results will be placed in `output` dir, format - `<problem name>.out`, 
rewriting old files with the same names.

## Project structure:

### Reader
Data file parser that transforms input to objects defined in entities
To get parsed data, run:

```python 
reader = VehicleAssignmentReader('input/{}.in'.format(file))
data = reader.process()
```

### Greedy
Algorithm class that receives input once and then store its state 
while solving. Greedy algorithm instance contains both full problem's 
data and operations required to solve it. 
Method `run` controls the solving flow.

```python 
g = Greedy(data.header, data.rides)
g.run()
g.output("output/{}.out".format(file))
```

### Entities
Prototypes of involved objects, operations definition
