"""Стартовое наполнение сайта A «МираМе».

Русские тексты — из приложения Б ТЗ, SEO — из приложения Д.
Английские тексты — черновики для проверки владельцем (заполняются вручную,
автоматический перевод не используется). Тон: теплый, доброжелательный,
с легким юмором; без выдуманных фактов, цен, сроков и продаж.
"""

SETTINGS = {
    "brand_name_ru": "МираМе",
    "brand_name_en": "MiraMe",
    "slogan_ru": "Картины, в которых есть вы.",
    "slogan_en": "Paintings with a bit of you in them.",
    "logo": "logo.png",
    "certificate_image": "mirame_gift_certificate.jpg",
    "logo_alt_ru": "МираМе — картины, в которых есть вы",
    "logo_alt_en": "MiraMe — paintings with a bit of you in them",
    "logo_contains_slogan": True,
    "geography_ru": "",
    "geography_en": "",
    "hours_ru": "",
    "hours_en": "",
    "copyright_ru": "© {year} {brand}",
    "copyright_en": "© {year} {brand}",
    "painting_prefix_ru": "картина",
    "painting_prefix_en": "painting",
    "header_note_ru": "Картины в наличии и на заказ",
    "header_note_en": "Paintings ready to hang and made to order",
    "map_tiles_url": "",
}

# Надписи, которые на этом сайте звучат иначе, чем по умолчанию: ключ → (RU, EN).
LABELS = {
    "form.sample_note": ("Картину из каталога можно взять за образец: напишем похожую — индивидуально для вас.", "Any painting in the catalogue can be a sample: we will paint a similar one individually for you."),
    "catalog.list_hint": ("Каждая работа может стать образцом — напишем похожую для вас", "Any work can be a sample — we will paint a similar one for you"),
    "catalog.sample_badge": ("Образец · напишем похожую", "Sample · we paint a similar one"),
    "painting.status_page_sold": ("SOLD / Продано", "SOLD / Sold"),
    "catalog.order_cta": ("Любой сюжет можно обсудить", "Any subject is up for discussion"),
    "painting.sold_note": (
        "Эта картина уже дома у своего владельца. Можно заказать новую — по ее мотивам и с вашими деталями.",
        "This painting has already found its home. You can order a new one inspired by it, with your own details.",
    ),
    "painting.custom_note": (
        "Эта работа — пример. Новую картину обсудим под ваш размер, оттенки и настроение.",
        "This work is an example. We will talk through a new painting for your size, colours and mood.",
    ),
    "form.consent": (
        "Отправляя форму, вы соглашаетесь на обработку указанных данных, чтобы мы могли ответить на обращение.",
        "By sending the form you agree to the processing of the data provided so that we can reply.",
    ),
    "error404.text": (
        "Похоже, эта страница переехала или ее никогда не было. Загляните в каталог — там точно есть что посмотреть.",
        "Looks like this page has moved or never existed. Have a look at the catalogue — there is plenty to see there.",
    ),
}

