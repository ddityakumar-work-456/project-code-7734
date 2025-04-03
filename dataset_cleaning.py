from prod_charts.settings import *

# Define the input file path
input_file_path = r'C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\dataset\KPMG.xlsx'

# Load Excel sheets into DataFrames
CustomerAddress = pd.read_excel(input_file_path, sheet_name='CustomerAddress', header=1)
CustomerDemographic = pd.read_excel(input_file_path, sheet_name='CustomerDemographic', header=1)
NewCustomerList = pd.read_excel(input_file_path, sheet_name='NewCustomerList', header=1)
Transactions = pd.read_excel(input_file_path, sheet_name='Transactions', header=1)



# ---------------------- Data Cleaning ----------------------


# 1.1 Validating Data Integrity

# Validate uniqueness of customer_id in CustomerAddress
assert not CustomerAddress['customer_id'].duplicated().any(), "Duplicate customer IDs found in CustomerAddress"

# Validate address field length
CustomerAddress['lena'] = CustomerAddress['address'].apply(len)
CustomerAddress.drop(columns=['lena'], inplace=True)

# Validate postcode format (should be exactly 4 digits)
CustomerAddress['postcode'] = CustomerAddress['postcode'].astype(str)
CustomerAddress['lenp'] = CustomerAddress['postcode'].apply(len)
assert not CustomerAddress.loc[CustomerAddress['lenp'] != 4, :].any().any(), "Invalid postcode lengths detected"
CustomerAddress.drop(columns=['lenp'], inplace=True)

# Map state abbreviations to full state names
mapping_dict = {
    'NSW': 'New South Wales',
    'VIC': 'Victoria',
    'QLD': 'Queensland',
    'New South Wales': 'New South Wales',
    'Victoria': 'Victoria'
}
CustomerAddress['state'] = CustomerAddress['state'].map(mapping_dict)

# Validate country values
print(CustomerAddress['country'].value_counts())  # No anomalies detected

# Validate property valuation values
print(CustomerAddress['property_valuation'].value_counts())  # All values have reasonable frequencies

# Validate uniqueness of customer_id in CustomerDemographic
assert not CustomerDemographic['customer_id'].duplicated().any(), "Duplicate customer IDs found in CustomerDemographic"

# Validate gender column by standardizing values
CustomerDemographic['gender'] = CustomerDemographic['gender'].replace({
    "F": "Female",
    "M": "Male",
    "Femal": "Female",
    "U": "Undefined"
})

# Ensure there are no negative values in past_3_years_bike_related_purchases
assert not (CustomerDemographic['past_3_years_bike_related_purchases'] < 0).any(), "Negative values found in bike purchases"

# Validate DOB column type
CustomerDemographic['DOB']= pd.to_datetime(CustomerDemographic['DOB'], errors='coerce')
assert CustomerDemographic['DOB'].dtype == 'datetime64[ns]', "DOB column is not of datetime type"

# Validate categorical fields
print(CustomerDemographic['job_title'].value_counts())
print(CustomerDemographic['job_industry_category'].value_counts())
print(CustomerDemographic['wealth_segment'].value_counts())
print(CustomerDemographic['deceased_indicator'].value_counts())
print(CustomerDemographic['owns_car'].value_counts())
print(CustomerDemographic['tenure'].value_counts())

# Validate Transactions DataFrame for duplicate IDs
for col in ['transaction_id', 'product_id', 'customer_id']:
    duplicate_count = Transactions[col].duplicated().sum()
    print(f"{col}: {duplicate_count} duplicates found")

# Validate categorical variables in Transactions
for col in ['online_order', 'order_status', 'brand', 'product_line', 'product_class', 'product_size']:
    print(f"{col}: {Transactions[col].value_counts().index}")

# Validate numerical attributes using boxplots
for col in ['list_price', 'standard_cost', 'product_first_sold_date']:
    sns.boxplot(Transactions[col])
    plt.show()



# 1.2 Handling Missing Values

# Drop unnecessary columns in CustomerDemographic
CustomerDemographic.drop(columns=['last_name', 'default'], inplace=True)

# Handle missing values in DOB and tenure by removing rows (only 2% missing data)
missing_dob_tenure = CustomerDemographic['DOB'].isnull().sum()
print(f"Removing {missing_dob_tenure} rows with missing DOB and tenure")
CustomerDemographic.dropna(subset=['DOB', 'tenure'], inplace=True)

# Drop job_industry_category as job_title provides similar information
CustomerDemographic.drop(columns=['job_industry_category'], inplace=True)

# Fill missing job titles using KNN Imputer
job_title_mapping = dict(zip(CustomerDemographic['job_title'].value_counts().index, range(len(CustomerDemographic['job_title'].value_counts().index))))
CustomerDemographic['job_title'] = CustomerDemographic['job_title'].map(job_title_mapping)
knn = KNNImputer(n_neighbors=10)
CustomerDemographic[['past_3_years_bike_related_purchases', 'tenure', 'job_title']] = knn.fit_transform(CustomerDemographic[['past_3_years_bike_related_purchases', 'tenure', 'job_title']])
CustomerDemographic['job_title'] = CustomerDemographic['job_title'].round().astype(int).map({v: k for k, v in job_title_mapping.items()})

# Drop missing values in Transactions (only 1% missing data)
Transactions.dropna(inplace=True)



# 1.3 Rectifying Values and Data Types

# Standardize deceased_indicator values
CustomerDemographic['deceased_indicator'] = CustomerDemographic['deceased_indicator'].replace({'Y': 'Yes', 'N': 'No'})

# Convert tenure to integer type
CustomerDemographic['tenure'] = CustomerDemographic['tenure'].astype(int)

# Standardize online_order column
Transactions['online_order'] = Transactions['online_order'].replace({0.0: 'No', 1.0: 'Yes'})

# Convert list_price and standard_cost to integer (rounding down)
Transactions['list_price'] = Transactions['list_price'].apply(math.floor)
Transactions['standard_cost'] = Transactions['standard_cost'].apply(math.floor)

# Convert product_first_sold_date to integer
Transactions['product_first_sold_date'] = Transactions['product_first_sold_date'].astype(int)



# 1.4 Checking for Duplicates
assert not CustomerAddress['customer_id'].duplicated().any(), "Duplicate customer IDs found in CustomerAddress"
assert not CustomerDemographic['customer_id'].duplicated().any(), "Duplicate customer IDs found in CustomerDemographic"
assert not Transactions['transaction_id'].duplicated().any(), "Duplicate transaction IDs found in Transactions"

# 1.5 Merging Datasets
print(f"CustomerAddress: {CustomerAddress.shape}, CustomerDemographic: {CustomerDemographic.shape}")
uncommon_customers = len(set(CustomerAddress['customer_id']) - set(CustomerDemographic['customer_id']))
print(f"There are {uncommon_customers} customers missing between datasets")

# Merge CustomerAddress and CustomerDemographic on customer_id
CustomerAddress.set_index('customer_id', inplace=True)
CustomerDemographic.set_index('customer_id', inplace=True)
Customer_complete = CustomerAddress.merge(CustomerDemographic, left_index=True, right_index=True)

Customer_complete.to_json(r"C:\Users\anish\OneDrive\Desktop\Projects\KPMG\project-code-7734\Input\dataset" + "//" + "customer_complete.json", orient= 'records')