import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from dateutil.relativedelta import relativedelta

# Load the CSV file into a DataFrame
df = pd.read_csv('C:\\Ecomplete\\GMC - Data by Day.csv')

# 1. Strip whitespace from column names
df.columns = df.columns.str.strip()

# 2. Strip whitespace from all data in the DataFrame (only for string type)
df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

# 3. Replace '-' with NaN in numeric columns
currency_cols = ['net_revenue', 'product_revenue', 'shipping_revenue', 'cogs', 'GP', 'gross_discount',
                 'shipping_cost', 'TikTok_DTC_Spend', 'Google_Spend', 'Meta_spend', 'Microsoft_Spend',
                 'TikTok_Shop_Spend', 'new_customer_revenue', 'returning_customer_revenue', 'sessions_visitors']

df[currency_cols] = df[currency_cols].replace({'£': '', ',': '', '-': np.nan}, regex=True)

# 4. Convert currency and numeric columns to numeric types
df[currency_cols] = df[currency_cols].astype(float)

# 5. Convert date column to datetime format
df['date'] = pd.to_datetime(df['date'], format='%d/%m/%Y')

# 6. Save the cleaned data back to CSV (if needed)
df.to_csv('cleaned_data.csv', index=False)

# Display the cleaned DataFrame
#print(df.head())

df_cleaned = pd.read_csv('cleaned_data_test.csv')

#==============================
today = datetime.now().strftime('%Y/%m/%d')
today_date = datetime.now()
start_of_week = today_date - timedelta(days=today_date.weekday())
start_of_week_str = start_of_week.strftime('%Y/%m/%d')
this_day_last_week = today_date - timedelta(days=7)
day_last_week = this_day_last_week.strftime('%Y/%m/%d')

print(f'start of week{this_day_last_week}')
same_date_last_year = today_date - relativedelta(years=1)
same_date_last_year_str = same_date_last_year.strftime('%Y/%m/%d')
#print(f'todays datee last yearr{same_date_last_year_str}')
print("Dates")
print(today)
print(start_of_week_str)
print(same_date_last_year_str)
#========================================

df_cleaned['date'] = pd.to_datetime(df_cleaned['date'])
desired_date = today
filtered_data_day = df_cleaned[df_cleaned['date'] == today]
data_dtc_day = filtered_data_day[filtered_data_day['DTC_or_TikTok'] == 'DTC']
data_dtc_day.fillna(0, inplace=True)

revenue = data_dtc_day['net_revenue'].iloc[0]
########################

filtered_data_week = df_cleaned[df_cleaned['date'] == day_last_week]
data_dtc_week = filtered_data_week[filtered_data_week['DTC_or_TikTok'] == 'DTC']
data_dtc_week.fillna(0, inplace=True)

week_revenue = data_dtc_week['net_revenue'].iloc[0]
week_percentage = ((revenue - week_revenue) / revenue) * 100

year_date = same_date_last_year_str
filtered_data_year = df_cleaned[df_cleaned['date'] == same_date_last_year_str]
data_dtc_year = filtered_data_year[filtered_data_year['DTC_or_TikTok'] == 'DTC']
data_dtc_year.fillna(0, inplace=True)

year_revenue = data_dtc_year['net_revenue'].iloc[0]
year_percentage = ((revenue - year_revenue) / revenue) * 100

###########################

day_gp = data_dtc_day['GP'].iloc[0]
week_gp = data_dtc_week['GP'].iloc[0]
year_gp = data_dtc_year['GP'].iloc[0]
week_percentage_GP = ((day_gp - week_gp) / day_gp * 100)
year_percentage_GP = ((day_gp - year_gp) / day_gp * 100)


gp_percentage_day = ((day_gp / revenue) * 100)
gp_percentage_week = ((day_gp / week_revenue) * 100)
gp_percentage_year = ((day_gp / year_revenue) * 100)
gp_percentage_week_increase = ((gp_percentage_day - gp_percentage_week) / gp_percentage_day) * 100
gp_percentage_year_increase = ((gp_percentage_day - gp_percentage_year) / gp_percentage_year) * 100

day_orders = data_dtc_day['orders'].iloc[0]
week_orders = data_dtc_week['orders'].iloc[0]
year_orders = data_dtc_year['orders'].iloc[0]
week_orders_percentage = ((day_orders - week_orders) / day_orders * 100)
year_orders_percentage = ((day_orders - year_orders) / day_orders * 100)

aov_day = revenue / day_orders
aov_week = week_revenue / week_orders
aov_year = year_revenue / year_orders
week_aov_percentage = ((aov_day - aov_week) / aov_day) * 100
year_aov_percentage = ((aov_day - aov_year) / aov_day) * 100

day_sessions = data_dtc_day['sessions_visitors'].iloc[0]
week_sessions = data_dtc_week['sessions_visitors'].iloc[0]
year_sessions = data_dtc_year['sessions_visitors'].iloc[0]
week_sessions_percentage = ((day_sessions - week_sessions) / day_sessions) * 100
year_sessions_percentage = ((day_sessions - year_sessions) / day_sessions) * 100

day_conversion_rate = (day_orders / day_sessions) * 100
week_conversion_rate = (week_orders / week_sessions) * 100
year_conversion_rate = (year_orders / year_sessions) * 100
week_conversion_rate_percentage = ((day_conversion_rate - week_conversion_rate) / day_conversion_rate) * 100
year_conversion_rate_percentage = ((day_conversion_rate - year_conversion_rate) / day_conversion_rate) * 100

meta_spend = data_dtc_day['Meta_spend'].iloc[0]
google_spend = data_dtc_day['Google_Spend'].iloc[0]
microsoft_spend = data_dtc_day['Microsoft_Spend'].iloc[0]
tiktok_shop_spend = data_dtc_day['TikTok_Shop_Spend'].iloc[0]
tiktok_dtc_spend = data_dtc_day['TikTok_DTC_Spend'].iloc[0]
meta_spend_week = data_dtc_week['Meta_spend'].iloc[0]
google_spend_week = data_dtc_week['Google_Spend'].iloc[0]
microsoft_spend_week = data_dtc_week['Microsoft_Spend'].iloc[0]
tiktok_shop_spend_week = data_dtc_week['TikTok_Shop_Spend'].iloc[0]
tiktok_dtc_spend_week = data_dtc_week['TikTok_DTC_Spend'].iloc[0]
meta_spend_year = data_dtc_year['Meta_spend'].iloc[0]
google_spend_year = data_dtc_year['Google_Spend'].iloc[0]
microsoft_spend_year = data_dtc_year['Microsoft_Spend'].iloc[0]
tiktok_shop_spend_year = data_dtc_year['TikTok_Shop_Spend'].iloc[0]
tiktok_dtc_spend_year = data_dtc_year['TikTok_DTC_Spend'].iloc[0]

day_ad_spend = meta_spend + google_spend + microsoft_spend + tiktok_shop_spend + tiktok_dtc_spend + tiktok_dtc_spend
week_ad_spend = (meta_spend_week + google_spend_week + microsoft_spend_week + tiktok_shop_spend_week +
                 tiktok_dtc_spend_week)
year_ad_spend = (meta_spend_year + google_spend_year +
                 microsoft_spend_year + tiktok_shop_spend_year + tiktok_dtc_spend_year)
week_ad_spend_percentage = ((day_ad_spend - week_ad_spend) / day_ad_spend) * 100
year_ad_spend_percentage = ((day_ad_spend - year_ad_spend) / day_ad_spend) * 100

day_cos = (day_ad_spend / revenue) * 100
week_cos = (week_ad_spend / week_revenue) * 100
year_cos = (year_ad_spend / year_revenue) * 100
week_cos_percentage = ((day_cos - week_cos) / day_cos) * 100
year_cos_percentage = ((day_cos - year_cos) / day_cos) * 100

day_gp_post_ad = day_gp - day_ad_spend
week_gp_post_ad = week_gp - week_ad_spend
year_gp_post_ad = year_gp - year_ad_spend
week_gp_post_ad_percentage = ((day_gp_post_ad - week_gp_post_ad) / day_gp_post_ad) * 100
year_gp_post_ad_percentage = ((day_gp_post_ad - year_gp_post_ad) / day_gp_post_ad) * 100

day_gp_post_ad_percentage = (day_gp / revenue) * 100
week_gp_post_ad_percentage = (week_gp / week_revenue) * 100
year_gp_post_ad_percentage = (year_gp / year_revenue) * 100
week_gp_post_ad_percentage_increase = ((
                                                   day_gp_post_ad_percentage - week_gp_post_ad_percentage) / day_gp_post_ad_percentage) * 100
year_gp_post_ad_percentage_increase = ((
                                                   day_gp_post_ad_percentage - year_gp_post_ad_percentage) / day_gp_post_ad_percentage) * 100

day_contribution_pre_marketing = day_gp
week_contribution_pre_marketing = week_gp
year_contribution_pre_marketing = year_gp
week_contribution_pre_marketing_percentage = ((
                                                          day_contribution_pre_marketing - week_contribution_pre_marketing) / day_contribution_pre_marketing) * 100
year_contribution_pre_marketing_percentage = ((
                                                          day_contribution_pre_marketing - year_contribution_pre_marketing) / day_contribution_pre_marketing) * 100

day_contribution_post_marketing = day_gp_post_ad
week_contribution_post_marketing = week_gp_post_ad
year_contribution_post_marketing = year_gp_post_ad
week_contribution_post_marketing_percentage = ((
                                                           day_contribution_post_marketing - week_contribution_post_marketing) / day_contribution_post_marketing) * 100
year_contribution_post_marketing_percentage = ((
                                                           day_contribution_post_marketing - year_contribution_post_marketing) / day_contribution_post_marketing) * 100

cost_per_session_day = day_ad_spend / day_sessions
cost_per_session_week = week_ad_spend / week_sessions
cost_per_session_year = year_ad_spend / year_sessions
week_cost_per_session_percentage = ((cost_per_session_day - cost_per_session_week) / cost_per_session_day) * 100
year_cost_per_session_percentage = ((cost_per_session_day - cost_per_session_year) / cost_per_session_day) * 100

