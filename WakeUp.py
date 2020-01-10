import sys
import os
original = sys.stdout
out = open('./console.log', 'w')
sys.stdout = out
sys.stderr = out

if (os.access("running.wt", os.W_OK)):
    os.remove("running.wt")
    
import Brainstem
