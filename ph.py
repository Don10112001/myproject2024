import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
from mpl_toolkits.basemap import Basemap


st.set_page_config(page_title="Pharma Sales" ,
                   page_icon="💊",
                   layout="wide"
)

# Load data
@st.cache_data
def load_data(path: str):
    data=pd.read_excel(path)
    return data
df=load_data("Hanuman.xlsx")


# Create tabs in the sidebar using radio buttons
tab_selected = st.sidebar.radio("Navigation", [ "Summary","Dashboard"])

if tab_selected == "Dashboard":
    
    
#-------------MAINPAGE--------------#
    
# Define unique values for each filter parameter
    unique_months = df['Month'].unique()
    unique_product_classes = df['Product Class'].unique()
    unique_sales_teams = df['Sales Team'].unique()


# Interactive Filters
    st.sidebar.header("Please filter Here:")
    selected_months = st.sidebar.multiselect("Select the Month:", options=unique_months, default=unique_months)
    selected_product_classes = st.sidebar.multiselect("Select the Product Class:", options=unique_product_classes, default=unique_product_classes)
    selected_sales_teams = st.sidebar.multiselect("Select the Sales Team:", options=unique_sales_teams, default=unique_sales_teams)

    st.markdown("# 💊 PHARMA | SALES ANALYSIS")
    

    st.divider()


# Filter the data based on user selections
    filtered_df = df.query("Month in @selected_months & `Product Class` in @selected_product_classes & `Sales Team` in @selected_sales_teams")

    

    lef_colm,righ_colm=st.columns(2)
# Grouping by 'Customer Name' and calculating total sales
    sales_by_customer = filtered_df.groupby('Customer Name')['Sales'].sum().reset_index()
# Plotting the graph using Plotly Express
    fig1 = px.bar(
    sales_by_customer,
    x='Customer Name',
    y='Sales',
    title='Sales by Customer',
    labels={'Sales': 'Total Sales'}
     )
    fig1.update_layout(
   
    plot_bgcolor="rgba(0,0,0,0)",  # Match the background color of the bar chart
    yaxis=(dict(showgrid=False))
    )


    st.divider()

# Grouping by 'Month' and calculating total sales
    monthly_sales = filtered_df.groupby('Month')['Sales'].sum().reset_index()
# Plotting the line chart using Plotly Express
    fig2 = px.line(
    monthly_sales,
    x='Month',
    y='Sales',
    title='Monthly Sales',
    labels={'Sales': 'Total Sales'}
    )
    fig2.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",  # Match the background color of the bar chart
    yaxis=(dict(showgrid=False))
     )


    lef_colm.plotly_chart(fig1, use_container_width=True,align='center')


    righ_colm.plotly_chart(fig2, use_container_width=True,align='center')


    col1,col2,col3=st.columns(3)
# Grouping by 'Product Class' and calculating total sales
    class_sales = filtered_df.groupby('Product Class')['Sales'].sum().reset_index()
# Plotting pie chart for total sales across all product classes using Plotly Express
    fig3 = px.pie(
    class_sales,
    values='Sales',
    names='Product Class',
    title='Total Sales Distribution Across Product Classes', 
    labels={'Product Class': 'Class', 'Sales': 'Total Sales'},
    hole=0.3
     )


# Grouping by 'Sales Team' and calculating total sales
    sales_by_team = filtered_df.groupby('Sales Team')['Sales'].sum().reset_index()
# Plotting the horizontal bar graph using Plotly Express
    fig4 = px.bar(
    sales_by_team,
    x='Sales',
    y='Sales Team',
    title='Total Sales by Sales Team',
    orientation='h',  # Horizontal orientation
    labels={'Sales': 'Total Sales'}
    )

# Aggregate sales volume by product class
    sales_by_product_class = filtered_df.groupby('Product Class')['Sales'].sum().reset_index()
# Plotting the bar chart for sales volume by product class
    fig5 = px.bar(
    sales_by_product_class,
    x='Sales',
    y='Product Class',
    title='Sales Volume by Product Class',
    orientation='h',  # Horizontal orientation
    labels={'Sales': 'Total Sales'}
     )
    col1.plotly_chart(fig3, use_container_width=True,align='center')
    col2.plotly_chart(fig4, use_container_width=True,align='center')
    col3.plotly_chart(fig5, use_container_width=True,align='center')

    st.divider()

    col4,col5,col6=st.columns(3)
