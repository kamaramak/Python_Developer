from datetime import timezone

# MAIN MENU KEYBOARD
KEYBOARD_MAIN_MENU = [
    "🗓 Календарь",
    "📊 Таблицы",
    "🏆 Результаты",
    "🏁 Результаты крайней гонки",
    "⏭️ Ближайший Гран-При",
    "💬 Связаться с разработчиком",
]
KEYBOARD_USER_VERSION_KEY = "keyboard_version:user"
KEYBOARD_CURRENT_VERSION = "1.0"

# RESPONSES
NO_DATA_ERROR = "❌ Запрашиваемые данные отсутствюуют."

# DRIVERS
HARD_NAMES = {
    "MAX VERSTAPPEN": "МАКС ФЕРСТАППЕН",
    "LEWIS HAMILTON": "ЛЬЮИС ХЭМИЛЬТОН",
    "CHARLES LECLERC": "ШАРЛЬ ЛЕКЛЕР",
    "YUKI TSUNODA": "ЮКИ ЦУНОДА",
}

# SECTION PREFIXES
CALENDAR_PREFIX = "calendar"
DRIVERS_PREFIX = "drivers"
CONSTRUCTORS_PREFIX = "constructors"
STANDINGS_PREFIX = "standings"
RESULTS_PREFIX = "results"
USER_SET_PREFIX = "users:set"
USER_DATA_PREFIX = "user:data"

# CONTENT NAMES
CALENDAR_CONTENT_NAME = "календаря гонок"
DRIVERS_CONTENT_NAME = "таблицы личного зачета"
CONSTRUCTORS_CONTENT_NAME = "таблицы кубка конструкторов"
STANDINGS_CONTENT_NAME = "таблиц"
RESULTS_CONTENT_NAME = "результатов"

# BASE API_URL
API_URL = "https://f1api.dev/api/"

# Cache
RESPONSE_CACHE_TTL = 600
TRANSLATE_CACHE_TTL = 2592000

# Pagination
CALLBACK_IGNORE = "ignore"
PAGE_SIZE = 4000
PAGINATION_MAX_PAGES_ON_LINE = 5

# DATETIME FORMATS
DATETIME_FORMAT_INP = "%Y-%m-%d %H:%M:%SZ"
DATETIME_FORMAT_OUT = "%d.%m.%y | %H:%M(мск) |"
DATETIME_FORMAT_SMALL_INP = "%Y-%m-%d"
DATETIME_FORMAT_SMALL_OUT = "%d.%m.%y |"
TIME_FORMAT_INP = "%H:%M:%SZ"
TIME_FORMAT_OUT = "%H:%M"
UTC = timezone.utc
UTC_DELTA = 3
RACE_TIME = "%M:%S.%f"

# RACES DATA
FP1_ID = "fp1"
FP2_ID = "fp2"
FP3_ID = "fp3"
SPRINT_QUALY_ID = "sprintQualy"
SPRINT_RACE_ID = "sprintRace"
QUALY_ID = "qualy"
RACE_ID = "race"
EVENTS = {
    FP1_ID: "Практика 1",
    FP2_ID: "Практика 2",
    FP3_ID: "Практика 3",
    SPRINT_QUALY_ID: "Спринт-квалификация",
    SPRINT_RACE_ID: "Спринт-гонка",
    QUALY_ID: "Квалификация",
    RACE_ID: "Гонка",
}
EVENTS_FOR_REMAINING_TIME = {
    FP1_ID: "первой практики",
    FP2_ID: "второй практики",
    FP3_ID: "третьей практики",
    SPRINT_QUALY_ID: "спринт-квалификации",
    SPRINT_RACE_ID: "спринт-гонки",
    QUALY_ID: "квалификации",
    RACE_ID: "гонки",
}
EVENTS_FOR_RESULTS = {
    FP1_ID: "🔧 Практика 1",
    FP2_ID: "🔧 Практика 2",
    FP3_ID: "🔧 Практика 3",
    SPRINT_QUALY_ID: "⚡⏱️ Квалификация",
    QUALY_ID: "⏱️ Квалификация",
    SPRINT_RACE_ID: "⚡🏁 Гонка",
    RACE_ID: "🏁 Гонка",
}
COUNTRIES = {
    "Соединенные Штаты": "США",
    "Объединенные Арабские Эмираты": "ОАЭ",
}