BLOCKS = [
    {
        "key": "painting-sample-available", "name": "Картина в наличии — пояснение об образце",
        "usage": "Страница картины: блок под названием (по статусу работы)",
        "title_ru": "Понравилась, но хочется немного иначе?", "title_en": "Liked it, but want it a little different?",
        "text_ru": "Эта картина — оригинал в наличии, и её можно забрать домой. А ещё она может стать образцом: напишем похожую работу под ваш размер и оттенки. Новая картина будет индивидуальной — не копией, а вашей версией сюжета.",
        "text_en": "This painting is an original in stock, ready to go home with you. It can also become a sample: we will paint a similar work in your size and shades. The new painting will be individual — not a copy, but your own version of the subject.",
    },
    {
        "key": "painting-sample-custom", "name": "Картина под заказ — пояснение об образце",
        "usage": "Страница картины: блок под названием (по статусу работы)",
        "title_ru": "Это образец — картину напишем для вас", "title_en": "This is a sample — we will paint one for you",
        "text_ru": "Работа показывает сюжет, настроение и манеру. Мы напишем похожую картину специально для вас, и она будет индивидуальной: размер, оттенки и детали обсудим вместе. Точной копии не будет — и в этом её ценность.",
        "text_en": "The work shows the subject, mood and style. We will paint a similar picture especially for you, and it will be individual: we will agree the size, shades and details together. It won’t be an exact copy — and that is what makes it valuable.",
    },
    {
        "key": "painting-sample-sold", "name": "Проданная картина — пояснение об образце",
        "usage": "Страница картины: блок под названием (по статусу работы)",
        "title_ru": "Оригинал уже дома у владельца", "title_en": "The original is already in its new home",
        "text_ru": "Но эту картину можно взять за образец: напишем новую работу по её мотивам. Она будет индивидуальной — со своими отличиями, вашим размером и вашей историей.",
        "text_en": "But this painting can be used as a sample: we will paint a new work inspired by it. It will be individual — with its own differences, your size and your story.",
    },
    {
        "key": "painting-description", "name": "Общий текст описания картины",
        "usage": "Страница картины, если выбран «Общий текст описания»",
        "text_ru": "Нравится эта работа? Оставьте заявку — обсудим детали, оформление и доставку. Статус и известные характеристики указаны в карточке.",
        "text_en": "Like this work? Send a request and we will talk through the details, framing and delivery. The status and known details are listed on this page.",
    },
    {
        "key": "delivery-short", "name": "Краткие условия доставки",
        "usage": "Страница «Доставка» (выделенный блок), страница картины, главная",
        "title_ru": "Коротко о доставке", "title_en": "Delivery in short",
        "text_ru": "Отправляем в любой город через СДЭК или другую ТК по согласованию с Заказчиком. Доставка оплачивается отдельно. Стоимость и сроки согласуются индивидуально.",
        "text_en": "We ship to any city via CDEK or another carrier agreed with the customer. Delivery is paid separately. Cost and timing are agreed individually.",
    },
    {
        "key": "sales-map", "name": "География наших продаж — заголовок и текст",
        "usage": "Блок карты на странице «Доставка» (#geography-sales)",
        "title_ru": "География наших продаж", "title_en": "Where our paintings have gone",
        "text_ru": "У этих городов уже есть небольшая общая история: туда отправились наши картины. Каждая отметка — место, где работа нашла своего владельца. Приятно знать, что у искусства столько разных адресов.",
        "text_en": "These cities already share a small story: our paintings have travelled there. Every marker is a place where a work found its owner. It is nice to know that art has so many different addresses.",
    },
    {
        "key": "form-intro", "name": "Вступление в форме заказа",
        "usage": "Модальное окно заказа",
        "text_ru": "Расскажите немного о своей картине. Имени и одного удобного контакта достаточно, чтобы начать.",
        "text_en": "Tell us a little about your painting. A name and one convenient contact are enough to get started.",
    },
    {
        "key": "form-success", "name": "Сообщение после сохранения заявки",
        "usage": "Форма заказа — после успешной отправки",
        "text_ru": "Спасибо, заявка у нас. Свяжемся с вами выбранным способом и обсудим детали.",
        "text_en": "Thank you, we have your request. We will get in touch the way you chose and talk through the details.",
    },
    {
        "key": "form-error", "name": "Ошибка отправки заявки",
        "usage": "Форма заказа — если заявку не удалось сохранить",
        "text_ru": "Заявку пока не удалось отправить. Ваш текст остался в форме — попробуйте еще раз или напишите нам другим способом.",
        "text_en": "We could not send your request just now. Your text is still in the form — please try again or contact us another way.",
    },
    {
        "key": "empty-category", "name": "Пустая рубрика",
        "usage": "Рубрика без опубликованных картин",
        "text_ru": "Здесь пока свободная стена. Можно посмотреть другие сюжеты или рассказать, что хотелось бы увидеть именно вам.",
        "text_en": "This wall is still empty. Have a look at other subjects or tell us what you would like to see here.",
    },
    {
        "key": "size-hint", "name": "Подсказка к полю размера",
        "usage": "Поле «Желаемый размер новой картины»",
        "text_ru": "Выберите формат, которому найдется место дома. Нужен другой размер? Укажите ширину и высоту — обсудим. Пока не определились? Тоже хороший повод начать разговор.",
        "text_en": "Pick a format that has a place at home. Need a different size? Enter the width and height and we will discuss it. Not sure yet? That is a fine way to start the conversation too.",
    },
    {
        "key": "size-caption", "name": "Подпись к полям размера",
        "usage": "Под полем размера",
        "text_ru": "Ширина × высота, см. Размер самой картины, без рамы.",
        "text_en": "Width × height, cm. The size of the painting itself, without a frame.",
    },
    {
        "key": "delivery-steps", "name": "Доставка — три коротких пункта",
        "usage": "Страница «Доставка», над картой. Строки «Заголовок | текст»",
        "text_ru": "Упаковка | Защищаем работу при перевозке\nОтправка | Способ согласовываем с вами\nСтоимость | Считаем для вашего маршрута до отправки",
        "text_en": "Packaging | We protect the work in transit\nShipping | We agree the method with you\nCost | We work it out for your route before shipping",
    },
    {
        "key": "about-steps", "name": "Как мы работаем — шаги",
        "usage": "Страница «О нас» под текстом. Строки «Заголовок | текст». Пусто — блок не показывается",
        "text_ru": "", "text_en": "",
    },
    {
        "key": "footer-order", "name": "Подпись в футере",
        "usage": "Футер, над кнопками",
        "text_ru": "Картина — отдельно, дорога — отдельно. Отправляем через СДЭК или согласованную с вами ТК; стоимость доставки оплачивается дополнительно.",
        "text_en": "The painting is one thing, the journey is another. We ship via CDEK or a carrier agreed with you; delivery is paid separately.",
    },
    {
        "key": "painting-under-button", "name": "Подпись под кнопкой заказа",
        "usage": "Страница картины",
        "text_ru": "Название картины уже будет в заявке — искать и копировать ссылку не придется.",
        "text_en": "The painting will already be named in your request — no need to copy any links.",
    },
]

SEO_TEMPLATES = {
    "painting_available": {
        "title_ru": "{painting_name} — в наличии", "title_en": "{painting_name} — available",
        "description_ru": "«{painting_name}» ждет своего дома. Посмотрите изображение и характеристики; обсудим оформление и доставку. Доставка оплачивается отдельно.",
        "description_en": "“{painting_name}” is waiting for its home. See the image and details; we will talk through framing and delivery. Delivery is paid separately.",
    },
    "painting_custom": {
        "title_ru": "{painting_name} — под заказ", "title_en": "{painting_name} — made to order",
        "description_ru": "«{painting_name}» — отправная точка вашей идеи. Обсудим размер, оттенки и новую картину; стоимость и сроки согласуем отдельно.",
        "description_en": "“{painting_name}” is a starting point for your idea. We will discuss the size, colours and a new painting; price and timing are agreed separately.",
    },
    "painting_sold": {
        "title_ru": "{painting_name} — продана", "title_en": "{painting_name} — sold",
        "description_ru": "«{painting_name}» уже нашла владельца. Понравился сюжет? Обсудим похожую новую картину со своими деталями.",
        "description_en": "“{painting_name}” has already found its owner. Like the subject? Let’s talk about a similar new painting with your own details.",
    },
    "category": {
        "title_ru": "Картины: {category_name}", "title_en": "Paintings: {category_name}",
        "description_ru": "Посмотрите картины в рубрике «{category_name}» и найдите близкий сюжет. Подробности работы или свою идею можно обсудить в заявке.",
        "description_en": "Browse paintings in “{category_name}” and find a subject close to you. Details of a work or your own idea can be discussed in a request.",
    },
    "article": {"title_ru": "", "title_en": "", "description_ru": "", "description_en": ""},
    "page": {"title_ru": "", "title_en": "", "description_ru": "", "description_en": ""},
    "list_page": {"title_ru": "{seo_title} — страница {N}", "title_en": "{seo_title} — page {N}", "description_ru": "", "description_en": ""},
}

TECHNIQUES = [
    ("Масло", "Oil"), ("Акрил", "Acrylic"), ("Акварель", "Watercolour"), ("Жидкий акрил", "Fluid acrylic"),
    ("Фактурная живопись", "Textured painting"), ("Кофе", "Coffee"), ("Вино", "Wine"),
    ("Смешанная техника", "Mixed media"), ("Графика", "Drawing"),
]

