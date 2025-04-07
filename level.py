

from vital import choice,randint,GAME_STATE
from art_assets import *
from blocks import blk,grid,DE,concius,AO,scr,blk_constructor,Handler,EE,ANIM_SYS


class level(DE,concius,EE):
    def __init__(self,name:str):
        DE.__init__(
            self,
            _name=name,
            ap=0
        )
        concius.__init__(
            self,
            ap=0,
            actions={'put':0,'rtrn':0,'ms_down':0,'key_down':0},
            counters=['timer']
        )
        EE.__init__(
            self,
            events=['space','mouse_down','mouse_released','mouse_pos',"esc"]
            )
        self.bg=AO(
                img=UIS[self.data['back_ground']],
                display=scr,
                pos=(0,0),
                resize=(800,700)
                )
        self.groups={'move':[],"current_set":[],'grids':[grid(data=dt) for dt in self.data['grids'] ]}
        # Handler.append(groups=['key_down','mouse_down','mouse_released'],ent=self)

    def moveing(self):
        for blk in self.groups['current_set']:
            # print(Handler.events['mouse_pos'])
            if blk.rect.collidepoint(self.events['mouse_pos']) and self.events['mouse_down']:
                self.groups['move'].append(blk)
        self.events['mouse_down']=0

        if self.events['mouse_released']:
            self.groups['move'].clear()
            self.events['mouse_released']=0


        for blk in self.groups['move']:
            blk.move(self.events['mouse_pos'])

    def construct(self,**kargs):
            dim=20
            min_available=min(kargs['data'].data['row_data'])
            st=''
            if min_available<kargs['grid_size']//2:
                st='most_frequent'
            else:
                st='limited'
            sz=blk_constructor.determine_size(size=kargs['grid_size'],empty=kargs['data'].data['row_data'],state=st)
            print(sz,st)
            for i in range(kargs['blk_no']):
                self.groups['current_set'].append(blk(randint(1,11),[100+((dim+5)*sz[0]*i),600,dim,dim],size=sz,invert=randint(-10,10)>0)) 

    def behavior(self):
        for gr in self.groups['grids']:
            
            for ent in self.groups['move']:
                possible,st,blk_len=ent.GetMostCoverdRect(gr.fundrects)
                
                ## put_condtion
                put=[]
                for re in possible :
                    re.state=0 if re.state==-1 else re.state
                    if re.state in [st,0]: 
                        put.append(1)
                    else:
                        put.append(0)
                
                if self.events['mouse_released'] and (0 not in put)  : 
                    up_data=['row','colored','empty']

                    print('pur',possible)
                    for re in possible:
                        re.state=st
                    self.groups['current_set'].remove(ent)
                    for fund in ent.fundrects:
                        ANIM_SYS.lists['ents'].remove(fund)
                    blk_constructor.Manage(gr.blk_data,up_data)
                    print(gr.blk_data.data['row_data'])


            gr.interaction()

        self.moveing()



        if self.events['space'] :
                # if  len(self.groups['current_set']) < 2:
                gr=self.groups['grids'][0]
                self.construct(
                        grid_size=gr.data['grid_size'][0],
                        blk_no=4,
                        data=gr.blk_data
                        )
                self.events['space']=0

        if self.events['esc']:
            self.events['esc']=0
            # print('to puase menu')
            GAME_STATE['UI']='ui_4'
            GAME_STATE['change'][0]=1





