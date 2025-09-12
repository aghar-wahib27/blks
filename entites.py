from extractor import DATA_DICT,SEP
from vital import load,save,ABC,abstractmethod,pygame,scr,singleton,BI,GAL3,choice,ROUA,GAME_STATE,DirectedAttrSearch

AllData={ k:load(v) for (k,v) in DATA_DICT.items() }


class DataSystem:
    def __init__(self):
        self.lists={'all':[]}

    def ChangeEntities(self,Entities:list,Changes:list):
        ents = []
        for name in Entities :
            ents.append( ROUA(self.lists['all'],['name',name])) 
        # print(ents,'this is the ents to be changed',Entities)
        for i in range(len(ents)):
            ents[i].ChangeData(Changes[i][0],Changes[i][1])

    def MapDataEntity(self,_name:str):
        for ent in self.lists['all']:
            print(ent.get_data(),len(self.lists['all']))
        return ROUA(self.lists['all'],['name',_name])

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

class entity:
    def __init__(self,name,data):
        self.n = name
        self.data = data

    def get_data(self):
        return {'name':self.n}


class DE(entity):
    """ DE : data entitiy
    """
    
    def __init__(self,_name:list,ap=1):
        # for n in self.n:
        # 	self.data=AllData[_name]
        # self.n=_name
        # self.data=AllData[_name]
        entity.__init__(self,name=_name,data=AllData[_name])
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

    def ChangeData(self,_attr,new_val):
         # GetAttrFromNestedObj(self.data,_attr,change=[1,new_val])
        DirectedAttrSearch(self.data,_attr,change=[1,new_val,1])
        self.save()
        # print(self.data)

    # def get_data(self):
    #     # print({'name':self.n})

    #     return {'name':self.n}

    def save(self):
        save(DATA_DICT[self.n],AllData[self.n])

def IntializeAllDataEntites():
    for name in AllData:
        DE(name)
IntializeAllDataEntites()

class concius(ABC):
    def __init__(self,ap=1,**kargs):
        self.actions=kargs['actions']
        self.count:dict={}

        for ke in kargs['counters']:
            self.count[ke]=[0,0]
        if ap:
            AI_SYS.lists['concius'].append(self)

    def counts(self,**kargs):
            """

            COUNERNAME = [ CONDTION TO START COUNTING , TYPE OF COUNTING + DURATION , CONDTION TO STOP COUNTING]
            COUNERNAME : must be a counter name passed to the init count kargs , if it ends with 'o' it will be played once 
            TYPE OF COUNTING : un for looping ,o for counting once 
            """
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

        self.FadeScreen = 0 

    def draw_rect(self):
        for rct in self.lists['rects']:
            pygame.draw.rect(scr,rct.color,rct.rect)
        
    def StartFade(self,changes=[0,0],fadePeriod=20,**kargs):
        GAME_STATE['fade'][0]=1
        GAME_STATE['fade'][1]=fadePeriod
        GAME_STATE['fade'][-1]=1
        if changes[0]:
            GAME_STATE['change'][0]=1
            GAME_STATE['UI']=kargs['new_ui']

        if changes[1]:
            GAME_STATE['change'][1]=1
            GAME_STATE['level']=kargs['new_level']
    
    def BgFade(self):
        if GAME_STATE['fade'][0] == 1 :
            self.FadeScreen.style['fade'][1]=10
            self.FadeScreen.style['fade'][0]=10
            GAME_STATE['fade'][0]=0

        if self.FadeScreen.style['fade'][0] >=255 and GAME_STATE['fade'][1]:
            GAME_STATE['fade'][1] += -1
            if GAME_STATE['fade'][1]==15:
                GAME_STATE['fade'][-1]=0
            if GAME_STATE['fade'][1]==0:
                GAME_STATE['fade'][0]=2

        
        if GAME_STATE['fade'][0] == 2:
            self.FadeScreen.style['fade'][1] = -10
            self.FadeScreen.style['fade'][0]=255
            GAME_STATE['fade'][0]=0

        self.FadeScreen.AnimationPlayer()

    def Manage(self):

        for ent in self.lists['ents']:
            ent.AnimationPlayer()

        self.BgFade()

ANIM_SYS=AimationSystem()