PAGES = [
    {
        "kind": "home",
        "title_ru": "Картины, с которыми дома еще уютнее",
        "title_en": "Paintings that make home even cosier",
        "nav_title_ru": "Главная", "nav_title_en": "Home",
        "banner_image": "mirame_home_hero_desktop.jpg", "banner_image_mobile": "mirame_home_hero_mobile.jpg",
        "banner_title_ru": "", "banner_title_en": "",
        "banner_text_ru": "У стены уже есть цвет. Осталось добавить настроение. Выберите картину из наличия или расскажите, о какой мечтаете, — начнем с вашей идеи.",
        "banner_text_en": "The wall already has a colour. All it needs now is a mood. Choose a painting that is ready or tell us about the one you dream of — we will start with your idea.",
        "banner_button1_ru": "Найти свою картину", "banner_button1_en": "Find your painting", "banner_button1_link": "catalog",
        "banner_button2_ru": "Рассказать об идее", "banner_button2_en": "Tell us your idea",
        "seo_title_ru": "Картины в наличии и на заказ", "seo_title_en": "Paintings ready to hang and made to order",
        "seo_description_ru": "Выберите картину для своего дома или расскажите о задумке. Готовые работы и картины на заказ: любимые сюжеты, понятные детали и немного уюта.",
        "seo_description_en": "Choose a painting for your home or tell us about your idea. Ready works and paintings made to order: favourite subjects, clear details and a little cosiness.",
    },
    {
        "kind": "about", "image": "mirame_about_studio.jpg", "image_alt_ru": "Светлая комната: морской пейзаж на стене, оливковое деревце и рабочий стол", "image_alt_en": "A bright room: a seascape on the wall, an olive plant and a work table", "cta_text_ru": "Расскажите, какую картину вы ищете", "cta_text_en": "Tell us what painting you are looking for", "cta_button_ru": "Обсудить заказ", "cta_button_en": "Discuss an order", "slug_ru": "о-нас", "slug_en": "about",
        "title_ru": "Чтобы дома было чуть больше вас", "title_en": "A little more of you at home",
        "nav_title_ru": "О нас", "nav_title_en": "About",
        "body_ru": (
            "Иногда комнате не хватает совсем немного: теплого оттенка, морского горизонта или картины, на которую приятно посмотреть между делами. Не обязательно знать имя каждого художника и отличать все направления живописи. «Мне нравится» — уже хороший повод присмотреться.\n\n"
            "Здесь можно выбрать готовую работу или обсудить картину под заказ. Мы начинаем с простых вещей: что вам нравится, где будет жить картина и какое настроение хочется видеть рядом. Фотография комнаты и несколько слов подойдут не хуже длинного списка художественных терминов.\n\n"
            "В карточках указаны статус работы и известные характеристики. Размер, оформление, стоимость и детали заказа уточним до окончательного решения. Если понравилась уже проданная картина, она может стать отправной точкой для новой — со своими отличиями и вашей историей."
        ),
        "body_en": (
            "Sometimes a room is missing just a little something: a warm shade, a sea horizon or a painting that is nice to glance at between chores. You don’t need to know every artist’s name or tell all the art movements apart. “I like it” is already a good reason to take a closer look.\n\n"
            "Here you can choose a ready work or talk about a painting made to order. We start with simple things: what you like, where the painting will live and what mood you would like to have around. A photo of the room and a few words work just as well as a long list of art terms.\n\n"
            "Each work’s page shows its status and the details we know. Size, framing, price and order details are agreed before any final decision. If you fell for a painting that has already been sold, it can become the starting point for a new one — with its own differences and your story."
        ),
        "button_ru": "Давайте знакомиться", "button_en": "Let’s get acquainted",
        "seo_title_ru": "О нас", "seo_title_en": "About us",
        "seo_description_ru": "Помогаем начать с простого «мне нравится». Познакомьтесь с нашим подходом к выбору готовой картины и обсуждению работы по вашей идее.",
        "seo_description_en": "We help you start with a simple “I like it”. Get to know how we help choose a ready painting and discuss a work based on your idea.",
    },
    {
        "kind": "catalog", "cta_text_ru": "Любой сюжет можно обсудить", "cta_text_en": "Any subject is up for discussion", "cta_button_ru": "Заказать картину", "cta_button_en": "Order a painting", "slug_ru": "каталог", "slug_en": "catalog",
        "title_ru": "Каталог картин", "title_en": "Painting catalogue",
        "nav_title_ru": "Каталог", "nav_title_en": "Catalogue",
        "intro_ru": "Какой сюжет хочется забрать домой? Выберите рубрику, посмотрите работы и откройте ту, к которой хочется вернуться взглядом.",
        "intro_en": "Which subject would you like to take home? Choose a category, browse the works and open the one your eyes keep coming back to.",
        "seo_title_ru": "Каталог картин", "seo_title_en": "Painting catalogue",
        "seo_description_ru": "Море без чемодана, цветы без вазы и другие сюжеты для дома. Посмотрите картины по рубрикам и найдите работу, к которой хочется возвращаться.",
        "seo_description_en": "The sea without a suitcase, flowers without a vase and other subjects for your home. Browse paintings by category and find one you will want to come back to.",
    },
    {
        "kind": "sold", "kicker_ru": "Проданные картины / SOLD", "kicker_en": "Sold paintings / SOLD", "cta_text_ru": "Понравилась проданная работа?", "cta_text_en": "Liked a sold work?", "cta_button_ru": "Заказать похожую", "cta_button_en": "Order a similar one", "slug_ru": "проданные-картины", "slug_en": "sold",
        "title_ru": "Уже дома. Но могут вдохновить вашу историю", "title_en": "Already home. But they can inspire your story",
        "nav_title_ru": "SOLD", "nav_title_en": "SOLD",
        "intro_ru": "Эти работы нашли своих владельцев. Если одна из них вам особенно понравилась, нажмите «Заказать похожую». Возьмем ее за ориентир и обсудим новую картину: размер, оттенки, сюжет и детали. Та же любовь к живописи — но уже ваша история.",
        "intro_en": "These works have found their owners. If one of them caught your eye, press “Order a similar one”. We will take it as a reference and discuss a new painting: size, colours, subject and details. The same love of painting — but your own story.",
        "empty_ru": "Проданные работы появятся здесь после добавления. А пока можно заглянуть в каталог — вдруг ваша картина еще ждет знакомства.",
        "empty_en": "Sold works will appear here once they are added. Meanwhile, have a look at the catalogue — your painting may still be waiting to meet you.",
        "button_ru": "Заказать похожую", "button_en": "Order a similar one",
        "seo_title_ru": "Проданные картины — SOLD", "seo_title_en": "Sold paintings — SOLD",
        "seo_description_ru": "Эти картины уже нашли свой дом. Посмотрите проданные работы и выберите пример, с которого может начаться ваша новая история.",
        "seo_description_en": "These paintings have already found their home. Browse the sold works and pick an example your new story can start from.",
    },
    {
        "kind": "reviews", "cta_text_ru": "Поможем выбрать вашу картину", "cta_text_en": "We will help you choose your painting", "cta_button_ru": "Связаться с нами", "cta_button_en": "Contact us", "slug_ru": "отзывы", "slug_en": "reviews",
        "title_ru": "Отзывы", "title_en": "Reviews",
        "intro_ru": "Здесь говорят те, у кого картины уже дома. Спасибо за впечатления — приятно узнавать, как работа стала частью чьего-то пространства.",
        "intro_en": "Here you hear from people whose paintings are already at home. Thank you for sharing — it is lovely to learn how a work became part of someone’s space.",
        "empty_ru": "Пока здесь тихо: отзывы появятся после публикации. А задать вопрос о картине можно уже сейчас.",
        "empty_en": "It is quiet here for now: reviews will appear once published. You can ask about a painting right away, though.",
        "seo_title_ru": "Отзывы", "seo_title_en": "Reviews",
        "seo_description_ru": "Впечатления покупателей о картинах и заказах. Когда отзывы опубликованы, здесь можно узнать, как работа стала частью чьего-то дома.",
        "seo_description_en": "Customers’ impressions of paintings and orders. Once reviews are published, you can read here how a work became part of someone’s home.",
    },
    {
        "kind": "delivery", "image": "mirame_delivery.jpg", "image_alt_ru": "Картина, упакованная для отправки: защитная плёнка, уголки и крафт-бумага", "image_alt_en": "A painting packed for shipping: protective wrap, corner guards and kraft paper", "cta_text_ru": "Уточнить доставку в ваш город", "cta_text_en": "Check delivery to your city", "cta_button_ru": "Обсудить доставку", "cta_button_en": "Discuss delivery", "slug_ru": "доставка", "slug_en": "delivery",
        "title_ru": "Картина собирается к вам в гости", "title_en": "A painting is coming to visit",
        "nav_title_ru": "Доставка", "nav_title_en": "Delivery",
        "intro_ru": "Чемодан ей не нужен. А подходящая упаковка и согласованный маршрут — очень даже.",
        "intro_en": "It doesn’t need a suitcase. The right packaging and an agreed route, on the other hand, are very welcome.",
        "body_ru": (
            "Хорошей картине не обязательно жить в том же городе, где ее выбрали. Отправляем работы в любой город через СДЭК или любую другую транспортную компанию по согласованию с Заказчиком. Если у вас уже есть удобная ТК, напишите ее название — обсудим отправку с ней.\n\n"
            "## Сначала знакомимся с маршрутом\n"
            "Сообщите город и выбранную картину. Для работы на заказ пригодится предполагаемый размер. Вместе уточним способ получения, условия перевозки и ориентировочный срок. Карта наших продаж при этом не работает шлагбаумом: если вашего города на ней еще нет, это не мешает обсудить доставку.\n\n"
            "## У картины свой багаж\n"
            "Подготовку к отправке и упаковку подбираем с учетом размера, основы, оформления и условий перевозки. Это не тот случай, когда хочется отправиться налегке. Детали согласуем до передачи работы транспортной компании.\n\n"
            "## Без сюрпризов в стоимости\n"
            "Доставка оплачивается Заказчиком отдельно и не входит в стоимость картины. Сумма зависит от маршрута, параметров упакованной работы и условий выбранного перевозчика. Стоимость и порядок оплаты согласуем до отправки. Картина может удивлять цветом и настроением — счет за дорогу неожиданным быть не должен.\n\n"
            "## Если картина едет к празднику\n"
            "Напишите нужную дату получения заранее. Время изготовления и время перевозки — разные части пути. Обсудим их отдельно, без обещаний, что большая картина умеет телепортироваться.\n\n"
            "Не уверены, какую компанию выбрать или что написать в заявке? Начните с города и ссылки на работу. Остальное спокойно обсудим."
        ),
        "body_en": (
            "A good painting doesn’t have to live in the city where it was chosen. We ship works to any city via CDEK or any other carrier agreed with the customer. If you already have a carrier you like, tell us its name and we will discuss shipping with them.\n\n"
            "## First, we get to know the route\n"
            "Tell us your city and the painting you have chosen. For a work made to order, the planned size helps. Together we will agree how you receive it, the shipping conditions and a rough timeframe. Our sales map is not a barrier: if your city is not on it yet, we can still discuss delivery.\n\n"
            "## A painting has its own luggage\n"
            "We choose the preparation and packaging based on the size, support, framing and shipping conditions. This is not a case for travelling light. We agree the details before handing the work to the carrier.\n\n"
            "## No surprises in the cost\n"
            "Delivery is paid by the customer separately and is not included in the price of the painting. The amount depends on the route, the packed dimensions and the chosen carrier’s terms. We agree the cost and how to pay before shipping. A painting may surprise you with its colours and mood — the bill for the journey shouldn’t.\n\n"
            "## If the painting is travelling for a special day\n"
            "Tell us the date you need it by well in advance. Making a painting and shipping it are different parts of the journey. We will discuss them separately, without promising that a large painting can teleport.\n\n"
            "Not sure which carrier to choose or what to write in your request? Start with your city and a link to the work. We will calmly sort out the rest."
        ),
        "note_ru": "Здесь показаны состоявшиеся продажи, а не границы доставки. Вашего города пока нет? Это не мешает ему стать следующим.",
        "note_en": "The map shows completed sales, not delivery limits. Your city is not there yet? That doesn’t stop it from being next.",
        "empty_ru": "Собираем на карте истории наших картин. Отметки появятся после добавления подтвержденных продаж.",
        "empty_en": "We are gathering the stories of our paintings on the map. Markers will appear once confirmed sales are added.",
        "button_ru": "Обсудить дорогу картины", "button_en": "Discuss the painting’s journey",
        "seo_title_ru": "Доставка картин", "seo_title_en": "Painting delivery",
        "seo_description_ru": "Картина собирается к вам: отправляем в любой город через СДЭК или согласованную ТК. Доставка оплачивается отдельно; детали обсудим заранее.",
        "seo_description_en": "A painting is on its way to you: we ship to any city via CDEK or an agreed carrier. Delivery is paid separately; we discuss the details in advance.",
    },
    {
        "kind": "contacts", "slug_ru": "контакты", "slug_en": "contacts",
        "title_ru": "Давайте начнем с «Здравствуйте»", "title_en": "Let’s start with “Hello”",
        "nav_title_ru": "Контакты", "nav_title_en": "Contacts",
        "intro_ru": "Можно спросить о готовой картине, прислать свою идею или просто уточнить размер. Выберите удобный способ связи. Если пишете со страницы работы, она уже будет указана в заявке — искать и копировать ссылку не придется.",
        "intro_en": "You can ask about a ready painting, send us your idea or simply check a size. Choose the way to contact us that suits you. If you write from a work’s page, it will already be named in your request — no need to hunt for links.",
        "seo_title_ru": "Контакты", "seo_title_en": "Contacts",
        "seo_description_ru": "Начнем со «Здравствуйте». Напишите о понравившейся картине, своей идее или доставке — одного удобного способа связи достаточно.",
        "seo_description_en": "Let’s start with “Hello”. Write to us about a painting you like, your idea or delivery — one convenient way to reach you is enough.",
    },
    {
        "kind": "certificate", "image_alt_ru": "Подарочная коробка с розовой лентой и открытка с сердечком", "image_alt_en": "A gift box with a pink ribbon and a card with a heart", "slug_ru": "подарочный-сертификат", "slug_en": "gift-certificate",
        "title_ru": "Подарите выбор. Он тоже бывает красивым", "title_en": "Give the gift of choice. It can be beautiful too",
        "nav_title_ru": "Подарочный сертификат", "nav_title_en": "Gift certificate",
        "body_ru": (
            "Угадать любимый сюжет иногда сложнее, чем выбрать подарок человеку, у которого «все есть». Сертификат оставляет самое приятное решение получателю: какая картина будет радовать именно его.\n\n"
            "Выберите доступный номинал и оставьте удобный контакт. До оформления согласуем формат, срок действия и условия использования сертификата. Вы дарите возможность выбрать — а все практические вопросы обсудим заранее."
        ),
        "body_en": (
            "Guessing someone’s favourite subject can be harder than choosing a present for a person who “has everything”. A certificate leaves the most enjoyable decision to the recipient: which painting will make them happy.\n\n"
            "Choose an available amount and leave a convenient contact. Before issuing it we will agree the format, validity period and terms of use. You give the chance to choose — and we sort out all the practical questions in advance."
        ),
        "button_ru": "Обсудить сертификат", "button_en": "Discuss a certificate",
        "seo_title_ru": "Подарочный сертификат", "seo_title_en": "Gift certificate",
        "seo_description_ru": "Подарите человеку приятное решение: выбрать свою картину. Обсудим номинал, формат и условия сертификата до оформления.",
        "seo_description_en": "Give someone a pleasant decision to make: choosing their own painting. We will discuss the amount, format and terms before issuing the certificate.",
    },
    {
        "kind": "custom", "image": "mirame_custom_order.jpg", "image_alt_ru": "Кисти в керамической банке и картина с пионами на рабочем столе", "image_alt_en": "Brushes in a ceramic jar and a painting of peonies on a work table", "cta_text_ru": "А можно такую, но немного другую?", "cta_text_en": "Could I have one like this, but a little different?", "cta_button_ru": "Рассказать об идее", "cta_button_en": "Tell us your idea", "slug_ru": "картины-на-заказ", "slug_en": "custom-paintings",
        "title_ru": "Сначала ваша идея. Потом — картина", "title_en": "Your idea first. Then the painting",
        "nav_title_ru": "Картины на заказ", "nav_title_en": "Paintings to order",
        "body_ru": (
            "Любимый вид из окна, спокойные оттенки для спальни или портрет того, кто обычно не хочет фотографироваться. Расскажите, какую работу представляете. Идея не обязана приходить в идеальной формулировке — ей достаточно прийти.\n\n"
            "Пришлите пример, назовите приблизительный размер и добавьте пару слов о цвете и настроении. Если картина нужна к событию, сразу укажите желаемую дату получения: ей понадобится время не только на создание, но и на дорогу.\n\n"
            "Обсудим возможность исполнения, сюжет, технику, оформление, стоимость и сроки. Если точного решения пока нет, начнем с ваших предпочтений. Заявка — это начало разговора, а не автоматическая оплата или резерв."
        ),
        "body_en": (
            "A favourite view from the window, calm shades for the bedroom or a portrait of someone who usually hides from cameras. Tell us what kind of work you imagine. An idea doesn’t have to arrive perfectly worded — it just has to arrive.\n\n"
            "Send an example, give an approximate size and add a couple of words about colour and mood. If the painting is for a special occasion, mention the date you need it by: it will need time not only to be created but also to travel.\n\n"
            "We will discuss whether it can be done, the subject, technique, framing, price and timing. If there is no exact plan yet, we will start from your preferences. A request is the start of a conversation, not an automatic payment or reservation."
        ),
        "button_ru": "Рассказать об идее", "button_en": "Tell us your idea",
        "seo_title_ru": "Картины на заказ", "seo_title_en": "Paintings made to order",
        "seo_description_ru": "Есть идея для картины, но пока нет точного плана? Пришлите пример, размер или пару слов о настроении — начнем с этого.",
        "seo_description_en": "Have an idea for a painting but no exact plan yet? Send an example, a size or a few words about the mood — we will start from there.",
    },
    {
        "kind": "studio", "image": "mirame_studio_main.jpg", "image_alt_ru": "Мастерская: мольберт с картиной, кисти и палитра на рабочем столе", "image_alt_en": "A studio: an easel with a painting, brushes and a palette on the work table", "cta_text_ru": "Расскажите, какую картину вы ищете", "cta_text_en": "Tell us what painting you are looking for", "cta_button_ru": "Рассказать об идее", "cta_button_en": "Tell us your idea", "slug_ru": "студия", "slug_en": "studio",
        "title_ru": "Немного о нашей мастерской", "title_en": "A little about our studio",
        "nav_title_ru": "О студии", "nav_title_en": "The studio",
        "body_ru": (
            "Мастерская — место, где идеи становятся картинами: здесь пахнет краской, сохнут холсты и лежат эскизы будущих работ. Обсудить заказ удобно онлайн, а адрес и способ встречи для вашего города указаны на его странице и в контактах.\n\n"
            "Как проходит работа: вы рассказываете об идее или выбираете готовую картину, мы уточняем детали — размер, оформление, стоимость и доставку. Для работы на заказ согласуем сюжет и сроки до начала. Если нужно что-то показать — пришлите фото комнаты или пример, это лучше тысячи слов.\n\n"
            "Изображение в этом разделе — иллюстрация настроения мастерской, а не фотография конкретного помещения."
        ),
        "body_en": (
            "The studio is where ideas turn into paintings: it smells of paint, canvases are drying and sketches of future works lie on the table. An order is easy to discuss online, and the address and way to meet in your city are listed on its page and in the contacts.\n\n"
            "How it works: you tell us your idea or choose a ready painting, and we agree the details — size, framing, price and delivery. For a work made to order, we agree the subject and timing before starting. If you want to show us something, send a photo of the room or an example — it says more than a thousand words.\n\n"
            "The image in this section is an illustration of the studio’s mood, not a photograph of a specific room."
        ),
        "button_ru": "Рассказать об идее", "button_en": "Tell us your idea",
        "seo_title_ru": "О студии", "seo_title_en": "About the studio",
        "seo_description_ru": "Как устроена наша мастерская и как проходит работа над картиной: от идеи и размера до оформления и доставки.",
        "seo_description_en": "How our studio works and how a painting comes together: from the idea and size to framing and delivery.",
    },
    {
        "kind": "guides", "slug_ru": "полезное", "slug_en": "guides",
        "title_ru": "Полезное", "title_en": "Guides",
        "intro_ru": "Короткие и честные ответы на вопросы, которые возникают перед выбором картины: как подобрать размер, чем отличается заказ от готовой работы и как картина доберется до дома.",
        "intro_en": "Short, honest answers to the questions that come up before choosing a painting: how to pick a size, how an order differs from a ready work and how a painting gets home.",
        "empty_ru": "Статьи скоро появятся.", "empty_en": "Articles are coming soon.",
        "seo_title_ru": "Полезное о выборе и заказе картин", "seo_title_en": "Guides to choosing and ordering paintings",
        "seo_description_ru": "Советы без строгих правил: как выбрать картину для комнаты, подобрать размер, заказать свою идею и организовать доставку.",
        "seo_description_en": "Advice without strict rules: how to choose a painting for a room, pick a size, order your own idea and arrange delivery.",
    },
]

