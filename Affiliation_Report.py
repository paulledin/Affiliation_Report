# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:40:15 2024

@author: PLedin
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

###############################################################################
#Function Definitions
###############################################################################
def get_report_periods():
    periods = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/MonthlyReportPeriods.csv')
    
    retVal = list()
    index = 0
    for x in periods:
        retVal.insert(index, periods[x])
        index += 1

    return pd.DataFrame(retVal[0])

def getTable1(aflType, groupBy, month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/afl_table_1_' + groupBy + '_' + aflType + '_' + month + '.csv'))

def getTable2(aflType, groupBy, month):
    return pd.DataFrame(pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/afl_table_2_' + groupBy + '_' + aflType + '_' + month + '.csv'))

def getChartData(aflType, groupBy):
    periods = get_report_periods()
    
    retVal = pd.DataFrame({"Period" : [],
                           "Measure" : [],
                           "AFL Rate" : []})    
    for x in periods.index:
        df_this_period = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/afl_table_1_' + groupBy + '_' + aflType + '_' + str(periods['period'][x]) + '.csv')
        df_this_period = df_this_period.loc[(df_this_period['State'] == 'Totals')]
        df_this_period = df_this_period[['% CUs Affiliated', '% Memberships Affiliated', '% Assets Affiliated']]
        df_this_period['period'] = str(periods['period'][x])
        
        pct_cus_value = pd.DataFrame(df_this_period.iloc[0:, 0])
        pct_mem_value = pd.DataFrame(df_this_period.iloc[0:, 1])
        pct_asset_value = pd.DataFrame(df_this_period.iloc[0:, 2])
        retVal.loc[len(retVal.index)] = [str(periods['period'][x]), '% CUs Affiliated', pct_cus_value['% CUs Affiliated'].iloc[0] * 100]
        retVal.loc[len(retVal.index)] = [str(periods['period'][x]), '% Memberships Affiliated', pct_mem_value['% Memberships Affiliated'].iloc[0] * 100]
        retVal.loc[len(retVal.index)] = [str(periods['period'][x]), '% Assets Affiliated', pct_asset_value['% Assets Affiliated'].iloc[0] * 100]

    return (retVal)

def convertDateToDisplay(date):
    switcher = {
        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December",
    }
    
    return switcher.get(date[4:], "**Bad Month**") + "-" + date[:4]

def convertDateToSystem(date):
    switcher = {
        "January":  "01",
        "February": "02",
        "March":    "03",
        "April":    "04",
        "May":      "05",
        "June":     "06",
        "July":     "07",
        "August":   "08",
        "September":"09",
        "October":  "10",
        "November": "11",
        "December": "12",
    }
    
    return date[len(date)-4:len(date)] + switcher.get(date[:len(date)-5], "**Bad Month**")

def get_report_periods_for_display():
    periods = pd.read_csv('https://raw.githubusercontent.com/paulledin/data/master/MonthlyReportPeriods.csv')
    
    retVal = list()

    index = 0
    for x in periods:
        retVal.insert(index, periods[x])
        index += 1
        
    df_retVal = pd.DataFrame(retVal[0])
        
    for i in range(len(df_retVal)):
        period = df_retVal.loc[i, "period"]
        df_retVal.loc[df_retVal['period'] == period, 'report_periods_formatted'] = convertDateToDisplay(str(period))

    return df_retVal
    
def format_currency(amount):
    return '${:,.2f}'.format(amount)
###############################################################################
#Start building Streamlit App
###############################################################################
report_periods = get_report_periods_for_display()

add_sidebar_afl_type = st.sidebar.selectbox('Affiliation Type', ('Member of CUNA and/or NAFCU','Legacy CUNA', 'Legacy NAFCU', 'Member of Both'))
add_sidebar_group_by = st.sidebar.selectbox('Group By', ('State','League', 'Asset Class(9)', 'Asset Class(13)'))
add_sidebar_month = st.sidebar.selectbox('Month', report_periods['report_periods_formatted'])

month = convertDateToSystem(add_sidebar_month)

st.title("America's Credit Unions")
st.write("----------------------------------------------------------")
st.write("Affiliation Report")
st.write("Month Ended: " + add_sidebar_month)

if add_sidebar_afl_type == 'Member of CUNA and/or NAFCU':
    st.write("Affiliated Members of Legacy CUNA and/or NAFCU")
    aflType = "Either"
    
if add_sidebar_afl_type == 'Legacy CUNA':
    st.write("Affiliated Members of Legacy CUNA")
    aflType = "Legacycuna"

if add_sidebar_afl_type == 'Legacy NAFCU':
    st.write("Affiliated Members of Legacy NAFCU")
    aflType = "Legacynafcu"

if add_sidebar_afl_type == 'Member of Both':
    st.write("Affiliated Members of Both Legacy CUNA and NAFCU")
    aflType = "Both"
    
if add_sidebar_group_by == 'State':
    st.write("Grouped by State")
    st.write("----------------------------------------------------------")
    groupBy = "ByState"
    
if add_sidebar_group_by == 'League':
    st.write("Grouped by League")
    st.write("----------------------------------------------------------")
    groupBy = "ByLeague"

if add_sidebar_group_by == 'Asset Class(9)':
    st.write("Grouped by Asset Class (9)")
    st.write("----------------------------------------------------------")
    groupBy = "ByAcl_9"

if add_sidebar_group_by == 'Asset Class(13)':
    st.write("Grouped by Asset Class (13)")
    st.write("----------------------------------------------------------")
    groupBy = "ByAcl_13"

table1 = getTable1(aflType, groupBy, month)
table1['% CUs Affiliated'] = table1['% CUs Affiliated'] * 100
table1['% Memberships Affiliated'] = table1['% Memberships Affiliated'] * 100
table1['% Assets Affiliated'] = table1['% Assets Affiliated'] * 100

column_configuration = {
    "State": st.column_config.TextColumn(
        "State", max_chars=50
    ),
    "Affiliated CUs": st.column_config.NumberColumn(
        "Affiliated CUs",
        min_value=0,
        max_value=10000,
    ),
    "Non Affiliated CUs": st.column_config.NumberColumn(
        "Non Affiliated CUs",
        min_value=0,
        max_value=10000,
    ),
    "State Chartered": st.column_config.NumberColumn(
        "State Chartered",
        min_value=0,
        max_value=10000,
    ),
    "Fed Chartered": st.column_config.NumberColumn(
        "Fed Chartered",
        min_value=0,
        max_value=10000,
    ),
    "Total CUs": st.column_config.NumberColumn(
        "Total CUs",
        min_value=0,
        max_value=10000,
    ),
    "Affiliated Memberships": st.column_config.NumberColumn(
        "Affiliated Memberships",
        min_value=0,
        max_value=10000,
    ),
    "Affiliated Assets": st.column_config.NumberColumn(
        "Affiliated Assets",
        min_value=0,
        max_value=10000,
    ),
    "Total Assets": st.column_config.NumberColumn(
        "Total Assets",
        min_value=0,
        max_value=10000,
    ),
    "% CUs Affiliated": st.column_config.NumberColumn(
        "% CUs Affiliated",
        min_value=0,
        max_value=10000,
        format="%.1f"
    ),
    "% Memberships Affiliated": st.column_config.NumberColumn(
        "% Memberships Affiliated",
        min_value=0,
        max_value=10000,
        format="%.1f"
    ),
    "% Assets Affiliated": st.column_config.NumberColumn(
        "% Assets Affiliated",
        min_value=0,
        max_value=10000,
        format="%.1f"
    ),
}

chart_data = getChartData("Either", "ByState")
st.header('Affiliation Chart')

chart = alt.Chart(chart_data).mark_line().encode(
    x='Period',
    y='AFL Rate'
)
#st.write(chart, use_container_width = True)

st.dataframe(data = table1, 
             column_config=column_configuration,
             use_container_width = True, 
             hide_index = True,
            )

if add_sidebar_group_by == 'State' or add_sidebar_group_by == 'League':
    table2 = getTable2(aflType, groupBy, month)
    table2['% CUs Affiliated'] = table2['% CUs Affiliated'] * 100
    table2['% Memberships Affiliated'] = table2['% Memberships Affiliated'] * 100
    table2['% Assets Affiliated'] = table2['% Assets Affiliated'] * 100
    st.dataframe(data = table2, 
                 column_config=column_configuration,
                 use_container_width = True, 
                 hide_index = True,
                )





 
