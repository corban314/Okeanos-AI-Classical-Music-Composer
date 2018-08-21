# melodic_interval_rules.py
#
#   File containing all of the logic to evaluate the counterpoint's horizontal motion

from __future__ import division  # To get Python 2 to do floating point division properly
from music21 import *
from evaluation_score import *
from harmonic_interval_rules import isPerfectConsonance, isOctave

class MelodicIntervalRules:
    # Instance variables:
    melodic_intervals_stream = []
    melodic_generic_intervals_stream = []
    harmonic_intervals_stream = []
    motion_type_list = []
    length = 0  # This will be the length of the streams, which is one minus the number
    # of notes within a part.
    contrary_motion_count = 0
    oblique_motion_count = 0
    similar_motion_count = 0
    parallel_motion_count = 0
    
    # Recall that we should only put the counterpoint melodic intervals into the constructor:
    def __init__(self, melodic_intervals_stream, melodic_generic_intervals_stream, motion_type_list, harmonic_intervals_stream):
        self.melodic_intervals_stream = melodic_intervals_stream
        self.melodic_generic_intervals_stream = melodic_generic_intervals_stream
        self.motion_type_list = motion_type_list
        self.harmonic_intervals_stream = harmonic_intervals_stream  # Needed for direct motion test.
        self.length = len(melodic_intervals_stream)
    #End constructor 
    
# Evaluate contrary and oblique motion (Steele rule 2)
    def assignMotionTypes(self):
        cm_count = 0
        om_count = 0
        sm_count = 0
        pm_count = 0
        for i in range(self.length):
            if self.motion_type_list[i] == 'c':
                cm_count = cm_count + 1
            elif self.motion_type_list[i] == 'o':
                om_count = om_count + 1
            elif self.motion_type_list[i] == 's':
                sm_count = sm_count + 1
            elif self.motion_type_list[i] == 'p':
                pm_count = pm_count + 1
            else: # This shouldn't happen
                exit(1)
        # End for loop
        self.contrary_motion_count = cm_count
        self.oblique_motion_count = om_count
        self.similar_motion_count = sm_count
        self.parallel_motion_count = pm_count
    # No return value: end method

# Score contrary/oblique vs. parallel/similar motion (Steele rule 2 -- part 2)
# As a first approximation, take the ratio of contrary / oblique motion to parallel / similar motion
# TO-DO: improve this first approximation.
    def scoreMotionTypes(self):
        self.assignMotionTypes()
        total_count = self.contrary_motion_count + self.oblique_motion_count + self.similar_motion_count + self.parallel_motion_count
        less_ideal_count = self.similar_motion_count + self.parallel_motion_count
        ratio = less_ideal_count / total_count
        return(ratio)

# Avoid augmented, diminished, chromatic intervals (Steele rule 3)
#    Right now this really just avoids augmented and diminisned intervals.
#    We can retain this rule even when allowing harmonic dissonances, because this is melodic.
    def avoidAwkwardIntervals(self):
        violations = 0
        qualities_to_avoid = ['A','d']
        for i in range(self.length):
            quality = self.melodic_intervals_stream[i].diatonic.specifierAbbreviation
            if quality in qualities_to_avoid:
                violations = violations + 1
        # End for loop
        return(violations)

# Avoid melodic intervals larger than a fifth, excepting octave and minor sixth
#   which must only be ascending (Steele rule 3 -- part 2)
#    Modification: For now, let's allow major sixths -- 
#    not clear to me why those should be prohibited
    def avoidLargeDissonantLeaps(self):
        violations = 0
        for i in range(self.length):
            # Test to see if the interval is larger than a fifth
            if self.melodic_generic_intervals_stream[i].undirected > 5:
                # if so, then is it a sixth or an octave?
                if self.melodic_generic_intervals_stream[i].undirected in [6, 8]:
                    if self.melodic_generic_intervals_stream[i].directed < 0:
                        violations = violations + 1   # If so, penalize only if descending
                    else:
                        pass # An ascending interval is fine
                else:  # If not, penalize.
                    violations = violations + 1
        # End for loop
        return(violations)
    
# Avoid skips following each other in the same direction (Steele rule 3 -- part 3)
    def avoidSuccessiveSkips(self):
        violations = 0
        for i in range(self.length - 1):  # Because now we are taking pairs of intervals
            this_interval = self.melodic_generic_intervals_stream[i]
            next_interval = self.melodic_generic_intervals_stream[i+1]
            if (this_interval.directed == 3) and (this_interval.directed == next_interval.directed):
                violations = violations + 1
        # End for loop
        return(violations)

