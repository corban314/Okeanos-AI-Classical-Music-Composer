# evaluation_score.py
#
#   file providing the methods for scoring a section of counterpoint according to different weights on the rules.

# def basic_function(parameter):
#     print(parameter)
#     thisval = 42
#     return(thisval)

from music21 import *
from harmonic_interval_rules import *
from melodic_interval_rules import *
from random import randint
from counterpoint_evaluation.phrase_structure_rules import PhraseStructureRules

class Evaluator:
    key = []
    cpt_part = []
    cf_part = []
    # The various types of interval streams we may need:
    mi_stream = []
    gmi_stream = []
    hi_stream = []
    ghi_stream = []
    # The motion list:
    mt_list = []
    # The harmonic, melodic, phrase rule objects:
    hir = []
    mir = []
    psr = []
    # The results from the harmonic, melodic, phrase rule evaluations:
    hir_locations = []
    mir_locations = []
    psr_locations = []
    
    def __init__(self, which_is_cpt_part, mykey, part1 = 0, part2 = 0, myscore = 0):
        if myscore != 0:
            part1 = myscore[0]
            part2 = myscore[1]
        # end
        # Currently we assume that we have a two-part, first species counterpoint.
        if which_is_cpt_part == 1:
            self.cpt_part = part1
            self.cf_part = part2
        else:
            self.cpt_part = part2
            self.cf_part = part1
        
        # Rule
        self.key = mykey
        self.mi_stream = obtain_melodic_intervals(self.cpt_part)
        self.gmi_stream = obtain_generic_melodic_intervals(self.cpt_part)
        self.hi_stream = obtain_harmonic_intervals(part1, part2)
        self.ghi_stream = obtain_generic_harmonic_intervals(part1, part2)
        self.mt_list = obtain_motion_type(part1, part2)
        self.hir = HarmonicIntervalRules(self.hi_stream, self.ghi_stream)
        self.mir = MelodicIntervalRules(self.mi_stream, self.gmi_stream, self.mt_list, self.hi_stream)
        self.psr = PhraseStructureRules(self.hi_stream, self.ghi_stream, self.mi_stream, self.gmi_stream, self.mt_list, self.cpt_part, self.cf_part, mykey)
    # End constructor
    
    def getRulesInstances(self):
        mytuple = (self.hir, self.mir, self.mi_stream, self.hi_stream, self.mt_list)
        return(mytuple)
    
    # The first shot at a fitness function for the first species counterpoint examples
    #    Observe from the testing results in the counterpoint_evaluation module that
    #    we may need to downweight the importance of jump preparation and compensation.
    def firstSpeciesEvaluation(self, harmonic_weighting_scheme = 'unweighted', melodic_weighting_scheme = 'unweighted'):
        fitness = 0
        
        # Under the default weighting scheme, all rule violations are treated as equal.
        # The ratios are not scaled at all.
        if harmonic_weighting_scheme == 'unweighted':
            hweights = [1,1,1,1,1,1,1]
        elif harmonic_weighting_scheme == 'consonance rectified':
            hweights = [4,3,1,1,1,1,2]
        # Rules for harmonic weights, in order: 
        # (1)    checkConsonances
        # (2)    scoreConsonanceRatio
        # (3)    checkEndBeginning
        # (4)    checkCadence
        # (5)    checkTritones
        # (6)    checkUnisons
        # (7)    checkParallelPerfectConsonances
        
        if melodic_weighting_scheme == 'unweighted':
            mweights = [1,1,1,1,1,1,1,1,1]
        elif melodic_weighting_scheme == 'repetition rectified':
            mweights = [1,1,1,0.5,1,1,4,1,1]
        # Rules for melodic weights, in order:
        # (1)    scoreMotionTypes
        # (2)    avoidAwkwardIntervals
        # (3)    avoidLargeDissonantLeaps
        # (4)    avoidSuccessiveSkips
        # (5)    preferJumpPreparation
        # (6)    preferJumpFollowingCompensation
        # (7)    checkToneRepetition
        # (8)    guardMotionToPerfectConsonances
        # (9)    guardMotionToOctave
        
        rule_results_list = []
        # Evaluate all of the harmonic interval rules:
        hir_tuple = self.hir.masterEvaluate()
        hir_evaluation = hir_tuple[0]
        self.hir_locations = hir_tuple[1]
        hir_component = listDotProduct(hir_evaluation,hweights)
        # Evaluate all of the melodic interval rules:
        mir_evaluation = self.mir.masterEvaluate()
        mir_component = listDotProduct(mir_evaluation,mweights)
        # Evaluate all of the phrase structure rules:
#         psr_evaluation = []
        # Obtain the unweighted fitness (Python list concatenation):
