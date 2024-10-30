pip install socketify
apt install libuv1 zlib1g

recv dict = {
    "Text":...,
    "Language":...,
    "ClientId":...,
    "RequestId":...
}

ru_test = ['Маленький человек в дырявом желтом котелке и с грушевидным малиновым носом.',
    'В клетчатых брюках и лакированных ботинках выехал на сцену на обыкновенном двухколесном велосипеде.', 
    'Под звуки фокстрота он сделал круг.', 
    'А затем испустил победный вопль, от чего велосипед поднялся на дыбы.', 
    'Проехавшись на одном заднем колесе, человек перевернулся вверх ногами.' 
    'Ухитрился на ходу отвинтить переднее колесо и пустить его за кулисы.', 
    'А затем продолжал путь на одном колесе, вертя педали руками.',
    "На высокой металлической мачте с седлом наверху,",
    "C одним колесом выехала полная блондинка в трико.",
    "Юбочка ее была усеяна серебряными звездами.",
    "Она начала ездить по кругу по арене.",
    "Человек встречал ее приветственными криками.",
    "Ногой он снимал котелок с головы при встрече.",
    "Наконец, прикатил мальчик лет восьми.",
    "У него было старческое лицо и маленький велосипед.",
    "Велосипед был с приделанным автомобильным гудком.",
    "Мальчик маневрировал между взрослыми на сцене.",
    "Под барабанную дробь они подъехали к краю сцены.",
    "Зрители ахнули и откинулись назад в страхе.",
    "Им казалось, что трое упадут в оркестр.",
] - 1 голос, плохо с ударениями

en_test = ['A small man in a holey yellow bowler hat and a pear-shaped crimson nose.',
    'In checkered trousers and patent leather boots rode onto the stage on an ordinary two-wheeled bicycle.',
    'He made a circle to the sound of a foxtrot.', 
    'And then let out a triumphant cry, causing the bicycle to rear up.',
    'Having ridden on one rear wheel, the man turned upside down.', 
    'Managed to unscrew the front wheel while moving and let it go behind the scenes.',
    'And then continued on one wheel, turning the pedals with his hands.',
    "On a tall metal pole with a saddle on top,",
    "a full blonde in tights rode out with one wheel.",
    "Her skirt was studded with silver stars.",
    "She started riding in circles around the arena.",
    "The man greeted her with loud shouts.",
    "With his foot, he knocked off his hat when meeting.",
    "Finally, a little boy around eight years old rode out.",
    "He had an old man’s face and a tiny bike.",
    "The bike had a big car horn attached to it.",
    "The boy weaved between adults on the stage.",
    "Under the drumroll, they approached the stage edge.",
    "The audience gasped and leaned back in fear.",
    "They thought all three would fall into the orchestra.",
    ] - 2 мужчких голоса

deu_test = ['Ein kleiner Mann mit einer undichten gelben Melone und einer birnenförmigen purpurnen Nase.',
    'Er trug karierte Hosen und Lackstiefel und fuhr mit einem gewöhnlichen zweirädrigen Fahrrad auf die Bühne.',
    'Er machte einen Kreis zu den Klängen des Foxtrotts.', 
    'Und dann stieß er einen Siegesschrei aus, wodurch das Fahrrad aufbäumte.', 
    'Nachdem er auf einem Hinterrad mitgefahren war, drehte sich der Mann auf den Kopf.',
    'Ich habe es geschafft, während der Fahrt das Vorderrad abzuschrauben und es hinter den Kulissen laufen zu lassen.', 
    'Und dann fuhr er auf einem Rad weiter und drehte die Pedale mit seinen Händen.',
    "Auf einem hohen Metallmast mit Sattel oben,",
    "fuhr eine blonde Frau in Strumpfhosen mit einem Rad.",
    "Ihr Rock war mit silbernen Sternen übersät.",
    "Sie begann, im Kreis um die Arena zu fahren.",
    "Der Mann begrüßte sie mit lauten Rufen.",
    "Mit seinem Fuß stieß er seinen Hut ab bei der Begegnung.",
    "Schließlich fuhr ein kleiner Junge von etwa acht Jahren vor.",
    "Er hatte ein greisenhaftes Gesicht und ein kleines Fahrrad.",
    "Das Fahrrad hatte eine große Autohupe angebracht.",
    "Der Junge schlängelte sich zwischen den Erwachsenen hindurch.",
    "Unter Trommelwirbel fuhren sie an den Bühnenrand.",
    "Das Publikum schnappte nach Luft und lehnte sich zurück.",
    "Sie dachten, alle drei würden ins Orchester stürzen.",
] - 2 голоса (м и ж)

