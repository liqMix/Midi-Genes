# Midi-Genes
Generates melodies based on an evolutionary model using reproduction, cross-over, and mutation.
Uses a backing track in the given key in order to give the melody context.
Currently only supports a set BPM of 120 and the key of 'C'.

## Modules
* Python3
* [python-midi](https://github.com/vishnubob/python-midi) - python3 branch

## Execution
Can be ran with <pre>python midi-gene</pre>

## Parameters
* Epoch, population size, and mutation rate are currently set in midi-gene.py
* Fitness rewards are set in Fitness.py
* BPM and Key are set in Parameters.py

## Fitness
Currently a track's fitness is calculated by six heuristics:
* Rewarded for each note whose pitch lies in the track's key
* Rewarded for starting on the root or fifth of the track's key, penalized for not ending on the root
* Rewarded for following a jump in pitch with reverse pitch movement
* Penalized for large distances between note pitches
* Penalized for a "tritone" interval
* Penalized for repeating the same note duration

## TODO
* Localize all parameters into one location for simple control
* Add parameter setting through argument values
* Tune rewards improve output
* Add less naive fitness heuristics
* Modulate timing and pitch of backing track to match other BPMs and Keys
* Allow setting the melodical instrument used
