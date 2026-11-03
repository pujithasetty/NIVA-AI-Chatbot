from pathlib import Path
import base64, html
import streamlit as st
from niva_ai.chatbot import NivaChatbot
from niva_ai.language import SUPPORTED

ROOT=Path(__file__).parent
st.set_page_config(page_title='Niva AI | Every Language. Every Customer.',page_icon='🤖',layout='wide',initial_sidebar_state='expanded')
bot=NivaChatbot()
for k,v in {'messages':[],'context':{},'theme':'Dark','page':'Chat with Niva AI','manual_language':'Auto-detect'}.items():
 if k not in st.session_state:st.session_state[k]=v

def asset_b64(path):return base64.b64encode(Path(path).read_bytes()).decode()
background_b64=asset_b64(ROOT/'niva_ai'/'assets'/'chatbot_background.png')
def product_image(kind,model):
 slug=''.join(ch.lower() if ch.isalnum() else '_' for ch in model).strip('_')
 path=ROOT/'niva_ai'/'assets'/'products'/f'{slug}.svg'
 if not path.exists():path=ROOT/'niva_ai'/'assets'/'products'/f'{kind}.svg'
 return 'data:image/svg+xml;base64,'+asset_b64(path)
def render_product(p,cat):
 labels={'phones':'📱 Smartphone','watches':'⌚ Smartwatch','buds':'🎧 Audio'}
 image=product_image({'phones':'phone','watches':'watch','buds':'buds'}[cat],p['model'])
 price=f"₹{p['price']:,}"
 specs=[]
 for key in ('display','processor','battery','audio','anc','features','water_resistance'):
  if key in p:specs.append(p[key])
 specs=' · '.join(specs[:3])
 return f'<div class="product-card"><div class="product-art"><img style="filter:drop-shadow(0 16px 18px #000A)" src="{image}"/></div><div class="product-info"><div class="product-cat">{labels[cat]}</div><div class="product-name">{html.escape(p['model'])}</div><div class="product-price">{price}</div><div class="product-spec">{html.escape(specs)}</div><div class="product-stock">● {html.escape(p['availability'])}</div></div></div>'

with st.sidebar:
 logo=ROOT/'niva_ai'/'assets'/'niva_ai_logo.png'
 st.image(str(logo),use_container_width=True)
 st.markdown('<div class="side-tagline">Every Language. Every Customer.<br/>One Assistant.</div>',unsafe_allow_html=True)
 st.markdown('---')
 page=st.radio('NAVIGATION',['Chat with Niva AI','Our Products','Track Order','FAQs','Settings'],label_visibility='collapsed',key='page')
 st.markdown('<div class="side-promo"><b>Innovating a<br/>Smarter Tomorrow ✨</b><p>One assistant. Ten languages. Every customer.</p></div>',unsafe_allow_html=True)
 st.markdown('**🌐 Language Support**')
 st.caption('10 supported languages · Offline response templates')
 st.caption('Choose your response language in the chat area, or keep Auto-detect enabled.')
 st.markdown('---')
 if st.button('🗑️ Clear conversation',use_container_width=True):
  st.session_state.messages=[];st.session_state.context={};st.rerun()

# CSS palette sampled from the supplied reference image.
dark=st.session_state.theme=='Dark'
if dark:
 bg='#050D20';panel='#0B1731';panel2='#111E3D';text='#F4F7FF';muted='#B8C8E8';border='#263D70';user='#3215A5'
else:
 bg='#F4F7FF';panel='#FFFFFF';panel2='#EAF0FF';text='#10234A';muted='#536582';border='#CCD9F4';user='#E6E1FF'
