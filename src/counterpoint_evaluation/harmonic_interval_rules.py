# harmonic_interval_rules.py
#
#   File containing all of the logic to evaluate the counterpoint's vertical structure.

from __future__ import division  # To get Python 2 to do floating point division properly
from music21 import *
from evaluation_score import *

class HarmonicIntervalRules:
    # Instance variables:
    harmonic_intervals_stream = []
    harmonic_generic_intervals_stream = []
    length = 0
    num_body_perfect_consonances = 0
    num_body_imperfect_consonances = 0
    
    def __init__(self, harmonic_intervals_stream, harmonic_generic_intervals_stream):
        self.harmonic_intervals_stream = harmonic_intervals_stream
        self.harmonic_generic_intervals_stream = harmonic_generic_intervals_stream
        self.length = len(harmonic_intervals_stream)
    #End constructor

# Check for consonance (Steele rule 1)
# Return an integer giving the number of times the consonance rule has been violated.
    def checkConsonances(self):
        rule_violations = 0
        violation_locations = []
        for i in range(self.length):
            if self.harmonic_intervals_stream[i].isConsonant():
                pass
            else:
                rule_violations = rule_violations + 1
                violation_locations.append(i)
        # End for loop        
        return((rule_violations, violation_locations))
        
# Assign perfect vs. imperfect consonance (Steele rule 4)
# Note that we only want to assign the body of the counterpoint here.
    def assignConsonances(self):
        num_perfect = 0
        num_imperfect = 0
#         perfect_consonances_list = ['P1','P5','P8']
#         imperfect_consonances_list = ['m3','M3','m6','M6']
#         for i in range(1, self.length - 1):
#             if self.harmonic_intervals_stream[i].isConsonant():
#                 n = self.harmonic_intervals_stream[i].semiSimpleName
#                 if n in perfect_consonances_list:
#                     num_perfect = num_perfect + 1
#                 elif n in imperfect_consonances_list:
#                     num_imperfect = num_imperfect + 1
#                 else: # This shouldn't happen
#                     exit(1)

        for i in range(1, self.length - 1):
            if isPerfectConsonance(self.harmonic_intervals_stream[i]):
                num_perfect = num_perfect + 1
            elif isImperfectConsonance(self.harmonic_intervals_stream[i]):
                num_imperfect = num_imperfect + 1
        # End for loop
        self.num_body_perfect_consonances = num_perfect
        self.num_body_imperfect_consonances = num_imperfect
        # There isn't a return on this method
    # End method

# Score ratio of perfect / imperfect consonances (Steele rule 4 -- part 2)
# Deal with weighting the ratio in the evaluation module.
# Note that we use the ratio of perfect consonances to total because more perfect consonances are generally worse
# We will seek to minimize the fitness function metric.
    def scoreConsonanceRatio(self):
        self.assignConsonances()
        total_body_cons = self.num_body_perfect_consonances + self.num_body_imperfect_consonances
        ratio = self.num_body_perfect_consonances / total_body_cons
        return(ratio)
        
# The beginning and end of the counterpoint must consist of perfect consonances (Steele rule 4 -- part 3)
# Return 1 if one rule is violated; return 2 if two rules are violated
# TO-DO: we might not actually want to require this for some styles (just demand consonance?)
    def checkEndBeginning(self):
        violations = 0
        violation_locations = []
        if isPerfectConsonance(self.harmonic_intervals_stream[0]):
            pass
        elif isImperfectConsonance(self.harmonic_intervals_stream[0]):
            pass
        else:
            violations = violations + 1
            violation_locations.append(0)
            
        # This should be the final element:    
        if isPerfectConsonance(self.harmonic_intervals_stream[self.length - 1]):
            pass
        else:
            violations = violations + 1
            violation_locations.append(self.length-1)
            
        return(violations, violation_locations)
    
    # Penultimate bar must contain major sixth (c.f. upper part) or minor third (c.f. lower part)
#    (Steele rule 5)
    def checkCadence(self):
        penultimate_interval = self.harmonic_intervals_stream[self.length - 2]
        allowable_intervals = ['m3','M6']  # Should automatically be the ascending interval by construction
        if not(penultimate_interval.semiSimpleName in allowable_intervals):
            #print('This is the self length:%d' % self.length) 
            return(1,[self.length - 2])  # The error here is really associated with the second to last note.
        else:
            return(0,[])
    
