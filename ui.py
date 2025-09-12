from entites import concius,abstractmethod,DE,container,EE,BackGround,AnimF,ANIM_SYS,AllData,DT_SYS
from vital import pygame,CDBTP,singleton,ROUA,SYSTEMS,scr,GAME_STATE,EDUS,EDUL,BI,SN,flatten,NodeFlatten
from art_assets import UIS,FFF,FFFF,_FONTS_
from clay_pythonized import *


ANIM_SYS.FadeScreen = AnimF.ANIMS['AO'](ap=0,img=UIS['fade'],type='FD',display=scr,position=(0,0),fade='',resize=scr.get_size())

class ui(concius,EE,Node):
    def __init__(self,_name:str):
        # self.de=AllData[_name]
        # DE.__init__(self,_name)
        self.de = DT_SYS.MapDataEntity(_name)
        self.name=_name
        self.positions=[]
        self.components=[]
        concius.__init__(
            self,
            actions={'running':0},
            counters={'transion':20}
            )

        self.bgs=BackGround(
            bg_names=self.de.data['back_ground'],
            bg_imgs=
                [
                    AnimF.ANIMS['BG'](
                        img=UIS[i],
                        blur= 0 if 'blur' not in self.de.data['back_ground'][i] else self.de.data['back_ground'][i]['blur']
                        )
                 for i in self.de.data['back_ground']
                 ],
            bg_ainmations=[
                    AnimF.ANIMS['BGA'](
                                img=UIS[f[0]],
                                start=[0,0],
                                w=f[-2],
                                h=f[-1],
                                display=scr,
                                nf=f[3],
                                fr_speed=range(f[-4],f[-3]),
                                position=(f[1],f[2]),
                                layer=i
                                )
                    for i in self.de.data['back_ground'] for f in self.de.data['back_ground'][i]['anims']
                    ]
            )
        

        EE.__init__(
            self,
            events=['mouse_down','mouse_released','mouse_pos']
            )

        RootNode.__init__(
            self,
            [],
            sizing=list(scr.get_size()),
            pos_data={'padding':self.de.data['padding'],'gap':self.de.data['gap'],'mode':self.de.data['mode']}
            )

        print('size of scr',self.size,scr.get_size())

        self.all_nodes=[]
        self.include_node_containers()

    def include_node_containers(self):
        for cont in self.de.data['containers']:
            c=Node(
                    _dir=cont['dir'],
                    parent=SN(self,cont['parent_name']),
                    children=[],
                    name=cont['name'],
                    width_size_type=cont['sizing'][0],
                    height_size_type=cont['sizing'][1],
                    pos_data=cont['spacing']
                    )

    def behavior(self):
        for child in self.all_nodes:
            pygame.draw.rect(scr,(child.size['w']%155,child.size['h']%155,50),child.noderect)

        for comp in self.components:
            comp.behavior()
            # pygame.draw.rect(scr,(200,100,50),comp.rect)

        self.events['mouse_down']=0

    def clear(self):
        for nd in self.all_nodes:
            if nd.t=='leaf':
                nd.a.remove()

        self.children.clear()

        for bg in self.bgs.bgs_list:
            bg.remove()

        # for bg_anim in self.bgs.bg_anims:
        #   bg_anim.remove()


@singleton
class UIs(container):
    def __init__(self):
        container.__init__(self)
        self.general_components={}


        
        

SYSTEMS['ui']=UIs()


class TextWrapper(Node):
    def __init__(self,**kargs):
        LeafNode.__init__(
            self,
            kargs['parent'],
            f'text_{kargs['parent'].nodename}_{kargs['subname']}',
            {}
            )

        self.a=AnimF.ANIMS['AO'](
                        ap=1,
                        type='P',
                        img=_FONTS_['25'].render(kargs['sur'],True,(250,250,250)),
                        display=scr,
                        position=self.noderect.topleft
                        )
        # self.TextWrap( sur='hello '+kargs['sur']+' ',parent = kargs['parent'])
        # self.dir = 'UTD'
        self.Text = kargs['sur']
        self.size={'w':self.a.img.get_width(),'h':self.a.img.get_height()}
        self.resize(update=0)

    def NodePositioning(self):
        self.a.pos=self.noderect.topleft

    def TextWrap(**kargs):
        texts=EDUS(kargs['sur'],kargs['parent'].noderect.width,_FONTS_['25'])[-1]
        for sen in texts:
            TextWrapper(parent=kargs['parent'],sur=" ".join(sen),subname=texts)