st.markdown(f'''<style>
:root{{--niva-cyan:#08D5D2;--niva-blue:#147FEA;--niva-purple:#7735F2;}}
.stApp{{background:linear-gradient(135deg,rgba(4,10,32,.90),rgba(7,18,53,.84) 48%,rgba(20,10,52,.90)),url('data:image/png;base64,{background_b64}') center/cover fixed no-repeat;color:{text};}}
.main .block-container{{position:relative;}}
.main .block-container:before{{content:'';position:fixed;inset:0;pointer-events:none;opacity:.22;background-image:radial-gradient(#7DEBFF 1px,transparent 1px),linear-gradient(120deg,transparent 0 46%,#8C59FF12 46.2% 46.5%,transparent 46.7%);background-size:34px 34px,100% 100%;z-index:0;}}
.main .block-container:after{{content:'✦  N I V A  A I  ✦';position:fixed;right:3.5%;bottom:3%;pointer-events:none;color:#B9D9FF20;font-size:clamp(18px,3vw,34px);font-weight:800;letter-spacing:5px;z-index:0;}}
[data-testid="stHeader"]{{background:transparent;}}
[data-testid="stSidebar"]{{background:linear-gradient(180deg,#06122B,#0A1632 65%,#11174A);border-right:1px solid #1B3D70;}}
[data-testid="stSidebar"] *{{color:#EEF4FF!important;}}
.stApp, .stApp p,.stApp label,.stApp h1,.stApp h2,.stApp h3,.stApp span,.stApp div{{color:inherit;}}
.stApp p,.stApp label{{color:{text};}}
.niva-hero{{position:relative;overflow:hidden;background:linear-gradient(105deg,#17258BEE 0%,#071A48E8 48%,#063A65E8 100%);border:1px solid #27C9E8;border-radius:26px;padding:28px 32px;margin:5px 0 22px;box-shadow:0 18px 45px #02081788,0 0 32px #05CDE538;}}
.niva-hero:after{{content:'✧';position:absolute;right:5%;top:-38px;font-size:170px;color:#78E9FF18;transform:rotate(15deg);pointer-events:none;}}
.niva-hero h1{{font-size:34px!important;color:#fff!important;margin:0 0 6px!important;}}
.niva-hero p{{color:#E8F6FF!important;margin:3px 0!important;}}
.hero-kicker{{font-size:14px;color:#72E9F4!important;letter-spacing:1px;text-transform:uppercase;}}
.chat-user{{background:linear-gradient(110deg,#3713A8,#4A22D2);color:#fff;border:1px solid #7B42FF;border-radius:19px 19px 5px 19px;padding:14px 18px;margin:12px 0 12px auto;max-width:78%;box-shadow:0 0 18px #7735F233;}}
.chat-bot{{background:linear-gradient(130deg,{panel2},{panel});color:{text};border:1px solid {border};border-radius:6px 19px 19px 19px;padding:15px 18px;margin:12px 0;max-width:88%;box-shadow:0 8px 24px #0003;white-space:pre-wrap;}}
.product-card{{display:flex;flex-direction:column;overflow:hidden;border:1px solid #318ACB;border-radius:23px;background:linear-gradient(145deg,#172C59 0%,#0A1733 52%,#24164D 100%);box-shadow:0 15px 35px #0005,0 0 20px #08CDEB20;min-height:360px;transition:transform .25s,box-shadow .25s;}}
.product-card:hover{{transform:translateY(-5px);box-shadow:0 20px 42px #0007,0 0 25px #08CDEB35;}}
.product-art{{height:225px;background:radial-gradient(ellipse at 50% 55%,#176A9D88 0%,#15265D 43%,#11152F 78%);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden;}}
.product-art:before{{content:'';position:absolute;width:170px;height:170px;border:1px solid #8AEAFF44;border-radius:50%;box-shadow:0 0 0 18px #8AEAFF0A,0 0 0 38px #8AEAFF08;}}
.product-art img{{width:100%;height:225px;object-fit:contain;position:relative;filter:drop-shadow(0 16px 18px #000A);transition:transform .35s ease;}}
.product-card:hover .product-art img{{transform:scale(1.055) translateY(-3px);}}
.product-info{{padding:15px 17px 18px;}}
.product-cat{{color:#61E5F4;font-size:12px;text-transform:uppercase;letter-spacing:1px;}}
.product-name{{color:#F6F8FF;font-size:20px;font-weight:750;margin:5px 0;}}
.product-price{{color:#55E9F2;font-size:23px;font-weight:800;}}
.product-spec{{color:#C5D4F3;font-size:12px;min-height:38px;margin:8px 0;}}
.product-stock{{color:#4DE0B0;font-size:12px;font-weight:700;}}
.side-tagline{{text-align:center;color:#DCEBFF;font-size:13px;margin-top:-8px;line-height:1.5;}}
.side-promo{{padding:18px;border:1px solid #3144A7;border-radius:18px;background:linear-gradient(135deg,#122F8B,#11194C);margin:15px 0;}}
.side-promo b{{font-size:19px;color:white!important;}}.side-promo p{{color:#BFD9FF!important;font-size:12px;}}
.metric-card{{padding:16px;border:1px solid #1D6CB5;border-radius:16px;background:linear-gradient(130deg,#12245A,#111833);}}
.stButton button{{border-radius:13px!important;border:1px solid #357FEA!important;background:linear-gradient(100deg,#123DAB,#6334DC)!important;color:#fff!important;font-weight:700!important;}}
.stTextInput input,.stTextArea textarea,[data-testid="stChatInput"] textarea{{background:{panel2}!important;color:{text}!important;border:1px solid #4260A0!important;}}
[data-testid="stChatInput"]{{border-color:#713BEB!important;}}
[data-testid="stChatInput"] textarea::placeholder{{color:{muted}!important;}}
[data-testid="stSelectbox"] div,[data-testid="stRadio"] label{{color:{text}!important;}}
hr{{border-color:{border}!important;}}
.small-muted{{color:{muted}!important;font-size:12px;}}
</style>''',unsafe_allow_html=True)