rev_per_session_day = revenue / day_sessions
rev_per_session_week = week_revenue / week_sessions
rev_per_session_year = year_revenue / year_sessions
week_rev_per_session_percentage = ((rev_per_session_day - rev_per_session_week) / rev_per_session_day) * 100
year_rev_per_session_percentage = ((rev_per_session_day - rev_per_session_year) / rev_per_session_day) * 100

new_cust_revenue_day = data_dtc_day['new_customer_revenue'].iloc[0]
new_cust_revenue_week = data_dtc_week['new_customer_revenue'].iloc[0]
new_cust_revenue_year = data_dtc_year['new_customer_revenue'].iloc[0]
week_new_cust_revenue_percentage = ((new_cust_revenue_day - new_cust_revenue_week) / new_cust_revenue_day) * 100
year_new_cust_revenue_percentage = ((new_cust_revenue_day - new_cust_revenue_year) / new_cust_revenue_day) * 100

ret_cust_revenue_day = data_dtc_day['returning_customer_revenue'].iloc[0]
ret_cust_revenue_week = data_dtc_week['returning_customer_revenue'].iloc[0]
ret_cust_revenue_year = data_dtc_year['returning_customer_revenue'].iloc[0]
week_ret_cust_revenue_percentage = ((ret_cust_revenue_day - ret_cust_revenue_week) / ret_cust_revenue_day) * 100
year_ret_cust_revenue_percentage = ((ret_cust_revenue_day - ret_cust_revenue_year) / ret_cust_revenue_day) * 100

ret_cust_orders_day = data_dtc_day['returning_customer_orders'].iloc[0]
ret_cust_orders_week = data_dtc_week['returning_customer_orders'].iloc[0]
ret_cust_orders_year = data_dtc_year['returning_customer_orders'].iloc[0]
week_ret_cust_orders_percentage = ((ret_cust_orders_day - ret_cust_orders_week) / ret_cust_orders_day) * 100
year_ret_cust_orders_percentage = ((ret_cust_orders_day - ret_cust_orders_year) / ret_cust_orders_day) * 100

new_cust_aov_day = new_cust_revenue_day / (day_orders - ret_cust_orders_day)
new_cust_aov_week = new_cust_revenue_week / (week_orders - ret_cust_orders_week)
new_cust_aov_year = new_cust_revenue_year / (year_orders - ret_cust_orders_year)
week_new_cust_aov_percentage = ((new_cust_aov_day - new_cust_aov_week) / new_cust_aov_day) * 100
year_new_cust_aov_percentage = ((new_cust_aov_day - new_cust_aov_year) / new_cust_aov_day) * 100

ret_cust_aov_day = ret_cust_revenue_day / ret_cust_orders_day
ret_cust_aov_week = ret_cust_revenue_week / ret_cust_orders_week
ret_cust_aov_year = ret_cust_revenue_year / ret_cust_orders_year
week_ret_cust_aov_percentage = ((ret_cust_aov_day - ret_cust_aov_week) / ret_cust_aov_day) * 100
year_ret_cust_aov_percentage = ((ret_cust_aov_day - ret_cust_aov_year) / ret_cust_aov_day) * 100

print("KPIs Yesterday Total")
print("=========================================================================")
print("Net Rev")
print(f'Yesterday £{revenue}')
print(f'vs Last Week £{week_revenue}, ({week_percentage:.2f}%)')
print(f'vs Last Year £{year_revenue}, ({year_percentage:.2f}%)')

print("      ")
print("Gross Profit")

print(f'Yesterday £{day_gp} ')
print(f'Last Week £{week_gp} ({week_percentage_GP:.2f}%)')
print(f'Last Year £{year_gp} ({year_percentage_GP:.2f}%)')
print("      ")
print("Gross Profit Percentage")
print(f'Gross profit percent {gp_percentage_day:.2f}%')
print(f'vs last week {gp_percentage_week:.2f}%  ({gp_percentage_week_increase:.2f}%)')
print(f'vs last year {gp_percentage_year:.2f}%  ({gp_percentage_year_increase:.2f}%)')
print("      ")

print("Number of Orders")

day_orders = data_dtc_day['orders'].iloc[0]
week_orders = data_dtc_week['orders'].iloc[0]
year_orders = data_dtc_year['orders'].iloc[0]
week_orders_percentage = ((day_orders - week_orders) / day_orders * 100)
year_orders_percentage = ((day_orders - year_orders) / day_orders * 100)
print(f'Yesterday {day_orders}')
print(f'Week Orders {week_orders}')
print(f'Year Orders {year_orders}')
print(f'vs Last Week {week_orders} ({week_orders_percentage:.2f}%)')
print(f'vs Last Year {year_orders} ({year_orders_percentage:.2f}%)')

print(" ")
print("AOV")
print(f'Yesterday £{aov_day:.2f}')
print(f'vs Last Week £{aov_week:.2f}, ({week_aov_percentage:.2f}%)')
print(f'vs Last Year £{aov_year:.2f}, ({year_aov_percentage:.2f}%)')
print(" ")


print("Sessions")
print(f'Yesterday {day_sessions}')
print(f'Last Week {week_sessions} ({week_sessions_percentage:.2f}%)')
print(f'Last Year {year_sessions} ({year_sessions_percentage:.2f}%)')
print(" ")

print("Conversion Rate")
print(f'Yesterday {day_conversion_rate:.2f}%')
print(f'Last Week {week_conversion_rate:.2f}%, ({week_conversion_rate_percentage:.2f}%)')
print(f'Last Year {year_conversion_rate:.2f}%, ({year_conversion_rate_percentage:.2f}%)')
print(" ")

print("Ad Spend")
print(f'Yesterday £{day_ad_spend:.2f}')
print(f'Last Week £{week_ad_spend:.2f}, ({week_ad_spend_percentage:.2f}%)')
print(f'Last Year £{year_ad_spend:.2f}, ({year_ad_spend_percentage:.2f}%)')
print(" ")

print("Cost of Sale (COS)")
print(f'Yesterday {day_cos:.2f}%')
print(f'Last Week {week_cos:.2f}%, ({week_cos_percentage:.2f}%)')
print(f'Last Year {year_cos:.2f}%, ({year_cos_percentage:.2f}%)')
print(" ")

print("Gross Profit Post Ad Spend")
print(f'Yesterday £{day_gp_post_ad:.2f}')
print(f'Last Week £{week_gp_post_ad:.2f}, ({week_gp_post_ad_percentage:.2f}%)')
print(f'Last Year £{year_gp_post_ad:.2f}, ({year_gp_post_ad_percentage:.2f}%)')
print(" ")

print("Gross Profit Post Ad Spend Percentage")
print(f'Yesterday {day_gp_post_ad_percentage:.2f}%')
print(f'Last Week {week_gp_post_ad_percentage:.2f}%, ({week_gp_post_ad_percentage_increase:.2f}%)')
print(f'Last Year {year_gp_post_ad_percentage:.2f}%, ({year_gp_post_ad_percentage_increase:.2f}%)')
print(" ")

print("Contribution Pre Marketing")
print(f'Yesterday £{day_contribution_pre_marketing:.2f}')
print(f'Last Week £{week_contribution_pre_marketing:.2f}, ({week_contribution_pre_marketing_percentage:.2f}%)')
print(f'Last Year £{year_contribution_pre_marketing:.2f}, ({year_contribution_pre_marketing_percentage:.2f}%)')
print(" ")

print("Contribution Post Marketing")
print(f'Yesterday £{day_contribution_post_marketing:.2f}')
print(f'Last Week £{week_contribution_post_marketing:.2f}, ({week_contribution_post_marketing_percentage:.2f}%)')
print(f'Last Year £{year_contribution_post_marketing:.2f}, ({year_contribution_post_marketing_percentage:.2f}%)')
print(" ")

print("Cost per Session")
print(f'Yesterday £{cost_per_session_day:.2f}')
print(f'Last Week £{cost_per_session_week:.2f}, ({week_cost_per_session_percentage:.2f}%)')
print(f'Last Year £{cost_per_session_year:.2f}, ({year_cost_per_session_percentage:.2f}%)')
print(" ")

print("Revenue per Session")
print(f'Yesterday £{rev_per_session_day:.2f}')
print(f'Last Week £{rev_per_session_week:.2f}, ({week_rev_per_session_percentage:.2f}%)')
print(f'Last Year £{rev_per_session_year:.2f}, ({year_rev_per_session_percentage:.2f}%)')
print(" ")

# Customer Net Revenue
print("New Customer Net Revenue")
print(f'Yesterday £{new_cust_revenue_day:.2f}')
print(f'Last Week £{new_cust_revenue_week:.2f}, ({week_new_cust_revenue_percentage:.2f}%)')
print(f'Last Year £{new_cust_revenue_year:.2f}, ({year_new_cust_revenue_percentage:.2f}%)')
print(" ")

print("Returning Customer Net Revenue")
print(f'Yesterday £{ret_cust_revenue_day:.2f}')
print(f'Last Week £{ret_cust_revenue_week:.2f}, ({week_ret_cust_revenue_percentage:.2f}%)')
print(f'Last Year £{ret_cust_revenue_year:.2f}, ({year_ret_cust_revenue_percentage:.2f}%)')
print(" ")

print("Returning Customer Orders")
print(f'Yesterday {ret_cust_orders_day:.2f}')
print(f'Last Week {ret_cust_orders_week:.2f}, ({week_ret_cust_orders_percentage:.2f}%)')
print(f'Last Year {ret_cust_orders_year:.2f}, ({year_ret_cust_orders_percentage:.2f}%)')
print(" ")

print("New Customer AOV")
print(f'Yesterday £{new_cust_aov_day:.2f}')
print(f'Last Week £{new_cust_aov_week:.2f}, ({week_new_cust_aov_percentage:.2f}%)')
print(f'Last Year £{new_cust_aov_year:.2f}, ({year_new_cust_aov_percentage:.2f}%)')
print(" ")