urd_test = ['پیلے رنگ کی بولر ہیٹ اور ناشپاتی کی شکل والی سرخ رنگ کی ناک میں ایک چھوٹا آدمی۔',
    'چیکرڈ ٹراؤزر اور پیٹنٹ چمڑے کے جوتے پہنے وہ ایک عام دو پہیوں والی سائیکل پر سٹیج پر پہنچا۔',
    'اس نے لومڑی کی آوازوں کا دائرہ بنایا۔',
    'اور پھر اس نے جیت کا نعرہ لگایا، جس سے سائیکل پیچھے ہو گئی۔',
    'ایک پچھلے پہیے پر سوار ہونے کے بعد آدمی الٹا ہو گیا۔',
    'میں حرکت کرتے ہوئے سامنے والے پہیے کو کھولنے میں کامیاب ہوگیا اور اسے پردے کے پیچھے جانے دیا۔',
    'اور پھر اس نے اپنے ہاتھوں سے پیڈل گھماتے ہوئے ایک پہیے پر اپنا سفر جاری رکھا۔',
    "ایک لمبے دھاتی ستون پر زین کے ساتھ،",
    "ایک مکمل سنہری بالوں والی ٹائٹس میں ایک پہیہ پر سوار ہوئی۔",
    "اس کا سکرٹ چاندی کے ستاروں سے جڑا ہوا تھا۔",
    "اس نے میدان میں دائرے میں گھومنا شروع کیا۔",
    "آدمی نے اونچی آواز میں چیخوں کے ساتھ اس کا استقبال کیا۔",
    "اس نے ملاقات کے دوران اپنے پاؤں سے ہیٹ اتار لیا۔",
    "آخرکار، تقریباً آٹھ سال کا ایک چھوٹا لڑکا سامنے آیا۔",
    "اس کے چہرے پر بوڑھا پن تھا اور چھوٹی سی سائیکل تھی۔",
    "سائیکل کے ساتھ ایک بڑی کار کا ہارن لگا ہوا تھا۔",
    "لڑکا اسٹیج پر بڑوں کے درمیان سے گزرا۔",
    "ڈھول کی آواز کے تحت وہ اسٹیج کے کنارے پہنچ گئے۔",
    "ناظرین نے چونک کر پیچھے کی طرف ہٹ گئے۔",
    "انہیں لگا کہ تینوں اپنے وہیکل سمیت آرکسٹرا میں گر جائیں گے۔",
] - 1 голос

ara_test = ['رجل صغير يرتدي قبعة صفراء متسربة وأنف قرمزي على شكل كمثرى.',
    'كان يرتدي بنطالاً مربعات وحذاءً جلديًا لامعًا، وركب على المسرح على دراجة عادية ذات عجلتين.',
    'قام بعمل دائرة على أصوات الفوكستروت.',
    'ثم أطلق صرخة النصر، مما دفع الدراجة إلى الوقوف.',
    'وبعد الركوب على عجلة خلفية واحدة، انقلب الرجل رأسًا على عقب.',
    'تمكنت من فك العجلة الأمامية أثناء التحرك وتركها خلف الكواليس.',
    'وبعد ذلك واصل رحلته على عجلة واحدة، وهو يحرك الدواسات بيديه.',
    "على عمود معدني طويل مع سرج في الأعلى،",
    "خرجت امرأة شقراء ممتلئة ترتدي لباس ضيق وعجلة واحدة.",
    "كان تنورتها مرصعًا بالنجوم الفضية.",
    "بدأت تدور في دائرة حول الساحة.",
    "رحب بها الرجل بصيحات تحية.",
    "بقدمه خلع قبعة الرأس عند اللقاء.",
    "أخيرًا، جاء صبي صغير يبلغ حوالي ثماني سنوات.",
    "كان لديه وجه شبيه بالشيخوخة ودراجة صغيرة.",
    "كانت الدراجة مزودة ببوق سيارة ضخم.",
    "تجول الصبي بين البالغين على المسرح.",
    "تحت صوت الطبول، اقتربوا من حافة المسرح.",
    "أخذ الجمهور نفسًا عميقًا وتراجع خوفًا.",
    "ظنوا أن الثلاثة سيسقطون في الأوركسترا.",
] - 1 голос

