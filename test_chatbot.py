from niva_ai.chatbot import NivaChatbot
from niva_ai.language import detect_language, is_romanized_input

bot=NivaChatbot()
def ask(q,manual='Auto-detect'):
 return bot.reply(q,{},manual)

def test_english_short_query_models():
 a,l,_=ask('niva phone models');assert l=='en' and 'Niva Phone Lite' in a and 'Niva Phone Pro Max' in a

def test_english_smartwatch_models():
 a,l,_=ask('List all available Niva smartwatch models.');assert l=='en' and 'Niva Watch Fit' in a and 'Niva Watch Pro' in a and 'Available Smartwatches' in a

def test_telugu_return_policy_native():
 a,l,_=ask('మీ రిటర్న్ మరియు రీఫండ్ పాలసీ ఏమిటి?');assert l=='te' and 'రోజుల్లో' in a and '15' in a

def test_hindi_payments_native():
 a,l,_=ask('भुगतान के कौन-कौन से तरीके उपलब्ध हैं?');assert l=='hi' and 'UPI' in a and 'तरीके' in a

def test_tamil_payments_native():
 a,l,_=ask('என்னென்ன கட்டண முறைகள் உள்ளன?');assert l=='ta' and 'கட்டண' in a

def test_telugu_buds_product_native():
 a,l,_=ask('Niva Buds Air గురించి వివరించండి.');assert l=='te' and 'Niva Buds Air' in a and 'ధర' in a

def test_kannada_warranty_native():
 a,l,_=ask('Niva Phone Pro ವಾರಂಟಿ ಎಷ್ಟು?');assert l=='kn' and 'ವಾರಂಟಿ' in a and '₹24,999' not in a

def test_phone_category_models():
 a,l,_=ask('List all available Niva smartphone models.');assert l=='en' and 'Niva Phone Plus' in a

def test_product_details():
 a,l,_=ask('What is the price of Niva Phone Pro?');assert '₹24,999' in a

def test_language_detection_latin_is_english():
 assert detect_language('niva phone models')=='en'


def test_all_ten_language_detection():
 cases = [
  ('What is the price of Niva Phone Pro?', 'en'),
  ('Niva Phone Pro ధర ఎంత?', 'te'),
  ('Niva Phone Pro की कीमत कितनी है?', 'hi'),
  ('Niva Phone Pro விலை எவ்வளவு?', 'ta'),
  ('Niva Phone Pro ಬೆಲೆ ಎಷ್ಟು?', 'kn'),
  ('Niva Phone Pro വില എത്രയാണ്?', 'ml'),
  ('Niva Phone Pro-এর দাম কত?', 'bn'),
  ('Niva Phone Pro ची किंमत किती आहे?', 'mr'),
  ('Niva Phone Pro ની કિંમત કેટલી છે?', 'gu'),
  ('Niva Phone Pro ਦੀ ਕੀਮਤ ਕਿੰਨੀ ਹੈ?', 'pa'),
 ]
 for question, expected in cases:
  _, detected, _ = ask(question)
  assert detected == expected, (question, detected, expected)

def test_telugu_phone_models():
 a,l,_=ask('Niva ఫోన్ మోడల్స్ చూపించండి')
 assert l=='te' and 'Niva Phone Lite' in a and 'ఫోన్లు' in a

def test_tamil_watch_models():
 a,l,_=ask('Niva வாட்ச் மாடல்கள் பட்டியல்')
 assert l=='ta' and 'Niva Watch Fit' in a


def test_romanized_telugu_product_question():
 a,l,_=ask('Niva Buds Air gurinchi vivarinchandi')
 assert l=='te' and 'Niva Buds Air' in a and 'ధర' in a

def test_romanized_telugu_price_question():
 a,l,_=ask('Niva Phone Pro price entha')
 assert l=='te' and '₹24,999' in a and 'ధర' in a

def test_romanized_telugu_models_question():
 a,l,_=ask('Niva phone models chupinchandi')
 assert l=='te' and 'Niva Phone Lite' in a and 'ఫోన్లు' in a


def test_romanized_telugu_detection_and_response_mode():
 q = 'Niva Buds Air gurinchi cheppu'
 _, lang, _ = ask(q)
 assert lang == 'te'
 assert is_romanized_input(q, lang)

def test_native_hindi_input_keeps_native_script():
 answer, lang, _ = ask('रिटर्न पॉलिसी क्या है?')
 assert lang == 'hi'
 assert 'लौटाए' in answer
 assert not is_romanized_input('रिटर्न पॉलिसी क्या है?', lang)

def test_romanized_output_uses_indic_transliteration_when_installed():
 import pytest
 pytest.importorskip('indic_transliteration')
 answer, lang, _ = ask('Niva Buds Air gurinchi cheppu')
 assert lang == 'te'
 assert 'ధర' not in answer
 assert 'Niva Buds Air' in answer
