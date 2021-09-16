from global_vars import * 

def regressions(lf,emp,ahrs):
  import stata_setup
  stata_setup.config('/Applications/Stata/', 'be')
  from pystata import stata

  samples = [lf,emp,ahrs]
  outcomes = ['labforce','emp','ahrsworkt']
  reg_type = ['logit','logit','regress']

  ################ FULL REGRESSIONS
  stata.run('''
  est clear
  ''')
  
  reglist = [
    "eststo: gsem ({outcome} <- `list' c.sharemiddlehighclosed50#c.nchildmh c.shareelemclosed50#c.nchildele `datelist', {reg}), vce(cl cpsid) nolog", 
    "eststo: gsem ({outcome} <- `list' `indints' `sexints' `raceints' `citints' `marints' `eduints' `incints' c.sharemiddlehighclosed50#c.nchildmh c.shareelemclosed50#c.nchildele `datelist', {reg}), vce(cl cpsid) nolog",
    "eststo: gsem ({outcome} <- `list' c.sharemiddlehighclosed50#c.nchildmh c.shareelemclosed50#c.nchildele L[county], {reg}), vce(robust) nolog",
    "eststo: gsem ({outcome} <- `list' `indints' `sexints' `raceints' `citints' `marints' `eduints' `incints' c.sharemiddlehighclosed50#c.nchildmh c.shareelemclosed50#c.nchildele L[county], {reg}), vce(robust) nolog",
    '''eststo: gsem ({outcome} <- `list' c.sharemiddlehighclosed50#c.nchildmh c.shareelemclosed50#c.nchildele `datelist', {reg}) ///
       (sharemiddlehighclosed50 <- `list' expensesstudents `datelist', family(beta) link(logit)) ///
       (shareelemclosed50 <- `list' expensesstudents `datelist', family(beta) link(logit)), vce(cl cpsid) nolog
    ''',
    '''eststo: gsem ({outcome} <- `list' `indints' `sexints' `raceints' `citints' `marints' `eduints' `incints' c.sharemiddlehighclosed50#c.nchildmh c.shareelemclosed50#c.nchildele `datelist', {reg}) ///
       (sharemiddlehighclosed50 <- `list' `indints' expensesstudents `datelist', family(beta) link(logit)) ///
       (shareelemclosed50 <- `list' `indints' expensesstudents `datelist', family(beta) link(logit)), vce(cl cpsid) nolog
    '''
    ]
  titlelist = [
  "(Full) Base: Month-Year FE, Std. Errors Clustered at the Family Level \label{{reg1}}", 
  "(Full) Base: Month-Year FE, Std. Errors Clustered at the Family Level with Int \label{{reg2}}",
  "(Full) Base: County RE, Heteroskedasticity Robust Std.Errors \label{{reg3}}",
  "(Full) Base: County RE, Heteroskedasticity Robust Std.Errors with Int \label{{reg4}}",
  "(Full) Instrumented: Month-Year FE, Std. Errors Clustered at the Family Level \label{{reg5}}",
  "(Full) Instrumented: Month-Year FE, Std. Errors Clustered at the Family Level with Int \label{{reg6}}",
    ]
  droplist = [
  " `datelist' ", 
  " `datelist' ", 
  " L[county] ", 
  " L[county] ",
  " `datelist' ",
  " `datelist' ", 
    ]
  
  for y in range(0,len(reglist)):
    for x in range(0,len(samples)): 
      stata.pdataframe_to_data(samples[x], force=True)
      stata.run('''
      *** Full Regressions
      *** Omitted Indicators: White, Some College, Spouse Present, Industry 0, January 2019
      
      lab var labforce "In Labor Force"
      lab var emp "Employed, at work"
      lab var ahrsworkt "Hours Worked (log)"

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
      lab var faminc "Fam Inc (k \$)"
      lab var newdeathrate "COV Death/100k"
      lab var newcaserate "COV Cases/100k"
      lab var gpsawayfromhome " \% $\Delta$ T Away Home"

      lab var sharemiddlehighclosed50 "\% MH Closed"
      lab var shareelemclosed50 "\% Elem Closed"
      lab var expensesstudents "Union Expen"

      local datelist " date1112020	date1112021	date11012019	date11012020	date11112019	date11112020	date1212019	date1212020	date1212021	date1312019	date1312020	date1312021	date1412019	date1412020	date1412021	date1512019	date1512020	date1612019	date1612020	date1912019	date1912020 "

      local list " nchildmh nchildele raceamericanindian raceasian raceblack racemixedrace racepacificislander marstdivorced marstseparated marstsingle marstspouseabsent marstwidowed educ10 educ11 educ9 educcollege educhs educhigher ind1 ind2 ind3 ind4 ind5 ind6 ind7 ind8 ind9 sex citizen hispan age faminc newdeathrate newcaserate gpsawayfromhome "
      local indints " ind1#c.gpsawayfromhome  ind2#c.gpsawayfromhome  ind3#c.gpsawayfromhome  ind4#c.gpsawayfromhome  ind5#c.gpsawayfromhome  ind6#c.gpsawayfromhome  ind7#c.gpsawayfromhome  ind8#c.gpsawayfromhome  ind9#c.gpsawayfromhome "
      local sexints " sex#c.nchildmh#c.sharemiddlehighclosed50 sex#c.nchildele#c.shareelemclosed50 "
      local raceints " raceblack#c.nchildmh#c.sharemiddlehighclosed50 raceblack#c.nchildele#c.shareelemclosed50 raceasian#c.nchildmh#c.sharemiddlehighclosed50 raceasian#c.nchildele#c.shareelemclosed50 raceamericanindian#c.nchildmh#c.sharemiddlehighclosed50 raceamericanindian#c.nchildele#c.shareelemclosed50 racepacificislander#c.nchildmh#c.sharemiddlehighclosed50 racepacificislander#c.nchildele#c.shareelemclosed50 racemixedrace#c.nchildmh#c.sharemiddlehighclosed50 racemixedrace#c.nchildele#c.shareelemclosed50 hispan#c.nchildmh#c.sharemiddlehighclosed50 hispan#c.nchildele#c.shareelemclosed50 "
      local citints " citizen#c.nchildmh#c.sharemiddlehighclosed50 citizen#c.nchildele#c.shareelemclosed50 "
      local marints " marstdivorced#c.nchildmh#c.sharemiddlehighclosed50 marstdivorced#c.nchildele#c.shareelemclosed50 marstsingle#c.nchildmh#c.sharemiddlehighclosed50 marstsingle#c.nchildele#c.shareelemclosed50 marstseparated#c.nchildmh#c.sharemiddlehighclosed50 marstseparated#c.nchildele#c.shareelemclosed50 marstspouseabsent#c.nchildmh#c.sharemiddlehighclosed50 marstspouseabsent#c.nchildele#c.shareelemclosed50 "
      local eduints " educcollege#c.nchildmh#c.sharemiddlehighclosed50 educcollege#c.nchildele#c.shareelemclosed50 educhs#c.nchildmh#c.sharemiddlehighclosed50 educhs#c.nchildele#c.shareelemclosed50 educhigher#c.nchildmh#c.sharemiddlehighclosed50 educhigher#c.nchildele#c.shareelemclosed50 educ9#c.nchildmh#c.sharemiddlehighclosed50 educ9#c.nchildele#c.shareelemclosed50 educ10#c.nchildmh#c.sharemiddlehighclosed50 educ10#c.nchildele#c.shareelemclosed50 educ11#c.nchildmh#c.sharemiddlehighclosed50 educ11#c.nchildele#c.shareelemclosed50"
      local incints " c.faminc#c.nchildmh#c.sharemiddlehighclosed50 c.faminc#c.nchildele#c.shareelemclosed50 "

      {reglist}
    
      '''.format(reglist = reglist[y]).format(outcome = outcomes[x], reg = reg_type[x])
      )

    stata.run('''
    esttab using "Outputs/tables/full_regressions{number}.tex", long booktabs label replace  ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    drop({drop}) ///
    title( {title} ) ///
    nomtitle collabels(none) ///
    alignment(D{{.}}{{.}}{{-1}})  ///
    mgroups("Labor Force" "Employed" "Hours Worked (log)", pattern(1 1 1) prefix(\multicolumn{{@span}}{{c}}{{) suffix(}}) span erepeat(\cmidrule(lr){{@span}}))

    est clear
    '''.format(number = str(6), title = titlelist[y], drop = droplist[y])
    )
  
  ############# PARENT REGRESSIONS
  stata.run('''
  est clear
  ''')

  reglist = [
    "eststo: gsem ({outcome} <- `list' xl `datelist', {reg}), vce(cl cpsid) nolog", 
    "eststo: gsem ({outcome} <- `list' `indints' `sexints' `raceints' `citints' `marints' `eduints' `incints' xl `datelist', {reg}), vce(cl cpsid) nolog",
    "eststo: gsem ({outcome} <- `list' xl L[county], {reg}), vce(robust) nolog", 
    "eststo: gsem ({outcome} <- `list' `indints' `sexints' `raceints' `citints' `marints' `eduints' `incints' xl L[county], {reg}), vce(robust) nolog",
    '''eststo: gsem ({outcome} <- `list' xl `datelist', {reg}) ///
       (xl <- `list' bl `datelist', family(beta) link(logit)), vce(cl cpsid) nolog''',
    '''eststo: gsem ({outcome} <- `list' `indints' `sexints' `raceints' `citints' `marints' `eduints' `incints' xl `datelist', {reg}) ///
       (xl <- `list' `indints' bl `datelist', family(beta) link(logit)), vce(cl cpsid) nolog'''
    ]
  titlelist = ["(Parent) Base: Month-Year FE, Std Errors Clustered at the Family Level \label{{preg1}}", 
  "(Parent) Base: Month-Year FE, Std. Errors Clustered at the Family Level with Int \label{{preg2}}",
  "(Parent) Base: County RE, Heteroskedasticity Robust Std. Errors \label{{preg3}}",
  "(Parent) Base: County RE, Heteroskedasticity Robust Std. Errors with Int \label{{preg4}}",
  "(Parent) Instrumented: Month-Year FE, Std. Errors Clustered at the Family Level \label{{preg5}}",
  "(Parent) Instrumented: Month-Year FE, Std. Errors Clustered at the Family Level with Int \label{{preg6}}",
    ]
  droplist = [
  " `datelist' ", 
  " `datelist' ", 
  " L[county] ", 
  " L[county] ",
  " `datelist' ",
  " `datelist' ", 
    ]
  
  for y in range(0,len(reglist)):
    for x in range(0,len(samples)):
      data = samples[x][(samples[x]['percentnchildele'] > 0) | (samples[x]['percentnchildmh'] > 0)]
      stata.pdataframe_to_data(data, force=True)
      stata.run('''
      *** Full Regressions
      *** Omitted Indicators: White, Some College, Spouse Present, Industry 0, January 2019
      
      lab var labforce "In Labor Force"
      lab var emp "Employed, at work"
      lab var ahrsworkt "Hours Worked (log)"

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
      lab var faminc "Fam Inc (k \$)"
      lab var newdeathrate "COV Death/100k"
      lab var newcaserate "COV Cases/100k"
      lab var gpsawayfromhome " \% $\Delta$ T Away Home"

      lab var xl "Weighted Avg. School Closed Prob."
      lab var bl "Bartik Instr."

      local datelist " date1112020	date1112021	date11012019	date11012020	date11112019	date11112020	date1212019	date1212020	date1212021	date1312019	date1312020	date1312021	date1412019	date1412020	date1412021	date1512019	date1512020	date1612019	date1612020	date1912019	date1912020 "

      local list " percentnchildele raceamericanindian raceasian raceblack racemixedrace racepacificislander marstdivorced marstseparated marstsingle marstspouseabsent marstwidowed educ10 educ11 educ9 educcollege educhs educhigher ind1 ind2 ind3 ind4 ind5 ind6 ind7 ind8 ind9 sex citizen hispan age faminc newdeathrate newcaserate gpsawayfromhome "
      local indints " ind1#c.gpsawayfromhome  ind2#c.gpsawayfromhome  ind3#c.gpsawayfromhome  ind4#c.gpsawayfromhome  ind5#c.gpsawayfromhome  ind6#c.gpsawayfromhome  ind7#c.gpsawayfromhome  ind8#c.gpsawayfromhome  ind9#c.gpsawayfromhome "
      local sexints " sex#c.xl "
      local raceints " raceblack#c.xl raceasian#c.xl raceamericanindian#c.xl racepacificislander#c.xl racemixedrace#c.xl hispan#c.xl "
      local citints " citizen#c.xl "
      local marints " marstdivorced#c.xl marstsingle#c.xl marstseparated#c.xl marstspouseabsent#c.xl "
      local eduints " educcollege#c.xl educhs#c.xl educhigher#c.xl educ9#c.xl educ10#c.xl educ11#c.xl "
      local incints " c.faminc#c.xl "

      {reglist}
    
      '''.format(reglist = reglist[y]).format(outcome = outcomes[x], reg = reg_type[x])
      )

    stata.run('''
    esttab using "Outputs/tables/parent_regressions{number}.tex", long booktabs label replace  ///
    b(3) se(3) star(* 0.10 ** 0.05 *** 0.01) ///
    drop({drop}) ///
    title( {title} ) ///
    nomtitle collabels(none) ///
    alignment(D{{.}}{{.}}{{-1}})  ///
    mgroups("Labor Force" "Employed" "Hours Worked (log)", pattern(1 1 1) prefix(\multicolumn{{@span}}{{c}}{{) suffix(}}) span erepeat(\cmidrule(lr){{@span}}))

    est clear
    '''.format(number = str(y+1), title = titlelist[y], drop = droplist[y])
    )