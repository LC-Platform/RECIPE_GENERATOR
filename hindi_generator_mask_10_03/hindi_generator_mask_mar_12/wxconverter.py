# from googleapiclient.discovery import build
# import json

# def transliterate_text(text):
#     # Set up API key and build the service
#     api_key = 'YOUR_API_KEY'
#     service = build('transliterate', 'v1', developerKey=api_key)

#     # Make the request
#     result = service.transliterate().transliterate(
#         sourceText=text, 
#         targetLanguage='hi'
#     ).execute()

#     # Extract and return the transliterated text
#     transliterated_text = result.get('transliterations', [{}])[0].get('transliteratedText', '')
#     return transliterated_text

# text = "Hello, how are you?"
# print(transliterate_text(text))


from wxconv import WXC

def convert_to_hindi(input_list):
    wx = WXC(order='wx2utf', lang='hin')
    wx1 = WXC(order='utf2wx', lang='hin')
    hindi_text_list = [wx.convert(word) for word in input_list]
    return hindi_text_list

one_markers = ["filtered_data"]
converted_text1 = convert_to_hindi(one_markers)
print(converted_text1)
# def convert_to_hindi(input_list):
#     wx = WXC(order='wx2utf', lang='hin')
#     wx1 = WXC(order='utf2wx', lang='hin')
#     hindi_text_list = [wx1.convert(word) for word in input_list]
#     return hindi_text_list

# # Assuming you have obtained the one_markers and zero_markers lists from the previous code

# one_markers = ['खिलवाया']
#                # ["Ora" ,':', "samuccaya",
# #                 #    "ki" ,':', "pariNAma",
# #                    "evaM" ,':', "samuccaya",
# #                    "waWA" ,':', "samuccaya",
# #                 #    "agara" ,':', "AvaSyakawApariNAma",
# #                 #    "yaxi" ,':', "AvaSyakawApariNAma",
# #                    "wo" ,':', "AvaSyakawApariNAma",
# #                    "nahIM wo",':', "AvaSyakawApariNAma",
# #                    "kyoMki" ,':', "kAryakAraNa",
# #                    'cUzki'  ,':',"kAryakAraNa",
# #                    'cUMki'  ,':',"kAryakAraNa",
# #                    "isIlie" ,':', "pariNAma",
# #                    "isalie" ,':', "pariNAma",
# #                    "awaH" ,':', "pariNAma",
# #                    "jabaki" ,':', "viroXI_xyowaka",
# #                    "yaxyapi" ,':', "vyaBicAra",
# #                    "waWApi" ,':', "vyaBicAra",
# #                    "hAlAzki" ,':', "vyaBicAra",
# #                    "Pira BI" ,':', "vyaBicAra",
# #                    "lekina" ,':', "viroXI",
# #                    "kiMwu" ,':', "viroXI",
# #                    "paraMwu" ,':', "viroXI",
# #                    "yA",':', "anyawra",
# #                    "aWavA",':', "anyawra",
# #                    'isake pariNAmasvarUpa' ,':', "pariNAma",
# #                    'isI kAraNa',':', 'pariNAma',
# #                    'isake viparIwa' ,':', "viroXI",
# #                    "viparIwa" ,':', 'viroXI',
# #                    "isake alAvA" ,':', 'samuccaya x' ,
# #                    'isake awirikwa' ,':', 'samuccaya x',
# #                    'isake sAWa-sAWa' ,':', 'samuccaya x',
# #                    'isake sAWa sAWa' ,':', 'samuccaya x',
# #                    'isa kAraNa' ,':', 'pariNAma',
# #                    'isake kAraNa',':','kAryakAraNa',
# #                    'isake bAvajZUxa' ,':', 'vavicAra',
# #                    'nA kevala',':', 'samuccaya']# print(len(one_markers))

# # ['और', ':', 'समुच्चय', 'एवं', ':', 'समुच्चय', 'तथा', ':', 'समुच्चय', 'तो', ':', 'आवश्यकतापरिणाम', 'नहीं तो', ':', 'आवश्यकतापरिणाम', 'क्योंकि', ':', 'कार्यकारण', 'चूँकि', ':', 'कार्यकारण', 'चूंकि', ':', 'कार्यकारण', 'इसीलिए', ':', 'परिणाम', 'इसलिए', ':', 'परिणाम', 'अतः', ':', 'परिणाम', 'जबकि', ':', 'विरोधी_द्योतक', 'यद्यपि', ':', 'व्यभिचार', 'तथापि', ':', 'व्यभिचार', 'हालाँकि', ':', 'व्यभिचार', 'फिर भी', ':', 'व्यभिचार', 'लेकिन', ':', 'विरोधी', 'किंतु', ':', 'विरोधी', 'परंतु', ':', 'विरोधी', 'या', ':', 'अन्यत्र', 'अथवा', ':', 'अन्यत्र', 'इसके परिणामस्वरूप', ':', 'परिणाम', 'इसी कारण', ':', 'परिणाम', 'इसके विपरीत', ':', 'विरोधी', 'विपरीत', ':', 'विरोधी', 'इसके अलावा', ':', 'समुच्चय द्', 'इसके अतिरिक्त', ':', 'समुच्चय द्', 'इसके साथ-साथ', ':', 'समुच्चय द्', 'इसके साथ साथ', ':', 'समुच्चय द्', 'इस कारण', ':', 'परिणाम', 'इसके कारण', ':', 'कार्यकारण', 'इसके बावज़ूद', ':', 'वविचार', 'ना केवल', ':', 'समुच्चय']

# # # print(len(zero_markers))
# converted_text1 = convert_to_hindi(one_markers)
# # # converted_text0 = convert_to_hindi(zero_markers)
# print("1,':',", converted_text1)
