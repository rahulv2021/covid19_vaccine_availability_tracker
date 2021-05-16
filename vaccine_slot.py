class VaccineSlot:
    def __init__(self, date, age_limit, vaccine, district_name, pincode, center_name, available_capacity_dose1, available_capacity_dose2):
        self.date = date
        self.age_limit = age_limit
        self.vaccine = vaccine
        self.district_name = district_name
        self.pincode = pincode
        self.center_name = center_name
        self.available_capacity_dose1 = available_capacity_dose1
        self.available_capacity_dose2 = available_capacity_dose2

    def __repr__(self):
        return "Age_limit={age_limit}, Vaccine={vaccine}, District_name={district_name}, DATE={date}, Pincode={pincode}, Center={center_name}, available_capacity_dose1={available_capacity_dose1}, available_capacity_dose2={available_capacity_dose2}".format(
                date=self.date,
                age_limit=self.age_limit,
                vaccine=self.vaccine,
                district_name=self.district_name,
                pincode=self.pincode,
                center_name=self.center_name,
                available_capacity_dose1=self.available_capacity_dose1,
                available_capacity_dose2=self.available_capacity_dose2)


