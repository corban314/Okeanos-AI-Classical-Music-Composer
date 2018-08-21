'''
Created on Apr 16, 2018
build_scores.py
Module for building first species counterpoint scores just from intervalic input.
@author: nathanaelkazmierczak
'''

from music21 import *


# Method for retrieving the Fux ionian score often used as a testing device:
def getFuxIonianFirstSpecies():
    cf_scale_degrees = [1, 3, 4, 5, 3, 6, 5, 3, 4, 3, 2, 1]
    cpt_scale_degrees = [5, 5, 4, 3, 1, 1, 3, 5, 6, 8, 7, 8]
    fux_ionian_score = buildFirstSpeciesScore('c', cf_scale_degrees, cpt_scale_degrees, 1) 
    return(fux_ionian_score)
# End function

# Returns a tuple with ten example counterpoints that I have written to the Fux ionian CF
def getMultipleFuxIonianFirstSpecies():
    score_list = []
    cf_scale_degrees = [1, 3, 4, 5, 3, 6, 5, 3, 4, 3, 2, 1]
    cpt_scale_degrees_list = [
        [12, 12, 11, 10, 8, 8, 10, 12, 13, 15, 14, 15],
        [10,12,11,10,12,13,14,15,9,8,7,8],
        [8,8,6,7,8,8,7,8,9,8,7,8],
        [8,12,9,10,8,8,7,8,6,5,7,8],
        [8,5,6,7,8,8,10,12,11,12,14,15],
        [3,8,6,7,8,11,10,12,11,14,14,15],
        [5,5,8,7,8,6,7,8,9,8,7,8],
        [3,5,6,7,8,8,10,12,13,12,14,15],
        [12,15,13,12,12,11,10,8,9,8,7,8],
        [8,5,6,7,8,8,10,8,6,5,7,8]
        ]
    
    for i in range(len(cpt_scale_degrees_list)):
        score_list.append(buildFirstSpeciesScore('c', cf_scale_degrees, cpt_scale_degrees_list[i], octaveup = 0))
    
    return(score_list)
        
def getFuxNo3inF():
    cf_scale_degrees = [1, 2, 3, 1, -1, 0, 1, 5, 3, 1, 2, 1]
    cpt_scale_degrees = [8,7,5,6,4,5,6,7,8,10,7,8]
    fux_ionian_score = buildFirstSpeciesScore('f', cf_scale_degrees, cpt_scale_degrees, 0) 
    return(fux_ionian_score)

# Method for building the first species score from given intervals.
# An example for key is as follows: 'c'
def buildFirstSpeciesScore(key, cf_scale_degrees, cpt_scale_degrees, octaveup):
    myscore = stream.Score()
    assert(len(cf_scale_degrees) == len(cpt_scale_degrees))
    mylength = len(cf_scale_degrees)
    cpt = stream.Part()
    cf = stream.Part()
    this_scale = scale.MajorScale(key)
    for i in range(mylength):
        this_cf_pitch = this_scale.pitchFromDegree(cf_scale_degrees[i])
        this_cf_note = note.Note(this_cf_pitch)
       
        
        this_cpt_pitch = this_scale.pitchFromDegree(((cpt_scale_degrees[i]-1) % 7) + 1)#, minPitch = 'C4')
        this_cpt_note = note.Note(this_cpt_pitch)
        if octaveup:
            this_cpt_note = interval.transposeNote(this_cpt_note, 'p8')
        #print(cpt_scale_degrees[i])
        if cpt_scale_degrees[i] >= 8:
            # Then we want a second octave transposition to line everything up correctly
            #print('entered')
            #print(this_cpt_note.nameWithOctave)
            this_cpt_note = interval.transposeNote(this_cpt_note, 'p8')
            #print(this_cpt_note.nameWithOctave)
        elif cpt_scale_degrees[i] < 1:
            this_cpt_note = interval.transposeNote(this_cpt_note, 'p-8') 
        if cf_scale_degrees[i] >= 8:
            this_cf_note = interval.transposeNote(this_cf_note, 'p8')
        elif cf_scale_degrees[i] < 1:
            this_cf_note = interval.transposeNote(this_cf_note, 'p-8')
        if cpt_scale_degrees[i] >= 15:
            this_cpt_note = interval.transposeNote(this_cpt_note, 'p8')
        elif cpt_scale_degrees[i] < -6:
            this_cpt_note = interval.transposeNote(this_cpt_note, 'p-8') 
        if cf_scale_degrees[i] > 15: 
            this_cf_note = interval.transposeNote(this_cf_note, 'p8')
        elif cf_scale_degrees[i] < -6: 
            this_cf_note = interval.transposeNote(this_cf_note, 'p-8')
        # End if block
        this_cf_measure = stream.Measure()
        this_cf_measure.append(this_cf_note)
        this_cpt_measure = stream.Measure()
        #print(this_cpt_note.nameWithOctave)
        this_cpt_measure.append(this_cpt_note)
        cpt.append(this_cpt_measure)
        cf.append(this_cf_measure)
    # End for loop
    
    myscore.append(cpt)
    myscore.append(cf)
    return(myscore)
# End functions


if __name__ == '__main__':
#     thisscore = getMultipleFuxIonianFirstSpecies()
#     for i in range(10):
#         thisscore[i].show()
#     thisscore = getFuxNo3inF()
#     thisscore.show()
    pass
# end main code