# NATIONALITIES
NATIONALITY_TO_COUNTRY = {
    "австралийский": "Австралия",
    "австрийский": "Австрия",
    "азербайджанский": "Азербайджан",
    "албанский": "Албания",
    "алжирский": "Алжир",
    "ангольский": "Ангола",
    "андоррский": "Андорра",
    "антигуанский": "Антигуа и Барбуда",
    "аргентинский": "Аргентина",
    "армянский": "Армения",
    "афганский": "Афганистан",
    "багамский": "Багамы",
    "бангладешский": "Бангладеш",
    "барбадосский": "Барбадос",
    "бахрейнский": "Бахрейн",
    "белорусский": "Беларусь",
    "белизский": "Белиз",
    "бельгийский": "Бельгия",
    "бенинский": "Бенин",
    "болгарский": "Болгария",
    "боливийский": "Боливия",
    "боснийский": "Босния и Герцеговина",
    "ботсванский": "Ботсвана",
    "бразильский": "Бразилия",
    "брунейский": "Бруней",
    "буркинийский": "Буркина-Фасо",
    "бурундийский": "Бурунди",
    "бутанский": "Бутан",
    "вануатский": "Вануату",
    "ватиканский": "Ватикан",
    "британский": "Великобритания",
    "венгерский": "Венгрия",
    "венесуэльский": "Венесуэла",
    "восточнотиморский": "Восточный Тимор",
    "вьетнамский": "Вьетнам",
    "габонский": "Габон",
    "гаитянский": "Гаити",
    "гайанский": "Гайана",
    "гамбийский": "Гамбия",
    "ганский": "Гана",
    "гватемальский": "Гватемала",
    "гвинейский": "Гвинея",
    "гвинейско-бисауский": "Гвинея-Бисау",
    "немецкий": "Германия",
    "гондурасский": "Гондурас",
    "гренадский": "Гренада",
    "греческий": "Греция",
    "грузинский": "Грузия",
    "датский": "Дания",
    "джибутийский": "Джибути",
    "доминикский": "Доминика",
    "доминиканский": "Доминиканская Республика",
    "египетский": "Египет",
    "замбийский": "Замбия",
    "зимбабвийский": "Зимбабве",
    "израильский": "Израиль",
    "индийский": "Индия",
    "индонезийский": "Индонезия",
    "иорданский": "Иордания",
    "иракский": "Ирак",
    "иранский": "Иран",
    "ирландский": "Ирландия",
    "исландский": "Исландия",
    "испанский": "Испания",
    "итальянский": "Италия",
    "йеменский": "Йемен",
    "кабовердианский": "Кабо-Верде",
    "казахский": "Казахстан",
    "камбоджийский": "Камбоджа",
    "камерунский": "Камерун",
    "канадский": "Канада",
    "катарский": "Катар",
    "кенийский": "Кения",
    "кипрский": "Кипр",
    "киргизский": "Киргизия",
    "кирибатийский": "Кирибати",
    "китайский": "Китай",
    "колумбийский": "Колумбия",
    "коморский": "Коморы",
    "северокорейский": "КНДР",
    "костариканский": "Коста-Рика",
    "ивуарийский": "Кот-д’Ивуар",
    "кубинский": "Куба",
    "кувейтский": "Кувейт",
    "лаосский": "Лаос",
    "латвийский": "Латвия",
    "лесотский": "Лесото",
    "либерийский": "Либерия",
    "ливанский": "Ливан",
    "ливийский": "Ливия",
    "литовский": "Литва",
    "лихтенштейнский": "Лихтенштейн",
    "люксембургский": "Люксембург",
    "маврикийский": "Маврикий",
    "мавританский": "Мавритания",
    "мадагаскарский": "Мадагаскар",
    "малавийский": "Малави",
    "малайзийский": "Малайзия",
    "малийский": "Мали",
    "мальдивский": "Мальдивы",
    "мальтийский": "Мальта",
    "марокканский": "Марокко",
    "мексиканский": "Мексика",
    "мозамбикский": "Мозамбик",
    "молдавский": "Молдова",
    "монакский": "Монако",
    "монгольский": "Монголия",
    "мьянманский": "Мьянма",
    "намибийский": "Намибия",
    "науруанский": "Науру",
    "непальский": "Непал",
    "нигерский": "Нигер",
    "нигерийский": "Нигерия",
    "нидерландский": "Нидерланды",
    "никарагуанский": "Никарагуа",
    "новозеландский": "Новая Зеландия",
    "норвежский": "Норвегия",
    "эмиратский": "ОАЭ",
    "оманский": "Оман",
    "пакистанский": "Пакистан",
    "палауский": "Палау",
    "панамский": "Панама",
    "папуанский": "Папуа — Новая Гвинея",
    "парагвайский": "Парагвай",
    "перуанский": "Перу",
    "польский": "Польша",
    "португальский": "Португалия",
    "российский": "Россия",
    "руандийский": "Руанда",
    "румынский": "Румыния",
    "сальвадорский": "Сальвадор",
    "самоанский": "Самоа",
    "санмаринский": "Сан-Марино",
    "саудовский": "Саудовская Аравия",
    "северомакедонский": "Северная Македония",
    "сейшельский": "Сейшелы",
    "сенегальский": "Сенегал",
    "винсентский": "Сент-Винсент и Гренадины",
    "китсский": "Сент-Китс и Невис",
    "люсийский": "Сент-Люсия",
    "сербский": "Сербия",
    "сингапурский": "Сингапур",
    "сирийский": "Сирия",
    "словацкий": "Словакия",
    "словенский": "Словения",
    "американский": "США",
    "суринамский": "Суринам",
    "сьерралеонский": "Сьерра-Леоне",
    "таджикский": "Таджикистан",
    "таиландский": "Таиланд",
    "танзанийский": "Танзания",
    "тоголезский": "Того",
    "тонганский": "Тонга",
    "тринидадский": "Тринидад и Тобаго",
    "тувалуанский": "Тувалу",
    "тунисский": "Тунис",
    "туркменский": "Туркмения",
    "турецкий": "Турция",
    "угандийский": "Уганда",
    "узбекский": "Узбекистан",
    "украинский": "Украина",
    "уругвайский": "Уругвай",
    "фиджийский": "Фиджи",
    "филиппинский": "Филиппины",
    "финский": "Финляндия",
    "французский": "Франция",
    "хорватский": "Хорватия",
    "центральноафриканский": "ЦАР",
    "чадский": "Чад",
    "чешский": "Чехия",
    "чилийский": "Чили",
    "швейцарский": "Швейцария",
    "шведский": "Швеция",
    "шриланкийский": "Шри-Ланка",
    "эквадорский": "Эквадор",
    "экваториальногвинейский": "Экваториальная Гвинея",
    "эритрейский": "Эритрея",
    "эстонский": "Эстония",
    "эфиопский": "Эфиопия",
    "южноафриканский": "ЮАР",
    "южнокорейский": "Южная Корея",
    "южносуданский": "Южный Судан",
    "ямайский": "Ямайка",
    "японский": "Япония",
}

