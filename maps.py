from prod_charts.settings import *

file = gpd.read_file(r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\shape_file\STE_2021_AUST_GDA2020.shp')

print(file['STE_NAME21'].unique())

# # Plot with thicker borders
# fig, ax = plt.subplots(figsize=(10, 6))
# file.boundary.plot(ax=ax, linewidth=2, color="black")  # Increase linewidth
# file.plot(ax=ax, edgecolor="black", linewidth=1)  # Main map

# plt.show()