hin_test = [
    "छोटा आदमी फटे हुए पीले टोपी और नाशपाती जैसी लाल नाक के साथ।",
    "चेक पैंट और पॉलिश किए हुए जूते पहने हुए, वह मंच पर साधारण दो पहियों वाली साइकिल पर आया।",
    "फॉक्सट्रॉट संगीत के साथ उसने एक चक्कर लगाया।",
    "फिर उसने विजय की चिल्लाहट लगाई, जिससे साइकिल उठी।",
    "पीछे के पहिए पर सवारी करते हुए, आदमी उल्टा हो गया।",
    "उसने चलते-चलते आगे का पहिया हटा दिया और उसे पर्दे के पीछे भेजा।",
    "फिर उसने एक पहिए पर यात्रा जारी रखी, और हाथों से पैडल मारे।",
    "एक ऊँचे धातु के खंभे पर ऊपरी हिस्से में काठी थी।",
    "एक पहिए पर, एक पूरी गोरी महिला तंग कपड़े में आई।",
    "उसका स्कर्ट चांदी के सितारों से सजा हुआ था।",
    "वह सर्कल में घूमने लगी।",
    "आदमी ने जोर से चिल्ला कर उसे बधाई दी।",
    "मुलाकात के दौरान उसने पैर से टोपी हटा दी।",
    "अंत में, लगभग आठ साल का एक लड़का आ गया।",
    "उसका चेहरा बूढ़ा जैसा था और उसकी एक छोटी साइकिल थी।",
    "साइकिल में एक बड़ा कार हॉर्न लगा हुआ था।",
    "लड़का मंच पर बड़ों के बीच से घूम रहा था।",
    "ड्रम की धड़कन के साथ, वे मंच के किनारे पहुंचे।",
    "दर्शक डर से पीछे हट गए।",
    "उन्हें लगा कि तीनों ऑर्केस्ट्रा में गिर जाएंगे।",
] - 1-2 голоса (?), шум на некоторых аудио

ben_test = [
    "ছোট মানুষটি ছিদ্রযুক্ত হলুদ টুপিতে এবং নাশপাতি আকৃতির লাল নাক নিয়ে।",
    "চেক প্যান্ট এবং পালিশ জুতা পরে, সে মঞ্চে সাধারণ দুই চাকার সাইকেল নিয়ে উঠল।",
    "ফক্সট্রট সুরের সাথে, সে একটি বৃত্ত করল।",
    "তারপর সে বিজয়ের চিৎকার করল, এবং সাইকেল দাঁড়িয়ে গেল।",
    "পিছনের চাকার উপর চলতে চলতে, লোকটি উল্টো হয়ে গেল।",
    "সে সামনের চাকা খুলে ফেলে সেটিকে পর্দার পেছনে ছুড়ে দিল।",
    "তারপর সে এক চাকার উপর চালিয়ে যেতে থাকল, হাতে প্যাডেল ঘুরিয়ে।",
    "উঁচু ধাতব খুঁটির উপরে একটি আসন ছিল।",
    "এক চাকার উপর, এক মোটা সোনালি চুলের মহিলা ত্রিকো পরিহিত অবস্থায় বেরিয়ে এল।",
    "তার স্কার্ট রূপালী তারায় ভরা ছিল।",
    "সে বৃত্তে ঘুরতে শুরু করল।",
    "লোকটি তাকে উচ্চস্বরে চিৎকার করে অভিবাদন জানাল।",
    "পায়ের সাহায্যে সে টুপি খুলে ফেলল যখন তাদের দেখা হল।",
    "অবশেষে, প্রায় আট বছর বয়সের একটি ছোট ছেলে এসে পড়ল।",
    "তার মুখ বয়স্ক লোকের মতো ছিল এবং তার একটি ছোট সাইকেল ছিল।",
    "সাইকেলটির সাথে একটি বড় গাড়ির হর্ন লাগানো ছিল।",
    "ছেলেটি মঞ্চের উপর বড়দের মধ্যে দিয়ে ঘোরাঘুরি করল।",
    "ড্রামের আওয়াজের সাথে, তারা মঞ্চের প্রান্তে পৌঁছাল।",
    "দর্শকরা ভয়ে সরে গেল।",
    "তারা ভেবেছিল তিনজনই অর্কেস্ট্রায় পড়ে যাবে।",
] - 1 голос 

