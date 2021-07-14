import checklist
from checklist.test_suite import TestSuite
import sys

output=sys.stdout
outputfile=open('summary.txt','w')
sys.stdout=outputfile


suite = TestSuite.from_file('/home/sstl/dmj/checklist/release_data/sentiment/sentiment_suite.pkl')

suite.run_from_file('/home/sstl/dmj/checklist/release_data/sentiment/predictions/bert',overwrite=True)
suite.summary()

outputfile.close()
sys.stdout=output