class ImageNode(Node):
    def __init__(self,**kargs):
        LeafNode.__init__(
            self,
            kargs['parent'],
            f'img_{kargs['parent'].nodename}_{kargs['subname']}',
            {}
            )
        self.a=AnimF.ANIMS['AO'](
                        ap=1,
                        type='P',
                        img=UIS[kargs['sur']],
                        display=scr,
                        position=self.noderect.topleft
                        )

        self.size={'w':self.a.img.get_width(),'h':self.a.img.get_height()}
        self.resize(update=0)


    def NodePositioning(self):
        self.a.pos=self.noderect.topleft


leafnodes={'text':TextWrapper,'img':ImageNode}

def WrapText(group:list):
    for node in [i for i in group if 'text' in i.nodename]:
            # for sr in node.nodeparent.data['children']['text']:
            # st=node.nodeparent.data['children']['text'][0]
            if node.size['w']>node.nodeparent.size['w']:
                # print('wrap testx',st)
                node.a.remove()
                node.nodeparent.children.remove(node)
                TextWrapper.TextWrap(
                        sur = node.Text,
                        parent = node.nodeparent,
                        subname = node.Text 
                        )

class ui_component(concius):
    def __init__(self,ui,_name,**kargs):
        self.parent=ui
        for comp in self.parent.de.data['components']:
            if comp['name']==_name:
                self.data=comp

        concius.__init__(
                self,
                actions=kargs['actions'],
                counters=kargs['counters']
                )


        Node.__init__(
                self,
                parent=SN(self.parent,self.data['parent_name']),
                children=[],
                name=f'{self.data['type']}_{_name}',
                width_size_type='fit_w', height_size_type='fit_h',
                pos_data=self.data['spacing']
                )

        self.rect=self.noderect
        for type,lns in self.data['children'].items():
            [leafnodes[type](parent=self,sur=ln,subname=ln) for ln in lns ]



    def get_data(self):
        return {'name':self.data['name'],'nodename':self.nodename}

    @abstractmethod
    def behavior(self):
        ...


def Functionailty():
    def GameData(dta):
        if dta['system']=="UI":
            GAME_STATE['change'][0]=1
        if dta['system']=="level":
                GAME_STATE['change'][1]=1
        if dta['system']:
            GAME_STATE[dta['system']]=dta['state']

    def Fade(dta):
            ANIM_SYS.StartFade(changes=dta['data'][0],new_ui=dta['data'][1],new_level=dta['data'][2])

    def EntData():
        ...

    return {'game_state':GameData,"entity":EntData,'fade':Fade}

funcs=Functionailty()

