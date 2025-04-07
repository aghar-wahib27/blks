
# big=[]

# class obj:
# 	def __init__(self,order:tuple):
# 		self.order=order
# 		self.state=order[0]+order[1]

# 	def __str__(self):
# 		return f'obj in pos:{self.order} its state is:{self.state}'

# 	def get_data(self):
# 		return {'order':self.order,'state':self.state}


# for i in range(20):
# 	for j in range(20):
# 		big.append(obj(order=(i,j)))

# r,c=14,10
# cn_mt=[(i-1+r,j-1+c) for i in range(3) for j in range(3)]

# def surr(center:tuple):
# 	return [(i-1+center[0],j-1+center[1]) for i in range(3) for j in range(3)]

# # for i in range(3):
# # 	for j in range(3):
# # 		cn_mt.append((i-1+r,j-1+c))

# def ROUA(obj_li:list,req_data:list):
# 	"""
# 	ROUA : return_obj_upon_attr
# 	"""
# 	for obj in obj_li : 
# 		data=obj.get_data()
# 		if data[req_data[0]]==req_data[1]:
# 			return obj
			

# # mod=[ ROUA(big,['order',order]) for order in surr((r,c)) ]

# # # [ print(obj) for obj in mod]
# # print( list((9,19)) )

# # def chek(ni):
# # 	if ni%2:
# # 		return 1
# # 	else : 
# # 		return -1

# # def neli(li:list):
# # 	return li + [-i for i in li]

# # print([ k*chek(i) for i,k in  enumerate([1,4,2,5]*2)])


# # print(neli([1,2,4,5]))

# print(7//6 + 1)

from random import choice

lis=[0,10,24,0,1,2,4,2,4,5,3,2,1]
print(max(lis),lis.count(2))