mya_test = [
    "အကွက်ထဲမှာ စိန်တောက်ကပ်ပြီး အလျားနည်းတဲ့ လူလေးတစ်ယောက်။",
    "စစ်ကိုင်းရေတွင်းနဲ့ ကြမ်းတမ်းတဲ့ဖိနပ်ဝတ်ပြီး နှစ်ဘီးစက်ဘီးနဲ့ ဇာတ်ရုံကို ဝင်လာတယ်။",
    "ဖောက်စထရော့သံတိတ်နဲ့ သူက အမှတ်တရ လှည့်ပတ်ပြီး။",
    "ပြီးတော့ သူက အောင်မြင်မှုကို ထင်ရှားစွာ ဂေါ်ရပ်ပြခဲ့တာ။",
    "နောက်ဘီးတစ်ဘီးပေါ်မှာ စီးနင်းရင်း သူ့ကို ရှိခိုးခဲ့တယ်။",
    "မောင်းနေစဉ် မျက်နာဘီးကို ခွာပြီး ဇာတ်ခုံအပြင်ဘက်က ဖြုတ်လိုက်တယ်။",
    "ပြီးတော့ သူက လက်တွေဖြင့် အောက်မှပတ်ရင်း သွားခဲ့တယ်။",
    "အမြင့်မားတဲ့ သံတံတားတစ်ခုအပေါ်မှာ အစွန်းမှာ ခုံရှိတယ်။",
    "တစ်ဘီးဖြင့် အမဲဖြူဝတ်ဆန်ပြည့်နေတဲ့ လူအမျိုးသမီးတစ်ယောက်ထွက်လာတယ်။",
    "သူမရဲ့ရှပ်စကတ်ကို ငွေရောင်ကြယ်လေးတွေနဲ့ ပြည့်နှက်နေခဲ့တယ်။",
    "သူမက အဝိုင်းလေးနဲ့ လှည့်ပတ်စီးနင်းသွားတယ်။",
    "သူ့ကိုတွေ့တော့ လူတစ်ယောက်က ကြီးမြတ်တဲ့ အသံနဲ့ ကြိုဆိုတယ်။",
    "သူနဲ့ တွေ့ဆုံနေစဉ် သူ့ချစ်သူက ခေါင်းစွပ်တစ်ခုကို ချခဲ့တယ်။",
    "နောက်ဆုံးတွင် အရွယ်တင်နှစ်ရှစ်ခန့်ရှိတဲ့ ဆင်ဆာလေးတစ်ယောက်က လာပြီ။",
    "သူ့ရဲ့မျက်နှာမှာ အိုမင်းသော အသွင်ကဲ့သို့ရှိခဲ့တယ်။",
    "သူ့စက်ဘီးက ကားကဲ့သို့သော မြေပုံတစ်ခုနဲ့ ထည့်ထားတယ်။",
    "လူကြီးတွေကြားက လူကလေးက အရင်အရင်လိုပဲ အရပ်ပျက်နေခဲ့တယ်။",
    "ဒရမ်သံလက်နှင့်အတူ သူတို့ဟာ ဇာတ်ခုံရဲ့ နောက်ဆုံးအစွန်းကို ရောက်လာခဲ့တယ်။",
    "ကြည့်ရှုသူတွေက အံ့အားသင့်ပြီး နောက်ကျတိုးခဲ့တယ်။",
    "သူတို့စိတ်ထင်ယောင်ပြီး နှစ်ယောက်လုံး အုပ်စုမှာ ကာလတွင်းဖြစ်မယ်လို့ထင်တယ်။",
] - 1-2 голоса ??