# Tritone is the devil in music (Steele rule 9)
# Note that this will also get flagged under dissonance -- really here we are just adding extra weight to the violation.
# NOTE: when we go to do harmonic counterpoint, this rule should be eliminated.
#    TO-DO: Try to come up with a scheme for flagging this as a candidate for an accidental.
    def checkTritones(self):
        violations = 0
        violation_locations = []
        for i in range(self.length):
            if isTritone(self.harmonic_intervals_stream[i]):
                violations = violations + 1
                violation_locations.append(i)
        # end for loop
        return(violations, violation_locations)  
        
# Prohibition against unisons except at beginning and end. (Steele rule 11)
    def checkUnisons(self):
        violations = 0
        violation_locations = []
        for i in range(1, self.length - 1):
            if isUnison(self.harmonic_intervals_stream[i]):
                violations = violations + 1
                violation_locations.append(i)
        # end for loop
        return(violations, violation_locations)  
    
# Parallel perfect consonances are prohibited (Steele rule 8 --  part 2)
# Really we don't care whether these are the same parallel consonance 
    # or not; it's all a violation.
    def checkParallelPerfectConsonances(self):
        violations = 0
        violation_locations = []
        # Count these violations as imputing to both notes:
        #    depending on the situation, it might make more sense to move either of the two notes.
        for i in range(self.length - 1):
            if isPerfectConsonance(self.harmonic_intervals_stream[i]):
                if isPerfectConsonance(self.harmonic_intervals_stream[i+1]):
                    violations = violations + 1
                    violation_locations.append(i)
                    violation_locations.append(i+1)
        # End for loop
        return(violations, violation_locations)
    
# Master method for evaluating all of the above rules, returning results as a list:
    def masterEvaluate(self):
        evaluation_list = []
        locations_list = []
        cc = self.checkConsonances()
        evaluation_list.append(cc[0])
        locations_list.append(cc[1])
        scr = self.scoreConsonanceRatio()
        evaluation_list.append(scr)
        locations_list.append([])
        ceb = self.checkEndBeginning()
        evaluation_list.append(ceb[0])
        locations_list.append(ceb[1])
        cc2 = self.checkCadence()
        evaluation_list.append(cc2[0])
        locations_list.append(cc2[1])
        ct = self.checkTritones()
        evaluation_list.append(ct[0])
        locations_list.append(ct[1])
        cu = self.checkUnisons()
        evaluation_list.append(cu[0])
        locations_list.append(cu[1])
        cppc = self.checkParallelPerfectConsonances()
        evaluation_list.append(cppc[0])
        locations_list.append(cppc[1])
        return(evaluation_list, locations_list)



###
###
###
### These are factored - out functions
def isPerfectConsonance(interval):
    perfect_consonances_list = ['P1','P5','P8']
    n = interval.semiSimpleName
    if interval.isConsonant():
        if n in perfect_consonances_list:
            return(1)
        else:
            return(0)
    else:
        return(0)
                    
def isImperfectConsonance(interval):
    imperfect_consonances_list = ['m3','M3','m6','M6']
    n = interval.semiSimpleName
    if interval.isConsonant():
        if n in imperfect_consonances_list:
            return(1)
        else:
            return(0)
    else:
        return(0)

def isTritone(interval):
    tritone_list = ['d5', 'A4']
    n = interval.semiSimpleName
    if n in tritone_list:
        return(1)
    else:
        return(0)
    
def isUnison(interval):
    unison_nice_names = ['Perfect Unison', 'Diminished Unison', 'Augmented Unison']
    n = interval.niceName
    if n in unison_nice_names:
        return(1)
    else:
        return(0)
    
# This method is actually imported into the melodic intervals module, used for testing
#    for skips to octaves.
def isOctave(interval):
    octave_nice_names = ['Perfect Octave', 'Diminished Octave', 'Augmented Octave']
    n = interval.niceName
    if n in octave_nice_names:
        return(1)
    else:
        return(0)
    
    