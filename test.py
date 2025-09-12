"""
from vital import pygame,scr
from art_assets import _FONTS_

def WOW(word:str,font_size:int):
    return (len(word)+1)*font_size


def EDUS(text:str,allowed_width:int,Font:any)->list :
   ess:dict={'acc_width':0,'words_to_ignore':['9','#'],"status":'',"list_of_sec":[],"a_list_of_sec":[],
                        'list_of_sur':[],"new_sen":[],'list_of_words':text.split(),'fs':0,'gs':0,'gaps':0}

    ess['fs']=Font.render(ess['list_of_words'][0],1,(0,0,0)).get_width()//len(ess['list_of_words'][0])


    for single in ess['list_of_words']:


        if sum([WOW(wr,ess['fs']) for wr in ess['new_sen']+[single] ]) > allowed_width :
            ess['status']='break'
 
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

                # if single not in ess['words_to_ignore'] :
                ess['new_sen'].append(single)






    if len(ess['new_sen']):
            ess['list_of_sec'].append(ess['new_sen'])



    for lis in ess['list_of_sec']:
            ess['list_of_sur'].append(Font.render(" ".join(lis),True,(255,255,255)))

    return [ess['list_of_sur'] , len(ess['list_of_sec']),ess['fs'] ,ess['list_of_sec'] ]


cnt=pygame.Surface((300,600))
cnt.fill((100,40,160))

dvt=EDUS('this is the funniest joke i have heard in my life !!! ha ha haa  ',cnt.get_width(),_FONTS_['50'])

print('senteces are',dvt[-1])

for i in range(len(dvt[0])):
    cnt.blit(dvt[0][i],(0,i*dvt[-2]*2))

print([ (k,f.render('s',1,(0,0,0)).get_width()) for k,f in _FONTS_.items() ])

run=1

while run:
    scr.fill((0,0,0))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:        
            run=0


    scr.blit(cnt,(250,50))
    pygame.display.update()
    
pygame.quit()
"""

# def flatten(lis:list):
# 	"""
# 	combine nested lists into one big list
# 	"""
# 	lu=[]
# 	h=copy(lis)
# 	for i in h:
# 		if type(i)!= list:
# 			lu.append(i)
# 		else:
# 			lu.extend(flatten(i))
			
# 	return lu

# import copy

# def ROUA(obj_li:list,req_data:list):
# 	"""
# 	ROUA : return_obj_upon_attr
# 	"""
# 	for obj in obj_li : 
# 		data=obj.get_data()
# 		# print(data,'this is roua')
# 		if data[req_data[0]]==req_data[1]:
# 			return obj
# 		# else:
# 		# 	print (data[req_data[0]],req_data[1])

# 	return 'not_found'

# def TurnListIntoDict(__lis:list,change=0):
    # if change:
    #     co = __lis
    # else:
    #     co = copy.deepcopy(__lis)
    # return { str(k):co[k] for k in range(len(co)) }

# def GetAttrFromNestedObj(obj:dict,attr:str,change=[0,0,0]):
    # """
    # write discription here 
    # this function has two jobs searching a nested dictionary and changeing a value in it which is a bas design
    # """
    # search = 1 
    # if change[0]:
    #     co = obj
    # else:
    #     co = copy.deepcopy(obj)

    # next_level_objs = [co]
    # value = 0
    # while search: 
    #     co = next_level_objs[0]
    #     next_level_objs.pop(0)
    #     for k in co.keys():

    #         if k == attr:
    #             if change[0]:
    #                 if change[1]!=None:
    #                     co[k]=change[1]
    #             value = co[k]
    #             search = 0

    #         if type(co[k])==dict:
    #             next_level_objs.append(co[k])
    # if type(value) == list :
    #     value = TurnListIntoDict(value,change=1)
    # return value 

# def GetAttrFromNestedObjWithRepeatedNames(obj:dict,attrs:str,change=[0,0]):
    # attr_order = attrs.split('+')
    # val = obj
    # for i in range(len(attr_order)):
    #     ch =[0,0]
    #     if i == len(attr_order)-1:
    #         ch=change
    #     val = GetAttrFromNestedObj(val,attr_order[i],change=ch)

    # return val

# def DirectedAttrSearch(obj,attrs:str,change=[0,0,1]):
    # attrsList = [attrs] if '+' not in attrs else attrs.split('+')
    # print(attrsList)
    # if change[2]:
    #     objCopy = obj
    # else:
    #     objCopy = copy.deepcopy(obj)
    # for attr in attrsList:
    #     ch = [1,None,1] if attrsList.index(attr)!=len(attrsList)-1 else change
    #     print(ch)
    #     objCopy = GetAttrFromNestedObj(objCopy,attr,change=ch)
    #     print(objCopy)
    # return objCopy

# dic = {
    #     "month":"feb",
    #     "day":{
    #         "name":'monday',
    #         "number":'12',
    #         'details':{
    #             "moist":'average',
    #             "temp":27,
    #             'working':{
    #                 "hours":'8-10pm',
    #                 "days":'sunday-thursday'
    #             }
    #             }
    #         },
    #     "year":1954
    #     }

