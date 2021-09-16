from global_vars import *

def df_mapper(df, LabelBinary, StandardScaler, Nothing):
        
        listlist =[]
        for i in LabelBinary:
                listlist.append( (i,sklearn.preprocessing.LabelBinarizer()) )
        for i in StandardScaler:
                listlist.append( ([i],sklearn.preprocessing.StandardScaler()) )
        for i in Nothing:
                listlist.append( (i, None) )
        
        mapper = DataFrameMapper(listlist, df_out=True)

        df = mapper.fit_transform(df)

        return df