# phrase_structure_rules.py
#
#   File providing the logic for the higher-order phrase structure rules

# harmonic structure: do all of the harmonies make sense within the context of the key?

# phrase structure: do the harmonies progress towards a sensible cadence?

# harmonic rhythm: do we change chords at a sensible rate? 
#   ---consider using the music21 analysis functions to do this.

from music21 import *

class PhraseStructureRules:
    
    harmonic_intervals_stream = []
    harmonic_generic_intervals_stream = []
    melodic_intervals_stream = []
    melodic_generic_intervals_stream = []
    motion_type_list = []
    cpt = []
    cf = []
    mykey = []
    myscale = []
    
    def __init__(self, harmonic_intervals_stream, harmonic_generic_intervals_stream, melodic_intervals_stream, melodic_generic_intervals_stream, motion_type_list, cpt, cf, mykey):
        self.melodic_intervals_stream = melodic_intervals_stream
        self.melodic_generic_intervals_stream = melodic_generic_intervals_stream
        self.motion_type_list = motion_type_list
        self.harmonic_intervals_stream = harmonic_intervals_stream
        self.harmonic_generic_intervals_stream = harmonic_generic_intervals_stream
        self.cpt = cpt
        self.cf = cf
        self.mykey = mykey
        self.myscale = scale.MajorScale(mykey)
    
    # Give preference to first-species counterpoint shapes that are unimodal (approximately). Give second preference to ones
    #    that don't really have any mode, but ascend or descend in a straight line. Give third preference to polymodal melodies.
    #    Here mode is used in the mathematical/statistical sense.
    def isUnimodal(self):
        #First, convert all of the notes into a list of integers:
        cf_integer_list = []
        for i in range(len(self.cf)):
            this_note = self.cf.flat[i]
            this_scale_degree = self.myscale.getScaleDegreeFromPitch(this_note)
            if i == 0:
                # If this is the first one, uncritically use it as the zero point.
                cf_integer_list.append(this_scale_degree)
            else:
                last_note = self.cf.flat[i-1]
                last_scale_degree = self.myscale.getScaleDegreeFromPitch(last_note)
                # Now figure out which octave our number should be in.
                octaves_up_or_down = getNumOctavesApart(this_note, last_note)
                this_number = getScaleDegreeAwayFromReference(last_scale_degree, this_scale_degree, octaves_up_or_down)
                cf_integer_list.append(this_number)
        # End the for loop
        print(cf_integer_list)
        return(cf_integer_list)
               
    # Give preference to melodies that maintain a good balance between leap, skip, and step.
    def preferVarietyandUnity(self):
        pass
    
    #Penalize repetition of the same note: three times within a six-measure moving frame gets a small penalty, four times a large penality.
    # Note that this implementation could easily penalize multiple times for the sam repetitious cluster - decide if this is 
    #    desirable or not.
    def avoidTooMuchNoteUse(self):
        pass
    
    def masterEvaluateFirstSpecies(self):
        pass
    
#Helper function not actually in the class:
#octaves_up_or_down = 0 implies that we should be a unison
#octaves_up_or_down = 1 implies that we should be above the reference degree number, but by no more than 8.
#octaves_up_or_down = 1 implies that we should be above the reference degree number, but by no less than 8.
#octaves_up_or_down = 2 implies that we should be above the reference degree number, by between 9 and 15. 
#etc.
def getScaleDegreeAwayFromReference(reference_number, new_number_mod_octave, octaves_up_or_down):
    if abs(octaves_up_or_down) > 7:
        print("that's ridiculous number of octaves - exiting program")
        exit(1)
    
    if octaves_up_or_down == 0:
        return(reference_number)
    
    #Generate 10 numbers going up, 10 going down: should be amply sufficient.
    possible_numbers = []
    possible_numbers.append(new_number_mod_octave)
    current_upper_num = new_number_mod_octave
    current_lower_num = new_number_mod_octave
    for i in range(1,11):
        #Get the number this far up
        current_upper_num = current_upper_num + 7
        possible_numbers.append(current_upper_num)
        #Get the number this far down
        current_lower_num = current_lower_num - 7
        possible_numbers.append(current_lower_num)
       
    possible_numbers.sort()

    # Now, search the list for the number that satisfies the octave requirement:
    for i in range(len(possible_numbers)):
        current_num = possible_numbers[i]
        # See if the current trial solution satisfies the requirement:
        difference = current_num - reference_number
        #test for correct octave distance, correct sign:
        if octaves_up_or_down > 0:
            crit1 = (difference > 0)
        else:
            crit1 = (difference < 0)
            
        # Fence/fenceposts: a difference of 7 is actually octave equivalence
        upper_allowable_diff_range = 7*octaves_up_or_down 
        lower_allowable_diff_range = 1 + 7*(octaves_up_or_down-1)   
        crit2 = ((abs(difference) < upper_allowable_diff_range) and (abs(difference) > lower_allowable_diff_range))
        if crit1 and crit2:
            return(current_num)
            #breaks the loop, terminates function
        else:
            pass
            #go back to the beginning and try a new index
    
    # We should have returned by now; If we haven't, throw an error.
    print("Function getScaleDegreeAwayFromReference failed to find a number satisfying the desired properties")
    exit(2) 
# End the helper function.   
    
#of the first note relative to the second note:    
def getNumOctavesApart(note1, note2):
    if note1.pitch == note2.pitch:
        return(0)    
    elif note1.pitch > note2.pitch:
        current_transposition_level = 1
        note2.pitch.transpose('P8')
        print('Entering the first while loop')
        print('here is the note 1 pitch')
        print(note1.pitch)
        while note1.pitch > note2.pitch:
            current_transposition_level = current_transposition_level + 1
            note2.pitch.transpose('P8', inPlace = True)
            print(note2.pitch)
        print('Exiting the first while loop')
        return(current_transposition_level)  
    elif note1.pitch < note2.pitch:
        current_transposition_level = -1
        note2.transpose('P-8', inPlace = True)
        print('Entering the first while loop')
        while note1.pitch < note2.pitch:
            current_transposition_level = current_transposition_level - 1
            note2.pitch.transpose('P-8')
        print('Exiting the first while loop')
        return(current_transposition_level)
    