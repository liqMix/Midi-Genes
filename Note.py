import random as rand
from midigene import PARAMS

# Each note is
#         name                desc                         range
#      start tick     the tick the note begins at         0 - inf
#      duration       how many ticks the note lasts       0 - inf
#      pitch          what the note's sound is            0 - 127
#      velocity       how hard the note is played         0 - 127
#
#             There are 12 notes in total
#        C  C#  D  D#  E  F  F#  G  G#  A  A#  B
# pitch  0  1   2  3   4  5  6   7  8   9  10  11
#
#        These repeat until the max value of 127 (which happens to be a G)
#        Each repetition is called an Octave, with 0-11 being octave 1,
#        12-23 octave 2, etc...
#
#        You can get the note name by using:
#           midi.NOTE_NAMES[note.pitch % midi.OCTAVE_MAX_VALUE]
#        where note.pitch is the note you want the name of
class Note:
    def __init__(self, start=0, duration=0, pitch=0, velocity=100):
        self.start = start
        self.duration = duration
        self.pitch = pitch
        self.velocity = velocity

    def __lt__(self, other):
        return self.start < other.start

    def __repr__(self):
        return "Note(start=%r, duration=%r, pitch=%r, velocity=%r)" % \
               (self.start, self.duration, self.pitch, self.velocity)

    # Creates a random note
    def random(self, start=0):
        self.start = start
        self.pitch = rand.randrange(PARAMS.PITCH_MIN, PARAMS.PITCH_MAX)
        self.duration = PARAMS.NOTE_DURATION[rand.choice(list(PARAMS.NOTE_DURATION))]
        self.velocity = 100
