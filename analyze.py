import pandas as pd
from states import states

da = open('fund_a.txt','r')
db = open('fund_b.txt','r')

state = set()
country = set()
industry = set()
focus = set()
assetclass = set()
strategy = set()
status = set()
size = []

allfunds = [['NULL']*197 for i in range(23)]
#print(len(allfunds[0]))

# Read data and store to a 2-d matrix

line = da.readline()

index = 0
while line:
    temp = line.split(', ')
    temp[-1] = temp[-1][:-1]
    for i in range(len(temp)):
        allfunds[i][index] = (temp[i])
    #if len(temp) != 20:
    #    print(line)
    #print(temp)
    
    assetclass.add(temp[3])
    strategy.add(temp[4])
    status.add(temp[5])
    state.add(temp[16])
    country.add(temp[17])
    ind = temp[-1][1:-1].split(',')
    industry |= set(ind)
    if temp[13] != 'NULL':
        size.append(float(temp[13]))
    index += 1
    line = da.readline()

#print(index)
line = db.readline()
while line:
    temp = line.split(', ')
    temp[-1] = temp[-1][:-1]
    
    allfunds[0][index] = (temp[0])
    allfunds[20][index] = (temp[1])
    allfunds[1][index] = (temp[2])
    allfunds[11][index] = (temp[3])
    allfunds[3][index] = (temp[4])
    allfunds[4][index] = (temp[5])
    allfunds[5][index] = (temp[6])
    allfunds[13][index] = (temp[7])
    allfunds[7][index] = (temp[8])
    allfunds[19][index] = (temp[9])
    allfunds[15][index] = (temp[10])
    allfunds[16][index] = (temp[11])
    allfunds[17][index] = (temp[12])
    allfunds[9][index] = (temp[13])
    allfunds[10][index] = (temp[14])
    allfunds[8][index] = (temp[15])
    allfunds[21][index] = (temp[16])
    allfunds[22][index] = (temp[17])
    
    assetclass.add(temp[4])
    strategy.add(temp[5])
    status.add(temp[6])
    state.add(temp[11])
    country.add(temp[12])
    ind = temp[9][1:-1].split(',')
    industry |= set(ind)
    focus.add(temp[-1])
    if temp[7] != 'NULL':
        size.append(float(temp[7]))

    index += 1
    line = db.readline()
#print(index)
#print(allfunds)

# store the dataset to a dataframe
df = pd.DataFrame(columns = ['fund_id','fund_name','fund_former_name','asset_class','strategy','status','manager_id','manager','manager_phone','manager_website','manager_email','fund_vintage_year','fund_status','fund_size','native_currency','manager_city','manager_state_or_province','manager_country','manager_post_code','preferred_industries','firm_id','manager_fax','primary_geographic_focus'])

i = 0
for column in df:
    df[column] = allfunds[i]
    i += 1
print(df.columns)
#print(df.head())
df["fund_size"] = pd.to_numeric(df["fund_size"], errors='coerce')
df['fund_vintage_year'] = pd.to_numeric(df['fund_vintage_year'],errors='coerce')


# find duplicates and combine the two entries into the first entry
duplicate = df[df.duplicated(subset=['fund_name','asset_class','strategy','status','manager','fund_vintage_year','fund_size'], keep=False)]
fund_name = set(duplicate['fund_name'])
#print(duplicate[['fund_name','asset_class','strategy','status','manager','fund_vintage_year','fund_size','status','manager_country']])
#print(duplicate)

for n in fund_name:
    pair = duplicate.query('fund_name == "%s"'%n)
    p1 = pair.iloc[[0]].index[0]
    p2 = pair.iloc[[1]].index[0]
#    print(df.loc[p1])
#    print(pair.iloc[[1]])
    try: 
        size.remove(pair.loc[p2]['fund_size'])
    except:
        pass
    for column in pair.iloc[[1]]:
        #print('df: ',df.loc[p1][column])
        #print('dup: ',pair.loc[p2][column])
        if df.loc[p1][column]== 'NULL' and pair.loc[p2][column] != 'NULL':
            df.loc[p1][column]= pair.loc[p2][column]
    df = df.drop(p2)

'''
print('asset class: \n',assetclass)
print('strategy: \n',strategy)
print('fund country: \n',country)
print('industry focus: \n',industry)
print('geographic focus: \n',focus)
print('fund size range: %f - %f\n' % (min(size), max(size) ))
print()
'''

# filter by themes
print( ' -----------------------------------\n ' )

val = 'go'
flag = False
printque = False
while val != 'quit':
    print('asset class: 1, strategy: 2, fund country: 3, \nstatus: 4, geographic focus: 5, industry focus: 6, \nfund size: 7, quit: 0\n')
    val = input('What theme (core data (default) use flag -c, full data -a): ')
    
    if len(val)>1:
        if val[-1] == 'a':
            flag = True
        else:
            flag = False
        val = int(val[:1])
    else:
        flag = False
        val = int(val)

    if val == 0:
        break
    elif val == 1:
        val = input('%s \nType assest class: ' % assetclass)
        if val in assetclass:
            que = df.query('asset_class == "%s"'%val)
            printque = True
        else:
            val = input('Typo, try again (go back: type anything) :')
            if val in assetclass:
                que = df.query('asset_class == "%s"'%val)
                printque = True
    elif val == 2:
        val = input('%s \nType strategy: ' % strategy)
        if val in strategy:
            que = df.query('strategy == "%s"'%val)
            printque = True
        else:
            val = input('Typo, try again (go back: type anything) :')
            if val in strategy:
                que = df.query('strategy == "%s"'%val)
                printque = True
    elif val == 3:
        val = input('%s \nType country: ' % country)
        if val in country:
            que = df.query('manager_country == "%s"'%val)
            printque = True
        else:
            print('Country does not exist')
    elif val == 4:
        val = input('%s \nType status: ' % status)
        if val in status:
            que = df.query('status == "%s"'%val)
            printque = True
        else:
            val = input('Typo, try again (go back: type anything) :')
            if val in status:
                que = df.query('status == "%s"'%val)
                printque = True
    elif val == 5:
        val = input('%s \nType geographic focus: ' % focus)
        if val in focus:
            que = df.query('primary_geographic_focus == "%s"'%val)
            printque = True
        else:
            val = input('Typo, try again (go back: type anything) :')
            if val in focus:
                que = df.query('primary_geographic_focus == "%s"'%val)
                printque = True
    elif val == 6:
        val = input('%s \nType industry: ' % industry)
        if val in industry:
            que = df.query('preferred_industries.str.contains("%s")'%val, engine='python')
            printque = True
        else:
            val = input('Typo, try again (go back: type anything) :')
            if val in industry:
                que = df.query('preferred_industries.str.contains("%s")'%val, engine='python')
                printque = True
    elif val == 7:
        val = float(input('%f - %f \nType range \nMin: '%(min(size),max(size))))
        max_ =float(input("Max: "))
        que = df.query('%f <= fund_size <= %f'%(val,max_))
        printque = True

    #elif val == 8:
    #    val = input('Customize query: ')
    #    try:
    #        que = df.query(para)
    #        print(que)
    #    except:
    #        print('False Entry')

    if printque and val != 8:
        if flag:
            print(que)
            #que.to_csv('output.csv',mode = 'a', index=False) 
        else:
            core = que[['fund_name','asset_class','strategy','status','manager','fund_size','manager_country','preferred_industries','primary_geographic_focus']]
            print(core)
            #core.to_csv('output.csv',mode='a', index=False)
        printque = False

    

