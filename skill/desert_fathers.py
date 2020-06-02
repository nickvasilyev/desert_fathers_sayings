import json
import random
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.utils import is_request_type, is_intent_name, get_slot_value
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model import Response
from ask_sdk_model.ui import SimpleCard
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from sayings import SAYINGS

try:
    with open('./desert_father_sayings_v2.json', 'r') as f:
        DESERT_FATHER_WISDOM = json.load(f)
except Exception as e:
    import os
    print(os.listdir('.'))
    raise e
# try:
#     DESERT_FATHER_WISDOM = SAYINGS
# except Exception as e:
#     import os
#     print(os.listdir('.'))
#     raise e

class LaunchRequestHandler(AbstractRequestHandler):
    PREFIX_SAYING = 'Saying Number {}. {}'
    def can_handle(self, handler_input):
        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input, **kwargs):
        print("LaunchRequestHandler", handler_input, kwargs)
        desert_father_saying = random.choice(DESERT_FATHER_WISDOM)
        saying_text = desert_father_saying['saying']
        if 'saying_ssml' in desert_father_saying:
            saying_text = desert_father_saying['saying_ssml']
        speech_text = self.PREFIX_SAYING.format(str(desert_father_saying['id']), saying_text)

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

class SayingByNumberRequestHandler(AbstractRequestHandler):
    PREFIX_SAYING = 'Saying Number {}. {}'
    def can_handle(self, handler_input):
        return is_intent_name("SayingByNumber")(handler_input)

    def handle(self, handler_input):
        print("SayingByNumberRequestHandler", handler_input)
        saying_number = int(get_slot_value(handler_input=handler_input, slot_name="saying_number"))
        print("SayingByNumberRequestHandler Saying Number ({})".format(saying_number))
        desert_father_saying = [x for x in DESERT_FATHER_WISDOM if x['id'] == saying_number][0]
        saying_text = desert_father_saying['saying']
        if 'saying_ssml' in desert_father_saying:
            saying_text = desert_father_saying['saying_ssml']
        speech_text = self.PREFIX_SAYING.format(str(desert_father_saying['id']), saying_text)

        handler_input.response_builder.speak(speech_text).set_should_end_session(True)
        return handler_input.response_builder.response

class SayingByTopicRequestHandler(AbstractRequestHandler):
    PREFIX_SAYING = 'Saying Number {}. {}'
    def can_handle(self, handler_input):
        return is_intent_name("SayingByTopic")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        print("SayingByTopic", handler_input)
        topic = get_slot_value(handler_input=handler_input, slot_name="topic")
        print("SayingByTopic about ({})".format(topic))
        desert_father_saying = random.choice([x for x in DESERT_FATHER_WISDOM if topic in x['tags']])
        saying_text = desert_father_saying['saying']
        if 'saying_ssml' in desert_father_saying:
            saying_text = desert_father_saying['saying_ssml']
        speech_text = self.PREFIX_SAYING.format(str(desert_father_saying['id']), saying_text)

        #handler_input.response_builder.speak(speech_text).set_card(SimpleCard("Desert Fathers Saying {}".format(desert_father_saying['id']), saying_text)).set_should_end_session(True) #Set this to true to see if this can be invoked from launch
        handler_input.response_builder.speak(speech_text).set_should_end_session(True) #Set this to true to see if this can be invoked from launch
        return handler_input.response_builder.response


class HelpIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "You can say hello to me!"

        handler_input.response_builder.speak(speech_text).ask(speech_text).set_card(
            SimpleCard("Hello World", speech_text))
        return handler_input.response_builder.response

class CancelAndStopIntentHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.CancelIntent")(handler_input) or is_intent_name("AMAZON.StopIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speech_text = "Goodbye! May God be with you!"

        handler_input.response_builder.speak(speech_text).set_card(
            SimpleCard("Hello World", speech_text)).set_should_end_session(True)
        return handler_input.response_builder.response

class SessionEndedRequestHandler(AbstractRequestHandler):
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        # any cleanup logic goes here

        return handler_input.response_builder.response

class AllExceptionHandler(AbstractExceptionHandler):

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        # Log the exception in CloudWatch Logs
        print(exception)

        speech = "Sorry, I didn't get it. Can you please say it again!!"
        handler_input.response_builder.speak(speech).ask(speech)
        return handler_input.response_builder.response

sb = SkillBuilder()
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(SayingByNumberRequestHandler())
sb.add_request_handler(SayingByTopicRequestHandler())

sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelAndStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_exception_handler(AllExceptionHandler())

handler = sb.lambda_handler()
