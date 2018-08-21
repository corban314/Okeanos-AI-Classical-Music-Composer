# generate_counterpoint.py
#
#   Module for generating many counterpoint examples that will subsequently be evaluated.

import random
from music21 import *

# Supporting Function
def buildScore(cpt_part, cf_part):
    new_best_score = stream.Score()
    new_best_score.append(cpt_part)
    new_best_score.append(cf_part)
    return(new_best_score)

class CounterpointGenerator:
    cantus_firmus_part = []
    length = []
    key = []
    mode = []
    scale = []
    
    def __init__(self, mykey, cantus_firmus_part):
        self.cantus_firmus_part = cantus_firmus_part
        self.length = len(cantus_firmus_part.flat)
        # self.key = cantus_firmus_part.analyze('key')
        self.key = key.Key(mykey);
        self.mode = self.key.mode
        self.scale = self.key.getScale(self.mode)
        
    # Generates multiple (n) counterpoint examples using the generateRandomFilteredCounterpointExample()
    #    method, and returns them as a list. Note that we should include options for settings in the future,
    #    mapping to different methods for generating the cpts.
    def generateNcounterpoints(self, n, verbose = False):
        score_list = []
        for i in range(n):
            this_part = self.generateRandomFilteredCounterpointExample()
            this_score = buildScore(this_part, self.cantus_firmus_part)
            score_list.append(this_score)
            if verbose:
                print('Generating %dth counterpoint example' % i)
        return(score_list)
    # End method    
        
        
        
    # Generates a single counterpoint example, returned as a Part stream.
    #     TO-DO: for now, we are letting music21 do the key analysis to figure out what
    #    scale we should use. Make this more robust in the future.
    def generateRandomFilteredCounterpointExample(self):
        VOICE_CROSSING_TOLERANCE = 10  # Maximum number of times to fail a voice crossing before we start a new counterpoint example.
        
        # For now, start all of the specimens at the third, fifth, octave, or tenth.
        terminate = 0
        while not terminate:
#             print('Inside while not terminate')
            cpt_part = stream.Part()
            terminate = 1  # The default is to break out of the loop.
            init_cf_note = self.cantus_firmus_part.flat[0]
            init_choice = random.randint(0,3)
            if init_choice == 0: # build a third above the cf
                current_degree = 3
                first_cpt_note = note.Note(self.key.pitchFromDegree(current_degree))
            elif init_choice == 1:
                current_degree = 5
                first_cpt_note = note.Note(self.key.pitchFromDegree(current_degree))
            elif init_choice == 2:
                current_degree = 8
                first_cpt_note = note.Note(self.key.pitchFromDegree(current_degree))
                first_cpt_note = interval.transposeNote(first_cpt_note, 'p8')
            else:
                current_degree = 3
                first_cpt_note = note.Note(self.key.pitchFromDegree(current_degree))
                first_cpt_note = interval.transposeNote(first_cpt_note, 'p8')
                # Transpose up so that when we transpose to common level below, this will be an
                #    octave higher than the third.
            
            # Figure out if we need to transpose the initial counterpoint note up or down at all.
            # The assumption is that the counterpoint is above the cantus firmus, for now.
            cf_octave = self.cantus_firmus_part.flat[0].octave
            reference_scale_note = note.Note(self.scale.getTonic())
            reference_scale_octave = reference_scale_note.octave
            # We want the reference scale to start at the same pitch as the first cantus firmus note.
            if reference_scale_octave < cf_octave:
                # This will be the number of times we need to transpose up by an octave
                difference = reference_scale_octave - cf_octave
                for i in range(difference):
                    first_cpt_note = interval.transposeNote(first_cpt_note, 'p8')
                # End for loop
            elif reference_scale_octave > cf_octave:
                difference = reference_scale_octave - cf_octave
                for i in range(abs(difference)):
                    first_cpt_note = interval.transposeNote(first_cpt_note, 'p-8')
                # End for loop
            else:
                difference = 0  # note sure if we will need this.
                
            this_cpt_measure = stream.Measure()
            this_cpt_measure.append(first_cpt_note)
            cpt_part.append(this_cpt_measure)
            # Now we need to generate the notes for the body of the counterpoint.
            #    For now, assume that we will end on either an octave or a unison.
            #    Further assume that the approach is correct (stepwise contrary) to reduce search space.
            #    TO-DO: currently we only have a possibility for "allowed" leaps over a fifth -- sixth and octave.
            current_note = first_cpt_note
            voice_crossing_failures = 0  # Track the number of times we have failed to generate a good counterpoint because of a voice-crossing problem.
            for i in range(1, self.length - 2):
