from vital import ABC,abstractmethod,scr,CDBTP,copy,neli,freq
from art_assets import main_surfaces
from entites import *
from level_character import *

# from factories import *

blkContainer=container()


class FundBlk(AO):
	def __init__(self, image:pygame.Surface,order:list ,state:int,pos:list,size=[20,20]):

		# self.img=image
		self.ord=order
		self.size=size
		self.state=state
		self.rect=pygame.Rect(pos[0]+order[1]*size[0],pos[1]+order[0]*size[1],size[0],size[1])
		AO.__init__(
				self,
				img=image,
				display=scr,
				pos=self.rect
				)

		# self.num=FFF.render(f'{order[0]},{order[1]}',True,(0,0,0))

	def get_data(self):
		return {'ord':self.ord,'state':self.state}

	def render(self):
		scr.blit(self.img,self.rect)
		# scr.blit(self.num,self.rect)

class RowFactory:
	"""
		
	@staticmethod
	def independent_row(size:int,order:int,state:int,randomize=1):
		row=[0]*size
		if randomize:
			start=randint(0,size-1)
			end=randint(start+1,size)
		else:
			start,end=0,size
		i=0

		while i!=(end-start):
			row[start+i]=FundBlk(main_surfaces[str(state)],[order,start+i],state)
			i+=1
		
		return row,(start,end)



	@staticmethod
	def dependent_row(size:int,last_pos:tuple,order,state:int):
		row=[0]*size
		end=randint(last_pos[0]+1,last_pos[1])
		start=randint(0,end-1)
		e,s=copy(end),copy(start)

		if e-s < last_pos[1]-last_pos[0]:
			e,s=last_pos[1]-1,last_pos[0]

		i=s

		while i!=e:
			row[i]=FundBlk(main_surfaces[str(state)],[order,i],state)
			i+=1
		return row,(s,e)
	"""

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
		if kargs['rows'][0]:
				self.data['row_data']=[5,5]


		if kargs['color'][0]:
			self.data['colored_data']={
			'most':'',
			'comb':kargs['color'][1],
			'needed':[]
			}
		
		if kargs['empty']:
			self.data['empty_data']={'count':0,'surrondings':[],'color_surr':{}}

