from global_vars import *

def begin_process(segment):

  if 0 in segment: # clean/merge data
    df = cleaning_merging()
    pickle.dump(df, open(LOCAL_PATH + "Outputs/pickles/data_proc.p", "wb" ))

  if 1 in segment: # create regression samples
    df = pickle.load(open(LOCAL_PATH + "Outputs/pickles/data_proc.p", "rb" ))
    (lf, emp, ahrs) = reg_sample(df)
    pickle.dump(lf, open(LOCAL_PATH + "Outputs/pickles/lf_sample.p", "wb" ))
    pickle.dump(emp, open(LOCAL_PATH + "Outputs/pickles/emp_sample.p", "wb" ))
    pickle.dump(ahrs, open(LOCAL_PATH + "Outputs/pickles/ahrs_sample.p", "wb" ))
    
  if 2 in segment: # run regressions
    lf = pickle.load(open(LOCAL_PATH + "Outputs/pickles/lf_sample.p", "rb" ))
    emp = pickle.load(open(LOCAL_PATH + "Outputs/pickles/emp_sample.p", "rb" ))
    ahrs = pickle.load(open(LOCAL_PATH + "Outputs/pickles/ahrs_sample.p", "rb" ))
    regressions(lf,emp,ahrs)

  if 3 in segment: # create figures and summary stats
    lf = pickle.load(open(LOCAL_PATH + "Outputs/pickles/lf_sample.p", "rb" ))
    create_figures(lf)

  cleaned_file_path = LOCAL_PATH + "Outputs/csv/latest.csv"
  lf.to_csv(cleaned_file_path, index=False, quoting=csv.QUOTE_ALL)

if __name__ == '__main__':
    begin_process([2]) 