#                 print('Inside for loop')
#                 debugbuf = "This is the %dth note in the counterpoint" % i
#                 print(debugbuf)
                accepted = 0
                while not accepted:
#                     print('Inside while not accepted')
                    # We want to have a probability of stepwise motion higher than leap, etc.
                    # This will not affect fitness, but will tend to generate more fit samples (less disjoint motion)
                    # So use a triangle distribution out to the octave, perhaps, or maybe sigmas on a Gaussian.
                    # Positioning of notes is generated relative to the current note.
                    choice_number0 = random.random()
                    if choice_number0 < 0.1:  # 10% chance of sampling oblique motion
                        this_interval_number = 1
                    else:
                        choice_number = random.gauss(0,1)  # mu = 0, sigma = 1
                        if choice_number > 0 and choice_number <= 1:  # ascending step
                            this_interval_number = 2
                        elif choice_number <= 0 and choice_number > -1:  # descending step
                            this_interval_number = -2
                        elif choice_number > 1 and choice_number <= 2: # ascending skip
                            this_interval_number = 3
                        elif choice_number <= -1 and choice_number > -2:  # descending skip
                            this_interval_number = -3
                        else:  # Leaps may be chosen uniformly between fourth, fifth, or something else (less probability).
                            choice_number2 = random.uniform(-0.5,0.5)
                            if choice_number2 >= -0.5 and choice_number2 <= -0.3:  #choose ascending fourth:
                                this_interval_number = 4
                            elif choice_number2 > -0.3 and choice_number2 <= -0.1:  # choose descending fourth:
                                this_interval_number = -4
                            elif choice_number2 > -0.1 and choice_number2 <= 0.1:  # choose ascending fifth:
                                this_interval_number = 5
                            elif choice_number2 > 0.1 and choice_number2 <= 0.3:  # choose descending fifth:
                                this_interval_number = -5
                            else:  # choose something else.
                                choice_number3 = random.random()
                                if choice_number3 < 0.5:
                                    this_interval_number = 6  # choose ascending sixth
                                else:
                                    this_interval_number = 8  # choose ascending octave
                    # End logic for choosing interval ......
                    # Now construct the new interval and new note:
                    new_degree = this_interval_number + current_degree - 1 
                    this_interval_mod7 = self.scale.intervalBetweenDegrees(current_degree, new_degree)
                    this_interval_mod7.noteStart = current_note
                    this_note = this_interval_mod7.noteEnd
                    if new_degree > 7:
                        this_note = interval.transposeNote(this_note, 'p8')
                    elif new_degree < 0:
                        this_note = interval.transposeNote(this_note, 'p-8') 
                    # Now, test for voice-crossing.
                    # After selecting a note, check to see if we are voice-crossing with cf. If so, reject and try again.
                    if this_note < self.cantus_firmus_part.flat[i]:
                        accepted = 0  # redundant, really.
                        voice_crossing_failures = voice_crossing_failures + 1