# Header
st.markdown('''<div class="niva-hero"><div class="hero-kicker">✦ Your multilingual customer-care companion</div><h1>👋 Hello! I’m <span style="color:#08D5D2">Niva AI</span></h1><p>Your smart customer support assistant.</p><p>Ask me anything about Niva Phones, Watches, or Buds in your preferred language.</p><p style="font-size:12px;color:#80DDFB!important;margin-top:12px">“Every Language. Every Customer. One Assistant.”</p></div>''',unsafe_allow_html=True)

if page=='Chat with Niva AI':
 c1,c2,c3=st.columns(3)
 for col,(emoji,label,val) in zip((c1,c2,c3),[('📱','Phone models','4'),('⌚','Watch models','3'),('🎧','Buds models','3')]):
  with col:st.markdown(f'<div class="metric-card"><div style="font-size:13px;color:#9FB7E8">{emoji} {label}</div><div style="font-size:25px;font-weight:800;color:#fff">{val}</div></div>',unsafe_allow_html=True)
 st.markdown('')
 st.markdown('### 🌐 Choose your response language')
 language_options=['Auto-detect']+list(SUPPORTED.values())
 st.selectbox('Choose language',language_options,key='manual_language',label_visibility='collapsed',help='Select a language to receive answers in it, or choose Auto-detect.')
 st.caption('You can type in the selected language’s native script or in English letters (Romanized text), for example: “Niva Buds Air gurinchi vivarinchandi”.')
 for item in st.session_state.messages:
  if item['role']=='user':st.markdown(f'<div class="chat-user">👤 {html.escape(item["content"])}</div>',unsafe_allow_html=True)
  else:st.markdown(f'<div class="chat-bot">🤖 <b>Niva AI</b><br/>{html.escape(item["content"]).replace(chr(10),"<br/>")}</div>',unsafe_allow_html=True)
 prompt=st.chat_input('Type your question in any supported language...')
 if prompt:
  st.session_state.messages.append({'role':'user','content':prompt})
  answer,lang,ctx=bot.reply(prompt,st.session_state.context,st.session_state.manual_language)
  st.session_state.context=ctx
  st.session_state.messages.append({'role':'assistant','content':answer})
  st.rerun()
 st.caption('🌐 Powered by multilingual NLP · 10 languages · Native-script and Romanized questions supported · Product facts from the local Niva catalogue ❤️')
elif page=='Our Products':
 st.subheader('🛍️ Explore the Niva Collection')
 st.caption('Choose a category and explore every available model, specification and price.')
 category=st.tabs(['📱 Phones','⌚ Watches','🎧 Buds'])
 for tab,cat in zip(category,['phones','watches','buds']):
  with tab:
   products=bot.products(cat)
   cols=st.columns(2)
   for i,p in enumerate(products):
    with cols[i%2]:
     st.markdown(render_product(p,cat),unsafe_allow_html=True)
     with st.expander(f'View {p["model"]} specifications'):
      st.write(f'**Price:** ₹{p["price"]:,}')
      for k,v in p.items():
       if k not in ('model','price'):
        st.write(f'**{k.replace("_"," ").title()}:** {", ".join(v) if isinstance(v,list) else v}')
elif page=='Track Order':
 st.subheader('🚚 Track your Niva order')
 order_id=st.text_input('Enter sample order ID',placeholder='e.g. NIVA1001')
 if st.button('Track order'):
  answer,lang,ctx=bot.reply('track '+order_id,{},'English')
  st.info(answer)
 st.caption('Academic demo only: NIVA1001, NIVA1002 and NIVA1003 are sample orders.')
elif page=='FAQs':
 st.subheader('💡 Frequently asked questions')
 for q,a in [('What products does Niva offer?','Niva offers Phones, Smartwatches and Wireless Buds.'),('What is the warranty?','All Niva products include a 1-year limited manufacturer warranty.'),('What is the return window?','Eligible unused products can be returned within 15 days of delivery.'),('How long do refunds take?','Approved refunds are processed within 5–7 business days.'),('Which languages are supported?','English, Telugu, Hindi, Tamil, Kannada, Malayalam, Bengali, Marathi, Gujarati and Punjabi.')]:
  with st.expander(q):st.write(a)
elif page=='Settings':
 st.subheader('⚙️ Appearance & preferences')
 st.radio('Appearance',['Dark','Light'],horizontal=True,key='theme')
 st.caption('Dark mode uses deep navy surfaces with cyan, electric-blue and violet accents. Light mode uses high-contrast text for readability.')
 st.write('Preferred response language:', st.session_state.manual_language)
 st.caption('The chat language selector is also available above the conversation. Romanized queries such as Telugu typed with English letters are supported for common product questions.')
 st.success('Language detection is performed locally. Translation services are not required for product answers.')

st.markdown('<div style="text-align:center;color:#92A9D2;font-size:12px;padding:25px 0 5px">Niva AI · Every Language. Every Customer. One Assistant. 💙<br/>Fictional product catalogue for academic demonstration.</div>',unsafe_allow_html=True)
