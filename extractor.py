# from vital import sys,os

import sys
import os


if sys.platform == 'linux': 

        SEP='/'
        #print('on linux')
else:

        SEP='\\'
        #print('on others')



def CP(paths:list=[])->str:
    """CP: concatenate paths 
    
    returns a path from the elements of list argument ,
 
    Args:
        paths (list, optional): the path to the file is splited to strings which are the elements of this arg . Defaults to [].

    Returns:
        str: a valid path 
    EX:
      CP(['downloads','sub_folder','File.txt'])= downloads/sub_folder/File.txt
    """
    if sys.platform == 'linux':
        s=os.path.abspath('').replace('/assets','') #this is a very bad way to get the parent directory
        #print('on linumx',s)
    else:
        s=''
        #print('on othersx')


    for i in paths:
        s=os.path.join(s,i)
    if os.path.exists(s):
        return    s
    else:
        return "not valid"

def OA(sp:str)->str:
    """OA : order alphabitcaly
    """
    li=sp.split(SEP)
    return li[-1][0:3]

def CP_DIR(path:str='',o=False,r=False)->list:
    """ CD_DIR : concatenate paths in directory
    
    returns all the files in a folder

    """
    l=[]
    for re in os.walk(path): # os.listdir can be used instead
        for i in re[2]:
            l.append( os.path.join(re[0],i) )
    if o:
        l.sort(reverse=r,key=OA)
    return l

def LS_DIR(path:str):
    l=[]
    for re in os.listdir(path): # os.listdir can be used instead
        #for i in re[2]:
        l.append( re )
    l.sort(key=OA)
    return l



DRAWINGS=CP_DIR(CP(['art_assets','blks']),o=1)
DR={k.split(SEP)[-1].split('.')[0]:k for k in DRAWINGS}

UIs=CP_DIR(CP(['art_assets','UIs']),o=1)
ui_assets={k.split(SEP)[-1].split('.')[0]:k for k in UIs}


DATA=CP_DIR(CP(['data']),o=1,r=1)
FONT=CP(['art_assets','Cascadia.ttf'])


print(ui_assets)

