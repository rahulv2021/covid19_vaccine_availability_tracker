import telegram 
import telegram_config
from decorators import retry

class SlotNotifier:
    def __init__(self):
        self.bot = telegram.Bot(token=telegram_config.bot_token)

    def _get_chat_id(self, age_limit, vaccine, state, dose):
        chat_id_key = "%s_%s_%s_%s" %(age_limit, vaccine.lower(), state.lower(), dose)
        if chat_id_key not in telegram_config.chat_ids:
            raise Exception("Invalid chat id %s. Please ensure the channel is added in config" %(chat_id_key))
        return chat_id_key

    @retry(Exception, max_retries=7, delay=6, backoff=2)
    def send_message(self, age_limit, vaccine, state, message, dose):
        if 'sputnik' in vaccine.lower():
            vaccine = "sputnik"    #don't know the exact name cowin are using
        chat_id_key = self._get_chat_id(age_limit, vaccine, state, dose)
        chat_id = telegram_config.chat_ids[chat_id_key]
        try:
            #print "Sending message for chat_id %s" %(chat_id_key)
            self.bot.sendMessage(chat_id=chat_id, text=message, parse_mode="html")
        except Exception as e:
            raise Exception("Exception = %s. chat_id=%s" % (e, chat_id_key))