#         rule_results_list = hir_evaluation + mir_evaluation + psr_evaluation
        rule_results_list = [hir_component, mir_component]
        fitness = sum(rule_results_list)
        return(fitness)
    # End the main First Species evaluation method.    
    
    # On the basis of the harmonic evaluation, this will look for the locations of 
    #    dissonance, identify allowable consonances, and randomly sample them.
    #    Gives one new score per counterpoint generation
    def improveCounterpointConsonances(self):
        new_cpt_part = self.cpt_part
        dissonance_locations = self.hir_locations[0]
        myscale = scale.MajorScale(self.key)
        for i in dissonance_locations:
            cf_degree = myscale.getScaleDegreeFromPitch(self.cf_part.flat[i])
            cpt_current_degree = myscale.getScaleDegreeFromPitch(self.cpt_part.flat[i])
            new_possibilities_tuple = getConsonantScaleDegrees(cf_degree, cpt_current_degree, myrange = 6)
#             print(new_possibilities)
            higher_or_lower = new_possibilities_tuple[1]
            pitchvals = new_possibilities_tuple[0]
            randchoice = randint(0, len(pitchvals) - 1)
            new_cpt_degree = pitchvals[randchoice]
            new_cpt_pitch = myscale.pitchFromDegree(new_cpt_degree)
            old_pitch = new_cpt_part.flat[i].pitch
            # Trying to correct wacky octave problems.
            #print('fixing an octave')
            new_cpt_tranposed_pitch = getCorrectOctave(new_cpt_pitch, old_pitch)
            #print(new_cpt_tranposed_pitch)
            new_cpt_part.flat[i].pitch = new_cpt_tranposed_pitch
#             thismeasure = stream.Measure()
#             thismeasure.append(new_cpt_note)
#             new_cpt_part[i] = thismeasure
        # End for loop
        
        newscore = stream.Score()
        newscore.append(new_cpt_part)
        newscore.append(self.cf_part)
        return(newscore)
            ########TODO - INSERT THIS NOTE INTO THE APPROPRIATE PLACE IN THE NEW COUNTERPOINT STREAM
            #RETURN THE STREAM AND SCORE AS A NEW CANDIDATE
            #SEE HOW WELL THEY DO UNDER EVALUATION - SHOULD BE BETTER THAN RANDOM SAMPLING.
            
    def invokePhraseStructure(self):
        result = self.psr.isUnimodal()
        return(result)
### END EVALUATOR CLASS
### Factored - out functions:

# Given a part, obtain a stream containing all of the melodic intervals
def obtain_melodic_intervals(mypart):
    melodic_intervals_stream = stream.Stream()
    # Really we want to obtain the number of notes contained in one of the parts.
#     part_1 = myscore[0]
    part_length = len(mypart.flat.getElementsByClass(note.Note))
#     print(score_length)
    # There are one fewer intervals than notes:
    for i in range(part_length-1):
        first_note = mypart.flat[i]
        next_note = mypart.flat[i+1]
        this_interval = interval.notesToInterval(first_note, next_note)
        melodic_intervals_stream.append(this_interval)
    # End for loop
#     melodic_intervals_stream.show('text')
    return(melodic_intervals_stream)


# Given a part, obtain a stream containing all of the melodic generic intervals
def obtain_generic_melodic_intervals(mypart):
    melodic_generic_intervals_stream = stream.Stream()
    # Really we want to obtain the number of notes contained in one of the parts.
#     part_1 = myscore[0]
    part_length = len(mypart.flat.getElementsByClass(note.Note))
#     print(score_length)
    # There are one fewer intervals than notes:
    for i in range(part_length-1):
        first_note = mypart.flat[i]
        next_note = mypart.flat[i+1]
        this_interval = interval.notesToGeneric(first_note, next_note)
        melodic_generic_intervals_stream.append(this_interval)
    # End for loop
#     melodic_generic_intervals_stream.show('text')
    return(melodic_generic_intervals_stream)


# Given two parts, obtain a stream containing all of the harmonic intervals between the two:
# Note that this stream will be longer by one interval than the longest melodic interval. 
def obtain_harmonic_intervals(mypart1, mypart2):
    harmonic_intervals_stream = stream.Stream()
    part1_length = len(mypart1.flat.getElementsByClass(note.Note))
    part2_length = len(mypart2.flat.getElementsByClass(note.Note))
    if part1_length == part2_length:  # All that is supported for now (first species)
        for i in range(part1_length):
            part1_note = mypart1.flat[i]
            part2_note = mypart2.flat[i]
            this_interval = interval.notesToInterval(part1_note, part2_note)
            harmonic_intervals_stream.append(this_interval)
    else:
        pass
    
#     harmonic_intervals_stream.show('text')
    return(harmonic_intervals_stream)

# Given two parts, obtain a stream containing all of the harmonic intervals between the two:
# Note that this stream will be longer by one interval than the longest melodic interval. 
def obtain_generic_harmonic_intervals(mypart1, mypart2):
    harmonic_generic_intervals_stream = stream.Stream()
    part1_length = len(mypart1.flat.getElementsByClass(note.Note))
    part2_length = len(mypart2.flat.getElementsByClass(note.Note))
    if part1_length == part2_length:  # All that is supported for now (first species)
        for i in range(part1_length):
            part1_note = mypart1.flat[i]
            part2_note = mypart2.flat[i]
            this_interval = interval.notesToGeneric(part1_note, part2_note)
            harmonic_generic_intervals_stream.append(this_interval)
    else:
        pass
    