# Calculate customer distribution by country
    country_distribution = filtered_df['Country'].value_counts().reset_index()
    country_distribution.columns = ['Country', 'Count']
# Plotting the pie chart for customer distribution by country
    fig6 = px.pie(
    country_distribution,
    values='Count',
    names='Country',
    title='Customer Distribution by Country',
     )


# Aggregate sales volume by channel
    sales_by_channel = filtered_df.groupby('Channel')['Sales'].sum().reset_index()
# Plotting the bar chart for sales volume by channel
    fig7 = px.bar(
    sales_by_channel,
    x='Sales',
    y='Channel',
    title='Sales Volume by Channel',
    orientation='h',  # Horizontal orientation
    labels={'Sales': 'Total Sales'}
     )


# Sample data
    managers = filtered_df['Manager']
    sales = filtered_df['Sales']
    teams = filtered_df['Sales Team']

# Create DataFrame for scatter plot
    scatter_df = pd.DataFrame({'Manager': managers, 'Sales': sales, 'Sales Team': teams})
# Create scatter plot using Plotly Express
    fig8 = px.scatter(
    scatter_df,
    x='Sales',
    y='Sales Team',
    color='Manager',
    title='Manager Dashboard',
    labels={'Sales': 'Sales', 'Sales Team': 'Sales Team'},
    color_discrete_sequence=px.colors.qualitative.Set1,
    opacity=0.8,
    size_max=100
    )

    col4.plotly_chart(fig6, use_container_width=True,align='center')
    col5.plotly_chart(fig7, use_container_width=True,align='center')
    col6.plotly_chart(fig8, use_container_width=True,align='center')



# Rename the columns to 'latitude' and 'longitude'
    filtered_df = filtered_df.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'})

# Display map using st.map
    st.map(filtered_df, latitude='latitude', longitude='longitude')

    # Filter the data for distributors in Poland
    poland_data = filtered_df[filtered_df['Country'] == 'Poland']

# Calculate total sales for each distributor
    distributor_sales = poland_data.groupby('Distributor')['Sales'].sum().reset_index()

# Sort the data by total sales
    distributor_sales = distributor_sales.sort_values(by='Sales', ascending=False)

# Plot the pie chart
    fig10 = px.pie(distributor_sales, values='Sales', names='Distributor', title='Distribution of Sales Among Distributors in Poland')
    #st.plotly_chart(fig)
    
    # Filter the data for distributors in Poland
    germany_data = filtered_df[filtered_df['Country'] == 'Germany']

# Calculate total sales for each distributor
    distributor_sales = germany_data.groupby('Distributor')['Sales'].sum().reset_index()

# Sort the data by total sales
    distributor_sales = distributor_sales.sort_values(by='Sales', ascending=False)

# Plot the pie chart
    fig11 = px.pie(distributor_sales, values='Sales', names='Distributor', title='Distribution of Sales Among Distributors in Germany')
    #st.plotly_chart(fig)

    
    col1,col2,col3=st.columns(3)
    
    col1.plotly_chart(fig10, use_container_width=True, align='center')
    col3.plotly_chart(fig11, use_container_width=True, align='center')


elif tab_selected == "Summary":
    st.title("Summary")

    # Summary statistics
    st.write("## Summary Statistics")
    st.write(df.describe())
    # Explanation of product categories
     # Explanation of product categories
    st.write("## Product Categories:")
    st.write("1. □ **Analgesics**: Medications used to relieve pain.")
    st.write("2. □ **Antibiotics**: Drugs used to treat bacterial infections.")
    st.write("3. □ **Antimalarial**: Medications used to prevent or treat malaria.")
    st.write("4. □ **Antipyretics**: Medications used to reduce fever.")
    st.write("5. □ **Antiseptics**: Substances applied to living tissues to reduce the risk of infection.")
    st.write("6. □ **Mood Stabilizers**: Medications used to treat mood disorders.")