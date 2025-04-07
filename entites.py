
from extractor import DATA,SEP
from vital import load,save,ABC,abstractmethod,pygame,scr,singleton


AllData={k.split(SEP)[-1].replace('.json',''):load(k) for k in DATA }


class DataSystem:
    def __init__(self):
        self.lists={'all':[]}

    @staticmethod
    def save_last_pos(**kargs):
        for ke in kargs.keys():
            AllData['game_status']['last_pos_info'][ke]=kargs[ke]

        print(AllData['game_status'],'have saved')
        		
        # save(JSONs['game_status'],AllData['game_status'])

    def Manage(self):
        for ent in self.lists['all']:
            ent.save()

class AiSystem:
    """
    uses singleton pattern
    """
    def __init__(self):
        self.lists:dict[str,list]={"concius":[]}

    def Manage(self):
        for ai_ent in self.lists['concius']:
            ai_ent.behavior()


AI_SYS=AiSystem()

DT_SYS=DataSystem()



class DE:
    """ DE : data entitiy
    """
    def __init__(self,_name:list,ap=1):
        # for n in self.n:
        # 	self.data=AllData[_name]
        self.n=_name
        self.data=AllData[_name]
        if ap :
            DT_SYS.lists['all'].append(self)


    def modify_data(self,gr:str,__type:any,mod:any):
        if __type==int:
            self.data[gr]+=mod

        if __type==list:
            self.data[gr].extend(mod)

        if __type==dict:
            for ke in mod.keys():
                self.data[gr][ke]=mod[ke]

    def save(self):

    # with open(JSONs[self.n[0]],'w') as d:    
    #     		json.dump(AllData[self.n[0]],d,indent="\t")
        # save(JSONs[self.n[0]],AllData[self.n[0]])
        ...

class concius(ABC):
    def __init__(self,ap=1,**kargs):
        self.actions=kargs['actions']
        self.count:dict={}

        for ke in kargs['counters']:
            self.count[ke]=[0,0]
        if ap:
            AI_SYS.lists['concius'].append(self)

    def counts(self,**kargs):
            for k in kargs.keys():
              
                if kargs[k][0] and self.count[k][1]>=0:
                    self.count[k][1]=1

                if kargs[k][1].split('+')[0]=='un':
                    if self.count[k][0] == int(kargs[k][1].split('+')[1]) :
                        #self.count.pop(k)
                        if k[-1]=='o':
                            self.count[k][1]=-1
                        else:
                            self.count[k][1]=0
                        self.count[k][0]=0


                if kargs[k][2]:
                    if k[-1]=='o':
                        self.count[k][1]=-1
                    else:
                        self.count[k][1]=0
                        self.count[k][0]=0

                if self.count[k][1]>0:
                    self.count[k][0]+=1

    def inter(self,**kargs):
        for act in kargs.keys():
            for tpl in kargs[act]:
                if tpl[1]:
                    if self.actions[act]!=tpl[0]:
                        self.actions[act]=tpl[0]

    @abstractmethod
    def behavior(self):
        ...


class AimationSystem:
    """
    uses singleton pattern
    """
    def __init__(self):
        self.lists={'ents':[],'rects':[]}
        self.bgs={"layers":{},"wallpapers":{}}
        self.layers={}

    def append_layers(self):
        tr=set()
        for bg in self.bgs["wallpapers"].keys():
            tr.add(bg.split("_")[0])

        for lr in tr :
            self.bgs['layer_s'][f'layer_{lr}']={}

        for bg in self.bgs["wallpapers"]:
            self.bgs['layers'][f'layer_{bg.split("_")[0]}'][bg]=(self.bgs['wallpapers'][bg])

        for layer in self.bgs['layer'].keys():
            self.bgs['layer'][layer].append(
                pygame.Surface(
                    (
                        max([i.get_width() for i in self.bgs['layer'][layer]]),
                        max([i.get_height() for i in self.bgs['layer'][layer]])

                        )
                    )
                )

    def draw_rect(self):
        for rct in self.lists['rects']:
            pygame.draw.rect(scr,rct.color,rct.rect)
        
    def Manage(self):
        for ent in self.lists['ents']:
            ent.AnimationPlayer()


ANIM_SYS=AimationSystem()

def put(main:pygame.Surface,img:pygame.Surface,pos:tuple):
    main.blit(img,pos)

def AG(oe:any,OBJ:dict,sur:pygame.Surface,pos:tuple):

    if oe.anim['_n_'][-1]=='right':
            put(sur,OBJ[oe.anim['_n_'][2]][oe.anim [ oe.anim['_n_'][2] ] [1]],pos)
    else:
            put(sur,pygame.transform.flip(OBJ[oe.anim['_n_'][2]][oe.anim [ oe.anim['_n_'][2] ] [1]],True,False),pos)


    # if oe.actions['allow_moveing']:

    if oe.anim[oe.anim['_n_'][2]][0] != oe.anim[oe.anim['_n_'][2]][2]:
        oe.anim[oe.anim['_n_'][2]][0]+=1
    else:
        oe.anim[oe.anim['_n_'][2]][0]=0
        oe.anim[oe.anim['_n_'][2]][1]+=1

    if oe.anim[oe.anim['_n_'][2]][1]  == len(OBJ[oe.anim['_n_'][2]]) :
            
            oe.anim[oe.anim['_n_'][2]][1]=0

            if oe.anim[oe.anim['_n_'][2]][-1]=='o':
                oe.anim['change_anim']=1
                oe.anim['_n_'][0]=oe.anim['_n_'][1] 
    
    if oe.anim['change_anim']==1:
        if oe.anim["_n_"][0] in oe.anim["cha"]:
                ne=oe.anim['_n_'][0] + oe.anim["_n_"][3]
        else:
                ne=oe.anim['_n_'][0]
        
        oe.anim['_n_'][2]=ne

        oe.anim[oe.anim['_n_'][2]][1]=0
        oe.anim[oe.anim['_n_'][2]][0]=0
    oe.anim['_n_'][-1]=oe.anim['_n_'][-2]  

