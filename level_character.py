from vital import randint,freq

def SIZE():
	def upon_most_frequent_empty(**kargs)->list:
		blk_sz=kargs['size']
		min_available=min(kargs['empty'])
		sz=[ min(freq(kargs['empty']),int(blk_sz*0.75)) ]*2
		return sz

	def upon_random(**kargs):
		blk_sz=kargs['size']
		sz=[
			randint(3,
				int(blk_sz*randint(blk_sz//2,blk_sz)/10)
					)]*2
		return sz

	return {'freq':upon_most_frequent_empty,'rand':upon_random}

def COLOR():
	def upon_most_frequent_color(**kargs)->list:
		blk_sz=kargs['size']
		min_available=min(kargs['empty'])
		sz=[ min(freq(kargs['empty']),int(blk_sz*0.75)) ]*2
		return sz

	def upon_random(**kargs):
		blk_sz=kargs['size']
		sz=[
			randint(3,
				int(blk_sz*randint(blk_sz//2,blk_sz)/10)
					)]*2
		return sz

	def restricted_random(**kargs):
		...

	return {'freq':upon_most_frequent_color,'rand':upon_random}


def PROGRESS():
	def complete(blks,sz,color=-1,checked=0):
		if checked:
			ch='row'
		else:
			ch='col'
		rows={f'{ch}_{k}':0 for k in range(sz)}
		for blk in blks:
			if  blk.state!=color:
				rows[f'{ch}_{blk.ord[checked]}']+=1

		return rows
		
	def reduced_to(blks:list,color=-1):
		return blks.count(color)
		
	return {'com':complete,'red':reduced_to}


def PUT_COND():
	def put_on_same_color(poss_list:list,st:int,blk_len:int):
		put=[]
		std={f'{st}':st,'-1':st}
		for re in poss_list :
			re.state=0 if re.state==-1 else re.state
			if re.state in [st,0]: 
				put.append(1)
			else:
				put.append(0)

		return put,std
		
	def combinations(poss_list:list,st:int,blk_len:int,combs:dict,allow_same:0):
		std={}
		std[f'-1+{st}']=st
		if allow_same:
			std[f'{st}+{st}']=st
		put=[]

		for re in poss_list:
			ke=f'{st}+{re.state}'
			legit=0
			if ke in combs.keys() :
				std[re.state]=combs[ke]
				legit=1
			if ke[::-1] in combs.keys():
				std[re.state]=combs[ke[::-1]]
				legit=1
			if ke[::-1] == f'-1+{st}':
				legit=1
			if ke==ke[::-1]:
				legit=1

			put.append(legit)


		return put,std

	def put_on_empty(poss_list:list,blk_len:int):
		put_on_same_color(poss_list,0,blk_len)

	return {'same_color':put_on_same_color,'comb':combinations,'on_empty':put_on_empty}