#     harmonic_generic_intervals_stream.show('text')
    return(harmonic_generic_intervals_stream)

# Given two melodic parts, return a list (python-style) of the type of motion
#    Types of motion: parallel (p), contrary (c), similar (s), oblique (o)
#    This function is going to require some overhauls for second species.
def obtain_motion_type(mypart1, mypart2):
    mypart1_generic_melodic_intervals = obtain_generic_melodic_intervals(mypart1)
    mypart2_generic_melodic_intervals = obtain_generic_melodic_intervals(mypart2)
    mypart1_melodic_intervals = obtain_melodic_intervals(mypart1)
    mypart2_melodic_intervals = obtain_melodic_intervals(mypart2)
    part_length = len(mypart1.flat.getElementsByClass(note.Note))
    motion_type_list = list()
    
    for i in range(part_length-1):
        mypart1_direction = mypart1_melodic_intervals[i].direction
        mypart2_direction = mypart2_melodic_intervals[i].direction
        
        if mypart1_direction == mypart2_direction:
            #We have either parallel or similar motion
            #Construct generic intervals from the two:
            
            if mypart1_generic_melodic_intervals[i].niceName == mypart1_generic_melodic_intervals[i].niceName:
                motion_type = 'p'  #Parallel motion
            else:
                motion_type = 's'  #Similar motion
        else:  # We have either oblique or contrary motion
            if (mypart1_direction == 0) or (mypart2_direction == 0):
                motion_type = 'o'  #Oblique motion
            else:
                motion_type = 'c'  #Contrary motion
        #End logic for determining intervals
        motion_type_list.append(motion_type)
    #End for loop
#     
#     # The test to see if this is well defined.
#     print(mypart1_melodic_intervals[0].direction)
#     print(motion_type_list)
    return(motion_type_list)
# End function obtain_motion_type
 
#From stack overflow:    
#https://stackoverflow.com/questions/32669855/dot-product-of-two-lists-in-python
def listDotProduct(list1, list2):
    if len(list1) != len(list2):
        return 0
    return sum(i[0] * i[1] for i in zip(list1, list2))

def getConsonantScaleDegrees(cf_degree, current_degree, myrange = 6):
    consonant_degrees = []
    higher_or_lower = []
    consonant_diffs = [0, 2, 4, 5, 7, 9, 11, 12, 14]
    bottom = current_degree - myrange
    top = current_degree + myrange
#     print(bottom) 
#     print(top)
    for i in range(bottom,top):
        diff = abs(cf_degree - i)
#         print(diff)
        if diff in consonant_diffs:
#             print('in diffs with cf and i:')
#             print(cf_degree)
#             print(i)
#             print('and conds")')
#             print((cf_degree != 7 and i != 11))
#             print((cf_degree != 0 and i != 4))
            if not ((cf_degree == 7 and i == 11) or (cf_degree == 0 and i == 4)):  
                consonant_degrees.append(i)
                if (cf_degree - i) < 0:
                    higher_or_lower.append(1)
                elif (cf_degree - i) == 0:
                    higher_or_lower.append(0)
                else:
                    higher_or_lower.append(-1)
#                 print('appending consonant juice')
                # Otherwise we got a tritone
    return(consonant_degrees, higher_or_lower)
    # End function
    
def getCorrectOctave(newpitch, oldpitch):
    if newpitch < oldpitch:
        current_direction = -1
    elif newpitch > oldpitch:
        current_direction = 1
    else:
        current_direction = 0
        
    if current_direction == -1:
        while True:
            newpitch.octave = newpitch.octave + 1
            if newpitch > oldpitch:
                break
            
        newpitch2 = newpitch
        newpitch2.octave = newpitch2.octave - 1
        cand1 = newpitch 
        cand2 = newpitch2
        # Pick the candidate that gets closer: - this could actually invert a fourth into a fifth e.g. by accident
        interval1 = interval.Interval(oldpitch,cand1)
        interval2 = interval.Interval(cand2,oldpitch)
        if interval1 > interval2:
            return(cand2)
        else:
            return(cand1)
    elif current_direction == 1:
        while True:
            newpitch.octave = newpitch.octave - 1
            if newpitch < oldpitch:
                break
            
        newpitch2 = newpitch
        newpitch2.octave = newpitch2.octave + 1
        cand1 = newpitch2 
        cand2 = newpitch
        # Pick the candidate that gets closer: - this could actually invert a fourth into a fifth e.g. by accident
        interval1 = interval.Interval(oldpitch,cand1)
        interval2 = interval.Interval(cand2,oldpitch)
        if interval1 > interval2:
            return(cand2)
        else:
            return(cand1)
    elif current_direction == 0:
        return(newpitch)
    else:
        assert(False)
# End method
    
    
# # Testing code to make sure the functions are working:   
# if __name__ == '__main__':
#     myparam = 'fourty-two'
#     valreturned = basic_function(myparam)
#     print(valreturned)
    