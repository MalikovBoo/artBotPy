import random
import sqlite3
from sqlite3 import Error

# Создаём нужные таблицы
__create_style_table = """
CREATE TABLE IF NOT EXISTS style (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  style_name TEXT NOT NULL,
  dates TEXT NOT NULL
);
"""
__create_painting_table = """
CREATE TABLE IF NOT EXISTS painting (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  painting_url TEXT NOT NULL,
  painting_name TEXT NOT NULL,
  painting_date TEXT NOT NULL,
  painting_artist_id INTEGER NOT NULL,
  FOREIGN KEY (painting_artist_id) REFERENCES artist (id)
);
"""
__create_artist_table = """
CREATE TABLE IF NOT EXISTS artist (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  artist_name TEXT NOT NULL,
  country TEXT NOT NULL,
  artist_style TEXT NOT NULL
);
"""
__create_theme_table = """
CREATE TABLE IF NOT EXISTS theme (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  theme_name TEXT NOT NULL
  );
"""
__create_technique_table = """
CREATE TABLE IF NOT EXISTS technique (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  technique_name TEXT NOT NULL
  );
"""
__create_holding_place_table = """
CREATE TABLE IF NOT EXISTS holding_place (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  place_name TEXT NOT NULL,
  city TEXT NOT NULL,
  country TEXT NOT NULL
);
"""
__create_gaming_table = """
CREATE TABLE IF NOT EXISTS gaming (
  id INTEGER PRIMARY KEY AUTOINCREMENT, 
  painting_id INTEGER NOT NULL,
  holding_place_id INTEGER NOT NULL,
  style_id INTEGER NOT NULL,
  artist_id INTEGER NOT NULL,
  theme_id INTEGER NOT NULL,
  technique_id INTEGER NOT NULL, 
  FOREIGN KEY (painting_id) REFERENCES painting (id) FOREIGN KEY (holding_place_id) REFERENCES holding_place (id) 
  FOREIGN KEY (style_id) REFERENCES style (id) FOREIGN KEY (artist_id) REFERENCES artist (id) 
  FOREIGN KEY (theme_id) REFERENCES theme (id) FOREIGN KEY (technique_id) REFERENCES technique (id)
);
"""

