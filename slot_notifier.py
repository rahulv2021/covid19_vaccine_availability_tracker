import telegram
import telegram_config
from decorators import retry


class SlotNotifier:
    message_counter = 0

    def _get_chat_id(self, age_limit, vaccine, state, dose):
        chat_id_key = "%s_%s_%s_%s" % (
            age_limit, vaccine.lower(), state.lower(), dose)
        if chat_id_key not in telegram_config.chat_ids:
            raise Exception(
                "Invalid chat id %s. Please ensure the channel is added in config" % (chat_id_key))
        return chat_id_key

    @retry(Exception, max_retries=7, delay=6, backoff=2)
    def send_message(self, age_limit, vaccine, state, message, dose):
        bot = self._get_bot()
        if 'sputnik' in vaccine.lower():
            vaccine = "sputnik"  # don't know the exact name cowin are using
        chat_id_key = self._get_chat_id(age_limit, vaccine, state, dose)
        chat_id = telegram_config.chat_ids[chat_id_key]
        try:
            # print "Sending message for chat_id %s" %(chat_id_key)
            bot.sendMessage(
                chat_id=chat_id, text=message, parse_mode="html")
            SlotNotifier.message_counter += 1
            SlotNotifier.message_counter %= 100  # to not extend counter forever
        except Exception as e:
            raise Exception("Exception = %s. chat_id=%s" % (e, chat_id_key))

    def _get_token_from_config(self):
        all_tokens = telegram_config.bot_tokens
        token_index = SlotNotifier.message_counter % len(all_tokens)
        token = all_tokens[token_index]  # pick tokens based on the token_number generated to avoid hitting api limits
        return token

    def _get_bot(self):
        token = self._get_token_from_config()
        bot = telegram.Bot(token=token)
        return bot
