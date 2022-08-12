This folder contains replication files for the paper "Is Murder Bad for Business? Evidence from Colombia"
By Sandra V Rozo. It was constructed using Stata 14.0. Please follow the instructions below to replicate the main tables and figures of the paper.
------------------------------------------------------------------------------------------
1. Replicating Figures
------------------------------------------------------------------------------------------
a. Figures 1, 3, and 4: save the files "figures1_3_4.do", "figures1_3_4_data.dta", and "figures1_panelb_data.dta" in your preferred path folder and specify the folder path in the do file "figures1_3_4.do". Then run the do file to replicate Figures 1, 3, and 4. The outputs should look like "figure1.png", "figure3_all.png", "figure3_eam.png", "figure4_all.png", and "figure4_eam".
b. Figure 2: The shapefiles used to construct the maps are titled "Figure2_Shapefile". You need 5 files with the same name but with extensions .dbf, prj, shp, shx, xml. To construct the map for 2002 put the five files in the same folder and open the shapefile "Figure2_shapefile" in ArcMap ArcGIS 10.3.1. Click on the layer Figure2_shapefile. In the window that will pop click on "Quantities". Select field value HOM_R2002. Classify break values manually in 3 intervals using 20 and 40 as upper end intervals. Click ok and then click apply. Repeat the process using the variable HOM_R2011 to get the secod map.
------------------------------------------------------------------------------------------
2. Replicating Tables
------------------------------------------------------------------------------------------
Do files and non-proprietary data that needs to be merged with DANE's proprietary data are:
"controls.dta"
"ipp.dta"
"Constructing_Data_Tables1_3.do"
"Constructing_Data_Table2.do"
"Estimates_Table1.do"
"Estimates_Table2.do"
"Estimates_Table3.do"
These files are meant to be run with the raw data available in the data processing data center at DANE (instruction on how to get access to the data at DANE can be found in numeral 3).
a. Using DANE's raw data and the dta files "controls.dta" and "ipp.dta" first run the do files "Constructing_Data_Table..." to construct the data base for each table.
b. Once the data bases are constructed run the do files "Estimates_Table..." to replicate each table of the paper.
-----------------------------------------------------------
3. Instructions for accessing the proprietary data at DANE
-----------------------------------------------------------
The manufacturing census can be accessed by signing a confidential information agreement with DANE (the Colombian Statistics Department) an action available to any researcher. Detailed instructions and information on getting access to DANE's data processing center can be found at: http://www.dane.gov.co/files/noticias/Actualidad_DANE_06_03_2015.pdf?phpMyAdmin=a9ticq8rv198vhk5e8cck52r11
To access the information the researcher needs to present a brief research proposal and request access to the data through a formal letter (which can be sent to contact@dane.gov.co or by calling to Bogota to the number 5978300 extension 2605 or 2532). Once the research proposal is approved the researcher will sign a confidential agreement and will be able to work inside of DANE with the micro data. 
----------------------------------------------------------
4. Data dictionary:
----------------------------------------------------------
Each variable contained in the stata files has a label that describes what each variable stands for.