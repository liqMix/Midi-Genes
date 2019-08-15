# Midi-Genes
Generates melodies based on an evolutionary model using reproduction, cross-over, and mutation.
Uses a backing track in the given key in order to give the melody context.
Mostly used as an interesting application; only occasionally have produced melodies sounded 'pleasing'.

## Modules
* Python3
* [python-midi](https://github.com/vishnubob/python-midi) - python3 branch

## Execution
Can be ran with <pre>python midigene.py</pre>
This is the same as running with arguments:
    <pre>python midigene.py -note=C -scale=major -bpm=120 -pop_size=1000 -epochs=50000 -mut_rate=0.15 -bass=true -drums=true</pre>

## Parameters
* Epoch, population size, and mutation rate are currently set in midigene.py
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
* Tune rewards to improve output
* Add less naive fitness heuristics
* Allow setting the melodical instrument used