nld_test = [
    "Een klein mannetje met een kapotte gele bolhoed en een peervormige rode neus.",
    "Gekleed in geruite broek en gepoetste schoenen, reed hij het podium op met een gewone tweewieler.",
    "Op de klanken van de foxtrot reed hij een rondje.",
    "Daarna slaakte hij een triomfantelijke kreet, waardoor de fiets steigerde.",
    "Terwijl hij op het achterwiel reed, sloeg de man over de kop.",
    "Hij slaagde erin om tijdens het rijden het voorwiel los te draaien en het achter de coulissen te sturen.",
    "Daarna reed hij verder op één wiel, met zijn handen aan de pedalen.",
    "Op een hoge metalen paal met een zadel bovenop,",
    "Op één wiel kwam een dikke blondine in een strak pak naar buiten.",
    "Haar rokje was bezaaid met zilveren sterren.",
    "Ze begon in een cirkel rond de arena te rijden.",
    "De man begroette haar met luide kreten.",
    "Met zijn voet tikte hij zijn hoed af bij de ontmoeting.",
    "Eindelijk kwam er een jongetje van ongeveer acht jaar oud aan.",
    "Hij had een oud gezicht en een kleine fiets.",
    "De fiets had een grote claxon.",
    "De jongen laveerde tussen de volwassenen op het podium.",
    "Onder het geluid van tromgeroffel naderden ze de rand van het podium.",
    "Het publiek slaakte een zucht van opluchting en leunde achterover van angst.",
    "Ze dachten dat de drie met hun voertuigen in het orkest zouden vallen.",
] - 1-2 голоса (?) женские!!!

fin_test = [
    "Pieni mies rikkinäisessä keltaisessa hatussa.",
    "Päärynänmuotoinen punainen nenä.",
    "Ruudullisissa housuissa ja kiillotetuissa kengissä.",
    "Hän ajoi näyttämölle tavallisella kaksipyöräisellä pyörällä.",
    "Fox-trot musiikin tahdissa hän teki kierroksen.",
    "Sitten hän päästi voittoisan huudon.",
    "Pyörä nousi pystyyn huudon myötä.",
    "Hän ajoi yhdellä takapyörällä ympäri.",
    "Hän onnistui irrottamaan etupyörän.",
    "Hän jatkoi matkaa yhdellä pyörällä.",
    "Korkealla metallipylväällä oli satula.",
    "Yksi pyörä ilmestyi näyttämölle täyteläisen blondin alla.",
    "Hänen hameensa oli täynnä hopeisia tähtiä.",
    "Hän alkoi ajaa ympyrää areenan ympäri.",
    "Mies tervehti häntä kovilla huudoilla.",
    "Hän otti hatun jalallaan pois tervehtiessään.",
    "Lopulta saapui noin kahdeksanvuotias poika.",
    "Hänellä oli vanhennut kasvot ja pieni polkupyörä.",
    "Pyörässä oli valtava auton torvi kiinni.",
    "Poika pujotteli aikuisten välissä lavalla.",
    "Rummun pärinän säestyksellä he lähestyivät lavan reunaa.",
    "Yleisö huokaisi pelosta ja vetäytyi taaksepäin.",
    "He luulivat kolmen pyörineen kaatuvan orkesteriin."
] - 1 голос

