from entites import AO,AE,concius,abstractmethod,AllData,container,EE
from vital import pygame,CDBTP,singleton,ROUA,SYSTEMS,scr,GAME_STATE
from art_assets import UIS,FFF


class ui(concius,AO,EE):
	def __init__(self,_name:str):
		self.data=AllData[_name]
		self.name=_name
		self.positions=[]
		self.components=[]
		concius.__init__(
			self,
			actions={'running':0},
			counters={'transion':20}
			)
		AO.__init__(
			self,
			img=UIS[_name],
			pos=(0,0),
			display=scr,
			resize=[800,700]

			)
		EE.__init__(
			self,
			events=['mouse_down','mouse_released','mouse_pos']
			)
		
	def positioning(self):

		if 'pattern' in self.data['positions']['components']:
			start=self.data['positions']['components']['pattern']['start']
			step=self.data['positions']['components']['pattern']['step']
			self.positions.append(tuple(start))
			for i in range(len(self.data['components'])):
				new_pos=(start[0]+step[0],start[1]+step[1]*(i+1))
				self.positions.append(new_pos)

		else:
			self.positions=self.data['positions']['components']

		for comp in self.components:
			comp.rect.topleft=self.positions[comp.data['pos']-1]
			comp.pos=comp.rect.topleft
		print(self.components)
		print([re.rect.x for re in self.components])

	def behavior(self):
		for comp in self.components:
			comp.behavior()
			pygame.draw.rect(scr,(200,100,50),comp.rect)
		self.events['mouse_down']=0

@singleton
class UIs(container):
	def __init__(self):
		container.__init__(self)
		# self.events={'mouse_clicked':0,'mouse_pos':(0,0)}
		self.general_components={}


		
		

SYSTEMS['ui']=UIs()

class TextWrapper:
	...



class ui_component(AO,concius):
	def __init__(self,ui,_name,**kargs):
		self.parent=ui
		for comp in self.parent.data['components']:
			if comp['name']==_name:
				self.data=comp
		self.rect=pygame.Rect(50,50,self.data['diminsions'][0],self.data['diminsions'][1])

		concius.__init__(
				self,
				actions=kargs['actions'],
				counters=kargs['counters']
				)
		AO.__init__(
				self,
				img=kargs['img'],
				display=scr,
				pos=self.rect.topleft
				)

	def get_data(self):
		return {'name':self.data['name']}

	@abstractmethod
	def behavior(self):
		...


def Functionailty():
	def GameData(dta):
		if dta['system']=="UI":
			GAME_STATE['change'][0]=1
		if dta['system']=="level":
				GAME_STATE['change'][1]=1
		GAME_STATE[dta['system']]=dta['state']

	def EntData():
		...

	return {'game_state':GameData,"entity":EntData}

funcs=Functionailty()

def ButtonActions():
	
	def hover(btn,**kargs):
		if CDBTP(btn.rect.center,list(kargs['mouse_pos']),btn.rect.width//2):
			if not btn.actions['hover'][0] and btn.rect.collidepoint(kargs['mouse_pos']):
				btn.actions['hover'][0]=1
				mod=ROUA(btn.parent.components,['name',kargs['btn_data']['func'][0]])
				print(mod,btn.img.get_width(),btn.img.get_height())
				if type(mod) != str :
					btn.actions['hover'][1]=mod.actions[kargs['btn_data'][1]]
					mod.actions[kargs['btn_data'][1]]=kargs['btn_data'][-1]
				
			if btn.actions['hover'][0] and not btn.rect.collidepoint(kargs['mouse_pos']) : ### upon unhovering
				btn.actions['hover'][0]=0
				mod=ROUA(btn.parent.components,['name',kargs['btn_data']['func'][0]])
				if type(mod) != str :
					mod.actions[kargs['btn_data'][1]]=btn.actions['hover'][1]


			
	def click(btn,**kargs):
		if btn.rect.collidepoint(kargs['mouse_pos']):
			if kargs['mouse_clicked'] :
				print('clicked',btn.data['name'],kargs['mouse_pos'],btn.rect.center)
				funcs[kargs['btn_data']['modify']](dta=kargs['btn_data'])


	return {'hover':hover,'click':click}

BtnInters=ButtonActions()

class button(ui_component):
	def __init__(self,_name,parent):
		self.text=FFF.render(_name,True,(150,150,150))
		ui_component.__init__(
					self,
					ui=parent,
					_name=_name,
					actions={'hover':[0,0],'clicked':0,'color':(255,255,255)},
					counters=[],
					img=self.text
					)

	def behavior(self):
		for func in self.data['func']:
			BtnInters[func['respond']](
										btn=self,
										mouse_pos=self.parent.events['mouse_pos'],
										mouse_clicked=self.parent.events['mouse_down'],
										btn_data=func
										)



class representer(ui_component):
	def __init__(self):
		...



SYSTEMS['ui'].general_components={'button':button,'representer':representer}


def create(**kargs):
	new_ui=ui(_name=kargs['name'])
	for comp in new_ui.data['components']:
		c=SYSTEMS['ui'].general_components[comp['type']](_name=comp['name'],parent=new_ui)
		new_ui.components.append(c)
	new_ui.positioning()
	return new_ui
		# self.entities.append()