def AnimationTypes()->list: 

    def put(oe:any):
        oe.display.blit(oe.img,oe.pos)
    
    def fade(oe:any):
        oe.img.set_alpha(oe.style['fade'][0])
        if 9< oe.style['fade'][0]<256:
            oe.style['fade'][0] += oe.style['fade'][1]
            print('fading in or out',oe.style['fade'])
        oe.display.blit(oe.img,oe.pos)

    def BackGroundPut(oe:any):
        oe.main_sur.blit(oe.img,oe.pos)
        for anim in oe.anims:
            anim.AnimationPlayer()
        oe.display.blit(BI(oe.main_sur,oe.blur),oe.pos)


    def AllAnimationsController(oe:any):
            """ACC : All Animations Controller 
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
            

            if oe.anim[oe.anim['_n_'][2]][1]  == len(oe.OBJ[oe.anim['_n_'][2]]) :
                
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
                oe.display.blit(oe.OBJ[oe.anim['_n_'][2]][oe.anim [ oe.anim['_n_'][2] ] [1]],oe.pos)
            else:
                oe.d.blit(pygame.transform.flip(oe.OBJ[oe.anim['_n_'][2]][oe.anim [ oe.anim['_n_'][2] ] [1]],True,False),oe.pos)

    def BackGroundAnimtaion(oe:any):
        oe.anim[0]+=1

        if oe.anim[0]==oe.anim[2]:
            oe.anim[0]=0
            oe.anim[1]+=1

        if oe.anim[1]==len(oe.frames):
            oe.anim[1]=0
            oe.anim[2]=choice(oe.speeds)

        oe.display.blit(oe.frames[oe.anim[1]],oe.pos)

    return {'P':put,'BP':BackGroundPut,'ACC':AllAnimationsController,"BGA":BackGroundAnimtaion,'FD':fade}

AT=AnimationTypes()

class Animation:
    def __init__(self,ap=1,**kargs):
        if type(kargs['type']) == list :
            self.animationfunc = { k : AT[ k ] for k in kargs['type']}
        else:
            self.animationfunc=AT[kargs['type']]
        self.display=kargs['display']
        self.pos=kargs['position']

        if ap:
            ANIM_SYS.lists['ents'].append(self)

    
    def remove(self):
        if self in ANIM_SYS.lists['ents']: 
            ANIM_SYS.lists['ents'].remove(self)


    def AnimationPlayer(self):
        self.animationfunc(self)

class AnimationFactory:
    
    @staticmethod
    def AnimationObject(**kargs)->Animation:
        AO=Animation(ap=kargs['ap'],type=kargs['type'],display=kargs['display'],position=kargs['position'])
        AO.img=kargs['img']
        AO.style = {}
        if 'fade' in kargs:
            AO.style['fade'] = [5,0,10]
        if 'resize' in kargs:
            AO.img=pygame.transform.scale(AO.img,kargs['resize'])   
        return AO

    @staticmethod
    def AnimationEntity(**kargs)->Animation:
        AE=Animation(type='ACC',display=scr,position=kargs['position'])
        AE.anim:dict[str,list]={k:v for (k,v) in zip( [i for i in kargs['keys']] , [i for i in kargs['args']]) }
        AE.AA=kargs['all_animations']       
        return AE

    @staticmethod
    def BackGroundAnimation(**kargs)->Animation:
        BGA=Animation(ap=0,type='BGA',display=kargs['display'],position=kargs['position'])
        BGA.frames=GAL3(img=kargs['img'],no_of_frames=kargs['nf'],start=kargs['start'],w=kargs['w'],h=kargs['h'])
        BGA.speeds=kargs['fr_speed']
        BGA.anim=[0,0,choice(BGA.speeds)]
        BGA.layer=kargs['layer']

        return BGA

    @staticmethod
    def Background(**kargs)->Animation:
        BG=AnimationFactory.AnimationObject(ap=0,img=kargs['img'],type='BP',display=scr,position=(0,0),resize=scr.get_size())
        BG.main_sur=pygame.Surface(BG.img.get_size())
        # BG.display=BG.main_sur
        BG.main_sur.set_colorkey((0,0,0))
        BG.blur=kargs['blur']
        return BG


    @staticmethod
    def UiAnimation(**kargs)->Animation:
        uia=AnimationFactory.AnimationObject(type='BGA',display=scr,position=kargs['position'])
        return uia

    ANIMS={"AO":AnimationObject,"AE":AnimationEntity,"BGA":BackGroundAnimation,"BG":Background,"UIA":UiAnimation}

AnimF=AnimationFactory()

class BackGround:
    def __init__(self,**kargs):
        self.bgs={
            k:v for (k,v) in 
                zip(
                    [name for name in kargs['bg_names']],[img for img in kargs['bg_imgs'] ]
                    )
                }

        self.bg_anims=kargs['bg_ainmations']
        for anim in self.bg_anims:
            anim.display=self.bgs[anim.layer].main_sur

        for bg in self.bgs:
            self.bgs[bg].anims=[bg_anim for bg_anim in self.bg_anims if bg_anim.layer == bg ]


        self.bgs_list=[self.bgs[ord_name] for ord_name in sorted(self.bgs.keys(),key=lambda x:int(x[-1]))]
        ANIM_SYS.lists['ents'].extend(self.bgs_list)
    




class container:
    def __init__(self):
        self.entities=[]
        self.inter={}
    
    def clear(self):
        self.entities.clear()


@singleton
class EventHandler:
    def __init__(self):

        self.events={
            k:[] for k in 
                ['mouse_down','mouse_released','key_down'
                ,'mouse_pos','esc','space']
                }

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



def clearanims():
    ANIM_SYS.lists['ents'].clear()