class DataFactory:
	@staticmethod
	def update_row_data(gird:BlkData):
		
		gird.data['row_data'].clear()

		ctr=0
		for i,blk in enumerate(gird.parentblk['blocks']):
			if blk.state!=-1 or i%10==0:
				if ctr>0 :
					gird.data['row_data'].append(ctr)
				ctr=0

			if blk.state==-1:
				ctr+=1

	@staticmethod
	def update_colored_data(gird:BlkData):
		gird.data['empty_data']['surrondings'].clear()
		gird.data['empty_data']['color_surr']={str(k):0 for k in range(-2,12)}
		for i,blk in enumerate(gird.parentblk['blocks']):
			
			if blk.state == -1:
				# gird.data['row_data'][f'row_{blk.ord[1]}'].append(blk)
				surli=neli([1,gird.parentblk['size']-1,gird.parentblk['size'],gird.parentblk['size']+1])

				if (i+1)%gird.parentblk['size']==0:
					surli=neli([gird.parentblk['size']-1,gird.parentblk['size']]) + [-1]
				if (i+1)%gird.parentblk['size']==1 :
					surli=neli([gird.parentblk['size']+1,gird.parentblk['size']]) + [1]


				for j in surli:
					if 0 < j+i < gird.parentblk['size']**2:
						sur=gird.parentblk['blocks'][j+i]
						# if sur.ord[0]<self.parentblk['size'] and 0<sur.ord[1] < self.parentblk['size']-1:
						# self.data['empty_data']['surrondings'].append((sur.state,sur.ord,i)) 
						gird.data['empty_data']['surrondings'].append(sur.state)


		print(gird.data['empty_data']['color_surr'])
		for i in gird.data['empty_data']['surrondings']:
			gird.data['empty_data']['color_surr'][f'{i}']+=1

	@staticmethod
	def update_empty_data(gird:BlkData):
		gird.data['empty_data']['count']=0				

		for blk in gird.parentblk['blocks']:
			if blk.state==-1:
				gird.data['empty_data']['count']+=1				

	funcs={'row':update_row_data,'colored':update_colored_data,'empty':update_empty_data}
	
	@staticmethod
	def Manage(gird:BlkData,funcs:list=['row']):
		for func in funcs:
			DataFactory.funcs[func](gird)

	@staticmethod
	def determine_size(**kargs)->list:
		blk_sz=kargs['size']
		min_available=min(kargs['empty'])
		sz=[0,0]
		if kargs['state']=='open':
			sz=[max(randint(blk_sz//4,blk_sz),4)]*2

		if kargs['state']=='limited':
			sz=[max( randint(min_available//2,min_available) , 4 )]*2

		if kargs['state']=='most_frequent':
			sz=[ min(freq(kargs['empty']),int(blk_sz*0.75)) ]*2

		return sz

	# @staticmethod
	# def determine_color(**kargs)->list:
	# 	blk_sz=kargs['size']
	# 	min_available=kargs['empty']
	# 	sz=[0,0]
	# 	if kargs['state']=='open':
	# 		sz=[max(randint(blk_sz//4,blk_sz),4)]*2

	# 	if kargs['state']=='limited':
	# 		sz=[max( randint(min_available//2,min_available) , 4 )]*2

	# 	return sz

blk_constructor=DataFactory()

class blocks(ABC):
	def __init__(self,**kargs):
		self.values:list[list]=[]
		self.poss=[]
		self.rect=pygame.Rect(kargs['dims'][0],kargs['dims'][1],kargs['dims'][2]*kargs['size'][0],kargs['dims'][3]*kargs['size'][1])
		self.inter=kargs['inter']
		self.fundrects=[]
		# if self.inter not in blkContainer.inter.keys():
		# 	blkContainer.inter[self.inter]=[]	
		
		# blkContainer.inter[self.inter].append(self)
		# blkContainer.entities.append(self)


	# def render(self,dem:int):
	# 	# pygame.draw.rect(scr,(dem%255,dem%150,40),self.rect)
	# 	for row in self.values:
	# 		for blk in row:
	# 			if blk!=0:
	# 				pygame.draw.rect(scr,(abs(blk.state)*15,abs(blk.state)*20,140//abs(blk.state+2)),blk.rect)
	# 				blk.render()

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
	def __init__(self,data:dict):
		# DE.__init__(self,kargs['name'],ap=0)
		self.data=data
		blocks.__init__(self,dims=[400-(self.data['grid_size'][0]*20)//2,50,20,20],size=self.data['grid_size'],inter='puttalbe')
		self.char={
			'put':PUT_COND()[self.data['put']] ,
			'progress':{ k[0]:[PROGRESS()[k[0]],k[1:]] for k in self.data['progress']},
			'color_det':{ k:COLOR()[k] for k in self.data['color']},
			'size_det':{ k:SIZE()[k] for k in self.data['size']}
			}

		for i in range(0,self.data['grid_size'][1]):
			
			row,pos=RowFactory.independent_row(size=self.data['grid_size'][0],order=len(self.values),state=-1,randomize=0,pos=list(self.rect.topleft))
			
			self.poss.append(pos)		
			self.values.append(row)
			[self.fundrects.append(fund) for fund in row if fund!=0 ]

		self.blk_data=BlkData(
								parent_data={'blocks':self.fundrects,'size':self.data['grid_size'][0]},
								rows=[True],
								empty=[True],
								color=[True,[]]
								)


	def interaction(self):
		for blk in self.fundrects:
			blk.img=main_surfaces[str(blk.state)]

			if blk.state==0:
				blk.state=-1

















