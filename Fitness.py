from Track import *


def calc_fitness(track):
    fit = key_fitness(track)
    fit += rule_one(track)
    fit += rule_two(track)
    fit += rule_three(track)
    fit += rule_four(track)
    return fit


# calculates fitness of track based on notes falling within key
def key_fitness(track):
    fit = 0
    for n in track.notes:
        if midi.NOTE_NAMES[(n.pitch % midi.NOTE_PER_OCTAVE)] in PARAMS.NOTES_IN_KEY:
            fit += 200
        else:
            fit -= 100
    return fit


# This rule rewards starting and ending notes
def rule_one(track):
    fit = 0
    starting_note = midi.NOTE_NAMES[(track.notes[0].pitch % midi.NOTE_PER_OCTAVE)]
    # Start note
    if (starting_note is PARAMS.NOTES_IN_KEY[0]) or \
            (starting_note is PARAMS.NOTES_IN_KEY[4]):
        fit += 200

    # End note
    if (midi.NOTE_NAMES[(track.notes[-1].pitch % midi.NOTE_PER_OCTAVE)]
            != PARAMS.NOTES_IN_KEY[0]):
        fit -= 100
    else:
        fit += 200

    return fit


# This rule penalizes large jumps in pitch
def rule_two(track):
    fit = 0
    for i in range(len(track.notes)):
        if i != 0:
            dist = abs(track.notes[i].pitch - track.notes[i - 1].pitch)
            if dist != 2:
                fit -= dist * 5
    return fit


# This rule rewards jumps in pitch if followed by reverse movement
def rule_three(track):
    fit = 0
    for i in range(len(track.notes)):
        if i != 0 and i != (len(track.notes) - 1):
            if ((track.notes[i].pitch - track.notes[i - 1].pitch)
                    >= 3):
                if track.notes[i + 1].pitch - track.notes[i].pitch < 0:
                    fit += 50
                else:
                    fit -= 100

            elif (track.notes[i].pitch - track.notes[i - 1].pitch) <= -3:
                if track.notes[i + 1].pitch - track.notes[i].pitch > 0:
                    fit += 50
                else:
                    fit -= 100

    return fit


# This rule penalizes a tritone jump
def rule_four(track):
    fit = 0
    for i in range(len(track.notes)):
        if i != (len(track.notes) - 1):
            first_note = midi.NOTE_NAMES[(track.notes[i].pitch % midi.NOTE_PER_OCTAVE)]
            second_note = midi.NOTE_NAMES[(track.notes[i + 1].pitch % midi.NOTE_PER_OCTAVE)]
            if (((first_note == PARAMS.NOTES_IN_KEY[3]) and (second_note == PARAMS.NOTES_IN_KEY[6]))
                    or ((first_note == PARAMS.NOTES_IN_KEY[6]) and (second_note == PARAMS.NOTES_IN_KEY[3]))):
                fit -= 250

    return fit
