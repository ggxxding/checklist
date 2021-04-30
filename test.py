import checklist
import spacy
import itertools

import checklist.editor
import checklist.text_generation
from checklist.test_types import MFT, INV, DIR
from checklist.expect import Expect
from checklist.test_suite import TestSuite
import numpy as np
import spacy
from checklist.perturb import Perturb


editor = checklist.editor.Editor()
a=editor.template(('Is {first_name} {last_name} a {mask}?','Is {first_name} {last_name} a good?'), nsamples=2)
print(a)