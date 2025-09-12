from vital import ABC,abstractmethod,scr,CDBTP,copy,neli,freq,randint
from art_assets import main_surfaces
from entites import *


# from factories import * AO

blkContainer=container()


class FundBlk:
    def __init__(self, image:pygame.Surface,order:list ,state:int,pos:list,size=[20,20]):

        self.ord=order
        self.size=size
        self.state=state
        self.rect=pygame.Rect(pos[0]+order[1]*size[0],pos[1]+order[0]*size[1],size[0],size[1])
        self.a=AnimF.ANIMS['AO'](
                        img=image,
                        type='P',
                        ap=1,
                        display=scr,
                        position=self.rect
                        )

    def get_data(self):
        return {'ord':self.ord,'state':self.state}


class RowFactory:
    @staticmethod
    def independent_row(randomize=1,**kargs):
        row=[0]*kargs['size']
        if randomize:
            start=randint(0,kargs['size']-1)
            end=randint(start+1,kargs['size'])
        else:
            start,end=0,kargs['size']
        i=0

        while i!=(end-start):
            row[start+i]=FundBlk(main_surfaces[str(kargs['state'])],[kargs['order'],start+i],kargs['state'],kargs['pos'])
            i+=1
        
        return row,(start,end)

    @staticmethod
    def dependent_row(**kargs):
        row=[0]*kargs['size']
        end=randint(kargs['last_pos'][0]+1,kargs['last_pos'][1])
        start=randint(0,end-1)
        e,s=copy(end),copy(start)

        if e-s < kargs['last_pos'][1]-kargs['last_pos'][0]:
            e,s=kargs['last_pos'][1]-1,kargs['last_pos'][0]

        i=s

        while i!=e:
            row[i]=FundBlk(main_surfaces[str(kargs['state'])],[kargs['order'],i],kargs['state'],kargs['pos'])
            i+=1
        return row,(s,e)

class BlkData:
    def __init__(self,**kargs):
        self.data={}
        self.parentblk:dict=kargs['parent_data']
        self.data['completed'] = []
        if kargs['rows'][0]:
                self.data['row_data']=[5,5]
                self.data['most_available']=self.parentblk['size']


        if kargs['color'][0]:
            self.data['colored_data']={
            'most':'',
            'comb':kargs['color'][1],
            'all_colors':{'4':10}
            }
        
        if kargs['empty']:
            self.data['empty_data']={'count':0,'surrondings':[],'color_surr':{}}


def DataUpdater()->dict:

    def update_row_data(gird:BlkData):
        """
        counts the number of consecutive non empty blocks
        """
        gird.data['row_data'].clear()

        ctr=0
        for i,blk in enumerate(gird.parentblk['blocks']):
            if blk.state!=-1 or i%10==0:
                if ctr>0 :
                    gird.data['row_data'].append(ctr)
                ctr=0

            if blk.state==-1:
                ctr+=1

        gird.data['most_available'] = freq( gird.data['row_data'] )

    def update_surronding_colored_data(gird:BlkData):
        """
        not complete
        """
        gird.data['empty_data']['surrondings'].clear()
        gird.data['empty_data']['color_surr']={str(k):0 for k in range(-2,12)}
        for i,blk in enumerate(gird.parentblk['blocks']):
            
            if blk.state == -1:
                surli=neli([1,gird.parentblk['size']-1,gird.parentblk['size'],gird.parentblk['size']+1])

                if (i+1)%gird.parentblk['size']==0:
                    surli=neli([gird.parentblk['size']-1,gird.parentblk['size']]) + [-1]
                if (i+1)%gird.parentblk['size']==1 :
                    surli=neli([gird.parentblk['size']+1,gird.parentblk['size']]) + [1]


                for j in surli:
                    if 0 < j+i < gird.parentblk['size']**2:
                        sur=gird.parentblk['blocks'][j+i]
                        gird.data['empty_data']['surrondings'].append(sur.state)


        for i in gird.data['empty_data']['surrondings']:
            gird.data['empty_data']['color_surr'][f'{i}']+=1

        print(gird.data['empty_data']['color_surr'])

    def update_empty_data(gird:BlkData):
        """
        counts number of empty_data
        """
        gird.data['empty_data']['count']=0              

        for blk in gird.parentblk['blocks']:
            if blk.state==-1:
                gird.data['empty_data']['count']+=1             

    def update_colored_data(grid:BlkData):
        """
        count the number of blocks for each color
        """
        grid.data['colored_data']['all_colors']={str(k):0 for k in range(-2,19)}
        for blk in grid.parentblk['blocks']:
            grid.data['colored_data']['all_colors'][str(blk.state)]+=1



    return {'row':update_row_data,'most_color':update_colored_data,'sur_colored':update_surronding_colored_data,'empty':update_empty_data}
    


