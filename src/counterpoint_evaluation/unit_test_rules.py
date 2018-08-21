'''
Created on Apr 16, 2018

filename: unit_test_rules.py
Performs unit tests for 
    harmonic_interval_rules.py
    melodic_interval_rules.py

@author: nathanaelkazmierczak
'''

from music21 import *
from counterpoint_evaluation import *

class RulesTester:
    # Use constructor to build the standard Fux Ionian score, and a couple of other examples:
    # Attributes:
    # self.fux_ionian_score
    # self.shortexample1
    # self.shortexample2
    # self.se1eval
    # self.se2eval
    # self.fieval
    def __init__(self):
        # Example 1: (shortexample1) a bad example
        self.shortexample1_score = buildFirstSpeciesScore('b-', [1,3,2,1], [2,7,5,1], 0)
        self.shortexample2_score = buildFirstSpeciesScore('f', [1,3,4,5,6,4,5,1], [6,5,6,7,8,9,7,8], 0)
        self.fux_ionian_score = getFuxIonianFirstSpecies()
        # Optional code to show the scores:
#         if __name__ == '__main__':
#             self.shortexample1_score.show()
#             self.shortexample2_score.show()
#             self.fux_ionian_score.show()
        
        self.se1eval = Evaluator(which_is_cpt_part = 1, mykey = 'b-', myscore = self.shortexample1_score)
        self.se2eval = Evaluator(which_is_cpt_part = 1, mykey = 'f', myscore = self.shortexample2_score)
        self.fieval = Evaluator(which_is_cpt_part = 1, mykey = 'c', myscore = self.fux_ionian_score)
        self.se1info = self.se1eval.getRulesInstances()
        self.se2info = self.se2eval.getRulesInstances()
        self.fiinfo = self.fieval.getRulesInstances()
        
    def runAllTests(self):
        print('Running unit tests...')
        self.runHarmonicTests()
        self.runMelodicTests()
    
    def runHarmonicTests(self):
        print('Running harmonic tests:')
        self.testCheckConsonances()
        self.testScoreConsonanceRatio()
        self.testCheckEndBeginning()
        self.testCheckCadence()
        self.testCheckTritones()
        self.testCheckUnisons()
        self.testCheckParallelPerfectConsonances()
        print('All tests passed!')
    
    def runMelodicTests(self):
        print('Running melodic tests:')
        
        print('All tests passed!')
    
    def testCheckConsonances(self):
        print('-----Testing checkConsonances()-----')
        se1hir = self.se1info[0]
        results = se1hir.checkConsonances()
        assert(results[0] == 2)
        assert(results[1] == [0, 2])
        
        se2hir = self.se2info[0]
        results = se2hir.checkConsonances()
        assert(results[0] == 0)
        assert(results[1] == [])
   
        fihir = self.fiinfo[0]
        results = fihir.checkConsonances()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        print('-----Passed!-----')
        
    def testScoreConsonanceRatio(self):
        print('-----Testing scoreConsonanceRatio()-----')
        se1hir = self.se1info[0]
        results = se1hir.scoreConsonanceRatio()
        assert(results == 1)
        
        se2hir = self.se2info[0]
        results = se2hir.scoreConsonanceRatio()
        assert(results == 0)
        
        fihir = self.fiinfo[0]
        results = fihir.scoreConsonanceRatio()
        assert(results == 0.1)
        
        print('-----Passed!-----')
        
    def testCheckEndBeginning(self):
        print('-----Testing checkEndBeginning()-----')
        se1hir = self.se1info[0]
        results = se1hir.checkEndBeginning()
        assert(results[0] == 1)
        assert(results[1] == [0])
        
        se2hir = self.se2info[0]
        results = se2hir.checkEndBeginning()
        assert(results[0] == 0)
        assert(results[1] == [])
   
        fihir = self.fiinfo[0]
        results = fihir.checkEndBeginning()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        print('-----Passed!-----')
        
    def testCheckCadence(self):
        print('-----Testing checkCadence()-----')
        se1hir = self.se1info[0]
        results = se1hir.checkCadence()
        assert(results[0] == 1)
        assert(results[1] == [2])
        
        se2hir = self.se2info[0]
        results = se2hir.checkCadence()
        assert(results[0] == 1)
        assert(results[1] == [6])
   
        fihir = self.fiinfo[0]
        results = fihir.checkCadence()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        print('-----Passed!-----')
        
    def testCheckTritones(self):
        print('-----Testing checkTritones()-----')
        se1hir = self.se1info[0]
        results = se1hir.checkTritones()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        se2hir = self.se2info[0]
        results = se2hir.checkTritones()
        assert(results[0] == 0)
        assert(results[1] == [])
   
        fihir = self.fiinfo[0]
        results = fihir.checkTritones()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        example_with_tritones = buildFirstSpeciesScore('a', [1,4,2,0,1], [8,7,6,4,5], 0)