# Prefer skips and leaps that are prepared with stepwise motion in the compensating DIRECTION
#   (Steele rule 3 -- part 4),
#    Don't penalize a jump on the first interval for now -- no chance to prepare it. 
#    You could make an argument for penalizing this on the grounds of disjoint motion.
#    Currently, we are really testing two rules here.
    def preferJumpPreparation(self):
        violations = 0
        for i in range(1, self.length): # So there will always be a preceding interval
            this_interval = self.melodic_generic_intervals_stream[i]
            if this_interval.undirected > 2:  # We have a leap or a skip
                last_interval = self.melodic_generic_intervals_stream[i-1]
                if last_interval.undirected != 2:  # Failure to prepare with stepwise motion
                    violations = violations + 1
                if last_interval.directed * this_interval.directed > 0:
                    violations = violations + 1  # In this case, the directions are the same.
        # End for loop
        return(violations)
    
# Prefer skips and leaps that are followed with stepwise motion in the compensating DIRECTION
#   (Steele rule 3 -- part 5)
    def preferJumpFollowingCompensation(self):
        violations = 0
        for i in range(0, self.length - 1):
            this_interval = self.melodic_generic_intervals_stream[i]
            if this_interval.undirected > 2:  # We have a leap or a skip
                next_interval = self.melodic_generic_intervals_stream[i+1]
                if next_interval.undirected != 2:  # Failure to prepare with stepwise motion
                    violations = violations + 1
                if next_interval.directed * this_interval.directed > 0:
                    violations = violations + 1  # In this case, the directions are the same.
        # End for loop
        return(violations)

### Note: Steele rule 5 may still be applicable here, as we can mark the chromatic alteration.
### But for now, take care of this in the harmonic intervals module.
 # Penultimate bar must contain major sixth (c.f. upper part) or minor third (c.f. lower part)
#    (Steele rule 5)
        
# Repetition of the same tone in counterpoint should not be used more than once. (Steele rule 6)
#    Under this first simple implementation, this just prohibits successive oblique motion.
    def checkToneRepetition(self):
        violations = 0
        for i in range(self.length - 1):
            if self.motion_type_list[i] == 'o':
                if self.motion_type_list[i+1] == 'o':
                    violations = violations + 1
        # End for loop
        return(violations)
    
# The counterpoint must be in the same mode as the cantus firmus (Steele rule 7)
#   This may prove very hard to implement -- put off for later?

# Do not approach a perfect consonance by direct motion (Steele rule 8)
#    TO-DO: This will need to be overhauled to get an appropriate spatial correspondence
#    between the harmonic and the melodic intervals.
    def guardMotionToPerfectConsonance(self):
        violations = 0
        forbidden_motions = ['s','p']
        harmonic_length = len(self.harmonic_intervals_stream)
        for i in range(1, harmonic_length):
            if isPerfectConsonance(self.harmonic_intervals_stream[i]):
                melodic_index = i - 1
                # Note that for first species, the melodic index is one minus because we want 
                # the interval that comes just before the perfect consonance.
                if self.motion_type_list[melodic_index] in forbidden_motions:
                    violations = violations + 1
        # End for loop
        return(violations)

# Octaves should not be approached by skip. (Steele rule 12)
#    TO-DO: note that this is only a partial fix, because we won't actually be testing 
#    whether the cantus firmus skips into the octave or not. Really we should, because 
#    then this will act as a deterrent to putting an octave consonance at all at that position.
    def guardMotionToOctave(self):
        violations = 0
        harmonic_length = len(self.harmonic_intervals_stream)
        for i in range(1, harmonic_length):
            if isOctave(self.harmonic_intervals_stream[i]):
                melodic_index = i - 1
                if self.melodic_generic_intervals_stream[melodic_index].undirected == 3:
                    violations = violations + 1
        # End for loop
        return(violations)
    
    def masterEvaluate(self):
        evaluation_list = []
        evaluation_list.append(self.scoreMotionTypes())
        evaluation_list.append(self.avoidAwkwardIntervals())
        evaluation_list.append(self.avoidLargeDissonantLeaps())
        evaluation_list.append(self.avoidSuccessiveSkips())
        evaluation_list.append(self.preferJumpPreparation())
        evaluation_list.append(self.preferJumpFollowingCompensation())
        evaluation_list.append(self.checkToneRepetition())
        evaluation_list.append(self.guardMotionToPerfectConsonance())
        evaluation_list.append(self.guardMotionToOctave())
        return(evaluation_list)

### TO-DO: Some additional rules to implement:
# Voice crossing a bad idea - but maybe can screen this in the generation of the counterpoint.
# Deal with chromatic alterations marking
# Prefer conjoint motion to disjoint motion  