from global_vars import *
from Functions.df_mapper import *

def reg_sample(df):
    ######### CLEANING/MASKING #######
    df = df.loc[~(df['COUNTY']==0)]
    df = df.loc[~(df['EDUC']=='Preschool')]
    df = df.loc[~(df['EDUC']=='Elem')]
    df = df.loc[~(df['EDUC']=='Junior')]
    df = df.loc[~(df['EDUC']=='Middle')]
    df['IND'] = pd.to_numeric(df['IND'])
    df['AHRSWORKT'] = df['AHRSWORKT'].apply(lambda x: np.log(float(x)) if (x>=1) else 0.0)
    df = df.loc[(df['NOTDISC']==0) & (df['NOTDISCELE']==0) & (df['AGE']>=18) & (df['NCHLT5']==0)]
    df = df.loc[~(df['MONTH'].isin([7,8,12]))]

    df = df[['YEAR','MONTH','CPSID','CPSIDP','STATEFIP','COUNTY','FAMINC','AGE','SEX','RACE','MARST','CITIZEN','HISPAN','EDUC','EMP','IND','LABFORCE','AHRSWORKT','NCHILDELE','NCHILDMH','new_death_rate','new_case_rate','gps_away_from_home','share_elem_closed_50','share_middlehigh_closed_50','mean_elem_change','mean_middlehigh_change','Dues/Teachers','Revenue/Teachers','Expenses/Students']]
        
    df['DATE'] = df.apply(lambda x: str(x['MONTH'])+'/1/'+str(x['YEAR']), axis=1)

    ######### REMOVING COUNTIES W/O MOBILITY DATA#####
    df = df.sort_values(by=['COUNTY','gps_away_from_home'])

    for i in list(set(df['COUNTY'])):
        obj = df.loc[(df['COUNTY']==i)]
        if pd.isnull(obj['gps_away_from_home'].iloc[0]):
            print(f'Delete  {str(i)}')
            df = df.loc[~(df['COUNTY']==i)]
    
    ####### FILLING PRE-COVID DATA #########
    fill = df[['new_death_rate','new_case_rate','gps_away_from_home','share_elem_closed_50','share_middlehigh_closed_50','mean_elem_change','mean_middlehigh_change']]
    fill = fill.fillna(0)
    df = df[['DATE','CPSID','CPSIDP','STATEFIP','COUNTY','FAMINC','AGE','SEX','RACE','MARST','CITIZEN','HISPAN','EDUC','EMP','IND','LABFORCE','AHRSWORKT','NCHILDELE','NCHILDMH','Dues/Teachers','Revenue/Teachers','Expenses/Students']]
    df = pd.concat([df,fill], axis=1)

    ##### APPLYING TRANSFORMATION TO COVARIATES ######
    
    df['LABFORCE'] = df['LABFORCE'].replace(['NILF','LF'],[0,1])
    df['SEX'] = df['SEX'].replace([1,2],[0,1])
    df['CITIZEN'] = df['CITIZEN'].replace(['Citizen','Not a Citizen'],[1,0])
    df['HISPAN'] = df['HISPAN'].replace(['Not Hispanic','Hispanic'],[0,1])
    df['DATE1'] = df['DATE']
    
    label = ['RACE','MARST','EDUC','IND','DATE1']
    scaler = []
    nothing = ['DATE','CPSID','CPSIDP','STATEFIP','LABFORCE','SEX','CITIZEN','HISPAN','AHRSWORKT','EMP','AGE','FAMINC','NCHILDELE','NCHILDMH','COUNTY','new_death_rate','new_case_rate','gps_away_from_home','share_elem_closed_50','share_middlehigh_closed_50','mean_elem_change','mean_middlehigh_change','Dues/Teachers','Revenue/Teachers','Expenses/Students']

    df = df_mapper(df, label, scaler, nothing)

    df[['RACE_American Indian', 'RACE_Asian', 'RACE_Black', 'RACE_Mixed-Race', 'RACE_Pacific Islander', 'RACE_White']] = df[['RACE_American Indian', 'RACE_Asian', 'RACE_Black', 'RACE_Mixed-Race', 'RACE_Pacific Islander', 'RACE_White', 'HISPAN']].apply(lambda x: 0 if x['HISPAN']==1 else x[['RACE_American Indian', 'RACE_Asian', 'RACE_Black', 'RACE_Mixed-Race', 'RACE_Pacific Islander', 'RACE_White']], axis=1)

    ###### Define BARTIK INSTRUMENT 
    
    df['percent_nchildele'] = df.apply(lambda x: x['NCHILDELE']/(x['NCHILDELE']+x['NCHILDMH']) if (x['NCHILDELE']+x['NCHILDMH'])>0 else 0.0, axis=1)
    df['percent_nchildmh'] = df.apply(lambda x: x['NCHILDMH']/(x['NCHILDELE']+x['NCHILDMH']) if (x['NCHILDELE']+x['NCHILDMH'])>0 else 0.0, axis=1)
    df['X_l'] = df.apply(lambda x: x['percent_nchildele']*x['share_elem_closed_50']+x['percent_nchildmh']*x['share_middlehigh_closed_50'], axis=1)
    ## B_l w/ natl. avg
    date_county = df[['DATE','COUNTY','share_elem_closed_50','share_middlehigh_closed_50']].groupby(['DATE','COUNTY']).mean().reset_index()
    for index, row in date_county.iterrows():
        date_county.at[index,'bartik_elem'] = date_county[(date_county['DATE']==row['DATE']) & (date_county['COUNTY']!=row['COUNTY'])]['share_elem_closed_50'].mean()
        date_county.at[index, 'bartik_mh'] = date_county[(date_county['DATE']==row['DATE']) & (date_county['COUNTY']!=row['COUNTY'])]['share_middlehigh_closed_50'].mean()
    del date_county['share_elem_closed_50']
    del date_county['share_middlehigh_closed_50']

    df = df.merge(date_county, how='left', on=['DATE', 'COUNTY'])
    df['B_l'] = df.apply(lambda x: x['percent_nchildele']*x['bartik_elem']+x['percent_nchildmh']*x['bartik_mh'], axis=1)

    ##### CREATE REG SAMPLES #######
    lf = df

    emp = df[df['LABFORCE']==1]
    
    ahrs = df[df['EMP']==1]

    ##### APPLY Smithson and Verkuilen (2006) Transform to betareg outcomes
    samples = [lf, emp, ahrs]
    for samp in samples:
        samp['share_elem_closed_50'] = samp['share_elem_closed_50'].apply(lambda x: (x*(len(samp)-1)+.5)/len(samp))
        samp['share_middlehigh_closed_50'] = samp['share_middlehigh_closed_50'].apply(lambda x: (x*(len(samp)-1)+.5)/len(samp))
        samp['X_l'] = samp['X_l'].apply(lambda x: (x*(len(samp)-1)+.5)/len(samp))

        samp.columns = samp.columns.str.replace('_','').str.replace(' ','').str.replace('/','').str.lower()

    return lf, emp, ahrs
