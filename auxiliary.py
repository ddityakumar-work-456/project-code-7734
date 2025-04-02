from prod_charts.settings import * 

class HELPERS_TOOLS:

    def __init__(self):
        pass

    #Function for marking customer Extreme valuable, Most valuable and valuable.
    def worth_meter(self, x):
        if x > 15:
            return "extreme_valuable"
        elif x > 5 and x < 15:
            return "most_valuable"
        else:
            return "valuable"
    
    #For getting dictionary of encoding
    def dict_encoding(self, dataframe, column):
        value_counts = dataframe[column].value_counts().index 
        sorted_values = sorted(value_counts)
        return {i: val for i, val in enumerate(sorted_values)}

    #Function for label encoding
    def lab_enc(self, dataframe,col_name):
        le= LabelEncoder()
        dataframe[f'{col_name}']=le.fit_transform(dataframe[f'{col_name}'])

    #Function for feature scaling
    def std_sca(self, dataframe,col_name):
        ssc= StandardScaler()
        dataframe[f'{col_name}']=ssc.fit_transform(dataframe[[f'{col_name}']])

    #Function for outlier removing
    def outlier_remover(self, dataframe,col_name):
        ul= dataframe[f'{col_name}'].mean() + 3*dataframe[f'{col_name}'].std()
        ll= dataframe[f'{col_name}'].mean() -3*dataframe[f'{col_name}'].std()

        ul_index= dataframe[dataframe[f'{col_name}'] > ul].index
        ll_index= dataframe[dataframe[f'{col_name}'] < ll].index

        req_index= np.append(ul_index,ll_index)

        dataframe.drop(req_index, axis=0, inplace=True)

    #Creating synthetic samples for dataset
    def equilising_targets(self, dataset, ycol):
        y= dataset[[ycol]]
        x= dataset.drop([ycol], axis=1)
        dg= imblearn.over_sampling.SMOTE()
        x,y= dg.fit_resample(x,y)
        dataset4= pd.concat([x,y], axis=1)
        return dataset4



