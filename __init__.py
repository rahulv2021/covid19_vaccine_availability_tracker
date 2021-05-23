import copy
import cowin_gateway
import config
import datetime
import vaccine_slot
from collections import OrderedDict
from database_connection import DatabaseConnection
from slot_notifier import SlotNotifier

# Tweak the parameters in this function as per your requirement. By default fetches availability for all ages, all vaccines and all doses (first and second)


def get_available_slots_by_state_id_and_district_id_and_dates(scheme, hostname, headers, state_id, district_id, dates, start_time, dose_1=True, dose_2=True, age_limits=[18, 45], vaccines=["covaxin", "covishield", "sputnik"]):
    api_calls = 1
    available_slots = []
    for date in dates:
        vaccine_centers = cowin_gateway.get_vaccine_centers_by_district_and_date(scheme, hostname, headers, district_id, date)
        for center in vaccine_centers:
            for slot in center["sessions"]:
                if slot["min_age_limit"] in age_limits and \
                   ((dose_1 and slot["available_capacity_dose1"] > 0) or (dose_2 and slot["available_capacity_dose2"] > 0)) and \
                   slot["vaccine"].lower() in vaccines:
                    available_slot = vaccine_slot.VaccineSlot(date=slot["date"],
                                                              age_limit=slot["min_age_limit"],
                                                              vaccine=slot["vaccine"],
                                                              district_id=district_id,
                                                              district_name=center["district_name"],
                                                              pincode=center["pincode"],
                                                              state_id=state_id,
                                                              state_name=center["state_name"].lower(),
                                                              center_name=center["name"],
                                                              center_id=center["center_id"],
                                                              available_capacity_dose1=slot["available_capacity_dose1"],
                                                              available_capacity_dose2=slot["available_capacity_dose2"])
                    available_slots.append(available_slot)

    print "Total api calls = %s" % (api_calls)
    # Order by age limit, vaccine, district, date, pincode, available doses
    sorted_slots = sorted(available_slots, key=lambda slot: (slot.district_id, slot.center_id, slot.age_limit, slot.vaccine,
                                                             slot.date))
    # Filter unique slots
    # The json sometimes has ambiguous slots with same date
    # If that's the case then consider the max capacity among those slots to notify people
    unique_slots = []
    for slot in sorted_slots:
        if not unique_slots:
            unique_slots.append(slot)
            continue
        previous_slot = unique_slots[-1]
        if slot.center_id == previous_slot.center_id and slot.age_limit == previous_slot.age_limit and slot.vaccine == previous_slot.vaccine and slot.date==previous_slot.date:
            print "\n======Duplicate slot found"
            print slot
            slot.available_capacity_dose1 = max(slot.available_capacity_dose1, previous_slot.available_capacity_dose1)
            slot.available_capacity_dose2 = max(slot.available_capacity_dose2, previous_slot.available_capacity_dose2)
            unique_slots[-1] = slot
        else:
            unique_slots.append(slot)
    return unique_slots



def update_slots_in_database(available_slots):
    connection = DatabaseConnection().get_connection()
    cursor = connection.cursor()
    for slot in available_slots:
        query = slot.get_upsert_query()
        cursor.execute(query)
        connection.commit()


def get_updated_slots_from_database(start_time, vaccine, state_id, district_id, age_limit, dose_1=False, dose_2=False):
    records = []

    query = vaccine_slot.VaccineSlot.get_updated_records_query(
        start_time, vaccine, state_id, district_id, age_limit, dose_1, dose_2)
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
        message += "<b>%s: </b> %s \n" % (key, value)

    return message


def get_dates_from_weeks_range():
    """
    Returns list of first date of each week for given number of weeks
    """
    dates = []
    for week in range(0, config.week_range):
        date = datetime.datetime.now() + datetime.timedelta(weeks=week)
        dates.append(date.strftime("%d-%m-%Y"))
    return dates

def send_notifications_for_updated_slots_in_district(start_time, state, state_id, district_id):
    # Send notifications on Telegram
    slot_notifier = SlotNotifier()
    for vaccine in config.vaccines:
        for age_limit in config.age_limits:
            for dose in config.vaccines[vaccine][age_limit]:
                # get recent updated records from database for covaxin 18
                updated_slots_in_district = get_updated_slots_from_database(
                    start_time=start_time, vaccine=vaccine, state_id=state_id, district_id=district_id, age_limit=age_limit, **{dose: config.vaccines[vaccine][age_limit][dose]})
                print "Updated records for %s, %s, %s" % (vaccine, age_limit, dose)
                for record in updated_slots_in_district:
                    print "Sending message for record"
                    message = get_formatted_message(
                        record, **{dose: config.vaccines[vaccine][age_limit][dose]})
                    print message
                    slot_notifier.send_message(
                        age_limit, vaccine, state, message, dose)

def get_headers_for_cowin_apis():
    """
    Return token for cowin apis
    """
    token = config.tokens[0]
    headers = copy.deepcopy(config.headers)
    headers["authorization"] = headers["authorization"].format(token=token)
    print "Using token %s " % (headers["authorization"])
    return headers


if __name__ == "__main__":
    while True:
        try:
            date_format = "%Y-%m-%d %H:%M:%S"
            headers = get_headers_for_cowin_apis()
            dates = get_dates_from_weeks_range()

            program_start_time = datetime.datetime.now().strftime(date_format)

            for state in config.state_ids:
                state_id = config.state_ids[state]["id"]

                district_ids = config.state_ids[state]["district_ids"]
                if not district_ids:
                    district_ids = cowin_gateway.get_districts_by_state_id(
                        config.scheme, config.hostname, headers, state_id)

                for district_id in district_ids:
                    request_start_time = datetime.datetime.now().strftime(date_format)
                    available_slots_in_district = get_available_slots_by_state_id_and_district_id_and_dates(config.scheme,
                                                                                                            config.hostname,
                                                                                                            headers,
                                                                                                            state_id,
                                                                                                            district_id,
                                                                                                            dates,
                                                                                                            request_start_time)
                    time.sleep(1)
                    # save updated records from database
                    update_slots_in_database(available_slots_in_district)

                    # Send notifications on Telegram
                    send_notifications_for_updated_slots_in_district(request_start_time, state, state_id, district_id)
        except Exception as e:
            print ("Exception was raised. message = %s" % (e))
        finally:
            program_end_time = datetime.datetime.now().strftime(date_format)
            diff = datetime.datetime.strptime(
                program_end_time, date_format) - datetime.datetime.strptime(program_start_time, date_format)
            print "Total time taken = %s seconds" % (diff.total_seconds())