print("Returning Customer AOV")
print(f'Yesterday £{ret_cust_aov_day:.2f}')
print(f'Last Week £{ret_cust_aov_week:.2f}, ({week_ret_cust_aov_percentage:.2f}%)')
print(f'Last Year £{ret_cust_aov_year:.2f}, ({year_ret_cust_aov_percentage:.2f}%)')


print(" ")
print(" ")
print("KPIs Week To Date Total ")
print("==============================================================================")
print("Week to date")


start_of_current_week = today_date - timedelta(days=today_date.weekday())
start_of_previous_week = start_of_current_week - timedelta(days=7)
start_of_same_day_last_year = start_of_current_week - timedelta(days=365)
#third kpi

current_week_data = df_cleaned[df_cleaned['date'].between(start_of_current_week, today_date)]
previous_week_data = df_cleaned[df_cleaned['date'].between(start_of_previous_week, today_date - timedelta(days=7))]
same_period_last_year_data = df_cleaned[df_cleaned['date'].between(start_of_same_day_last_year,
                                                                   today_date - timedelta(days=365))]


def aggregate_data(data):
    net_revenue = data['net_revenue'].sum()
    gp = data['GP'].sum()
    orders = data['orders'].sum()
    sessions = data['sessions_visitors'].sum()
    ad_spend = (
            data['Meta_spend'].sum() +
            data['Google_Spend'].sum() +
            data['Microsoft_Spend'].sum() +
            data['TikTok_Shop_Spend'].sum() +
            data['TikTok_DTC_Spend'].sum()
    )
    conversion_rate = ((orders / sessions) * 100)
    gp_percent = ((gp / net_revenue ) * 100)
    new_customer_net_revenue = data['new_customer_revenue'].sum() if 'new_customer_revenue' in data.columns else 0
    returning_customer_net_revenue = data[
        'returning_customer_revenue'].sum() if 'returning_customer_revenue' in data.columns else 0
    returning_customer_orders = data[
        'returning_customer_orders'].sum() if 'returning_customer_orders' in data.columns else 0
    new_customer_orders = data['new_customer_orders'].sum() if 'new_customer_orders' in data.columns else 0
    cost_of_sales = net_revenue - gp
    gp_post_ad_spend = gp - ad_spend
    contribution_pre_marketing = gp
    contribution_post_marketing = gp_post_ad_spend

    return {
        'revenue': net_revenue,
        'gp': gp,
        'gp_percent': gp_percent,
        'orders': orders,
        'sessions': sessions,
        'ad_spend': ad_spend,
        'aov': (net_revenue / orders) if orders > 0 else 0,
        'conversion_rate': conversion_rate,
        'new_customer_net_revenue': new_customer_net_revenue,
        'returning_customer_net_revenue': returning_customer_net_revenue,
        'returning_customer_orders': returning_customer_orders,
        'new_customer_orders': new_customer_orders,
        'cost_of_sales': cost_of_sales,
        'gp_post_ad_spend': gp_post_ad_spend,
        'gp_post_ad_spend_percentage': (gp_post_ad_spend / net_revenue) if net_revenue > 0 else 0,
        'contribution_pre_marketing': contribution_pre_marketing,
        'contribution_post_marketing': contribution_post_marketing,
        'cost_per_session': (ad_spend / sessions) if sessions > 0 else 0,
        'revenue_per_session': (net_revenue / sessions) if sessions > 0 else 0,
        'new_customer_aov': (new_customer_net_revenue / new_customer_orders) if new_customer_orders > 0 else 0,
        'returning_customer_aov': (
                    returning_customer_net_revenue / returning_customer_orders) if returning_customer_orders > 0 else 0,
    }


current_week_aggregates = aggregate_data(current_week_data)
previous_week_aggregates = aggregate_data(previous_week_data)
same_period_last_year_aggregates = aggregate_data(same_period_last_year_data)



def calculate_change(current, previous):
    return ((current - previous) / current) * 100 if previous != 0 else 0


week_to_date_revenue_change = calculate_change(current_week_aggregates['revenue'], previous_week_aggregates['revenue'])
week_to_date_gp_change = calculate_change(current_week_aggregates['gp'], previous_week_aggregates['gp'])
week_to_date_gp_percent_change = calculate_change(current_week_aggregates['gp_percent'], previous_week_aggregates['gp_percent'])
week_to_date_orders_change = calculate_change(current_week_aggregates['orders'], previous_week_aggregates['orders'])
week_to_date_sessions_change = calculate_change(current_week_aggregates['sessions'], previous_week_aggregates['sessions'])
week_to_date_ad_spend_change = calculate_change(current_week_aggregates['ad_spend'], previous_week_aggregates['ad_spend'])
week_to_date_aov_change = calculate_change(current_week_aggregates['aov'], previous_week_aggregates['aov'])
week_to_date_conversion_rate_change = calculate_change(current_week_aggregates['conversion_rate'], previous_week_aggregates['conversion_rate'])
week_to_date_new_customer_net_revenue_change = calculate_change(current_week_aggregates['new_customer_net_revenue'], previous_week_aggregates['new_customer_net_revenue'])
week_to_date_returning_customer_net_revenue_change = calculate_change(current_week_aggregates['returning_customer_net_revenue'], previous_week_aggregates['returning_customer_net_revenue'])
week_to_date_returning_customer_orders_change = calculate_change(current_week_aggregates['returning_customer_orders'], previous_week_aggregates['returning_customer_orders'])
week_to_date_new_customer_orders_change = calculate_change(current_week_aggregates['new_customer_orders'], previous_week_aggregates['new_customer_orders'])
week_to_date_cost_of_sales_change = calculate_change(current_week_aggregates['cost_of_sales'], previous_week_aggregates['cost_of_sales'])
week_to_date_gp_post_ad_spend_change = calculate_change(current_week_aggregates['gp_post_ad_spend'], previous_week_aggregates['gp_post_ad_spend'])
week_to_date_gp_post_ad_spend_percentage_change = calculate_change(current_week_aggregates['gp_post_ad_spend_percentage'], previous_week_aggregates['gp_post_ad_spend_percentage'])
week_to_date_contribution_pre_marketing_change = calculate_change(current_week_aggregates['contribution_pre_marketing'], previous_week_aggregates['contribution_pre_marketing'])
week_to_date_contribution_post_marketing_change = calculate_change(current_week_aggregates['contribution_post_marketing'], previous_week_aggregates['contribution_post_marketing'])
week_to_date_cost_per_session_change = calculate_change(current_week_aggregates['cost_per_session'], previous_week_aggregates['cost_per_session'])
week_to_date_revenue_per_session_change = calculate_change(current_week_aggregates['revenue_per_session'], previous_week_aggregates['revenue_per_session'])
week_to_date_new_customer_aov_change = calculate_change(current_week_aggregates['new_customer_aov'], previous_week_aggregates['new_customer_aov'])
week_to_date_returning_customer_aov_change = calculate_change(current_week_aggregates['returning_customer_aov'], previous_week_aggregates['returning_customer_aov'])



week_to_date_revenue_change_vs_last_year = calculate_change(current_week_aggregates['revenue'], same_period_last_year_aggregates['revenue'])
week_to_date_gp_change_vs_last_year = calculate_change(current_week_aggregates['gp'], same_period_last_year_aggregates['gp'])
week_to_date_gp_percent_change_vs_last_year = calculate_change(current_week_aggregates['gp_percent'], same_period_last_year_aggregates['gp_percent'])
week_to_date_orders_change_vs_last_year = calculate_change(current_week_aggregates['orders'], same_period_last_year_aggregates['orders'])
week_to_date_sessions_change_vs_last_year = calculate_change(current_week_aggregates['sessions'], same_period_last_year_aggregates['sessions'])
week_to_date_ad_spend_change_vs_last_year = calculate_change(current_week_aggregates['ad_spend'], same_period_last_year_aggregates['ad_spend'])
week_to_date_aov_change_vs_last_year = calculate_change(current_week_aggregates['aov'], same_period_last_year_aggregates['aov'])
week_to_date_conversion_rate_change_vs_last_year = calculate_change(current_week_aggregates['conversion_rate'], same_period_last_year_aggregates['conversion_rate'])
week_to_date_new_customer_net_revenue_change_vs_last_year = calculate_change(current_week_aggregates['new_customer_net_revenue'], same_period_last_year_aggregates['new_customer_net_revenue'])
week_to_date_returning_customer_net_revenue_change_vs_last_year = calculate_change(current_week_aggregates['returning_customer_net_revenue'], same_period_last_year_aggregates['returning_customer_net_revenue'])
week_to_date_returning_customer_orders_change_vs_last_year = calculate_change(current_week_aggregates['returning_customer_orders'], same_period_last_year_aggregates['returning_customer_orders'])
week_to_date_new_customer_orders_change_vs_last_year = calculate_change(current_week_aggregates['new_customer_orders'], same_period_last_year_aggregates['new_customer_orders'])
week_to_date_cost_of_sales_change_vs_last_year = calculate_change(current_week_aggregates['cost_of_sales'], same_period_last_year_aggregates['cost_of_sales'])
week_to_date_gp_post_ad_spend_change_vs_last_year = calculate_change(current_week_aggregates['gp_post_ad_spend'], same_period_last_year_aggregates['gp_post_ad_spend'])
week_to_date_gp_post_ad_spend_percentage_change_vs_last_year = calculate_change(current_week_aggregates['gp_post_ad_spend_percentage'], same_period_last_year_aggregates['gp_post_ad_spend_percentage'])
week_to_date_contribution_pre_marketing_change_vs_last_year = calculate_change(current_week_aggregates['contribution_pre_marketing'], same_period_last_year_aggregates['contribution_pre_marketing'])
week_to_date_contribution_post_marketing_change_vs_last_year = calculate_change(current_week_aggregates['contribution_post_marketing'], same_period_last_year_aggregates['contribution_post_marketing'])
week_to_date_cost_per_session_change_vs_last_year = calculate_change(current_week_aggregates['cost_per_session'], same_period_last_year_aggregates['cost_per_session'])
week_to_date_revenue_per_session_change_vs_last_year = calculate_change(current_week_aggregates['revenue_per_session'], same_period_last_year_aggregates['revenue_per_session'])
week_to_date_new_customer_aov_change_vs_last_year = calculate_change(current_week_aggregates['new_customer_aov'], same_period_last_year_aggregates['new_customer_aov'])
week_to_date_returning_customer_aov_change_vs_last_year = calculate_change(current_week_aggregates['returning_customer_aov'], same_period_last_year_aggregates['returning_customer_aov'])