def AAC(oe:any,OBJ:dict,d:pygame.Surface,pos:tuple):
        """ACC : All Animations Controller l l l l l 
        """
        if  0<oe.actions['allow_moveing']<3 :
            #self.anim['_n_'][3]='cd'
            if oe.anim["_n_"][0] in oe.anim["cha"]:
                ne=oe.anim['_n_'][0] + oe.anim["_n_"][3]
            else:
                ne=oe.anim['_n_'][0]
            
            oe.anim['_n_'][2]=ne
            oe.anim[oe.anim['_n_'][2]][1]=0
            oe.anim[oe.anim['_n_'][2]][0]=0
            oe.anim['_n_'][-1]=oe.anim['_n_'][-2]  

        if oe.anim[oe.anim['_n_'][2]][0] != oe.anim[oe.anim['_n_'][2]][2]:
            oe.anim[oe.anim['_n_'][2]][0]+=1
        else:
            oe.anim[oe.anim['_n_'][2]][0]=0
            oe.anim[oe.anim['_n_'][2]][1]+=1
        

        if oe.anim[oe.anim['_n_'][2]][1]  == len(OBJ[oe.anim['_n_'][2]]) :
            
            # oe.anim[oe.anim['_n_'][2]][1]=0
            oe.anim[oe.anim['_n_'][2]][1]=0

            if oe.anim[oe.anim['_n_'][2]][-1]=='o':
                oe.actions['allow_moveing']=1
                oe.anim['_n_'][0]=oe.anim['_n_'][1] 
            
               
            
        
        # print( oe.anim['_n_'][:3],oe.actions['allow_moveing'],oe.anim [ oe.anim['_n_'][2] ] )        
        if oe.anim[oe.anim['_n_'][2]][-1]=='o':
                oe.actions['allow_moveing']=3
                
        if oe.anim[oe.anim['_n_'][2]][-1]=='p':
                oe.actions['allow_moveing']=0
                #oe.AM()

        # print( oe.anim['_n_'][2] , oe.anim [ oe.anim['_n_'][2] ])
           
        if oe.anim['_n_'][-1]=='right':
            d.blit(OBJ[oe.anim['_n_'][2]][oe.anim [ oe.anim['_n_'][2] ] [1]],pos)
        else:
            d.blit(pygame.transform.flip(OBJ[oe.anim['_n_'][2]][oe.anim [ oe.anim['_n_'][2] ] [1]],True,False),pos)


class Animation(ABC):

    @abstractmethod
    def AnimationPlayer(self):
        ...


class AO(Animation):
    """
    AO : animation object 
    """
    def __init__(self,ap=1,**kargs):

        self.img=kargs['img']
        self.display=kargs['display'] 
        self.pos=kargs['pos']   
        if 'resize' in kargs:
            self.img=pygame.transform.scale(self.img,kargs['resize'])   
        
        if ap:
            ANIM_SYS.lists['ents'].append(self)

    def remove(self):
        ANIM_SYS.lists['ents'].remove(self)

    def AnimationPlayer(self):
        put(self.display,self.img,self.pos)

class AE(Animation):
    """
    AE : animation entity 
    """
    def __init__(self,ap=1,**kargs):
        self.anim:dict[str,list]={k:v for (k,v) in zip( [i for i in kargs['keys']] , [i for i in kargs['args']]) }
        self.AA=kargs['all_animations']
        self.off_set=kargs['pos']
        self.display=kargs['display']        
        if ap:
            ANIM_SYS.lists['ents'].append(self)

    def AnimationPlayer(self):
            AG(self,self.AA,self.display,(self.rect.x-self.off_set[0],self.rect.y-self.off_set[1]))

    def StopParallyze(self,**kargs):    
        for act in kargs.keys():
            for tpl in kargs[act]:
                if tpl[1]:
                    if self.actions[act]!=tpl[0]:
                        self.actions[act]=tpl[0]

    def CA(self,list_of_conds:list):
        self.anim['change_anim']=0    
        for cond in list_of_conds:
            if cond:
                self.anim['change_anim']=1

    def DAS(self,**kargs):
        """
        DAS : determine animtions state
        """
        for k in kargs.keys():
            if kargs[k][0]:
                self.anim['_n_'][0]=kargs[k][-1]
                if kargs[k][-1] in self.anim['cha']:
                    self.anim["_n_"][0]+=f'_{kargs[k][1]}'

                if self.anim[k][-1]=="o":
                    self.anim["_n_"][1]=kargs[k][2]


class container:
    def __init__(self):
        self.entities=[]
        self.inter={}
    
    def clear(self):
        self.entities.clear()




@singleton
class EventHandler:
    def __init__(self):
        self.events={'mouse_down':[],'mouse_released':[],"key_down":[],'mouse_pos':[],'esc':[],'space':[]}
        self.actions={k:0 for k in self.events}

    def append(self,groups:list,ent:any):
        for gr in groups:
            self.events[gr].append(ent)

    def update_event(self,event='',val=1):
        for ent in self.events[event]:
            ent.events[event]=val

Handler=EventHandler()

class EE:
    def __init__(self,events:list):
        self.events={k:0 if k!='mouse_pos' else (0,0)   for k in events}

        Handler.append(groups=[evt for evt in self.events],ent=self)





