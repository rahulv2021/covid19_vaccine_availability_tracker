import cowin_gateway
import config
import datetime
import vaccine_slot



# Tweak the parameters in this function as per your requirement. By default fetches availability for all ages, all vaccines and all doses (first and second)
def get_available_slots_by_state_id_and_dates(scheme, hostname, headers, state_id, dates, dose_1=True, dose_2=True, age_limits=[18, 45], vaccines=["covaxin", "covishield", "sputnik"]):
    district_ids = cowin_gateway.get_districts_by_state_id(scheme, hostname, headers, state_id)
    available_slots = []
    for date in dates:
        for district_id in district_ids:
            centers = cowin_gateway.get_vaccine_centers_by_district_and_date(scheme, hostname, headers, district_id, date)
            for center in centers:
                for slot in center["sessions"]:
                    if slot["min_age_limit"] in age_limits and \
                       ((dose_1 and slot["available_capacity_dose1"]>0) or (dose_2 and slot["available_capacity_dose2"]>0)) and \
                       slot["vaccine"].lower() in vaccines:
                        available_slot = vaccine_slot.VaccineSlot(date=slot["date"],
                                                                  age_limit=slot["min_age_limit"],
                                                                  vaccine=slot["vaccine"],
                                                                  district_name=center["district_name"],
                                                                  pincode=center["pincode"],
                                                                  center_name=center["name"],
                                                                  available_capacity_dose1=slot["available_capacity_dose1"],
                                                                  available_capacity_dose2=slot["available_capacity_dose2"])
                        available_slots.append(available_slot)
    # Order by age limit, vaccine, district, date, pincode, available doses
    sorted_slots = sorted(available_slots, key=lambda slot: (slot.age_limit, slot.vaccine, slot.district_name, slot.date, slot.pincode, slot.available_capacity_dose1, slot.available_capacity_dose2))
    for slot in sorted_slots:
        print slot
    return sorted_slots


if __name__ == "__main__":
    dates = []
    # Get first date of each week for given week ranges. Default 2 weeks
    for week in range(0, config.week_range):
        date = datetime.datetime.now() + datetime.timedelta(weeks=week)
        dates.append(date.strftime("%d-%m-%Y"))

    for state in config.state_ids:
        get_available_slots_by_state_id_and_dates(config.scheme,
                                                  config.hostname,
                                                  config.headers,
                                                  config.state_ids[state],
                                                  dates)
