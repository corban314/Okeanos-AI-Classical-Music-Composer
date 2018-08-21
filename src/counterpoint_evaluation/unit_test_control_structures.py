'''
Created on Apr 18, 2018
Module for unit testing control structures in the computational counterpoint project.
(That is, things like list sorting and handling)
@author: nathanaelkazmierczak
'''

from counterpoint_evaluation import *

class ControlStructuresTester:
    def runTests(self):
        self.testGetFittestExamples(printout = 0, showout = 0)
        self.testEliminateDuplicates()
        self.testIsEqualScore(showout = 0)
    
    def testGetFittestExamples(self, printout = 1, showout = 0):
        print('Testing getFittestExamples...')
        manual_examples = getMultipleFuxIonianFirstSpecies()
        eval1 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[0])
        eval2 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[1])
        eval3 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[2])
        eval4 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[3])
        eval5 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[4])
        eval6 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[5])
        eval7 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[6])
        eval8 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[7])
        eval9 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[8])
        eval10 = Evaluator(which_is_cpt_part=1, mykey='c', myscore=manual_examples[9])
        fitness1 = eval1.firstSpeciesEvaluation()
        fitness2 = eval2.firstSpeciesEvaluation()
        fitness3 = eval3.firstSpeciesEvaluation()
        fitness4 = eval4.firstSpeciesEvaluation()
        fitness5 = eval5.firstSpeciesEvaluation()
        fitness6 = eval6.firstSpeciesEvaluation()
        fitness7 = eval7.firstSpeciesEvaluation()
        fitness8 = eval8.firstSpeciesEvaluation()
        fitness9 = eval9.firstSpeciesEvaluation()
        fitness10 = eval10.firstSpeciesEvaluation()
        
        
        rfitness1 = eval1.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness2 = eval2.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness3 = eval3.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness4 = eval4.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness5 = eval5.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness6 = eval6.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness7 = eval7.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness8 = eval8.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness9 = eval9.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        rfitness10 = eval10.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
        
        if printout:
            print('The unweighted fitness of example 1 is %f' % fitness1)
            print('The unweighted fitness of example 2 is %f' % fitness2)
            print('The unweighted fitness of example 3 is %f' % fitness3)
            print('The unweighted fitness of example 4 is %f' % fitness4)
            print('The unweighted fitness of example 5 is %f' % fitness5)
            print('The unweighted fitness of example 6 is %f' % fitness6)
            print('The unweighted fitness of example 7 is %f' % fitness7)
            print('The unweighted fitness of example 8 is %f' % fitness8)
            print('The unweighted fitness of example 9 is %f' % fitness9)
            print('The unweighted fitness of example 10 is %f' % fitness10)
            
            print('The rectified fitness of example 1 is %f' % rfitness1)
            print('The rectified fitness of example 2 is %f' % rfitness2)
            print('The rectified fitness of example 3 is %f' % rfitness3)
            print('The rectified fitness of example 4 is %f' % rfitness4)
            print('The rectified fitness of example 5 is %f' % rfitness5)
            print('The rectified fitness of example 6 is %f' % rfitness6)
            print('The rectified fitness of example 7 is %f' % rfitness7)
            print('The rectified fitness of example 8 is %f' % rfitness8)
            print('The rectified fitness of example 9 is %f' % rfitness9)
            print('The rectified fitness of example 10 is %f' % rfitness10)
        
        fittest_list = getFittestExamples(manual_examples, enterkey='c', top_selection_n=10, showout=True , printout = True, manual = True)
        print(fittest_list)
        if showout:
            for i in range(10):
                fittest_list[i].show()
            
        # It does appear that the sorting is taking place correctly, although doing a formal unit test wouldb e tricky.
        
    def testEliminateDuplicates(self, printout = 1, showout = 0):
        # Get the list of ten examples that I wrote on the basis of this thing:
        fux8cpt_list = getMultipleFuxIonianFirstSpecies()
        # Fux ionian is always in C
        fux8cpt_list_sorted = getFittestExamples(fux8cpt_list, 'c', weighting_type = 'rectified', top_selection_n = 10, showout = True, printout = True, verbose = False)
        duplicate_numbers = (3,5,8)
        num_duplicates = 3
        list_with_duplicates = fux8cpt_list_sorted
        for i in duplicate_numbers:
            for j in range(num_duplicates):
                new_score = fux8cpt_list_sorted[i-1] # So that #3 is actually pulling example #3 (which is the highly ranked one).
                list_with_duplicates.append(new_score)
           
        print('The following is the list that should have the highly-ranked duplicates')      
        duplicate_sorted_list = getFittestExamples(list_with_duplicates, 'c', weighting_type = 'rectified', top_selection_n = 10, showout = True, printout = True, verbose = False, manual = True)
#         duplicate_sorted_list[0].show('text')
#         duplicate_sorted_list[1].show('text')
#         duplicate_sorted_list[2].show('text')
#         duplicate_sorted_list[3].show('text')
#         duplicate_sorted_list[4].show('text')
#         duplicate_sorted_list[5].show('text')
#         duplicate_sorted_list[6].show('text')
#         duplicate_sorted_list[7].show('text')
#         duplicate_sorted_list[8].show('text')
#         duplicate_sorted_list[9].show('text')
        
        duplicates_removed_list = eliminateDuplicates(duplicate_sorted_list, which_is_cpt = 1, num_to_examine = 20)
        # Recall here that the num_to_examine parameter is set just to ensure that we don't spend O(N^2) time on the comparisons.
        # this list should already be sorted, but pass it back through the function to get the correct values.
        
        
        # Some problem in the function with the indices being screwed up????
        
        
        duplicates_removed_sorted_list = getFittestExamples(duplicates_removed_list, 'c', weighting_type = 'rectified', top_selection_n = 5, showout = True, printout = True, verbose = False, manual = True)
       
        #verify that now there are no duplicates
      
    def testIsEqualScore(self, showout = 1):
        print('Testing function isEqualScore....')
        fux8cpt_list = getMultipleFuxIonianFirstSpecies()
        test_cpt = fux8cpt_list[0][0]
        equal_cpt = fux8cpt_list[0][0]
        unequal_cpt = fux8cpt_list[3][0]
        
        if showout:
            test_cpt.show()
            time.sleep(3)
            equal_cpt.show()
            time.sleep(3)
            unequal_cpt.show()
            
        print("this is the first invocation of isEqual")
        assert(isEqualScore(test_cpt, equal_cpt))
        print("this is the second invocation of isEqual")
        assert(not isEqualScore(test_cpt, unequal_cpt))
        print('All Tests Passed!')
        
if __name__ == '__main__':
    cst = ControlStructuresTester()
    cst.runTests()
        