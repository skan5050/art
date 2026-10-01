"""Обложки статей «Полезное» №4–20: привязка по теме статьи (slug) к картинкам пакета ARTICLE_COVERS.

Первые три обложки (статьи №1–3) утверждены ранее и здесь не меняются. Изображения без текста;
заголовки статей остаются HTML. Любую обложку можно заменить, удалить или скрыть в админке.
Формат: slug статьи → (файл, ALT RU, ALT EN, ALT 中文).
"""

COVERS = {
    "a": {
        "на-какой-высоте-вешать-картину": ("mirame_cover_14_care.jpg", "Светлая комната с картиной на стене и корзинами", "A bright room with a painting on the wall and baskets", "墙上挂着画作、摆着篮子的明亮房间"),
        "размер-картины-над-диваном": ("mirame_cover_06_sofa.jpg", "Светлая стена с картиной с морским видом и диван", "A bright wall with a seascape painting and a sofa", "明亮的墙面，海景画和沙发"),
        "картина-в-подарок": ("mirame_cover_11_gift.jpg", "Подарочная коробка с розовой лентой и открытка с сердечком", "A gift box with a pink ribbon and a card with a heart", "系着粉色丝带的礼盒和带爱心的卡片"),
        "уход-за-картиной": ("mirame_cover_20_small_room.jpg", "Букет розовых и белых пионов", "A bouquet of pink and white peonies", "粉色和白色牡丹花束"),
        "картина-по-фотографии": ("mirame_cover_19_portrait.jpg", "Женщина в светлом платье на фоне моря", "A woman in a light dress by the sea", "海边身穿浅色连衣裙的女子"),
        "масло-акрил-акварель": ("mirame_cover_04_size.jpg", "Кисти в керамической банке и картина с пионами", "Brushes in a ceramic jar and a painting of peonies", "陶罐里的画笔和牡丹画"),
        "жидкий-акрил": ("mirame_cover_12_gallery_wall.jpg", "Абстрактная фактура в голубых и бежевых тонах", "Abstract texture in blue and beige", "蓝色和米色的抽象肌理"),
        "картина-в-спальню": ("mirame_cover_09_hall.jpg", "Уютная комната с цветами, подушками и картиной у окна", "A cosy room with flowers, cushions and a painting by the window", "窗边摆着花、靠垫和画作的舒适房间"),
        "картина-на-кухню": ("mirame_cover_08_dining.jpg", "Чаша с лимонами и веткой оливы", "A bowl of lemons with an olive branch", "盛着柠檬和橄榄枝的碗"),
        "картина-в-детскую": ("mirame_cover_13_frame.jpg", "Золотистый ретривер, лежащий у окна", "A golden retriever resting by a window", "窗边趴着的金毛犬"),
        "композиция-из-картин": ("mirame_cover_07_bedroom.jpg", "Две картины в рамах и ромашки у окна", "Two framed paintings and daisies by a window", "窗边的两幅装框画和雏菊"),
        "нужна-ли-картине-рама": ("mirame_cover_05_palette.jpg", "Стол с книгами, чашкой и картиной с морским видом", "A table with books, a cup and a painting of a sea view", "摆着书、杯子和海景画的桌子"),
        "как-повесить-картину": ("mirame_cover_10_office.jpg", "Мастерская: мольберт, кисти и рабочий стол", "A studio: an easel, brushes and a work table", "工作室：画架、画笔和工作台"),
        "получение-картины": ("mirame_cover_15_measure_wall.jpg", "Упакованная картина, крафтовая бумага и комнатные растения", "A wrapped painting, kraft paper and houseplants", "包装好的画作、牛皮纸和室内植物"),
        "свет-и-картина": ("mirame_cover_18_landscape.jpg", "Тосканский пейзаж с оливковыми деревьями и холмами", "A Tuscan landscape with olive trees and hills", "有橄榄树和山丘的托斯卡纳风景"),
        "формат-картины": ("mirame_cover_16_subject.jpg", "Абстракция в бежевых, синих и коралловых оттенках", "Abstraction in beige, blue and coral shades", "米色、蓝色和珊瑚色的抽象画"),
        "как-выбрать-абстракцию": ("mirame_cover_17_abstract.jpg", "Абстракция в голубых и золотистых тонах", "Abstraction in blue and golden tones", "蓝色与金色调的抽象画"),
    },
    "d": {
        "расчет-размера-картины": ("holstori_cover_09_hall.jpg", "Большое абстрактное полотно на стене рядом с чёрным креслом", "A large abstract canvas on the wall beside a black armchair", "墙上的大幅抽象画，旁边是黑色扶手椅"),
        "картины-для-офиса": ("holstori_cover_05_palette.jpg", "Рабочий стол с книгами и картиной на стене", "A desk with books and a painting on the wall", "摆着书、墙上挂着画作的书桌"),
        "техники-живописи": ("holstori_cover_04_size.jpg", "Кисти, палитра и картина в раме на столе мастерской", "Brushes, a palette and a framed painting on a studio table", "工作室桌上的画笔、调色板和装框画作"),
        "основа-картины": ("holstori_cover_14_care.jpg", "Рука художника с кистью у холста", "An artist’s hand with a brush at a canvas", "画家手持画笔，靠近画布"),
        "оформление-картины": ("holstori_cover_07_bedroom.jpg", "Деревянный стол и стул, картины в рамах на стене", "A wooden table and chair with framed pictures on the wall", "木桌木椅和墙上的装框画"),
        "картина-корпоративный-подарок": ("holstori_cover_11_gift.jpg", "Абстрактное полотно в чёрных, золотых и белых тонах на стене", "An abstract canvas in black, gold and white on the wall", "墙上黑、金、白三色的抽象画"),
        "хранение-картин": ("holstori_cover_06_sofa.jpg", "Мастерская: мольберт, бюст и рабочий стол у окна", "A studio: an easel, a bust and a work table by the window", "工作室：窗边的画架、半身像和工作台"),
        "перевозка-картины-при-переезде": ("holstori_cover_10_office.jpg", "Кисти в банке, палитра и бюст в мастерской", "Brushes in a jar, a palette and a bust in the studio", "工作室里罐中的画笔、调色板和半身像"),
        "приемка-отправления": ("holstori_cover_16_subject.jpg", "Абстракция в серых, синих и золотых тонах", "Abstraction in grey, blue and gold tones", "灰、蓝、金色调的抽象画"),
        "портрет-по-фотографии": ("holstori_cover_19_portrait.jpg", "Портрет женщины на нейтральном фоне", "A portrait of a woman on a neutral background", "中性背景下的女子肖像"),
        "развеска-картин": ("holstori_cover_12_gallery_wall.jpg", "Городская набережная с классическим зданием и фонарями", "A city embankment with a classical building and street lamps", "有古典建筑和路灯的城市河岸"),
        "диптих-и-триптих": ("holstori_cover_15_measure_wall.jpg", "Абстракция в чёрных и золотых плоскостях", "Abstraction in black and gold planes", "黑色与金色块面的抽象画"),
        "как-оформить-сертификат": ("holstori_cover_20_small_room.jpg", "Белые пионы в тёмной вазе", "White peonies in a dark vase", "深色花瓶中的白牡丹"),
        "как-читать-карточку-картины": ("holstori_cover_08_dining.jpg", "Груши и тёмная чаша на фактурном фоне", "Pears and a dark bowl on a textured background", "肌理背景上的梨和深色碗"),
        "освещение-картин": ("holstori_cover_18_landscape.jpg", "Дерево на берегу озера и горы вдали", "A tree on a lake shore with mountains beyond", "湖岸边的一棵树和远山"),
        "абстрактная-живопись-выбор": ("holstori_cover_17_abstract.jpg", "Абстракция с чёрными и золотыми мазками", "Abstraction with black and gold strokes", "黑色与金色笔触的抽象画"),
        "картины-для-коммерческих-интерьеров": ("holstori_cover_13_frame.jpg", "Стая рыб в тёмно-синей воде", "A school of fish in dark blue water", "深蓝水中的鱼群"),
    },
}