#                         testbuf = "voice_crossing_failures is %d" % voice_crossing_failures
#                         print(testbuf)
                        if voice_crossing_failures > VOICE_CROSSING_TOLERANCE:
                            terminate = 0
                            break  # Should break the while not accepted loop
    #                     print('note not accepted due to voice crossing')
                    else:
                        accepted = 1
                # End while loop for voice crossing........... 
                if terminate == 0:
                    break # should break the for loop
                current_degree = new_degree
                current_note = this_note
                # Update current_degree, current_note so we will start at the right spot on the next for-loop iteration.
                # Add the new note to the cpt:
                this_cpt_measure = stream.Measure()
                this_cpt_measure.append(this_note)
                cpt_part.append(this_cpt_measure)
            # End for loop over notes
            # If we have made it through all of the notes without throwing the terminate = 0, we should have terminate = 1, and exit the loop. 
        # End while loop for termination (if undoing voice crossing is taking too long)....
#         print('Exiting while not terminate')   
#         print(cpt_part)
#         cpt_part.show('text')
        # Now fill in the final cadence:
        # Find the two octave notes that are closest to where we have ended up.
        octave1 = this_note.octave
        tonic_pc = getScalePitchClass(self.scale, 1)
        ending_note1 = buildNoteAtOctave(tonic_pc, octave1)
        if ending_note1 < this_note:
            ending_note2 = buildNoteAtOctave(tonic_pc, octave1 + 1)
        elif ending_note1 > this_note:
            ending_note2 = buildNoteAtOctave(tonic_pc, octave1 - 1)
        else:
            ending_note2 = ending_note1 # if we are already at the octave, we should stay there
        
        choice_number4 = random.random()
        if choice_number4 < 0.5:
            final_cpt_note = ending_note1
        else:
            final_cpt_note = ending_note2
        
        # Final note has been determined: get the penultimate note by ascertaining the motion needed.
        # TODO: modify this to allow different types of motion: descending fifth, etc.
        # TODO: pull some of this logic out into generalized functions for building a note above, below a pitch.
        final_cf_note = self.cantus_firmus_part.flat[-1]
        penult_cf_note = self.cantus_firmus_part.flat[-2]
        ending_note_octave = final_cpt_note.octave
        if final_cf_note > penult_cf_note:
            # this situation has ascending cf motion into the cadence
            pitch_class = getScalePitchClass(self.scale, 2) # so we will descend
            penult_cpt_note = buildNoteAtOctave(pitch_class, ending_note_octave)
            if penult_cpt_note < final_cpt_note: # shouldn't be the case
                penult_cpt_note = interval.transposeNote(penult_cpt_note,'p8')
        elif final_cf_note < penult_cf_note:
            # this situation has descending cf motion into the cadence
            pitch_class = getScalePitchClass(self.scale, 7) # so we will ascend
            penult_cpt_note = buildNoteAtOctave(pitch_class, ending_note_octave)
            if penult_cpt_note > final_cpt_note: # shouldn't be the case
                penult_cpt_note = interval.transposeNote(penult_cpt_note,'p-8')
        else:
            exit(1)
        
        this_cpt_measure = stream.Measure()
        this_cpt_measure.append(penult_cpt_note)
        cpt_part.append(this_cpt_measure)
        this_cpt_measure = stream.Measure()
        this_cpt_measure.append(final_cpt_note)
        cpt_part.append(this_cpt_measure)
        return(cpt_part)
    #End generation method           
            
        
        
        
#         final_cf_note = self.cantus_firmus_part.flat[-1]
#         penult_cf_note = self.cantus_firmus_part.flat[-2]
#         if final_cf_note > penult_cf_note: 
#             # this situation has ascending cf motion into the cadence
#             choice_number4 = random.random()
#             if choice_number4 < 0.5:
#                 cpt_final_note
#         elif penult_cf_note > final_cf_note:  
#             # This situation has descending cf motion into the cadence
        

### Supporting functions:
def buildNoteAtOctave(pitch_class, myoctave):
    this_note = note.Note(pitch_class)
    this_note.octave = myoctave
    return(this_note)

def getScalePitchClass(myscale, degree):
    degree_note = myscale.pitchFromDegree(degree)
    pitch_class = degree_note.name
    return(pitch_class)   
        
        
        
         