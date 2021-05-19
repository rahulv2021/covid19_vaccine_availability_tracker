import cowin_gateway
import config
import datetime
import time
import vaccine_slot
from collections import OrderedDict
from database_connection import DatabaseConnection
from slot_notifier import SlotNotifier

# Tweak the parameters in this function as per your requirement. By default fetches availability for all ages, all vaccines and all doses (first and second)
def get_available_slots_by_state_id_and_dates(scheme, hostname, headers, state_id, district_ids, dates, start_time, dose_1=True, dose_2=True, age_limits=[18, 45], vaccines=["covaxin", "covishield", "sputnik"]):
    if not district_ids:
        district_ids = cowin_gateway.get_districts_by_state_id(scheme, hostname, headers, state_id)
    available_slots = []
    api_calls = 1
    for date in dates:
        for district_id in district_ids:
            centers = cowin_gateway.get_vaccine_centers_by_district_and_date(scheme, hostname, headers, district_id, date)
            api_calls += 1
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
                                                                  state_name=center["state_name"].lower(),
                                                                  center_name=center["name"],
                                                                  center_id=center["center_id"],
                                                                  available_capacity_dose1=slot["available_capacity_dose1"],
                                                                  available_capacity_dose2=slot["available_capacity_dose2"])
                        available_slots.append(available_slot)
    print "Total api calls = %s" % (api_calls)
    # Order by age limit, vaccine, district, date, pincode, available doses
    sorted_slots = sorted(available_slots, key=lambda slot: (slot.age_limit, slot.vaccine, slot.district_name, slot.date, slot.pincode, slot.available_capacity_dose1, slot.available_capacity_dose2))
    return sorted_slots

def update_records_in_database(available_slots):
    connection = DatabaseConnection().get_connection()
    cursor = connection.cursor()
    for slot in available_slots:
        query = slot.get_upsert_query()
        cursor.execute(query)
        connection.commit()

def get_records_from_database(start_time, vaccine, state_name, age_limit, dose_1=False, dose_2=False):
    records = []

    query = vaccine_slot.VaccineSlot.get_updated_records_query(start_time, vaccine, state_name, age_limit, dose_1, dose_2)
    if query:
        connection = DatabaseConnection().get_connection()
        cursor = connection.cursor()
        cursor.execute(query)

        column_names = [description[0] for description in cursor.description]
        for record in cursor.fetchall():
            records.append(OrderedDict(zip(column_names, record)))
        cursor.close()
    return records

def get_formatted_message(record, dose_1=False, dose_2=False):
    # message_object = namedtuple('X', record.keys())(*record.values())
    message = ""

    # index=0
    for key in record:
        if dose_1 and key == "available_capacity_dose2" or \
           dose_2 and key == "available_capacity_dose1":
            continue
        value = record[key]
        message += "<b>%s: </b> %s \n" %(key, value)

    return message



if __name__ == "__main__":
    count = 1
    while True:
        date_format = "%Y-%m-%d %H:%M:%S"
        start_time = datetime.datetime.now().strftime(date_format)
        dates = []
        token = config.tokens[count%3]
        config.headers["authorization"] = config.headers["authorization"].format(token=token)
        headers = config.headers
        print "Using token %s " % (config.headers["authorization"])
        # Get first date of each week for given week ranges. Default 2 weeks
        for week in range(0, config.week_range):
            date = datetime.datetime.now() + datetime.timedelta(weeks=week)
            dates.append(date.strftime("%d-%m-%Y"))

        for state in config.state_ids:
            state_id = config.state_ids[state]["id"]
            district_ids = config.state_ids[state]["district_ids"]
            available_slots = get_available_slots_by_state_id_and_dates(config.scheme,
                                                                        config.hostname,
                                                                        headers,
                                                                        state_id,
                                                                        district_ids,
                                                                        dates,
                                                                        start_time)

            # save updated records from database
            update_records_in_database(available_slots)

            # dispatch results on Telegram
            slot_notifier = SlotNotifier()
            for vaccine in config.vaccines:
                for age_limit in config.age_limits:
                    for dose in config.vaccines[vaccine][age_limit]:
                        # get recent updated records from database for covaxin 18
                        updated_slots = get_records_from_database(start_time=start_time, vaccine=vaccine, state_name=state, age_limit=age_limit, **{dose: config.vaccines[vaccine][age_limit][dose]})
                        print "Updated records for %s, %s, %s" %(vaccine, age_limit, dose)
                        for record in updated_slots:
                            print "Sending message for record"
                            message = get_formatted_message(record, **{dose: config.vaccines[vaccine][age_limit][dose]})
                            print message
                            slot_notifier.send_message(age_limit, vaccine, state, message, dose)
        end_time = datetime.datetime.now().strftime(date_format)
        diff = datetime.datetime.strptime(end_time, date_format) - datetime.datetime.strptime(start_time, date_format)
        print "Total time taken = %s seconds" %(diff.total_seconds())
        count += 1