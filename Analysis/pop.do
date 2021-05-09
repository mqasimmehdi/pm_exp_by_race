clear
pwd
import delimited "C:\Users\mqasi\OneDrive\Desktop\Charley\Census data 2010-2019\cc-est2019-alldata.csv"
keep if year==12
drop if agegrp ==0
collapse (sum) tot_pop tot_male tot_female wa_male wa_female ba_male ba_female ia_male ia_female aa_male aa_female na_male na_female tom_male tom_female wac_male wac_female bac_male bac_female iac_male iac_female aac_male aac_female nac_male nac_female nh_male nh_female nhwa_male nhwa_female nhba_male nhba_female nhia_male nhia_female nhaa_male nhaa_female nhna_male nhna_female nhtom_male nhtom_female nhwac_male nhwac_female nhbac_male nhbac_female nhiac_male nhiac_female nhaac_male nhaac_female nhnac_male nhnac_female h_male h_female hwa_male hwa_female hba_male hba_female hia_male hia_female haa_male haa_female hna_male hna_female htom_male htom_female hwac_male hwac_female hbac_male hbac_female hiac_male hiac_female haac_male haac_female hnac_male hnac_female, by(state county stname ctyname)

gen total = tot_pop
gen nonhisp_white = nhwa_male + nhwa_female
gen nonhisp_black = nhba_male + nhba_female
gen nonhisp_NA_alaska = nhia_male + nhia_female 
gen nonhisp_hawai_pacific = nhna_male + nhna_female
gen nonhisp_asian = nhaa_male + nhaa_female
gen hisp_white = hwa_male + hwa_female 
gen hisp_black = hba_male + hba_female

keep state county stname ctyname total nonhisp_white nonhisp_black nonhisp_NA_alaska nonhisp_hawai_pacific nonhisp_asian hisp_black hisp_white
save 2019demo.dta, replace
export delimited using "2019demo", replace