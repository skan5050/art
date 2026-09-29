"""Стартовое наполнение сайта D «ХолСтори».

Русские тексты — из приложения В ТЗ, SEO — из приложения Д.
Английские тексты — черновики для проверки владельцем. Тон: деловой, спокойный,
конкретный; без шуток, канцелярита и обещаний, которых нет в условиях.
"""

SETTINGS = {
    "brand_name_ru": "ХолСтори",
    "brand_name_en": "HolStory",
    "slogan_ru": "Ваши истории на холсте.",
    "slogan_en": "Your stories on canvas.",
    "logo": "logo.png",
    "logo_alt_ru": "ХолСтори — ваши истории на холсте",
    "logo_alt_en": "HolStory — your stories on canvas",
    "logo_contains_slogan": True,
    "geography_ru": "Новосибирск и Москва. Заказы из России, стран СНГ и Европы.",
    "geography_en": "Novosibirsk and Moscow. Orders from Russia, the CIS and Europe.",
    "copyright_ru": "© {year} {brand}",
    "copyright_en": "© {year} {brand}",
    "painting_prefix_ru": "картина",
    "painting_prefix_en": "painting",
}

LABELS = {
    "catalog.order_cta": ("Картина по вашей идее", "A painting based on your idea"),
    "btn.certificate": ("Сертификат", "Certificate"),
    "painting.sold_note": (
        "Оригинал продан. Доступен запрос на новую работу по мотивам этого примера.",
        "The original has been sold. You can request a new work based on this example.",
    ),
    "painting.custom_note": (
        "Работа представлена как пример. Параметры новой картины согласуются по заявке.",
        "This work is shown as an example. The parameters of a new painting are agreed on request.",
    ),
    "error404.text": (
        "Страница не найдена: возможно, адрес изменился. Перейдите в каталог или на главную страницу.",
        "Page not found: the address may have changed. Go to the catalogue or the home page.",
    ),
}

BLOCKS = [
    {
        "key": "painting-description", "name": "Общий текст описания картины",
        "usage": "Страница картины, если выбран «Общий текст описания»",
        "text_ru": "Для уточнения информации и оформления обращения отправьте заявку по этой работе. Параметры, оформление и условия доставки согласуются индивидуально.",
        "text_en": "To clarify details or place a request, send an inquiry about this work. Parameters, framing and delivery terms are agreed individually.",
    },
    {
        "key": "delivery-short", "name": "Краткие условия доставки",
        "usage": "Страница «Доставка» (выделенный блок), страница картины, главная",
        "title_ru": "Условия доставки", "title_en": "Delivery terms",
        "text_ru": "СДЭК или любая другая ТК по согласованию с Заказчиком. Доставка в любой город; маршрут и условия уточняются индивидуально. Стоимость доставки оплачивается отдельно.",
        "text_en": "CDEK or any other carrier agreed with the customer. Delivery to any city; route and terms are agreed individually. Delivery is paid separately.",
    },
    {
        "key": "sales-map", "name": "География наших продаж — заголовок и текст",
        "usage": "Блок карты на странице «Доставка» (#geography-sales)",
        "title_ru": "География наших продаж", "title_en": "Sales geography",
        "text_ru": "На карте представлены города, в которых находятся покупатели проданных работ. Раздел дополняет портфолио и отражает подтвержденную географию продаж.",
        "text_en": "The map shows the cities where buyers of sold works are located. This section complements the portfolio and reflects confirmed sales geography.",
    },
    {
        "key": "form-intro", "name": "Вступление в форме заказа", "usage": "Модальное окно заказа",
        "text_ru": "Укажите имя и один контакт для обратной связи. Пожелания, город, размер и файл примера можно добавить при необходимости.",
        "text_en": "Enter your name and one contact for a reply. Wishes, city, size and an example file can be added if needed.",
    },
    {
        "key": "form-success", "name": "Сообщение после сохранения заявки", "usage": "Форма заказа — после успешной отправки",
        "text_ru": "Обращение зарегистрировано. Мы свяжемся с вами указанным способом для уточнения деталей.",
        "text_en": "Your request has been registered. We will contact you the way you specified to clarify the details.",
    },
    {
        "key": "form-error", "name": "Ошибка отправки заявки", "usage": "Форма заказа — если заявку не удалось сохранить",
        "text_ru": "Не удалось сохранить обращение. Введенные данные сохранены в форме. Повторите отправку либо используйте другой способ связи.",
        "text_en": "The request could not be saved. Your data remains in the form. Please try again or use another contact method.",
    },
    {
        "key": "empty-category", "name": "Пустая рубрика", "usage": "Рубрика без опубликованных картин",
        "text_ru": "В этой рубрике пока нет опубликованных работ. Выберите другую категорию или направьте запрос на индивидуальный заказ.",
        "text_en": "There are no published works in this category yet. Choose another category or send a request for a custom order.",
    },
    {
        "key": "size-hint", "name": "Подсказка к полю размера", "usage": "Поле «Желаемый размер новой картины»",
        "text_ru": "Выберите стандартный формат или укажите индивидуальные ширину и высоту. Размер, возможность исполнения и стоимость согласуются при обработке заявки.",
        "text_en": "Choose a standard format or enter a custom width and height. Size, feasibility and price are agreed when the request is processed.",
    },
    {
        "key": "size-caption", "name": "Подпись к полям размера", "usage": "Под полем размера",
        "text_ru": "Ширина × высота, см. Размер произведения без внешней рамы.",
        "text_en": "Width × height, cm. Size of the work without an outer frame.",
    },
    {
        "key": "footer-order", "name": "Подпись в футере", "usage": "Футер, над кнопками",
        "text_ru": "Давайте создадим вашу картину.",
        "text_en": "Let’s create your painting.",
    },
    {
        "key": "painting-under-button", "name": "Подпись под кнопкой заказа", "usage": "Страница картины",
        "text_ru": "Информация о выбранной работе передается в заявке автоматически.",
        "text_en": "Details of the selected work are passed on in the request automatically.",
    },
]