# Заполняем нужные таблицы
create_styles = """
INSERT INTO
  style (style_name, dates)
VALUES
    ('Первобытное искусство', '50 000 - 250 лет до н.э.'),
    ('Искусство древней Греции и Древнего Рима', '650г. до н.э. - 476г. н.э.'),
    ('Византийское искусство', '476-1453 гг.'),
    ('Искусство средневековья', '500-1400 гг.'),
    ('Раннее Возрождение', '1400-1490 гг.'),
    ('Северное Возрождение', '1430-1550 гг.'),
    ('Возрождение', '1400-1550 гг.'),
    ('Высокое Возрождение', '1490-1530 гг.'),
    ('Венецианское Возрождение', '1430-1550 гг.'),
    ('Маньеризм', '1520-1600 гг.'),
    ('Золотой век голландской живописи', '1585-1702 гг.'),
    ('Барокко', '1600-1730/50 гг.'),
    ('Рококо', '1720-1780 гг.'),
    ('Классицизм', '1750-1830/50 гг.'),
    ('Романтизм', '1790-1880 гг.'),
    ('Реализм', '1830-1890 гг.'),
    ('Импрессионизм', '1865-1885 гг.'),
    ('Постимпрессионизм', '1885-1910 гг.'),
    ('Неоимпрессионизм', '1886-1906 гг.'),
    ('Ар-нуво (модерн)', '1890-1914 гг.'),
    ('Экспрессионизм', '1905-1930 гг.'),
    ('Немецкий экспрессионизм', '1905-1935 гг.'),
    ('Фовизм', '1905-1909 гг.'),
    ('Кубизм', '1907-1914 гг.'),
    ('Футуризм', '1909-1914 гг.'),
    ('Супрематизм', '1915-1925 гг.'),
    ('Дадаизм', '1916-1930 гг.'),
    ('Неопластицизм', '1917-1931 гг.'),
    ('Магический реализм', '1920-1960 гг.'),
    ('Сюрреализм', '1924-1966 гг.'),
    ('Абстрактный экспрессионизм', '1943-1965 гг.'),
    ('Живопись цветового поля', '1947-1965 гг.'),
    ('Поп-арт', '1955-1970 гг.'),
    ('Перформанс', '1960-е гг.-наст. вр.'),
    ('Минимализм', '1960-е гг.-наст. вр.'),
    ('Концептуализм', '1960-е гг.-наст. вр.');
"""
create_paintings = """
INSERT INTO
  painting (painting_url, painting_name, painting_date, painting_artist_id)
VALUES
    ('./img/zal_bykov.jpg', 'Зал быков', '16000-14000 лет до н.э.', 1),
    ('./img/venera_milosskaya.jpg', 'Венера Милосская', 'ок. 150г. до н.э.', 2),
    ('./img/christo_Pantokrator.jpg', 'Христос Пантократор', 'ок. 1261', 1),
    ('./img/oplakivanie-xrista-djotto.jpg', 'Оплакивание Христа', '1304-1306', 3),
    ('./img/Van_Eyck_-_Arnolfini_Portrait.jpg', 'Портрет четы Арнольфини', '1434', 4),
    ('./img/Botticelli-primavera.jpg', 'Весна', 'ок. 1478', 7),
    ('./img/hercules.jpg', 'Геркулес', 'ок. 1498', 5),
    ('./img/Michelangelos_Pieta.jpg', 'Пьета', '1498-1499', 9),
    ('./img/Mona_Lisa.jpg', 'Мона Лиза', 'ок. 1503-1519', 8),
    ('./img/Christ_Falling_on_the_Way_to_Calvary_-_Raphael.jpg', 'Крестный путь', 'ок. 1514-1516', 10),
    ('./img/Tizian_Venera.jpg', 'Венера Урбинская', '1538', 12),
    ('./img/Ohotniki_na_snegu.jpg', 'Охотники на снегу', '1565', 6),
    ('./img/Sovlechenie_odezd_s_Christa.jpg', 'Совлечение одежд с Христа', '1577-1579', 47),
    ('./img/Vakh.jpg', 'Вакх', 'ок. 1595', 15),
    ('./img/yudif-obezglavlivayuschaya-oloferna.jpg', 'Юдифь, обезглавливающая Олоферна', 'ок. 1620', 17),
    ('./img/Descent_From_The_Cross.jpg', 'Снятие с креста', '1612-1614', 16),
    ('./img/Apollo_and_Daphne_(Bernini).jpg', 'Апполон и Дафна', '1622-1625', 11),
    ('./img/avtoportret_Rembrandt.jpg', 'Автопортрет с широко раскрытыми глазами', '1630', 13),
    ('./img/Las_Meninas_(1656),_by_Velazquez.jpg', 'Менины', '1656', 18),
    ('./img/Devushka_s_zhemchuzhnoi_serezhkoi.jpg', 'Девушка с жемчужной сережкой', 'ок. 1665', 14),
    ('./img/Fragonard,_The_Swing.jpg', 'Качели', '1767', 19),
    ('./img/David-Oath_of_the_Horatii-1784.jpg', 'Клятва Горациев', '1784', 20),
    ('./img/Raikhenbasch.jpg', 'Верхний водопад Райхенбах, радуга', '1810', 23),
    ('./img/El_Tres_de_Mayo_by_Francisco_de_Goya.jpg', 'Третье мая 1808 года в Мадриде', '1814', 24),
    ('./img/Eugene_Delacroix_-_Le_Massacre_de_Scio.jpg', 'Резня на острове Хиос', '1824', 22),
    ('./img/Le_Bain_Turc_by_Jean_Auguste_Dominique_Ingres.jpg', 'Турецкая баня', '1862', 21),
    ('./img/manet_olympia.jpg', 'Олимпия', '1863', 25),
    ('./img/Claude_Monet_Impression,_soleil_levant.jpg', 'Восход солнца. Впечатление', '1872', 26),
    ('./img/bronz_vek.jpg', 'Бронзовый век', '1877', 48),
    ('./img/Georges_Seurat_-_Grande_Jatte.jpg', 'Воскресный день на острове Гранд-Жатт', '1884-1886', 29),
    ('./img/nochnoe_cafe.jpg', 'Ночное кафе', '1888', 28),
    ('./img/The_Scream.jpg', 'Крик', '1893', 31),
    ('./img/naturmort_s_lykovitsami.jpg', 'Натюрморт с луковицами', 'ок. 1895', 27),
    ('./img/lodki_v_Kolliure.jpg', 'Рыбацкие лодки, Колиур', '1905', 34),
    ('./img/pocelui-klimt.jpg', 'Поцелуй', '1907-1908', 30),
    ('./img/akkordeonist.jpeg', 'Аккордеонист', '1911', 35),
    ('./img/Unique_Forms_of_Continuity_in_Space.jpg', 'Уникальная формула непрерывности в пространстве', '1913', 36),
    ('./img/ulitsa_s_krasnoi_kokotkoi.jpg', 'Улица с красной кокоткой', '1914-1925', 32),
    ('./img/Red_Square.jpg', 'Красный квадрат', '1915', 37),
    ('./img/Fountain.jpg', 'Фонтан', '1917', 38),
    ('./img/vlublennie.jpg', 'Влюбленные', '1928', 41),
    ('./img/Dve_Fridy.jpg', 'Две Фриды', '1939', 40),
    ('./img/Broadway_Boogie_Woogie.jpg', 'Бродвей. Буги-вуги', '1942-1943', 39),
    ('./img/volnistie_linii.jpg', 'Волнистые линии', '1947', 42),
    ('./img/Untitled_1952_Rothko.jpg', 'Без названия', '1952', 43),
    ('./img/ulitka-matiss.jpg', 'Улитка', '1953', 33),
    ('./img/merilyn.jpg', 'Без названия, из цикла «Мэрилин»', '1967', 44),
    ('./img/Donald_Judd_multi-colored_floor_work.jpg', 'Без названия', '1968', 46),
    ('./img/i-like-america-and-america-likes-me.jpg', 'Я люблю Америку, Америка любит меня', '1974', 45),
    ('./img/fizicheskaya_nevozmozhnost_smerti_v_soznanii_zhivushego.jpg', 'Физическая невозможность смерти в сознании живущего', '1991', 49);
"""
create_artists = """
INSERT INTO
  artist (artist_name, country, artist_style)
VALUES
    ('НЕИЗВЕСТНЫЙ АВТОР', 'Неизвестно', 'Неизвестно'),
    ('АЛЕКСАНДР АНТИОХИЙСКИЙ', 'Греция', 'Скульптор эллинистической эпохи'),
    ('ДЖОТТО ДИ БОНДОНЕ', 'Италия', 'Проторенессанс'),
    ('ЯН ВАН ЭЙК', 'Нидерланды (Бельгия)', 'Северное Возрождение'),
    ('АЛЬБРЕХТ ДЮРЕР', 'Германия', 'Высокое Возрождение'),
    ('ПИТЕР БРЕЙГЕЛЬ СТАРШИЙ', 'Нидерланды (Бельгия)', 'Северное Возрождение'),
    ('САНДРО БОТТИЧЕЛЛИ', 'Италия', 'Возрождение'),
    ('ЛЕОНАРДО ДА ВИНЧИ', 'Италия', 'Высокое Возрождение'),
    ('МИКЕЛАНДЖЕЛО', 'Италия', 'Возрождение и раннее Барокко'),
    ('РАФАЭЛЬ', 'Италия', 'Высокое Возрождение'),
    ('ДЖОВАННИ ЛОРЕНЦО БЕРНИНИ', 'Италия', 'Барокко в скульптуре'),
    ('ТИЦИАН', 'Италия', 'Высокое и позднее Возрождение'),
    ('РЕМБРАНДТ', 'Нидерланды', 'Барокко'),
    ('ЯН ВЕРМЕЕР', 'Нидерланды', 'Барокко'),
    ('КАРАВАДЖО', 'Италия', 'Барокко'),
    ('ПИТЕР ПАУЛЬ РУБЕНС', 'Нидерланды (Бельгия)', 'Барокко'),
    ('АРТЕМИЗИЯ ДЖЕНТИЛЕСКИ', 'Италия', 'Барокко'),
    ('ДИЕГО ВЕЛАСКЕС', 'Испания', 'Барокко'),
    ('ЖАН-ОНОРЕ ФРАГОНАР', 'Франция', 'Рококо'),
    ('ЖАК-ЛУИ ДАВИД', 'Франция', 'Неоклассицизм'),
    ('ЖАН ОГЮСТ ДОМИНИК ЭНГР', 'Франция', 'Неоклассицизм'),
    ('ЭЖЕН ДЕЛАКРУА', 'Франция', 'Романтизм'),
    ('УИЛЬЯМ ТЁРНЕР', 'Великобритания', 'Романтизм'),
    ('ФРАНСИСКО ГОЙЯ', 'Испания', 'Романтизм и Рококо'),
    ('ЭДУАРД МАНЕ', 'Франция', 'Импрессионизм'),
    ('КЛОД МОНЕ', 'Франция', 'Импрессионизм'),
    ('ПОЛЬ СЕЗАНН', 'Франция', 'Постимпрессионизм'),
    ('ВИНСЕНТ ВАН ГОГ', 'Нидерланды', 'Постимпрессионизм'),
    ('ЖОРЖ СЁРА', 'Франция', 'Импрессионизм, неоимпрессионизм и пуантилизм'),
    ('ГУСТАВ КЛИМТ', 'Австрия', 'Модерн'),
    ('ЭДВАРД МУНК', 'Норвегия', 'Экспрессионизм'),
    ('ЭРНСТ ЛЮДВИГ КИРХНЕР', 'Германия', 'Экспрессионизм'),
    ('АНРИ МАТИСС', 'Франция', 'Фовизм'),
    ('АНДРЕ ДЕРЕН', 'Франция', 'Фовизм'),
    ('ПАБЛО ПИКАССО', 'Испания', 'Кубизм и Сюрреализм'),
    ('УМБЕРТО БОЧЧОНИ', 'Италия', 'Футуризм'),
    ('КАЗИМИР МАЛЕВИЧ', 'Россия (СССР)', 'Авангард, супрематизм и кубизм'),
    ('МАРСЕЛЬ ДЮШАН', 'Франция', 'Дадаизм и кубизм'),
    ('ПИТ МОНДРИАН', 'Нидерланды', 'Импрессионизм и абстракционизм'),
    ('ФРИДА КАЛО', 'Мексика', 'Сюрреализм'),
    ('РЕНЕ МАГРИТТ', 'Бельгия', 'Сюрреализм'),
    ('ДЖЕКСОН ПОЛЛОК', 'США', 'Абстрактный экспрессионизм'),
    ('МАРК РОТКО', 'США', 'Абстрактный экспрессионизм'),
    ('ЭНДИ УОРХОЛ', 'США', 'Поп-арт'),
    ('ЙОЗЕФ БОЙС', 'Германия', 'Постмодернизм'),
    ('ДОНАЛЬД ДЖАДД', 'США', 'Минимализм'),
    ('ЭЛЬ ГРЕКО', 'Испания', 'Возрождение'),
    ('ОГЮСТ РОДЕН', 'Франция', 'Импрессионизм'),
    ('ДЭМЬЕН ХЁРСТ', 'Великобритания', 'Современное искусство');
"""
create_themes = """
INSERT INTO
  theme (theme_name)
VALUES
    ('Животные'),
    ('Люди'),
    ('Религия'),
    ('Портрет'),
    ('Автопортрет'),
    ('Интерьеры'),
    ('Мифология'),
    ('Аллегория'),
    ('Пейзаж'),
    ('Цвет'),
    ('Жанровая живопись'),
    ('Природа'),
    ('Война'),
    ('История'),
    ('Морской пейзаж'),
    ('Натюрморт'),
    ('Одиночество'),
    ('Смерть'),
    ('Бессознательное'),
    ('Любовь'),
    ('Движение'),
    ('Городской пейзаж'),
    ('Фигуры и формы'),
    ('Массовое производство'),
    ('Абстракция'),
    ('Консюмеризм');
"""
create_techniques = """
INSERT INTO
  technique (technique_name)
VALUES
    ('Карандаш'),
    ('Керамика'),
    ('Мозаика'),
    ('Мел/пастель'),
    ('Мрамор'),
    ('Темпера'),
    ('Золочение'),
    ('Подмалевок'),
    ('Сфумато'),
    ('Масло на доске'),
    ('Линейная перспектива'),
    ('Воздушная перспектива'),
    ('Ракурс'),
    ('Ксилография'),
    ('Глина'),
    ('Холст, масло'),
    ('Фреска'),
    ('Кьяроскуро'),
    ('Гравюра резцовая'),
    ('Офорт'),
    ('Тушь, перо'),
    ('Камера-обскура'),
    ('Акварель'),
    ('Бронза'),
    ('Пуантилизм'),
    ('Импасто'),
    ('Реди-мейд'),
    ('Гуашь'),
    ('Коллаж'),
    ('Шелкография');
"""
create_holding_places = """
INSERT INTO
  holding_place (place_name, city, country)
VALUES
    ('Галерея Бельведер', 'Вена', 'АВСТРИЯ'),
    ('Музей истории искусств', 'Вена', 'АВСТРИЯ'),
    ('Музей Леопольда', 'Вена', 'АВСТРИЯ'),
    ('Британская галерея Тейт', 'Лондон', 'ВЕЛИКОБРИТАНИЯ'),
    ('Институт искусства Курто', 'Лондон', 'ВЕЛИКОБРИТАНИЯ'),
    ('Лондонская национальная галерея', 'Лондон', 'ВЕЛИКОБРИТАНИЯ'),
    ('Музей Виндзора и Королевского района', 'Лондон', 'ВЕЛИКОБРИТАНИЯ'),
    ('Собрание Уоллеса', 'Лондон', 'ВЕЛИКОБРИТАНИЯ'),
    ('Современная галерея Тейт', 'Лондон', 'ВЕЛИКОБРИТАНИЯ'),
    ('Галерея старых мастеров', 'Дрезден', 'ГЕРМАНИЯ'),
    ('Городская галерея в доме Ленбаха', 'Мюнхен', 'ГЕРМАНИЯ'),
    ('Музей Людвига', 'Кельн', 'ГЕРМАНИЯ'),
    ('Израильский музей', 'Иерусалим', 'ИЗРАИЛЬ'),
    ('Музей Тиссена-Борнемисы', 'Мадрид', 'ИСПАНИЯ'),
    ('Национальный музей Прадо', 'Мадрид', 'ИСПАНИЯ'),
    ('Вилла Фарнезина', 'Рим', 'ИТАЛИЯ'),
    ('Галерея Академии', 'Венеция', 'ИТАЛИЯ'),
    ('Галерея Боргезе', 'Рим', 'ИТАЛИЯ'),
    ('Галерея Джорджио Франкетти в Золотом Доме', 'Венеция', 'ИТАЛИЯ'),
    ('Галерея Уффици', 'Флоренция', 'ИТАЛИЯ'),
    ('Городской музей', 'Сансеполькро', 'ИТАЛИЯ'),
    ('Государственный музей Сан-Марко', 'Флоренция', 'ИТАЛИЯ'),
    ('Музеи Ватикана', 'Рим', 'ИТАЛИЯ'),
    ('Музей-дель-Новеченто', 'Милан', 'ИТАЛИЯ'),
    ('Национальная галерея современного искусства', 'Рим', 'ИТАЛИЯ'),
    ('Национальная галерея старинного искусства', 'Рим', 'ИТАЛИЯ'),
    ('Национальный археологический музей', 'Флоренция', 'ИТАЛИЯ'),
    ('Национальный музей Барджелло', 'Флоренция', 'ИТАЛИЯ'),
    ('Палатинская галерея', 'Флоренция', 'ИТАЛИЯ'),
    ('Палаццо Барберини', 'Рим', 'ИТАЛИЯ'),
    ('Пинакотека Брера', 'Милан', 'ИТАЛИЯ'),
    ('Музей современного искусства', 'Мехико', 'МЕКСИКА'),
    ('Маурицхёйс', 'Гаага', 'НИДЕРЛАНДЫ'),
    ('Музей Ван Аббе', 'Эйндховен', 'НИДЕРЛАНДЫ'),
    ('Рейксмюсеум', 'Амстердам', 'НИДЕРЛАНДЫ'),
    ('Национальный музей искусства, архитектуры и дизайна', 'Осло', 'НОРВЕГИЯ'),
    ('Государственный музей изобразительных искусств имени А. С. Пушкина', 'Москва', 'РОССИЯ'),
    ('Государственный Русский музей', 'Санкт-Петербург', 'РОССИЯ'),
    ('Йельский центр британского искусства', 'Нью-Хейвене', 'США'),
    ('Метрополитен-музей', 'Нью-Йорк', 'США'),
    ('Музей американского искусства Уитни', 'Нью-Йорк', 'США'),
    ('Музей искусств округа Лос-Анджелес', 'Лос-Анджелес', 'США'),
    ('Музей Соломона Гуггенхейма', 'Нью-Йорк', 'США'),
    ('Национальная галерея искусства', 'Вашингтон', 'США'),
    ('Нью-Йоркский музей современного искусства', 'Нью-Йорк', 'США'),
    ('Художественная галерея Йельского университета', 'Нью-Хейвене', 'США'),
    ('Чикагский институт искусств', 'Чикаго', 'США'),
    ('Лувр', 'Париж', 'ФРАНЦИЯ'),
    ('Музей Мармоттан-Моне', 'Париж', 'ФРАНЦИЯ'),
    ('Музей национальной археологии', 'Сен-Жермен-ан-Ле', 'ФРАНЦИЯ'),
    ('Музей Орсе', 'Париж', 'ФРАНЦИЯ'),
    ('Музей Отель-Дьё', 'Бон', 'ФРАНЦИЯ');
"""

