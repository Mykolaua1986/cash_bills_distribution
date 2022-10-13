# this method will distribute available bills between amounts we neet to hand out
# by the way, the distribution seeks for minimal amount of bills that will be handed out per each payment
# method returns:
# dataframe: cantains bills distribution for each amount
# dictionary: amount of used bills for each denominations 
# dictionary: amount of left bills for each denominations 
# dictionary: amount of needed bills, which are not available in stock, for each denominations 
# integer: sum, which is impossibly to hand out because of the lack of bills
# integer: sum, which is impossibly to hand out because of absence of needed denomination in input list

# 2 input dictionaries which keys and values must be integers: 
# first contains list of amounts which we want to hand out, e.g.: {0:1230, 1:450, 2:54}
# this mean that we have to hand out 3 different amounts: $1230, $450, $54
# second - is the amount of cash bills we have in stock, e.g.: {100:13, 50:100, 20:10, 10:1, 5:0}
# this means that we have only 4 bills denominations: $100 - 13pcs, $50 - 100pcs, $20 - 10pcs, $10 - 1pcs
def bills_distribution(sumlist, str_count_bills):
    # check if all values are integers
    def check_types(vals_list):
        error_type = 0
        available_types = {int, float}
        for i in vals_list:
            if type(i) in available_types:
                if i != int(i):
                    error_type = 1
            else:
                error_type = 2
        return error_type
    chk = max(check_types(sumlist.values()), check_types(str_count_bills.values()), check_types(str_count_bills.keys()))
    if chk == 0:
        # sort dictionary keys by values
        str_count_bills = {i:str_count_bills[i] for i in sorted(str_count_bills)}
        # import pandas for operation on the result data frame
        import pandas as pd
        # create the dataframe
        # the index of dataframe is the key of second input dictioanry (so it may be not only an integer)
        # the column name of needed amount is "sum"
        # the colums name of rest amount is "sum_rest"
        sum_df = pd.DataFrame(list(sumlist.items())).set_index(0)
        sum_df.columns=['sum']
        sum_df['sum_rest'] = sum_df['sum']
        # create the dictionary of left bills denominations. at first it equals the dict with available amounts
        lft_count_bills = str_count_bills.copy()
        # create the list of available bills denominations in reversed order (from max to min)
        bil_names = [int(i) for i in reversed(str_count_bills.keys())]
        # method for defining the decimal exponent of number (the amount of zeros in the end of number)
        def zeros(num): 
            return len ([i for i in str(num)[::-1] if i == '0'])
        # creating utility column whith the number of end-zeros in amounts, this will be the operation order
        sum_df['order'] = sum_df['sum'].apply(zeros)

        # next code is necessary for creating 2 lists of corresponding quantities between 2 different bills denominations
        def get_q(m, n, st):
            res = 0
            for i in st:
                if i[0][0] == m and i[1][0] == n and res == 0:
                    res = (m, i[0][1], n, i[1][1])
            return res
        # this list creates correspondings in format: denomination_1 * quantity_1 = denomination_2 * quantity_2
        st = [] 
        for i in bil_names: 
            for j in bil_names:
                r = int(max(i,j)/min(i,j)+0.5) 
                for k in range(1,r*2): 
                    c = (k*i)/(j)
                    if c == int(c) and c != 1 and i != j and k%c != 0 and get_q(i,j,st) == 0 and get_q(j,i,st) == 0: 
                        st.append([[j,int(c)],[i,k],[0,0]])
        # this list creates correspondings in format: denomination_1 * quantity_1 + denomination_2 * quantity_2 = sum_1 + sum_2
        # where one sum equals to one of denominations and second sum is the number of higher exponent
        sm = [] 
        for i in st:
            if len(str(i[1][0])) == len(str(i[0][0])):
                num1 = i[1][0]
                qty1 = i[1][1]
                num0 = i[0][0]
                qty0 = i[0][1]
                lrg = 10**(zeros(num1)+1)
                for s in range(qty1):
                    res_s = num1*(s+1)+num0
                    res_n = res_s-lrg
                    if res_s >= lrg and lrg != 0 and res_n != num0 and res_n != num1 and res_n in bil_names and lrg in bil_names:
                        sm.append([[num0,1],[num1,s+1],[res_n,1],[lrg,1]])
                        lrg = 0
                num1 = i[0][0]
                qty1 = i[0][1]
                num0 = i[1][0]
                qty0 = i[1][1]
                lrg = 10**(zeros(num1)+1)
                for s in range(qty1):
                    res_s = num1*(s+1)+num0
                    res_n = res_s-lrg
                    if res_s >= lrg and lrg != 0 and res_n != num0 and res_n != num1 and res_n in bil_names and lrg in bil_names:
                        sm.append([[num0,1],[num1,s+1],[res_n,1],[lrg,1]])
                        lrg = 0

        # guessing the combinations of bills:
        # 1. create columns in data_frame, with the name of each denomination
        # rows contain quantity of each bill by each sum, start quantity is 0
        for b in bil_names: 
            sum_df[b] = int(0)
        # define the max value of bills
        mxbl = max(bil_names)
        # 2. iterate amounts by amount of zeros starting with less zeros
        for l in sum_df['order'].sort_values().unique():
            # 3. iterate each sum containing defined number of zeros (sorted by amount)
            for i in sum_df[sum_df['order']==l].sort_values('sum').iterrows():  
                rst = int(i[1]['sum_rest'])
                for nr in range(1,len(str(rst))+1):
                    if rst > 0: 
                        if len(str(rst))>=nr: 
                            dec = rst%(10**nr) 
                            if dec > 0: 
                                for bl in bil_names: 
                                    # 4. search fitting bills denominations starting with less denominations
                                    # or try to fit all available bills if the rest sum is greater then max denomination
                                    # commit used bill in the dataframe and its consumption in a dictioary
                                    if len(str(dec)) == len(str(bl)) or dec >= mxbl: 
                                        need_bills = int(dec/bl)
                                        deduct_bills = min(need_bills, lft_count_bills[bl])
                                        deduct_sum = int(deduct_bills * bl)
                                        lft_count_bills[bl] = lft_count_bills[bl] - deduct_bills
                                        sum_df.loc[i[0],bl] = int(sum_df.loc[i[0],bl] + deduct_bills)
                                        sum_df.loc[i[0],'sum_rest'] = int(sum_df.loc[i[0],'sum_rest'] - deduct_sum)
                                        dec = int(dec - deduct_sum)
                                        rst = int(rst - deduct_sum)
                                        # 5. calculate the rest by each zeros rest sum amount
                                        lrg = 10**(zeros(dec)+1)
                                # 5. if we dont have alailable bills for sum consumption - we try to guess the combination of other bills
                                if dec != 0 and rst >= lrg:
                                    for s in sm:
                                        while s[2][0] <= dec and lft_count_bills[s[0][0]] >= s[0][1] and lft_count_bills[s[1][0]] >= s[1][1]:
                                            bl_c1 = s[0][1]
                                            bl_v1 = s[0][0]
                                            bl_c2 = s[1][1]
                                            bl_v2 = s[1][0]
                                            lft_count_bills[bl_v1] -= bl_c1
                                            lft_count_bills[bl_v2] -= bl_c2
                                            sum_df.loc[i[0],bl_v1] = int(sum_df.loc[i[0],bl_v1] + bl_c1)
                                            sum_df.loc[i[0],bl_v2] = int(sum_df.loc[i[0],bl_v2] + bl_c2)
                                            sum_df.loc[i[0],'sum_rest'] = int(sum_df.loc[i[0],'sum_rest'] - (s[2][0]+s[3][0]))
                                            dec -= s[2][0]
                                            rst -= (s[2][0]+s[3][0])
                        # 6. if there is a rest of sum which doesnt fit any bill denomination - we commit that sum
                        else: 
                            for bl in bil_names:
                                need_bills = int(dec/bl)
                                deduct_bills = min(need_bills, lft_count_bills[bl])
                                deduct_sum = deduct_bills * bl
                                lft_count_bills[bl] = lft_count_bills[bl] - deduct_bills
                                sum_df.loc[i[0],bl] = int(sum_df.loc[i[0],bl] + deduct_bills)
                                sum_df.loc[i[0],'sum_rest'] = int(sum_df.loc[i[0],'sum_rest'] - deduct_sum)
                                dec = int(dec - deduct_sum)
                                rst = int(rst - deduct_sum)
                # 7. extra guessing cycle for rest of amount
                if rst > 0: 
                    for bl in bil_names:
                        need_bills = int(dec/bl)
                        deduct_bills = min(need_bills, lft_count_bills[bl])
                        deduct_sum = deduct_bills * bl
                        lft_count_bills[bl] = lft_count_bills[bl] - deduct_bills
                        sum_df.loc[i[0],bl] = int(sum_df.loc[i[0],bl] + deduct_bills)
                        sum_df.loc[i[0],'sum_rest'] = int(sum_df.loc[i[0],'sum_rest'] - deduct_sum)
                        dec = int(dec - deduct_sum)
                        rst = int(rst - deduct_sum)
            # 8. in case if bills are guessed not optimal - we make exchange for less count of total bills quantity
            for s in st:
                bl_c1 = s[0][1]
                bl_v1 = s[0][0]
                bl_c2 = s[1][1]
                bl_v2 = s[1][0]
                while sum_df.loc[i[0],bl_v1] >= bl_c1 and lft_count_bills[bl_v2] >= bl_c2:
                    sum_df.loc[i[0],bl_v1] -= bl_c1
                    sum_df.loc[i[0],bl_v2] += bl_c2
                    lft_count_bills[bl_v2] -= bl_c2
                    lft_count_bills[bl_v1] += bl_c1
        # 9. in case if bills are guessed not optimal - we make exchange for less count of total bills quantity
        for s in st:
            bl_c1 = s[0][1]
            bl_v1 = s[0][0]
            bl_c2 = s[1][1]
            bl_v2 = s[1][0]
            for i in sum_df.sort_values('sum', ascending=False).iterrows():
                ch_cn1 = i[1][bl_v1]
                while ch_cn1 >= bl_c1 and len(sum_df[sum_df[bl_v2]>=bl_c2])>0:
                    for j in sum_df.sort_values('sum').iterrows():
                        ch_cn2 = j[1][bl_v2]
                        while ch_cn2 >= bl_c2 and ch_cn1 >= bl_c1:
                            sum_df.loc[i[0],bl_v1] -= bl_c1
                            sum_df.loc[i[0],bl_v2] += bl_c2
                            sum_df.loc[j[0],bl_v2] -= bl_c2
                            sum_df.loc[j[0],bl_v1] += bl_c1
                            ch_cn1 -= bl_c1
                            ch_cn2 -= bl_c2 
        # create dictionary with used quantity of bills
        use_count_bills = {}
        for i in lft_count_bills:
            use_count_bills[i] = str_count_bills[i]-lft_count_bills[i]
        # create dictionary with quantity of bills thich we lack to hand out full amounts
        need_count_bills = {i:0 for i in bil_names}
        for i in sum_df.iterrows():
            rst = int(i[1]['sum_rest'])
            if rst > 0: 
                for bl in bil_names:
                    dec = int(str(rst)[-len(str(bl)):])
                    if dec > 0: 
                        need_bills = int(dec/bl)
                        need_sum = int(need_bills * bl)
                        need_count_bills[bl] = need_count_bills[bl] + need_bills
                        dec = dec - need_sum
                        rst = rst - need_sum
        # calculate sum which is impossoble to hand out because of lack of bills quantity
        sum_need = 0
        for i in need_count_bills:
            sum_need+=need_count_bills[i]*i
        # calculate sum which is impossoble to hand out because of absence of needed denomination in input list
        sum_rest = sum_df['sum_rest'].sum()-sum_need
        sum_df.drop('order', axis=1, inplace=True)
        return (sum_df, use_count_bills, lft_count_bills, need_count_bills, sum_need, sum_rest)
    else:
        if chk == 1:
            return 'not all values are integers'
        elif chk == 2:
            return 'not all values are numbers'
