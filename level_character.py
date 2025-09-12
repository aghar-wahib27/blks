from vital import randint,freq,choice,GetColoumsOf2DArray,CDFL

def SIZE():
    def upon_most_frequent_empty(**kargs)->list:
        blk_sz=kargs['size']
        # min_available=min(kargs['empty'])
        # sz=[  min(freq(kargs['empty']),int(blk_sz*0.75))  ]*2
        sz=[  max(min(freq(kargs['empty']),6),2)  ]*2

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

    def upon_random(**kargs):
        return choice([3,4,8,11,6])

    def upon_most_frequent_color(**kargs)->list:
        msfc=int(list(kargs['color_data'].keys())[list(kargs['color_data'].values()).index(max(kargs['color_data'].values()))])
        # return msfc if msfc!=-1 else upon_random()
        return upon_random()

    def restricted_random(**kargs):
        return choice(kargs['color_set'])

    return {'freq':upon_most_frequent_color,'rand':upon_random,'rest_rand':restricted_random}


def PROGRESS():
    def IsComplete(row_or_col:list,color:int):
        size = len(row_or_col)
        complete = 0
        for blk in row_or_col:
            if blk.state == color and color>0:
                complete += 1
        if complete == size :
            return 1
        else:
            return 0

    def complete(grid:any,*args):
        data = list(args)[0]
        # print(args,data)
        if data[-2] == 'row':
            matrix = grid.values
        else:
            matrix = GetColoumsOf2DArray(grid.values)

        is_complete = 0
        completed = [ [ IsComplete( row_or_col,row_or_col[0].state ), matrix.index( row_or_col ) ] for row_or_col in matrix]
        # print(completed)
        for check in completed:
            if check[0] :
                if check[1] not in  grid.blk_data.data['completed']:
                    is_complete = 1
                    grid.blk_data.data['completed'].append(check[1])
        # for row_or_col in matrix:
        #     color= row_or_col[0].state
        #     if color in data[0]:
        #         is_complete = IsComplete(row_or_col,color)
        #         print('check color',color,is_complete)

        # print('complete is ',is_complete)
        return is_complete

        
    def reduced_to(grid:any,*args):
        data = list(args)[0]
        # print(data,blk_data.data['colored_data']['all_colors'])
        if grid.blk_data.data['colored_data']['all_colors'][f'{data[0]}'] <=  data[1]:
            return 1
        else:
            return 0

    def consecutive():
        ...
        
    return {'com':complete,'red':reduced_to}
# hello world

def PUT_COND():
    def put_on_same_color(poss_list:list,st:int,*args):#poss_list:list,st:int
        put=[]
        std={str( st ):st,'0':st}
        for re in poss_list :
            re.state=0 if re.state==-1 else re.state
            if re.state in [st,0]: 
                put.append(1)
            else:
                put.append(0)

        return put,std
        
    def combinations(poss_list:list,st:int,*args):#poss_list:list,st:int,combs:dict,allow_same:0
        dta = list(args)[0]
        std={}
        std[f'{st}+0']=st
        if dta[-1]:
            std[f'{st}+{st}']=st
        put=[]

        for re in poss_list:
            re.state=0 if re.state==-1 else re.state
            ke=f'{st}+{re.state}'
            legit=0
            # print('this is dtass',dta,ke)
            if ke in dta[0].keys() :
                std[re.state]=dta[0][ke]
                legit=1
            if ke[::-1] in dta[0].keys():
                std[re.state]=dta[0][ke[::-1]]
                legit=1
            if ke[::-1] == f'{st}+0'[::-1] :
                legit=1
            if ke==ke[::-1]:
                legit=1

            put.append(legit)

        print(std)

        return put,CDFL([ dta[0], std ])

    def put_on_empty(poss_list:list,st:int,*args):#poss_list:list,blk_len:int
        return [put_on_same_color(poss_list,-1,*args)[0],{k:st for k in ['0',str(st)] }]

    return {'same_color':put_on_same_color,'comb':combinations,'on_empty':put_on_empty}







