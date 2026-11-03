"""Deterministic multilingual detection for ten supported Indian/English languages.
Indic-script detection is offline and avoids unreliable short-text language guesses."""
import unicodedata
SUPPORTED={"en":"English","te":"తెలుగు","hi":"हिन्दी","ta":"தமிழ்","kn":"ಕನ್ನಡ","ml":"മലയാളം","bn":"বাংলা","mr":"मराठी","gu":"ગુજરાતી","pa":"ਪੰਜਾਬੀ"}
SCRIPT_RANGES={"te":(0x0C00,0x0C7F),"hi":(0x0900,0x097F),"ta":(0x0B80,0x0BFF),"kn":(0x0C80,0x0CFF),"ml":(0x0D00,0x0D7F),"bn":(0x0980,0x09FF),"mr":(0x0900,0x097F),"gu":(0x0A80,0x0AFF),"pa":(0x0A00,0x0A7F)}
ROMANIZED_MARKERS={
 "te":("gurunchi","gurinchi","gurिंchi","vivarinchandi","vivarinchu","cheppandi","cheppu","cheppu","entha","dhara","velu","andubatulo","modelu","modals","chupinchandi","chupinchu","kavali","emi","ela undhi","ela undi","bagundha","bagundi","niva buds air gurinchi","unnayi","undha","undi","chesukovali","return policy enti","policy enti","cheppava","ivvu"),
 "hi":("ke bare mein","ke baare mein","bataiye","bataye","batao","kya hai","kya h","kitna hai","kitne ka","kimat","keemat","daam","kaise hai","mujhe batao","phone ki","return policy"),
 "ta":("patri sollungal","vilai evvalavu","enna vilai","eppadi irukku","vivarangal","enna","sollunga","enna seivathu"),
 "kn":("bagge heli","bagge heli","bele eshtu","hege ide","vivarisi","enu","heli","yestu"),
 "ml":("kurichu parayoo","vila ethraya","engane undu","vivarikkuka","enthaanu","parayamo"),
 "bn":("somproke bolun","dam koto","kemon ache","ki bhabe","bolun"),
 "mr":("baddal sanga","kimat kiti","kase aahe","kay aahe","sanga"),
 "gu":("vishe janavo","kimat ketli","kevu che","shu che","janavo"),
 "pa":("bare dasso","keemat kinni","kiven hai","ki hai","dasso")}
def detect_language(text, manual="Auto-detect"):
    if manual and manual!="Auto-detect":
        for code,name in SUPPORTED.items():
            if name==manual: return code
    latin=str(text).casefold()
    roman_hits={code:sum(1 for marker in markers if marker in latin) for code,markers in ROMANIZED_MARKERS.items()}
    best_roman=max(roman_hits,key=roman_hits.get)
    if roman_hits[best_roman]: return best_roman
    counts={k:0 for k in SCRIPT_RANGES}
    for ch in text:
        n=ord(ch)
        for code,(lo,hi) in SCRIPT_RANGES.items():
            if lo<=n<=hi: counts[code]+=1
    if not any(counts.values()): return "en" if any(c.isalpha() for c in text) else "unknown"
    # Hindi and Marathi share Devanagari; distinguish common Marathi-specific words.
    if counts["hi"]:
        q=text.casefold()
        marathi_markers=("आहे","माझे","किंमत","कृपया","माहिती","किती","करा","तुमची")
        return "mr" if any(x in q for x in marathi_markers) else "hi"
    return max(counts,key=counts.get)


# True when the user wrote an Indian language using Latin characters.
def is_romanized_input(text, lang):
    if lang == "en":
        return False
    letters = [c for c in str(text) if c.isalpha()]
    return bool(letters) and all(ord(c) < 128 for c in letters)