# Порядок пунктов верхнего меню (SOLD можно включить в админке).
# Пункт «Полезные статьи» включён на период согласования (ТЗ 1.3, Е2): владелец скрывает его в админке
# снятием галочки «Показывать», статьи и их адреса при этом не меняются. В футере ссылка уже есть.
MENU = [
    "about", "catalog", "sold", "reviews", "delivery",
    {"page": "guides", "label_ru": "Полезные статьи", "label_en": "Useful articles", "visible": True, "in_footer": False},
    "contacts",
]

HOME_SECTIONS = [
    {
        "kind": "intro",
        "title_ru": "", "title_en": "",
        "text_ru": "Море без билетов, цветы без вазы, любимый город без чемодана. Начните с сюжета, который вам близок. В каталоге есть готовые работы и примеры для заказа — статус каждой картины указан в карточке.",
        "text_en": "The sea without tickets, flowers without a vase, a favourite city without a suitcase. Start with the subject closest to you. The catalogue has ready works and examples for orders — each painting’s status is shown on its card.",
    },
    {"kind": "categories", "title_ru": "Найдите свой сюжет", "title_en": "Find your subject", "button_ru": "Весь каталог", "button_en": "Whole catalogue", "limit": 12},
    {"kind": "available", "title_ru": "В наличии", "title_en": "Available now", "button_ru": "Все работы", "button_en": "All works", "limit": 4},
    {"kind": "custom", "title_ru": "Картины под заказ", "title_en": "Made to order", "button_ru": "Все работы", "button_en": "All works", "limit": 4},
    {
        "kind": "order",
        "title_ru": "А можно такую, но немного другую?", "title_en": "Could I have one like this, but a little different?",
        "text_ru": "Можно начать с этого вопроса. Покажите понравившийся пример, расскажите о размере и оттенках — обсудим новую картину для вашего пространства.",
        "text_en": "You can start with exactly that question. Show us an example you like, tell us about the size and colours — and we will discuss a new painting for your space.",
        "button_ru": "Обсудить мою картину", "button_en": "Discuss my painting",
    },
    {"kind": "sold", "title_ru": "Проданные работы", "title_en": "Sold works", "button_ru": "Все проданные", "button_en": "All sold works", "limit": 4},
    {"kind": "reviews", "title_ru": "Отзывы", "title_en": "Reviews", "button_ru": "Все отзывы", "button_en": "All reviews", "limit": 3},
    {"kind": "delivery", "title_ru": "Картина — отдельно, дорога — отдельно", "title_en": "The painting and the journey",
     "text_ru": "Отправляем через СДЭК или согласованную с вами ТК; стоимость доставки оплачивается дополнительно.",
     "text_en": "We ship via CDEK or a carrier agreed with you; delivery is paid separately.",
     "button_ru": "Подробнее о доставке", "button_en": "More about delivery"},
    {"kind": "guides", "title_ru": "Полезное", "title_en": "Guides", "button_ru": "Все статьи", "button_en": "All articles", "limit": 3, "visible": False},
]


