# Midi-Genes
Generates melodies based on an evolutionary model using reproduction, cross-over, and mutation.
Uses a backing track in the given key in order to give the melody context.
Mostly used as an interesting application; only occasionally produces 'pleasing' sounding melodies, although I
am currently updating the heuristics and rewards to increase these odds.

## Modules
* Python3
* [python-midi](https://github.com/vishnubob/python-midi) - python3 branch

## Execution
Can be ran with <pre>python midigene.py</pre>
This is the same as running with arguments:
    <pre>python midigene.py -note=C -scale=major -bpm=120 -pop_size=1000 -epochs=50000 -mut_rate=0.15 -instrument=0 -bass=true -drums=true</pre>
    
Alternatively, remote execution of this program can be found on my website, which allows for easy setting of the parameters. You can access that [here](https://liqmix.github.io/midi-genes).

## Parameters
* Epoch, population size, and mutation rate are currently set in midigene.py
* Fitness rewards are set in Fitness.py
* BPM and Key are set in Parameters.py

## Instruments
Instrument values are based on the General MIDI standard and the list of acceptable values can be found [here](https://en.wikipedia.org/wiki/General_MIDI#Program_change_events).\
If not provided, the program defaults to using the 'Acoustic Grand Piano' for the melody.

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
* Add rhythm focused heuristics
* Add less naive fitness heuristics