# dic2 = {
    #     'holiday1':{
    #         'name':'easter',
    #         'date':'12-3',
    #         'duration':4,
    #         'exceptions':[]
    #         },
    #     'holiday2':{
    #         'name':'christmas',
    #         'date':'30-12',
    #         'duration':7,
    #         'exceptions':[]
    #         },
    #     'holiday3':{
    #         'name':'independence',
    #         'date':'23-8',
    #         'duration':1,
    #         'exceptions':[]
    #         },
    #     'holiday4':{
    #         'name':'nationalday',
    #         'date':'14-4',
    #         'duration':3,
    #         'exceptions':[]
    #         }
    #     }


# ui_data={

	# "name":"main_menu",
	# "gap":32,
	# "padding":[30,30,30,30],

	# "mode":["align"],


		# "back_ground":{
				# "bg_ui_21":{
					# "anims":[]
				# }
			# },

	# "components":[

		# {
			# "type":"button",
			# "name":"Kahira",
			# "img":"level_1_logo",
			# "parent_name":"cont_1",
			# "children":{
				# "img":["level_1_logo"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order"],
				# "alignx":"per+90",
				# "aligny":""

			# },
			# "func":[
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":"kahira"
				# },
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":0
				# },
				# {
				# "respond":"hover",
				# "func":["hover_menu","show",1]
				# }

			# ]

		# },

		# {
			# "type":"button",
			# "name":"Menofia",
			# "children":{
				# "img":["level_2_logo"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order"],
				# "alignx":"per+70",
				# "aligny":""

			# },
			# "parent_name":"cont_1",
			# "func":[
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":"menofia"
				# },
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":0
				# },
				# {
				# "respond":"hover",
				# "func":["hover_menu","show",1]
				# }

			# ]

		# },
		# {
			# "type":"button",
			# "name":"Domyat",
			# "children":{
				# "img":["level_3_logo"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order"],
				# "alignx":"per+40",
				# "aligny":""

			# },
			# "parent_name":"cont_1",
			# "func":[
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":"domyat"
				# },
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":0
				# },
				# {
				# "respond":"hover",
				# "func":["hover_menu","show",1]
				# }

			# ]

		# },
		# {
			# "type":"button",
			# "name":"Sharkia",
			# "parent_name":"cont_1",
			# "children":{
				# "img":["level_4_logo"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order"],
				# "alignx":"per+20",
				# "aligny":""

			# },
			# "func":[
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":"sharkia"
				# },
				# {
				# "respond":"click",
				# "system":0,
				# "modify":"game_state",
				# "state":0
				# },
				# {
				# "respond":"hover",
				# "func":["hover_menu","show",1]
				# }

			# ]
		# },
		# {
			# "type":"button",
			# "name":"Helwan",
			# "parent_name":"cont_1",
			# "children":{
				# "img":["level_5_logo"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order"],
				# "alignx":"per+45",
				# "aligny":""

			# },
			# "func":[
				# {
				# "respond":"click",
				# "system":"level",
				# "modify":"game_state",
				# "state":"helwan"
				# },
				# {
				# "respond":"click",
				# "system":"UI",
				# "modify":"game_state",
				# "state":0
				# },
				# {
				# "respond":"hover",
				# "func":["hover_menu","show",1]
				# }

			# ]

		
		# },
		# {
			# "type":"button",
			# "name":"back",
			# "parent_name":"root",
			# "children":{
				# "img":["bomareng_pointer"],
				# "text":["back"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order","align"],
				# "alignx":"left",
				# "aligny":"bottom"


			# },
			# "func":[
				# {
				# "respond":"click",
				# "system":"UI",
				# "modify":"game_state",
				# "state":"ui_1"
				# }

			# ]

		# },
		# {
			# "type":"representer",
			# "name":"book",
			# "parent_name":"root",
			# "children":{
				# "img":["book"]

			# },
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[0,0,0,0],
				# "gap":30,
				# "mode":["order"],
				# "alignx":"right",
				# "aligny":"bottom"


			# }

			
		# }
	# ],

	# "containers":[
		# {
			# "name":"cont_1",
			# "parent_name":"root",
			# "sizing":["per_w+60","fit_h"],
			# "spacing":{
				# "margin":[0,0,0,0],
				# "padding":[10,10,10,10],
				# "gap":40,
				# "mode":["order","align"],
				# "alignx":"center",
				# "aligny":"center"


			# },
			# "dir":"UTD"
		# }

	# ]


# }

# class entity:
    # def __init__(self,name,data):
    #     self.name = name
    #     self.data = data

    # def get_data(self):
    #     return {'name':self.name}

# val = DirectedAttrSearch(ui_data,'components+0+func+0+system',change=[1,'LEVELS',1])
# print(val)
# print(ui_data['components'][0])
# val = GetAttrFromNestedObj(obj=dic,attr="days",change=[1,'firday-wednesday'])
# val2 = GetAttrFromNestedObj(obj=ui_data,attr='components')
# comps = [ entity(data['name'],data) for data in val2 ]
# req_comp = ROUA(comps,['name','Sharkia'])
# print(req_comp.data['func'])

# import random

# choices = ['red', 'blue','green','trequise','purple','pink']
# w = [0.3 , 0.1 , 0.1 , 0.2 , 0.1 , 0.1]

# c= []
# for _ in range(10):
#     c .extend(random.choices(choices,w))


# print(c) 


tu1 = (1,-2)
tu2  = (-2,1)

print(tu2[::-1],tu2[::-1]==tu1,tuple("-1+3".split('+')))