CTA_DEFAULT = ("Нужен другой размер или сюжет?", "Need a different size or subject?", "Заказать картину", "Order a painting")
CTA = {
    "животные-и-птицы": ("Картина с вашим любимым животным", "A painting of your favourite animal", "Обсудить заказ", "Discuss an order"),
    "животные": ("Картина с вашим любимым животным", "A painting of your favourite animal", "Обсудить заказ", "Discuss an order"),
    "портрет-и-фигура": ("Портрет по вашей фотографии?", "A portrait from your photo?", "Обсудить заказ", "Discuss an order"),
}



def _covers(prefix, omit=()):
    """Обложки рубрик из комплекта заказчика: подписи выводятся HTML-текстом, в файлах текста нет."""
    files = {
        "женщины": "01_women", "пары": "02_couples", "дети": "03_children", "пейзажи": "04_landscape",
        "абстракция": "05_abstract", "цветы-и-ботаника": "06_flowers", "животные": "07_animals",
        "птицы": "08_birds", "рыбы": "09_fish", "морские-животные": "10_marine_animals", "море": "11_sea",
        "город-и-архитектура": "12_city", "натюрморт": "13_still_life", "интерьер-и-бытовые-сцены": "14_interior",
        "прочее": "15_other", "портрет-и-фигура": "01_women", "животные-и-птицы": "07_animals",
    }
    return {slug: f"{prefix}_category_{name}.jpg" for slug, name in files.items() if name.split("_")[0] not in omit}


