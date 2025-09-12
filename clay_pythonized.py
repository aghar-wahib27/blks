from vital import pygame,copy

def SIZING(): # for sizing
    def Grow(oe:any)->int:
        if oe.dir=="LTR":
            # overlap=max([i.size[w] for i in oe.nodeparent.children if ])
            sm=sum([int(child.size['w']) for child in oe.nodeparent.children if child!=oe]) + (oe.nodeparent.pos_data['gap']*len(oe.nodeparent.children))
            print('sum to grow in width',sm)
            return oe.nodeparent.size['w'] - sm

        if oe.dir=="UTD":
            return oe.nodeparent.size['h'] 

    def Shrink(oe:any):
        # if oe.dir=="LTR":
        #   # overlap=max([i.size[w] for i in oe.nodeparent.children if ])
        #   sm=sum([int(child.size['w']) for child in oe.nodeparent.children if child!=oe]) + (oe.nodeparent.pos_data['gap']*len(oe.nodeparent.children))
        #   print('sum to shrink in width',sm)
        #   return oe.nodeparent.size['w'] - sm

        # if oe.dir=="UTD":
        #   return oe.nodeparent.size['h'] 
        ...

    def FitWidth(oe:any)->int:
        _lis=[int(child.size['w']) for child in oe.children]
        # print(_lis)
        if _lis:
            if oe.dir=="LTR":
                return sum(_lis) + oe.pos_data['gap']*(max(len(oe.children)-1,0)) + sum(oe.pos_data['padding'][:2])

            if oe.dir=="UTD":
                return max(_lis) + sum(oe.pos_data['padding'][:2])
        
        return 0

    def FitHeight(oe:any)->int:
        _lis=[int(child.size['h']) for child in oe.children]
        # print(_lis)
        if _lis:
            if oe.dir=="LTR":
                return max(_lis) + sum(oe.pos_data['padding'][2:])

            if oe.dir=="UTD":
                return sum(_lis) + oe.pos_data['gap']*(len(oe.children)-1) + sum(oe.pos_data['padding'][2:])

        return 0

    def FixedWidth(oe:any)->int:
        return int(oe.size_data['w'][1])

    def FixedHeight(oe:any)->int:
        return int(oe.size_data['h'][1])

    def PercentageWidth(oe:any)->int:
            return  oe.nodeparent.size['w']*(int(oe.size_data['w'][1])/100) 

    def PercentageHeight(oe:any)->int:

            return oe.nodeparent.size['h']*(int(oe.size_data['h'][1])/100) 
        
    return {'fixed_w':FixedWidth,'fixed_h':FixedHeight,
            'fit_w':FitWidth,'fit_h':FitHeight,
            'grow':Grow,"per_w":PercentageWidth,
            "per_h":PercentageHeight,"shrink":Shrink}


def BLITER(): # for positioning
    def Stack(oe:any,offset=[0,0]):
        ...

    def Order(oe:any,offset=[0,0]):
        off=copy(offset)
        for chld in oe.children:
            # print("off is ",chld.nodename ,oe.nodename,off)
            chld.noderect.topleft=tuple(off)
            if oe.dir=='LTR':
                off[0]+=chld.noderect.width+oe.pos_data['gap']
            else:
                off[1]+=chld.noderect.height+oe.pos_data['gap']

    def Align(oee:any,offset=[0,0]):
        for oe in oee.children:
            if 'alignx' in oe.pos_data:
                if oe.pos_data['alignx']=='left':
                    oe.noderect.x= offset[0]

                if oe.pos_data['alignx']=='center':
                    oe.noderect.x= oee.noderect.width//2 - oe.noderect.width//2 + offset[0]

                if oe.pos_data['alignx']=='right':
                    oe.noderect.x= oee.noderect.width - oe.noderect.width - oee.pos_data['padding'][1] + offset[0]

                if 'per' in oe.pos_data['alignx'] :
                    pr=int(oe.pos_data['alignx'].split('+')[1])/100
                    oe.noderect.x= oee.noderect.width*pr - oe.noderect.width - oee.pos_data['padding'][1] + offset[0]

            if 'aligny' in oe.pos_data:
                if oe.pos_data['aligny']=='top':
                    oe.noderect.y = offset[1]

                if oe.pos_data['aligny']=='center':
                    oe.noderect.y = oee.noderect.height//2 - oe.noderect.height//2

                if oe.pos_data['aligny']=='bottom':
                    print(oe.noderect.height,oee.noderect.height)

                    oe.noderect.y=(700-oe.noderect.height-oee.pos_data['padding'][3])
                    print(oe.noderect.y)

                if 'per' in oe.pos_data['aligny'] :
                    pr=int(oe.pos_data['aligny'].split('+')[1])/100
                    oe.noderect.y= oee.noderect.height*pr - oe.noderect.height - oee.pos_data['padding'][0]



    return {'stack':Stack,'order':Order,'align':Align}


S=SIZING()
B=BLITER()

class Node:
    def __init__(self,children=[],name='',t='node',_dir="LTR",**kargs):
        self.nodeparent=kargs['parent']

        if self.nodeparent!=None :
            self.nodeparent.children.append(self) 
        
        self.children=children
        self.t=t
        self.nodename=name
        self.dir=_dir
        self.pos_data=kargs['pos_data']
        self.size_data={'w':kargs['width_size_type'].split("+"),'h':kargs['height_size_type'].split("+")}
        self.size={'w':S[self.size_data['w'][0]](self),'h':S[self.size_data['h'][0]](self)}
        self.noderect=pygame.Rect(0,0,self.size['w'],self.size['h'])


    def resize(self,update=1):
        _dir='w' if self.dir=='LTR' else 'h'

        if update:
            self.size={'w':S[self.size_data['w'][0]](self),'h':S[self.size_data['h'][0]](self)}

        self.noderect.width=self.size['w']
        self.noderect.height=self.size['h']
        # print(self.size)

    def NodePositioning(self):
        off=[self.noderect.topleft[0]+self.pos_data['padding'][0],self.noderect.topleft[1]+self.pos_data['padding'][2]]
        for mode in self.pos_data['mode']:
            B[mode](self,offset=off )

        for n in self.children:
            n.NodePositioning()




    def get_data(self):
        return {'nodename':self.nodename}




class RootNode:
    def __init__(self,children:list,sizing:list=[0,0],pos_data={}):
        Node.__init__(
                    self,
                    t='root',
                    children=children,
                    parent=None,
                    name='root',
                    width_size_type=f'fixed_w+{sizing[0]}',
                    height_size_type=f'fixed_h+{sizing[1]}',
                    pos_data=pos_data
                    )
        

class LeafNode:
    def __init__(self,parent,_name,pos_data):
        Node.__init__(
                self,
                t='leaf',
                _dir='',
                parent=parent,
                children=None,
                width_size_type='fixed_w+0',
                height_size_type='fixed_h+0',
                name=_name,
                pos_data=pos_data
                )

        





"""

"""



