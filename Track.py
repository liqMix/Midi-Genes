from Fitness import Fitness
from Note import *
import midi

fit = Fitness(PARAMS)
# A track is a container for a list of notes,
# and is effectively a "genome" for our use,
# with the notes list serving as the "alleles"
class Track:
    def __init__(self, notes=[]):
        self.notes = notes
        self.num = 0
        self.fitness = 0

    # Prints each note in the list
    def __repr__(self):
        for note in self.notes:
            print(self.notes.index(note), " ", note)
        return " "

    # Used to sort tracks by fitness
    def __lt__(self, other):
        return self.fitness < other.fitness

    # Outputs the track as a midi.Pattern to be encoded back into a midi file
    # by the midi module
    # 
    # NEEDS an input pattern in order to reattach certain parts
    def output_pattern(self, pattern):
        output = midi.Pattern(resolution=pattern.resolution)

        # pattern[0] is midi meta info for the pattern
        output.append(pattern[0])

        track = midi.Track()

        # pattern[1][0] contains the meta information for that track
        track.append(pattern[1][0])
        # changes instrument to piano
        # TODO: allow user to change the instrument
        track.append(midi.ProgramChangeEvent(tick=0, channel=2, data=[0]))

        # Translates the notes in the track to midi events
        for note in self.notes:
            track.append(midi.NoteOnEvent(tick=note.start, channel=2,
                                          pitch=note.pitch,
                                          velocity=note.velocity))

            track.append(midi.NoteOffEvent(tick=(note.start + note.duration),
                                           channel=2,
                                           pitch=note.pitch,
                                           velocity=100))

        # Attach track end event
        track.append(midi.EndOfTrackEvent(tick=PARAMS.END_TICK))

        # Sets each event's ticks to be relative to the next event
        # Sets each start tick to 0 to ensure no overlapping events
        track.tick_relative = False
        track.make_ticks_rel()
        for e in track:
            if isinstance(e, midi.NoteOnEvent):
                e.tick = 0

        # Appends our track to output
        # pattern[2] and [3] are accompaniment tracks
        output.append(track)
        output.append(pattern[2])
        output.append(pattern[3])
        return output

    # Creates random notes and stores them in the tracks note list
    def random(self, num_of_notes):
        self.notes = []
        self.num = num_of_notes
        temp_note = Note()
        temp_note.random(0)
        self.notes.append(temp_note)

        for x in range(0, self.num - 1):
            temp_note = Note()
            temp_note.random(self.notes[-1].start + self.notes[-1].duration)

            if temp_note.start >= PARAMS.LAST_NOTE:
                temp_note.start = PARAMS.LAST_NOTE
                temp_note.duration = PARAMS.NOTE_DURATION["WHOLE"]

                for n in self.notes:
                    if (n.start + n.duration) >= PARAMS.LAST_NOTE:
                        del n

                self.notes.append(temp_note)
                self.fitness = fit.calc_fitness(self)
                return self.fitness

            self.notes.append(temp_note)

    # Removes notes with same start tick
    def remove_dup(self):
        i = 1

        while i < len(self.notes):
            if (self.notes[i].start == self.notes[i - 1].start) or (self.notes[i].start > PARAMS.LAST_NOTE):
                del self.notes[i]
                i -= 1
            i += 1

    # Restructures the note start times after readjusting the last note
    def normalize(self):
        i = len(self.notes) - 1

        self.notes[i].start = PARAMS.LAST_NOTE
        self.notes[i].duration = PARAMS.NOTE_DURATION["WHOLE"]
        while i > 0:
            self.notes[i - 1].start = self.notes[i].start - self.notes[i - 1].duration
            i -= 1
            if self.notes[i].start <= 0:
                self.notes[i].start = 0
                self.notes[i].duration = self.notes[i + 1].start
                i -= 1
                break

        while i >= 0:
            del self.notes[i]
            i -= 1