COVERS = _covers("mirame", omit=("10",))


def _cat(name_ru, slug_ru, name_en, slug_en, intro_ru, intro_en, seo_title_ru, seo_desc_ru, seo_title_en, seo_desc_en, children=None):
    return {
        "name_ru": name_ru, "slug_ru": slug_ru, "name_en": name_en, "slug_en": slug_en,
        "intro_ru": intro_ru, "intro_en": intro_en,
        "seo_title_ru": seo_title_ru, "seo_description_ru": seo_desc_ru,
        "seo_title_en": seo_title_en, "seo_description_en": seo_desc_en,
        "cover": COVERS.get(slug_ru), "children": children or [],
        "cover_alt_ru": "", "cover_alt_en": "",
        "cta_text_ru": CTA.get(slug_ru, CTA_DEFAULT)[0], "cta_text_en": CTA.get(slug_ru, CTA_DEFAULT)[1],
        "cta_button_ru": CTA.get(slug_ru, CTA_DEFAULT)[2], "cta_button_en": CTA.get(slug_ru, CTA_DEFAULT)[3],
    }


CATEGORIES = [
    _cat("Пейзажи", "пейзажи", "Landscapes", "landscapes",
         "Окно в любимое место — без ремонта и сквозняков. Найдите пейзаж, к которому хочется возвращаться взглядом.",
         "A window onto a favourite place — no renovation or draughts involved. Find a landscape your eyes will keep returning to.",
         "Картины-пейзажи", "Лес, горы и любимые горизонты — без сквозняков из открытого окна. Посмотрите пейзажи, уточните параметры или обсудите свою картину.",
         "Landscape paintings", "Forests, mountains and favourite horizons — without the draught from an open window. Browse landscapes, check the details or discuss your own painting."),
    _cat("Абстракция", "абстракция", "Abstract Art", "abstract-art",
         "Не обязательно искать, на что это похоже. Иногда достаточно того, как цвет и форма звучат именно для вас.",
         "No need to work out what it looks like. Sometimes it is enough how colour and shape sound to you.",
         "Абстрактные картины", "Цвет, форма и настроение без обязательного «на что похоже». Найдите свою абстракцию или расскажите, какие оттенки хочется видеть дома.",
         "Abstract paintings", "Colour, shape and mood without the obligatory “what is it?”. Find your abstract piece or tell us which shades you would like at home."),
    _cat("Животные и птицы", "животные-и-птицы", "Animals & Birds", "animals-and-birds",
         "Те, кто делает мир живее. Домашние любимцы, птицы и дикие животные — со своим характером, даже на холсте.",
         "The ones who make the world livelier. Pets, birds and wild animals — each with its own character, even on canvas.",
         "Картины с животными и птицами", "Домашние любимцы, птицы и дикие соседи по планете. Посмотрите картины с характером и выберите сюжет для своей истории.",
         "Paintings of animals and birds", "Pets, birds and our wild neighbours on the planet. Browse paintings with character and choose a subject for your story.",
         children=[
             _cat("Животные", "животные", "Animals", "animals",
                  "Домашние любимцы и дикие животные со своим характером.", "Pets and wild animals, each with its own character.",
                  "Картины с животными", "Домашние любимцы и дикие животные со своим характером. Посмотрите сюжеты или расскажите, кого хочется увидеть на вашей картине.",
                  "Paintings of animals", "Pets and wild animals with character. Browse the subjects or tell us who you would like to see in your painting."),
             _cat("Птицы", "птицы", "Birds", "birds",
                  "Легкость, перья и немного свободы для вашей стены.", "Lightness, feathers and a little freedom for your wall.",
                  "Картины с птицами", "Легкость, перья и немного свободы для вашей стены. Найдите картину с птицами или обсудите собственный сюжет и настроение.",
                  "Paintings of birds", "Lightness, feathers and a little freedom for your wall. Find a painting with birds or discuss your own subject and mood."),
             _cat("Рыбы", "рыбы", "Fish", "fish",
                  "Немного подводной жизни — без ухода за аквариумом.", "A little underwater life — no aquarium maintenance required.",
                  "Картины с рыбами", "Немного подводной жизни — без ухода за аквариумом. Посмотрите картины с рыбами, уточните размер или предложите свою идею.",
                  "Paintings of fish", "A little underwater life — no aquarium to clean. Browse paintings of fish, check a size or suggest your own idea."),
             _cat("Морские животные", "морские-животные", "Marine Animals", "marine-animals",
                  "Черепахи и другие морские обитатели, кроме рыб, собраны здесь.", "Turtles and other sea creatures — apart from fish — live here.",
                  "Картины с морскими животными", "Черепахи и другие морские обитатели, кроме рыб, собраны здесь. Посмотрите их истории и выберите сюжет, который хочется забрать домой.",
                  "Paintings of marine animals", "Turtles and other sea creatures, apart from fish, are gathered here. See their stories and choose the one you would like to take home."),
         ]),
    _cat("Море", "море", "Seascapes", "seascapes",
         "Немного моря для тех дней, когда отпуск еще не скоро. Выбирайте спокойный горизонт или волны с характером.",
         "A little sea for the days when your holiday is still far away. Choose a calm horizon or waves with character.",
         "Картины с морем", "Когда отпуск еще впереди, море может быть рядом. Спокойные горизонты, волны и береговые сюжеты — выбирайте настроение своей картины.",
         "Seascape paintings", "While your holiday is still ahead, the sea can be close by. Calm horizons, waves and coastal scenes — choose the mood of your painting."),
    _cat("Цветы и ботаника", "цветы-и-ботаника", "Flowers & Botanicals", "flowers-and-botanicals",
         "Букет, которому не нужно менять воду. Цветы и растения для своего уголка хорошего настроения.",
         "A bouquet that never needs fresh water. Flowers and plants for your own corner of good mood.",
         "Картины с цветами", "Букет, которому не нужна ваза. Посмотрите картины с цветами и растениями, выберите оттенки или обсудите собственную композицию.",
         "Flower paintings", "A bouquet that needs no vase. Browse paintings of flowers and plants, choose the shades or discuss your own composition."),
    _cat("Портрет и фигура", "портрет-и-фигура", "Portraits & Figures", "portraits-and-figures",
         "Взгляд, жест, знакомый образ. Картины о людях и том, что делает каждый образ особенным.",
         "A look, a gesture, a familiar image. Paintings about people and what makes each of them special.",
         "Портреты и картины с людьми", "Знакомый взгляд, выразительный жест, особенный образ. Посмотрите портреты и фигуративные сюжеты или расскажите о своей идее.",
         "Portraits and paintings of people", "A familiar look, an expressive gesture, a special image. Browse portraits and figurative scenes or tell us your idea.",
         children=[
             _cat("Женщины", "женщины", "Women", "women",
                  "Женские образы: нежные, смелые, задумчивые — разные, как и сами героини.",
                  "Images of women: tender, bold, thoughtful — as different as the women themselves.",
                  "Картины с женскими образами", "Нежные, смелые и задумчивые женские образы. Посмотрите картины или расскажите, какой портрет хочется видеть у себя дома.",
                  "Paintings of women", "Tender, bold and thoughtful images of women. Browse the paintings or tell us which portrait you would like to have at home."),
             _cat("Пары", "пары", "Couples", "couples",
                  "Картины о двоих: прогулки, объятия и те моменты, которые хочется сохранить.",
                  "Paintings about two people: walks, hugs and the moments worth keeping.",
                  "Картины с парами", "Прогулки, объятия и моменты, которые хочется сохранить. Выберите картину о двоих или обсудите сюжет по вашей истории.",
                  "Paintings of couples", "Walks, hugs and moments worth keeping. Choose a painting about two people or discuss a scene based on your story."),
             _cat("Дети", "дети", "Children", "children",
                  "Детство на холсте: игры, открытия и немного озорства.",
                  "Childhood on canvas: games, discoveries and a little mischief.",
                  "Картины с детьми", "Игры, открытия и немного озорства. Посмотрите картины с детьми или расскажите, какой сюжет хочется сохранить.",
                  "Paintings of children", "Games, discoveries and a little mischief. Browse paintings of children or tell us which moment you would like to keep."),
         ]),
    _cat("Город и архитектура", "город-и-архитектура", "City & Architecture", "city-and-architecture",
         "Любимые улицы могут быть ближе. Найдите свой городской сюжет или расскажите о месте, которое хочется сохранить.",
         "Favourite streets can be closer than you think. Find your city scene or tell us about a place you want to keep.",
         "Картины с городами", "Любимые улицы ближе, чем кажется. Найдите городской сюжет или расскажите о месте, которое хочется сохранить не только в телефоне.",
         "City paintings", "Favourite streets are closer than they seem. Find a city scene or tell us about a place you want to keep somewhere other than your phone."),
    _cat("Натюрморт", "натюрморт", "Still Life", "still-life",
         "Привычные вещи умеют удивлять, если посмотреть чуть внимательнее. Цвет, свет и маленькие радости повседневности.",
         "Everyday things can surprise you if you look a little closer. Colour, light and the small joys of daily life.",
         "Картины-натюрморты", "Обычные вещи тоже умеют быть главными героями. Посмотрите натюрморты, сочетания цвета и света — возможно, здесь найдется ваша картина.",
         "Still life paintings", "Ordinary things can be the main characters too. Browse still lifes and plays of colour and light — your painting may be here."),
    _cat("Интерьер и бытовые сцены", "интерьер-и-бытовые-сцены", "Interiors & Everyday Scenes", "interiors-and-everyday-scenes",
         "Тихие истории про дом и жизнь между большими событиями. Те самые моменты, из которых складывается уют.",
         "Quiet stories about home and life between the big events. The very moments cosiness is made of.",
         "Картины о доме и повседневности", "Тихие истории между большими событиями. Интерьерные сюжеты и сцены жизни для тех, кто замечает настроение в знакомых деталях.",
         "Paintings of home and everyday life", "Quiet stories between the big events. Interior scenes and moments of life for those who notice the mood in familiar details."),
    _cat("Прочее", "прочее", "Other Subjects", "other",
         "Для сюжетов, которые пока не захотели жить в одной из рубрик. Возможно, именно здесь найдется что-то ваше.",
         "For subjects that didn’t want to settle into any one category. Something of yours may be waiting right here.",
         "Другие сюжеты картин", "Для историй, которым пока тесно в одной рубрике. Посмотрите другие сюжеты — ваша картина может ждать знакомства именно здесь.",
         "Other painting subjects", "For stories that feel cramped in a single category. Browse other subjects — your painting may be waiting to meet you here."),
]

# У МираМе отдельной галереи мастерской нет: изображение страницы «О студии» задано в PAGES.
STUDIO_IMAGES = []