heb_test = [
    "איש קטן עם כובע צהוב קרוע ואף אדום.",
    "לבש מכנסיים משובצים ונעליים מצוחצחות.",
    "רכב על אופניים דו גלגליים לבמה.",
    "תחת צלילי פוקסטרוט, עשה סיבוב שלם.",
    "אז הוא צעק קריאת ניצחון חזקה.",
    "האופניים התרוממו על הגלגל האחורי.",
    "הוא המשיך על גלגל אחד.",
    "הצליח לפרק את הגלגל הקדמי.",
    "שלח אותו מאחורי הקלעים.",
    "על עמוד גבוה עם מושב בפסגה.",
    "אישה בלונדינית מלאה יצאה רכובה.",
    "חצאיתה הייתה מכוסה בכוכבי כסף.",
    "היא החלה לרכב במעגלים על הבמה.",
    "האיש קרא לה ברכות בקול רם.",
    "הוא הוריד את הכובע ברגלו בברכה.",
    "לבסוף הופיע ילד בן כשמונה.",
    "פניו נראו מבוגרות והיה לו אופניים קטנים.",
    "על האופניים היה צופר מכונית גדול.",
    "הוא תמרן בין המבוגרים שעל הבמה.",
    "תחת קולות תופים הם הגיעו לקצה הבמה.",
    "הקהל נבהל ונסוג לאחור באימה.",
    "הם חשבו שהשלישייה תיפול לתזמורת."
] - 2 голоса мужских

spa_test = [
    "Un hombre pequeño con sombrero amarillo roto.",
    "Tenía una nariz roja en forma de pera.",
    "Llevaba pantalones a cuadros y zapatos brillantes.",
    "Entró en escena en una bicicleta de dos ruedas.",
    "Con la música de foxtrot, dio una vuelta.",
    "Luego lanzó un grito de victoria.",
    "La bicicleta se levantó sobre una rueda.",
    "Logró desmontar la rueda delantera.",
    "Y la envió tras bambalinas.",
    "Siguió rodando en una sola rueda.",
    "En un poste alto de metal con un asiento en la cima.",
    "Una rubia corpulenta salió montada.",
    "Su falda estaba cubierta de estrellas plateadas.",
    "Comenzó a rodar en círculos por la arena.",
    "El hombre la saludó con fuertes gritos.",
    "Con el pie, se quitó el sombrero al saludarla.",
    "Finalmente, apareció un niño de unos ocho años.",
    "Tenía una cara de anciano y una bicicleta pequeña.",
    "La bicicleta tenía una bocina de coche enorme.",
    "El niño maniobraba entre los adultos en el escenario.",
    "Al son de tambores, llegaron al borde del escenario.",
    "El público se asustó y retrocedió en pánico.",
    "Parecía que los tres caerían en la orquesta."
] - 1 голос

