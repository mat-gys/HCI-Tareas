# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

#### Import package

from wwo_hist import retrieve_hist_data


#### Set working directory to store output csv file(s)

import os
os.chdir("C:\\Users\\Matias\\Documents\\UDESA\\Herramientas computacionales\\Clase 3\\out\\weather")



#### Example code

frequency=24
start_date = '1-Jan-2015'
end_date = '31-Dec-2015'
api_key = 'ad1ec718ca634fbdaa9124306221107'
location_list = ['20637', '20653', '20688', '20735', '20874', '21040', '21043', '21157', '21211', '21220', '21412', '21502', '21601', '21638', '21639', '21643', '21651', '21702', '21746', '21804', '21811', '21853', '21902']


hist_weather_data = retrieve_hist_data(api_key,
                                location_list,
                                start_date,
                                end_date,
                                frequency,
                                location_label = False,
                                export_csv = True,
                                store_df = True)