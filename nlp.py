"""Offline multilingual NLP: normalization, script-aware tokenization, intent scoring,
product entity linking, feature extraction, typo tolerance and conversational context."""
import re, unicodedata
from rapidfuzz import fuzz, process
from .language import detect_language

CATEGORY_WORDS={
"phones":{"en":["phone","phones","mobile","smartphone","mobiles"],"te":["ఫోన్","ఫోన్లు","మొబైల్","phone","phones","mobile"],"hi":["फोन","मोबाइल"],"ta":["போன்","தொலைபேசி"],"kn":["ಫೋನ್","ಮೊಬೈಲ್"],"ml":["ഫോൺ","മൊബൈൽ"],"bn":["ফোন","মোবাইল"],"mr":["फोन","मोबाईल"],"gu":["ફોન","મોબાઇલ"],"pa":["ਫੋਨ","ਮੋਬਾਈਲ"]},
"watches":{"en":["watch","watches","smartwatch"],"te":["వాచ్","వాచెస్","స్మార్ట్ వాచ్","watch","watches"],"hi":["घड़ी","वॉच","स्मार्टवॉच"],"ta":["வாட்ச்","கடிகாரம்"],"kn":["ವಾಚ್","ಗಡಿಯಾರ"],"ml":["വാച്ച്","ഘടികാരം"],"bn":["ঘড়ি","ওয়াচ"],"mr":["घड्याळ","वॉच"],"gu":["ઘડિયાળ","વોચ"],"pa":["ਘੜੀ","ਵਾਚ"]},
"buds":{"en":["buds","earbuds","earphones","headphones"],"te":["బడ్స్","ఇయర్ బడ్స్","హెడ్‌ఫోన్స్","buds","earbuds"],"hi":["ईयरबड्स","बड्स","हेडफोन"],"ta":["இயர்பட்ஸ்","பட்ஸ்","ஹெட்போன்"],"kn":["ಇಯರ್‌ಬಡ್ಸ್","ಬಡ್ಸ್","ಹೆಡ್‌ಫೋನ್"],"ml":["ഇയർബഡ്സ്","ബഡ്സ്","ഹെഡ്ഫോൺ"],"bn":["ইয়ারবাডস","বাডস","হেডফোন"],"mr":["इयरबड्स","बड्स","हेडफोन"],"gu":["ઇયરબડ્સ","બડ્સ","હેડફોન"],"pa":["ਈਅਰਬਡਸ","ਬਡਸ","ਹੈੱਡਫੋਨ"]}}
INTENT_WORDS={
"models":{"en":["models","model list","list all","show all","which models","available models","product range"],"te":["మోడల్స్","మోడళ్లు","జాబితా","అన్ని చూపించు","ఏ మోడల్స్","models","modelu","modals","chupinchandi"],"hi":["मॉडल","मॉडल्स","सूची","सभी दिखाएं","कौन से मॉडल"],"ta":["மாடல்கள்","பட்டியல்","அனைத்தையும் காட்டு"],"kn":["ಮಾದರಿಗಳು","ಪಟ್ಟಿ","ಎಲ್ಲವನ್ನೂ ತೋರಿಸಿ"],"ml":["മോഡലുകൾ","പട്ടിക","എല്ലാം കാണിക്കുക"],"bn":["মডেল","তালিকা","সব দেখান"],"mr":["मॉडेल","यादी","सर्व दाखवा"],"gu":["મોડલ","યાદી","બધા બતાવો"],"pa":["ਮਾਡਲ","ਸੂਚੀ","ਸਾਰੇ ਦਿਖਾਓ"]},
"price":{"en":["price","cost","how much","rate"],"te":["ధర","ఎంత","dhara","entha","velu"],"hi":["कीमत","दाम","कितने"],"ta":["விலை","எவ்வளவு"],"kn":["ಬೆಲೆ","ಎಷ್ಟು"],"ml":["വില","എത്ര"],"bn":["দাম","মূল্য","কত"],"mr":["किंमत","किती"],"gu":["કિંમત","કેટલી"],"pa":["ਕੀਮਤ","ਕਿੰਨੀ"]},
"warranty":{"en":["warranty","guarantee"],"te":["వారంటీ","గ్యారంటీ","warranty","garantee"],"hi":["वारंटी","गारंटी"],"ta":["உத்தரவாதம்","வாரண்டி"],"kn":["ವಾರಂಟಿ","ಖಾತರಿ"],"ml":["വാറന്റി","ഗ്യാരണ്ടി"],"bn":["ওয়ারেন্টি","গ্যারান্টি"],"mr":["वॉरंटी","हमी"],"gu":["વોરંટી","ખાતરી"],"pa":["ਵਾਰੰਟੀ","ਗਾਰੰਟੀ"]},
"availability":{"en":["available","availability","stock","in stock"],"te":["అందుబాటులో","స్టాక్","andubatulo","stock"],"hi":["उपलब्ध","स्टॉक"],"ta":["கிடைக்குமா","இருக்கிறதா","கையிருப்பு"],"kn":["ಲಭ್ಯವಿದೆಯೇ","ಲಭ್ಯ","ಸ್ಟಾಕ್"],"ml":["ലഭ്യമാണോ","ലഭ്യം","സ്റ്റോക്ക്"],"bn":["পাওয়া যায়","উপলব্ধ","স্টক"],"mr":["उपलब्ध","साठा"],"gu":["ઉપલબ્ધ","સ્ટોક"],"pa":["ਉਪਲਬਧ","ਸਟਾਕ"]},
"battery":{"en":["battery","backup"],"te":["బ్యాటరీ","బ్యాకప్","battery","backup"],"hi":["बैटरी","बैकअप"],"ta":["பேட்டரி","பேக்கப்"],"kn":["ಬ್ಯಾಟರಿ","ಬ್ಯಾಕಪ್"],"ml":["ബാറ്ററി","ബാക്കപ്പ്"],"bn":["ব্যাটারি","ব্যাকআপ"],"mr":["बॅटरी","बॅकअप"],"gu":["બેટરી","બેકઅપ"],"pa":["ਬੈਟਰੀ","ਬੈਕਅੱਪ"]},
"returns":{"en":["return","returns","exchange"],"te":["రిటర్న్","తిరిగి"],"hi":["रिटर्न","वापस"],"ta":["திரும்ப","ரிட்டர்ன்"],"kn":["ಹಿಂತಿರುಗಿ","ರಿಟರ್ನ್"],"ml":["തിരികെ","റിട്ടേൺ"],"bn":["ফেরত","রিটার্ন"],"mr":["परत","रिटर्न"],"gu":["પરત","રિટર્ન"],"pa":["ਵਾਪਸ","ਰਿਟਰਨ"]},
"refunds":{"en":["refund","money back"],"te":["రీఫండ్","డబ్బు తిరిగి"],"hi":["रिफंड","पैसे वापस"],"ta":["பணத்தைத் திரும்ப","ரீஃபண்ட்"],"kn":["ಮರುಪಾವತಿ","ರಿಫಂಡ್"],"ml":["റീഫണ്ട്","പണം തിരികെ"],"bn":["রিফান্ড","টাকা ফেরত"],"mr":["परतावा","रिफंड"],"gu":["રિફંડ","પૈસા પાછા"],"pa":["ਰਿਫੰਡ","ਪੈਸੇ ਵਾਪਸ"]},
"payments":{"en":["payment","payments","pay","upi","cash on delivery"],"te":["చెల్లింపు","చెల్లింపులు","పేమెంట్"],"hi":["भुगतान","पेमेंट"],"ta":["கட்டணம்","கட்டண","பணம் செலுத்த"],"kn":["ಪಾವತಿ","ಹಣ ಪಾವತಿ"],"ml":["പേയ്മെന്റ്","പണമടയ്ക്കൽ"],"bn":["পেমেন্ট","অর্থপ্রদান"],"mr":["पेमेंट","भरणा"],"gu":["ચુકવણી","પેમેન્ટ"],"pa":["ਭੁਗਤਾਨ","ਪੇਮੈਂਟ"]},
"tracking":{"en":["track","tracking","order status"],"te":["ట్రాక్","ఆర్డర్ స్థితి"],"hi":["ट्रैक","ऑर्डर स्थिति"],"ta":["கண்காணி","ஆர்டர் நிலை"],"kn":["ಟ್ರ್ಯಾಕ್","ಆರ್ಡರ್ ಸ್ಥಿತಿ"],"ml":["ട്രാക്ക്","ഓർഡർ നില"],"bn":["ট্র্যাক","অর্ডারের অবস্থা"],"mr":["ट्रॅक","ऑर्डर स्थिती"],"gu":["ટ્રેક","ઓર્ડરની સ્થિતિ"],"pa":["ਟਰੈਕ","ਆਰਡਰ ਸਥਿਤੀ"]},
"greeting":{"en":["hello","hi","hey","good morning","good evening"],"te":["నమస్కారం","హాయ్","హలో"],"hi":["नमस्ते","हैलो","नमस्कार"],"ta":["வணக்கம்","ஹலோ"],"kn":["ನಮಸ್ಕಾರ","ಹಾಯ್"],"ml":["നമസ്കാരം","ഹായ്"],"bn":["নমস্কার","হ্যালো"],"mr":["नमस्कार","हाय"],"gu":["નમસ્તે","હાય"],"pa":["ਸਤ ਸ੍ਰੀ ਅਕਾਲ","ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ","ਹੈਲੋ"]},
"help":{"en":["help","what can you do","support"],"te":["సహాయం","ఏమి చేయగలవు"],"hi":["मदद","सहायता"],"ta":["உதவி","என்ன செய்ய முடியும்"],"kn":["ಸಹಾಯ","ಏನು ಮಾಡಬಹುದು"],"ml":["സഹായം","എന്ത് ചെയ്യാം"],"bn":["সাহায্য","কি করতে পারেন"],"mr":["मदत","सहाय्य"],"gu":["મદદ","શું કરી શકો"],"pa":["ਮਦਦ","ਸਹਾਇਤਾ"]}}
FEATURE_WORDS={"display":{"en":["display","screen"],"te":["డిస్ప్లే","స్క్రీన్","display","screen"],"hi":["डिस्प्ले","स्क्रीन"],"ta":["திரை","டிஸ்ப்ளே"],"kn":["ಡಿಸ್ಪ್ಲೇ","ಪರದೆ"],"ml":["ഡിസ്‌പ്ലേ","സ്ക്രീൻ"],"bn":["ডিসপ্লে","স্ক্রিন"],"mr":["डिस्प्ले","स्क्रीन"],"gu":["ડિસ્પ્લે","સ્ક્રીન"],"pa":["ਡਿਸਪਲੇ","ਸਕ੍ਰੀਨ"]},"camera":{"en":["camera","photo"],"te":["కెమెరా","camera"],"hi":["कैमरा"],"ta":["கேமரா"],"kn":["ಕ್ಯಾಮೆರಾ"],"ml":["ക്യാമറ"],"bn":["ক্যামেরা"],"mr":["कॅमेरा"],"gu":["કેમેરા"],"pa":["ਕੈਮਰਾ"]},"anc":{"en":["anc","noise cancellation"],"te":["నాయిస్ క్యాన్సిలేషన్","noise cancellation"],"hi":["नॉइज़ कैंसलेशन"],"ta":["நாய்ஸ் கேன்சலேஷன்"],"kn":["ನಾಯ್ಸ್ ಕ್ಯಾನ್ಸಲೇಶನ್"],"ml":["നോയിസ് ക്യാൻസലേഷൻ"],"bn":["নয়েজ ক্যানসেলেশন"],"mr":["नॉईज कॅन्सलेशन"],"gu":["નોઇઝ કેન્સલેશન"],"pa":["ਨੌਇਜ਼ ਕੈਂਸਲੇਸ਼ਨ"]}}