kan_test = [
    "ಚಿಕ್ಕ ಮನುಷ್ಯನು ಬಿಳಿಯ ಹಳದಿ ಟೋಪಿ ಹಾಕಿದ್ದ.",
    "ಅವನಿಗೆ ಆಕಾರದ ಕೆಂಪು ಮೂಗು ಇತ್ತು.",
    "ಅವನಿಗೆ ಚೆಕ್ಸ್ ಪ್ಯಾಂಟ್ ಮತ್ತು ಬಿಳಿಯ ಬೂಟುಗಳು.",
    "ಅವನು ಎರಡು ಚಕ್ರದ ಸೈಕಲ್ ಮೇಲೆ ಹತ್ತಿದನು.",
    "ಫಾಕ್ಸ್ಟ್ರಾಟ್ ಮ್ಯೂಸಿಕ್ ಕೇಳಿಸುತ್ತಿದ್ದಾಗ ಸುತ್ತು ಹಾಕಿದನು.",
    "ಆಮೇಲೆ ಅವನು ಜಯಘೋಷಿಸಿದನು.",
    "ಅವನ ಸೈಕಲ್ ಹಿಂದಿನ ಚಕ್ರದ ಮೇಲೆ ಏರಿತು.",
    "ಅವನಿಗೆ ಮುಂದಿನ ಚಕ್ರವನ್ನು ತೆಗೆದುಹಾಕಲು ಸಾಧ್ಯವಾಯಿತು.",
    "ಅವನ ಸೈಕಲ್ ಒಂದು ಚಕ್ರದಲ್ಲಿ ಸಾಗಿದೆ.",
    "ಒಂದು ಉದ್ದ ಮೊಟ್ಟೆಯ ಕಂಬದಲ್ಲಿ ತಲೆಚುಕ್ಕಿ ಇತ್ತು.",
    "ಬಲಿಷ್ಟ ಶ್ವೇತಕಾಯಿತನು ಹೊರಬಂದು ಚಲಿಸಿತು.",
    "ಅವನ ಹಣೆ ಬಿಳಿ ನಕ್ಷತ್ರಗಳಿಂದ ತುಂಬಿತ್ತು.",
    "ಅವಳು ರಿಂಗ್ ಸುತ್ತಲೂ ಸುತ್ತುತ್ತಿದ್ದಳು.",
    "ಆ ಮನುಷ್ಯನು ಅವಳನ್ನು ಉತ್ಸಾಹದಿಂದ ಹಾರೈಸಿದನು.",
    "ಅವನು ಟೋಪಿ ಕಾಲಿನಿಂದ ತೆಗೆಯುವಾಗ ಹಾರೈಸಿದನು.",
    "ಅವನು ಸುಮಾರು ಎಂಟು ವರ್ಷದ ಹುಡುಗ.",
    "ಅವನ ಚಹರೆ ವಯೋವೃದ್ಧರಂತೆ ಇತ್ತು.",
    "ಅವನ ಸೈಕಲ್ ದೊಡ್ಡ ಹೊಣೆಕಿತ್ತ ಬೈಕಿನಂತೆ ಇತ್ತು.",
    "ಅವನು ಪ್ರಾರಂಭಿಸಿದನು ವಯಸ್ಸಾದವರ ನಡುವೆ.",
    "ಅವರು ವೇದಿಕೆಯ ಅಂಚಿನಲ್ಲಿ ನಿಲ್ಲಿದರು.",
    "ಜನ ಬೆದರಿದಂತೆ ಹಿಂದಕ್ಕೆ ಸರಿದರು.",
    "ಅವರು ಹತ್ತಿರ ಬಂದಾಗ ವೇದಿಕೆ ನಡುಗುತಿತ್ತು."
] - 1 голос

ind_test = [
    "Seorang pria kecil dengan topi kuning yang robek.",
    "Hidungnya berbentuk seperti buah pir merah.",
    "Memakai celana kotak-kotak dan sepatu mengkilap.",
    "Dia memasuki panggung dengan sepeda roda dua.",
    "Dengan iringan musik foxtrot, dia berputar.",
    "Kemudian dia berteriak dengan kemenangan.",
    "Sepeda itu berdiri di atas satu roda.",
    "Dia berhasil melepas roda depan.",
    "Dan mengirimkannya ke belakang panggung.",
    "Dia terus mengayuh dengan satu roda.",
    "Di tiang logam tinggi dengan sadel di puncaknya.",
    "Seorang wanita pirang gemuk muncul mengendarai.",
    "Roknya dipenuhi dengan bintang perak.",
    "Dia mulai berkeliling arena dalam lingkaran.",
    "Pria itu menyambutnya dengan teriakan keras.",
    "Dia melepas topi dengan kakinya saat menyambut.",
    "Akhirnya, muncul seorang anak sekitar delapan tahun.",
    "Wajahnya terlihat tua dan dia memiliki sepeda kecil.",
    "Sepedanya dilengkapi dengan klakson mobil besar.",
    "Anak itu bermanuver di antara orang dewasa di panggung.",
    "Dengan suara drum, mereka mendekati tepi panggung.",
    "Penonton terkejut dan mundur ketakutan.",
    "Mereka berpikir bahwa ketiganya akan jatuh ke orkestra."
] - 1 голос (ШУМЫ)


