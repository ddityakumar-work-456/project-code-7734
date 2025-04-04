from prod_charts.settings import *

class MapPlotter:

    def __init__(self):
        pass

    def choropleth_map(self, dataframe, col_name, title, file_path, cmap= 'Set1', line_width= 0.2, edgecolor= 'black', legend= True):
        fig, ax = plt.subplots(1, 1, figsize=(12, 8))
        dataframe.plot(column=col_name,
                    cmap= cmap,  
                    linewidth=line_width,
                    ax=ax,
                    edgecolor=edgecolor,
                    legend=legend)
        plt.title(title)
        plt.axis('off')
        plt.savefig(file_path, dpi=300, transparent=True, bbox_inches='tight')


if __name__ == "__main__":

    plotter= MapPlotter()

    state_shape_file = gpd.read_file(
        r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\shape_file\state_wise\STE_2021_AUST_GDA2020.shp"
    )

    state_shape_file = state_shape_file[['STE_NAME21', 'geometry']]
    state_shape_file= state_shape_file.dropna().reset_index(drop=True)
    state_shape_file.rename(columns= {'STE_NAME21':"state"}, inplace=True)

    postal_shape_file = gpd.read_file(
        r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\shape_file\postal_wise\POA_2021_AUST_GDA2020.shp"
    )

    postal_shape_file = postal_shape_file[['POA_CODE21', 'geometry']]
    postal_shape_file= postal_shape_file.dropna().reset_index(drop=True)
    postal_shape_file.rename(columns= {'POA_CODE21':'postcode'}, inplace= True)

    customers_data = pd.read_json(
        r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\dataset\customer_complete.json"
    )
    customers_data['postcode'] = customers_data['postcode'].astype(str)

    attributes_numeric = [
        'tenure', 'property_valuation','past_3_years_bike_related_purchases'
    ]
    attributes_string = [
        'job_title', 'wealth_segment', 'deceased_indicator', 'owns_car','gender'
    ]

    for typ in tqdm.tqdm(['state', 'postcode']):

        for col in sorted(attributes_numeric + attributes_string):

            os.makedirs(r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Output\Maps\Basic_Maps' + "\\" + col, exist_ok= True)

            if col in attributes_numeric:

                if typ == 'state':

                    temp= customers_data[['state', col]]

                    for attr in tqdm.tqdm(['min', 'max', 'median', 'sum', 'mean']):

                        temp_= temp.pivot_table(index= ['state'], values=col, aggfunc=attr)
                        final_temp= state_shape_file.merge(temp_, on= 'state', how= 'left')
                        final_temp.fillna(0,  inplace= True)

                        plotter.choropleth_map(final_temp, col, col + "_" + attr, r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Output\Maps\Basic_Maps' + "\\" + col + "\\" + "state" + "_" + col + "_" + attr +".png")

                elif typ == 'postcode':

                    temp= customers_data[['postcode', col]]

                    for attr in tqdm.tqdm(['min', 'max', 'median', 'sum', 'mean']):

                        temp_= temp.pivot_table(index= ['postcode'], values=col, aggfunc=attr)
                        final_temp= postal_shape_file.merge(temp_, on= 'postcode', how= 'left')
                        final_temp.fillna(0,  inplace= True)

                        plotter.choropleth_map(final_temp, col, col + "_" + attr, r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Output\Maps\Basic_Maps' + "\\" + col + "\\" + "postcode" + "_" + col + "_" + attr +".png")


            elif col in attributes_string:

                for uniq in tqdm.tqdm(customers_data[col].unique()):

                    temp= customers_data[customers_data[col] == uniq].reset_index(drop=True)

                    if typ == 'state':

                        frt= pd.DataFrame(temp["state"].value_counts()).reset_index()
                        frt.columns= ['state', 'count']
                        final_temp= state_shape_file.merge(frt, on= 'state', how= 'left')
                        final_temp.fillna(0,  inplace= True)

                        plotter.choropleth_map(final_temp, "count", col + "_" + uniq, r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Output\Maps\Basic_Maps' + "\\" + col + "\\" + "state" + "_" + col + "_" + uniq +".png")

                    elif typ == 'postcode':

                        pasfrt= pd.DataFrame(temp["postcode"].value_counts()).reset_index()
                        pasfrt.columns= ['postcode', 'count']

                        final_temp= postal_shape_file.merge(pasfrt, on= 'postcode', how= 'left')

                        final_temp.fillna(0,  inplace= True)

                        plotter.choropleth_map(final_temp, 'count', col + "_" + uniq, r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Output\Maps\Basic_Maps' + "\\" + col + "\\" + "postcode" + "_" + col + "_" + uniq +".png")



