from prod_charts.settings import *



class CategoricalMapPlotter:
    """
    Class for plotting categorical or choropleth maps using GeoPandas.
    """

    def __init__(
        self, gdf, column, title="Categorical Map", cmap="Set1", border_color="black",
        border_width=0.5, legend_title=None, figsize=(10, 6), save_path=None
    ):
        """
        Initializes the CategoricalMapPlotter class.

        Parameters:
        - gdf: GeoDataFrame with geometry column.
        - column: Name of the column to visualize.
        - title: Title of the map.
        - cmap: Colormap (default: 'Set1' for categorical, 'viridis' for choropleth).
        - border_color: Color of the borders (default: 'black').
        - border_width: Width of the borders (default: 0.5).
        - legend_title: Title of the legend (default: None).
        - figsize: Tuple defining figure size (default: (10, 6)).
        - save_path: Path to save the map as a PNG (default: None, meaning no save).
        """
        self.gdf = gdf
        self.column = column
        self.title = title
        self.cmap = cmap
        self.border_color = border_color
        self.border_width = border_width
        self.legend_title = legend_title
        self.figsize = figsize
        self.save_path = save_path

    def plot_map(self, choropleth=False):
        """
        Plots either a categorical or a choropleth map based on the given column.
        """
        fig, ax = plt.subplots(figsize=self.figsize)

        if choropleth:
            norm = mcolors.Normalize(
                vmin=self.gdf[self.column].min(), vmax=self.gdf[self.column].max()
            )
            sm = plt.cm.ScalarMappable(cmap=self.cmap, norm=norm)
            sm.set_array([])

            self.gdf.plot(
                ax=ax,
                column=self.column,
                cmap=self.cmap,
                linewidth=self.border_width,
                edgecolor=self.border_color,
                legend=True,
                norm=norm
            )
            plt.colorbar(sm, ax=ax, label=self.legend_title or self.column)
        else:
            self.gdf[self.column] = self.gdf[self.column].astype(str)
            unique_categories = self.gdf[self.column].unique()
            cmap = plt.get_cmap(self.cmap, len(unique_categories))
            color_dict = {cat: cmap(i) for i, cat in enumerate(unique_categories)}

            self.gdf.plot(
                ax=ax,
                column=self.column,
                edgecolor=self.border_color,
                linewidth=self.border_width,
                color=self.gdf[self.column].map(color_dict),
                legend=False,
            )

            handles = [
                plt.Line2D([0], [0], marker='o', color='w',
                           markerfacecolor=color_dict[cat], markersize=10, label=cat)
                for cat in unique_categories
            ]
            ax.legend(handles=handles, title=self.legend_title or self.column, loc='upper right')

        ax.set_title(self.title, fontsize=14)
        ax.axis("off")

        if self.save_path:
            plt.savefig(self.save_path, dpi=300, transparent=True, bbox_inches='tight')
        
        plt.show()


if __name__ == "__main__":
    state_shape_file = gpd.read_file(
        r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\shape_file\state_wise\STE_2021_AUST_GDA2020.shp"
    )
    postal_shape_file = gpd.read_file(
        r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\shape_file\postal_wise\POA_2021_AUST_GDA2020.shp"
    )

    state_shape_file = state_shape_file[['STE_NAME21', 'geometry']]
    state_shape_dict = dict(zip(state_shape_file['STE_NAME21'].values, state_shape_file['geometry'].values))
    
    postal_shape_file = postal_shape_file[['POA_CODE21', 'geometry']]
    postal_shape_dict = dict(zip(postal_shape_file['POA_CODE21'].values, postal_shape_file['geometry'].values))

    customers_data = pd.read_json(
        r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\dataset\customer_complete.json"
    )
    customers_data['postcode'] = customers_data['postcode'].astype(str)

    attributes = [
        'job_title', 'wealth_segment', 'deceased_indicator', 'owns_car',
        'tenure', 'property_valuation', 'gender', 'past_3_years_bike_related_purchases'
    ]

    for geos in tqdm.tqdm(['state', 'postcode']):
        for col in tqdm.tqdm(attributes):
            temp_ = customers_data[[geos, col]]
            
            if col in ['property_valuation', 'past_3_years_bike_related_purchases', 'tenure']:
                temp_ = temp_.pivot_table(index=[geos], values=col, aggfunc='average').reset_index()

            if geos == 'state':
                temp_['geometry'] = temp_[geos].map(state_shape_dict)
            elif geos == 'postcode':
                temp_['geometry'] = temp_[geos].map(postal_shape_dict)

            temp_ = gpd.GeoDataFrame(temp_, geometry='geometry', crs="EPSG:4326")

            output_path = (
                rf"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Output\Maps\Basic_Maps\{col}"
            )
            os.makedirs(output_path, exist_ok=True)
            save_file = rf"{output_path}\{geos}_{col}.png"

            plotter = CategoricalMapPlotter(
                temp_, column=col, title=f"{col} Distribution",
                cmap="Set2", border_width=1.0, save_path=save_file
            )
            plotter.plot_map()