print("\nWeek to Date Totals for Current Week:")
print(f'Revenue: ${current_week_aggregates["revenue"]:.2f} ')
print(f'Revenue vs Last Week: ${previous_week_aggregates["revenue"]:.2f} ({week_to_date_revenue_change:.2f}%)')
print(f'Revenue vs Last Year: ${same_period_last_year_aggregates["revenue"]:.2f} ({week_to_date_revenue_change_vs_last_year:.2f}%)\n')

print(f'Gross Profit: ${current_week_aggregates["gp"]:.2f}')
print(f'Gross Profit vs Last Week: ${previous_week_aggregates["gp"]:.2f} ({week_to_date_gp_change:.2f}%)')
print(f'Gross Profit vs Last Year: ${same_period_last_year_aggregates["gp"]:.2f} ({week_to_date_gp_change_vs_last_year:.2f}%)\n')

print(f'Orders: {current_week_aggregates["orders"]}')
print(f'Orders vs Last Week: {previous_week_aggregates["orders"]} ({week_to_date_orders_change:.2f}%)')
print(f'Orders vs Last Year: {same_period_last_year_aggregates["orders"]} ({week_to_date_orders_change_vs_last_year:.2f}%)\n')

print(f'Sessions: {current_week_aggregates["sessions"]}')
print(f'Sessions vs Last Week: {previous_week_aggregates["sessions"]} ({week_to_date_sessions_change:.2f}%)')
print(f'Sessions vs Last Year: {same_period_last_year_aggregates["sessions"]} ({week_to_date_sessions_change_vs_last_year:.2f}%)\n')

print(f'Ad Spend: ${current_week_aggregates["ad_spend"]:.2f}')
print(f'Ad Spend vs Last Week: ${previous_week_aggregates["ad_spend"]:.2f} ({week_to_date_ad_spend_change:.2f}%)')
print(f'Ad Spend vs Last Year: ${same_period_last_year_aggregates["ad_spend"]:.2f} ({week_to_date_ad_spend_change_vs_last_year:.2f}%)\n')

print(f'Average order value: ${current_week_aggregates["aov"]:.2f}')
print(f'Average order value vs Last Week: ${previous_week_aggregates["aov"]:.2f} ({week_to_date_aov_change:.2f}%)')
print(f'Average order value vs Last Year: ${same_period_last_year_aggregates["aov"]:.2f} ({week_to_date_aov_change_vs_last_year:.2f}%)\n')

print(f'Conversion rate: {current_week_aggregates["conversion_rate"]:.2f}%')
print(f'Conversion rate vs Last Week: {previous_week_aggregates["conversion_rate"]:.2f}% ({week_to_date_conversion_rate_change:.2f}%)')
print(f'Conversion rate vs Last Year: {same_period_last_year_aggregates["conversion_rate"]:.2f}% ({week_to_date_conversion_rate_change_vs_last_year:.2f}%)\n')

print(f'New customer net revenue: ${current_week_aggregates["new_customer_net_revenue"]:.2f}')
print(f'New customer net revenue vs Last Week: ${previous_week_aggregates["new_customer_net_revenue"]:.2f} ({week_to_date_new_customer_net_revenue_change:.2f}%)')
print(f'New customer net revenue vs Last Year: ${same_period_last_year_aggregates["new_customer_net_revenue"]:.2f} ({week_to_date_new_customer_net_revenue_change_vs_last_year:.2f}%)\n')

print(f'Returning customer net revenue: ${current_week_aggregates["returning_customer_net_revenue"]:.2f}')
print(f'Returning customer net revenue vs Last Week: ${previous_week_aggregates["returning_customer_net_revenue"]:.2f} ({week_to_date_returning_customer_net_revenue_change:.2f}%)')
print(f'Returning customer net revenue vs Last Year: ${same_period_last_year_aggregates["returning_customer_net_revenue"]:.2f} ({week_to_date_returning_customer_net_revenue_change_vs_last_year:.2f}%)\n')

print(f'Returning customer orders: {current_week_aggregates["returning_customer_orders"]}')
print(f'Returning customer orders vs Last Week: {previous_week_aggregates["returning_customer_orders"]} ({week_to_date_returning_customer_orders_change:.2f}%)')
print(f'Returning customer orders vs Last Year: {same_period_last_year_aggregates["returning_customer_orders"]} ({week_to_date_returning_customer_orders_change_vs_last_year:.2f}%)\n')

print(f'New customer orders: {current_week_aggregates["new_customer_orders"]}')
print(f'New customer orders vs Last Week: {previous_week_aggregates["new_customer_orders"]} ({week_to_date_new_customer_orders_change:.2f}%)')
print(f'New customer orders vs Last Year: {same_period_last_year_aggregates["new_customer_orders"]} ({week_to_date_new_customer_orders_change_vs_last_year:.2f}%)\n')

print(f'Cost of sales: ${current_week_aggregates["cost_of_sales"]:.2f}')
print(f'Cost of sales vs Last Week: ${previous_week_aggregates["cost_of_sales"]:.2f} ({week_to_date_cost_of_sales_change:.2f}%)')
print(f'Cost of sales vs Last Year: ${same_period_last_year_aggregates["cost_of_sales"]:.2f} ({week_to_date_cost_of_sales_change_vs_last_year:.2f}%)\n')

print(f'GP post ad spend: ${current_week_aggregates["gp_post_ad_spend"]:.2f}')
print(f'GP post ad spend vs Last Week: ${previous_week_aggregates["gp_post_ad_spend"]:.2f} ({week_to_date_gp_post_ad_spend_change:.2f}%)')
print(f'GP post ad spend vs Last Year: ${same_period_last_year_aggregates["gp_post_ad_spend"]:.2f} ({week_to_date_gp_post_ad_spend_change_vs_last_year:.2f}%)\n')

print(f'GP post ad spend percentage: {current_week_aggregates["gp_post_ad_spend_percentage"]:.2f}%')
print(f'GP post ad spend percentage vs Last Week: {previous_week_aggregates["gp_post_ad_spend_percentage"]:.2f}% ({week_to_date_gp_post_ad_spend_percentage_change:.2f}%)')
print(f'GP post ad spend percentage vs Last Year: {same_period_last_year_aggregates["gp_post_ad_spend_percentage"]:.2f}% ({week_to_date_gp_post_ad_spend_percentage_change_vs_last_year:.2f}%)\n')

print(f'Contribution pre marketing: ${current_week_aggregates["contribution_pre_marketing"]:.2f}')
print(f'Contribution pre marketing vs Last Week: ${previous_week_aggregates["contribution_pre_marketing"]:.2f} ({week_to_date_contribution_pre_marketing_change:.2f}%)')
print(f'Contribution pre marketing vs Last Year: ${same_period_last_year_aggregates["contribution_pre_marketing"]:.2f} ({week_to_date_contribution_pre_marketing_change_vs_last_year:.2f}%)\n')

print(f'Contribution post marketing: ${current_week_aggregates["contribution_post_marketing"]:.2f}')
print(f'Contribution post marketing vs Last Week: ${previous_week_aggregates["contribution_post_marketing"]:.2f} ({week_to_date_contribution_post_marketing_change:.2f}%)')
print(f'Contribution post marketing vs Last Year: ${same_period_last_year_aggregates["contribution_post_marketing"]:.2f} ({week_to_date_contribution_post_marketing_change_vs_last_year:.2f}%)\n')

print(f'Cost per session: ${current_week_aggregates["cost_per_session"]:.2f}')
print(f'Cost per session vs Last Week: ${previous_week_aggregates["cost_per_session"]:.2f} ({week_to_date_cost_per_session_change:.2f}%)')
print(f'Cost per session vs Last Year: ${same_period_last_year_aggregates["cost_per_session"]:.2f} ({week_to_date_cost_per_session_change_vs_last_year:.2f}%)\n')

print(f'Revenue per session: ${current_week_aggregates["revenue_per_session"]:.2f}')
print(f'Revenue per session vs Last Week: ${previous_week_aggregates["revenue_per_session"]:.2f} ({week_to_date_revenue_per_session_change:.2f}%)')
print(f'Revenue per session vs Last Year: ${same_period_last_year_aggregates["revenue_per_session"]:.2f} ({week_to_date_revenue_per_session_change_vs_last_year:.2f}%)\n')

print(f'New customer AOV: ${current_week_aggregates["new_customer_aov"]:.2f}')
print(f'New customer AOV vs Last Week: ${previous_week_aggregates["new_customer_aov"]:.2f} ({week_to_date_new_customer_aov_change:.2f}%)')
print(f'New customer AOV vs Last Year: ${same_period_last_year_aggregates["new_customer_aov"]:.2f} ({week_to_date_new_customer_aov_change_vs_last_year:.2f}%)\n')

print(f'Returning customer AOV: ${current_week_aggregates["returning_customer_aov"]:.2f}')
print(f'Returning customer AOV vs Last Week: ${previous_week_aggregates["returning_customer_aov"]:.2f} ({week_to_date_returning_customer_aov_change:.2f}%)')
print(f'Returning customer AOV vs Last Year: ${same_period_last_year_aggregates["returning_customer_aov"]:.2f} ({week_to_date_returning_customer_aov_change_vs_last_year:.2f}%)\n')

start_of_current_month = today_date.replace(day=1)
start_of_previous_month = start_of_current_month - timedelta(days=30)
start_of_same_month_last_year = start_of_current_month - timedelta(days=365)