#         if __name__ == '__main__':
#             example_with_tritones.show()
        tritone_eval = Evaluator(1, myscore = example_with_tritones)
        tupleinfo = tritone_eval.getRulesInstances()
        tritone_hir = tupleinfo[0]
        results = tritone_hir.checkTritones()
        assert(results[0] == 2)
        assert(results[1] == [1,3])
        
        print('-----Passed!-----')
        
    def testCheckUnisons(self):
        print('-----Testing checkUnisons()-----')
        se1hir = self.se1info[0]
        results = se1hir.checkUnisons()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        se2hir = self.se2info[0]
        results = se2hir.checkUnisons()
        assert(results[0] == 0)
        assert(results[1] == [])
   
        fihir = self.fiinfo[0]
        results = fihir.checkUnisons()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        example_with_unisons = buildFirstSpeciesScore('f#', [1,4,3,2,1], [5,4,3,4,1], 0)
#         if __name__ == '__main__':
#             example_with_unisons.show()
        unisons_eval = Evaluator(1, myscore = example_with_unisons)
        tupleinfo = unisons_eval.getRulesInstances()
        unisons_hir = tupleinfo[0]
        results = unisons_hir.checkUnisons()
        assert(results[0] == 2)
        assert(results[1] == [1,2])
    
        print('-----Passed!-----')
        
    def testCheckParallelPerfectConsonances(self):
        print('-----Testing checkUnisons()-----')
        se1hir = self.se1info[0]
        results = se1hir.checkParallelPerfectConsonances()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        se2hir = self.se2info[0]
        results = se2hir.checkParallelPerfectConsonances()
        assert(results[0] == 0)
        assert(results[1] == [])
   
        fihir = self.fiinfo[0]
        results = fihir.checkParallelPerfectConsonances()
        assert(results[0] == 0)
        assert(results[1] == [])
        
        example_with_unisons = buildFirstSpeciesScore('f#', [1,4,3,2,1], [5,4,3,4,1], 0)
#         if __name__ == '__main__':
#             example_with_unisons.show()
        unisons_eval = Evaluator(1, myscore = example_with_unisons)
        tupleinfo = unisons_eval.getRulesInstances()
        unisons_hir = tupleinfo[0]
        results = unisons_hir.checkParallelPerfectConsonances()
        assert(results[0] == 2)
        assert(results[1] == [0,1,1,2])
        
        pfifths = buildFirstSpeciesScore('g', [4,3,2,1], [8,7,6,12], 0)
