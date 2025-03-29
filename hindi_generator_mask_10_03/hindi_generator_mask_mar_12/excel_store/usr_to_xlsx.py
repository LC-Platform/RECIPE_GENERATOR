import openpyxl

# Sample input data
segments = """
<segment_id=Geo_nios_2ch_0034>
#इसका घनत्व 11.0 से भी अधिक है ।
$wyax	1	-	-	2:dem	Geo_nios_2ch_0032.5:coref	proximal	-	-
Ganatwa_1	2	-	-	4:k1	-	-	-	-
11.0	3	numex	-	2:quantmore	-	BI_2	-	-
hE_1-pres	4	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0027b>
#कि वह वेधन में प्रयोग किए जाने वाले किसी भी प्रकार के यंत्र को पिघला सकता है ।
$wyax	1	-	-	7:k1	Geo_nios_2ch_0027a.4:coref	distal	-	-
veXana_1	2	-	-	7:k7	-	-	-	-
prayoga_1	8	-	-	-	-	-	-	3:kriyAmUla
kara_2	9	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	6:mod	-	-	-	-
koI_1	4	-	-	5:quant	-	-	-	-
prakAra_1	5	-	-	6:r6	-	-	-	-
yaMwra_1	6	-	-	7:k2	-	-	-	-
piGalA_1-0_sakawA_hE_1	7	-	-	0:main	Geo_nios_2ch_0027a.5:pariNAMa	iwanA_ki	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0010>
#ये दोनों प्रक्रिया ही शैलों की टूट फूट और नई स्थलाकृतियों के निर्माण के लिए जिम्मेदार हैं ।
$wyax	1	-	-	3:dem	-	proximal	-	-
xonoM_1	2	-	pl	3:card	-	-	-	-
prakriyA_1	3	-	-	10:k1	-	hI_2	-	-
SEla_1	4	-	pl	5:r6	-	-	-	-
tUta+Puta_1	5	-	-	-	-	-	-	11:op1
naI_1	6	-	-	7:mod	-	-	-	-
sWalAkqwi_2	7	-	pl	8:r6	-	-	-	-
nirmANa_15	8	-	-	-	-	-	-	11:op2
jimmexAra_1	9	-	-	10:k1s	-	-	-	-
hE_1-pres	10	-	-	0:main	-	-	-	-
[conj_1]	11	-	-	10:rt	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0038>
#इसकी भीतरी परत ठोस है जिसे चित्र सी2 से दिखाया गया है ।
$wyax	1	-	-	3:r6	Geo_nios_2ch_0037.1:coref	proximal	-	-
BIwarI_1	2	-	-	3:mod	-	-	-	-
parawa_1	3	-	-	5:k1	-	-	-	-
Tosa_1	4	-	-	5:k1s	-	-	-	-
hE_1-pres	5	-	-	0:main	-	-	-	-
$yax	6	-	-	8:k2	4:coref	-	-
ciwra_1+sI2	7	numex	-	8:k3	-	-	-	-
xiKA_1-yA_gayA_hE_1	8	-	-	4:rcdelim	-	-	-	-
%pass_affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0023>
#इस पाठ का अध्ययन करने के पश्चात् आप मृदा निर्माण में सहायक विभिन्न कारकों की व्याख्या कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	12	-	-	-	-	-	-	3:kriyAmUla
kara_2	13	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	9:rblak	-	-	-	-
$addressee	4	anim	pl	9:k1	-	respect	-	-
mqxA_1	11	-	-	-	-	-	-	10:mod
nirmANa_1	5	-	-	-	-	-	-	10:head
sahAyaka_1	6	-	-	8:mod	-	-	-	-
viBinna_1	7	-	-	8:mod	-	-	-	-
kAraka_1	8	-	pl	9:k2	-	-	-	-
vyAKyA_1	14	-	-	-	-	-	-	9:kriyAmUla
kara_1-0_sakegA_1	15	-	-	-	-	-	-	9:verbalizer
[cp_2]	9	-	-	0:main	-	-	-	-
[compound_1]	10	-	-	6:rt	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0024c>
#और इसके भूगर्भीय पदार्थों की बनावट गहराई बढने के साथ बदलती जाती है ।
$wyax	1	-	-	3:r6	Geo_nios_2ch_0024a.3:coref	proximal	-	-
BUgarBIya_1	2	-	-	3:mod	-	-	-	-
paxArWa_1	3	-	pl	4:r6	-	-	-	-
banAvata_1	4	-	-	7:k1	-	-	-	-
gaharAI_1	5	-	-	6:k1	-	-	-	-
baDa_1	6	-	-	7:rproportion	-	-	-	-
baxala_5-wA_jAwA_hE_1	7	-	-	0:main	Geo_nios_2ch_0024b.5:samuccaya	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0016>
#इस पाठ का अध्ययन करने के पश्चात् आप शैल और खनिजों में अन्तर कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	8	-	-	-	-	-	-	3:kriyAmUla
kara_2	9	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	pl	7:rblak	-	-	-	-
$addressee	4	anim	pl	7:k1	-	respect	-	-
SEla_1	5	-	-	-	-	-	-	12:op1
Kanija_1	6	-	pl	-	-	-	-	12:op2
anwara_1	10	-	-	-	-	-	-	7:kriyAmUla
kara_1-0_sakegA_1	11	-	-	-	-	-	-	7:verbalizer
[cp_2]	7	-	-	0:main	-	-	-	-
[conj_1]	12	-	-	7:k7	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0018>
#इस पाठ का अध्ययन करने के पश्चात् आप शैलों का आर्थिक महत्व बता सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	9	-	-	-	-	-	-	3:kriyAmUla
kara_2	10	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	8:rblak	-	-	-	-
$addressee	4	anim	pl	8:k1	-	respect	-	-
SEla_1	5	-	pl	6:r6	-	-	-	-
ArWika_1	6	-	-	7:mod	-	-	-	-
mahawva_1	7	-	-	8:k2	-	-	-	-
bawA_1-0_sakegA_1	8	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0001>
#संभवतः पृथ्वी ही पूरे ब्रह्मांड का एक ऐसा ज्ञात ग्रह है जिस पर विकसित जीवन पाया जाता है ।
saMBavawaH_1	1	-	-	9:vkvn	-	-	-	-
pqWvI_1	2	-	-	9:k1	-	hI_2	-	-
pUrA_3	3	-	-	4:mod	-	-	-	-
brahmAMda_3	4	-	-	8:r6	-	-	-	-
eka_2	5	-	-	8:quant	-	-	-	-
$wyax	6	-	-	14:dem	-	proximal	-	-
prakAra_1	14	-	-	8:r6	-	-	-	-
jFAwa_1	7	-	-	8:mod	-	-	-	-
graha_1	8	-	-	9:k1s	-	-	-	-
hE_1-pres	9	-	-	0:main	-	-	-	-
$yax	10	-	-	13:k7p	2:coref	-	-	-
vikasiwa_4	11	-	-	12:mod	-	-	-	-
jIvana_1	12	-	-	13:k1	-	-	-	-
pA_13-yA_jAwA_hE_1	13	-	-	2:rcdelim	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0013>
#हम अपक्षय और उसके प्रकार, तल संतुलन की प्रक्रिया और मृदा के निर्माण तथा उसके महत्व के विषय में भी अध्ययन करेंगे ।
$speaker	1	anim	pl	12:k1	-	-	-	-
apakRaya_1	2	-	-	-	-	-	-	17:op1
$wyax	3	-	-	4:r6	2:coref	proximal	-	-
prakAra_7	4	-	-	-	-	-	-	17:op2
wala_1	14	-	-	-	-	-	-	13:mod
saMwulana_1	5	-	-	-	-	-	-	13:head
prakriyA_1	6	-	-	-	-	-	-	17:op3
mqxA_1	7	-	-	8:r6	-	-	-	-
nirmANa_14	8	-	-	-	-	-	-	17:op4
$wyax	9	-	-	10:r6	8:coref	proximal	-	-
mahawva_1	10	-	-	-	-	-	-	17:op5
viRaya_1	11	-	-	12:k7	-	-	-	-
aXyayana_1	15	-	-	-	-	-	-	12:kriyAmUla
kara_2-gA_1	16	-	-	-	-	-	-	12:verbalizer
[cp_1]	12	-	-	0:main	-	-	-	-
[compound_1]	13	-	-	6:r6	-	-	-	-
[conj_1]	17	-	-	11:r6	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0048>
#स्थलमण्डल के ऊपरी भाग को भूपर्पटी कहते हैं ।
sWalamaNdala_1	1	-	-	3:r6	-	-	-	-
UparI_1	2	-	-	3:mod	-	-	-	-
BAga_2	3	-	-	5:k2	-	-	-	-
BUparpatI_1	4	-	-	5:k2s	-	-	-	-
kaha_1-wA_hE_1	5	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0008c>
# जो शैलों को विखंडित कर देती हैं ।
$yax	9	-	-	11:k1	Geo_nios_2ch_0008a.6:coref	-	-	-
SEla_1	10	-	pl	11:k2	-	-	-	-
viKaMdiwa_1	12	-	-	-	-	-	-	11:kriyAmUla
kara_1-wA_hE_1	13	-	-	-	-	[shade:xe_1]	-	11:verbalizer
[cp_1]	11	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0006b>
#स्थलाकृतियों का स्वरूप सदैव एक जैसा नहीं रहता ।
sWalAkqwi_2	1	-	pl	2:r6	-	-	-	-
svarUpa_2	2	-	-	6:k1	-	-	-	-
saxEva_1	3	-	-	6:freq	-	-	-	-
eka+jEsA_1	4	-	-	6:krvn	-	-	-	-
nahIM_1	5	-	-	6:neg	-	-	-	-
raha_1-wA_hE_1	6	-	-	0:main	-	-	-	-
%negative
</segment_id>
<segment_id=Geo_nios_2ch_0020>
#इस पाठ का अध्ययन करने के पश्चात् आप धरातल के स्वरूप को बदलने वाली तल संतुलन की विभिन्न प्रक्रियाओं की व्याख्या कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	14	-	-	-	-	-	-	3:kriyAmUla
kara_2	15	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	11:rblak	-	-	-	-
$addressee	4	anim	pl	11:k1	-	respect	-	-
XarAwala_1	5	-	-	6:r6	-	-	-	-
svaUpa_1	6	-	-	7:k2	-	-	-	-
baxala_1	7	-	-	8:mod	-	-	-	-
wala_1	13	-	-	-	-	-	-	12:mod
sMwulana_1	8	-	-	-	-	-	-	12:head
viBinna_1	9	-	pl	10:mod	-	-	-	-
prakriyA_1	10	-	pl	11:k2	-	-	-	-
vyAKya_1	16	-	-	-	-	-	-	11:kriyAmUla
kara_1-0_sakegA_1	17	-	-	-	-	-	-	11:verbalizer
[cp_2]	11	-	-	0:main	-	-	-	-
[compound_1]	12	-	-	10:r6	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0019b>
#और आप उपयुक्त उदाहरणों द्वारा उसके प्रकारों का वर्णन कर सकेंगे।
$addressee	4	anim	pl	9:k1	-	respect	-	-
upayukwa_2	5	-	-	6:mod	-	-	-	-
uxAharaNa_1	6	-	-	9:k3	-	-	-	-
$wyax	7	-	-	8:r6	Geo_nios_2ch_0019a.5:coref	proximal	-	-
prakAra_7	8	-	pl	9:k2	-	-	-	-
varNana_1	10	-	-	-	-	-	-	9:kriyAmUla
kara_1-0_sakegA_1	11	-	-	-	-	-	-	9:verbalizer
[cp_1]	9	-	-	0:main	Geo_nios_2ch_0019a.7:samuccaya	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0008b>
#जो शैलों को कमजोर कर देती हैं।
SEla_1	10	-	pl	11:k2	-	-	-	-
kamajora_1	12	-	-	-	-	-	-	11:kriyAmUla
kara_1-wA_hE_1	13	-	-	-	-	[shade:xe_1]	-	11:verbalizer
[cp_1]	11	-	-	-	-	-	-	-
$yax	9	-	-	11:k1	Geo_nios_2ch_0008a.6:coref	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0022>
#इस पाठ का अध्ययन करने के पश्चात् आप मृदा निर्माण और अपक्षय के बीच सम्बन्ध स्थापित कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	11	-	-	-	-	-	-	3:kriyAmUla
kara_2	12	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	8:rblak	-	-	-	-
$addressee	4	anim	pl	8:k1	-	respect	-	-
mqxA_1	10	-	-	-	-	-	-	9:mod
nirmANa_1	5	-	-	-	-	-	-	9:head
apakRaya_1	6	-	-	-	-	-	-	15:op2
sambanXa_1	7	-	-	8:k2	-	-	-	-
sWApiwa_1	13	-	-	-	-	-	-	8:kriyAmUla
kara_1-0_sakegA_1	14	-	-	-	-	-	-	8:verbalizer
[cp_2]	8	-	-	0:main	-	-	-	-
[compound_1]	9	-	-	7:r6	-	-	-	-
[conj_1]	15	-	-	-	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0042>
#इसलिए इस परत को सीमा (सिलीका + मैगनीशियम) भी कहते हैं ।
$wyax	1	-	-	2:dem	-	proximal	-	-
parawa_1	2	-	-	5:k2	-	-	-	-
sImA_1	3	-	ne	5:k2s	-	BI_1	-	-
silIkA_1+mEganISiyama_1	4	-	-	3:rs	-	-	-	-
kaha_1-wA_hE_1	5	-	-	0:main	Geo_nios_2ch_0041.6:pariNAma-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0028>
#अतः वेधन कार्य कम गहराइयों तक ही सीमित है ।
veXana_1	7	-	-	-	-	-	-	6:mod
kArya_1	1	-	-	-	-	-	-	6:head
kama_1	2	-	-	3:mod	-	-	-	-
gaharAI_1	3	-	pl	5:k7p	-	hI_2	-	-
sImiwa_1	4	-	pl	5:k1s	-	-	-	-
hE_1-pres	5	-	-	0:main	Geo_nios_2ch_0027b.7:pariNAma	-	-	-
[compound_1]	6	-	-	5:k1	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0051>
#यह पृथ्वी की सबसे अधिक घनत्व वाली परत है ।
$wyax	1	-	-	6:k1	Geo_nios_2ch_0050.1:coref	proximal	-	-
pqWvI_1	2	-	-	5:r6	-	-	-	-
aXika_1	3	-	superl	5:quant	-	-	-	-
Ganawva_1	4	-	mawupa	5:mod	-	-	-	-
parawa_1	5	-	-	6:k1s	-	-	-	-
hE_1-pres	6	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0012>
#इस पाठ में हम पृथ्वी के भूगर्भ और उसके ऊपरी भाग-भूपर्पटी के पदार्थों का अध्ययन करेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	11:k7	-	-	-	-
$speaker	3	anim	pl	11:k1	-	-	-	-
pqWvI_1	4	-	-	5:r6	-	-	-	-
BUgarBa_1	5	-	-	-	-	-	-	16:op1
$wyax	6	-	-	8:r6	5:coref	proximal	-	-
uparI_1	7	-	-	8:mod	-	-	-	-
BAga_1	8	-	-	10:r6	-	-	-	-
BU_1	13	-	-	-	-	-	-	12:avayavI
parpatI_1	9	-	-	-	-	-	-	12:avayava
paxArWa_10	10	-	pl	-	-	-	-	16:op2
aXyayana_1	14	-	-	-	-	-	-	11:kriyAmUla
kara_2-gA_1	15	-	-	-	-	-	-	11:verbalizer
[cp_1]	11	-	-	0:main	-	-	-	-
[compound_1]	12	-	-	8:rs	-	-	-	-
[conj_1]	16	-	-	11:k2	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0049>
#पृथ्वी के आन्तरिक भाग की तीन प्रमुख संकेन्द्रीय परते हैं - क्रोड, मैंटल और स्थलमंडल ।
pqWvI_1	1	-	-	3:r6	-	-	-	-
Anwarika_1	2	-	-	3:mod	-	-	-	-
BAga_1	3	-	-	7:r6	-	-	-	-
3	4	numex	-	7:card	-	-	-	-
pramuKa_1	5	-	-	7:mod	-	-	-	-
saMkenxrIya_1	6	-	pl	7:mod	-	-	-	-
parawa_1	7	-	-	8:k1	-	-	-	-
hE_1-pres	8	ne	-	0:main	-	-	-	-
kroda_1	9	-	-	-	-	-	-	12:op1
mEMtala_2	10	-	-	-	-	-	-	12:op2
sWalamaMdala_1	11	-	-	-	-	-	-	12:op3
[conj_1]	12	-	-	7:re	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0004a>
#इससे यह स्पष्ट होता है  ।
$wyax	1	-	-	2:k1	Geo_nios_2ch_0004b.6:coref	proximal	-	-
spaRta_1	3	-	-	-	-	-	-	2:kriyAmUla
ho_1-wA_hE_1	4	-	-	-	-	-	-	2:verbalizer
[cp_1]	2	-	-	0:main	Geo_nios_2ch_0003a.3:pariNAma	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0037>
#क्रोड को पुनः दो परतों में बाँट सकते हैं ।
$speaker	6	anim	pl	5:k1	-	-	-	-
kroda_1	1	-	-	5:k2	-	-	-	-
punaH_1	2	-	-	5:krvn	-	-	-	-
2	3	numex	-	4:card	-	-	-	-
parawa_1	4	-	pl	5:k7	-	-	-	-
bAzta_1-0_sakawA_hE_1	5	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0047>
#इसलिए इस परत की स्याल(सिलीका + एल्यूमीनियम) भी कहते हैं ।
$wyax	1	-	-	2:dem	-	proximal	-	-
parawa_1	2	-	-	5:k2	-	-	-	-
syAla_1	3	-	-	5:k2s	-	BI_1	-	-
silEkA_1+elyUmEniyama_1	4	-	-	3:rs	-	-	-	-
kaha_1-wA_hE_1	5	-	-	0:main	Geo_nios_2ch_0046.9:pariNAma	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0050>
#क्रोड सबसे आन्तरिक परत है ।
kroda_1	1	-	-	4:k1	-	-	-	-
Anwarika_1	2	-	superl	3:mod	-	-	-	-
parawa_1	3	-	-	4:k1s	-	-	-	-
hE_1-pres	4	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0033>
#यह सबसे अधिक घनत्व वाली परत है ।
$wyax	1	-	-	5:k1	Geo_nios_2ch_0032.5:coref	proximal	-	-
aXika_1	2	-	superl	3:mod	-	-	-	-
Ganawva_1	3	-	mawup	4:mod	-	-	-	-
parawa_1	4	-	-	5:k1s	-	-	-	-
hE_1-pres	5	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0045>
#इसे स्थलमण्डल कहते हैं, जिसका घनत्व 2.75 से 2.90 है ।
$wyax	1	-	-	3:k2	Geo_nios_2ch_0044.1:coref	proximal	-	-
sWalamaNdala_1	2	-	-	3:k2s	-	-	-	-
kaha_1-wA_hE_1	3	-	-	0:main	-	-	-	-
$yax	4	-	-	5:r6	2:coref	-	-	-
Ganawva_1	5	-	-	8:k1	-	-	-	-
2.75	6	numex	-	8:k1s	-	-	-	-
2.90	7	numex	-	8:k1s	-	-	-	-
hE_1-pres	8	-	-	2:rcelab	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0046>
#स्थलमण्डल के प्रमुख निर्माणकारी तत्व सिलीका (सि) एल्यूमीनियम (एल) हैं ।
sWalamaNdala_1	1	-	-	4:r6	-	-	-	-
pramuKa_1	2	-	-	4:mod	-	-	-	-
nirmANakArI_1	3	-	-	4:mod	-	-	-	-
wawva_1	4	-	-	9:k1	-	-	-	-
silIkA_1	5	-	-	9:k1s	-	-	-	-
^ci	6	-	-	5:rs	-	-	-	-
elyUmIniyama_1	7	-	-	9:k1s	-	-	-	-
^ela	8	-	-	7:rs	-	-	-	-
hE_1-pres	9	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0006a>
#हम यह जानते हैं।
$speaker	1	anim	pl	3:k1	-	-	-	-
$wyax	2	-	-	3:k2	Geo_nios_2ch_0006b.6:coref	proximal	-	-
jAna_10 (know_1)	3	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0003a>
#आप यह भी जानते हैं ।
$wyax	2	-	-	3:k2	Geo_nios_2ch_0003b.13:coref	proximal/BI_1	-	-
$addressee	1	anim	pl	3:k1	-	respect	-	-
jAna_10 (know_1)	3	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0009>
#दूसरे प्रकार की शक्तियाँ टूटी-फूटी शैलों को ऊँचे भू भागों से हटाकर नीचे के भू भागों में जमा करती रहती हैं ।
xUsarA_1	1	-	-	2:mod	-	-	-	-
prakAra_1	2	-	-	3:r6	-	-	-	-
Sakwi_1	3	-	pl	12:k1	-	-	-	-
tUtA+PUtA_1	5	-	-	6:mod	-	-	-	-
SEla_1	6	-	pl	9:k2	-	-	-	-
UzcA_1	7	-	-	8:mod	-	-	-	-
BU_1	14	-	-	-	-	-	-	13:avayavI
BAga_1	8	-	-	-	-	-	-	13:avayava
hatA_1	9	-	-	12:rpk	-	-	-	-
nIce_1	10	-	-	11:r6	-	-	-	-
BU_1	16	-	-	-	-	-	-	15:avayavI
BAga_1	11	-	-	-	-	-	-	15:avayava
jamA_1	17	-	-	-	-	-	-	12:kriyAmUla
kara_1-wA_rahawA_hE_1	18	-	-	-	-	-	-	12:verbalizer
[cp_1]	12	-	-	0:main	-	-	-	-
[compound_1]	13	-	-	9:k5	-	-	-	-
[compound_2]	15	-	-	12:k7p	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0015>
#इस पाठ का अध्ययन करने के पश्चात् आप भूगर्भ की विभिन्न परतों की तुलना उनकी मोटाई, तापमान, घनत्व और दबाव के संदर्भ में कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	15	-	-	-	-	-	-	3:kriyAmUla
kara_2	16	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	14:rblak	-	-	-	-
$addressee	4	anim	pl	14:k1	-	respect	-	-
BUgarBa_1	5	-	-	7:r6	-	-	-	-
viBinna_1	6	-	pl	7:mod	-	-	-	-
parawa_1	7	-	pl	14:k2	-	-	-	-
$wyax	8	-	-	9:r6	7:coref	proximal	-	-
motAI_4	9	-	-	-	-	-	-	19:op1
wApamAna_1	10	-	-	-	-	-	-	19:op2
Ganawva_1	11	-	-	-	-	-	-	19:op3
xabAva_1	12	-	-	-	-	-	-	19:op4
saMxarBa_1	13	-	-	14:k7	-	-	-	-
wulanA_1	17	-	-	-	-	-	-	14:kriyAmUla
kara_1-0_sakegA_1	18	-	-	-	-	-	-	14:verbalizer
[cp_2]	14	-	-	0:main	-	-	-	-
[conj_1]	19	-	-	13:r6	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0040>
#जो परत क्रोड को घेरे हुए है, उसे मैंटल कहते हैं ।
$yax	1	-	-	2:dem	-	-	-	-
parawa_1	2	-	-	5:k1	-	-	-	-
kroda_1	3	ne	-	5:k2	-	-	-	-
Gera_1	4	-	kqw	5:k1s	-	-	-	-
hE_1-pres	5	-	-	5:rcelab	-	-	-	-
$wyax	6	-	-	7:k2	5:coref	proximal	-	-
mEMtala_2	7	-	-	8:k2s	-	-	-	-
kaha_1-wA_hE_1	8	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0043>
#इसका घनत्व 3.1 से 5.1 तक है ।
$wyax	1	-	-	2:r6	Geo_nios_2ch_0042.2:coref	proximal	-	-
Ganawva_1	2	numex	-	5:k1	-	-	-	-
3.1	3	numex	-	5:k1s	-	-	-	-
5.1	4	-	-	5:k1s	-	-	-	-
hE_1-pres	5	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0036>
#इसीलिये क्रोड को निफे (निकिल+फेरम, लोहा) कहते हैं ।
koroda_1	1	ne	-	4:k2	-	-	-	-
@niPe	2	-	-	4:k2s	-	-	-	-
Nikila_1+Perama_1	3	-	-	2:rs	-	-	-	-
lohA_1	5	-	-	-	-	-	-	-
kaha_1-wA_hE_1	4	-	-	0:main	Geo_nios_2ch_0035.4:pariNAma	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0035>
#यह लोहा और निकिल धातुओं से बनी है ।
$wyax	1	-	-	4:k1	Geo_nios_2ch_0032.5:coref	proximal	-	-
lohA_1+XAwu_1	2	-	pl	-	-	-	-	5:op1
nikila_1+XAwu_1	3	-	pl	-	-	-	-	5:op2
bana_14-yA_hE_1	4	-	-	0:main	-	-	-	-
[conj_1]	5	-	-	4:k5prk	-	-	-	-
%pass_affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0044>
#मैंटल पृथ्वी की सबसे ऊपरी परत से घिरा है ।
mEMtala_2	1	-	-	5:k1	-	-	-	-
pqWvI_1	2	-	-	4:r6	-	-	-	-
UparI_1	3	-	superl	4:mod	-	-	-	-
parawa_1	4	-	-	5:k3	-	-	-	-
Gira_1-yA_hE_1	5	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0005>
#संसार में खनन कार्य 5 किलोमीटर से भी कम गहराई तक ही सीमित है ।
saMsAra_1	1	-	-	6:k7	-	-	-	-
Kanana_1+kArya_1	2	-	-	6:k1	-	-	-	-
5	7	-	-	8:card	-	-	-	3:count
kilomItara_1	8	-	-	-	-	-	-	3:unit
gaharAI_1	4	-	comperless	6:k7p	-	hI_2	-	-
sImiwa_1	5	-	-	6:k1s	-	-	-	-
hE_1-pres	6	-	-	0:main	-	-	-	-
[meas_1]	3	meas	-	4:quantless	-	BI_2	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0024a>
#पृथ्वी के आन्तरिक भाग को प्रत्यक्ष रूप से देखना सम्भव नहीं है; ।
pqWvI_1	1	-	-	3:r6	-	-	-	-
Anwarika_1	2	-	-	3:mod	-	-	-	-
BAga_1	3	-	-	6:k2	-	-	-	-
prawyakRa_7	4	-	-	5:mod	-	-	-	-
rUpa_1	5	-	-	6:krvn	-	-	-	-
xeKa_1	6	-	-	8:k1	-	-	-	-
nahIM_1	7	-	-	8:neg	-	-	-	-
samBava_1	9	-	-	8:k1s	-	-	-	-
hE_1-pres	8	-	-	0:main	-	-	-	-
%negative
</segment_id>
<segment_id=Geo_nios_2ch_0002>
#अन्य आकाशीय पिण्डों की भाँति पृथ्वी की आकृति भी गोलाकार है ।
anya_1	1	-	-	3:mod	-	-	-	-
AkASIya_1	2	-	-	3:mod	-	-	-	-
piNda_1	3	-	pl	5:ru	-	-	-	-
pqWvI_1	4	-	-	5:r6	-	-	dm_geo_B	-
Akqwi_1	5	-	-	7:k1	-	BI_1	-	-
hE_1-pres	7	-	-	0:main	-	-	-	-
golAkAra_1 (round_2)	6	-	-	7:k1s	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0011>
#हमारे लिए अत्यंत महत्वपूर्ण मृदा का निर्माण भी एक सीमा तक इन्हीं प्रक्रियाओं द्वारा होता है ।
$speaker	1	anim	pl	9:rt	-	-	-	-
awyaMwa_1	2	-	-l	3:intf	-	-	-	-
mahawvapUrNa_1	3	-	-	4:mod	-	-	-	-
mqxA_1	4	-	-	9:k2	-	BI_1	-	-
eka+sImA+waka_1	5	-	-	9:vkvn	-	-	-	-
$wyax	7	-	-	8:dem	-	proximal	-	-
prakriyA_1	8	-	pl	9:k3	-	-	-	-
nirmANa_1	10	-	-	-	-	-	-	9:kriyAmUla
ho_1-wA_hE_1	11	-	-	-	-	-	-	9:verbalizer
[cp_1]	9	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0025>
#मनुष्य ने खनन एवम वेधन क्रियाओं द्वारा इसके कुछ ही किलोमीटर तक के आन्तरिक भाग को प्रत्यक्ष रूप से देखा है ।
manuRya_1	1	anim	pl	12:k1	-	-	-	-
Kanana_1	14	-	-	-	-	-	-	13:mod
kriyA_1	2	-	-	-	-	-	-	13:head
veXana_1	16	-	-	-	-	-	-	15:mod
kriyA_1	3	-	-	-	-	-	-	15:head
$wyax	5	-	-	7:r6	Geo_nios_2ch_0024a.3:coref	proximal	-	-
kuCa_1	6	-	-	7:quant	-	hI_2	-	-
kilomItara_1	7	-	-	9:r6	-	-	-	-
Anwarika_1	8	-	-	9:mod	-	-	-	-
BAga_1	9	-	-	12:k2	-	-	-	-
prawyakRa_1	10	-	-	11:mod	-	-	-	-
rUpa_1	11	-	-	12:krvn	-	-	-	-
xeKa_5-yA_hE_1	12	-	-	0:main	-	-	-	-
[compound_1]	13	-	-	12:k3	-	-	-	-
[compound_2]	15	-	-	12:k3	-	-	-	-
[conj_1]	17	-	-	-	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0026>
#गहराई के साथ तापमान में तेजी से वृद्धि के कारण अधिक गहराइयों तक खनन और वेधन कार्य करना संभव नहीं है ।
gaharAI_1	1	-	-	12:rask7	-	-	-	-
wApamAna_1	2	-	-	4:k7	-	-	-	-
wejI+se_1	3	-	-	4:krvn	-	-	-	-
vqxXi_1	4	-	-	12:rh	-	-	-	-
aXika_1	5	-	-	6:mod	-	-	-	-
gaharAI_1	6	-	pl	9:k7p	-	-	-	-
Kanana_1	14	-	-	-	-	-	-	13:mod
kArya_1	7	-	-	-	-	-	-	13:head
veXana_1	16	-	-	-	-	-	-	15:mod
kArya_1	8	-	-	-	-	-	-	15:head
kara_1	9	-	-	12:k1	-	-	-	-
saMBava_1	18	-	-	12:k1s	-	-	-	-
nahIM_1	11	-	-	12:neg	-	-	-	-
hE_1-pres	12	-	-	0:main	-	-	-	-
[compound_1]	13	-	-	9:k2	-	-	-	-
[compound_2]	15	-	-	9:k2	-	-	-	-
[conj_1]	17	-	-	-	-	-	-	-
%negative
</segment_id>
<segment_id=Geo_nios_2ch_0007>
#उसका रूप लगातार बदलता रहता है ।
$wyax	1	-	-	2:r6	Geo_nios_2ch_0006b.1:coref	distal	-	-
rUpa_1	2	-	-	4:k1	-	-	-	-
lagAwara_1	3	-	-	4:krvn	-	-	-	-
baxala_1-wA_rahawA_hE_1	4	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0017>
#इस पाठ का अध्ययन करने के पश्चात् आप रचना के आधार पर शैलों का वर्गीकरण कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
axyayana_1	9	-	-	-	-	-	-	3:kriyAmUla
kara_2	10	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	8:rblak	-	-	-	-
$addressee	4	anim	pl	8:k1	-	respect	-	-
racanA_1	5	-	-	6:r6	-	-	-	-
AXAra_1	6	-	-	8:k7	-	-	-	-
SEla_1	7	-	pl	8:k2	-	-	-	-
vargIkaraN_1	11	-	-	-	-	-	-	8:kriyAmUla
kara_1-0_sakegA_1	12	-	-	-	-	-	-	8:verbalizer
[cp_2]	8	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0024b>
#क्योंकि यह बहुत बडा गोला है  ।
$wyax	1	-	-	5:k1	Geo_nios_2ch_0024a.1:coref	proximal	-	-
bahuwa_1	2	-	-	3:intf	-	-	-	-
badZA_2	3	-	-	4:mod	-	-	-	-
golA_1	4	-	-	5:k1s	-	-	-	-
hE_1-pres	5	-	-	0:main	Geo_nios_2ch_0024a.8:kAryakAraNa	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0014>
#इस पाठ का अध्ययन करने के पश्चात् आप पृथ्वी के आन्तरिक भाग या भूगर्भ के संबंध में प्रत्यक्ष प्रेक्षण करने की सीमाओं को समझा सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	14	-	-	-	-	-	-	3:kriyAmUla
kara_2	15	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	12:rblak	-	-	-	-
$addressee	4	anim	pl	12:k1	-	respect	-	-
pqWvI_1	5	-	-	7:r6	-	-	-	-
Anwarika_1	6	-	-	7:mod	-	-	-	-
BAga_1	7	-	-	-	-	-	-	18:op1
BUgarBa_1	8	-	-	-	-	-	-	18:op2
saMbaMXa_1	9	-	-	11:k7	-	-	-	-
prawyakRa_6	10	-	-	11:krvn	-	-	-	-
prekRaNa_1	16	-	-	-	-	-	-	11:kriyAmUla
kara_1	17	-	-	-	-	-	-	11:verbalizer
[cp_2]	11	-	pl	12:r6	-	-	-	-
sImA_1	12	-	pl	13:k2	-	-	-	-
samaJA_1-0_sakegA_1	13	-	-	0:main	-	-	-	-
[disjunct_1]	18	-	-	9:r6	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0004b>
#कि धरातल के नीचे तापमान बहुत ऊँचा है ।
XarAwala_1	1	-	-	2:rdl	-	-	-	-
nIce_1	2	-	-	6:k7p	-	-	-	-
wApamAna_1	3	-	-	6:k1	-	-	-	-
bahuwa_7	4	-	-	5:intf	-	-	-	-
UzcA_1	5	-	-	6:k1s	-	-	-	-
hE_1-pres	6	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0030>
#पृथ्वी के विशाल आकार और गइराई के साथ बढते तापमान ने भूगर्भ की प्रत्यक्ष जानकारी की सीमाएँ निश्चित कर दी है ।
pqWvI_1	1	-	-	3:r6	-	-	-	-
viSAla_1	2	-	-	3:mod	-	-	-	-
AkAra_3	3	-	-	-	-	-	-	14:op1
gairAI_1	4	-	-	-	-	-	-	14:op2
baDa_1	5	-	-	6:rvks	-	-	-	-
wApamAna_1	6	-	-	11:k1	-	-	-	-
BUgarBa_1	7	-	-	9:r6	-	-	-	-
prawyakRa_6	8	-	-	9:mod	-	-	-	-
jAnakArI_1	9	-	-	10:r6	-	-	-	-
sImA_6	10	-	pl	11:k2	-	-	-	-
niSciwa_1	12	-	-	-	-	-	-	11:kriyAmUla
kara_2-yA_hE_1	13	-	-	-	-	[shade:xe_1]	-	11:verbalizer
[cp_1]	11	-	-	0:main	-	-	-	-
[conj_1]	14	-	-	11:rask1	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0029>
#इसलिए पृथ्वी के गर्भ के विषय में प्रत्यक्ष जानकारी के मिलने में कई कठिनाइयाँ आती हैं ।
pqWvI_1	1	-	-	2:r6	-	-	-	-
garBa_1	2	-	-	3:r6	-	-	-	-
viRaya_1	3	-	-	6:k7	-	-	-	-
prawyakRa_6	4	-	-	4:mod	-	-	-	-
jAnakArI_1	5	-	-	6:k1	-	-	-	-
mila_1	6	-	-	9:k7	-	-	-	-
kaI_1	7	-	-	8:quant	-	-	-	-
kaTinAI_1	8	-	pl	9:k1	-	-	-	-
A_1-wA_hE_1	9	-	-	0:main	Geo_nios_2ch_0028.5:parinAma	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0003b>
#कि स्रोतों से गर्म जल और ज्वालामुखियों से अत्यंत गर्म लावा पृथ्वी के भीतरी भागों से निकलकर धरातल पर पहुंचता है ।
swrowra_1	1	-	pl	11:k5	-	-	-	-
garma_2	2	-	-	3:mod	-	-	-	-
jala_1	3	-	-	-	-	-	-	14:op1
jvAlAmuKI_1	4	-	pl	11:k5	-	-	-	-
awyaMwa_1	5	-	-	6:intf	-	-	-	-
garma_2	6	-	-	7:mod	-	-	-	-
lAvA_1	7	-	-	-	-	-	-	14:op2
pqWvI_1	8	-	-	10:r6	-	-	-	-
BIwarI_1	9	-	-	10:mod	-	-	-	-
BAga_1	10	-	pl	11:k5	-	-	-	-
nikala_21	11	-	-	13:rpk	-	-	-	-
XarAwala_1	12	-	-	13:k7p	-	-	-	-
pahuMca_3-wA_hE_1	13	-	-	0:main	-	-	-	-
[conj_1]	14	-	-	13:k1	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0032>
#पृथ्वी की सबसे अधिक गहराई वाली परत को क्रोड कहते हैं ।
pqWvI_1	1	-	-	4:r6	-	-	-	-
aXika_1	2	-	superl	3:mod	-	-	-	-
gaharAI_1	3	-	mawup	4:mod	-	-	-	-
parawa_1	4	-	-	6:k2	-	-	-	-
kroda	5	-	-	6:k2s	-	-	-	-
kaha_1-wA_hE_1-pres	6	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0031>
#पृथ्वी की आन्तरिक परतों का वर्गीकरण और उनकी मोटाइयों को चित्र संख्या 2.1 में दर्शाया गया है ।
pqWvI_1	1	-	-	3:r6	-	-	-	-
Anwarika_1	2	-	-	3:mod	-	-	-	-
parawa_1	3	-	pl	4:r6	-	-	-	-
vargIkaraNa_1	4	-	-	-	-	-	-	9:op1
$wyax	5	-	pl	6:dem	3:coref	proximal	-	-
motAi_1	6	-	pl	-	-	-	-	9:op2
ciwra_1+saMKyA_1	7	-	-	8:k7p	-	-	-	-
2.1	7	numex	-	-	-	-	-	-
xarSA_1-yA_gayA_hE_1	8	-	-	0:main	-	-	-	-
[conj_1]	9	-	-	8:k2	-	-	-	-
%pass_affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0021>
#इस पाठ का अध्ययन करने के पश्चात् आप निम्नीकरण और अधिवृद्धि में अन्तर कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	8	-	-	-	-	-	-	3:kriyAmUla
kara_2	9	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	7:rblak	-	-	-	-
$addressee	4	anim	pl	7:k1	-	respect	-	-
nimnIkaraNa_1	5	-	-	-	-	-	-	12:op1
aXivqxXi_1	6	-	-	-	-	-	-	12:op2
anwara_1	10	-	-	-	-	-	-	7:kriyAmUla
kara_1-0_sakegA_1	11	-	-	-	-	-	-	7:verbalizer
[cp_2]	7	-	-	0:main	-	-	-	-
[conj_1]	12	-	-	7:k7	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0008b>
#जो शैलों को कमजोर कर देती हैं।
SEla_1	10	-	pl	11:k2	-	-	-	-
kamajora_1	12	-	-	-	-	-	-	11:kriyAmUla
kara_1-wA_hE_1	13	-	-	-	-	[shade:xe_1]	-	11:verbalizer
[cp_1]	11	-	-	-	-	-	-	-
$yax	9	-	-	11:k1	Geo_nios_2ch_0008a.6:coref	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0027a>
#भूगर्भ में इतना अधिक ऊँचा तापमान है  ।
BUgarBa_1	1	-	-	5:k7p	-	-	-	-
aXika_1	2	-	-	3:mod	-	-	-	-
UzcA_1	3	-	-	4:mod	-	-	-	-
wApamAna_1	4	-	-	5:k1	-	-	-	-
hE_1-pres	5	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0008a>
#बाह्य शक्तियों के एक समूह में वे शक्तियाँ सम्मलित हैं ।
bAhya_1	1	-	-	2:mod	-	-	-	-
Sakwi_1	2	-	pl	4:r6	-	-	-	-
eka_2	3	-	-	4:quant	-	-	-	-
samUha_1	4	-	-	8:k7	-	-	-	-
$wyax	5	-	-	6:dem	-	distal	-	-
Sakwi_1	6	-	pl	8:k1	-	-	-	-
sammaliwa_1	7	-	-	8:k1s	-	-	-	-
hE_1-pres	8	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0019a>
#इस पाठ का अध्ययन करने के पश्चात् आप अपक्षय शब्द की व्याख्या कर सकेंगे ।
$wyax	1	-	-	2:dem	-	proximal	-	-
pATa_1	2	-	-	3:r6	-	-	-	-
aXyayana_1	8	-	-	-	-	-	-	3:kriyAmUla
kara_2	9	-	-	-	-	-	-	3:verbalizer
[cp_1]	3	-	-	7:rblak	-	-	-	-
$addressee	4	anim	pl	7:k1	-	respect	-	-
apakRaya_1	5	-	-	7:k2	-	-	-	-
Sabxa_1	6	-	-	5:rs	-	-	-	-
vyAKyA_1	10	-	-	-	-	-	-	7:kriyAmUla
kara_1-0_sakegA_1	11	-	-	-	-	-	-	7:verbalizer
[cp_2]	7	-	-	0:main	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0039>
#दूसरी परत अर्द्ध तरल है जिसे चित्र सी1 से दिखाया गया है ।
xUsarA_1	1	-	-	2:ord	-	-	-	-
parawa_1	2	-	-	5:k1	-	-	-	-
arxXa_1	3	-	-	4:mod	-	-	-	-
warala_1	4	-	-	5:k1s	-	-	-	-
hE_1-pres	5	-	-	0:main	-	-	-	-
$yax	6	-	-	8:k2	5:coref	4:coref	-	-
ciwra_1+sI1	7	numex	-	8:k3	-	-	-	-
xiKA_1-yA_gayA_hE_1	8	-	-	4:rcelab	-	-	-	-
%affirmative
</segment_id>
<segment_id=Geo_nios_2ch_0041>
#यह परत मुख्यतः सिलीका और मैगनीशियम से बनी है ।
$wyax	1	-	-	2:dem	-	proximal	-	-
parawa_1	2	-	-	6:k1	-	-	-	-
muKyawaH_1	3	-	-	6:krvn	-	-	-	-
silIka_1	4	-	-	-	-	-	-	7:op1
mEganISiyama_1	5	-	-	-	-	-	-	7:op2
bana_14-yA_hE_1	6	-	-	0:main	-	-	-	-
[conj_1]	7	-	-	6:k5prk	-	-	-	-
%affirmative
</segment_id>
"""


# Parse segments
def parse_segments(text):
    segments = []
    segment_data = text.strip().split('<segment_id=')
    for segment in segment_data[1:]:
        segment_content = "<segment_id=" + segment.strip()  # Re-add the '<segment_id=' to each segment
        segments.append(segment_content)
    return segments

# Save segments to an Excel file
def save_to_excel(segments, filename='segments.xlsx'):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Segments"
    
    # Add header row
    ws.append(["Segment"])
    
    # Add each segment in a row (in one cell)
    for segment in segments:
        ws.append([segment])
    
    # Save the workbook
    wb.save(filename)

# Parse the input data and save it to Excel
segment_list = parse_segments(segments)
save_to_excel(segment_list)

print(f"Segments saved to 'segments.xlsx'.")
