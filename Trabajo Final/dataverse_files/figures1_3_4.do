clear all
set more off
cd "HERE SPECIFY THE FOLDER PATH YOU ANT TO USE" 

********************************************************************************
**Figure I: Municipal and Annual Variation of Homicide Rates in Colombia********
********************************************************************************
use figures1_3_4_data, clear
bysort year: egen dev_hom_r=sd(hom_r)
keep dev_hom_r year
duplicates drop

set scheme s1mono
twoway (line dev_hom_r year, sort lwidth(thick)), ///
ytitle("Standard Deviation by Municipality", size(medium)) ///
xtitle("Year") ///
ylabel(30(10)80) ///
xlabel(1995(5)2010) ///
title("Panel A. Municipal Variation") ///
graphregion(color(white)) saving(f1_a, replace)

use figures1_panelb_data, clear
twoway (line hom_r year, sort lwidth(thick)), ///
ytitle("Homicide Rates per 100,000 individuals", size(medium)) ///
xtitle("Year") ///
ylabel(30(10)80, format(%9.0f)) ///
xlabel(1995(5)2010) ///
title("Panel B. Annual Variation") ///
graphregion(color(white)) saving(f1_b, replace)

gr combine f1_a.gph f1_b.gph, ycommon 
graph export "figure1.png", replace
erase "f1_a.gph"
erase "f1_b.gph"
********************************************************************************
**Figure III: Homicides by Vote Share in 1st and 2nd Presidential Elections*****
********************************************************************************
use figures1_3_4_data, clear
**Panel A&B: All municipalities**
g yes_02=(s_uribe_02>=0.5)
g no_02=(s_uribe_02<0.5)
g yes_02_y=(s_uribe_06>=0.5&yes_02==1)
bysort year: egen m_yes_02_y=mean(hom_r) if yes_02_y==1
g yes_02_n=(s_uribe_06<0.5&yes_02==1)
bysort year: egen m_yes_02_n=mean(hom_r) if yes_02_n==1
g no_02_y=(s_uribe_06>=0.5&no_02==1)
bysort year: egen m_no_02_y=mean(hom_r) if no_02_y==1
g no_02_n=(s_uribe_06<0.5&no_02==1)
bysort year: egen m_no_02_n=mean(hom_r) if no_02_n==1

set scheme s1mono
twoway (line m_yes_02_y year if year>2001, sort lwidth(thick)) ///
       (line m_yes_02_n year if year>2001, sort lwidth(thick) lpattern(dot)) ///
       (line m_no_02_y year if year>2001, sort lwidth(thick) lpattern(longdash_dot)) ///
       (line m_no_02_n year if year>2001, sort lwidth(thick) lpattern(dash)), ///
ytitle("Mean Hom Rates", size(medium)) ///
xtitle("Year", size(small)) ///
ylabel(20(10)100) ///
title("Panel B. During Uribe") ///
legend(order(1 "Always Won" 2 "Won 1-Lost 2" 3 "Lost 1-Won 2" 4 "Always Lost")) ///
graphregion(color(white)) saving(panel_b, replace)

twoway (line m_yes_02_y year if year<=2001, sort lwidth(thick)) ///
       (line m_yes_02_n year if year<=2001, sort lwidth(thick) lpattern(dot)) ///
       (line m_no_02_y year if year<=2001, sort lwidth(thick) lpattern(longdash_dot)) ///
       (line m_no_02_n year if year<=2001, sort lwidth(thick) lpattern(dash)), ///
title("Homicides by Vote Share of 1st and 2nd Elections") ///
ytitle("Mean Hom Rates", size(medium)) ///
xtitle("Year", size(small)) ///
ylabel(20(10)100) ///
title("Panel A. Before Uribe") ///
legend(order(1 "Always Won" 2 "Won 1-Lost 2" 3 "Lost 1-Won 2" 4 "Always Lost")) ///
graphregion(color(white)) saving(panel_a, replace)

gr combine panel_a.gph panel_b.gph, ycommon ///
title("All Municipalities", size(medium)) 
graph export "figure3_all.png", replace

**Panel C&D**
drop m_yes_02_y m_yes_02_n m_no_02_y m_no_02_n
bysort year: egen m_yes_02_y=mean(hom_r) if yes_02_y==1&manu_sample==1
bysort year: egen m_yes_02_n=mean(hom_r) if yes_02_n==1&manu_sample==1
bysort year: egen m_no_02_y=mean(hom_r) if no_02_y==1&manu_sample==1
bysort year: egen m_no_02_n=mean(hom_r) if no_02_n==1&manu_sample==1

twoway (line m_yes_02_y year if year>2001&manu_sample==1, sort lwidth(thick)) ///
       (line m_yes_02_n year if year>2001&manu_sample==1, sort lwidth(thick) lpattern(dot)) ///
       (line m_no_02_y year if year>2001&manu_sample==1, sort lwidth(thick) lpattern(longdash_dot)) ///
       (line m_no_02_n year if year>2001&manu_sample==1, sort lwidth(thick) lpattern(dash)), ///
ytitle("Mean Hom Rates", size(medium)) ///
xtitle("Year", size(small)) ///
ylabel(20(10)100) ///
title("Panel D. During Uribe") ///
legend(order(1 "Always Won" 2 "Won 1-Lost 2" 3 "Lost 1-Won 2" 4 "Always Lost")) ///
graphregion(color(white)) saving(panel_d, replace)

