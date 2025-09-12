
import pygame
import json
from abc import ABC,abstractmethod
from random import randint,choice
from copy import copy,deepcopy



pygame.init()
dims=(800,700)
scr=pygame.display.set_mode(dims)

GAME_STATE={
	"run":1,
	"UI":'ui_1',
	"level":"",
	"change":[1,0],
    "fade":[0,0,0]
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
		# print(data,'this is roua')
		if data[req_data[0]]==req_data[1]:
			return obj
		# else:
		# 	print (data[req_data[0]],req_data[1])

	return 'not_found'
			
def GetColoumsOf2DArray(matrix:list):
    cols = [ [] for _ in range(len(matrix[0])) ]
    
    for row in matrix:
        for blk_index,blk in enumerate(row):
            cols[blk_index].append(blk)
            
    return cols

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
    """
    GetMostFrequentElementInList
    """
    element_counts = set(lis)
    if lis :
        most_frequent_element = max(element_counts, key=lis.count)
        return most_frequent_element
    else : 
        return 0 

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

def CDFL(lis:list):
	"""
	combine dictionaries from list of dictionaries
	"""
	dic={}
	for di in lis:
		for ke in di.keys():
			dic[ke]=di[ke]

	return dic

class DataModifer:
    @staticmethod
    def GetAttrFromNestedObj(obj:dict,attr:str,change=[0,0]):
        """
        write discription here 
        """
        search = 1 
        if change[0]:
            co = obj
        else:
            co = copy.deepcopy(obj)

        next_level_objs = [co]
        value = 0
        while search: 
            co = next_level_objs[0]
            next_level_objs.pop(0)
            for k in co.keys():

                if k == attr:
                    if change[0]:
                        co[k]=change[1]
                    value = co[k]
                    search = 0

                if type(co[k])==dict:
                    next_level_objs.append(co[k])
            
        return value 

def TurnListIntoDict(__lis:list,change=0):
    if change:
        co = __lis
    else:
        co = deepcopy(__lis)
    return { str(k):co[k] for k in range(len(co)) }

def GetAttrFromNestedObj(obj:dict,attr:str,change=[0,0,0]):
    """
    write discription here 
    this function has two jobs searching a nested dictionary and changeing a value in it which is a bas design
    """
    search = 1 
    if change[0]:
        co = obj
    else:
        co = copy.deepcopy(obj)

    next_level_objs = [co]
    value = 0
    while search: 
        co = next_level_objs[0]
        next_level_objs.pop(0)
        for k in co.keys():

            if k == attr:
                if change[0]:
                    if change[1]!=None:
                        co[k]=change[1]
                value = co[k]
                search = 0

            if type(co[k])==dict:
                next_level_objs.append(co[k])
    if type(value) == list :
        value = TurnListIntoDict(value,change=1)
    return value 

def DirectedAttrSearch(obj,attrs:str,change=[0,0,1]):
    attrsList = [attrs] if '+' not in attrs else attrs.split('+')
    print(attrsList)
    if change[2]:
        objCopy = obj
    else:
        objCopy = deepcopy(obj)
    for attr in attrsList:
        ch = [1,None,1] if attrsList.index(attr)!=len(attrsList)-1 else change
        # print(ch)
        objCopy = GetAttrFromNestedObj(objCopy,attr,change=ch)
        # print(objCopy)
    return objCopy

def flatten(lis:list):
	"""
	combine nested lists into one big list
	"""
	lu=[]
	h=copy(lis)
	for i in h:
		if type(i)!= list:
			lu.append(i)
		else:
			lu.extend(flatten(i))
			
	return lu

def NodeFlatten(lis:list):
	"""
	flatten the node herarichy provided the root node only print
	"""
	h=[copy(lis)]
	reached_bottom=0
	while not reached_bottom:
		lu=[]
		for n in h[-1]:
			lu.append(n.children)
		h.append( REFL(flatten(lu),[None]))
		if 'node' in [i.t for i in h[-1]]:
			reached_bottom=0
		else:
			reached_bottom=1

	return flatten(h)


def SN(parent:any,name:str):
	"""
	search node
	"""
	nodes=copy(parent.children)
	nodes.append(parent)
	s=1

	while s:
		search=ROUA(nodes,['nodename',name])
		# print('nodes ate',[i.nodename for i in nodes])
		if type(search) !=str:
			return search
		else:
			nodes= flatten([n.children for n in nodes if n.t!='leaf'])



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


def WOW(word:str,font_size:int):
    return (len(word)+1)*font_size

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
    
    # for list in ess['list_of_sec']:
    #         ess['list_of_sur'].append(_FONTS_[font_size+2].render(" ".join(list),True,(255,255,255)))

    return ess['list_of_sur'] , len(ess['list_of_sec']) ,ess['list_of_sec']     


def EDUS(text:str,allowed_width:int,Font:any)->list :
    """EDUS : extract dialouge upon size
    
      to be written
    """
    ess:dict={'acc_width':0,'words_to_ignore':['9','#'],"status":'',"list_of_sec":[],"a_list_of_sec":[],
                        'list_of_sur':[],"new_sen":[],'list_of_words':text.split(),'fs':0,'gs':0,'gaps':0}

    ess['fs']=Font.render(ess['list_of_words'][0],1,(0,0,0)).get_width()//len(ess['list_of_words'][0])


    for single in ess['list_of_words']:


        if sum([WOW(wr,ess['fs']) for wr in ess['new_sen']+[single] ]) > allowed_width or single =='9' :
            ess['status']='break'
 
        if single not in ess['words_to_ignore']:
            ess['acc_width']+=WOW(single,ess['fs'])

       


        if ess['status']=='break':
            ess['status']=''
            ess['acc_width']=0

        if ess['acc_width']==0:
        
            # if single not in ess['words_to_ignore'] :
            #         ess['new_sen'].append(single)
                               
            ess['list_of_sec'].append(ess['new_sen'])
            ess['new_sen']=[]


        if ess['status']=='':
                print(ess['acc_width'],ess['fs'],single)

                if single not in ess['words_to_ignore'] :
	                ess['new_sen'].append(single)

    if len(ess['new_sen']):
            ess['list_of_sec'].append(ess['new_sen'])



    for lis in ess['list_of_sec']:
            ess['list_of_sur'].append(Font.render(" ".join(lis),True,(255,255,255)))

    return [ess['list_of_sur'] , len(ess['list_of_sec']),ess['fs'] ,ess['list_of_sec'] ]


def GI2(image,frame,height_frame,height,width,color=(0,0,0)) -> pygame.Surface: 
        """GI : get image

        """
        #print(width,height)
        img=pygame.Surface((width,height)).convert_alpha()
        img.set_colorkey(color)
        img.blit(image,(0,0),(width*frame,height_frame,width,height))
        return img

def GAL2(img,i,start,width,height,height_frame):
        """GAL : get animation list
        """
        list=[]
        for i in range(i):
            #frame=GI(img,start+i,width,height,(0,0,0),height_frame).convert()
            frame=GI2(img,start+i,height_frame*height,height,width,color=(0,0,0)).convert()
            list.append(frame)
        #ignore_c(list,c=(253,77,79))
        return list

def GI3(**kargs) -> pygame.Surface: 
        """GI : get image

        """
        #print(width,height)
        img=pygame.Surface((kargs['width'],kargs['height'])).convert_alpha()
        img.set_colorkey(kargs['color'])
        img.blit(kargs['img'],(0,0),(kargs['width']*kargs['start'][0],kargs['height']*kargs['start'][1],kargs['width'],kargs['height']))
        return img

def GAL3(**kargs):
        """GAL : get animation list
        """
        list=[]
        for i in range(kargs['no_of_frames']):
            frame=GI3(img=kargs['img'],start=[kargs['start'][0]+i,kargs['start'][1]],height=kargs['h'],width=kargs['w'],color=(0,0,0)).convert()
            list.append(frame)

        return list

def GAS(anim_obj:dict,sprites_paths:list) -> dict:
    """GAS : get all sprites

    Args:
        anim_obj (dict): a dict of dict ,each one of the child dict contains a `_n_`  and an `anim` key for more info refer the `docm.txt` section `R:A`
        sprites_paths (list): list containing paths for png files 

    Returns:
        dict: dict of animations name and thier corspnding pygame surfaces
         
    """
     
    
    
    SPRITES={
    k:v for (k,v) in 
           zip(
               sorted([anim_obj[i]["_n_"] for i in anim_obj],key=lambda ce: ce[0:3]),
               [pygame.image.load(i) for i in sprites_paths]
               )
           }
    
    SURFACES={
    k:v for (k,v) in 
           zip(
               [anim_obj[i]["_n_"] for i in anim_obj],
               [ [GAL2(SPRITES[i[0]],i[1],0,i[3],i[4],k) for k in range(i[2])] for i in   [i for i in [ i['anim']['info'] for i in [i for i in anim_obj.values()]] ]  ]
               )
           }
    
    ANIM_DATA={k:v for (k,v) in zip([i for i in anim_obj],[anim_obj[i]['anim'] for i in anim_obj])}
    
    ANIM_INFO=[ (i,f,ANIM_DATA[i][f],SURFACES[i][ANIM_DATA[i][f][0]-1][ANIM_DATA[i][f][1]:ANIM_DATA[i][f][2]])  for i,j in ANIM_DATA.items() for f in j if f!='info'  ]
    
    ALL_ANIM={k:{i[1] : i[3] for i in ANIM_INFO if i[0]==k} for (k,_) in ANIM_DATA.items() }
    
    return ALL_ANIM
    
def RI(img:pygame.Surface,new_size:tuple):
	return pygame.transform.scale(img,new_size)

def BI(img:pygame.Surface,factor:int):
	return pygame.transform.box_blur(img,factor)

SYSTEMS={}

##### file extraction 




##################
