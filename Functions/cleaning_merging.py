from global_vars import *

def cleaning_merging(): 
    ################## CPS ###################
    data = pd.read_csv('Data/cps_data.csv')

    data = data.apply(pd.to_numeric, errors='ignore')

    #Treat FAMINC (Family Income) Variable
    #data['FAMINC'] = data['FAMINC'].replace([100,210,300,430,470,500,600,710,720,730,740,820,830,841,842,843,999],['<5','5-7.5','7.5-10','10-12.5','12.5-15','15-20','20-25','25-30','30-35','35-40','40-50','50-60','60-75','75-100','100-150','>150',''])
    data['FAMINC'] = data['FAMINC'].replace([100,210,300,430,470,500,600,710,720,730,740,820,830,841,842,843,999],[5,6.25,8.75,11.25,13.75,17.5,22.5,27.5,32.5,37.5,45,55,67.5,87.5,125,150,''])

    #Treat RACE Variable
    data['RACE'] = pd.to_numeric(data['RACE'])
    data.loc[data['RACE']>=800, ['RACE']] = 'Mixed-Race'
    data['RACE'] = data['RACE'].replace([100,200,300,651,652,999],['White','Black','American Indian','Asian','Pacific Islander',''])

    # Treat MARST (Marital Status) Variable
    data['MARST'] = data['MARST'].replace([1,2,3,4,5,6,9],['Spouse Present','Spouse Absent','Separated','Divorced','Widowed','Single',''])
    
    #####Children definition#####
    #Create NCHILDSA (School-Age Children)
    data = data.assign(NCHILDSA = lambda x: (x['NCHILD']-x['NCHLT5']))
    data['NCHILDSA'] = data.apply(lambda x: x['NCHILDSA'] if (x['ELDCH']<=18) else 1 if ((x['NCHILDSA']==2) & (x['YNGCH']<=18) & (x['YNGCH']>=5)) else 0, axis=1)
    #Create NOTDISC (not discernible)
    data['NOTDISC'] = data.apply(lambda x: 1 if ((x['NCHILDSA']==0) & ((x['NCHILD']-x['NCHLT5'])>0) & (x['YNGCH']<=18)) else 0, axis=1)
    #Create NCHILDELE (Elementary Children)
    data['NCHILDELE'] = data.apply(lambda x: x['NCHILDSA'] if (x['ELDCH']<=12) else 1 if ((x['NCHILDSA']==2) & (x['YNGCH']<=12) & (x['YNGCH']>=5)) else 0, axis=1)
    #Create NOTDISCELE
    data['NOTDISCELE'] = data.apply(lambda x: 1 if (((x['NCHILDSA']>2) & (x['ELDCH']>12))|((x['NCHILDSA']==2) & (x['YNGCH']<5) & (x['ELDCH']>12))) else 0, axis=1)
    #Create NCHILDMH (Middle-High Children)
    data['NCHILDMH'] = data.apply(lambda x: (x['NCHILDSA']-x['NCHILDELE']) if (x['NOTDISCELE']==0) else 0, axis=1)
    
    #Treat CITIZEN
    data['CITIZEN'] = data['CITIZEN'].replace([1,2,3,4],'Citizen')
    data['CITIZEN'] = data['CITIZEN'].replace(5,'Not a Citizen')

    #Treat HISPAN (Hispanic)
    data['HISPAN'] = data['HISPAN'].replace(0,'Not Hispanic')
    data['HISPAN'] = data['HISPAN'].replace([100,200,300,400,500,600,611,612],'Hispanic')

    #Treat EDUC (educational attainment)
    data['EDUC'] = data['EDUC'].replace([1,2,10,20,30,40,50,60],['','Preschool','Elem','Middle','Junior','9','10','11'])
    data['EDUC'] = data['EDUC'].replace([71,73],'HS')
    data['EDUC'] = data['EDUC'].replace([81,91,92],'Some College')
    data['EDUC'] = data['EDUC'].replace(111,'College')
    data['EDUC'] = data['EDUC'].replace([123,124,125],'Higher')

    #Treat IND (Industry of last ocupation)
    data['IND'] = data.apply(lambda x: int(list(str(x['IND']))[0]) if (len(list(str(x['IND'])))==4) else 0 if (len(list(str(x['IND'])))==3) else 10, axis=1)

    #####Outcomes######
    
    #Treat EMPSTAT (employment)
    data.drop(data[data['EMPSTAT']==0].index, inplace = True)
    data.drop(data[data['EMPSTAT']==1].index, inplace = True)
    data['EMPSTAT'] = data['EMPSTAT'].replace([21,22],'Unemployed')
    data['EMPSTAT'] = data['EMPSTAT'].replace([10,12],['Employed - At Work','Employed - Not at Work'])
    data['EMPSTAT'] = data['EMPSTAT'].replace([32,34,36],'NILF')
    #Create EMP (Employed - At Work in last week)
    data['EMP'] = data.apply(lambda x: 1 if x['EMPSTAT']=='Employed - At Work' else 0, axis=1)
    
    #Treat LABFORCE (Labor force participation)
    data['LABFORCE'] = data['LABFORCE'].replace([0,1,2],['','NILF','LF'])

    #Treat AHRSWORKT (hours worked last week)
    data['AHRSWORKT'] = data['AHRSWORKT'].replace(999,0)

    ################## COVID/MOBILITY ##############
    covid = pd.read_csv('Data/COVID - County - Daily.csv', low_memory=False)
    covid = covid[['month','year','countyfips','new_death_rate','new_case_rate']]
    covid = covid.replace('.',0)
    covid[['new_death_rate','new_case_rate']] = covid[['new_death_rate','new_case_rate']].astype(float)
    covid = covid.groupby(['month','year','countyfips']).mean()

    mobility = pd.read_csv('Data/Google Mobility - County - Daily.csv')
    mobility = mobility[['month','year','countyfips','gps_away_from_home']]
    mobility = mobility.loc[~(mobility['gps_away_from_home']=='.')]
    mobility['gps_away_from_home'] = pd.to_numeric(mobility['gps_away_from_home'])
    mobility = mobility.groupby(['month','year','countyfips']).mean()

    cm = pd.merge(covid, mobility, how='inner', on=['month','year','countyfips'])
    cm = cm.dropna().reset_index()
    cm.columns = ['MONTH','YEAR','COUNTY','new_death_rate','new_case_rate','gps_away_from_home']
    
    ############## MERGE ##########
    school = pd.read_csv('Data/schools_county_csv.csv')
    union = pd.read_csv('Data/union.csv')
    union = union[['STATEFIP','Dues/Teachers','Revenue/Teachers','Expenses/Students']]

    data = pd.merge(data, cm, how = 'left', on =['YEAR','MONTH','COUNTY'])
    data = pd.merge(data, school, how = 'left', on =['YEAR','MONTH','COUNTY'])
    data = pd.merge(data, union, how='left', on=['STATEFIP'])
    data = data.reset_index()
    
    return data 