current_month_data = df_cleaned[df_cleaned['date'].between(start_of_current_month, today_date)]
previous_month_data = df_cleaned[df_cleaned['date'].between(start_of_previous_month, today_date - timedelta(days=30))]
same_period_month_year_data = df_cleaned[df_cleaned['date'].between(start_of_same_month_last_year,
                                                                   today_date - timedelta(days=365))]


current_month_aggregates = aggregate_data(current_month_data)
previous_month_aggregates = aggregate_data(previous_month_data)
same_month_last_year_aggregates = aggregate_data(same_period_month_year_data)

month_to_date_revenue_change = calculate_change(current_month_aggregates['revenue'], previous_month_aggregates['revenue'])
month_to_date_gp_change = calculate_change(current_month_aggregates['gp'], previous_month_aggregates['gp'])
month_to_date_gp_percent_change = calculate_change(current_month_aggregates['gp_percent'], previous_month_aggregates['gp_percent'])
month_to_date_orders_change = calculate_change(current_month_aggregates['orders'], previous_month_aggregates['orders'])
month_to_date_sessions_change = calculate_change(current_month_aggregates['sessions'], previous_month_aggregates['sessions'])
month_to_date_ad_spend_change = calculate_change(current_month_aggregates['ad_spend'], previous_month_aggregates['ad_spend'])
month_to_date_aov_change = calculate_change(current_month_aggregates['aov'], previous_month_aggregates['aov'])
month_to_date_conversion_rate_change = calculate_change(current_month_aggregates['conversion_rate'], previous_month_aggregates['conversion_rate'])
month_to_date_new_customer_net_revenue_change = calculate_change(current_month_aggregates['new_customer_net_revenue'], previous_month_aggregates['new_customer_net_revenue'])
month_to_date_returning_customer_net_revenue_change = calculate_change(current_month_aggregates['returning_customer_net_revenue'], previous_month_aggregates['returning_customer_net_revenue'])
month_to_date_returning_customer_orders_change = calculate_change(current_month_aggregates['returning_customer_orders'], previous_month_aggregates['returning_customer_orders'])
month_to_date_new_customer_orders_change = calculate_change(current_month_aggregates['new_customer_orders'], previous_month_aggregates['new_customer_orders'])
month_to_date_cost_of_sales_change = calculate_change(current_month_aggregates['cost_of_sales'], previous_month_aggregates['cost_of_sales'])
month_to_date_gp_post_ad_spend_change = calculate_change(current_month_aggregates['gp_post_ad_spend'], previous_month_aggregates['gp_post_ad_spend'])
month_to_date_gp_post_ad_spend_percentage_change = calculate_change(current_month_aggregates['gp_post_ad_spend_percentage'], previous_month_aggregates['gp_post_ad_spend_percentage'])
month_to_date_contribution_pre_marketing_change = calculate_change(current_month_aggregates['contribution_pre_marketing'], previous_month_aggregates['contribution_pre_marketing'])
month_to_date_contribution_post_marketing_change = calculate_change(current_month_aggregates['contribution_post_marketing'], previous_month_aggregates['contribution_post_marketing'])
month_to_date_cost_per_session_change = calculate_change(current_month_aggregates['cost_per_session'], previous_month_aggregates['cost_per_session'])
month_to_date_revenue_per_session_change = calculate_change(current_month_aggregates['revenue_per_session'], previous_month_aggregates['revenue_per_session'])
month_to_date_new_customer_aov_change = calculate_change(current_month_aggregates['new_customer_aov'], previous_month_aggregates['new_customer_aov'])
month_to_date_returning_customer_aov_change = calculate_change(current_month_aggregates['returning_customer_aov'], previous_month_aggregates['returning_customer_aov'])

month_to_date_revenue_change_vs_last_year = calculate_change(current_month_aggregates['revenue'], same_month_last_year_aggregates['revenue'])
month_to_date_gp_change_vs_last_year = calculate_change(current_month_aggregates['gp'], same_month_last_year_aggregates['gp'])
month_to_date_gp_percent_change_vs_last_year = calculate_change(current_month_aggregates['gp_percent'], same_month_last_year_aggregates['gp_percent'])
month_to_date_orders_change_vs_last_year = calculate_change(current_month_aggregates['orders'], same_month_last_year_aggregates['orders'])
month_to_date_sessions_change_vs_last_year = calculate_change(current_month_aggregates['sessions'], same_month_last_year_aggregates['sessions'])
month_to_date_ad_spend_change_vs_last_year = calculate_change(current_month_aggregates['ad_spend'], same_month_last_year_aggregates['ad_spend'])
month_to_date_aov_change_vs_last_year = calculate_change(current_month_aggregates['aov'], same_month_last_year_aggregates['aov'])
month_to_date_conversion_rate_change_vs_last_year = calculate_change(current_month_aggregates['conversion_rate'], same_month_last_year_aggregates['conversion_rate'])
month_to_date_new_customer_net_revenue_change_vs_last_year = calculate_change(current_month_aggregates['new_customer_net_revenue'], same_month_last_year_aggregates['new_customer_net_revenue'])
month_to_date_returning_customer_net_revenue_change_vs_last_year = calculate_change(current_month_aggregates['returning_customer_net_revenue'], same_month_last_year_aggregates['returning_customer_net_revenue'])
month_to_date_returning_customer_orders_change_vs_last_year = calculate_change(current_month_aggregates['returning_customer_orders'], same_month_last_year_aggregates['returning_customer_orders'])
month_to_date_new_customer_orders_change_vs_last_year = calculate_change(current_month_aggregates['new_customer_orders'], same_month_last_year_aggregates['new_customer_orders'])
month_to_date_cost_of_sales_change_vs_last_year = calculate_change(current_month_aggregates['cost_of_sales'], same_month_last_year_aggregates['cost_of_sales'])
month_to_date_gp_post_ad_spend_change_vs_last_year = calculate_change(current_month_aggregates['gp_post_ad_spend'], same_month_last_year_aggregates['gp_post_ad_spend'])
month_to_date_gp_post_ad_spend_percentage_change_vs_last_year = calculate_change(current_month_aggregates['gp_post_ad_spend_percentage'], same_month_last_year_aggregates['gp_post_ad_spend_percentage'])
month_to_date_contribution_pre_marketing_change_vs_last_year = calculate_change(current_month_aggregates['contribution_pre_marketing'], same_month_last_year_aggregates['contribution_pre_marketing'])
month_to_date_contribution_post_marketing_change_vs_last_year = calculate_change(current_month_aggregates['contribution_post_marketing'], same_month_last_year_aggregates['contribution_post_marketing'])
month_to_date_cost_per_session_change_vs_last_year = calculate_change(current_month_aggregates['cost_per_session'], same_month_last_year_aggregates['cost_per_session'])
month_to_date_revenue_per_session_change_vs_last_year = calculate_change(current_month_aggregates['revenue_per_session'], same_month_last_year_aggregates['revenue_per_session'])
month_to_date_new_customer_aov_change_vs_last_year = calculate_change(current_month_aggregates['new_customer_aov'], same_month_last_year_aggregates['new_customer_aov'])
month_to_date_returning_customer_aov_change_vs_last_year = calculate_change(current_month_aggregates['returning_customer_aov'], same_month_last_year_aggregates['returning_customer_aov'])

print("KPIs Month To Date Total")
print("\nMonth to Date Totals for Current Month:")
print(f'Revenue: ${current_month_aggregates["revenue"]:.2f}')
print(f'Revenue vs Last Month: ${previous_month_aggregates["revenue"]:.2f} ({month_to_date_revenue_change:.2f}%)')
print(f'Revenue vs Last Year: ${same_month_last_year_aggregates["revenue"]:.2f} ({month_to_date_revenue_change_vs_last_year:.2f}%)\n')

print(f'Gross Profit: ${current_month_aggregates["gp"]:.2f}')
print(f'Gross Profit vs Last Month: ${previous_month_aggregates["gp"]:.2f} ({month_to_date_gp_change:.2f}%)')
print(f'Gross Profit vs Last Year: ${same_month_last_year_aggregates["gp"]:.2f} ({month_to_date_gp_change_vs_last_year:.2f}%)\n')

print(f'Orders: {current_month_aggregates["orders"]}')
print(f'Orders vs Last Month: {previous_month_aggregates["orders"]} ({month_to_date_orders_change:.2f}%)')
print(f'Orders vs Last Year: {same_month_last_year_aggregates["orders"]} ({month_to_date_orders_change_vs_last_year:.2f}%)\n')

print(f'Sessions: {current_month_aggregates["sessions"]}')
print(f'Sessions vs Last Month: {previous_month_aggregates["sessions"]} ({month_to_date_sessions_change:.2f}%)')
print(f'Sessions vs Last Year: {same_month_last_year_aggregates["sessions"]} ({month_to_date_sessions_change_vs_last_year:.2f}%)\n')

print(f'Ad Spend: ${current_month_aggregates["ad_spend"]:.2f}')
print(f'Ad Spend vs Last Month: ${previous_month_aggregates["ad_spend"]:.2f} ({month_to_date_ad_spend_change:.2f}%)')
print(f'Ad Spend vs Last Year: ${same_month_last_year_aggregates["ad_spend"]:.2f} ({month_to_date_ad_spend_change_vs_last_year:.2f}%)\n')

print(f'Average order value: ${current_month_aggregates["aov"]:.2f}')
print(f'Average order value vs Last Month: ${previous_month_aggregates["aov"]:.2f} ({month_to_date_aov_change:.2f}%)')
print(f'Average order value vs Last Year: ${same_month_last_year_aggregates["aov"]:.2f} ({month_to_date_aov_change_vs_last_year:.2f}%)\n')

print(f'Conversion rate: {current_month_aggregates["conversion_rate"]:.2f}%')
print(f'Conversion rate vs Last Month: {previous_month_aggregates["conversion_rate"]:.2f}% ({month_to_date_conversion_rate_change:.2f}%)')
print(f'Conversion rate vs Last Year: {same_month_last_year_aggregates["conversion_rate"]:.2f}% ({month_to_date_conversion_rate_change_vs_last_year:.2f}%)\n')