twoway (line m_yes_02_y year if year<=2001&manu_sample==1, sort lwidth(thick)) ///
       (line m_yes_02_n year if year<=2001&manu_sample==1, sort lwidth(thick) lpattern(dot)) ///
       (line m_no_02_y year if year<=2001&manu_sample==1, sort lwidth(thick) lpattern(longdash_dot)) ///
       (line m_no_02_n year if year<=2001&manu_sample==1, sort lwidth(thick) lpattern(dash)), ///
title("Homicides by Vote Share of 1st and 2nd Elections") ///
ytitle("Mean Hom Rates", size(medium)) ///
xtitle("Year", size(small)) ///
ylabel(20(10)100) ///
title("Panel C. Before Uribe") ///
legend(order(1 "Always Won" 2 "Won 1-Lost 2" 3 "Lost 1-Won 2" 4 "Always Lost")) ///
graphregion(color(white)) saving(panel_c, replace)

gr combine panel_c.gph panel_d.gph, ycommon ///
title("Municipalities with Firm Data Available", size(medium)) 
graph export "figure3_eam.png", replace
erase "panel_a.gph"
erase "panel_b.gph"
erase "panel_c.gph"
erase "panel_d.gph"

********************************************************************************
***FIGURE IV: Mean Change in Homicide Rates for Uribe’s Supporters**************
********************************************************************************
**Panel A&B**
use figures1_3_4_data, clear
g d1=s_uribe_02
replace d1=0 if year<2002
bysort muncod: g d10_02=hom_r-hom_r[_n-8] if year==2010
g indicator=. 
replace indicator=1 if d1<=0.1
replace indicator=2 if d1>0.1&d1<=0.2
replace indicator=3 if d1>0.2&d1<=0.3
replace indicator=4 if d1>0.3&d1<=0.4
replace indicator=5 if d1>0.4&d1<=0.5
replace indicator=6 if d1>0.5&d1<=0.6
replace indicator=7 if d1>0.6&d1<=0.7
replace indicator=8 if d1>0.7&d1<=0.8
replace indicator=9 if d1>0.8&d1<=0.9
replace indicator=10 if d1>0.9&d1<=1
g ind=indicator/10
drop indicator
bysort ind: egen m_d10_02=mean(d10_02) if year==2010
replace ind=. if year!=2010

set scheme s1mono
twoway (lfitci m_d10_02 ind if year==2010, lwidth(thick)) ///
       (scatter m_d10_02 ind if year==2010, lwidth(thick)), ///
ytitle("Change in Homicide Rates 2010-2002", size(small)) ///
xtitle("% Votes for Uribe 1st Election", size(small)) ///
ylabel(-80(20)20) ///
title("Panel B. Change during Uribe (2010-2002)", size(medium)) ///
legend(order(1 "95% CI" 2 "Linear Fit" 3 "Mean Values")) ///
graphregion(color(white)) saving(panel_b, replace)

sort muncod year
bysort muncod: g ind1=ind[_n+9] if year==2001
bysort muncod: g d01_95=hom_r-hom_r[_n-6] if year==2001
bysort ind1: egen m_d01_95=mean(d01_95) if year==2001

set scheme s1mono
twoway (lfitci m_d01_95 ind1 if year==2001, lwidth(thick)) ///
       (scatter m_d01_95 ind1 if year==2001, lwidth(thick)), ///
ytitle("Change in Homicide Rates 2001-1995", size(small)) ///
xtitle("% Votes for Uribe 1st Election", size(small)) ///
ylabel(-80(20)20) ///
title("Panel A. Change before Uribe (2001-1995)", size(medium)) ///
legend(order(1 "95% CI" 2 "Linear Fit" 3 "Mean Values")) ///
graphregion(color(white)) saving(panel_a, replace)

gr combine panel_a.gph panel_b.gph, ycommon xcommon ///
title("All Municipalities" , size(medium))
graph export "figure4_all.png", replace


**Panel B: With 317 mun in EAM sample**
drop m_d10_02 m_d01_95
bysort ind: egen m_d10_02=mean(d10_02) if year==2010&manu_sample==1

set scheme s1mono
twoway (lfitci m_d10_02 ind if year==2010&manu_sample==1, lwidth(thick)) ///
       (scatter m_d10_02 ind if year==2010&manu_sample==1, lwidth(thick)), ///
ytitle("Change in Homicide Rates 2010-2002", size(small)) ///
xtitle("% Votes for Uribe 1st Election", size(small)) ///
ylabel(-80(20)20) ///
title("Panel D. Change during Uribe (2010-2002)", size(medium)) ///
legend(order(1 "95% CI" 2 "Linear Fit" 3 "Mean Values")) ///
graphregion(color(white)) saving(panel_d, replace)

sort muncod year
bysort ind1: egen m_d01_95=mean(d01_95) if year==2001&manu_sample==1

set scheme s1mono
twoway (lfitci m_d01_95 ind1 if year==2001&manu_sample==1, lwidth(thick)) ///
       (scatter m_d01_95 ind1 if year==2001&manu_sample==1, lwidth(thick)), ///
ytitle("Change in Homicide Rates 2001-1995", size(small)) ///
xtitle("% Votes for Uribe 1st Election", size(small)) ///
ylabel(-80(20)20) ///
title("Panel C. Change before Uribe (2001-1995)", size(medium)) ///
legend(order(1 "95% CI" 2 "Linear Fit" 3 "Mean Values")) ///
graphregion(color(white)) saving(panel_c, replace)

gr combine panel_c.gph panel_d.gph, ycommon xcommon ///
title("Municipalities with Firm Data Available" , size(medium))
graph export "figure4_eam.png", replace
erase "panel_a.gph"
erase "panel_b.gph"
erase "panel_c.gph"
erase "panel_d.gph"