# EMOJIS
EMOJI_TEAMS = {
    "A.J._Watson": "🏎️",  # noqa
    "ATS_(wheels)": '<tg-emoji emoji-id="5274165143079526812">🏎️</tg-emoji>',  # noqa
    "Adams_(constructor)": "🏎️",  # noqa
    "Alex_von_Falkenhausen_Motorenbau": '<tg-emoji emoji-id="5274048225479792314">🏎️</tg-emoji>',  # noqa
    "Alfa_Romeo_in_Formula_One": '<tg-emoji emoji-id="5274117400223061885">🏎️</tg-emoji>',  # noqa
    "Alpine_F1_Team": '<tg-emoji emoji-id="5274059340855159146">🏎️</tg-emoji>',  # noqa
    "Alta_auto_racing_team": '<tg-emoji emoji-id="5273998610017587485">🏎️</tg-emoji>',  # noqa
    "Amon_(Formula_One_team)": '<tg-emoji emoji-id="5274124319415376547">🏎️</tg-emoji>',  # noqa
    "Andrea_Moda_Formula": '<tg-emoji emoji-id="5274210759927178230">🏎️</tg-emoji>',  # noqa
    "Anglo_American_Racers": '<tg-emoji emoji-id="5273832162855002681">🏎️</tg-emoji>',  # noqa
    "Apollon_(Formula_One)": '<tg-emoji emoji-id="5274277529488756566">🏎️</tg-emoji>',  # noqa
    "Arrows_Grand_Prix_International": '<tg-emoji emoji-id="5274000680191827049">🏎️</tg-emoji>',  # noqa
    "Arzani-Volpini": '<tg-emoji emoji-id="5273742140340476006">🏎️</tg-emoji>',  # noqa
    "Aston_Butterworth": "🏎️",  # noqa
    "Aston_Martin_in_Formula_One": '<tg-emoji emoji-id="5273975030647136615">🏎️</tg-emoji>',  # noqa
    "Audi_in_Formula_One": '<tg-emoji emoji-id="5274057326515491047">🏎️</tg-emoji>',  # noqa
    "Automobiles_Gonfaronnaises_Sportives": '<tg-emoji emoji-id="5274029606796565121">🏎️</tg-emoji>',  # noqa
    "BMW": '<tg-emoji emoji-id="5273752499801598194">🏎️</tg-emoji>',  # noqa
    "BMW_Sauber": '<tg-emoji emoji-id="5273987675030852174">🏎️</tg-emoji>',  # noqa
    "BRM": '<tg-emoji emoji-id="5273833696158321885">🏎️</tg-emoji>',  # noqa
    "Behra-Porsche": "🏎️",  # noqa
    "Bellasi": '<tg-emoji emoji-id="5274061887770758824">🏎️</tg-emoji>',  # noqa
    "Benetton_Formula": '<tg-emoji emoji-id="5274134077581073199">🏎️</tg-emoji>',  # noqa
    "Boro_(Formula_One)": '<tg-emoji emoji-id="5273904902421125931">🏎️</tg-emoji>',  # noqa
    "Brabham": '<tg-emoji emoji-id="5274148994002491517">🏎️</tg-emoji>',  # noqa
    "Brawn_GP": '<tg-emoji emoji-id="5273867622104997056">🏎️</tg-emoji>',  # noqa
    "British_American_Racing": '<tg-emoji emoji-id="5273782259629987777">🏎️</tg-emoji>',  # noqa
    "British_Racing_Partnership": '<tg-emoji emoji-id="5274056209823997413">🏎️</tg-emoji>',  # noqa
    "Bromme": "🏎️",  # noqa
    "Bugatti": '<tg-emoji emoji-id="5274235318550169673">🏎️</tg-emoji>',  # noqa
    "Cadillac_in_Formula_One": '<tg-emoji emoji-id="5273900465719911208">🏎️</tg-emoji>',  # noqa
    "Caterham_F1": '<tg-emoji emoji-id="5273824234345372891">🏎️</tg-emoji>',  # noqa
    "Christensen_(constructor)": "🏎️",  # noqa
    "Cisitalia": '<tg-emoji emoji-id="5274077255163750770">🏎️</tg-emoji>',  # noqa
    "Connaught_Engineering": '<tg-emoji emoji-id="5273913728578918202">🏎️</tg-emoji>',  # noqa
    "Connew": '<tg-emoji emoji-id="5273801724421772636">🏎️</tg-emoji>',  # noqa
    "Cooper_Car_Company": '<tg-emoji emoji-id="5274209235213785596">🏎️</tg-emoji>',  # noqa
    "Dallara": '<tg-emoji emoji-id="5273851936884427238">🏎️</tg-emoji>',  # noqa
    "De_Tomaso": '<tg-emoji emoji-id="5273719291114462437">🏎️</tg-emoji>',  # noqa
    "Deidt": "🏎️",  # noqa
    "Del_Roy": "🏎️",  # noqa
    "Derrington-Francis": "🏎️",  # noqa
    "Dunn_Engineering": "🏎️",  # noqa
    "Ecurie_Nationale_Belge": "🏎️",  # noqa
    "Eisenacher_Motorenwerk": '<tg-emoji emoji-id="5274199180695347875">🏎️</tg-emoji>',  # noqa
    "Elder_(constructor)": "🏎️",  # noqa
    "Emeryson": '<tg-emoji emoji-id="5273930689404769592">🏎️</tg-emoji>',  # noqa
    "English_Racing_Automobiles": "🏎️",  # noqa
    "Ensign_%28racing_team%29": '<tg-emoji emoji-id="5273766179272430259">🏎️</tg-emoji>',  # noqa
    "Enzo_Coloni_Racing_Car_Systems": '<tg-emoji emoji-id="5273860973495622217">🏎️</tg-emoji>',  # noqa
    "Epperly": "🏎️",  # noqa
    "Euro_Brun": '<tg-emoji emoji-id="5273913672744343251">🏎️</tg-emoji>',  # noqa
    "Ewing_(constructor)": "🏎️",  # noqa
    "Ferguson_Research_Ltd.": '<tg-emoji emoji-id="5276010136475834012">🏎️</tg-emoji>',  # noqa
    "Fittipaldi_%28constructor%29": '<tg-emoji emoji-id="5276113597943028800">🏎️</tg-emoji>',  # noqa
    "Fondmetal": '<tg-emoji emoji-id="5276193303946105298">🏎️</tg-emoji>',  # noqa
    "Footwork_Arrows": '<tg-emoji emoji-id="5276334165988511606">🏎️</tg-emoji>',  # noqa
    "Forti": '<tg-emoji emoji-id="5276025748681953631">🏎️</tg-emoji>',  # noqa
    "Frank_Williams_Racing_Cars": '<tg-emoji emoji-id="5276449919652106468">🏎️</tg-emoji>',  # noqa
    "Frazer_Nash": '<tg-emoji emoji-id="5273912693491802001">🏎️</tg-emoji>',  # noqa
    "Fry_(racing_team)": "🏎️",  # noqa
    "Gilby": '<tg-emoji emoji-id="5276037847604826580">🏎️</tg-emoji>',  # noqa
    "Gordini": '<tg-emoji emoji-id="5274024031929013079">🏎️</tg-emoji>',  # noqa
    "Haas_F1_Team": '<tg-emoji emoji-id="5276355567810546804">🏎️</tg-emoji>',  # noqa
    "Hall_(constructor)": "🏎️",  # noqa
    "Hersham_and_Walton_Motors": '<tg-emoji emoji-id="5274213710569706909">🏎️</tg-emoji>',  # noqa
    "Hesketh_Racing": '<tg-emoji emoji-id="5275974539786882036">🏎️</tg-emoji>',  # noqa
    "Hill_(constructor)": '<tg-emoji emoji-id="5276007039804412902">🏎️</tg-emoji>',  # noqa
    "Hispania_Racing": '<tg-emoji emoji-id="5276272906869969793">🏎️</tg-emoji>',  # noqa
    "Honda_Racing_F1": '<tg-emoji emoji-id="5276460884703613414">🏎️</tg-emoji>',  # noqa
    "Iso_Marlboro": '<tg-emoji emoji-id="5274268969618935158">🏎️</tg-emoji>',  # noqa
    "JBW": '<tg-emoji emoji-id="5276484021692439223">🏎️</tg-emoji>',  # noqa
    "Jaguar_Racing": '<tg-emoji emoji-id="5276188918784496574">🏎️</tg-emoji>',  # noqa
    "Jordan_Grand_Prix": '<tg-emoji emoji-id="5276122140632978282">🏎️</tg-emoji>',  # noqa
    "Kauhsen": '<tg-emoji emoji-id="5276445697699256946">🏎️</tg-emoji>',  # noqa
    "Klenk": "🏎️",  # noqa
    "Kojima_Engineering": '<tg-emoji emoji-id="5274276481516737765">🏎️</tg-emoji>',  # noqa
    "Kurtis_Kraft": '<tg-emoji emoji-id="5274089701978968530">🏎️</tg-emoji>',  # noqa
    "Kuzma_(constructor)": "🏎️",  # noqa
    "LDS_(automobile)": '<tg-emoji emoji-id="5276249031146769780">🏎️</tg-emoji>',  # noqa
    "LEC_(Formula_One)": '<tg-emoji emoji-id="5276294085353704701">🏎️</tg-emoji>',  # noqa
    "Lancia_in_Formula_One": '<tg-emoji emoji-id="5276303456972344030">🏎️</tg-emoji>',  # noqa
    "Langley_(constructor)": '<tg-emoji emoji-id="5274009300191188098">🏎️</tg-emoji>',  # noqa
    "Larrousse": '<tg-emoji emoji-id="5274138132030198243">🏎️</tg-emoji>',  # noqa
    "Lesovsky": "🏎️",  # noqa
    "Leyton_House": '<tg-emoji emoji-id="5276114203533411655">🏎️</tg-emoji>',  # noqa
    "Life_(Racing_Team)": '<tg-emoji emoji-id="5276186530782679157">🏎️</tg-emoji>',  # noqa
    "Ligier": '<tg-emoji emoji-id="5276361293001951403">🏎️</tg-emoji>',  # noqa
    "Lotus_F1": '<tg-emoji emoji-id="5276234578581823104">🏎️</tg-emoji>',  # noqa
    "Lotus_Racing": '<tg-emoji emoji-id="5274007741118059978">🏎️</tg-emoji>',  # noqa
    "Lyncar": '<tg-emoji emoji-id="5276341776670560297">🏎️</tg-emoji>',  # noqa
    "Maki_(cars)": '<tg-emoji emoji-id="5273765981703933096">🏎️</tg-emoji>',  # noqa
    "Manor_Motorsport": '<tg-emoji emoji-id="5276098634276968073">🏎️</tg-emoji>',  # noqa
    "March_Engineering": '<tg-emoji emoji-id="5276436253066170602">🏎️</tg-emoji>',  # noqa
    "Marchese_(constructor)": "🏎️",  # noqa
    "Martini_(cars)": '<tg-emoji emoji-id="5276217282748518980">🏎️</tg-emoji>',  # noqa
    "Marussia_F1": '<tg-emoji emoji-id="5276102400963284401">🏎️</tg-emoji>',  # noqa
    "Maserati": '<tg-emoji emoji-id="5276025705732280300">🏎️</tg-emoji>',  # noqa
    "MasterCard_Lola": '<tg-emoji emoji-id="5276240492751787276">🏎️</tg-emoji>',  # noqa
    "Matra": '<tg-emoji emoji-id="5276314293174834285">🏎️</tg-emoji>',  # noqa
    "McGuire_(Formula_One)": "🏎️",  # noqa
    "McLaren": '<tg-emoji emoji-id="5273841289660506384">🏎️</tg-emoji>',  # noqa
    "McLaren_(racing)": '<tg-emoji emoji-id="5273841289660506384">🏎️</tg-emoji>',  # noqa
    "Mercedes-Benz_in_Formula_One": '<tg-emoji emoji-id="5276358419668834057">🏎️</tg-emoji>',  # noqa
    "Merzario": '<tg-emoji emoji-id="5273929886245884044">🏎️</tg-emoji>',  # noqa
    "Meskowski": "🏎️",  # noqa
    "Midland_F1_Racing": '<tg-emoji emoji-id="5276401128823623414">🏎️</tg-emoji>',  # noqa
    "Minardi": '<tg-emoji emoji-id="5276527254833240440">🏎️</tg-emoji>',  # noqa
    "Modena_(racing_team)": '<tg-emoji emoji-id="5274148031929814845">🏎️</tg-emoji>',  # noqa
    "Monteverdi_Basel_Motors": '<tg-emoji emoji-id="5274206988945887314">🏎️</tg-emoji>',  # noqa
    "Moore_(constructor)": "🏎️",  # noqa
    "Nichels": "🏎️",  # noqa
    "Officine_Specializate_Costruzione_Automobili": '<tg-emoji emoji-id="5276231696658764287">🏎️</tg-emoji>',  # noqa
    "Olson_(constructor)": "🏎️",  # noqa
    "Onyx_(racing_team)": '<tg-emoji emoji-id="5276446646887027638">🏎️</tg-emoji>',  # noqa
    "Osella": '<tg-emoji emoji-id="5276253197265048037">🏎️</tg-emoji>',  # noqa
    "Pacific_Racing": '<tg-emoji emoji-id="5276446518038011610">🏎️</tg-emoji>',  # noqa
    "Pankratz": "🏎️",  # noqa
    "Parnelli": '<tg-emoji emoji-id="5276208014209094445">🏎️</tg-emoji>',  # noqa
    "Pawl_(constructor)": "🏎️",  # noqa
    "Penske_Racing": '<tg-emoji emoji-id="5273827958082016840">🏎️</tg-emoji>',  # noqa
    "Phillips_(constructor)": "🏎️",  # noqa
    "Porsche_in_Formula_One": '<tg-emoji emoji-id="5276509306164909442">🏎️</tg-emoji>',  # noqa
    "Prost_Grand_Prix": '<tg-emoji emoji-id="5276147639853814638">🏎️</tg-emoji>',  # noqa
    "Protos_(constructor)": '<tg-emoji emoji-id="5276418931463073873">🏎️</tg-emoji>',  # noqa
    "RAM_Racing": '<tg-emoji emoji-id="5276134093526962163">🏎️</tg-emoji>',  # noqa
    "RB_Formula_One_Team": '<tg-emoji emoji-id="5273774399839837393">🏎️</tg-emoji>',  # noqa
    "RE_%28automobile%29": '<tg-emoji emoji-id="5276367516409567495">🏎️</tg-emoji>',  # noqa
    "Racing_Point_F1_Team": '<tg-emoji emoji-id="5276004939565403438">🏎️</tg-emoji>',  # noqa
    "Racing_Point_Force_India": '<tg-emoji emoji-id="5274129859923186460">🏎️</tg-emoji>',  # noqa
    "Rae_(motorsport)": "🏎️",  # noqa
    "Rebaque": "🏎️",  # noqa
    "Red_Bull_Racing": '<tg-emoji emoji-id="5276440109946804651">🏎️</tg-emoji>',  # noqa
    "Renault_in_Formula_One": '<tg-emoji emoji-id="5276214804552390411">🏎️</tg-emoji>',  # noqa
    "Rial_%28racing_team%29": '<tg-emoji emoji-id="5276443876633122096">🏎️</tg-emoji>',  # noqa
    "Sauber_Motorsport": '<tg-emoji emoji-id="5276199737807113992">🏎️</tg-emoji>',  # noqa
    "Scarab_(constructor)": '<tg-emoji emoji-id="5276524252651102398">🏎️</tg-emoji>',  # noqa
    "Schroeder_(constructor)": '<tg-emoji emoji-id="5276199063497247634">🏎️</tg-emoji>',  # noqa
    "Scirocco-Powell": '<tg-emoji emoji-id="5273860054372618666">🏎️</tg-emoji>',  # noqa
    "Scuderia_AlphaTauri": '<tg-emoji emoji-id="5276243649552748632">🏎️</tg-emoji>',  # noqa
    "Scuderia_Ferrari": '<tg-emoji emoji-id="5275990199237645195">🏎️</tg-emoji>',  # noqa
    "Scuderia_Milano": '<tg-emoji emoji-id="5276234857754695680">🏎️</tg-emoji>',  # noqa
    "Scuderia_Toro_Rosso": '<tg-emoji emoji-id="5276501437784824137">🏎️</tg-emoji>',  # noqa
    "Shadow_Racing_Cars": '<tg-emoji emoji-id="5276444778576255276">🏎️</tg-emoji>',  # noqa
    "Shannon_(Formula_One)": "🏎️",  # noqa
    "Sherman_(constructor)": "🏎️",  # noqa
    "Simca": '<tg-emoji emoji-id="5273794341372990722">🏎️</tg-emoji>',  # noqa
    "Simtek": '<tg-emoji emoji-id="5276297783320548012">🏎️</tg-emoji>',  # noqa
    "Snowberger": "🏎️",  # noqa
    "Spirit_(racing_team)": '<tg-emoji emoji-id="5276474254936806832">🏎️</tg-emoji>',  # noqa
    "Spyker_F1": '<tg-emoji emoji-id="5276438507924000894">🏎️</tg-emoji>',  # noqa
    "Stebro": "🏎️",  # noqa
    "Stevens_(constructor)": "🏎️",  # noqa
    "Stewart_Grand_Prix": '<tg-emoji emoji-id="5276498611696345499">🏎️</tg-emoji>',  # noqa
    "Super_Aguri_F1": '<tg-emoji emoji-id="5276408507577437660">🏎️</tg-emoji>',  # noqa
    "Surtees": '<tg-emoji emoji-id="5276433469927361571">🏎️</tg-emoji>',  # noqa
    "Sutton_(constructor)": "🏎️",  # noqa
    "Talbot-Lago": '<tg-emoji emoji-id="5276001078389806168">🏎️</tg-emoji>',  # noqa
    "Team_Lotus": '<tg-emoji emoji-id="5275988141948311713">🏎️</tg-emoji>',  # noqa
    "Team_McLaren": '<tg-emoji emoji-id="5273841289660506384">🏎️</tg-emoji>',  # noqa
    "Tec-Mec": '<tg-emoji emoji-id="5276239659528130799">🏎️</tg-emoji>',  # noqa
    "Tecno": '<tg-emoji emoji-id="5276153717232545086">🏎️</tg-emoji>',  # noqa
    "Theodore_Racing": '<tg-emoji emoji-id="5276397035719792754">🏎️</tg-emoji>',  # noqa
    "Token_(Racing_team)": '<tg-emoji emoji-id="5274265864357584491">🏎️</tg-emoji>',  # noqa
    "Toleman": '<tg-emoji emoji-id="5276023858896346360">🏎️</tg-emoji>',  # noqa
    "Toyota_Racing": '<tg-emoji emoji-id="5276199209526135985">🏎️</tg-emoji>',  # noqa
    "Trevis": "🏎️",  # noqa
    "Trojan_(Racing_team)": "🏎️",  # noqa
    "Turner_(constructor)": '<tg-emoji emoji-id="5273947242208730352">🏎️</tg-emoji>',  # noqa
    "Tyrrell_Racing": '<tg-emoji emoji-id="5276369015353151352">🏎️</tg-emoji>',  # noqa
    "Vanwall": '<tg-emoji emoji-id="5276300321646219312">🏎️</tg-emoji>',  # noqa
    "Veritas_(constructor)": '<tg-emoji emoji-id="5273829250867173116">🏎️</tg-emoji>',  # noqa
    "Virgin_Racing": '<tg-emoji emoji-id="5276158403041859248">🏎️</tg-emoji>',  # noqa
    "Walter_Wolf_Racing": '<tg-emoji emoji-id="5276507330479953933">🏎️</tg-emoji>',  # noqa
    "Wetteroth": "🏎️",  # noqa
    "Williams_Grand_Prix_Engineering": '<tg-emoji emoji-id="5276076794368269727">🏎️</tg-emoji>',  # noqa
    "Zakspeed": '<tg-emoji emoji-id="5276287312190281150">🏎️</tg-emoji>',  # noqa
}