SEO_TEMPLATES = {
    "painting_available": {
        "title_ru": "{painting_name} — в наличии", "title_en": "{painting_name} — available",
        "description_ru": "Картина «{painting_name}» в наличии. Изображение, заполненные характеристики и запрос по работе. Доставка оплачивается отдельно.",
        "description_en": "The painting “{painting_name}” is available. Image, listed details and an inquiry form. Delivery is paid separately.",
    },
    "painting_custom": {
        "title_ru": "{painting_name} — под заказ", "title_en": "{painting_name} — made to order",
        "description_ru": "«{painting_name}» — пример для индивидуального заказа. Формат, техника, параметры, стоимость и сроки нового исполнения согласуются по заявке.",
        "description_en": "“{painting_name}” is an example for a custom order. Format, technique, parameters, price and timing of a new work are agreed on request.",
    },
    "painting_sold": {
        "title_ru": "{painting_name} — продана", "title_en": "{painting_name} — sold",
        "description_ru": "Картина «{painting_name}» продана. Представлена как часть портфолио; доступен запрос на новую работу по мотивам выбранного примера.",
        "description_en": "The painting “{painting_name}” has been sold. Shown as part of the portfolio; you can request a new work based on this example.",
    },
    "category": {
        "title_ru": "Картины: {category_name}", "title_en": "Paintings: {category_name}",
        "description_ru": "Категория «{category_name}»: изображения, статусы и параметры работ. Просмотр каталога и обращение по выбранному произведению.",
        "description_en": "Category “{category_name}”: images, statuses and parameters of works. Browse the catalogue and inquire about a selected work.",
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
        "title_ru": "Картины для вашего пространства", "title_en": "Paintings for your space",
        "nav_title_ru": "Главная", "nav_title_en": "Home",
        "banner_image": "banner.jpg",
        "banner_kicker_ru": "Картины в наличии и на заказ", "banner_kicker_en": "Paintings available and made to order",
        "banner_title_ru": "", "banner_title_en": "",
        "banner_text_ru": "Готовые работы и индивидуальные заказы. Выберите произведение в каталоге или согласуйте сюжет, формат и исполнение новой картины.",
        "banner_text_en": "Ready works and custom commissions. Choose a work from the catalogue or agree the subject, format and execution of a new painting.",
        "banner_button1_ru": "Перейти в каталог", "banner_button1_en": "Go to catalogue", "banner_button1_link": "catalog",
        "banner_button2_ru": "Обсудить заказ", "banner_button2_en": "Discuss an order",
        "banner_focus_x": 60, "banner_focus_y": 45,
        "seo_title_ru": "Картины в наличии и на заказ", "seo_title_en": "Paintings available and made to order",
        "seo_description_ru": "Каталог готовых картин и индивидуальные заказы. Изображения, характеристики, статусы работ, портфолио и обращение по выбранному произведению.",
        "seo_description_en": "A catalogue of ready paintings and custom orders. Images, details, work statuses, portfolio and inquiries about a selected work.",
    },
    {
        "kind": "about", "slug_ru": "о-нас", "slug_en": "about",
        "title_ru": "Выбор и заказ картин", "title_en": "Choosing and ordering paintings",
        "nav_title_ru": "О нас", "nav_title_en": "About",
        "body_ru": (
            "Мы предлагаем два формата обращения: выбор конкретной картины из наличия и обсуждение новой работы по индивидуальным пожеланиям. Каталог помогает сопоставить сюжеты и перейти к рассмотрению подходящего произведения.\n\n"
            "Информация о работе размещается в ее карточке: фотография, статус, описание и известные параметры. Недостающие сведения можно уточнить до принятия решения. Для индивидуального заказа обсуждаются содержание, формат, техника, оформление, стоимость и срок выполнения.\n\n"
            "Проданные картины представлены в отдельном разделе портфолио. Они могут использоваться как ориентиры для новых заказов. География наших продаж показывает подтвержденные города покупателей и не определяет условия доставки."
        ),
        "body_en": (
            "We offer two ways to work with us: choosing a specific painting from stock, or discussing a new work to individual requirements. The catalogue helps compare subjects and move on to a suitable work.\n\n"
            "Information about each work is on its page: photograph, status, description and known parameters. Missing details can be clarified before you decide. For a custom order we discuss content, format, technique, framing, price and timing.\n\n"
            "Sold paintings are shown in a separate portfolio section. They can serve as references for new orders. Our sales geography shows confirmed buyers’ cities and does not define delivery terms."
        ),
        "button_ru": "Связаться с нами", "button_en": "Contact us",
        "seo_title_ru": "О нас", "seo_title_en": "About us",
        "seo_description_ru": "Информация о подходе к выбору и заказу картин. Готовые произведения, индивидуальное исполнение и порядок согласования параметров работы.",
        "seo_description_en": "How we approach choosing and ordering paintings. Ready works, custom execution and how the parameters of a work are agreed.",
    },
    {
        "kind": "catalog", "slug_ru": "каталог", "slug_en": "catalog",
        "title_ru": "Каталог картин", "title_en": "Painting catalogue",
        "nav_title_ru": "Каталог", "nav_title_en": "Catalogue",
        "intro_ru": "Выберите жанр и перейдите к просмотру работ. Статус, описание и заполненные характеристики доступны на странице каждой картины.",
        "intro_en": "Choose a genre and browse the works. Status, description and listed details are available on each painting’s page.",
        "seo_title_ru": "Каталог картин", "seo_title_en": "Painting catalogue",
        "seo_description_ru": "Картины по жанрам: пейзаж, абстракция, портрет, цветы и другие направления. Фотографии, актуальные статусы и параметры опубликованных работ.",
        "seo_description_en": "Paintings by genre: landscape, abstract, portrait, flowers and more. Photos, current statuses and parameters of published works.",
    },
    {
        "kind": "sold", "slug_ru": "проданные-картины", "slug_en": "sold",
        "title_ru": "Проданные работы", "title_en": "Sold works",
        "nav_title_ru": "SOLD", "nav_title_en": "SOLD",
        "intro_ru": "В разделе представлены картины, которые уже приобретены и не доступны как находящиеся в наличии оригиналы. Для обсуждения новой работы на основе выбранного примера воспользуйтесь действием «Заказать похожую». Параметры, стоимость и срок исполнения согласуются отдельно.",
        "intro_en": "This section shows paintings that have already been purchased and are not available as originals in stock. To discuss a new work based on a selected example, use “Order a similar one”. Parameters, price and timing are agreed separately.",
        "empty_ru": "Проданные работы еще не опубликованы. Доступные картины и примеры для заказа представлены в каталоге.",
        "empty_en": "Sold works have not been published yet. Available paintings and examples for orders are in the catalogue.",
        "button_ru": "Заказать похожую", "button_en": "Order a similar one",
        "seo_title_ru": "Проданные картины — SOLD", "seo_title_en": "Sold paintings — SOLD",
        "seo_description_ru": "Портфолио проданных картин. Представленные оригиналы недоступны как работы в наличии; можно направить запрос на похожую новую картину.",
        "seo_description_en": "Portfolio of sold paintings. The originals shown are not available in stock; you can request a similar new painting.",
    },
    {
        "kind": "reviews", "slug_ru": "отзывы", "slug_en": "reviews",
        "title_ru": "Отзывы", "title_en": "Reviews",
        "intro_ru": "В этом разделе публикуются отзывы покупателей о приобретенных работах и взаимодействии по заказам.",
        "intro_en": "This section publishes buyers’ reviews of purchased works and of working with us on orders.",
        "empty_ru": "Отзывы пока не опубликованы. Вопросы о картинах и условиях заказа можно направить через форму обращения.",
        "empty_en": "No reviews have been published yet. Questions about paintings and order terms can be sent via the inquiry form.",
        "seo_title_ru": "Отзывы", "seo_title_en": "Reviews",
        "seo_description_ru": "Раздел отзывов покупателей о приобретенных картинах и взаимодействии по заказам. Публикуются предоставленные и подтвержденные материалы.",
        "seo_description_en": "Buyers’ reviews of purchased paintings and of working with us on orders. Only provided and confirmed materials are published.",
    },
    {
        "kind": "delivery", "slug_ru": "доставка", "slug_en": "delivery",
        "title_ru": "Доставка картин: способы и условия", "title_en": "Painting delivery: methods and terms",
        "nav_title_ru": "Доставка", "nav_title_en": "Delivery",
        "intro_ru": "Отправляем работы в любой город через СДЭК или другую транспортную компанию по согласованию с Заказчиком. Доставка оплачивается отдельно от стоимости картины.",
        "intro_en": "We ship works to any city via CDEK or another carrier agreed with the customer. Delivery is paid separately from the price of the painting.",
        "body_ru": (
            "## Выбор перевозчика и маршрута\n"
            "Перевозчик определяется совместно с Заказчиком. Можно выбрать СДЭК либо предложить другую транспортную компанию. До отправки согласуются маршрут, доступный способ получения и условия перевозки конкретной работы. Для зарубежных направлений возможность выбранного маршрута и необходимые формальности уточняются отдельно.\n\n"
            "## Сведения для согласования\n"
            "Сообщите город назначения и выбранную картину. Если речь идет о новой работе, укажите предполагаемые размеры и оформление. Эти данные позволяют уточнить подходящий вариант перевозки и параметры отправления. Отсутствие города в карте продаж не препятствует обращению по доставке.\n\n"
            "## Стоимость\n"
            "Доставка оплачивается Заказчиком отдельно и не входит в стоимость картины. Итоговая сумма определяется по маршруту, габаритам и весу упакованной работы, а также условиям выбранной транспортной компании. Стоимость и порядок оплаты доставки согласуются до отправки. Фиксированный общий тариф для всех картин и направлений не применяется.\n\n"
            "## Подготовка и упаковка\n"
            "Подготовка к перевозке определяется размером, основой, оформлением картины и условиями транспортной компании. Требования к упаковке и особенности отправления согласуются до передачи груза перевозчику.\n\n"
            "## Сроки\n"
            "Срок изготовления картины и срок доставки учитываются отдельно. Ориентировочный срок перевозки уточняется по выбранному маршруту. Если получение необходимо к определенной дате, ее нужно указать при первом обращении, до согласования заказа.\n\n"
            "Для обсуждения отправки используйте форму связи. В обращении достаточно указать город и работу; остальные сведения уточняются в процессе согласования."
        ),
        "body_en": (
            "## Choosing the carrier and route\n"
            "The carrier is chosen together with the customer. You can choose CDEK or suggest another transport company. Before shipping we agree the route, the available way of receiving the parcel and the transport conditions for the specific work. For destinations abroad, the feasibility of the route and any formalities are clarified separately.\n\n"
            "## Information needed\n"
            "Tell us the destination city and the painting you have chosen. For a new work, give the planned size and framing. This lets us identify a suitable shipping option and the parcel parameters. If your city is not on the sales map, you can still ask about delivery.\n\n"
            "## Cost\n"
            "Delivery is paid by the customer separately and is not included in the price of the painting. The total depends on the route, the size and weight of the packed work and the chosen carrier’s terms. Delivery cost and payment method are agreed before shipping. There is no single fixed rate for all paintings and destinations.\n\n"
            "## Preparation and packaging\n"
            "Preparation for transport depends on the painting’s size, support, framing and the carrier’s requirements. Packaging requirements and shipping specifics are agreed before the parcel is handed to the carrier.\n\n"
            "## Timing\n"
            "The time to make a painting and the time to deliver it are counted separately. The approximate transit time is confirmed for the chosen route. If you need the painting by a certain date, state it in your first inquiry, before the order is agreed.\n\n"
            "To discuss shipping, use the contact form. It is enough to give the city and the work; other details are clarified along the way."
        ),
        "note_ru": "Отметки показывают состоявшиеся продажи. Перечень городов не ограничивает доставку и не является списком направлений транспортных компаний.",
        "note_en": "Markers show completed sales. The list of cities does not limit delivery and is not a list of carrier destinations.",
        "empty_ru": "Города будут отображены после добавления подтвержденных данных о продажах.",
        "empty_en": "Cities will be shown once confirmed sales data is added.",
        "button_ru": "Согласовать доставку", "button_en": "Arrange delivery",
        "seo_title_ru": "Доставка картин", "seo_title_en": "Painting delivery",
        "seo_description_ru": "Отправка картин в любой город через СДЭК или другую ТК по согласованию с Заказчиком. Стоимость доставки оплачивается отдельно от картины.",
        "seo_description_en": "Shipping paintings to any city via CDEK or another carrier agreed with the customer. Delivery is paid separately from the painting.",
    },
    {
        "kind": "contacts", "slug_ru": "контакты", "slug_en": "contacts",
        "title_ru": "Связь по вопросам покупки и заказа", "title_en": "Contact us about purchases and orders",
        "nav_title_ru": "Контакты", "nav_title_en": "Contacts",
        "intro_ru": "Обратитесь для уточнения наличия, характеристик, индивидуального исполнения или доставки. Выберите один удобный способ связи. В обращении со страницы картины информация о выбранной работе передается автоматически.",
        "intro_en": "Contact us to check availability, details, custom execution or delivery. Choose one convenient contact method. When you write from a painting’s page, the selected work is included automatically.",
        "seo_title_ru": "Контакты", "seo_title_en": "Contacts",
        "seo_description_ru": "Связь по вопросам наличия, характеристик картин, индивидуального исполнения и доставки. Актуальные контакты и форма обращения.",
        "seo_description_en": "Contact us about availability, painting details, custom execution and delivery. Current contacts and an inquiry form.",
    },
    {
        "kind": "certificate", "slug_ru": "подарочный-сертификат", "slug_en": "gift-certificate",
        "title_ru": "Сертификат на выбор картины", "title_en": "A certificate to choose a painting",
        "nav_title_ru": "Подарочный сертификат", "nav_title_en": "Gift certificate",
        "body_ru": (
            "Подарочный сертификат позволяет получателю самостоятельно выбрать подходящую работу в рамках согласованных условий. Для оформления укажите доступный номинал, формат и контакт для связи.\n\n"
            "До приобретения согласуются срок действия, порядок использования, доступные форматы и применимость к готовым работам или индивидуальным заказам. Заявка через сайт запускает обсуждение и не означает автоматический выпуск сертификата."
        ),
        "body_en": (
            "A gift certificate lets the recipient choose a suitable work within the agreed terms. To arrange one, specify an available amount, the format and a contact.\n\n"
            "Before purchase we agree the validity period, terms of use, available formats and whether it applies to ready works or custom orders. A request via the site starts the discussion and does not mean the certificate is issued automatically."
        ),
        "button_ru": "Оставить заявку на сертификат", "button_en": "Request a certificate",
        "seo_title_ru": "Подарочный сертификат", "seo_title_en": "Gift certificate",
        "seo_description_ru": "Сертификат на выбор картины. Доступные номиналы и форматы, заявка на оформление; срок действия и порядок использования согласуются заранее.",
        "seo_description_en": "A certificate to choose a painting. Available amounts and formats, request form; validity and terms of use are agreed in advance.",
    },
    {
        "kind": "custom", "slug_ru": "картины-на-заказ", "slug_en": "custom-paintings",
        "title_ru": "Индивидуальный заказ картины", "title_en": "Commissioning a painting",
        "nav_title_ru": "Картины на заказ", "nav_title_en": "Paintings to order",
        "body_ru": (
            "Для предварительного обсуждения укажите сюжет, предполагаемый размер и основные требования к цвету или композиции. При наличии приложите изображение-ориентир или фотографию пространства. Если заказ связан с определенной датой, сообщите желаемый день получения.\n\n"
            "После обращения уточняются возможность выполнения, техника, основа, оформление, стоимость и сроки. Параметры новой работы согласуются отдельно, в том числе при использовании проданной картины из портфолио в качестве примера.\n\n"
            "Отправка заявки не является оплатой, автоматическим резервированием или окончательным подтверждением заказа. Условия изготовления и получения согласуются до начала выполнения."
        ),
        "body_en": (
            "For a preliminary discussion, give the subject, planned size and main requirements for colour or composition. If available, attach a reference image or a photo of the space. If the order is tied to a date, state when you need to receive it.\n\n"
            "After your inquiry we clarify feasibility, technique, support, framing, price and timing. The parameters of the new work are agreed separately, including when a sold painting from the portfolio is used as an example.\n\n"
            "Sending a request is not a payment, an automatic reservation or a final order confirmation. Production and delivery terms are agreed before work begins."
        ),
        "button_ru": "Обсудить индивидуальный заказ", "button_en": "Discuss a custom order",
        "seo_title_ru": "Картины на заказ", "seo_title_en": "Paintings made to order",
        "seo_description_ru": "Индивидуальное исполнение картины по согласованным пожеланиям. Сюжет, формат, техника, оформление, стоимость и сроки обсуждаются до начала работы.",
        "seo_description_en": "Custom execution of a painting to agreed requirements. Subject, format, technique, framing, price and timing are discussed before work begins.",
    },
    {
        "kind": "studio", "slug_ru": "студия", "slug_en": "studio",
        "title_ru": "Мастерская и порядок работы", "title_en": "The studio and how we work",
        "nav_title_ru": "О студии", "nav_title_en": "The studio",
        "body_ru": (
            "Мастерская работает в Новосибирске и Москве. Заказы принимаются из России, стран СНГ и Европы. Личный прием клиентов не проводится: обсуждение, согласование и передача материалов выполняются дистанционно.\n\n"
            "## Порядок работы\n"
            "- Обращение: выбор картины из каталога или описание задачи для индивидуального заказа.\n"
            "- Согласование: параметры работы, оформление, стоимость, сроки и доставка.\n"
            "- Выполнение и подготовка к отправке — по согласованным условиям.\n"
            "- Передача транспортной компании и получение.\n\n"
            "Изображения в этом разделе являются иллюстрациями и не представляют фотографии конкретного помещения."
        ),
        "body_en": (
            "The studio works in Novosibirsk and Moscow. Orders are accepted from Russia, the CIS and Europe. We do not receive clients in person: discussion, agreement and exchange of materials take place remotely.\n\n"
            "## How we work\n"
            "- Inquiry: choosing a painting from the catalogue or describing the task for a custom order.\n"
            "- Agreement: parameters of the work, framing, price, timing and delivery.\n"
            "- Execution and preparation for shipping on the agreed terms.\n"
            "- Handover to the carrier and receipt.\n\n"
            "The images in this section are illustrations and do not show photographs of a specific room."
        ),
        "button_ru": "Отправить пожелания", "button_en": "Send your requirements",
        "seo_title_ru": "О студии", "seo_title_en": "About the studio",
        "seo_description_ru": "Мастерская в Новосибирске и Москве, заказы из России, СНГ и Европы. Порядок работы: обращение, согласование, выполнение, доставка.",
        "seo_description_en": "A studio in Novosibirsk and Moscow, orders from Russia, the CIS and Europe. How we work: inquiry, agreement, execution, delivery.",
    },
    {
        "kind": "guides", "slug_ru": "полезное", "slug_en": "guides",
        "title_ru": "Полезное", "title_en": "Guides",
        "intro_ru": "Справочные материалы о выборе, заказе, оформлении, хранении и доставке картин.",
        "intro_en": "Reference materials on choosing, ordering, framing, storing and shipping paintings.",
        "empty_ru": "Материалы будут опубликованы позже.", "empty_en": "Materials will be published later.",
        "seo_title_ru": "Полезное: выбор, заказ и доставка картин", "seo_title_en": "Guides: choosing, ordering and shipping paintings",
        "seo_description_ru": "Справочные материалы: как выбрать размер и формат картины, подготовить индивидуальный заказ, выбрать оформление, организовать хранение и доставку.",
        "seo_description_en": "Reference materials: choosing a painting’s size and format, preparing a custom order, framing, storage and delivery.",
    },
]