selected_artists = """
SELECT
  artist.artist_name,
  artist.country,
  artist.artist_style,
  painting.painting_url,
  painting.painting_name,
  painting.painting_date
FROM
  painting
  INNER JOIN artist ON artist.id = painting.painting_artist_id
"""


# Подключаемся к БД
def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Выполнить запрос на создание
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Выполнить запрос на получение списка с данными
def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# набор запросов для создания таблиц
def create_tables(connection):
    execute_query(connection, __create_style_table)
    execute_query(connection, __create_artist_table)
    execute_query(connection, __create_theme_table)
    execute_query(connection, __create_technique_table)
    execute_query(connection, __create_painting_table)
    execute_query(connection, __create_holding_place_table)
    execute_query(connection, __create_gaming_table)


# набор запросов для заполнения таблиц
def insert_into_tables(connection):
    execute_query(connection, create_styles)
    execute_query(connection, create_paintings)
    execute_query(connection, create_artists)
    execute_query(connection, create_themes)
    execute_query(connection, create_techniques)
    execute_query(connection, create_holding_places)


# Вытаскиваем 4 картины для игры
def select_paintings(connection):
    selected_paintings = "SELECT * from painting"
    paintings = execute_read_query(connection, selected_paintings)
    rand_nums = []
    rand_paintings = []
    while len(rand_nums) < 4:
        r = random.randint(1, 50)
        if r not in rand_nums:
            rand_nums.append(r)
            rand_paintings.append(paintings[r])

    correct_answer = random.randint(0, 3)
    paintings_dict = {'pict': rand_paintings[correct_answer][1],
                      'pict_date': rand_paintings[correct_answer][3],
                      'name1': rand_paintings[0][2],
                      'name2': rand_paintings[1][2],
                      'name3': rand_paintings[2][2],
                      'name4': rand_paintings[3][2],
                      'corr_answ': correct_answer+1}

    return paintings_dict


# Вытаскиваем 4 авторов для игры
def select_artists(connection):
    artists = execute_read_query(connection, selected_artists)
    rand_nums = []
    rand_artists = []
    while len(rand_nums) < 4:
        r = random.randint(1, 50)
        if r not in rand_nums:
            rand_nums.append(r)
            rand_artists.append(artists[r])

    correct_answer = random.randint(0, 3)
    artists_dict = {
                    'county': rand_artists[correct_answer][1],
                    'style': rand_artists[correct_answer][2],
                    'pict': rand_artists[correct_answer][3],
                    'painting_name': rand_artists[correct_answer][4],
                    'pict_date': rand_artists[correct_answer][5],
                    'name1': rand_artists[0][0],
                    'name2': rand_artists[1][0],
                    'name3': rand_artists[2][0],
                    'name4': rand_artists[3][0],
                    'corr_answ': correct_answer + 1
                    }

    return artists_dict
