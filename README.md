# covid19_vaccine_availability_tracker

How to use ?

1. Login to https://selfregistration.cowin.gov.in/ using mobile OTP
2. From the request headers get the

    a) `authorization` header value 

    b) `if-none-match` header value 

    and replace these in `config.py` 


3. run the program `python __init__.py`

A token works for 12 hours atleast (still counting and will update the lifetime accordingly)

Currently output looks like this 

```
Age_limit=18, Vaccine=COVISHIELD, District_name=Central Delhi, DATE=17-05-2021, Pincode=110005, Center=Dr B L Kapur Hospital Site 1, available_capacity_dose1=0, available_capacity_dose2=99
Age_limit=18, Vaccine=COVISHIELD, District_name=Central Delhi, DATE=17-05-2021, Pincode=110005, Center=Dr B L Kapur Hospital Site 3, available_capacity_dose1=0, available_capacity_dose2=100
Age_limit=18, Vaccine=COVISHIELD, District_name=Central Delhi, DATE=17-05-2021, Pincode=110005, Center=Dr B L Kapur Hospital Site 2, available_capacity_dose1=0, available_capacity_dose2=100
Age_limit=18, Vaccine=COVISHIELD, District_name=Central Delhi, DATE=17-05-2021, Pincode=110005, Center=Dr B L Kapur Hospital Site 4, available_capacity_dose1=0, available_capacity_dose2=100
Age_limit=18, Vaccine=COVISHIELD, District_name=East Delhi, DATE=18-05-2021, Pincode=110092, Center=Max Hospital Patparganj, available_capacity_dose1=0, available_capacity_dose2=1
Age_limit=18, Vaccine=COVISHIELD, District_name=East Delhi, DATE=19-05-2021, Pincode=110092, Center=Max Hospital Patparganj, available_capacity_dose1=0, available_capacity_dose2=1
Age_limit=18, Vaccine=COVISHIELD, District_name=North East Delhi, DATE=17-05-2021, Pincode=110094, Center=GBSSS Old Mustafabad S4, available_capacity_dose1=1, available_capacity_dose2=0
Age_limit=18, Vaccine=COVISHIELD, District_name=North West Delhi, DATE=17-05-2021, Pincode=110088, Center=Max Hospital Site 3, available_capacity_dose1=0, available_capacity_dose2=40
Age_limit=18, Vaccine=COVISHIELD, District_name=North West Delhi, DATE=17-05-2021, Pincode=110088, Center=Max Hospital Site 1, available_capacity_dose1=0, available_capacity_dose2=59
Age_limit=18, Vaccine=COVISHIELD, District_name=North West Delhi, DATE=17-05-2021, Pincode=110088, Center=Max Hospital Site 2, available_capacity_dose1=0, available_capacity_dose2=60
Age_limit=18, Vaccine=COVISHIELD, District_name=South East Delhi, DATE=17-05-2021, Pincode=110044, Center=Indraprastha Apollo Site 2, available_capacity_dose1=0, available_capacity_dose2=4
Age_limit=18, Vaccine=COVISHIELD, District_name=South East Delhi, DATE=17-05-2021, Pincode=110044, Center=Indraprastha Apollo Site 3, available_capacity_dose1=0, available_capacity_dose2=5
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110002, Center=MCW Kanchan Puri PHC, available_capacity_dose1=20, available_capacity_dose2=20
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110006, Center=MAMC SITE 1, available_capacity_dose1=0, available_capacity_dose2=3
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110006, Center=MAIDS SITE 1, available_capacity_dose1=0, available_capacity_dose2=9
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110007, Center=Hindu Rao Hosl DH SITE 2, available_capacity_dose1=0, available_capacity_dose2=1
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110007, Center=Hindu Rao Hosl DH SITE 3, available_capacity_dose1=0, available_capacity_dose2=3
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110007, Center=Hindu Rao Hospital DH SITE 1, available_capacity_dose1=0, available_capacity_dose2=4
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110007, Center=Hindu Rao Hospital SITE 6, available_capacity_dose1=0, available_capacity_dose2=7
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110007, Center=Hindu Rao Hospital SITE 5, available_capacity_dose1=1, available_capacity_dose2=5

Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=17-05-2021, Pincode=110007, Center=Hindu Rao Hospital SITE 4, available_capacity_dose1=2, available_capacity_dose2=7
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=18-05-2021, Pincode=110007, Center=Hindu Rao Hospital DH SITE 1, available_capacity_dose1=0, available_capacity_dose2=9
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=18-05-2021, Pincode=110007, Center=Hindu Rao Hospital SITE 5, available_capacity_dose1=0, available_capacity_dose2=10
Age_limit=45, Vaccine=COVAXIN, District_name=Central Delhi, DATE=18-05-2021, Pincode=110007, Center=Hindu Rao Hospital SITE 6, available_capacity_dose1=0, available_capacity_dose2=14

```

# TODO
1. Cron and notify on mobile when our requirement matches (For ex. 18+ covaxin anywhere in delhi)   URGENT and IMPORTANT
2. automate OTP login (figuring out some ways) NOT URGENT as current token has lifetime of 12+ hrs 