def normalize(text):
    text=unicodedata.normalize('NFKC',str(text)).casefold()
    text=re.sub(r'[\u200b-\u200f\ufeff]','',text)
    text=''.join(ch if (ch.isalnum() or ch.isspace() or unicodedata.category(ch).startswith('M') or ch in './-') else ' ' for ch in text)
    return re.sub(r'\s+',' ',text).strip()
def tokenize(text): return re.findall(r'\w+',normalize(text),flags=re.UNICODE)
def _has_any(q,terms):
    return any((re.search(r"\b"+re.escape(t.casefold())+r"\b",q) is not None) if len(t.strip())<=3 and t.isascii() else t.casefold() in q for t in terms)
def classify_intent(text,lang='en'):
    q=normalize(text)
    if lang=='te' and any(x in q for x in ('gurinchi','vivarinchandi','vivarinchu','cheppandi','cheppu')):
        return 'product_info'
    # Longest/high-priority semantic intents first.
    for intent in ('tracking','refunds','returns','warranty','payments','models','availability','battery','price','greeting','help'):
        terms=INTENT_WORDS.get(intent,{}).get(lang,[])+INTENT_WORDS.get(intent,{}).get('en',[])
        if _has_any(q,terms): return intent
    return 'product_info' if identify_category(text,lang) else 'unknown'
