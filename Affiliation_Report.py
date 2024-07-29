# -*- coding: utf-8 -*-
"""
Created on Mon Jul 29 13:40:15 2024

@author: PLedin
"""

import streamlit as st

###############################################################################
#Function Definitions
###############################################################################
def get_report_periods():
    retVal = True

    return retVal

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

def format_currency(amount):
    return '${:,.2f}'.format(amount)
###############################################################################
#Get Snowflake session
###############################################################################

###############################################################################
#Start building Streamlit App
###############################################################################
add_sidebar_afl_type = st.sidebar.selectbox('Affiliation Type', ('Member of CUNA and/or NAFCU','Legacy CUNA', 'Legacy NAFCU', 'Member of Both'))
add_sidebar_group_by = st.sidebar.selectbox('Group By', ('State','League', 'Asset Class(9)', 'Asset Class(13)'))
#add_sidebar_month = st.sidebar.selectbox('Month', get_report_periods(session))

#month = convertDateToSystem(add_sidebar_month)

st.title("America's Credit Unions")
st.write("----------------------------------------------------------")
st.write("Affiliation Report")
#st.write("Month Ended: " + add_sidebar_month)

if add_sidebar_afl_type == 'Member of CUNA and/or NAFCU':
    st.write("Affiliated Members of Legacy CUNA and/or NAFCU")
    aflType = "either"
    
if add_sidebar_afl_type == 'Legacy CUNA':
    st.write("Affiliated Members of Legacy CUNA")
    aflType = "legacycuna"

if add_sidebar_afl_type == 'Legacy NAFCU':
    st.write("Affiliated Members of Legacy NAFCU")
    aflType = "legacynafcu"

if add_sidebar_afl_type == 'Member of Both':
    st.write("Affiliated Members of Both Legacy CUNA and NAFCU")
    aflType = "both"
    
if add_sidebar_group_by == 'State':
    st.write("Grouped by State")
    st.write("----------------------------------------------------------")
    groupBy = "bystate"
#    table1 = session.table("monthly_report." + aflType + ".afl_table_1_" + groupBy + "_" + month).to_pandas()
    
if add_sidebar_group_by == 'League':
    st.write("Grouped by League")
    st.write("----------------------------------------------------------")
    groupBy = "byleague"
#    table1 = session.table("monthly_report." + aflType + ".afl_table_1_" + groupBy + "_" + month).to_pandas()

if add_sidebar_group_by == 'Asset Class(9)':
    st.write("Grouped by Asset Class (9)")
    st.write("----------------------------------------------------------")
    groupBy = "byacl_9"
#    table1 = session.table("monthly_report." + aflType + ".afl_table_4_" + groupBy + "_" + month).to_pandas()

if add_sidebar_group_by == 'Asset Class(13)':
    st.write("Grouped by Asset Class (13)")
    st.write("----------------------------------------------------------")
    groupBy = "byacl_13"
#    table1 = session.table("monthly_report." + aflType + ".afl_table_3_" + groupBy + "_" + month).to_pandas()

#table1['% CUs Affiliated'] = table1['% CUs Affiliated'] * 100
#table1['% Memberships Affiliated'] = table1['% Memberships Affiliated'] * 100
#table1['% Assets Affiliated'] = table1['% Assets Affiliated'] * 100

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

#st.dataframe(data = table1, 
#             column_config=column_configuration,
#             use_container_width = True, 
#             hide_index = True,
#            )

#if add_sidebar_group_by == 'State' or add_sidebar_group_by == 'League':
#    table2 = session.table("monthly_report." + aflType + ".afl_table_2_" + groupBy + "_" + month).to_pandas()
#    st.dataframe(data = table2, use_container_width = True)





 