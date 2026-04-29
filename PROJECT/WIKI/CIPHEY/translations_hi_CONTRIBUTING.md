<p align="center">
अनुवाद <br>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/de/CONTRIBUTING.md>🇩🇪 DE   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/CONTRIBUTING.md>🇬🇧 EN   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/fr/CONTRIBUTING.md>🇫🇷 FR   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/hu/CONTRIBUTING.md>🇭🇺 HU   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/hi/CONTRIBUTING.md>🇮🇳 HI   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/id/CONTRIBUTING.md>🇮🇩 ID   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/it/CONTRIBUTING.md>🇮🇹 IT   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/nl/CONTRIBUTING.md>🇳🇱 NL   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/pt-br/CONTRIBUTING.md>🇧🇷 PT-BR   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/ru/CONTRIBUTING.md>🇷🇺 RU   </a>
<a href="https://github.com/Ciphey/Ciphey/tree/master/translations/th/CONTRIBUTING.md">🇹🇭 TH   </a>
<a href=https://github.com/Ciphey/Ciphey/tree/master/translations/zh/CONTRIBUTING.md>🇨🇳 ZH   </a>
</p>

हैलो!

तो आप Ciphey में योगदान में रुचि रखते हैं? 🤔

लेकिन हो सकता है आप इस बारे में परेशान हों कि कहाँ से शुरुआत करें, या आप सोचते हों कि आपके कोडिंग कौशल "पर्याप्त अच्छे" नहीं हैं। अच्छा, बाद वाला - हास्यास्पद है! हम "खराब कोड" के साथ बिल्कुल ठीक हैं, और वैसे भी, यदि आपने इस दस्तावेज़ को पढ़ा है, तो आप शायद एक बेहतरीन प्रोग्रामर हैं। मेरा मतलब है, शुरुआती अक्सर GitHub परियोजनाओं में योगदान नहीं देते 😉

यहाँ कुछ तरीके हैं जिनसे आप Ciphey में योगदान दे सकते हैं:

- इसे नई भाषा में अनुवादित करें 🧏
- अधिक एन्क्रिप्शन प्रारूप जोड़ें 📚
- और दस्तावेज़ीकरण बनाएं (बहुत महत्वपूर्ण‼️ हम हमेशा के लिए आभारी होंगे)
- GitHub Issues में बग्स को ठीक करें (हम इसमें आपकी मदद करेंगे 😊)
- कोडबेस को रिफैक्टर करें 🥺

यदि ये कठिन लगते हैं, तो चिंता न करें! यह दस्तावेज़ ठीक-ठीक दिखाता है कि इन्हें कैसे प्राप्त करना है। और भी बहुत कुछ .... आपका नाम Ciphey योगदानकर्ताओं की सूची में जाएगा, और हम हमेशा के लिए आभारी होंगे! 🙏

हमारे पास एक छोटा Discord server है जहाँ आप डेवलपर्स से चैट कर सकते हैं और सहायता प्राप्त कर सकते हैं। वैकल्पिक रूप से, अपने सुझाव के लिए एक GitHub-Issue लिखें। यदि आप Discord में शामिल होना चाहते हैं:

[Discord Server](https://discord.gg/KfyRUWw)

# कैसे योगदान दें

Ciphey को हमेशा अधिक डिकोडिंग टूल्स की आवश्यकता होती है! यदि आप जानना चाहते हैं कि एन्क्रिप्शन में कोड को कैसे एकीकृत करना है, तो इन्हें देखें:

- <https://github.com/Ciphey/Ciphey/wiki/Adding-your-own-ciphers> सरल उदाहरण
- <https://github.com/Ciphey/Ciphey/wiki/Extending-Ciphey> API संदर्भ

यह अच्छा होगा यदि आप इसके लिए कुछ टेस्ट लिख सकें, बस Ciphey/tests/test_main.py फ़ाइल में एक function कॉपी करें, और ciphertext को अपने एन्क्रिप्शन के साथ एन्कोड किए गए किसी चीज़ से बदलें। यदि आप टेस्ट नहीं जोड़ते हैं, तो हम शायद अभी भी कोड को मर्ज कर देंगे, लेकिन बग्स का निदान करना कहीं अधिक कठिन होगा!

यह कहे बिना भी स्पष्ट है कि हम आपको आपकी मेहनत के लिए योगदानकर्ताओं की सूची में जोड़ेंगे!

# एक नई भाषा जोड़ें 🧏

डिफ़ॉल्ट भाषा चेकर, `brandon`, कई भाषाओं के साथ काम करता है। यह डरावना लग सकता है।
लेकिन ईमानदारी से, आपको बस एक शब्दकोश लेना है, थोड़ा विश्लेषण करना है (जिसके लिए हमारे पास सहायक कोड है), फिर शब्दकोश और विश्लेषण को एक रेपो में जोड़ना है। फिर आप `settings.yml` फ़ाइल में भाषा जोड़ते हैं।

# और दस्तावेज़ीकरण बनाएं

दस्तावेज़ीकरण Ciphey का सबसे महत्वपूर्ण हिस्सा है। जितना अधिक दस्तावेज़ीकरण, उतना अच्छा।

और मुझ पर भरोसा करें जब मैं कहता हूँ कि यदि आप महान दस्तावेज़ीकरण में योगदान देते हैं, तो आप कोड योगदानकर्ताओं के समान स्तर पर दिखाई देंगे। दस्तावेज़ीकरण आवश्यक है।

आप कई तरीकों से दस्तावेज़ीकरण में योगदान दे सकते हैं।

- कोड में docstrings जोड़ना
- वर्तमान दस्तावेज़ीकरण में सुधार (README, यह फ़ाइल, हमारी Read The Docs साइट)
- दस्तावेज़ीकरण का अनुवाद

और भी बहुत कुछ!

# बग्स को ठीक करें

हमारे GitHub-Issues पृष्ठ पर जाएं जहाँ आपको Ciphey की सभी समस्याएँ मिलेंगी! उन्हें ठीक करें और आप योगदानकर्ताओं की सूची में आ जाएंगे ;)

# कोडबेस को रिफैक्टर करें


Ciphey के सभी हिस्से PEP8 दिशानिर्देशों का पालन नहीं करते, और बहुत सारे दोहराए गए कोड हैं।