print(f'New customer net revenue: ${current_month_aggregates["new_customer_net_revenue"]:.2f}')
print(f'New customer net revenue vs Last Month: ${previous_month_aggregates["new_customer_net_revenue"]:.2f} ({month_to_date_new_customer_net_revenue_change:.2f}%)')
print(f'New customer net revenue vs Last Year: ${same_month_last_year_aggregates["new_customer_net_revenue"]:.2f} ({month_to_date_new_customer_net_revenue_change_vs_last_year:.2f}%)\n')

print(f'Returning customer net revenue: ${current_month_aggregates["returning_customer_net_revenue"]:.2f}')
print(f'Returning customer net revenue vs Last Month: ${previous_month_aggregates["returning_customer_net_revenue"]:.2f} ({month_to_date_returning_customer_net_revenue_change:.2f}%)')
print(f'Returning customer net revenue vs Last Year: ${same_month_last_year_aggregates["returning_customer_net_revenue"]:.2f} ({month_to_date_returning_customer_net_revenue_change_vs_last_year:.2f}%)\n')

print(f'Returning customer orders: {current_month_aggregates["returning_customer_orders"]}')
print(f'Returning customer orders vs Last Month: {previous_month_aggregates["returning_customer_orders"]} ({month_to_date_returning_customer_orders_change:.2f}%)')
print(f'Returning customer orders vs Last Year: {same_month_last_year_aggregates["returning_customer_orders"]} ({month_to_date_returning_customer_orders_change_vs_last_year:.2f}%)\n')

print(f'New customer orders: {current_month_aggregates["new_customer_orders"]}')
print(f'New customer orders vs Last Month: {previous_month_aggregates["new_customer_orders"]} ({month_to_date_new_customer_orders_change:.2f}%)')
print(f'New customer orders vs Last Year: {same_month_last_year_aggregates["new_customer_orders"]} ({month_to_date_new_customer_orders_change_vs_last_year:.2f}%)\n')

print(f'Cost of sales: ${current_month_aggregates["cost_of_sales"]:.2f}')
print(f'Cost of sales vs Last Month: ${previous_month_aggregates["cost_of_sales"]:.2f} ({month_to_date_cost_of_sales_change:.2f}%)')
print(f'Cost of sales vs Last Year: ${same_month_last_year_aggregates["cost_of_sales"]:.2f} ({month_to_date_cost_of_sales_change_vs_last_year:.2f}%)\n')

print(f'GP post ad spend: ${current_month_aggregates["gp_post_ad_spend"]:.2f}')
print(f'GP post ad spend vs Last Month: ${previous_month_aggregates["gp_post_ad_spend"]:.2f} ({month_to_date_gp_post_ad_spend_change:.2f}%)')
print(f'GP post ad spend vs Last Year: ${same_month_last_year_aggregates["gp_post_ad_spend"]:.2f} ({month_to_date_gp_post_ad_spend_change_vs_last_year:.2f}%)\n')

print(f'GP post ad spend percentage: {current_month_aggregates["gp_post_ad_spend_percentage"]:.2f}%')
print(f'GP post ad spend percentage vs Last Month: {previous_month_aggregates["gp_post_ad_spend_percentage"]:.2f}% ({month_to_date_gp_post_ad_spend_percentage_change:.2f}%)')
print(f'GP post ad spend percentage vs Last Year: {same_month_last_year_aggregates["gp_post_ad_spend_percentage"]:.2f}% ({month_to_date_gp_post_ad_spend_percentage_change_vs_last_year:.2f}%)\n')

print(f'Contribution pre marketing: ${current_month_aggregates["contribution_pre_marketing"]:.2f}')
print(f'Contribution pre marketing vs Last Month: ${previous_month_aggregates["contribution_pre_marketing"]:.2f} ({month_to_date_contribution_pre_marketing_change:.2f}%)')
print(f'Contribution pre marketing vs Last Year: ${same_month_last_year_aggregates["contribution_pre_marketing"]:.2f} ({month_to_date_contribution_pre_marketing_change_vs_last_year:.2f}%)\n')

print(f'Contribution post marketing: ${current_month_aggregates["contribution_post_marketing"]:.2f}')
print(f'Contribution post marketing vs Last Month: ${previous_month_aggregates["contribution_post_marketing"]:.2f} ({month_to_date_contribution_post_marketing_change:.2f}%)')
print(f'Contribution post marketing vs Last Year: ${same_month_last_year_aggregates["contribution_post_marketing"]:.2f} ({month_to_date_contribution_post_marketing_change_vs_last_year:.2f}%)\n')

print(f'Cost per session: ${current_month_aggregates["cost_per_session"]:.2f}')
print(f'Cost per session vs Last Month: ${previous_month_aggregates["cost_per_session"]:.2f} ({month_to_date_cost_per_session_change:.2f}%)')
print(f'Cost per session vs Last Year: ${same_month_last_year_aggregates["cost_per_session"]:.2f} ({month_to_date_cost_per_session_change_vs_last_year:.2f}%)\n')

print(f'Revenue per session: ${current_month_aggregates["revenue_per_session"]:.2f}')
print(f'Revenue per session vs Last Month: ${previous_month_aggregates["revenue_per_session"]:.2f} ({month_to_date_revenue_per_session_change:.2f}%)')
print(f'Revenue per session vs Last Year: ${same_month_last_year_aggregates["revenue_per_session"]:.2f} ({month_to_date_revenue_per_session_change_vs_last_year:.2f}%)\n')

print(f'New customer AOV: ${current_month_aggregates["new_customer_aov"]:.2f}')
print(f'New customer AOV vs Last Month: ${previous_month_aggregates["new_customer_aov"]:.2f} ({month_to_date_new_customer_aov_change:.2f}%)')
print(f'New customer AOV vs Last Year: ${same_month_last_year_aggregates["new_customer_aov"]:.2f} ({month_to_date_new_customer_aov_change_vs_last_year:.2f}%)\n')

print(f'Returning customer AOV: ${current_month_aggregates["returning_customer_aov"]:.2f}')
print(f'Returning customer AOV vs Last Month: ${previous_month_aggregates["returning_customer_aov"]:.2f} ({month_to_date_returning_customer_aov_change:.2f}%)')
print(f'Returning customer AOV vs Last Year: ${same_month_last_year_aggregates["returning_customer_aov"]:.2f} ({month_to_date_returning_customer_aov_change_vs_last_year:.2f}%)\n')

data_yesterday = {
    'Net Rev': [
        '£{:.2f}'.format(revenue),
        '£{:.2f}'.format(week_revenue),
        '£{:.2f}'.format(year_revenue),
        '',
        'vs Last Week ({:.2f}%)'.format(week_percentage),
        'vs Last Year ({:.2f}%)'.format(year_percentage)
    ],
    'Gross Profit': [
        '£{:.2f}'.format(day_gp),
        '£{:.2f}'.format(week_gp),
        '£{:.2f}'.format(year_gp),
        '',
        'Last Week ({:.2f}%)'.format(week_percentage_GP),
        'Last Year ({:.2f}%)'.format(year_percentage_GP)
    ],
    'GP%': [
        '{:.2f}%'.format(gp_percentage_day),
        '{:.2f}%'.format(week_percentage_GP),
        '{:.2f}%'.format(year_percentage_GP),
        '',
        'vs last week ({:.2f}%)'.format(gp_percentage_week),
        'vs last year ({:.2f}%)'.format(gp_percentage_year)
    ],
    'No. of Orders': [
        '{:.2f}'.format(day_orders),
        '{:.2f}'.format(week_orders),
        '{:.2f}'.format(year_orders),
        '',
        'vs Last Week ({:.2f}%)'.format(week_orders_percentage),
        'vs Last Year ({:.2f}%)'.format(year_orders_percentage)
    ],
    'AOV': [
        '£{:.2f}'.format(aov_day),
        '£{:.2f}'.format(aov_week),
        '£{:.2f}'.format(aov_year),
        '',
        'vs Last Week ({:.2f}%)'.format(week_aov_percentage),
        'vs Last Year ({:.2f}%)'.format(year_aov_percentage)
    ],
    'Sessions/Visitors': [
        '{:.2f}'.format(day_sessions),
        '{:.2f}'.format(week_sessions),
        '{:.2f}'.format(year_sessions),
        '',
        'Last Week ({:.2f}%)'.format(week_sessions_percentage),
        'Last Year ({:.2f}%)'.format(year_sessions_percentage)
    ],
    'Conversion Rate': [
        '{:.2f}%'.format(day_conversion_rate),
        '{:.2f}%'.format(week_conversion_rate),
        '{:.2f}%'.format(year_conversion_rate),
        '',
        'Last Week ({:.2f}%)'.format(week_conversion_rate_percentage),
        'Last Year ({:.2f}%)'.format(year_conversion_rate_percentage)
    ],
    'Ad Spend': [
        '£{:.2f}'.format(day_ad_spend),
        '£{:.2f}'.format(week_ad_spend),
        '£{:.2f}'.format(year_ad_spend),
        '',
        'Last Week ({:.2f}%)'.format(week_ad_spend_percentage),
        'Last Year ({:.2f}%)'.format(year_ad_spend_percentage)
    ],
    'COS': [
        '£{:.2f}'.format(day_cos),
        '£{:.2f}'.format(week_cos),
        '£{:.2f}'.format(year_cos),
        '',
        'Last Week ({:.2f}%)'.format(week_cos_percentage),
        'Last Year ({:.2f}%)'.format(year_cos_percentage)
    ],
    'GP Post Ad Spend': [
        '£{:.2f}'.format(day_gp_post_ad),
        '£{:.2f}'.format(week_gp_post_ad),
        '£{:.2f}'.format(year_gp_post_ad),
        '',
        'Last Week ({:.2f}%)'.format(week_gp_post_ad_percentage),
        'Last Year ({:.2f}%)'.format(year_gp_post_ad_percentage)
    ],
    'Cont. Pre Mktg': [
        '£{:.2f}'.format(day_contribution_pre_marketing),
        '£{:.2f}'.format(week_contribution_pre_marketing),
        '£{:.2f}'.format(year_contribution_pre_marketing),
        '',
        'Last Week ({:.2f}%)'.format(week_contribution_pre_marketing_percentage),
        'Last Year ({:.2f}%)'.format(year_contribution_pre_marketing_percentage)
    ],
    'Cost/Session': [
        '£{:.2f}'.format(cost_per_session_day),
        '£{:.2f}'.format(cost_per_session_week),
        '£{:.2f}'.format(cost_per_session_year),
        '',
        'Last Week ({:.2f}%)'.format(week_cost_per_session_percentage),
        'Last Year ({:.2f}%)'.format(year_cost_per_session_percentage)
    ],
    'Rev/Session': [
        '£{:.2f}'.format(rev_per_session_day),
        '£{:.2f}'.format(rev_per_session_week),
        '£{:.2f}'.format(rev_per_session_year),
        '',
        'Last Week ({:.2f}%)'.format(week_rev_per_session_percentage),
        'Last Year ({:.2f}%)'.format(year_rev_per_session_percentage)
    ],
    'New Cust Net Rev': [
        '£{:.2f}'.format(new_cust_revenue_day),
        '£{:.2f}'.format(new_cust_revenue_week),
        '£{:.2f}'.format(new_cust_revenue_year),
        '',
        'Last Week ({:.2f}%)'.format(week_new_cust_revenue_percentage),
        'Last Year ({:.2f}%)'.format(year_new_cust_revenue_percentage)
    ],
    'Ret Cust Net Rev': [
        '£{:.2f}'.format(ret_cust_revenue_day),
        '£{:.2f}'.format(ret_cust_revenue_week),
        '£{:.2f}'.format(ret_cust_revenue_year),
        '',
        'Last Week ({:.2f}%)'.format(week_ret_cust_revenue_percentage),
        'Last Year ({:.2f}%)'.format(year_ret_cust_revenue_percentage)
    ],
    'Ret Cust Orders': [
        '{:.2f}'.format(ret_cust_orders_day),
        '{:.2f}'.format(ret_cust_orders_week),
        '{:.2f}'.format(ret_cust_orders_year),
        '',
        'Last Week ({:.2f}%)'.format(week_ret_cust_orders_percentage),
        'Last Year ({:.2f}%)'.format(year_ret_cust_orders_percentage)
    ],
    'New Cust AOV': [
        '£{:.2f}'.format(new_cust_aov_day),
        '£{:.2f}'.format(new_cust_aov_week),
        '£{:.2f}'.format(new_cust_aov_year),
        '',
        'Last Week ({:.2f}%)'.format(week_new_cust_aov_percentage),
        'Last Year ({:.2f}%)'.format(year_new_cust_aov_percentage)
    ],
    'Ret Cust AOV': [
        '£{:.2f}'.format(ret_cust_aov_day),
        '£{:.2f}'.format(ret_cust_aov_week),
        '£{:.2f}'.format(ret_cust_aov_year),
        '',
        'Last Week ({:.2f}%)'.format(week_ret_cust_aov_percentage),
        'Last Year ({:.2f}%)'.format(year_ret_cust_aov_percentage)
    ]
}

