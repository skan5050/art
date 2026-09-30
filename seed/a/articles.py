"""Статьи раздела «Полезное / Guides» сайта A «МираМе».

Статьи 1–3 — тексты приложения Б (Б11–Б13) и метаданные Д4.
Остальные — черновики под реальные вопросы покупателей; владелец может
править и снимать их с публикации в админке. Тексты не содержат выдуманных
сроков, цен, продаж и фактов о мастерской.
"""
from .articles_more import ARTICLES_MORE

ARTICLES = [
    {
        "slug_ru": "картина-в-интерьере", "slug_en": "painting-for-your-room",
        "cover": "mirame_article_01_interer.jpg", "cover_alt_ru": "Две картины в светлых рамах у окна: морской пейзаж и ветка оливы", "cover_alt_en": "Two framed paintings by a window: a seascape and an olive branch",
        "title_ru": "Как выбрать картину для интерьера — и не спрашивать разрешения у дивана",
        "title_en": "How to choose a painting for your interior — without asking the sofa’s permission",
        "excerpt_ru": "Картине не обязательно быть точной родственницей штор. Начните с места, размера и собственного ощущения: хочется ли видеть эту работу рядом каждый день?",
        "excerpt_en": "A painting doesn’t have to be a close relative of your curtains. Start with the place, the size and your own feeling: would you like to see this work every day?",
        "body_ru": (
            "## Сначала найдите ей место\n"
            "Посмотрите на комнату так, будто вы только что в нее вошли. Где взгляд задерживается, а где остается пустое пространство? Представьте картину над диваном, у стола или на отдельной стене. Сделайте фотографию с мебелью в кадре: так легче обсуждать работу вместе с интерьером, а не в воображаемой комнате без размеров.\n\n"
            "## Примерка — не только для одежды\n"
            "Прежде чем выбирать формат, обозначьте будущую картину бумажным шаблоном подходящего размера. Закрепляйте его способом, безопасным для вашей отделки. Посмотрите из разных точек комнаты и сравните несколько вариантов. Слишком маленький размер может потеряться, слишком большой — занять больше внимания, чем хотелось. Универсального ответа здесь нет: примерка нужна именно для вашего пространства.\n\n"
            "## Цвет может соглашаться, а может спорить\n"
            "Один путь — поддержать оттенки, которые уже есть в комнате. Другой — добавить новый акцент. Попробуйте оба. Не отказывайтесь от понравившейся работы только потому, что в ней нет цвета подушки: у подушки уже есть важная работа — быть удобной. Оцените общее настроение, свет и сочетание крупных цветовых пятен.\n\n"
            "## Выбирайте сюжет, к которому хочется возвращаться\n"
            "Сохраните несколько работ [из каталога](/каталог/) и посмотрите на них спустя время. Что по-прежнему нравится: [тихий горизонт](/каталог/море/), яркая линия, знакомый город или выразительный портрет? Запишите пару слов. «Спокойно», «воздушно» или «напоминает наш отпуск» помогают объяснить выбор не хуже специальных терминов.\n\n"
            "## Перед решением — немного практики\n"
            "Проверьте статус, размер, технику и оформление в карточке. Уточните, показана готовая работа или пример для заказа. Если параметры не указаны, задайте вопрос. Отдельно обсудите раму и [доставку](/доставка/): фотография не заменяет эти сведения. Если подходящей работы не нашлось, можно [заказать картину](/картины-на-заказ/). Начать можно с изображения комнаты и короткого сообщения — большой художественный совет созывать не нужно."
        ),
        "body_en": (
            "## First, find it a place\n"
            "Look at the room as if you have just walked in. Where does your eye linger, and where is there empty space? Picture the painting above the sofa, by the desk or on a wall of its own. Take a photo with the furniture in the frame: it is easier to discuss a work together with the interior than in an imaginary room with no dimensions.\n\n"
            "## Trying on isn’t just for clothes\n"
            "Before choosing a format, mark out the future painting with a paper template of the right size. Fix it in a way that is safe for your walls. Look at it from different spots in the room and compare a few options. A size that is too small can get lost; one that is too big can take more attention than you wanted. There is no universal answer — the trial is for your particular space.\n\n"
            "## Colour can agree or it can argue\n"
            "One way is to support the shades already in the room. Another is to add a new accent. Try both. Don’t give up on a work you love just because it lacks the colour of your cushion: the cushion already has an important job — being comfortable. Judge the overall mood, the light and how the large areas of colour work together.\n\n"
            "## Choose a subject you want to come back to\n"
            "Save a few works [from the catalogue](/en/catalog/) and look at them again after a while. What do you still like: [a quiet horizon](/en/catalog/seascapes/), a bold line, a familiar city or an expressive portrait? Write down a couple of words. “Calm”, “airy” or “reminds us of our holiday” explain a choice as well as any technical term.\n\n"
            "## A little practicality before deciding\n"
            "Check the status, size, technique and framing on the work’s page. Make sure whether it is a ready work or an example for an order. If details are missing, ask. Discuss the frame and [delivery](/en/delivery/) separately: a photo doesn’t replace that information. If you don’t find the right work, you can [order a painting](/en/custom-paintings/). You can start with a picture of your room and a short message — no need to convene a grand art council."
        ),
        "button_ru": "Подобрать картину для моей комнаты", "button_en": "Find a painting for my room",
        "seo_title_ru": "Как выбрать картину для комнаты", "seo_title_en": "How to choose a painting for a room",
        "seo_description_ru": "Нужно ли спрашивать разрешения у дивана? Разбираемся с местом, размером, цветом и сюжетом картины без строгих правил и лишней суеты.",
        "seo_description_en": "Do you need the sofa’s permission? We look at the place, size, colour and subject of a painting — without strict rules or fuss.",
    },
    {
        "slug_ru": "готовая-или-на-заказ", "slug_en": "ready-made-or-commissioned",
        "cover": "mirame_article_02_gotovaya_ili_zakaz.jpg", "cover_alt_ru": "Мастерская: мольберт с морским пейзажем, кисти и палитра на рабочем столе", "cover_alt_en": "A studio: an easel with a seascape, brushes and a palette on the work table",
        "title_ru": "Готовая картина или картина на заказ: что выбрать?",
        "title_en": "A ready painting or a painting made to order: which to choose?",
        "excerpt_ru": "Иногда все понятно с первого взгляда. А иногда нравится почти все, кроме размера, оттенка и еще одной маленькой детали. Для этих случаев есть два разных пути.",
        "excerpt_en": "Sometimes it is clear at first sight. And sometimes you like almost everything except the size, the shade and one more little detail. There are two different paths for these cases.",
        "body_ru": (
            "## Готовая работа: нравится именно она\n"
            "Картина [из наличия](/каталог/) подходит, когда вы выбираете конкретную представленную работу. Посмотрите размеры, технику, оформление и задайте вопросы, которые остались. Не нужно придумывать новый сюжет, если нужный уже нашелся. Но слово «в наличии» не означает «завтра у двери»: способ и срок получения согласуются отдельно.\n\n"
            "## Под заказ: хочется сделать по-своему\n"
            "Другой размер для узкой стены, спокойнее оттенки, важное место или личный сюжет — повод [обсудить новую работу](/картины-на-заказ/). Можно прийти с фотографией комнаты, снимком из поездки или примером из каталога. Хорошее начало — сказать, что именно нравится и что хотелось бы изменить. Готовое профессиональное задание не требуется.\n\n"
            "## А если на карточке написано SOLD?\n"
            "Значит, эта конкретная картина уже [продана](/проданные-картины/). Ее нельзя заказать как свободный оригинал, зато можно обсудить новую работу по мотивам выбранного примера. Кнопка «Заказать похожую» сохранит его в заявке. Размер, цвет, возможность исполнения и стоимость новой картины уточняются заново: SOLD — вдохновение, а не кнопка копирования.\n\n"
            "## Четыре вопроса, которые полезно задать\n"
            "Подходит ли размер? Что входит в оформление? Какова стоимость картины? Как организовать [доставку](/доставка/)? Для индивидуального заказа добавятся сюжет и срок изготовления. Если работа нужна в подарок, назовите дату получения сразу. Это помогает обсуждать весь путь — от идеи до вашей двери.\n\n"
            "## Первое сообщение ни к чему не привязывает\n"
            "Заявка нужна, чтобы начать разговор. Она не является оплатой и не бронирует картину автоматически. Можно сначала спросить о готовой работе, а потом решить, что вашему пространству нужен другой вариант. Главное — рассказать, что вы ищете. Остальные подробности обсудим без спешки."
        ),
        "body_en": (
            "## A ready work: you love this one\n"
            "A painting [from stock](/en/catalog/) suits you when you are choosing a specific work shown on the site. Check the size, technique and framing and ask any remaining questions. There is no need to invent a new subject if the right one is already here. But “available” doesn’t mean “at your door tomorrow”: how and when you receive it are agreed separately.\n\n"
            "## Made to order: you want it your way\n"
            "A different size for a narrow wall, calmer shades, a place that matters to you or a personal subject — all good reasons to [discuss a new work](/en/custom-paintings/). You can come with a photo of your room, a snapshot from a trip or an example from the catalogue. A good start is to say what exactly you like and what you would change. No professional brief is needed.\n\n"
            "## What if the card says SOLD?\n"
            "It means that particular painting has been [sold](/en/sold/). It can’t be ordered as an available original, but you can discuss a new work inspired by it. The “Order a similar one” button keeps it in your request. Size, colours, feasibility and price of the new painting are agreed afresh: SOLD is inspiration, not a copy button.\n\n"
            "## Four questions worth asking\n"
            "Does the size fit? What does the framing include? What does the painting cost? How will [delivery](/en/delivery/) work? For a custom order, add the subject and how long it will take. If the work is a gift, mention the date you need it by straight away. That helps discuss the whole journey — from the idea to your door.\n\n"
            "## A first message commits you to nothing\n"
            "A request is there to start a conversation. It isn’t a payment and doesn’t automatically reserve a painting. You can ask about a ready work first and then decide your space needs something else. The main thing is to tell us what you are looking for. We will go through the rest without hurry."
        ),
        "button_ru": "Посмотреть картины", "button_en": "Browse paintings",
        "seo_title_ru": "Готовая картина или своя идея?", "seo_title_en": "A ready painting or your own idea?",
        "seo_description_ru": "Забрать готовую работу или придумать свою? Объясняем разницу между наличием, заказом и SOLD, чтобы выбрать подходящий путь без спешки.",
        "seo_description_en": "Take a ready work or dream up your own? We explain the difference between available, made to order and SOLD so you can choose calmly.",
    },
    {
        "slug_ru": "как-заказать-картину", "slug_en": "how-to-order-a-painting",
        "cover": "mirame_article_03_kak_zakazat.jpg", "cover_alt_ru": "Светлая гостиная с морским пейзажем на стене над диваном", "cover_alt_en": "A bright living room with a seascape on the wall above the sofa",
        "title_ru": "Как заказать картину, если пока не знаете, какую хотите",
        "title_en": "How to order a painting if you don’t yet know which one you want",
        "excerpt_ru": "Не нужно приходить с дипломом искусствоведа и папкой на сорок страниц. Несколько понятных ориентиров помогут превратить «что-нибудь красивое» в предметный разговор.",
        "excerpt_en": "You don’t need an art history degree and a forty-page folder. A few simple pointers will turn “something beautiful” into a real conversation.",
        "body_ru": (
            "## Опишите чувство или сюжет\n"
            "Начните с одной фразы: [«Спокойное море для спальни»](/каталог/море/), «Яркая абстракция в гостиную», «Наш любимый город» или «Портрет в подарок». Добавьте, для кого и для какого места нужна работа. Пока этого достаточно: важнее найти направление, чем сразу решить судьбу каждого мазка.\n\n"
            "## Покажите пример — и расскажите, что в нем нравится\n"
            "У одной картины из [каталога](/каталог/) может нравиться цвет, у другой — композиция, у третьей — настроение. Напишите это рядом с изображениями. Комментарий «Хочу этот свет, но без лодки» понятнее, чем несколько картинок без пояснений. Пример служит ориентиром, а не автоматически согласованным требованием точного повторения.\n\n"
            "## Разделите «обязательно» и «можно обсудить»\n"
            "Если работа должна поместиться в определенное место, назовите допустимые размеры. Если нужен конкретный объект или важно избежать какого-то цвета, тоже скажите сразу. А там, где вы открыты предложениям, так и напишите. Это оставляет пространство для идеи, не теряя ваших пожеланий.\n\n"
            "## Сообщите размер, дату и удобный ориентир по бюджету\n"
            "Размер пока может быть приблизительным. Если картина нужна к событию, укажите день получения: создание и [доставка](/доставка/) требуют отдельного согласования. Бюджетный ориентир можно написать в комментарии, но это не обязательное поле для первого обращения. Стоимость и параметры подтвердим после обсуждения задачи.\n\n"
            "## Оставьте один контакт — этого достаточно\n"
            "Имя и удобный способ связи помогут продолжить разговор. Подробнее об индивидуальных работах — на странице [«Картины на заказ»](/картины-на-заказ/). Необязательно заполнять все дополнительные поля формы. Если начали со страницы картины, выбранный пример уже попадет в заявку. Дальше обсудим возможность выполнения и детали. Хорошая идея имеет право начинаться с простого «А можно?..»"
        ),
        "body_en": (
            "## Describe a feeling or a subject\n"
            "Start with one phrase: [“A calm sea for the bedroom”](/en/catalog/seascapes/), “A bright abstract for the living room”, “Our favourite city” or “A portrait as a gift”. Add who the work is for and where it will go. That is enough for now: finding a direction matters more than deciding the fate of every brushstroke.\n\n"
            "## Show an example — and say what you like about it\n"
            "You might like the colour of one painting from the [catalogue](/en/catalog/), the composition of another and the mood of a third. Write that next to the images. A note like “I want this light, but without the boat” is clearer than a few pictures with no explanation. An example is a reference, not an automatically agreed demand for an exact copy.\n\n"
            "## Separate “must have” from “open to discussion”\n"
            "If the work has to fit a particular spot, give the acceptable sizes. If you need a specific object or want to avoid a colour, say so right away. And where you are open to suggestions, say that too. It leaves room for the idea without losing your wishes.\n\n"
            "## Mention the size, the date and a rough budget\n"
            "The size can be approximate for now. If the painting is for an occasion, give the date you need it by: creating it and [delivering](/en/delivery/) it need to be agreed separately. You can put a budget guide in the comment, but it isn’t required for a first request. We will confirm the price and details after discussing the task.\n\n"
            "## Leave one contact — that’s enough\n"
            "A name and a convenient way to reach you are all we need to continue. You can read more about individual works on the [“Paintings to order”](/en/custom-paintings/) page. You don’t have to fill in every optional field. If you started from a painting’s page, that example will already be in the request. Then we will discuss whether it can be done and the details. A good idea is allowed to start with a simple “Could you…?”"
        ),
        "button_ru": "Обсудить мою идею", "button_en": "Discuss my idea",
        "seo_title_ru": "Как начать заказ своей картины", "seo_title_en": "How to start ordering your own painting",
        "seo_description_ru": "Хочется картину, но пока непонятно какую? Несколько ориентиров помогут рассказать об идее, выбрать примеры и начать разговор без папки документов.",
        "seo_description_en": "Want a painting but not sure which? A few pointers will help you describe your idea, pick examples and start a conversation — no paperwork needed.",
    },
    {
        "slug_ru": "на-какой-высоте-вешать-картину", "slug_en": "how-high-to-hang-a-painting",
        "title_ru": "На какой высоте вешать картину, чтобы не задирать голову",
        "title_en": "How high to hang a painting so nobody has to crane their neck",
        "excerpt_ru": "Самая частая ошибка — повесить картину слишком высоко, «чтобы было видно». Рассказываем про простой ориентир и про случаи, когда его стоит нарушить.",
        "excerpt_en": "The most common mistake is hanging a painting too high “so it can be seen”. Here is a simple guideline — and when it is worth breaking.",
        "body_ru": (
            "## Ориентир — уровень глаз\n"
            "Часто советуют располагать центр картины примерно на уровне глаз стоящего человека — это около полутора метров от пола. Это не закон, а удобная отправная точка: в такой позиции работу рассматривают без усилий, а стена не выглядит «пустой снизу».\n\n"
            "## Над диваном и комодом — ближе к мебели\n"
            "Если картина висит над мебелью, она становится частью одной композиции. Оставьте между верхом спинки или столешницы и нижним краем рамы небольшой зазор — примерно в ладонь или две. Слишком большой просвет «отрывает» картину от мебели, и она начинает жить своей отдельной жизнью под потолком.\n\n"
            "## Там, где сидят, — чуть ниже\n"
            "В столовой, спальне или кабинете на картину чаще смотрят сидя. Здесь ее можно опустить немного ниже обычного ориентира. Проверьте просто: сядьте на привычное место и посмотрите, удобно ли.\n\n"
            "## Высокие потолки не повод поднимать картину\n"
            "Даже при высоком потолке лучше ориентироваться на человека, а не на высоту стены. Если хочется заполнить большое пространство, помогает крупный формат или композиция из нескольких работ — а не подъем одной картины повыше.\n\n"
            "## Проверьте до того, как сверлить\n"
            "Вырежьте шаблон из бумаги по размеру картины, закрепите его безопасным для стены способом и поживите с ним день-другой. Отметьте на шаблоне место крепления — так вы сразу поймете, где нужен гвоздь или крючок, и сделаете одно отверстие вместо трех.\n\n"
            "Если вы выбираете картину под конкретную стену, пришлите нам ее фото с мебелью — вместе будет проще понять, какой размер впишется."
        ),
        "body_en": (
            "## The guideline: eye level\n"
            "A common tip is to place the centre of a painting at roughly the eye level of a standing person — about one and a half metres from the floor. It isn’t a law, just a handy starting point: at that height people look at the work without effort, and the wall doesn’t look “empty at the bottom”.\n\n"
            "## Above a sofa or chest of drawers — closer to the furniture\n"
            "When a painting hangs above furniture, they become one composition. Leave a small gap between the top of the sofa back or the chest and the bottom of the frame — about a hand’s width or two. Too much space “detaches” the painting, and it starts living a separate life up near the ceiling.\n\n"
            "## Where people sit — a little lower\n"
            "In a dining room, bedroom or study, people often look at paintings while sitting. There you can hang it a bit lower than the usual guideline. The test is simple: sit in your usual spot and see whether it feels comfortable.\n\n"
            "## High ceilings are no reason to hang higher\n"
            "Even with a high ceiling, it is better to follow the person rather than the height of the wall. To fill a large space, a bigger format or a group of several works helps — not raising a single painting higher.\n\n"
            "## Test before you drill\n"
            "Cut a paper template the size of the painting, fix it to the wall in a safe way and live with it for a day or two. Mark the hanging point on the template — you will see exactly where the nail or hook goes and make one hole instead of three.\n\n"
            "If you are choosing a painting for a particular wall, send us a photo of it with the furniture — it will be easier to work out together which size fits."
        ),
        "button_ru": "Подобрать размер для моей стены", "button_en": "Find the right size for my wall",
        "seo_title_ru": "На какой высоте вешать картину", "seo_title_en": "How high to hang a painting",
        "seo_description_ru": "Простой ориентир для высоты картины: уровень глаз, расстояние до дивана и комода, стены в столовой и спальне. Как проверить место до сверления.",
        "seo_description_en": "A simple guide to painting height: eye level, the gap above a sofa or chest, dining rooms and bedrooms — and how to test the spot before drilling.",
    },
    {
        "slug_ru": "размер-картины-над-диваном", "slug_en": "painting-size-above-a-sofa",
        "title_ru": "Какого размера картина нужна над диваном",
        "title_en": "What size painting do you need above a sofa?",
        "excerpt_ru": "Диван — главный кандидат на соседство с картиной. Разбираемся, как не выбрать «марку на конверте» и не закрыть полстены.",
        "excerpt_en": "The sofa is the prime candidate for living next to a painting. Here is how to avoid a “stamp on an envelope” — and not cover half the wall either.",
        "body_ru": (
            "## Начните с ширины дивана\n"
            "Популярный ориентир — картина или группа картин примерно в половину или две трети ширины дивана. Так работа выглядит связанной с мебелью: не теряется над широкой спинкой и не нависает над подлокотниками. Если диван длиной два метра, это примерно от метра до метра тридцати по ширине композиции.\n\n"
            "## Одна большая или несколько поменьше\n"
            "Одна крупная картина создает спокойный акцент и хорошо смотрится в минималистичном интерьере. Пара или тройка работ одного настроения добавляет ритм. Для нескольких картин считайте ширину всей группы вместе с промежутками — именно она должна соотноситься с диваном.\n\n"
            "## Горизонталь или вертикаль\n"
            "Над длинным диваном естественнее смотрятся горизонтальные форматы и панорамы — они повторяют линию мебели. Вертикальная картина тоже возможна, но обычно в паре с еще одной или над небольшим диваном. Квадрат — хороший компромисс, если стена не слишком широкая.\n\n"
            "## Не забудьте про высоту стены\n"
            "Между диваном и потолком должно остаться место «подышать». Если потолок невысокий, очень высокая картина может сделать стену тесной. Если стена высокая и пустая, небольшая работа рискует выглядеть одиноко — тогда выручает групповая развеска.\n\n"
            "## Примерьте до заказа\n"
            "Вырежьте из бумаги или картона прямоугольник нужного размера и закрепите над диваном. Посмотрите от входа в комнату и с дивана напротив. Это пять минут, которые помогают избежать сомнений после покупки.\n\n"
            "В нашем общем списке есть прямоугольные, квадратные и панорамные форматы. Если ни один не подходит, укажите свои ширину и высоту в заявке — обсудим."
        ),
        "body_en": (
            "## Start with the width of the sofa\n"
            "A popular guideline is a painting, or group of paintings, about half to two thirds the width of the sofa. That way the work looks connected to the furniture: it doesn’t get lost above a wide back or overhang the armrests. For a two-metre sofa, that means a composition roughly one to one point three metres wide.\n\n"
            "## One large or several smaller\n"
            "One big painting creates a calm focal point and suits a minimalist interior. Two or three works with the same mood add rhythm. For several paintings, measure the width of the whole group including the gaps — that is what should relate to the sofa.\n\n"
            "## Landscape or portrait format\n"
            "Above a long sofa, horizontal and panoramic formats look most natural — they echo the line of the furniture. A vertical painting works too, but usually in a pair or above a small sofa. A square is a good compromise if the wall isn’t very wide.\n\n"
            "## Don’t forget the height of the wall\n"
            "Leave some breathing room between the sofa and the ceiling. With a low ceiling, a very tall painting can make the wall feel cramped. With a tall, empty wall, a small work may look lonely — a group arrangement helps there.\n\n"
            "## Try it on before ordering\n"
            "Cut a rectangle of paper or card to the size you are considering and fix it above the sofa. Look at it from the doorway and from the seat opposite. Five minutes that save a lot of second-guessing later.\n\n"
            "Our standard list includes rectangular, square and panoramic formats. If none fits, enter your own width and height in the request and we will discuss it."
        ),
        "button_ru": "Обсудить размер картины", "button_en": "Discuss the painting size",
        "seo_title_ru": "Размер картины над диваном", "seo_title_en": "What size painting above a sofa",
        "seo_description_ru": "Как выбрать размер картины над диваном: соотношение с шириной мебели, одна работа или несколько, горизонталь или вертикаль и простая примерка.",
        "seo_description_en": "How to choose a painting size above a sofa: proportion to the furniture, one work or several, landscape or portrait, and a simple trial fit.",
        "categories": ["пейзажи", "море"],
    },
    {
        "slug_ru": "картина-в-подарок", "slug_en": "a-painting-as-a-gift",
        "title_ru": "Картина в подарок: как не промахнуться",
        "title_en": "A painting as a gift: how not to miss the mark",
        "excerpt_ru": "Картина — подарок личный. Поэтому немного страшно. Несколько способов угадать настроение — и один запасной вариант, если угадывать не хочется.",
        "excerpt_en": "A painting is a personal gift, which makes it a little scary. Here are a few ways to guess the mood — and a back-up plan if you’d rather not guess.",
        "body_ru": (
            "## Подсмотрите, что уже есть дома\n"
            "Интерьер многое рассказывает о человеке. Какие цвета преобладают? Есть ли уже картины, фотографии, постеры? Светлая скандинавская квартира и уютная комната с коврами и книгами просят разного. Не обязательно попадать в тон подушкам — достаточно не спорить с общим настроением.\n\n"
            "## Вспомните, что человек любит\n"
            "Море, горы, родной город, собака, цветы с дачи — сюжет, связанный с приятными воспоминаниями, почти всегда попадает в цель. Если есть общая история — поездка, место первой встречи, любимый вид из окна, — это хороший повод для картины на заказ.\n\n"
            "## Выбирайте спокойный размер\n"
            "Огромная работа — смелое решение, которое удобно принимать самому владельцу стены. Для подарка чаще выбирают средний формат: его проще найти место, и он не требует перестановки мебели. Если сомневаетесь, лучше немного меньше, чем немного больше.\n\n"
            "## Подумайте о сроках заранее\n"
            "Если работа нужна к дате, назовите ее в первом же сообщении. Время на создание картины и время на дорогу — разные части пути, и оба стоит обсудить до начала. Так подарок приедет вовремя, а не «в следующий праздник».\n\n"
            "## Запасной вариант — сертификат\n"
            "Если угадывать не хочется, подарите возможность выбрать. [Подарочный сертификат](/подарочный-сертификат/) оставляет самое приятное решение получателю — а практические детали (номинал, формат, срок действия) мы согласуем с вами заранее.\n\n"
            "И маленький совет напоследок: оставьте в заявке пару слов о человеке, которому предназначена картина. Иногда одна фраза вроде «она всегда фотографирует закаты» подсказывает больше, чем длинный список пожеланий."
        ),
        "body_en": (
            "## Take a peek at what is already at home\n"
            "An interior says a lot about a person. Which colours dominate? Are there already paintings, photos, posters? A bright Scandinavian flat and a cosy room full of rugs and books call for different things. You don’t have to match the cushions — just avoid arguing with the overall mood.\n\n"
            "## Remember what the person loves\n"
            "The sea, mountains, their home town, the dog, flowers from the garden — a subject tied to happy memories almost always hits the mark. If you share a story — a trip, the place you first met, a favourite view — that is a lovely reason for a commissioned painting.\n\n"
            "## Choose a comfortable size\n"
            "A huge work is a bold decision best made by the owner of the wall. For a gift, a medium format is the usual choice: it is easier to find it a place, and nobody has to move furniture. If in doubt, go slightly smaller rather than slightly bigger.\n\n"
            "## Think about timing early\n"
            "If you need the work by a certain date, mention it in your very first message. Creating a painting and delivering it are different parts of the journey, and both are worth discussing before starting. That way the gift arrives on time, not “in time for next year”.\n\n"
            "## The back-up plan: a certificate\n"
            "If you’d rather not guess, give the chance to choose. A [gift certificate](/en/gift-certificate/) leaves the most enjoyable decision to the recipient — and we agree the practical details (amount, format, validity) with you in advance.\n\n"
            "One last tip: add a couple of words in the request about the person the painting is for. Sometimes a single phrase like “she always photographs sunsets” tells us more than a long list of wishes."
        ),
        "button_ru": "Подобрать картину в подарок", "button_en": "Choose a painting as a gift",
        "seo_title_ru": "Картина в подарок: как выбрать", "seo_title_en": "A painting as a gift: how to choose",
        "seo_description_ru": "Как выбрать картину в подарок: интерьер и вкусы получателя, сюжет с историей, удобный размер, сроки и подарочный сертификат как запасной вариант.",
        "seo_description_en": "How to choose a painting as a gift: the recipient’s interior and taste, a subject with a story, a sensible size, timing, and a gift certificate as a back-up.",
    },
    {
        "slug_ru": "уход-за-картиной", "slug_en": "caring-for-a-painting",
        "title_ru": "Как ухаживать за картиной дома: пыль, солнце и батареи",
        "title_en": "How to care for a painting at home: dust, sun and radiators",
        "excerpt_ru": "Картина не требует ежедневного внимания, как комнатный цветок. Но несколько простых привычек помогут ей долго оставаться такой же яркой, как в первый день.",
        "excerpt_en": "A painting doesn’t need daily attention like a houseplant. But a few simple habits help it stay as bright as on its first day.",
        "body_ru": (
            "## Солнцу — «нет», свету — «да»\n"
            "Прямые солнечные лучи — главный враг красок: со временем цвета могут выцветать. Лучше выбрать стену, куда солнце не светит напрямую, или место, где оно бывает недолго. Мягкий рассеянный свет, наоборот, помогает картине раскрыться.\n\n"
            "## Подальше от батарей, плиты и ванной\n"
            "Резкие перепады температуры и влажности не полезны ни холсту, ни подрамнику. Не вешайте картину прямо над радиатором, рядом с плитой или в ванной комнате без хорошей вентиляции. Кухня возможна, но лучше на стене подальше от пара и жира.\n\n"
            "## Пыль — мягкой кистью\n"
            "Раз в несколько недель смахивайте пыль мягкой сухой кистью или чистой сухой тканью без ворса, легкими движениями. Не используйте воду, бытовую химию и влажные салфетки — они могут повредить красочный слой. Если на картине появилось серьезное загрязнение, лучше посоветоваться со специалистом, а не экспериментировать.\n\n"
            "## Масляной живописи нужно время\n"
            "Масляные краски высыхают полностью гораздо дольше, чем кажется на ощупь. Если работа написана недавно, особенно бережно относитесь к поверхности: не накрывайте ее пленкой вплотную и не ставьте лицом к другим предметам.\n\n"
            "## Переезд и хранение\n"
            "Если картину нужно временно снять, храните ее вертикально, в сухом месте, не прислоняя лицевой стороной к стене. Для перевозки защитите углы и поверхность — тем же принципом мы руководствуемся, когда [готовим картину в дорогу](/доставка/).\n\n"
            "Если сомневаетесь, подходит ли выбранное место для конкретной работы, спросите нас — подскажем с учетом техники и оформления."
        ),
        "body_en": (
            "## No to direct sun, yes to light\n"
            "Direct sunlight is the main enemy of paint: over time colours can fade. Choose a wall the sun doesn’t hit directly, or a spot where it only shines briefly. Soft, diffused light, on the other hand, helps a painting come alive.\n\n"
            "## Away from radiators, the hob and the bathroom\n"
            "Sharp changes in temperature and humidity aren’t good for the canvas or the stretcher. Don’t hang a painting right above a radiator, next to the hob or in a poorly ventilated bathroom. A kitchen is possible, but on a wall away from steam and grease.\n\n"
            "## Dust with a soft brush\n"
            "Every few weeks, gently dust the surface with a soft dry brush or a clean, dry lint-free cloth. Don’t use water, household cleaners or wet wipes — they can damage the paint layer. If the painting gets seriously dirty, ask a specialist rather than experimenting.\n\n"
            "## Oil paintings need time\n"
            "Oil paint takes much longer to dry completely than it seems to the touch. If a work was painted recently, be especially careful with the surface: don’t wrap it tightly in film or lean it face-first against other objects.\n\n"
            "## Moving and storage\n"
            "If you need to take a painting down for a while, store it upright in a dry place, not leaning face-first against a wall. For transport, protect the corners and surface — the same principle we follow when [preparing a painting for its journey](/en/delivery/).\n\n"
            "If you are unsure whether a spot suits a particular work, ask us — we will advise based on the technique and framing."
        ),
        "button_ru": "Задать вопрос о картине", "button_en": "Ask about a painting",
        "seo_title_ru": "Уход за картиной дома", "seo_title_en": "Caring for a painting at home",
        "seo_description_ru": "Простые правила ухода за картиной: где вешать, как защитить от солнца и перепадов температуры, как убирать пыль и хранить работу при переезде.",
        "seo_description_en": "Simple rules for caring for a painting: where to hang it, protecting it from sun and temperature swings, dusting, and storing it during a move.",
    },
    {
        "slug_ru": "картина-по-фотографии", "slug_en": "painting-from-a-photo",
        "title_ru": "Картина по фотографии: какое фото подойдет",
        "title_en": "A painting from a photo: which picture works best",
        "excerpt_ru": "Любимый вид из поездки, дом, где прошло детство, или питомец в смешной позе — все это может стать картиной. Главное — чтобы фотография помогала, а не мешала.",
        "excerpt_en": "A favourite view from a trip, a childhood home or a pet in a funny pose — any of these can become a painting. The key is a photo that helps rather than hinders.",
        "body_ru": (
            "## Чем четче, тем лучше\n"
            "Для работы по фотографии важны детали: как падает свет, какого цвета небо, где проходит линия горизонта. Присылайте оригинал в хорошем разрешении, а не скриншот из переписки — мессенджеры часто сжимают снимки, и мелочи теряются.\n\n"
            "## Свет решает многое\n"
            "Фото при дневном свете обычно передает цвета честнее, чем вечернее со вспышкой. Если на снимке сильные тени или пересвеченное небо, это не приговор — просто расскажите, каким вы запомнили этот момент.\n\n"
            "## Можно собрать из нескольких снимков\n"
            "На одном фото хорош пейзаж, на другом — вы сами, на третьем — любимый пес? Пришлите все и объясните, что из чего взять. Картина не обязана повторять одну фотографию: она может собрать главное из нескольких.\n\n"
            "## Что оставить, а что убрать\n"
            "Провода, случайные прохожие, мусорный бак на углу — в жизни они есть, а на картине могут и не понадобиться. Отметьте, что важно сохранить, а от чего можно отказаться. И наоборот: если хочется добавить то, чего на снимке нет, — тоже скажите.\n\n"
            "## Портреты — отдельная история\n"
            "Для портрета лучше подходит снимок, где лицо хорошо освещено и не искажено широкоугольным объективом. Если это подарок-сюрприз и позировать некому, подберите несколько фото с разных ракурсов — так проще передать узнаваемые черты.\n\n"
            "Прикрепить фото можно прямо в форме заявки (JPG, PNG или WEBP). Остальные снимки пришлем друг другу в удобном мессенджере. Возможность исполнения, размер, технику и стоимость обсудим после того, как посмотрим материалы."
        ),
        "body_en": (
            "## The sharper, the better\n"
            "When painting from a photo, details matter: how the light falls, the colour of the sky, where the horizon runs. Send the original in good resolution, not a screenshot from a chat — messengers often compress images and the small things get lost.\n\n"
            "## Light decides a lot\n"
            "A daylight photo usually shows colours more honestly than an evening shot with flash. If the picture has harsh shadows or a blown-out sky, that isn’t a deal-breaker — just tell us how you remember the moment.\n\n"
            "## You can combine several photos\n"
            "Is the landscape great in one shot, you in another and your favourite dog in a third? Send them all and explain what to take from each. A painting doesn’t have to copy one photograph: it can gather the best of several.\n\n"
            "## What to keep and what to leave out\n"
            "Wires, random passers-by, a bin on the corner — they exist in real life, but the painting may not need them. Mark what is important to keep and what can go. And the other way round: if you want to add something that isn’t in the photo, say so too.\n\n"
            "## Portraits are a story of their own\n"
            "For a portrait, a photo with a well-lit face that isn’t distorted by a wide-angle lens works best. If it is a surprise gift and there is nobody to pose, choose a few photos from different angles — that makes it easier to capture recognisable features.\n\n"
            "You can attach a photo directly in the request form (JPG, PNG or WEBP). We can exchange more pictures in a messenger. Feasibility, size, technique and price are discussed once we have looked at the materials."
        ),
        "button_ru": "Прислать фото для картины", "button_en": "Send a photo for a painting",
        "seo_title_ru": "Картина по фотографии", "seo_title_en": "A painting from your photo",
        "seo_description_ru": "Какое фото подойдет для картины на заказ: четкость, свет, несколько снимков, что убрать с кадра и как подготовить материалы для портрета.",
        "seo_description_en": "Which photo works for a commissioned painting: sharpness, light, combining shots, what to leave out and how to prepare materials for a portrait.",
        "categories": ["портрет-и-фигура", "пейзажи"],
    },
    {
        "slug_ru": "масло-акрил-акварель", "slug_en": "oil-acrylic-watercolour",
        "title_ru": "Масло, акрил или акварель — разница простыми словами",
        "title_en": "Oil, acrylic or watercolour — the difference in plain words",
        "excerpt_ru": "В карточках картин указана техника. Но что она значит для вас, кроме красивого слова? Объясняем без лекции по химии.",
        "excerpt_en": "Every painting’s page lists its technique. But what does it mean for you, beyond a nice word? An explanation without a chemistry lecture.",
        "body_ru": (
            "## Масло: глубина и бархат\n"
            "Масляная живопись — классика, знакомая по музеям. Краски сохнут медленно, поэтому цвета можно мягко смешивать прямо на холсте. Результат — глубокие оттенки, плавные переходы и характерный бархатистый блеск. Масляной работе особенно важны бережное обращение в первые месяцы и защита от прямого солнца.\n\n"
            "## Акрил: яркость и характер\n"
            "Акриловые краски сохнут быстро. Это позволяет художнику работать слоями и добиваться насыщенных, чистых цветов. Акрил хорошо держит фактуру — можно делать объемные мазки. В быту акриловые работы, как правило, неприхотливы, хотя солнце и сырость им тоже не на пользу.\n\n"
            "## Акварель: легкость и воздух\n"
            "Акварель — прозрачная краска на воде, которая пишется по бумаге. Она дает легкость, воздушность и тонкие переливы, которые сложно повторить в других техниках. Акварель обычно оформляют под стекло: бумага чувствительна к влаге и свету.\n\n"
            "## А еще бывают жидкий акрил, кофе и вино\n"
            "В каталоге встречаются и более необычные техники. Жидкий акрил дает плавные переливы и органичные формы. Картины кофе и вином — теплые монохромные работы с особым характером. Такие техники мы отмечаем в характеристиках отдельно, чтобы вы знали, что выбираете.\n\n"
            "## Как выбрать\n"
            "Лучший критерий — ваше впечатление. Техника не делает картину «лучше» или «хуже»: она меняет настроение и способ ухода. Если нравится сюжет, а техника вызывает вопросы, спросите нас — расскажем о конкретной работе, ее оформлении и о том, как она будет себя чувствовать в вашем интерьере."
        ),
        "body_en": (
            "## Oil: depth and velvet\n"
            "Oil painting is the classic you know from museums. The paint dries slowly, so colours can be blended softly right on the canvas. The result: deep tones, smooth transitions and a characteristic velvety sheen. An oil work especially needs careful handling in its first months and protection from direct sun.\n\n"
            "## Acrylic: brightness and character\n"
            "Acrylic paint dries quickly. That lets the artist work in layers and achieve rich, clean colours. Acrylic holds texture well — brushstrokes can be thick and raised. At home, acrylic works are usually easy-going, though sun and damp aren’t good for them either.\n\n"
            "## Watercolour: lightness and air\n"
            "Watercolour is a transparent, water-based paint used on paper. It gives lightness, airiness and delicate shifts of colour that are hard to repeat in other techniques. Watercolours are usually framed behind glass because paper is sensitive to moisture and light.\n\n"
            "## And there are fluid acrylic, coffee and wine\n"
            "The catalogue includes some more unusual techniques. Fluid acrylic creates smooth flows and organic shapes. Paintings in coffee and wine are warm monochrome works with a special character. We list these techniques separately in the details so you know what you are choosing.\n\n"
            "## How to choose\n"
            "The best criterion is your impression. A technique doesn’t make a painting “better” or “worse”: it changes the mood and how to care for it. If you like the subject but the technique raises questions, ask us — we will tell you about the specific work, its framing and how it will feel in your interior."
        ),
        "button_ru": "Спросить о технике", "button_en": "Ask about the technique",
        "seo_title_ru": "Масло, акрил, акварель: в чем разница", "seo_title_en": "Oil, acrylic, watercolour: the difference",
        "seo_description_ru": "Чем отличаются масло, акрил и акварель: как выглядят, как стареют и как за ними ухаживать. Плюс пара слов о жидком акриле, кофе и вине.",
        "seo_description_en": "How oil, acrylic and watercolour differ: how they look, how they age and how to care for them — plus a word on fluid acrylic, coffee and wine.",
    },
    {
        "slug_ru": "жидкий-акрил", "slug_en": "fluid-acrylic",
        "title_ru": "Жидкий акрил: почему эти картины так переливаются",
        "title_en": "Fluid acrylic: why these paintings shimmer the way they do",
        "excerpt_ru": "Разводы, как на мраморе, морские волны без кисти и узоры, которые не повторяются. Рассказываем, что такое жидкий акрил и кому он понравится.",
        "excerpt_en": "Swirls like marble, sea waves without a brush and patterns that never repeat. What fluid acrylic is — and who will love it.",
        "body_ru": (
            "## Картина, которую «ведет» краска\n"
            "В технике жидкого акрила краску разводят до текучей консистенции и выливают на холст. Дальше художник управляет потоками — наклоном, слоями, движением. Кисть здесь почти не нужна: рисунок рождается из того, как краски текут и встречаются друг с другом.\n\n"
            "## Почему каждая работа уникальна\n"
            "Даже если повторить те же цвета и движения, узор получится другим. Поэтому картины жидким акрилом часто выбирают те, кому важно владеть единственным экземпляром — без двойников.\n\n"
            "## Как это выглядит в интерьере\n"
            "Такие работы хорошо смотрятся в современных интерьерах: они дают цвет и движение, не требуя «понимания сюжета». Спокойные оттенки подойдут спальне, контрастные — гостиной или прихожей, где нужен яркий акцент.\n\n"
            "## Можно ли заказать «такую же»\n"
            "Точную копию — нет, и в этом весь смысл техники. Но можно заказать работу в той же палитре, того же настроения и нужного размера. Покажите пример, который понравился, — и обсудим, что из него взять.\n\n"
            "## Уход\n"
            "Готовая работа жидким акрилом обычно покрыта защитным слоем и не требует сложного ухода: мягкая сухая кисть от пыли и место без прямого солнца. Точнее подскажем для конкретной картины.\n\n"
            "Посмотреть примеры можно в рубрике [«Абстракция»](/каталог/абстракция/) — жидкий акрил отмечен в характеристиках работ."
        ),
        "body_en": (
            "## A painting “led” by the paint\n"
            "In fluid acrylic, paint is thinned to a flowing consistency and poured onto the canvas. The artist then guides the flows — by tilting, layering and movement. A brush is barely needed: the pattern is born from how the colours flow and meet.\n\n"
            "## Why every work is unique\n"
            "Even with the same colours and movements, the pattern comes out differently. That is why fluid acrylic paintings are often chosen by people who want the only one of its kind — no twins.\n\n"
            "## How it looks at home\n"
            "These works look great in contemporary interiors: they bring colour and movement without asking you to “get the subject”. Calm shades suit a bedroom; contrasting ones suit a living room or hallway that needs a bright accent.\n\n"
            "## Can I order “the same one”?\n"
            "An exact copy — no, and that is the whole point of the technique. But you can order a work in the same palette and mood, at the size you need. Show us the example you liked, and we will discuss what to take from it.\n\n"
            "## Care\n"
            "A finished fluid acrylic work is usually varnished and needs no special care: a soft dry brush for dust and a spot out of direct sun. We will advise more precisely for a specific painting.\n\n"
            "You will find examples in the [Abstract Art](/en/catalog/abstract-art/) category — fluid acrylic is listed in the works’ details."
        ),
        "button_ru": "Обсудить абстракцию", "button_en": "Discuss an abstract painting",
        "seo_title_ru": "Картины жидким акрилом", "seo_title_en": "Fluid acrylic paintings",
        "seo_description_ru": "Что такое жидкий акрил и почему каждая такая картина уникальна. Как работы смотрятся в интерьере, можно ли заказать похожую и как за ними ухаживать.",
        "seo_description_en": "What fluid acrylic is and why each painting is one of a kind. How these works look at home, ordering a similar one and how to care for them.",
        "categories": ["абстракция"],
    },
] + ARTICLES_MORE
