from datetime import datetime


class VaccineSlot:
    def __init__(self, date, age_limit, vaccine, state_id, state_name, district_id, district_name, pincode, center_name, center_id, available_capacity_dose1, available_capacity_dose2):
        self.date = date
        self.age_limit = age_limit
        self.vaccine = vaccine
        self.state_id = state_id
        self.state_name = state_name
        self.district_id = district_id
        self.district_name = district_name
        self.pincode = pincode
        self.center_name = center_name
        self.center_id = center_id
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

    def get_upsert_query(self):
        query = """
        Insert into vaccine_slot (center_id, pincode, age_limit, vaccine, state_id, state_name, district_id, district_name, center_name, slot_date, available_capacity_dose1, timestamp_update_dose1, available_capacity_dose2, timestamp_update_dose2)
        VALUES ({center_id}, {pincode}, {age_limit}, '{vaccine}', {state_id}, '{state_name}', {district_id}, '{district_name}', '{center_name}', '{slot_date}', {available_capacity_dose1}, CURRENT_TIMESTAMP(), {available_capacity_dose2}, CURRENT_TIMESTAMP())
        ON DUPLICATE KEY UPDATE
            timestamp_update_dose1=IF(VALUES(available_capacity_dose1)>available_capacity_dose1, VALUES(timestamp_update_dose1), timestamp_update_dose1), 
            available_capacity_dose1=IF(VALUES(available_capacity_dose1)<>available_capacity_dose1, VALUES(available_capacity_dose1), available_capacity_dose1),
            timestamp_update_dose2=IF(VALUES(available_capacity_dose2)>available_capacity_dose2, VALUES(timestamp_update_dose2), timestamp_update_dose2), 
            available_capacity_dose2=IF(VALUES(available_capacity_dose2)<>available_capacity_dose2, VALUES(available_capacity_dose2), available_capacity_dose2);
        """.format(
                center_id=self.center_id,
                pincode=self.pincode,
                age_limit=self.age_limit,
                vaccine=self.vaccine,
                state_id=self.state_id,
                state_name=self.state_name,
                district_id=self.district_id,
                district_name=self.district_name,
                center_name=self.center_name,
                slot_date=str(datetime.strptime(self.date, '%d-%m-%Y').date()),
                available_capacity_dose1=self.available_capacity_dose1,
                available_capacity_dose2=self.available_capacity_dose2
        )
        return query

    @staticmethod
    def get_updated_records_query(start_time, vaccine, state_id, district_id, age_limit, dose_1=False, dose_2=False):
        if not dose_1 and not dose_2:
            return ""  # Need to specify atleast the criteria to get updated records based on dose1 or dose2

        query = """
        SELECT CAST(slot_date AS char) as "slot date", age_limit as age_category, vaccine, pincode, district_name as district, center_name as center, available_capacity_dose1, available_capacity_dose2 from vaccine_slot
        WHERE vaccine like '%{vaccine}%' and state_id={state_id} and district_id={district_id} and age_limit={age_limit} and (
        """.format(start_time=start_time, vaccine=vaccine, state_id=state_id, district_id=district_id, age_limit=age_limit)
        if dose_1:
            query += " (timestamp_update_dose1 > '{start_time}' and available_capacity_dose1>5)".format(
                start_time=start_time)
        if dose_2:
            if dose_1:
                query += " or "
            query += "(timestamp_update_dose2 > '{start_time}' and available_capacity_dose2>5)".format(
                start_time=start_time)
        query += ")"

        return query