MENU = ["about", "catalog", "sold", "reviews", "delivery", "contacts"]

HOME_SECTIONS = [
    {
        "kind": "intro", "title_ru": "Готовая работа или индивидуальный заказ", "title_en": "A ready work or a custom order",
        "text_ru": "Каталог организован по жанрам. На странице каждой работы представлены изображение, статус и заполненные характеристики. Для заказа или уточнения информации отправьте обращение из карточки — выбранная работа будет указана автоматически.",
        "text_en": "The catalogue is organised by genre. Each work’s page shows the image, status and listed details. To order or ask a question, send an inquiry from the work’s page — the selected work will be included automatically.",
    },
    {"kind": "categories", "title_ru": "Жанры каталога", "title_en": "Catalogue genres", "button_ru": "Весь каталог", "button_en": "Whole catalogue"},
    {
        "kind": "order", "title_ru": "Индивидуальная работа под ваши задачи", "title_en": "A custom work for your needs",
        "text_ru": "Передайте пожелания к сюжету, цвету, размеру и оформлению. Возможность исполнения, стоимость и сроки согласуются до начала работы.",
        "text_en": "Send your requirements for subject, colour, size and framing. Feasibility, price and timing are agreed before work begins.",
        "button_ru": "Отправить пожелания", "button_en": "Send your requirements",
    },
    {"kind": "available", "title_ru": "В наличии", "title_en": "Available", "button_ru": "Каталог", "button_en": "Catalogue", "limit": 4},
    {"kind": "custom", "title_ru": "Примеры для заказа", "title_en": "Examples for orders", "button_ru": "Каталог", "button_en": "Catalogue", "limit": 4},
    {"kind": "sold", "title_ru": "Проданные работы", "title_en": "Sold works", "button_ru": "Раздел SOLD", "button_en": "SOLD section", "limit": 4},
    {"kind": "reviews", "title_ru": "Отзывы", "title_en": "Reviews", "button_ru": "Все отзывы", "button_en": "All reviews", "limit": 3},
    {"kind": "delivery", "title_ru": "Доставка", "title_en": "Delivery",
     "text_ru": "Отправка через СДЭК или другую ТК по согласованию с Заказчиком. Стоимость доставки оплачивается отдельно от стоимости картины.",
     "text_en": "Shipping via CDEK or another carrier agreed with the customer. Delivery is paid separately from the price of the painting.",
     "button_ru": "Условия доставки", "button_en": "Delivery terms"},
    {"kind": "guides", "title_ru": "Полезное", "title_en": "Guides", "button_ru": "Все материалы", "button_en": "All materials", "limit": 3, "visible": False},
]