1.⁠ ⁠Afghanistan (Dari, Pashto) [-]
2.⁠ ⁠Arabic [ara]                       mms-tts
3.⁠ ⁠Bangladesh (Bengali) [ben]         mms-tts
4.⁠ ⁠Burmese [mya]                      2 голоса в mms-tts (?)
5.⁠ ⁠Urdu [urd-script_arabic]           mms-tts
6.⁠ ⁠Dutch [nld]                        2 женских голоса в mms-tts (?)
7.⁠ ⁠English [eng]                      styletts2 (звенит голос)
8.⁠ ⁠Finnish [fin]                      mms-tts
9.⁠ ⁠German [deu]                       xtts-v2 German (de)
10.⁠ ⁠Hebrew [heb]                      2 мужских голоса в mms-tts
11.⁠ ⁠Hindi [hin]                       xtts-v2 Hindi (hi)
12.⁠ ⁠Indonesia (Bahasa Indonesia) [ind] mms-tts + шумы
13.⁠ ⁠Spanish [spa]                     mms-tts
14.⁠ ⁠Kannada [kan]                     mms-tts
15.⁠ ⁠Maori [-]
16.⁠ ⁠Malay [mkn] - tbd временно убрать
17.⁠ ⁠Norwegian [-]


styletts2 для eng и mms-tts несовместимы пакетами python
hindi: 
        > time: 2.6159260272979736
        > time: 2.4978485107421875
        > time: 1.191528081893921
        > time: 1.313737154006958
        > time: 1.6637077331542969
        > time: 1.6917545795440674
        > time: 1.5195841789245605
        > time: 1.4295592308044434
        > time: 1.3831512928009033
        > time: 1.3794527053833008
        > time: 0.8979208469390869
        > time: 1.2854959964752197
        > time: 1.330122947692871
        > time: 1.3996586799621582
        > time: 1.6271371841430664
        > time: 1.1999318599700928
        > time: 1.4147908687591553
        > time: 1.4812061786651611
        > time: 1.0772275924682617
        > time: 1.220931053161621


**installing all for sockets (python3.10):**
1. activate env with model you need
2. pip install -r requirements.txt
3. apt install libuv1 zlib1g
4. run script


<!-- **installing styletts2 for eng (https://github.com/sidharthrajaram/StyleTTS2, python 3.10):**
1. python3.10 -m venv styletts_venv
2. source styletts_venv/bin/activate
3. mkdir libritts
4. cd libritts
5. wget https://huggingface.co/yl4579/StyleTTS2-LibriTTS/resolve/main/Models/LibriTTS/config.yml
6. wget https://huggingface.co/yl4579/StyleTTS2-LibriTTS/resolve/main/Models/LibriTTS/epochs_2nd_00020.pth
7. cd ..
8. pip install styletts2
9. run script styletts_try.py (need to run first inference while downloading model) -->


**installing mms-tts (https://huggingface.co/facebook/mms-tts-ben, python3.10):**
1. python3.10 -m venv mmstts_venv
2. source mmstts_venv/bin/activate
3. pip install --upgrade transformers accelerate
4. run script


**Installing xtts-v2 with deepspeed**
1. *INSTALLING PYTHON 3.10:*
2. sudo apt update
3. sudo apt install software-properties-common -y
4. sudo add-apt-repository ppa:deadsnakes/ppa
5. sudo apt update
6. sudo apt install python3.10 python3.10-venv python3.10-dev
7. **MAKE VENV WITH PYTHON 3.10**
8. python3.10 -m venv xtts-venv
9. source xtts-venv/bin/activate
10. cd TTS
11. pip install -r requirements.txt
12. pip install -U torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124
13. python xtts_try.py
12. pip install deepspeed

**error:**
Cython.Compiler.Errors.CompileError: spacy/kb.pyx
**solution:**
sudo apt-get install build-essential
pip install --upgrade cython
pip install -U spacy[ja]

pip install -U torch==2.4.1 torchvision==0.19.1 torchaudio==2.4.1 --index-url https://download.pytorch.org/whl/cu124