EMOJI_FLAGS = {
    "Австралия": ":flag_for_Australia:",
    "Австрия": ":flag_for_Austria:",
    "Азербайджан": ":flag_for_Azerbaijan:",
    "Албания": ":flag_for_Albania:",
    "Алжир": ":flag_for_Algeria:",
    "Ангола": ":flag_for_Angola:",
    "Андорра": ":flag_for_Andorra:",
    "Антигуа и Барбуда": ":flag_for_Antigua_&_Barbuda:",
    "Аргентина": ":flag_for_Argentina:",
    "Армения": ":flag_for_Armenia:",
    "Афганистан": ":flag_for_Afghanistan:",
    "Багамы": ":flag_for_Bahamas:",
    "Бангладеш": ":flag_for_Bangladesh:",
    "Барбадос": ":flag_for_Barbados:",
    "Бахрейн": ":flag_for_Bahrain:",
    "Беларусь": ":flag_for_Belarus:",
    "Белиз": ":flag_for_Belize:",
    "Бельгия": ":flag_for_Belgium:",
    "Бенин": ":flag_for_Benin:",
    "Болгария": ":flag_for_Bulgaria:",
    "Боливия": ":flag_for_Bolivia:",
    "Босния и Герцеговина": ":flag_for_Bosnia_&_Herzegovina:",
    "Ботсвана": ":flag_for_Botswana:",
    "Бразилия": ":flag_for_Brazil:",
    "Бруней": ":flag_for_Brunei:",
    "Буркина-Фасо": ":flag_for_Burkina_Faso:",
    "Бурунди": ":flag_for_Burundi:",
    "Бутан": ":flag_for_Bhutan:",
    "Вануату": ":flag_for_Vanuatu:",
    "Ватикан": ":flag_for_Vatican_City:",
    "Великобритания": ":flag_for_United_Kingdom:",
    "Венгрия": ":flag_for_Hungary:",
    "Венесуэла": ":flag_for_Venezuela:",
    "Восточный Тимор": ":flag_for_Timor-Leste:",
    "Вьетнам": ":flag_for_Vietnam:",
    "Габон": ":flag_for_Gabon:",
    "Гаити": ":flag_for_Haiti:",
    "Гайана": ":flag_for_Guyana:",
    "Гамбия": ":flag_for_Gambia:",
    "Гана": ":flag_for_Ghana:",
    "Гватемала": ":flag_for_Guatemala:",
    "Гвинея": ":flag_for_Guinea:",
    "Гвинея-Бисау": ":flag_for_Guinea-Bissau:",
    "Германия": ":flag_for_Germany:",
    "Гондурас": ":flag_for_Honduras:",
    "Гренада": ":flag_for_Grenada:",
    "Греция": ":flag_for_Greece:",
    "Грузия": ":flag_for_Georgia:",
    "Дания": ":flag_for_Denmark:",
    "Джибути": ":flag_for_Djibouti:",
    "Доминика": ":flag_for_Dominica:",
    "Доминиканская Республика": ":flag_for_Dominican_Republic:",
    "Египет": ":flag_for_Egypt:",
    "Замбия": ":flag_for_Zambia:",
    "Зимбабве": ":flag_for_Zimbabwe:",
    "Израиль": ":flag_for_Israel:",
    "Индия": ":flag_for_India:",
    "Индонезия": ":flag_for_Indonesia:",
    "Иордания": ":flag_for_Jordan:",
    "Ирак": ":flag_for_Iraq:",
    "Иран": ":flag_for_Iran:",
    "Ирландия": ":flag_for_Ireland:",
    "Исландия": ":flag_for_Iceland:",
    "Испания": ":flag_for_Spain:",
    "Италия": ":flag_for_Italy:",
    "Йемен": ":flag_for_Yemen:",
    "Кабо-Верде": ":flag_for_Cape_Verde:",
    "Казахстан": ":flag_for_Kazakhstan:",
    "Камбоджа": ":flag_for_Cambodia:",
    "Камерун": ":flag_for_Cameroon:",
    "Канада": ":flag_for_Canada:",
    "Катар": ":flag_for_Qatar:",
    "Кения": ":flag_for_Kenya:",
    "Кипр": ":flag_for_Cyprus:",
    "Киргизия": ":flag_for_Kyrgyzstan:",
    "Кирибати": ":flag_for_Kiribati:",
    "Китай": ":flag_for_China:",
    "Колумбия": ":flag_for_Colombia:",
    "Коморы": ":flag_for_Comoros:",
    "КНДР": ":flag_for_North_Korea:",
    "Коста-Рика": ":flag_for_Costa_Rica:",
    "Кот-д’Ивуар": ":flag_for_Côte_d’Ivoire:",
    "Куба": ":flag_for_Cuba:",
    "Кувейт": ":flag_for_Kuwait:",
    "Лаос": ":flag_for_Laos:",
    "Латвия": ":flag_for_Latvia:",
    "Лесото": ":flag_for_Lesotho:",
    "Либерия": ":flag_for_Liberia:",
    "Ливан": ":flag_for_Lebanon:",
    "Ливия": ":flag_for_Libya:",
    "Литва": ":flag_for_Lithuania:",
    "Лихтенштейн": ":flag_for_Liechtenstein:",
    "Люксембург": ":flag_for_Luxembourg:",
    "Маврикий": ":flag_for_Mauritius:",
    "Мавритания": ":flag_for_Mauritania:",
    "Мадагаскар": ":flag_for_Madagascar:",
    "Малави": ":flag_for_Malawi:",
    "Малайзия": ":flag_for_Malaysia:",
    "Мали": ":flag_for_Mali:",
    "Мальдивы": ":flag_for_Maldives:",
    "Мальта": ":flag_for_Malta:",
    "Марокко": ":flag_for_Morocco:",
    "Мексика": ":flag_for_Mexico:",
    "Мозамбик": ":flag_for_Mozambique:",
    "Молдова": ":flag_for_Moldova:",
    "Монако": ":flag_for_Monaco:",
    "Монголия": ":flag_for_Mongolia:",
    "Мьянма": ":flag_for_Myanmar:",
    "Намибия": ":flag_for_Namibia:",
    "Науру": ":flag_for_Nauru:",
    "Непал": ":flag_for_Nepal:",
    "Нигер": ":flag_for_Niger:",
    "Нигерия": ":flag_for_Nigeria:",
    "Нидерланды": ":flag_for_Netherlands:",
    "Никарагуа": ":flag_for_Nicaragua:",
    "Новая Зеландия": ":flag_for_New_Zealand:",
    "Норвегия": ":flag_for_Norway:",
    "ОАЭ": ":flag_for_United_Arab_Emirates:",
    "Оман": ":flag_for_Oman:",
    "Пакистан": ":flag_for_Pakistan:",
    "Палау": ":flag_for_Palau:",
    "Панама": ":flag_for_Panama:",
    "Папуа — Новая Гвинея": ":flag_for_Papua_New_Guinea:",
    "Парагвай": ":flag_for_Paraguay:",
    "Перу": ":flag_for_Peru:",
    "Польша": ":flag_for_Poland:",
    "Португалия": ":flag_for_Portugal:",
    "Россия": ":flag_for_Russia:",
    "Руанда": ":flag_for_Rwanda:",
    "Румыния": ":flag_for_Romania:",
    "Сальвадор": ":flag_for_El_Salvador:",
    "Самоа": ":flag_for_Samoa:",
    "Сан-Марино": ":flag_for_San_Marino:",
    "Саудовская Аравия": ":flag_for_Saudi_Arabia:",
    "Северная Македония": ":flag_for_North_Macedonia:",
    "Сейшелы": ":flag_for_Seychelles:",
    "Сенегал": ":flag_for_Senegal:",
    "Сент-Винсент и Гренадины": ":flag_for_Saint_Vincent_&_Grenadines:",
    "Сент-Китс и Невис": ":flag_for_Saint_Kitts_&_Nevis:",
    "Сент-Люсия": ":flag_for_Saint_Lucia:",
    "Сербия": ":flag_for_Serbia:",
    "Сингапур": ":flag_for_Singapore:",
    "Сирия": ":flag_for_Syria:",
    "Словакия": ":flag_for_Slovakia:",
    "Словения": ":flag_for_Slovenia:",
    "США": ":flag_for_United_States:",
    "Суринам": ":flag_for_Suriname:",
    "Сьерра-Леоне": ":flag_for_Sierra_Leone:",
    "Таджикистан": ":flag_for_Tajikistan:",
    "Таиланд": ":flag_for_Thailand:",
    "Танзания": ":flag_for_Tanzania:",
    "Того": ":flag_for_Togo:",
    "Тонга": ":flag_for_Tonga:",
    "Тринидад и Тобаго": ":flag_for_Trinidad_&_Tobago:",
    "Тувалу": ":flag_for_Tuvalu:",
    "Тунис": ":flag_for_Tunisia:",
    "Туркмения": ":flag_for_Turkmenistan:",
    "Турция": ":flag_for_Turkey:",
    "Уганда": ":flag_for_Uganda:",
    "Узбекистан": ":flag_for_Uzbekistan:",
    "Украина": ":flag_for_Ukraine:",
    "Уругвай": ":flag_for_Uruguay:",
    "Фиджи": ":flag_for_Fiji:",
    "Филиппины": ":flag_for_Philippines:",
    "Финляндия": ":flag_for_Finland:",
    "Франция": ":flag_for_France:",
    "Хорватия": ":flag_for_Croatia:",
    "ЦАР": ":flag_for_Central_African_Republic:",
    "Чад": ":flag_for_Chad:",
    "Чехия": ":flag_for_Czechia:",
    "Чили": ":flag_for_Chile:",
    "Швейцария": ":flag_for_Switzerland:",
    "Швеция": ":flag_for_Sweden:",
    "Шри-Ланка": ":flag_for_Sri_Lanka:",
    "Эквадор": ":flag_for_Ecuador:",
    "Экваториальная Гвинея": ":flag_for_Equatorial_Guinea:",
    "Эритрея": ":flag_for_Eritrea:",
    "Эстония": ":flag_for_Estonia:",
    "Эфиопия": ":flag_for_Ethiopia:",
    "ЮАР": ":flag_for_South_Africa:",
    "Южная Корея": ":flag_for_South_Korea:",
    "Южный Судан": ":flag_for_South_Sudan:",
    "Ямайка": ":flag_for_Jamaica:",
    "Япония": ":flag_for_Japan:",
}