COVERS = {"абстракция": "cover-abstract.jpg", "море": "cover-sea.jpg", "цветы-и-ботаника": "cover-flowers.jpg", "пейзажи": "cover-landscape.jpg"}


def _cat(name_ru, slug_ru, name_en, slug_en, intro_ru, intro_en, seo_title_ru, seo_desc_ru, seo_title_en, seo_desc_en, children=None):
    return {
        "cover": COVERS.get(slug_ru),
        "name_ru": name_ru, "slug_ru": slug_ru, "name_en": name_en, "slug_en": slug_en,
        "intro_ru": intro_ru, "intro_en": intro_en,
        "seo_title_ru": seo_title_ru, "seo_description_ru": seo_desc_ru,
        "seo_title_en": seo_title_en, "seo_description_en": seo_desc_en,
        "children": children or [],
    }


CATEGORIES = [
    _cat("Пейзажи", "пейзажи", "Landscapes", "landscapes",
         "Природные виды и ландшафтные композиции. Выберите работу по сюжету, формату и характеру исполнения.",
         "Natural views and landscape compositions. Choose a work by subject, format and style of execution.",
         "Картины-пейзажи", "Пейзажная живопись: природные виды и ландшафтные композиции. Фотографии работ, статус, заполненные характеристики и обращение по картине.",
         "Landscape paintings", "Landscape painting: natural views and landscape compositions. Photos, status, listed details and inquiries about each work."),
    _cat("Абстракция", "абстракция", "Abstract Art", "abstract-art",
         "Композиции, основанные на цвете, форме и фактуре. Представлены готовые работы и ориентиры для индивидуального заказа.",
         "Compositions based on colour, form and texture. Ready works and references for custom orders.",
         "Абстрактные картины", "Абстрактные композиции в каталоге. Изображения, формат и техника при наличии данных; выбор готовой работы или обсуждение индивидуального заказа.",
         "Abstract paintings", "Abstract compositions in the catalogue. Images, format and technique where available; choose a ready work or discuss a custom order."),
    _cat("Животные и птицы", "животные-и-птицы", "Animals & Birds", "animals-and-birds",
         "Изображения животных и птиц. Рыбы и остальные морские животные выделены в самостоятельные подрубрики.",
         "Images of animals and birds. Fish and other marine animals have their own subcategories.",
         "Картины с животными и птицами", "Изображения животных и птиц. Вложенные рубрики, фотографии, статусы и параметры работ; возможность обсуждения индивидуального сюжета.",
         "Paintings of animals and birds", "Images of animals and birds. Subcategories, photos, statuses and parameters of works; a custom subject can be discussed.",
         children=[
             _cat("Животные", "животные", "Animals", "animals",
                  "Картины с домашними и дикими животными.", "Paintings of domestic and wild animals.",
                  "Картины с животными", "Картины с домашними и дикими животными. Изображения, статус и параметры работ; запрос на индивидуальный сюжет или похожую композицию.",
                  "Paintings of animals", "Paintings of domestic and wild animals. Images, status and parameters; request a custom subject or a similar composition."),
             _cat("Птицы", "птицы", "Birds", "birds",
                  "Изображения птиц в живописи.", "Birds in painting.",
                  "Картины с птицами", "Изображения птиц в живописи. Выбор произведения по сюжету и характеристикам, актуальный статус и обращение по выбранной работе.",
                  "Paintings of birds", "Birds in painting. Choose a work by subject and details; current status and inquiries about a selected work."),
             _cat("Рыбы", "рыбы", "Fish", "fish",
                  "Живописные сюжеты с рыбами.", "Painted subjects with fish.",
                  "Картины с рыбами", "Живописные сюжеты с рыбами. Фотографии работ и известные параметры, выбор готовой картины или обсуждение нового исполнения.",
                  "Paintings of fish", "Painted subjects with fish. Photos and known parameters; choose a ready painting or discuss a new one."),
             _cat("Морские животные", "морские-животные", "Marine Animals", "marine-animals",
                  "Черепахи и другие морские животные, кроме рыб.", "Turtles and other marine animals, excluding fish.",
                  "Картины с морскими животными", "Картины с черепахами и другими морскими животными, кроме рыб. Изображения, статусы и характеристики; рыбы представлены в отдельной подрубрике.",
                  "Paintings of marine animals", "Paintings of turtles and other marine animals, excluding fish. Images, statuses and details; fish have a separate subcategory."),
         ]),
    _cat("Море", "море", "Seascapes", "seascapes",
         "Морские пейзажи, береговые виды и композиции с водной поверхностью. Характеристики уточняются в карточках работ.",
         "Seascapes, coastal views and compositions with water. Details are given on each work’s page.",
         "Морские пейзажи", "Картины с морем: береговые виды, волны и водная поверхность. Выбор по изображению и характеристикам; запрос по конкретной работе.",
         "Seascapes", "Paintings of the sea: coastal views, waves and water. Choose by image and details; inquire about a specific work."),
    _cat("Цветы и ботаника", "цветы-и-ботаника", "Flowers & Botanicals", "flowers-and-botanicals",
         "Цветочные и растительные сюжеты. Для каждой работы доступны изображение, статус и заполненные параметры.",
         "Floral and botanical subjects. Each work has an image, status and listed parameters.",
         "Картины с цветами и растениями", "Цветочные и ботанические сюжеты. Фотографии картин, доступные характеристики и статус; параметры индивидуального исполнения согласуются по заявке.",
         "Paintings of flowers and plants", "Floral and botanical subjects. Photos, available details and status; custom execution is agreed on request."),
    _cat("Портрет и фигура", "портрет-и-фигура", "Portraits & Figures", "portraits-and-figures",
         "Портретные и фигуративные произведения. Индивидуальный сюжет и параметры исполнения согласуются по заявке.",
         "Portrait and figurative works. A custom subject and execution parameters are agreed on request.",
         "Портреты и фигуративная живопись", "Портретные и фигуративные произведения. Каталог изображений и статусов работ; индивидуальный образ, формат и исполнение обсуждаются отдельно.",
         "Portraits and figurative painting", "Portrait and figurative works. A catalogue of images and statuses; a custom image, format and execution are discussed separately.",
         children=[
             _cat("Женщины", "женщины", "Women", "women",
                  "Женские портреты и фигуративные композиции.", "Portraits of women and figurative compositions.",
                  "Картины с женскими образами", "Женские портреты и фигуративные композиции. Изображения, статус и параметры работ; индивидуальный портрет обсуждается по заявке.",
                  "Paintings of women", "Portraits of women and figurative compositions. Images, status and parameters; a custom portrait is discussed on request."),
             _cat("Пары", "пары", "Couples", "couples",
                  "Композиции с парами: портреты и сюжетные сцены.", "Compositions with couples: portraits and narrative scenes.",
                  "Картины с парами", "Композиции с парами: портреты и сюжетные сцены. Выбор работы по изображению и характеристикам или запрос на индивидуальный сюжет.",
                  "Paintings of couples", "Compositions with couples: portraits and narrative scenes. Choose a work by image and details or request a custom subject."),
             _cat("Дети", "дети", "Children", "children",
                  "Детские портреты и сюжеты.", "Portraits and scenes of children.",
                  "Картины с детьми", "Детские портреты и сюжеты. Изображения, статус и параметры работ; портрет по фотографии обсуждается индивидуально.",
                  "Paintings of children", "Portraits and scenes of children. Images, status and parameters; a portrait from a photo is discussed individually."),
         ]),
    _cat("Город и архитектура", "город-и-архитектура", "City & Architecture", "city-and-architecture",
         "Городские виды и архитектурные композиции. Возможность выполнения конкретного сюжета обсуждается отдельно.",
         "Cityscapes and architectural compositions. Whether a specific subject can be done is discussed separately.",
         "Городские и архитектурные картины", "Городские виды и архитектурные композиции. Параметры готовых работ и примеры для индивидуального заказа; запрос из карточки картины.",
         "City and architecture paintings", "Cityscapes and architectural compositions. Parameters of ready works and examples for custom orders; inquire from a work’s page."),
    _cat("Натюрморт", "натюрморт", "Still Life", "still-life",
         "Композиции из предметов и природных элементов. Выбор по изображению и характеристикам работы.",
         "Compositions of objects and natural elements. Choose by image and details.",
         "Картины-натюрморты", "Натюрморты: предметные композиции и природные элементы. Фотографии, статусы и заполненные характеристики произведений, обращение по выбранной работе.",
         "Still life paintings", "Still lifes: compositions of objects and natural elements. Photos, statuses and listed details; inquire about a selected work."),
    _cat("Интерьер и бытовые сцены", "интерьер-и-бытовые-сцены", "Interiors & Everyday Scenes", "interiors-and-everyday-scenes",
         "Интерьерные сюжеты и сцены повседневной жизни. Работы представлены с указанием актуального статуса.",
         "Interior subjects and scenes of everyday life. Works are shown with their current status.",
         "Интерьерные и бытовые сцены", "Живописные интерьерные сюжеты и сцены повседневной жизни. Просмотр работ по изображению, статусу и доступным параметрам.",
         "Interiors and everyday scenes", "Painted interiors and scenes of everyday life. Browse works by image, status and available parameters."),
    _cat("Прочее", "прочее", "Other Subjects", "other",
         "Работы других тематических направлений. Уточнить параметры или обсудить похожий заказ можно из карточки.",
         "Works in other themes. Ask about parameters or discuss a similar order from the work’s page.",
         "Другие сюжеты картин", "Работы других тематических направлений. Изображения и сведения о картинах; уточнение параметров и обсуждение похожей работы через форму.",
         "Other painting subjects", "Works in other themes. Images and information; clarify parameters and discuss a similar work via the form."),
]
