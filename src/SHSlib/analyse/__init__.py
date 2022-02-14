

def build_Clib(lib_name):
    import sys 
    import os
    import pathlib

    # get files next to this one
    curretn_folder = str(pathlib.Path(__file__).parent.resolve())
    files = os.listdir(curretn_folder)
    # check if system is linux and  
    #       if a sheard libray of the lib is in current path
    if sys.platform.startswith('linux'):
        # preset "build_succesful" state  
        build_succesful = True 
        
        # if ".so" file is not present try build 
        if not any(x==lib_name +".so" for x in files):
            print("rebilding sheard c libray, because it was not flound ")
            import subprocess as bash 
            Bulid_Command = ["gcc", "-Wall", "-pedantic", 
                        "-shared","-fpic", "-O3","-o" ,
                        str(curretn_folder) + "/"+ lib_name + ".so", 
                        str(curretn_folder) + "/"+ lib_name + ".c" ]   
#             Bulid_Command = ["gcc", "-Wall", "-pedantic", 
#                         "-shared","-fpic","-o" ,
#                         str(curretn_folder) + "/"+ lib_name + ".so", 
#                         str(curretn_folder) + "/"+ lib_name + ".c" ]   
                        
            try:
                bash.run(Bulid_Command)
                build_succesful = True  
            except ValueError:
                build_succesful = False 
                print("Oops! buid was not sucsessful")
# import of C file

build_Clib("Clib")

from .getMomentum import getMomentum 
from .getPartner import getPartner
from .getSeperation import getSeperation

from .getIntegration import getIntegration