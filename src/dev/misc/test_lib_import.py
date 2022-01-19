#%%
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..")) 

import SHSlib
#%%


from ..src.SHSlib import SHSlib


#%%

import sys

for path in sys.path:
    print(path)
sys.path