data_week_to_date = {
    'Net Rev': [
        '£{:.2f}'.format(current_week_aggregates["revenue"]),
        '£{:.2f}'.format(previous_week_aggregates["revenue"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["revenue"]),
        '',
        'vs Last Week ({:.2f}%)'.format(week_to_date_revenue_change),
        'vs Last Year ({:.2f}%)'.format(week_to_date_revenue_change_vs_last_year)
    ],
    'Gross Profit': [
        '£{:.2f}'.format(current_week_aggregates["gp"]),
        '£{:.2f}'.format(previous_week_aggregates["gp"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["gp"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_gp_change),
        'Last Year ({:.2f}%)'.format(week_to_date_gp_change_vs_last_year)
    ],
    'GP%': [
        '{:.2f}%'.format(current_week_aggregates["gp_percent"]),
        '{:.2f}%'.format(previous_week_aggregates["gp_percent"]),
        '{:.2f}%'.format(same_period_last_year_aggregates["gp_percent"]),
        '',
        'vs Last Week ({:.2f}%)'.format(week_to_date_gp_percent_change),
        'vs Last Year ({:.2f}%)'.format(week_to_date_gp_percent_change_vs_last_year)
    ],
    'No. of Orders': [
        '{:.2f}'.format(current_week_aggregates["orders"]),
        '{:.2f}'.format(previous_week_aggregates["orders"]),
        '{:.2f}'.format(same_period_last_year_aggregates["orders"]),
        '',
        'vs Last Week ({:.2f}%)'.format(week_to_date_orders_change),
        'vs Last Year ({:.2f}%)'.format(week_to_date_orders_change_vs_last_year)
    ],
    'AOV': [
        '£{:.2f}'.format(current_week_aggregates["aov"]),
        '£{:.2f}'.format(previous_week_aggregates["aov"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["aov"]),
        '',
        'vs Last Week ({:.2f}%)'.format(week_to_date_aov_change),
        'vs Last Year ({:.2f}%)'.format(week_to_date_aov_change_vs_last_year)
    ],
    'Sessions/Visitors': [
        '{:.2f}'.format(current_week_aggregates["sessions"]),
        '{:.2f}'.format(previous_week_aggregates["sessions"]),
        '{:.2f}'.format(same_period_last_year_aggregates["sessions"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_sessions_change),
        'Last Year ({:.2f}%)'.format(week_to_date_sessions_change_vs_last_year)
    ],
    'Conversion Rate': [
        '{:.2f}%'.format(current_week_aggregates["conversion_rate"]),
        '{:.2f}%'.format(previous_week_aggregates["conversion_rate"]),
        '{:.2f}%'.format(same_period_last_year_aggregates["conversion_rate"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_conversion_rate_change),
        'Last Year ({:.2f}%)'.format(week_to_date_conversion_rate_change_vs_last_year)
    ],
    'Ad Spend': [
        '£{:.2f}'.format(current_week_aggregates["ad_spend"]),
        '£{:.2f}'.format(previous_week_aggregates["ad_spend"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["ad_spend"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_ad_spend_change),
        'Last Year ({:.2f}%)'.format(week_to_date_ad_spend_change_vs_last_year)
    ],
    'COS': [
        '£{:.2f}'.format(current_week_aggregates["cost_of_sales"]),
        '£{:.2f}'.format(previous_week_aggregates["cost_of_sales"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["cost_of_sales"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_cost_of_sales_change),
        'Last Year ({:.2f}%)'.format(week_to_date_cost_of_sales_change_vs_last_year)
    ],
    'GP Post Ad Spend': [
        '£{:.2f}'.format(current_week_aggregates["gp_post_ad_spend"]),
        '£{:.2f}'.format(previous_week_aggregates["gp_post_ad_spend"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["gp_post_ad_spend"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_gp_post_ad_spend_change),
        'Last Year ({:.2f}%)'.format(week_to_date_gp_post_ad_spend_change_vs_last_year)
    ],
    'Cont. Pre Mktg': [
        '£{:.2f}'.format(current_week_aggregates["contribution_pre_marketing"]),
        '£{:.2f}'.format(previous_week_aggregates["contribution_pre_marketing"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["contribution_pre_marketing"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_contribution_pre_marketing_change),
        'Last Year ({:.2f}%)'.format(week_to_date_contribution_pre_marketing_change_vs_last_year)
    ],
    'Cost/Session': [
        '£{:.2f}'.format(current_week_aggregates["cost_per_session"]),
        '£{:.2f}'.format(previous_week_aggregates["cost_per_session"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["cost_per_session"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_cost_per_session_change),
        'Last Year ({:.2f}%)'.format(week_to_date_cost_per_session_change_vs_last_year)
    ],
    'Rev/Session': [
        '£{:.2f}'.format(current_week_aggregates["revenue_per_session"]),
        '£{:.2f}'.format(previous_week_aggregates["revenue_per_session"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["revenue_per_session"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_revenue_per_session_change),
        'Last Year ({:.2f}%)'.format(week_to_date_revenue_per_session_change_vs_last_year)
    ],
    'New Cust Net Rev': [
        '£{:.2f}'.format(current_week_aggregates["new_customer_net_revenue"]),
        '£{:.2f}'.format(previous_week_aggregates["new_customer_net_revenue"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["new_customer_net_revenue"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_new_customer_net_revenue_change),
        'Last Year ({:.2f}%)'.format(week_to_date_new_customer_net_revenue_change_vs_last_year)
    ],
    'Ret Cust Net Rev': [
        '£{:.2f}'.format(current_week_aggregates["returning_customer_net_revenue"]),
        '£{:.2f}'.format(previous_week_aggregates["returning_customer_net_revenue"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["returning_customer_net_revenue"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_returning_customer_net_revenue_change),
        'Last Year ({:.2f}%)'.format(week_to_date_returning_customer_net_revenue_change_vs_last_year)
    ],
    'Ret Cust Orders': [
        '{:.2f}'.format(current_week_aggregates["returning_customer_orders"]),
        '{:.2f}'.format(previous_week_aggregates["returning_customer_orders"]),
        '{:.2f}'.format(same_period_last_year_aggregates["returning_customer_orders"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_returning_customer_orders_change),
        'Last Year ({:.2f}%)'.format(week_to_date_returning_customer_orders_change_vs_last_year)
    ],
    'New Cust AOV': [
        '£{:.2f}'.format(current_week_aggregates["new_customer_aov"]),
        '£{:.2f}'.format(previous_week_aggregates["new_customer_aov"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["new_customer_aov"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_new_customer_aov_change),
        'Last Year ({:.2f}%)'.format(week_to_date_new_customer_aov_change_vs_last_year)
    ],
    'Ret Cust AOV': [
        '£{:.2f}'.format(current_week_aggregates["returning_customer_aov"]),
        '£{:.2f}'.format(previous_week_aggregates["returning_customer_aov"]),
        '£{:.2f}'.format(same_period_last_year_aggregates["returning_customer_aov"]),
        '',
        'Last Week ({:.2f}%)'.format(week_to_date_returning_customer_aov_change),
        'Last Year ({:.2f}%)'.format(week_to_date_returning_customer_aov_change_vs_last_year)
    ]
}

data_month_to_date = {
    'Net Rev': [
        '£{:.2f}'.format(current_month_aggregates["revenue"]),
        '£{:.2f}'.format(previous_month_aggregates["revenue"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["revenue"]),
        '',
        'vs Last Month ({:.2f}%)'.format(month_to_date_revenue_change),
        'vs Last Year ({:.2f}%)'.format(month_to_date_revenue_change_vs_last_year)
    ],
    'Gross Profit': [
        '£{:.2f}'.format(current_month_aggregates["gp"]),
        '£{:.2f}'.format(previous_month_aggregates["gp"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["gp"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_gp_change),
        'Last Year ({:.2f}%)'.format(month_to_date_gp_change_vs_last_year)
    ],
'GP%': [
        '{:.2f}%'.format(current_month_aggregates["gp_percent"]),
        '{:.2f}%'.format(previous_month_aggregates["gp_percent"]),
        '{:.2f}%'.format(same_month_last_year_aggregates["gp_percent"]),
        '',
        'vs Last Week ({:.2f}%)'.format(month_to_date_gp_percent_change),
        'vs Last Year ({:.2f}%)'.format(month_to_date_gp_percent_change_vs_last_year)
    ],
    'No. of Orders': [
        '{:.2f}'.format(current_month_aggregates["orders"]),
        '{:.2f}'.format(previous_month_aggregates["orders"]),
        '{:.2f}'.format(same_month_last_year_aggregates["orders"]),
        '',
        'vs Last Month ({:.2f}%)'.format(month_to_date_orders_change),
        'vs Last Year ({:.2f}%)'.format(month_to_date_orders_change_vs_last_year)
    ],
    'AOV': [
        '£{:.2f}'.format(current_month_aggregates["aov"]),
        '£{:.2f}'.format(previous_month_aggregates["aov"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["aov"]),
        '',
        'vs Last Month ({:.2f}%)'.format(month_to_date_aov_change),
        'vs Last Year ({:.2f}%)'.format(month_to_date_aov_change_vs_last_year)
    ],
    'Sessions/Visitors': [
        '{:.2f}'.format(current_month_aggregates["sessions"]),
        '{:.2f}'.format(previous_month_aggregates["sessions"]),
        '{:.2f}'.format(same_month_last_year_aggregates["sessions"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_sessions_change),
        'Last Year ({:.2f}%)'.format(month_to_date_sessions_change_vs_last_year)
    ],
    'Conversion Rate': [
        '{:.2f}%'.format(current_month_aggregates["conversion_rate"]),
        '{:.2f}%'.format(previous_month_aggregates["conversion_rate"]),
        '{:.2f}%'.format(same_month_last_year_aggregates["conversion_rate"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_conversion_rate_change),
        'Last Year ({:.2f}%)'.format(month_to_date_conversion_rate_change_vs_last_year)
    ],
    'Ad Spend': [
        '£{:.2f}'.format(current_month_aggregates["ad_spend"]),
        '£{:.2f}'.format(previous_month_aggregates["ad_spend"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["ad_spend"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_ad_spend_change),
        'Last Year ({:.2f}%)'.format(month_to_date_ad_spend_change_vs_last_year)
    ],
    'COS': [
        '£{:.2f}'.format(current_month_aggregates["cost_of_sales"]),
        '£{:.2f}'.format(previous_month_aggregates["cost_of_sales"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["cost_of_sales"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_cost_of_sales_change),
        'Last Year ({:.2f}%)'.format(month_to_date_cost_of_sales_change_vs_last_year)
    ],
    'GP Post Ad Spend': [
        '£{:.2f}'.format(current_month_aggregates["gp_post_ad_spend"]),
        '£{:.2f}'.format(previous_month_aggregates["gp_post_ad_spend"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["gp_post_ad_spend"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_gp_post_ad_spend_change),
        'Last Year ({:.2f}%)'.format(month_to_date_gp_post_ad_spend_change_vs_last_year)
    ],
    'Cont. Pre Mktg': [
        '£{:.2f}'.format(current_month_aggregates["contribution_pre_marketing"]),
        '£{:.2f}'.format(previous_month_aggregates["contribution_pre_marketing"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["contribution_pre_marketing"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_contribution_pre_marketing_change),
        'Last Year ({:.2f}%)'.format(month_to_date_contribution_pre_marketing_change_vs_last_year)
    ],
    'Cost/Session': [
        '£{:.2f}'.format(current_month_aggregates["cost_per_session"]),
        '£{:.2f}'.format(previous_month_aggregates["cost_per_session"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["cost_per_session"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_cost_per_session_change),
        'Last Year ({:.2f}%)'.format(month_to_date_cost_per_session_change_vs_last_year)
    ],
    'Rev/Session': [
        '£{:.2f}'.format(current_month_aggregates["revenue_per_session"]),
        '£{:.2f}'.format(previous_month_aggregates["revenue_per_session"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["revenue_per_session"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_revenue_per_session_change),
        'Last Year ({:.2f}%)'.format(month_to_date_revenue_per_session_change_vs_last_year)
    ],
    'New Cust Net Rev': [
        '£{:.2f}'.format(current_month_aggregates["new_customer_net_revenue"]),
        '£{:.2f}'.format(previous_month_aggregates["new_customer_net_revenue"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["new_customer_net_revenue"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_new_customer_net_revenue_change),
        'Last Year ({:.2f}%)'.format(month_to_date_new_customer_net_revenue_change_vs_last_year)
    ],
    'Ret Cust Net Rev': [
        '£{:.2f}'.format(current_month_aggregates["returning_customer_net_revenue"]),
        '£{:.2f}'.format(previous_month_aggregates["returning_customer_net_revenue"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["returning_customer_net_revenue"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_returning_customer_net_revenue_change),
        'Last Year ({:.2f}%)'.format(month_to_date_returning_customer_net_revenue_change_vs_last_year)
    ],
    'Ret Cust Orders': [
        '{:.2f}'.format(current_month_aggregates["returning_customer_orders"]),
        '{:.2f}'.format(previous_month_aggregates["returning_customer_orders"]),
        '{:.2f}'.format(same_month_last_year_aggregates["returning_customer_orders"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_returning_customer_orders_change),
        'Last Year ({:.2f}%)'.format(month_to_date_returning_customer_orders_change_vs_last_year)
    ],
    'New Cust AOV': [
        '£{:.2f}'.format(current_month_aggregates["new_customer_aov"]),
        '£{:.2f}'.format(previous_month_aggregates["new_customer_aov"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["new_customer_aov"]),
        '',
        'Last Month ({:.2f}%)'.format(month_to_date_new_customer_aov_change),
        'Last Year ({:.2f}%)'.format(month_to_date_new_customer_aov_change_vs_last_year)
    ],
    'Ret Cust AOV': [
        '£{:.2f}'.format(current_month_aggregates["returning_customer_aov"]),
        '£{:.2f}'.format(previous_month_aggregates["returning_customer_aov"]),
        '£{:.2f}'.format(same_month_last_year_aggregates["returning_customer_aov"]),
        '',
        'Last Week ({:.2f}%)'.format(month_to_date_new_customer_aov_change),
        'Last Year ({:.2f}%)'.format(month_to_date_new_customer_aov_change_vs_last_year)
    ]
}



df_yesterday = pd.DataFrame(data_yesterday)

# Round numeric values to 2 decimal places
numeric_cols = df_yesterday.select_dtypes(include=[float]).columns
df_yesterday[numeric_cols] = df_yesterday[numeric_cols].round(2)
print(df_yesterday)

df_week = pd.DataFrame(data_week_to_date)

# Round numeric values to 2 decimal places
numeric_cols = df_week.select_dtypes(include=[float]).columns
df_week[numeric_cols] = df_week[numeric_cols].round(2)
print(df_week)

df_month = pd.DataFrame(data_month_to_date)

# Round numeric values to 2 decimal places
numeric_cols = df_month.select_dtypes(include=[float]).columns
df_month[numeric_cols] = df_month[numeric_cols].round(2)
print(df_month)
# Function to create table in PDF
def create_table(dataframe, title, pdf,y_position):
    # Convert DataFrame to list of lists for Table creation
    table_data = [dataframe.columns.to_list()] + dataframe.values.tolist()

    # Define Table
    table = Table(table_data, colWidths=[100] * len(dataframe.columns))  # Adjust column widths as needed

    # Define TableStyle
    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.green),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]

    # Apply TableStyle to Table
    # Apply conditional formatting to each cell
    for i in range(1, len(table_data)):
        for j in range(len(table_data[i])):
            cell_value = table_data[i][j]
            if isinstance(cell_value, str) and '%' in cell_value:
                value = float(cell_value.split('(')[-1].replace('%', '').replace(')', ''))
                if value < 0:
                    table_style.append(('TEXTCOLOR', (j, i), (j, i), colors.red))
                else:
                    table_style.append(('TEXTCOLOR', (j, i), (j, i), colors.green))

    # Apply TableStyle to Table
    table.setStyle(TableStyle(table_style))

    # Set the width and draw the table
    table.wrapOn(pdf, 1800, 800)  # Adjust dimensions as needed
    table.drawOn(pdf, 30, y_position - 20)  # Adjust x position as needed


    # Draw title on PDF
    pdf.drawString(30, y_position + 120, title)


# Generate PDF
pdf_filename = "KPIs_Report.pdf"
pdf = canvas.Canvas(pdf_filename, pagesize=(2000, 1000))  # Adjust the canvas size as needed

# Create tables stacked on the same page
create_table(df_yesterday, 'KPIs Yesterday Total', pdf, 770)
create_table(df_week, 'KPIs Week To Date Total', pdf, 600)
create_table(df_month, 'KPIs Month To Date Total', pdf, 430)

# Save and close PDF
pdf.save()

print(f"PDF saved as {pdf_filename}")