def ButtonActions():
    def hover(btn,**kargs):
        if CDBTP(btn.rect.center,list(kargs['mouse_pos']),btn.rect.width//2):
            if not btn.actions['hover'][0] and btn.rect.collidepoint(kargs['mouse_pos']):
                btn.actions['hover'][0]=1
                mod=ROUA(btn.parent.components,['name',kargs['btn_data']['func'][0]])
                print(mod,kargs['btn_data'])
                if type(mod) != str :
                    # btn.actions['hover'][1]=mod.actions[kargs['btn_data'][1]]
                    mod.actions[kargs['btn_data']['func'][1]]=kargs['btn_data']['func'][-1]
                    mod.actions['change'] = kargs['btn_data']['func'][2]    
            if btn.actions['hover'][0] and not btn.rect.collidepoint(kargs['mouse_pos']) : ### upon unhovering
                btn.actions['hover'][0]=0
                mod=ROUA(btn.parent.components,['name',kargs['btn_data']['func'][0]])
                # print('unhovered')
                if type(mod) != str: 
                    mod.actions['hover'][0]=0
                    mod.actions[kargs['btn_data']['func'][1]]=0
                # if type(mod) != str :
                #   mod.actions[kargs['btn_data'][1]]=btn.actions['hover'][1]


            
    def click(btn,**kargs):
        if btn.rect.collidepoint(kargs['mouse_pos']):
            if kargs['mouse_clicked'] :
                print('clicked',btn.data['name'],kargs['mouse_pos'],btn.rect.center)
                funcs[kargs['btn_data']['modify']](dta=kargs['btn_data'])


    return {'hover':hover,'click':click}

BtnInters=ButtonActions()

class button(ui_component,Node):
    def __init__(self,_name,parent):
        # self.text=FFF.render(_name,True,(150,150,150))
        ui_component.__init__(
                    self,
                    ui=parent,
                    _name=_name,
                    actions={'hover':[0,0],'clicked':0,'color':(255,255,255)},
                    counters=[],
                    )

        self.resize()

    def behavior(self):
        # pygame.draw.rect(scr,(self.size['w'],self.size['h'],50),self.children[0].noderect)

        for func in self.data['func']:
            BtnInters[func['respond']](
                                        btn=self,
                                        mouse_pos=self.parent.events['mouse_pos'],
                                        mouse_clicked=self.parent.events['mouse_down'],
                                        btn_data=func
                                        )



class representer(ui_component,Node):
    def __init__(self,_name,parent):
        ui_component.__init__(
                self,
                ui=parent,
                _name=_name,
                actions={'show':0,'hover':[0,0],'change':{'img':[],'txt':[],'ch':[0,0]},'clicked':0,'color':(255,255,255)},
                counters=[],
                )
        self.dir = "UTD" if 'dir' not in self.data.keys() else self.data['dir']
        if "width_size_type" in self.data['spacing']:
            self.size_data['w'][0]= self.data['spacing']["width_size_type"]

        if "height_size_type" in self.data['spacing']:
            self.size_data['h'][0]= self.data['spacing']["height_size_type"]

    def behavior(self):
        if self.actions['show'] and self.actions['hover'][0] == 0:
            
            for child in self.children:
                # if 'book' not in child.nodename:
                    child.a.remove()
                    # self.children.remove(child)

            self.children.clear()

            for type,lns in self.actions['change'].items():
                            if type!='ch':
                                [leafnodes[type](parent=self,sur=ln,subname=ln) for ln in lns ]
            WrapText(self.children)
            for chld in self.children:
                chld.pos_data = {'alignx':'center'}

            self.NodePositioning()
            # print('should add the level discp')
            self.actions['hover'][0]=1

        # if self.actions['hover']==1:
        #     for chld in self.children:
        #             child.a.remove()
        #             self.children.remove(child)
        #     self.actions['hover']=2

SYSTEMS['ui'].general_components={'button':button,'representer':representer}


def create(**kargs):
    new_ui=ui(_name=kargs['name'])
    for comp in new_ui.de.data['components']:
        c=SYSTEMS['ui'].general_components[comp['type']](_name=comp['name'],parent=new_ui)
        new_ui.components.append(c)

    all_nodes=NodeFlatten(new_ui.children)
    new_ui.all_nodes=all_nodes
    sizing_groups={k:[] for k in ['fixed','fit_w','grow',"per_w",'fit_h',"per_h"]}
    for node in [i for i in all_nodes if i.t!='leaf']:
            sizing_groups[node.size_data['w'][0]].append(node)
            sizing_groups[node.size_data['h'][0]].append(node)

    

    for nodes in list(sizing_groups.values())[:4]:
        for node in nodes:
            node.resize()

    WrapText(all_nodes)

    for nodes in list(sizing_groups.values())[2:]:
        for node in nodes:
            node.resize()

    new_ui.NodePositioning()


    return new_ui