def identify_category(text,lang='en',previous=None):
    q=normalize(text)
    for cat,by_lang in CATEGORY_WORDS.items():
        terms=by_lang.get(lang,[])+by_lang['en']
        if _has_any(q,terms): return cat
    return previous

def identify_model(text,catalog,previous=None):
    q=normalize(text)
    models=[p['model'] for group in catalog['products'].values() for p in group]
    for model in models:
        if normalize(model) in q: return model
    # Match model suffixes such as “Pro Max” when the brand/category is implied.
    aliases={'lite':'Lite','plus':'Plus','pro max':'Pro Max','active':'Active','fit':'Fit','air':'Air','go':'Go'}
    for alias,suffix in aliases.items():
        if re.search(r'\b'+re.escape(alias)+r'\b',q):
            candidates=[m for m in models if m.endswith(suffix)]
            if len(candidates)==1:return candidates[0]
    match=process.extractOne(q,models,scorer=fuzz.token_set_ratio)
    if match and match[1]>=86:return match[0]
    if previous and any(x in q for x in ['it','its','that','this','దాని','దాని','उसका','அதன்','ಅದರ']):return previous
    return None
def identify_feature(text,lang='en'):
    q=normalize(text)
    for feature,by_lang in FEATURE_WORDS.items():
        if _has_any(q,by_lang.get(lang,[])+by_lang['en']):return feature
    return None
def extract_order_id(text):
    m=re.search(r'\bNIVA\d{4}\b',str(text).upper()); return m.group(0) if m else None