#         if __name__ == '__main__':
#             pfifths.show()
        p5_eval = Evaluator(1, myscore = pfifths)
        p5info = p5_eval.getRulesInstances()
        p5_hir = p5info[0]
        results = p5_hir.checkParallelPerfectConsonances()
        assert(results[0] == 3)
        assert(results[1] == [0,1,1,2,2,3])
    
        print('-----Passed!-----')
        
        
    # Right now this is not a formal unit test, just seeing if the integer conversion is working correctly.
    def testIsUnimodal(self):
        ev = Evaluator(1, 'c', myscore = self.fux_ionian_score)
        ev.invokePhraseStructure()
        
    def originalTests(self):
        EXAMPLE_LENGTH = 12;
        
        this_scale = scale.MajorScale('c')
        
        myfirstscore = stream.Score();
        counterpoint_part = stream.Part();  # This is the upper voice here
        cantus_firmus_part = stream.Part();  # This is the lower voice here
        # Construct measures
        tonic_pitch = this_scale.getTonic()
        print(tonic_pitch)
        high_tonic_pitch = interval.transposePitch(tonic_pitch, 'p15')
        print(high_tonic_pitch)
        current_cf_pitch = tonic_pitch
        current_cpt_pitch = high_tonic_pitch
        
        for i in range(EXAMPLE_LENGTH):
            this_cpt_note = note.Note(current_cpt_pitch)
            this_cf_note = note.Note(current_cf_pitch)
            
            this_cpt_measure = stream.Measure()
            this_cf_measure = stream.Measure()
            this_cpt_measure.append(this_cpt_note)
            this_cf_measure.append(this_cf_note)
            counterpoint_part.append(this_cpt_measure)
            cantus_firmus_part.append(this_cf_measure)
            
            current_cf_pitch = this_scale.next(current_cf_pitch)
            current_cpt_pitch = this_scale.next(current_cpt_pitch, direction = 'descending')
        # End for loop 
        
        myfirstscore.insert(counterpoint_part);
        myfirstscore.insert(cantus_firmus_part);
        
    #     print(myfirstscore);
    #     myfirstscore.show('text')
    #     myfirstscore.show()
        fsmi = obtain_melodic_intervals(myfirstscore[0])
        fsgmi = obtain_generic_melodic_intervals(myfirstscore[0])
        fshi = obtain_harmonic_intervals(myfirstscore[1],myfirstscore[0])
        fsghi = obtain_generic_harmonic_intervals(myfirstscore[1],myfirstscore[0])
        fsmt = obtain_motion_type(myfirstscore[1],myfirstscore[0])
        
        
        # Now build a slightly more musical example, drawing off of the Fux book.
        fux_ionian_score = getFuxIonianFirstSpecies()  
        
        # Test out some of the functions
        mi = obtain_melodic_intervals(fux_ionian_score[0])
        gmi = obtain_generic_melodic_intervals(fux_ionian_score[0])
        hi = obtain_harmonic_intervals(fux_ionian_score[1],fux_ionian_score[0])
        ghi = obtain_generic_harmonic_intervals(fux_ionian_score[1],fux_ionian_score[0])
        mt = obtain_motion_type(fux_ionian_score[1],fux_ionian_score[0])
        
        print('\n--- Testing Harmonic Interval Rules ---\n')
        print('Number of consonance rules violated by the Fux counterpoint:')
        myHarmonicRules = HarmonicIntervalRules(hi, ghi)
        result = myHarmonicRules.checkConsonances()
        print(result)
        
        print('Number of consonance rules violated by the first score:')
        fsmyHarmonicRules = HarmonicIntervalRules(fshi, fsghi)
        fsresult = fsmyHarmonicRules.checkConsonances()
        print(fsresult)
        
        print('Consonance ratio for Fux counterpoint:')
        result = myHarmonicRules.scoreConsonanceRatio()
    #     print(myHarmonicRules.num_body_perfect_consonances)
    #     print(myHarmonicRules.num_body_imperfect_consonances)
        print(result)
        
        print('Consonance ratio for the first score:')
        fsresult = fsmyHarmonicRules.scoreConsonanceRatio()
    #     print(fsmyHarmonicRules.num_body_perfect_consonances)
    #     print(fsmyHarmonicRules.num_body_imperfect_consonances)
        print(fsresult)
        
        print('Check end beginning for Fux counterpoint:')
        result = myHarmonicRules.checkEndBeginning()
        print(result)
        
        print('Check end beginning for the first score:')
        fsresult = fsmyHarmonicRules.checkEndBeginning()
        print(fsresult)
        
        print('Check tritones for Fux counterpoint:')
        result = myHarmonicRules.checkTritones()
        print(result)
        
        print('Check tritones for the first score:')
        fsresult = fsmyHarmonicRules.checkTritones()
        print(fsresult)
        
        print('Check cadence for Fux counterpoint:')
        result = myHarmonicRules.checkCadence()
        print(result)
        
        print('Check cadence for first score:')
        fsresult = fsmyHarmonicRules.checkCadence()
        print(fsresult)
        
        print('Check unisons for Fux counterpoint:')
        result = myHarmonicRules.checkUnisons()
        print(result)
        
        print('Check unisons for first score:')
        fsresult = fsmyHarmonicRules.checkUnisons()
        print(fsresult)
        
        print('Check parallel perfect consonances for Fux counterpoint:')
        result = myHarmonicRules.checkParallelPerfectConsonances()
        print(result)
        
        print('Check parallel perfect consonances for first score:')
        fsresult = fsmyHarmonicRules.checkParallelPerfectConsonances()
        print(fsresult)
        
        print('Finished testing Harmonic Interval Rules')
        print('\n--- Testing Melodic Interval Rules ---\n')
        
        print('Score motion types for Fux counterpoint:')
        myMelodicRules = MelodicIntervalRules(mi, gmi, mt, hi)
        result = myMelodicRules.scoreMotionTypes()
        print(result)
        
        print('Score motion types for first score:')
        fsmyMelodicRules = MelodicIntervalRules(fsmi, fsgmi, fsmt, fshi)
        fsresult = fsmyMelodicRules.scoreMotionTypes()
        print(fsresult)
        
        print('Testing for awkward melodic intervals (diminished, augmented) in Fux counterpoint:')
        result = myMelodicRules.avoidAwkwardIntervals()
        print(result)
        
        print('Testing for awkward melodic intervals (diminished, augmented) in first score:')
        fsresult = fsmyMelodicRules.avoidAwkwardIntervals()
        print(fsresult)
        
        print('Testing for large dissonant leaps in Fux counterpoint:')
        result = myMelodicRules.avoidLargeDissonantLeaps()
        print(result)
        
        print('Testing for large dissonant leaps in first score:')
        fsresult = fsmyMelodicRules.avoidLargeDissonantLeaps()
        print(fsresult)
        
        print('Testing for successive skips in Fux counterpoint:')
        result = myMelodicRules.avoidSuccessiveSkips()
        print(result)
        
        print('Testing for successive skips in first score:')
        fsresult = fsmyMelodicRules.avoidSuccessiveSkips()
        print(fsresult)
        
        print('Testing for jump preparation in Fux counterpoint:')
        result = myMelodicRules.preferJumpPreparation()
        print(result)
        
        print('Testing for jump preparation in first score:')
        fsresult = fsmyMelodicRules.preferJumpPreparation()
        print(fsresult)
        
        print('Testing for posterior jump compensation in Fux counterpoint:')
        result = myMelodicRules.preferJumpFollowingCompensation()
        print(result)
        
        print('Testing for posterior jump compensation in first score:')
        fsresult = fsmyMelodicRules.preferJumpFollowingCompensation()
        print(fsresult)
        
        print('Testing for tone repetition in Fux counterpoint:')
        result = myMelodicRules.checkToneRepetition()
        print(result)
        
        print('Testing for tone repetition in first score:')
        fsresult = fsmyMelodicRules.checkToneRepetition()
        print(fsresult)
        
        print('Testing for direct perfect consonances in Fux counterpoint:')
        result = myMelodicRules.guardMotionToPerfectConsonance()
        print(result)
        
        print('Testing for direct perfect consonances in first score:')
        fsresult = fsmyMelodicRules.guardMotionToPerfectConsonance()
        print(fsresult)
        
        print('Testing for skips into octave in Fux counterpoint:')
        result = myMelodicRules.guardMotionToOctave()
        print(result)
        
        print('Testing for skips into octave in first score:')
        fsresult = fsmyMelodicRules.guardMotionToOctave()
        print(fsresult)
        
        print('Finished testing Melodic Interval Rules')
        print('\n--- Testing Evaluator ---\n')
        
        # Get the evaluator:
        fs_eval = Evaluator(myfirstscore[0], myfirstscore[1], 1)
        fux_ionian_eval = Evaluator(fux_ionian_score[0], fux_ionian_score[1], 1)
        fs_fitness = fs_eval.firstSpeciesEvaluation()
        fux_ionian_fitness = fux_ionian_eval.firstSpeciesEvaluation()
        print('Fitness metric for the first score:')
        print(fs_fitness)
        print('Fitness metric for the Fux ionian score:')
        print(fux_ionian_fitness)
        print('Finished testing Evaluator')
    
# main code:
if __name__ == '__main__':
    rt = RulesTester()
    #rt.runAllTests()
    rt.testIsUnimodal()
    print('Special test of psr rules')
    
    
# end main code     