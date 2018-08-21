from music21 import *
print('successfully imported music21')
s = corpus.parse('bach/bwv65.2.xml')
print(s.analyze('key'))