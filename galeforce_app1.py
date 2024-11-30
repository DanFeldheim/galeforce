#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 11:02:37 2024

An app that imports a csv file with workshop participant data and restructures it
so that it is easily filtered and analyzed. 

@author: danfeldheim
"""

# Imports
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import time
from st_aggrid import GridOptionsBuilder, AgGrid, GridUpdateMode, DataReturnMode, ColumnsAutoSizeMode
from pathlib import Path



# Page config
st.set_page_config(layout = "wide", 
                   page_title = 'Gale Force Analytics', 
                   initial_sidebar_state="auto", 
                   menu_items = None)


class Flow_Control():
    """This class makes all of the calls to other classes and methods."""
    
    def __init__(self):
        
        pass
            
    def all_calls(self):
        
        # Render the galeforce Header
        header = Setup().header()
        # Upload the data
        data = Upload()
        file = data.upload_button()
        
        try:
            # Split the dataframe into dfs for the admin and each registrant
            splitter = data.split()
            # Merge dataframes
            merge = data.df_merger(splitter)
            # Deal with "other" church affiliations
            other = data.move_other(merge)
            # Aggregate to yield the final result
            agg = data.agg_dataframe(other)
            # Show df as aggrid table
            table = data.create_table(agg)
            
        except:
            pass
        
        
        
class Setup():
    """Class that defines the font and button styles and lays out headers."""
    
    def __init__(self):
        
        # Get the directory of the current script
        current_dir = Path(__file__).parent
        
        # Build the full path to the file
        # Logo file must be in same folder as py file
        # self.logo_file = str(current_dir) + '/logo.jpg'
        self.logo_file = 'logo.jpg'
    
    
    def header(self):
        
        # Set styles
        st.markdown("""<style>
                        .blue-36 {
                        font-size:36px !important;
                        color:blue}
                        </style>
                        """, unsafe_allow_html=True)
                        
        st.markdown("""<style>
                        .blue-30 {
                        font-size:30px !important;
                        color:blue}
                        </style>
                        """, unsafe_allow_html=True)
                        
        st.markdown("""<style>
                        .purple-24 {
                        font-size:24px !important;
                        color:Purple}
                        </style>
                        """, unsafe_allow_html = True)
                        
        st.markdown("""<style>
                        .blueviolet-28 {
                        font-size:28px !important;
                        color:blueviolet}
                        </style>
                        """, unsafe_allow_html = True)
                        
        st.markdown("""<style>
                        .green-18 {
                        font-size:18px !important;
                        color:Green}
                        </style>
                        """, unsafe_allow_html = True)
                        
        st.markdown("""<style>
                        .green-24 {
                        font-size:24px !important;
                        color:DarkGreen;
                        font-weight: bold;}
                        </style>
                        """, unsafe_allow_html = True)
                        
        st.markdown("""<style>
                        .DarkBlue-24 {
                        font-size:24px !important;
                        color:DarkBlue;
                        font-weight: bold;}
                        </style>
                        """, unsafe_allow_html = True)
                        
        # Create a global button style
        st.markdown("""
        <style>
        div.stButton > button:first-child {
            background-color: rgb(0, 102, 102);
            color: white;
            font-size:20px;
            font-weight: bold;
            margin-left: 0;
            # margin: auto;
            display: block;
        }
        
        div.stButton {
        display: flex;
        justify-content: flex-start;
        }
        
        div.stButton > button:hover {
         	background:linear-gradient(to bottom, rgb(0, 204, 204) 5%, rgb(0, 204, 204) 100%);
         	background-color:rgb(0, 204, 204);
        }
        
        div.stButton > button:active {
         	position:relative;
         	top:3px;
        }
        </style>""", unsafe_allow_html=True) 
        
        # Set the color of the sidebar
        st.markdown("""
        <style>
        [data-testid=stSidebar] {
            background-color: LightSteelBlue;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Set the whitespace at the top of the app
        st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                }
        </style>
        """, unsafe_allow_html=True)
        
        # Style the widget text
        st.markdown("""
        <style>
        div[class*="stTextArea"] label p {
          font-size: 18px;
          color: DarkBlue;
        }
        
        div[class*="stTextInput"] label p {
          font-size: 18px;
          color: DarkBlue;
        }
        
        div[class*="stNumberInput"] label p {
          font-size: 18px;
          color: green;
        }
        
        div[class*="stDateInput"] label p {
          font-size: 18px;
          color: DarkBlue;
        }
        
        div[class*="stFileUploader"] label p {
          font-size: 18px;
          color: green;
        }
        </style>
        """, unsafe_allow_html=True)
        
        # Draw line across the page
        st.divider()
        
        # Add a logo and title
        col1, col2 = st.columns([1,4])
        
        with col1:
  
            st.image(self.logo_file, width = 175)
        
        with col2:
            st.write('')
            st.write('')
            st.write('')
            st.write('')
            st.markdown('<p class = "blue-36">Annual Council Registration Spreadsheet Analyzer</p>', unsafe_allow_html = True)
        
        st.divider()
        
class Upload():
    
    def __init__(self):
        
        pass
    
    def upload_button(self):
        
        file_upload = st.file_uploader('Upload File', accept_multiple_files = False)
        
        if file_upload is not None:
            
            # Read the file as a dataframe
            self.data_df = pd.read_csv(file_upload)
            # st.write(self.data_df)
    
    def split(self):
        
       # Create a dataframe with cols = Church through admin phone
       self.admin_info = self.data_df[['Church', 
                                       'Other', 
                                       'Registrants', 
                                       'Admin Name',
                                       'Admin Email',
                                       'Admin Phone']]
       
       # st.write(self.admin_info)
       
       # Make a df with all the registrants
       self.registrant_df = self.data_df.iloc[:, [1,2] + list(range(7, self.data_df.shape[1]))]
       # st.write(self.registrant_df)
       
       # Use the number of columns to calculate the number of registrants
       # Put col names in a list and the count the # of columns
       # Divide by the number of fields entered per registrant
       column_names_list = self.registrant_df.columns.tolist()
       max_registrant_number = int(len(column_names_list)/6)
       
       # Create a dict to hold the individual admin and registrant dataframes
       self.subset_df_dict = {'admin':self.admin_info}
       
       # Use the number of participants to loop through df and split out the individual registrants
       for number in range(1, max_registrant_number + 1):
           
           # Get the Church, Other and registrant columns by looking for the registrant number
           subset_df = self.registrant_df[['Church', 'Other'] + 
                                          [col for col in self.registrant_df.columns if str(number) in col]] 
           
           # Rename columns without the number
           subset_df = subset_df.rename(columns = {'First Name ' + str(number): 'First Name', 
                                                 'Last Name ' + str(number): 'Last Name',
                                                 'Email ' + str(number): 'Email',
                                                 'Type ' + str(number): 'Application',
                                                 'Kids ' + str(number): 'Kids',
                                                 'Workshop ' + str(number): 'Workshop'})
           # st.write(subset_df)
           
           # Add df to dictionary
           key_word = 'registrant_' + str(number)
           self.subset_df_dict[key_word] = subset_df
           
       return self.subset_df_dict
   
    def df_merger(self, subset_dict):
        
        subset_df_concat = pd.concat(subset_dict.values(), ignore_index=True)

        return subset_df_concat
    
    def move_other(self, merger):
        # Where church name was entered in the other column, move it to the church column
        column_to_check = "Church"
        column_to_move_from = "Other"
        
        for index, row in merger.iterrows():
            # Check if the value is None
            if pd.isnull(row[column_to_check]):  
                merger.loc[index, column_to_check] = row[column_to_move_from]
                
        # Drop the "Other" column
        merger.drop('Other', axis=1, inplace=True)
            
        # st.write(merger)
        
        return merger
        
    def agg_dataframe(self, unaggregated_df):
        
        # st.write(unaggregated_df)
        
        self.final_df = unaggregated_df.groupby('Church').agg({'Registrants': 'first',
                                                                        'Admin Name': 'first',
                                                                        'Admin Email': 'first',
                                                                        'Admin Phone': 'first',
                                                                        'First Name': 'first',
                                                                        'Last Name': 'first',
                                                                        'Email': 'first',
                                                                        'Application': 'first',
                                                                        'Kids': 'first',
                                                                        'Workshop': 'first',
                                                                        }).reset_index()
        
        # st.write(self.final_df)
        
        return self.final_df
    
    def create_table(self, final_df):
        
        st.write('')
        st.markdown('<p class = "DarkBlue-24">View Data</p>', unsafe_allow_html = True) 
        
        # Add an AgGrid table
        # Insert config file as an editable aggrid table 
        gb = GridOptionsBuilder.from_dataframe(final_df)
        
        # Add pagination
        # gb.configure_pagination(paginationAutoPageSize = True) 
        
        # Add a sidebar
        gb.configure_side_bar() 
        
        # Enable multi-row selection with checkboxes
        # gb.configure_selection('single', use_checkbox = True)
        
        # Add custom CSS styles
        gb.configure_default_column(headerClass="custom-header", filter = True)
        custom_css = {".ag-header-cell-label": {
                            "color": "yellow",
                            # "background-color": "blue",
                            "font-weight": "bold",
                            "font-size": "14px",
                            "text-align": "center",
                            },
                        ".ag-header-viewport": {
                            "background-color": "blue"  
                            },
                        "#gridToolBar": {
                            "padding-bottom": "0px !important",
                            }
                        }

        
        gb.configure_grid_options(domLayout = 'normal')
        
        # Build the table
        gridOptions = gb.build()
        
        # VALUE_CHANGED makes the change when the value is entered, MANUAL gives an update button at the top.
        # Padding changes the white space above the table.
        self.grid_return = AgGrid(final_df, 
                                  gridOptions = gridOptions, 
                                  update_mode = GridUpdateMode.SELECTION_CHANGED,
                                  columns_auto_size_mode = ColumnsAutoSizeMode.FIT_CONTENTS,
                                  theme = 'streamlit', 
                                  data_return_mode = 'AS_INPUT', 
                                  enable_enterprise_modules = True,
                                  reload_data = False, 
                                  height = 200, 
                                  fit_columns_on_grid_load = True, 
                                  allow_unsafe_jscode = True, 
                                  custom_css=custom_css
                                  )  
        
        # Get the grid data
        grid_data = self.grid_return['data']
        
        # Download button
        st.download_button(
            label="Download",
            data=grid_data.to_csv(index=False),
            file_name='data.csv',
            mime='text/csv'
        )
       



# Run 
if __name__ == '__main__':
    
    obj1 = Flow_Control()
    all_calls = obj1.all_calls()