class blocks(ABC):
    def __init__(self,**kargs):
        self.values:list[list]=[]
        self.poss=[]
        self.size=kargs['size']
        self.rect=pygame.Rect(kargs['dims'][0],kargs['dims'][1],kargs['dims'][2]*self.size[0],kargs['dims'][3]*self.size[1])
        self.org_pos=copy(self.rect.topleft)
        self.inter=kargs['inter']
        self.fundrects=[]

    def move(self,pos):
        self.rect.center=pos
        for fund in self.fundrects:

            fund.rect.topleft=(self.rect.x+fund.ord[0]*fund.size[0],self.rect.y+fund.ord[1]*fund.size[1])

    @abstractmethod
    def interaction(self):
        ...

class blk(blocks) :
    def __init__(self,state:int,dims:list,size=[3,3],invert=1):

        blocks.__init__(self,dims=dims,size=size,inter='put')
        self.state=state
        for i in range(randint(size[1]//2,size[1])):
            if i==0:
                row,pos=RowFactory.independent_row(size=size[0],order=len(self.values),state=state,pos=dims[0:2])
            else:
                row,pos=RowFactory.dependent_row(size=size[0],last_pos=self.poss[-1],order=len(self.values),state=state,pos=dims[0:2])
                
            self.poss.append(pos)       
            self.values.append(row)
            [self.fundrects.append(fund) for fund in row if fund!=0 ]

        if invert:
            for row in self.values:
                for blk in row: 
                    if blk!=0:
                        blk.ord[0]=((size[0]-1)-blk.ord[0])

        self.move(pos=dims[0:2]) #very important line 



    def GetMostCoverdRect(self,rects):
        lis={'cl':[],'mr':[],'rd':[]}
        for ent in rects:
            if ent!=0:
                if self.rect.colliderect(ent.rect):
                    lis['cl'].append(ent)

        for val in self.fundrects : 
                lis['mr'].append([val,[],[]])
                for re in lis['cl'] : 
                        if val.rect.colliderect(re.rect):
                            lis['mr'][-1][1].append(re)
                            lis['mr'][-1][2].append(CDBTP(val.rect.center,re.rect.center))

                if lis['mr'][-1][2]:
                    lis['rd'].append(lis['mr'][-1][1][lis['mr'][-1][2].index(min(lis['mr'][-1][2]))])

        return [lis['rd'],self.state,len(self.fundrects)]

    def interaction(self):
        ...

class grid(blocks):
    Updater=DataUpdater()
    def __init__(self,size:list=[10,10]):

        blocks.__init__(self,dims=[400-(size[0]*20)//2,50,20,20],size=size,inter='puttalbe')

        for i in range(0,size[1]):
            
            row,pos=RowFactory.independent_row(size=size[0],order=len(self.values),state=-1,randomize=0,pos=list(self.rect.topleft))
            
            self.poss.append(pos)       
            self.values.append(row)
            [self.fundrects.append(fund) for fund in row if fund!=0 ]

        self.blk_data=BlkData(
                                parent_data={'blocks':self.fundrects,'size':size[0]},
                                rows=[True],
                                empty=[True],
                                color=[True,[]]
                                )

    def update(self,funcs=[]):
        """
        to avoid over processing not all data of blk_data are updated , only the ones needed
        """
        [grid.Updater[i](self.blk_data) for i in funcs]

    def interaction(self):
        for blk in self.fundrects:
            blk.a.img=main_surfaces[str(blk.state)]

            if blk.state==0:
                blk.state=-1






