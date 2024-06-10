import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error

# Get preview of source data
def get_data_preview(file_path):
    xls = pd.ExcelFile(file_path)
    # Parse the sheets into DataFrames
    df_target = pd.read_excel(xls, 'Target')
    df_control = pd.read_excel(xls, 'Control')
    df_purchases = pd.read_excel(xls, 'Purchases')

    # Display the first few rows of each DataFrame to ensure they are loaded correctly
    print("Target DataFrame:")
    print(df_target.head())
    print("Control DataFrame:")
    print(df_control.head())
    print("Purchases DataFrame:")
    print(df_purchases.head())

    # Check columns for each DataFrame
    print("Columns in Target DataFrame:", df_target.columns)
    print("Columns in Control DataFrame:", df_control.columns)
    print("Columns in Purchases DataFrame:", df_purchases.columns)


# Load data from Excel file
def load_data(file_path):
    xls = pd.ExcelFile(file_path)
    df_target = pd.read_excel(xls, 'Target')
    df_control = pd.read_excel(xls, 'Control')
    df_purchases = pd.read_excel(xls, 'Purchases')
    return df_target, df_control, df_purchases


# Convert date columns to datetime
def convert_dates(df_target, df_purchases):
    df_target['target_month'] = pd.to_datetime(df_target['target_month'], format='%Y-%b')
    df_purchases['purchase_month'] = pd.to_datetime(df_purchases['purchase_month'], format='%Y-%b')


# Calculate common customers
def calculate_common_customers(df_target, df_control):
    common_customers = df_target[df_target['customer_id'].isin(df_control['customer_id'])]
    common_customers_percentage = (len(common_customers) / len(df_target)) * 100
    return common_customers_percentage


# Identify purchases within 3 months of the target month
def is_within_campaign(row):
    target_date = row['target_month']
    purchase_date = row['purchase_month']
    return (purchase_date >= target_date) & (purchase_date <= target_date + pd.DateOffset(months=3))


# Sum up purchase amounts in and out of campaign for target group
def calculate_campaign_purchases(df_purchases, df_target):
    df_purchases = df_purchases.merge(df_target, on='customer_id', how='left')
    df_purchases['in_campaign'] = df_purchases.apply(is_within_campaign, axis=1)
    target_in_campaign_purchases = df_purchases[df_purchases['in_campaign'] & df_purchases['target_month'].notnull()][
        'purchase_amount'].sum()
    target_out_campaign_purchases = df_purchases[~df_purchases['in_campaign'] & df_purchases['target_month'].notnull()][
        'purchase_amount'].sum()
    return target_in_campaign_purchases, target_out_campaign_purchases


# Sum up purchase amounts for control group in the specified period (Jan 2019 - Jun 2019)
def calculate_control_purchases(df_purchases, df_control):
    df_control_purchases = df_purchases[df_purchases['customer_id'].isin(df_control['customer_id'])]
    df_control_purchases_in_period = df_control_purchases[
        (df_control_purchases['purchase_month'] >= '2019-01-01') &
        (df_control_purchases['purchase_month'] <= '2019-06-30')
        ]
    control_group_purchases = df_control_purchases_in_period['purchase_amount'].sum()
    return control_group_purchases


# Additional statistics
def additional_statistics(df_purchases):
    avg_purchase_amount = df_purchases['purchase_amount'].mean()
    median_purchase_amount = df_purchases['purchase_amount'].median()
    std_dev_purchase_amount = df_purchases['purchase_amount'].std()
    return avg_purchase_amount, median_purchase_amount, std_dev_purchase_amount


# Apply a linear regression model to the data
def apply_regression_model(df_purchases):
    df_purchases['purchase_month'] = df_purchases['purchase_month'].map(lambda date: date.toordinal())
    X = df_purchases[['purchase_month']]
    y = df_purchases['purchase_amount']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    mae = mean_absolute_error(y_test, y_pred)
    return model, mse, mae


# Calculate campaign costs
def calculate_campaign_costs(df_target, fixed_costs, letter_cost):
    num_customers = len(df_target)
    total_costs = fixed_costs + (num_customers * letter_cost)
    return total_costs


# Main function to execute the analysis
def main():
    file_path = 'Data_kampan.xlsx'
    df_target, df_control, df_purchases = load_data(file_path)
    convert_dates(df_target, df_purchases)

    get_data_preview(file_path)

    common_customers_percentage = calculate_common_customers(df_target, df_control)
    print(f'Procento zákazníků v Target, kteří jsou také v Control: {common_customers_percentage:.2f}%')

    target_in_campaign_purchases, target_out_campaign_purchases = calculate_campaign_purchases(df_purchases, df_target)
    print(f'Celková suma nákupů v kampani pro Target: {target_in_campaign_purchases}')
    print(f'Celková suma nákupů mimo kampaň pro Target: {target_out_campaign_purchases}')

    control_group_purchases = calculate_control_purchases(df_purchases, df_control)
    print(f'Celková suma nákupů pro Control group během období leden 2019 - červen 2019: {control_group_purchases}')

    avg_purchase_amount, median_purchase_amount, std_dev_purchase_amount = additional_statistics(df_purchases)
    print(f'Průměrná výše nákupu: {avg_purchase_amount}')
    print(f'Medián výše nákupu: {median_purchase_amount}')
    print(f'Směrodatná odchylka výše nákupu: {std_dev_purchase_amount}')

    model, mse, mae = apply_regression_model(df_purchases)
    print(f'Model Mean Squared Error: {mse}')
    print(f'Model Mean Absolute Error: {mae}')

    # Calculate campaign costs
    fixed_costs = 38000
    letter_cost = 15
    campaign_costs = calculate_campaign_costs(df_target, fixed_costs, letter_cost)
    print(f'Celkové náklady na kampaň: {campaign_costs} Kč')

    # Calculate net revenue and ROI
    net_revenue = target_in_campaign_purchases - campaign_costs
    roi = (net_revenue / campaign_costs) * 100
    print(f'Čistý příjem z kampaně: {net_revenue} Kč')
    print("Plnění z kampaně bohužel neznáme, pokud by bylo 0 Kč, pak")
    print(f'návratnost investic (ROI): {roi:.2f}%')

    # Final assessment of the campaign
    print("Finální vyhodnocení:")
    if net_revenue > 0:
        print("Kampaň byla finančně úspěšná.")
    else:
        print("Kampaň nebyla finančně úspěšná.")


if __name__ == '__main__':
    main()