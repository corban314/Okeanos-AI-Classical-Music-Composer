# driver.py
#
#   Driver script for launching the computer_generated_counterpoint project.
from music21 import *
from counterpoint_evaluation import *

# Settings: Counterpoint length, algorithm method, time limit (if pertinent)
KEY = 'F'
# used_score = getFuxIonianFirstSpecies()
used_score = getFuxNo3inF()
fux_cg = CounterpointGenerator(KEY, used_score[1])

NUM_SAMPLES = 100
# Run the computation
initial_counterpoints = fux_cg.generateNcounterpoints(NUM_SAMPLES, verbose = True)
top_results = getFittestExamples(initial_counterpoints, enterkey = KEY, weighting_type = 'none', top_selection_n = 10, showout = False)
final_results = improveConsonanceOnExamples(top_results, enterkey = KEY, weighting_type = 'none', top_selection_n = 10, improvements_per_ex = 1, showout = True, printout = True, verbose = True)
final_results[0].show()
final_results[1].show()
print(final_results)    


# Render out to MuseScore:
