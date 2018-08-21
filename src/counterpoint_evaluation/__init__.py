# __init__ for counterpoint_evaluation module
#
#   Contains an example to make sure that the logic is working
#   TO-DO: should this be converted into a series of unit tests?

from music21 import *
from evaluation_score import *
from harmonic_interval_rules import *
from melodic_interval_rules import *
from generate_counterpoint import *
from build_scores import *
from operator import itemgetter  # for the random generation finding optimal
import time



# Function for taking a list of generated counterpoints, sorting them, and displaying the best ones.
#    In the future, can include more settigns
def getFittestExamples(score_list, enterkey, weighting_type = 'none', top_selection_n = 5, showout = True, printout = True, verbose = False, manual = True):
    # Use the zip functions, etc. to sort the list, show the best ones as below.
    fitness_list = []
    for i in range(len(score_list)):
        this_eval = Evaluator(which_is_cpt_part = 1, myscore = score_list[i], mykey = enterkey)
        if weighting_type == 'none':
            fitness_list.append(this_eval.firstSpeciesEvaluation())
            if verbose:
                print('Using default (unweighted) weightings')
        elif weighting_type == 'rectified':
            fitness_list.append(this_eval.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified'))
            if verbose:
                print('Using rectified weightings')
    # end for loop
    sorted_fitnesses = sorted(enumerate(fitness_list), key = itemgetter(1))
    top_results = []
    choice = 1
    for i in range(top_selection_n):
        print(i)
        index = sorted_fitnesses[i][0]
        top_results.append(score_list[index])
        if manual and choice:
            choice = input("Enter 1 to see the next counterpoint example, and enter 0 to see all of the examples at once: ")
        if printout:
            buf = "The fitness for the %dth best counterpoint generated is %f" % (i,sorted_fitnesses[i][1])
            print(buf)
        if showout:
            top_results[i].show()
            
    return(top_results)
    # End function
    
    
# Function for taking an already-computed list and doing a consonance-improvement, sort, and return top n.  
# Presumably they all have the Cf - required here.  
def improveConsonanceOnExamples(score_list, enterkey, weighting_type = 'none', top_selection_n = 5, improvements_per_ex = 10, showout = True, printout = True, verbose = False):
    num_init_samples = len(score_list)
    improvement_scores_list = []
    cf = score_list[0][1]  
    if verbose:
        print('Beginning unweighted counterpoint consonance improvement:')
    for i in range(num_init_samples):
        this_sample = buildScore(score_list[i][0],cf)
        #score_list[i][0].show('text')
        this_eval = Evaluator(which_is_cpt_part = 1, mykey = enterkey, myscore = this_sample)
        this_eval.firstSpeciesEvaluation() # A little inefficient - We computed these earlier.
        for j in range(improvements_per_ex):
            if verbose:
                print('%d\t%d' % (i,j))
            this_new_sample = this_eval.improveCounterpointConsonances()
#             this_new_sample.show()
            improvement_scores_list.append(this_new_sample)
    # Again this is a little inefficient, because we will be reforming the Evaluator objects.
    if verbose:
        print('Running key testing:')
        print(improvement_scores_list[0] == improvement_scores_list[1])
#         print(improvement_scores_list)
#         improvement_scores_list[0].show()
#         improvement_scores_list[1].show()
#         improvement_scores_list[2].show()
        
    final_list = getFittestExamples(improvement_scores_list, enterkey, weighting_type, top_selection_n, showout, printout, verbose)
    return(final_list)
    
# Function for weeding out duplicates from a list of scores.
def eliminateDuplicates(sorted_score_list, which_is_cpt = 1, num_to_examine = 10):
    new_list = []
    cpts = []
    if which_is_cpt == 1:
        idx = 0
    else:
        idx = 1
    cf = sorted_score_list[0][idx]
    for i in range(len(sorted_score_list)):
        cpts.append(sorted_score_list[i][idx])
    # Now we have all of the counterpoints. The checking for duplicates is N^2 as currently written.
    # For efficiency, can later modify this so that it only checks the first few.
    total_length = len(sorted_score_list)
    if total_length < num_to_examine:
        num_to_examine = total_length
    delete_flags = []
    for i in range(num_to_examine):
        for j in range(i+1, num_to_examine):
            # test equality
            print('i and j values are %d and %d' % (i,j))
            if isEqualScore(sorted_score_list[i][idx], sorted_score_list[j][idx]):
                print('Comparison yielded true - these are the same score')
                if not(j in delete_flags):
                    delete_flags.append(j)
    # All duplicates should be marked. Now delete:
    delete_flags.sort()
    print(delete_flags)
    new_list = sorted_score_list
    for delete_flag in delete_flags:
        del new_list[delete_flag]
        for i in range(len(delete_flags)):
            delete_flags[i] = delete_flags[i] - 1
    #Should be done, but unit tests!!!
    return(new_list)
  
  
def isEqualScore(cpt1, cpt2):
    print(cpt1)
    print(cpt2)
    length1 = len(cpt1.flat)
    length2 = len(cpt2.flat)
    if length1 != length2:
        return(False)
    else:
        for i in range(length1):
            this_comparison = (cpt1.flat[i] == cpt2.flat[i])
            if not this_comparison:
                return(False)
    return(True)
    #End of function
    
def manuallyViewScoresAndEvaluation():
    pass
    
if __name__ == '__main__':
    print('Running counterpoint evaluation as main program')
    # Architecture of counterpoint: Have two parts within a score object.
    # Set number of measures beforehand. Each measure will contain a single whole note to start.
    
    
#     print('\n--- Testing Counterpoint Generation ---\n')
#     fux_cg = CounterpointGenerator(fux_ionian_score[1])
#     new_cpt = fux_cg.generateRandomFilteredCounterpointExample()
#     
#     new_eval = Evaluator(new_cpt, fux_ionian_score[1], 1)
#     new_fitness = new_eval.firstSpeciesEvaluation()
#     print('Fitness metric for the new counterpoint:')
#     print(new_fitness)
#     print('\nDisplaying the new counterpoint')
#     new_score = stream.Score()
#     new_score.append(new_cpt)
#     new_score.append(fux_ionian_score[1])
#     new_score.show()

    print('\n--- Testing randomized counterpoint generation and selection ---\n')
    fux_ionian_score = getFuxIonianFirstSpecies()
    starttime = time.clock()
    NUM_SAMPLES = 100
    fux_cg = CounterpointGenerator(fux_ionian_score[1])
    new_cpt_list = []
    # Actually, don't really need to store the evaluators.
    #eval_list = []
    fitness_list = []
    rectified_fitness_list = []
    for i in range(NUM_SAMPLES):
        new_cpt = fux_cg.generateRandomFilteredCounterpointExample()
        new_cpt_list.append(new_cpt)
        buf = "Displaying evaluator breakdown for the %dth new counterpoint example" % i
        print(buf) 
        this_eval = Evaluator(which_is_cpt_part = 1, mykey = 'c', part1 = new_cpt, part2 = fux_ionian_score[1])
        this_fitness = this_eval.firstSpeciesEvaluation()
        rectified_fitness = this_eval.firstSpeciesEvaluation(harmonic_weighting_scheme = 'consonance rectified', melodic_weighting_scheme = 'repetition rectified')
#         eval_list.append(this_eval)
        fitness_list.append(this_fitness)
        rectified_fitness_list.append(rectified_fitness)
    # end for loop
    
    sorted_results = sorted(enumerate(fitness_list), key = itemgetter(1))
    rectified_sorted_results = sorted(enumerate(rectified_fitness_list), key = itemgetter(1))
#     print(sorted_results)
#     best_fitness = sorted_results[0][1]
#     best_index = sorted_results[0][0]
#     best_cpt = new_cpt_list[best_index]
    n = 5
    # Now, build and show the top five counterpoints.
    for i in range(n):
        index = sorted_results[i][0]
#         print(index)
        new_score = buildScore(new_cpt_list[index],fux_ionian_score[1])
#         new_score.show('text')
#         new_score.show()
#         time.sleep(3)
        buf = "The fitness for the %dth best unweighted counterpoint generated is %f" % (i,sorted_results[i][1])
        print(buf)
        
    for i in range(n):
        rect_index = rectified_sorted_results[i][0]
        rect_new_score = buildScore(new_cpt_list[rect_index],fux_ionian_score[1])
        # rect_new_score.show()
        buf = "The fitness for the %dth best rectified weight counterpoint generated is %f" % (i,rectified_sorted_results[i][1])
        print(buf)
        
    # This was code for showing the best counterpoint.
#     new_best_score = buildScore(cpt_part, cf_part)
#     new_best_score = stream.Score()
#     new_best_score.append(best_cpt)
#     new_best_score.append(fux_ionian_score[1])
    totaltime = time.clock() - starttime
    
    NUM_TOP_SAMPLES = 30
    NUM_NEW_SAMPLES_PER_COUNTERPOINT = 5 
    improvement_fitness_list = []
    improvement_scores_list = []
    print('Beginning unweighted counterpoint consonance improvement:')
    for i in range(NUM_TOP_SAMPLES):
        index = sorted_results[i][0]
        this_sample = buildScore(new_cpt_list[index],fux_ionian_score[1])
        this_eval = Evaluator(which_is_cpt_part = 1, mykey = 'c', myscore = this_sample)
        this_eval.firstSpeciesEvaluation() # A little inefficient - We computed these earlier.
        for j in range(NUM_NEW_SAMPLES_PER_COUNTERPOINT):
            print('%d\t%d' % (i,j))
            this_new_sample = this_eval.improveCounterpointConsonances()
            improvement_scores_list.append(this_new_sample)
            new_eval = Evaluator(which_is_cpt_part = 1, mykey = 'c', myscore = this_new_sample)
            this_fitness = new_eval.firstSpeciesEvaluation()
            improvement_fitness_list.append(this_fitness)
        # end for loop
    # end for loop
    
    
    
    sorted_results = sorted(enumerate(improvement_fitness_list), key = itemgetter(1))
    print(sorted_results)
    for i in range(5):
        index = sorted_results[i][0]
        improvement_scores_list[index].show()
    #end
    
#     new_best_score.show()
#     print('The fitness metric for the best new counterpoint was as follows:')
#     print(best_fitness)
    
#     print(fitness_list)
    print('The total computation time was as follows:')
    print(totaltime)
    
    
    # In sum, this counterpoint is okay, but not great. So we should detect some flaws via our rules.
    # I knocked out this counterpoint in about 2 minutes. Can the machine do better? 
    
# End if __name__ == '__main__'


