from vital import choice,randint,GAME_STATE,CDFL
from art_assets import *
from blocks import blk,grid,DE,concius,scr,Handler,EE,ANIM_SYS,AnimF,BackGround,DT_SYS
from level_character import *

class level(concius,EE):
    def __init__(self,name:str):
        self.de = DT_SYS.MapDataEntity(name)
        concius.__init__(
            self,
            ap=0,
            actions={'put':0,'rtrn':0,'ms_down':0,'key_down':0},
            counters=['timer','win']
        )

        EE.__init__(
            self,
            events=['space','mouse_down','mouse_released','mouse_pos',"esc"]
            )

        self.bgs=BackGround(
            bg_names=[bg for bg in self.de.data['back_ground']],
            bg_imgs=
                [
                    AnimF.ANIMS['BG'](
                        img=UIS[i],
                        blur=0
                        )
                 for i in [bg for bg in self.de.data['back_ground']]
                 ],
            bg_ainmations=[]
            )

        self.char={
              'put':PUT_COND()[self.de.data['put'][0]] ,
              # 'progress':{ k[0]:[PROGRESS()[k[0]],k[1:]] for k in self.de.data['progress']},
              # 'color_det':{ k:COLOR()[k] for k in self.de.data['color']},
              'progress':[PROGRESS()[i[0]] for i in  self.de.data['progress'] ],
              'color_det':COLOR()[self.de.data['color'][0]] ,
              'size_det':{ k:SIZE()[k] for k in self.de.data['size']},
              'color_set':[choice(range(1,11)) for i in range(randint(1,8))]
              }

        self.groups={
                    'move':[],"current_set":[],
                    'grids':[grid(size=dt) for dt in self.de.data['grid_size'] ],
                    }

        self.stage= CDFL(
            [
            {f'grid_{i}_stage':'first' for i in range(len(self.groups['grids']))} , 
            {f'grid_{i}_progress': 0 for i in range(len(self.groups['grids']))} ,
            {f'grid_{i}_win': 0 for i in range(len(self.groups['grids']))} ,
            {f'grid_{i}_loss': 0 for i in range(len(self.groups['grids']))} ,
            {"level_state":''}

            ]
            )


    def progress_tracker(self,grid_order):
        self.stage[f'grid_{grid_order}_progress'] += self.char['progress'][grid_order](
                self.groups['grids'][grid_order],
                self.de.data['progress'][grid_order][1:]
                )

        if self.stage[f'grid_{grid_order}_progress'] == self.de.data['progress'][grid_order][-1] :
            self.stage[f'grid_{grid_order}_win'] = 1

        won = sum([self.stage[f'grid_{i}_win'] for i in range(len(self.groups['grids'])) ])
        # print('cond to win is ',won)
        if won == len(self.groups['grids']) : 
            self.stage['level_state'] = 'win'
        print(self.stage)

    def WinOrLose(self):
        if self.count['win'][0] == 18: 

            for fund in self.groups['current_set'][0].fundrects:
                ANIM_SYS.lists['ents'].remove(fund.a)
            self.groups['current_set'].pop(0)

        if not self.groups['current_set'] and self.stage['level_state'] == 'win':
            ANIM_SYS.StartFade(changes=[1,1],new_ui='ui_100',new_level='')
            # print(self.de.data['upon_win']['Entities'],self.de.data['upon_win']['Changes'])
            DT_SYS.ChangeEntities(
                    Entities=self.de.data['upon_win']['Entities'],
                    Changes=self.de.data['upon_win']['Changes']
                    )
            self.stage['level_state'] = 'after_win'


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
            sz=self.char['size_det']['freq'](size=kargs['grid_size'],empty=kargs['data'].data['row_data'])
            for i in range(kargs['blk_no']):
                self.groups['current_set'].append(
                        blk(
                            self.char['color_det'](
                                        color_data=kargs['data'].data['colored_data']['all_colors'],
                                        range=[1,11],
                                        color_set=self.char['color_set']
                                        ),
                            [150*(i+1),600,dim,dim],
                            size=sz,
                            invert=randint(-10,10)>0
                            )
                        ) 

    def clear(self):
        for gr in self.groups:
            for blk in self.groups[gr]:
                for fund in blk.fundrects:
                    fund.a.remove()

        for bg in self.bgs.bgs_list:
            bg.remove()

    def play(self):
        for order,gr in enumerate(self.groups['grids']):
           
            for ent in self.groups['move']:
                possible,st,blk_len=ent.GetMostCoverdRect(gr.fundrects)
                
                ## put_condtion
                put,std=self.char['put'](possible,st,self.de.data['put'][1:])
                
                if self.events['mouse_released'] and (0 not in put) and gr.rect.colliderect(ent.rect)  : 
                    up_data=['row','most_color','empty']
                    # print(gr.blk_data)
                    if self.de.data['put'][0]=='comb':
                        for re in possible:
                            re.state=std[f'{st}+{re.state}']
                    else:
                        for re in possible:
                            re.state=std[f'{re.state}']
                    self.groups['current_set'].remove(ent)
                    for fund in ent.fundrects:
                        ANIM_SYS.lists['ents'].remove(fund.a)
                    gr.update(up_data)
                    # print(gr.blk_data.data)
                    self.progress_tracker(order)
                else :
                    ent.move(ent.org_pos)



            gr.interaction()

        # if self.stage['level_state']=='' :
        self.moveing()



        if self.events['space']  :
                gr=self.groups['grids'][0]
                self.construct(
                        grid_size=gr.size[0],
                        blk_no=4,
                        data=gr.blk_data
                        )
                self.events['space']=0

        if self.events['esc']:
            self.events['esc']=0
            GAME_STATE['UI']='ui_4'
            GAME_STATE['change'][0]=1

    def behavior(self):
        if self.stage['level_state'] == '' :
            self.play()
        else :
            self.WinOrLose()
        self.counts(win=[ self.stage['level_state']=='win' ,'un+20', not self.groups['current_set']])














