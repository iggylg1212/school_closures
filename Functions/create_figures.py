from global_vars import *

def create_figures(df):
    ############## SUMMARY STATISTICS 
    import stata_setup
    stata_setup.config('/Applications/Stata/', 'be')
    from pystata import stata
    
    stata.pdataframe_to_data(df, force=True)
    stata.run('''
    est clear

    lab var labforce "In Labor Force"
    lab var emp "Employed, at work"
    lab var ahrsworkt "Hours Worked (log)"

    lab var racewhite "White"
    lab var marstspousepresent "Spouse Present"
    lab var educsomecollege "Some College"
    lab var ind0 "Ind 0"

    lab var nchildmh "\# MH"
    lab var nchildele "\# Elem"
    lab var raceamericanindian "Native American"
    lab var raceasian "Asian"
    lab var raceblack "Black"
    lab var racemixedrace "Mixed"
    lab var racepacificislander "Pacific"
    lab var marstdivorced "Divorced"
    lab var marstseparated "Separated"
    lab var marstsingle "Single"
    lab var marstspouseabsent "Spouse Absent"
    lab var marstwidowed "Widowed"
    lab var educ10 "10th Grade"
    lab var educ11 "11th Grade"
    lab var educ9 "9th Grade"
    lab var educcollege "College"
    lab var educhs "High School"
    lab var educhigher "Grad Deg"
    lab var ind1 "Ind 1"
    lab var ind2 "Ind 2"
    lab var ind3 "Ind 3"
    lab var ind4 "Ind 4"
    lab var ind5 "Ind 5"
    lab var ind6 "Ind 6"
    lab var ind7 "Ind 7"
    lab var ind8 "Ind 8"
    lab var ind9 "Ind 9"
    lab var sex "Female"
    lab var citizen "Citizen"
    lab var hispan "Hispan"
    lab var age "Age"
    lab var faminc "Fam Inc (k \\$)"
    lab var newdeathrate "COV Death/100k"
    lab var newcaserate "COV Cases/100k"
    lab var gpsawayfromhome " \% $\Delta$ T Away Home"

    generate indicator = 0 
    replace indicator=1 if (nchildele > 0)
    replace indicator=1 if (nchildmh > 0)

    estpost tabstat sex age faminc racewhite raceamericanindian raceasian raceblack racemixedrace hispan citizen nchildmh nchildele marstspousepresent marstdivorced marstseparated marstsingle marstspouseabsent marstwidowed  ///
    educ9 educ10 educ11 educhs educsomecollege educcollege educhigher ind0 ind1 ind2 ind3 ind4 ind5 ind6 ind7 ind8 ind9 labforce emp ahrsworkt, by(indicator) c(stat) stat(mean sd)
    
    esttab using "Outputs/tables/sumstat.tex", long booktabs replace ///
    cells(mean(fmt(2)) sd(par)) nostar unstack nonumber ///
    compress nonote noobs gap label title(Summary Statistics) ///
    collabels(none) ///
    eqlabels("Non-Parent" "Parent" "Total") /// 
    nomtitles

    generate  indindicator = 0 
    replace  indindicator=1 if (ind1==1)
    replace  indindicator=2 if (ind2==1)
    replace  indindicator=3 if (ind3==1)
    replace  indindicator=4 if (ind4==1)
    replace  indindicator=5 if (ind5==1)
    replace  indindicator=6 if (ind6==1)
    replace  indindicator=7 if (ind7==1)
    replace  indindicator=8 if (ind8==1)
    replace  indindicator=9 if (ind9==1)
    replace  indindicator=10 if (ind10==1)

    estpost tabstat sex age faminc racewhite raceamericanindian raceasian raceblack racemixedrace hispan citizen nchildmh nchildele marstspousepresent marstdivorced marstseparated marstsingle marstspouseabsent marstwidowed  ///
    educ9 educ10 educ11 educhs educsomecollege educcollege educhigher labforce emp ahrsworkt, by( indindicator) c(stat) stat(mean sd) nototal

    esttab using "Outputs/tables/sumstat_ind.tex", long booktabs replace ///
    cells(mean(fmt(2)) sd(par)) nostar unstack nonumber ///
    compress nonote noobs gap label title(Summary Statistics) ///
    collabels(none) ///
    eqlabels("Ind 0" "Ind 1" "Ind 2" "Ind 3" "Ind 4" "Ind 5" "Ind 6" "Ind 7" "Ind 8" "Ind 9" "No Job History") /// 
    nomtitles
    ''')

    ################ FIGURES
    ### SCHOOL CLOSURES ###
    df['date'] = pd.to_datetime(df['date'])
    county = df.groupby(['date', 'county']).mean().reset_index()
    national = df.groupby(['date']).mean().reset_index()

    #Elem
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Elem. Schools')
    ax.set_title('Share of Elementary Schools with >50% Decline in Mobility')
    ax.grid(True)
    
    ax.plot(national['date'], national['shareelemclosed50'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.legend(['National Average'])

    for count in list(set(county['county'])):
        county_series = county.loc[ county['county'] == count]
        ax.plot(county_series['date'], county_series['shareelemclosed50'], linestyle='--', color=numpy.random.rand(3,), alpha=0.1, label=count)

    plt.savefig('Outputs/figures/elem.png')

    #MH
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of MH Schools')
    ax.set_title('Share of Middle/High Schools with >50% Decline in Mobility')
    ax.grid(True)

    ax.plot(national['date'], national['sharemiddlehighclosed50'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.legend(['National Average'])

    for count in list(set(county['county'])):
        county_series = county.loc[ county['county'] == count]
        ax.plot(county_series['date'], county_series['sharemiddlehighclosed50'], linestyle='--', color=numpy.random.rand(3,), alpha=0.1, label=count)

    plt.savefig('Outputs/figures/mh.png')

    #MH v. Elem
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Schools')
    ax.set_title('Mean Elementary and Middle/High Closure')
    ax.grid(True)

    ax.plot(national['date'], national['sharemiddlehighclosed50'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.plot(national['date'], national['shareelemclosed50'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.legend(['Middle/High','Elementary'])

    plt.savefig('Outputs/figures/mh_elem.png')

    #MH v. Elem Variation 
    sd = county[['sharemiddlehighclosed50','shareelemclosed50','date','county']].groupby('date').std().reset_index()
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Standard Deviation')
    ax.set_title('Standard Deviation Elementary and Middle/High Closure')
    ax.grid(True)

    ax.plot(sd['date'], sd['sharemiddlehighclosed50'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.plot(sd['date'], sd['shareelemclosed50'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.legend(['Middle/High','Elementary'])

    plt.savefig('Outputs/figures/mh_elem_sd.png')

    ### MOBILITY ###
    # General 
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Change from Baseline')
    ax.set_title('Change in Time Spent Away from Home')
    ax.grid(True)

    ax.plot(national['date'], national['gpsawayfromhome'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['National Average'])

    for count in list(set(county['county'])):
        county_series = county.loc[ county['county'] == count]
        ax.plot(county_series['date'], county_series['gpsawayfromhome'], linestyle='--', color=numpy.random.rand(3,), alpha=0.1, label=count)

    plt.savefig('Outputs/figures/general_mobility.png')
    
    #Elem
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Change from Baseline')
    ax.set_title('Change in Time Spent at Elementary Schools')
    ax.grid(True)
    
    ax.plot(national['date'], national['meanelemchange'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.legend(['National Average'])

    for count in list(set(county['county'])):
        county_series = county.loc[ county['county'] == count]
        ax.plot(county_series['date'], county_series['meanelemchange'], linestyle='--', color=numpy.random.rand(3,), alpha=0.1, label=count)

    plt.savefig('Outputs/figures/elem_mobility.png')

    #MH
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Change from Baseline')
    ax.set_title('Change in Time Spent at Middle/High Schools')
    ax.grid(True)

    ax.plot(national['date'], national['meanmiddlehighchange'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.legend(['National Average'])

    for count in list(set(county['county'])):
        county_series = county.loc[ county['county'] == count]
        ax.plot(county_series['date'], county_series['meanmiddlehighchange'], linestyle='--', color=numpy.random.rand(3,), alpha=0.1, label=count)

    plt.savefig('Outputs/figures/mh_mobility.png')
    
    #Elem vs. MH vs. General
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Change from Baseline')
    ax.set_title('Elementary, Middle/High, General Mobility')
    ax.grid(True)

    ax.plot(national['date'], national['gpsawayfromhome'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(national['date'], national['meanelemchange'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(national['date'], national['meanmiddlehighchange'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.legend(['General','Elementary','Middle/High'])

    plt.savefig('Outputs/figures/general_elem_mh_mobility.png')

    ### LABOR OUTCOMES ###
    total = df.groupby('date').mean().reset_index()
    parents = df[(df['nchildele']>0) | (df['nchildmh']>0)].groupby('date').mean().reset_index()
    nonparents = df[(df['nchildele']==0) & (df['nchildmh']==0)].groupby('date').mean().reset_index()

    # labforce
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Labor Market Participation by Parental Status')
    ax.grid(True)

    ax.plot(total['date'], total['labforce'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.plot(parents['date'], parents['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(nonparents['date'], nonparents['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['Full Sample','Parents','Non-Parents'])

    plt.savefig('Outputs/figures/labforce.png')
    
    # emp
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Employment by Parental Status')
    ax.grid(True)

    ax.plot(total['date'], total['emp'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.plot(parents['date'], parents['emp'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(nonparents['date'], nonparents['emp'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['Full Sample','Parents','Non-Parents'])

    plt.savefig('Outputs/figures/emp.png')
    
    # ahrsworkt
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Log of Hours')
    ax.set_title('Hours Worked (log) by Parental Status')
    ax.grid(True)

    ax.plot(total['date'], total['ahrsworkt'], color=[0.25951375, 0.65019493, 0.84601207], label='national')
    ax.plot(parents['date'], parents['ahrsworkt'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(nonparents['date'], nonparents['ahrsworkt'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['Full Sample','Parents','Non-Parents'])

    plt.savefig('Outputs/figures/ahrsworkt.png')

    # Heterogeneities in the Parent Sample
    ####Sex
    parents = df[(df['nchildele']>0) | (df['nchildmh']>0)]
    total = parents.groupby('date').mean().reset_index()
    mothers = parents[parents['sex']==1].groupby('date').mean().reset_index()
    fathers = parents[parents['sex']==0].groupby('date').mean().reset_index()
    
    # labforce
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Labor Market Participation by Sex')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(mothers['date'], mothers['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(fathers['date'], fathers['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['Parents','Mothers','Father'])
    plt.savefig('Outputs/figures/sex_labforce.png')
    # emp
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Employment by Sex')
    ax.grid(True)
    ax.plot(total['date'], total['emp'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(mothers['date'], mothers['emp'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(fathers['date'], fathers['emp'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['Parents','Mothers','Father'])
    plt.savefig('Outputs/figures/sex_emp.png')
    # ahrsworkt
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Log of Hours')
    ax.set_title('Parental Hours Worked (log) by Sex')
    ax.grid(True)
    ax.plot(total['date'], total['ahrsworkt'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(mothers['date'], mothers['ahrsworkt'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(fathers['date'], fathers['ahrsworkt'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.legend(['Parents','Mothers','Fathers'])
    plt.savefig('Outputs/figures/sex_ahrsworkt.png')

    ####Race
    total = parents.groupby('date').mean().reset_index()
    white = parents[ parents['racewhite']==1].groupby('date').mean().reset_index()
    black = parents[parents['raceblack']==1].groupby('date').mean().reset_index()
    asian = parents[parents['raceasian']==1].groupby('date').mean().reset_index()
    na = parents[parents['raceamericanindian']==1].groupby('date').mean().reset_index()
    pi = parents[parents['racepacificislander']==1].groupby('date').mean().reset_index()
    mixed = parents[parents['racemixed-race']==1].groupby('date').mean().reset_index()
    hispanic = parents[parents['hispan']==1].groupby('date').mean().reset_index()

    # labforce
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Labor Market Participation by Race')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(white['date'], white['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(black['date'], black['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(asian['date'], asian['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(na['date'], na['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(pi['date'], pi['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(mixed['date'], mixed['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.plot(hispanic['date'], hispanic['labforce'], color=[0.16033522, 0.88255372, 0.10614918], label='national')
    ax.legend(['Parents','White','Black','Asian','Native American','Pacific','Mixed Race','Hispanic'])
    plt.savefig('Outputs/figures/race_labforce.png')
    # emp
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Employment by Race')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(white['date'], white['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(black['date'], black['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(asian['date'], asian['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(na['date'], na['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(pi['date'], pi['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(mixed['date'], mixed['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.plot(hispanic['date'], hispanic['labforce'], color=[0.16033522, 0.88255372, 0.10614918], label='national')
    ax.legend(['Parents','White','Black','Asian','Native American','Pacific','Mixed Race','Hispanic'])
    plt.savefig('Outputs/figures/race_emp.png')
    # ahrsworkt
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Log of Hours')
    ax.set_title('Parental Hours Worked (log) by Race')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(white['date'], white['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(black['date'], black['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(asian['date'], asian['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(na['date'], na['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(pi['date'], pi['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(mixed['date'], mixed['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.plot(hispanic['date'], hispanic['labforce'], color=[0.16033522, 0.88255372, 0.10614918], label='national')
    ax.legend(['Parents','White','Black','Asian','Native American','Pacific','Mixed Race','Hispanic'])
    plt.savefig('Outputs/figures/race_ahrsworkt.png')

    ####Education
    total = parents.groupby('date').mean().reset_index()
    nine = parents[parents['educ9']==1].groupby('date').mean().reset_index()
    ten = parents[parents['educ10']==1].groupby('date').mean().reset_index()
    eleven = parents[parents['educ11']==1].groupby('date').mean().reset_index()
    hs = parents[parents['educhs']==1].groupby('date').mean().reset_index()
    somecollege = parents[parents['educsomecollege']==1].groupby('date').mean().reset_index()
    college = parents[parents['educcollege']==1].groupby('date').mean().reset_index()
    higher = parents[parents['educhigher']==1].groupby('date').mean().reset_index()

    # labforce
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Labor Market Participation by Education')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(nine['date'], nine['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(ten['date'], ten['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(eleven['date'], eleven['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(hs['date'], hs['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(somecollege['date'], somecollege['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(college['date'], college['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.plot(higher['date'], higher['labforce'], color=[0.16033522, 0.88255372, 0.10614918], label='national')
    ax.legend(['Parents','9th Grade','10th Grade','11th Grade','High School','Some College','College','Higher Degree'])
    plt.savefig('Outputs/figures/educ_labforce.png')
    # emp
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Employment by Education')
    ax.grid(True)
    ax.plot(total['date'], total['emp'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(nine['date'], nine['emp'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(ten['date'], ten['emp'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(eleven['date'], eleven['emp'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(hs['date'], hs['emp'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(somecollege['date'], somecollege['emp'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(college['date'], college['emp'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.plot(higher['date'], higher['emp'], color=[0.16033522, 0.88255372, 0.10614918], label='national')
    ax.legend(['Parents','9th Grade','10th Grade','11th Grade','High School','Some College','College','Higher Degree'])
    plt.savefig('Outputs/figures/educ_emp.png')
    # ahrsworkt
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Log of Hours')
    ax.set_title('Parental Hours Worked (log) by Education')
    ax.grid(True)
    ax.plot(total['date'], total['ahrsworkt'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(nine['date'], nine['ahrsworkt'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(ten['date'], ten['ahrsworkt'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(eleven['date'], eleven['ahrsworkt'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(hs['date'], hs['ahrsworkt'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(somecollege['date'], somecollege['ahrsworkt'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(college['date'], college['ahrsworkt'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.plot(higher['date'], higher['ahrsworkt'], color=[0.16033522, 0.88255372, 0.10614918], label='national')
    ax.legend(['Parents','9th Grade','10th Grade','11th Grade','High School','Some College','College','Higher Degree'])
    plt.savefig('Outputs/figures/educ_ahrsworkt.png')

    ####Marital Status
    total = parents.groupby('date').mean().reset_index()
    divorced = parents[parents['marstdivorced']==1].groupby('date').mean().reset_index()
    separated = parents[parents['marstseparated']==1].groupby('date').mean().reset_index()
    single = parents[parents['marstsingle']==1].groupby('date').mean().reset_index()
    absent = parents[parents['marstspouseabsent']==1].groupby('date').mean().reset_index()
    present = parents[parents['marstspousepresent']==1].groupby('date').mean().reset_index()
    widow = parents[parents['marstwidowed']==1].groupby('date').mean().reset_index()

    # labforce
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Labor Market Participation by Marital Status')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(divorced['date'], divorced['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(separated['date'], separated['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(single['date'], single['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(absent['date'], absent['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(present['date'], present['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(widow['date'], widow['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.legend(['Parents','Divorced','Separated','Single','Spouse Absent','Spouse Present','Widowed'])
    plt.savefig('Outputs/figures/marst_labforce.png')
    # emp
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Share of Individuals')
    ax.set_title('Parental Employment by Marital Status')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(divorced['date'], divorced['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(separated['date'], separated['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(single['date'], single['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(absent['date'], absent['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(present['date'], present['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(widow['date'], widow['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.legend(['Parents','Divorced','Separated','Single','Spouse Absent','Spouse Present','Widowed'])
    plt.savefig('Outputs/figures/marst_emp.png')
    # ahrsworkt
    plt.rc('font', size=12)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlabel('Date')
    ax.set_ylabel('Log of Hours')
    ax.set_title('Parental Hours Worked (log) by Marital Status')
    ax.grid(True)
    ax.plot(total['date'], total['labforce'], color=[0.0, 0.0, 0.0], label='national')
    ax.plot(divorced['date'], divorced['labforce'], color=[0.59199461, 0.86842389, 0.28947468], label='national')
    ax.plot(separated['date'], separated['labforce'], color=[0.11573491, 0.76799684, 0.69802386], label='national')
    ax.plot(single['date'], single['labforce'], color=[0.86759609, 0.0266954 , 0.40652914], label='national')
    ax.plot(absent['date'], absent['labforce'], color=[0.64098925, 0.41325821, 0.5798281 ], label='national')
    ax.plot(present['date'], present['labforce'], color=[0.34468937, 0.6967772 , 0.86020477], label='national')
    ax.plot(widow['date'], widow['labforce'], color=[0.89654792, 0.15419679, 0.15647831], label='national')
    ax.legend(['Parents','Divorced','Separated','Single','Spouse Absent','Spouse Present','Widowed'])
    plt.savefig('Outputs/figures/marst_ahrsworkt.png')