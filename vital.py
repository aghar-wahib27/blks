
import pygame
import json
from abc import ABC,abstractmethod
from random import randint,choice
from copy import copy




pygame.init()
dims=(800,700)
scr=pygame.display.set_mode(dims)

GAME_STATE={
	"run":1,
	"UI":'ui_1',
	"level":"",
	"change":[1,1]
	}

LEVELS=['menofia','kahira','domyat','sharkia','helwan']



def load(path:str):
    with open(path,'r') as pth:
        data=json.load(pth)

    return data

def save(path:str,obj:any):
	with open( path,'w') as dta:
			    json.dump(obj,dta,indent="\t")

def surr(center:tuple):
	"""
	returns the surronding of an element in a matrix
	"""
	return [(i-1+center[0],j-1+center[1]) for i in range(3) for j in range(3)]

def ROUA(obj_li:list,req_data:list):
	"""
	ROUA : return_obj_upon_attr
	"""
	for obj in obj_li : 
		data=obj.get_data()
		if data[req_data[0]]==req_data[1]:
			return obj
		# else:
		# 	print (data[req_data[0]],req_data[1])

	return 'not_found'
			
def singleton(cls):
    instacne={}
    def new(*args,**kargs):
        if cls not in instacne:
            instacne[cls]=cls(*args,**kargs)
        return instacne[cls]
    return new

def CDBTP(p1:tuple,p2:tuple, dis=10):
    return ((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**0.5 #< dis:
    #     return 1
    # else:
    #     return 0

def neli(li:list):
	return li + [-i for i in li]

def freq(lis):
	element_counts = set(lis)
	most_frequent_element = max(element_counts, key=lis.count)
	return most_frequent_element

# print(freq([1,2,1,3,1,5,6,5,6,5,5,5,5,1]))


def GI(image,frame,height_frame,height,width,color) -> pygame.Surface: 
    """GI : get image

    """
    if height>0 and width>0 :
        img=pygame.Surface((width,height)).convert_alpha()
        img.set_colorkey(color)
        img.blit(image,(0,0),(width*frame,height_frame,width,height))
        return img
    else:
        image.set_colorkey(color)    
        return image

def GAL(i,start,width,height,height_frame):
    """GAL : get animation list
    """
    list=[]
    for i in range(i):
        frame=GI(start+i,width,height,(0,0,0),height_frame).convert()
        list.append(frame)
    return list
 

def GAL2(img,i,start,width,height,height_frame):
        """GAL : get animation list
        """
        list=[]
        for i in range(i):
            #frame=GI(img,start+i,width,height,(0,0,0),height_frame).convert()
            frame=GI(img,start+i,height_frame*height,height,width,color=(0,0,0)).convert()
            list.append(frame)
        return list



def REFL(ls:list,ii:list):
    """REFL : remove element from list

    """
    li=[]
    for i in ls: 
        sub_li=[]
        if type(i)==list:
            for si in i:  
                if si not in ii:
                    #print(si) 
                    sub_li.append(si)
            li.append(sub_li)
        else:
           if i not in ii:
                    #print(si) 
                    li.append(i) 
    return li


def GCNFM(no:int,dv:int=3,st=[0,1])->int:
    """
    GCNFM : get closest number from multiple
    
    get the closest (least or biggest upon `st`  number from a multiple of `dv` defaulted to 3
    
    ex: 13->12, 20->18, 15->15 if `st[0]`
    ex: 13->15, 20->21, 15->15 if `st[1]`
    
    """
    cu=no%dv
    if no%dv == 0:
       return no
    else:
        if st[0]:
            return (no-cu)
        if st[1]:
            return (no-cu)+3


def IOT(li:list, re:any)->list:
    """IOT : index of items ,lol I just coppied it from the internet

    returns the indices of reapting elemnt `re` in `li`
    
    Args:
        li: list to search the repeating element for
        re : reapeting element to be searched
        
    ex : `li`=[0,20,4,5,20] `re`=20 , return is [1,4]

    """
    
    index_val = [] 
    i=0 #counter
    while i != len(li):
        try:
            ind = li[i:].index(re) #checking the index this line trims the first part of the list that dosent contain any instance of re
            index_val.append(ind+i)
            i = ind+1+i
        except ValueError:
            i = len(li)
    return index_val

#R:NPC:3
def EDUL(text:str,lw:int=12,font_size:int=0)->tuple:
    """EDUL : extract dialouge upon legth 
    
    extract dialouge of an npc upon one long sentence
    
    it can be used to divide any text `text` to sentences with equal no of words   `lw`
    
    then turns them to pygame surface and append to a list to be returned with its length
    """
    
    ess:dict={'counter':[0,0],'words_to_ignore':['9','#'],"status":'',"list_of_sec":[],"a_list_of_sec":[],
                        'list_of_sur':[],"new_sen":[],'list_of_words':text.split()}
    
    for single in ess['list_of_words']:

        ess["counter"][0]+=1
        ess["counter"][1]+=1
        
        if ess['status']=='break':
            ess['status']=''
        if single=='9':
            ess['status']='break'  
            ess["counter"][0]=1
        
        if ess["counter"][0]%lw!=0  and ess['status']=='':
            if  not ess['words_to_ignore'].count(single) :
                ess['new_sen'].append(single)
        else:
            if ess['status']=='break' or ess["counter"][0]%lw==0 :  #casses where I break the line and add a new sentence
                if  not ess['words_to_ignore'].count(single) :
                    ess['new_sen'].append(single)
                               
            ess['list_of_sec'].append(ess['new_sen'])
            ess['new_sen']=[]
           
        
    if len(ess['list_of_words'])%lw!=0:
            nl=REFL(ess['list_of_words'],['9','@'])
            ng=IOT(nl,ess['list_of_sec'][-1][-1])[-1]+1
        
            ess['list_of_sec'].append(REFL(nl[ng:],['#']))
    
    ess['a_list_of_sec']=ess['list_of_sec'].copy()
    ess['list_of_sec']=REFL(ess['list_of_sec'],['@'])
    
    for list in ess['list_of_sec']:
            ess['list_of_sur'].append(_FONTS_[font_size+2].render(" ".join(list),True,(255,255,255)))

    return ess['list_of_sur'] , len(ess['list_of_sec']) ,ess['a_list_of_sec']     

def EDUS(text:str,font_size:int,allowed_width:int)->tuple :
    """EDUS : extract dialouge upon size
    
      to be written
    """
    ...


    
SYSTEMS={}

##### file extraction 




##################