"""Статьи раздела «Полезное / Guides» сайта D «ХолСтори».

Статьи 1–3 — тексты приложения В (В11–В13) и метаданные Д4.
Остальные — черновики в деловом тоне. Тексты самостоятельные и не повторяют
статьи сайта «МираМе»; фактов о мастерской, сроков и цен не содержат.
"""
from .articles_more import ARTICLES_MORE

ARTICLES = [
    {
        "slug_ru": "картина-в-интерьере", "slug_en": "choosing-a-painting-for-an-interior",
        "title_ru": "Как выбрать картину для интерьера: пространство, формат и композиция",
        "title_en": "How to choose a painting for an interior: space, format and composition",
        "excerpt_ru": "Последовательная оценка места размещения и характеристик работы помогает сопоставить несколько вариантов до покупки или заказа.",
        "excerpt_en": "A step-by-step assessment of the placement and the work’s characteristics helps compare several options before buying or ordering.",
        "body_ru": (
            "## Определите задачу\n"
            "Сначала решите, какую роль будет выполнять картина: поддерживать спокойное оформление, создавать цветовой акцент или выделять определенную зону. Укажите помещение и место размещения. Фотография стены вместе с мебелью позволит оценивать выбранный сюжет в конкретном окружении.\n\n"
            "## Оцените доступный формат\n"
            "Измерьте свободную область и отметьте предметы, которые находятся рядом. Сравните вертикальную, горизонтальную и квадратную композиции. Для проверки размера можно использовать бумажный шаблон, закрепленный безопасным для отделки способом. Оцените его с обычных точек обзора, а не только непосредственно у стены. Пропорции выбираются применительно к пространству, без обязательной универсальной формулы.\n\n"
            "## Сопоставьте цвет и характер изображения\n"
            "Для согласованного решения можно опираться на существующую палитру помещения. Для акцентного — рассмотреть новый цвет или контраст. Сравнивайте не только отдельный оттенок, но и плотность композиции, распределение светлых и темных участков, общее настроение. Точное совпадение с мебелью не является обязательным условием.\n\n"
            "## Сформируйте перечень подходящих работ\n"
            "Выберите несколько изображений [в каталоге](/каталог/) и кратко зафиксируйте, что подходит в каждом: сюжет, цветовая гамма, формат или характер исполнения. Отделите параметры, которые обязательны, от предпочтений. Такой список пригодится как для выбора готовой картины, так и для обсуждения [индивидуальной работы](/картины-на-заказ/).\n\n"
            "## Проверьте предмет заказа\n"
            "Уточните статус произведения, фактические размеры, технику, основу и наличие рамы. Изображение может относиться к готовой работе, примеру для заказа или [проданному оригиналу](/проданные-картины/) — эти сценарии различаются. Стоимость картины и стоимость [доставки](/доставка/) рассматриваются отдельно. Если сведений в карточке недостаточно, запросите их до принятия решения."
        ),
        "body_en": (
            "## Define the task\n"
            "First decide what role the painting will play: supporting a calm design, creating a colour accent or marking out a particular area. Note the room and the placement. A photo of the wall with the furniture lets you assess the chosen subject in its actual surroundings.\n\n"
            "## Assess the available format\n"
            "Measure the free area and note the objects nearby. Compare vertical, horizontal and square compositions. To check a size, use a paper template fixed in a way that is safe for the wall finish. View it from the usual viewing points, not only right next to the wall. Proportions are chosen for the specific space; there is no mandatory universal formula.\n\n"
            "## Compare colour and character\n"
            "For a coordinated result you can build on the room’s existing palette. For an accent, consider a new colour or contrast. Compare not just individual shades but the density of the composition, the distribution of light and dark areas and the overall mood. An exact match with the furniture is not required.\n\n"
            "## Draw up a shortlist\n"
            "Choose several images [in the catalogue](/en/catalog/) and briefly note what works in each: subject, colour range, format or style. Separate mandatory parameters from preferences. Such a list is useful both for choosing a ready painting and for discussing a [custom work](/en/custom-paintings/).\n\n"
            "## Check what you are ordering\n"
            "Confirm the work’s status, actual dimensions, technique, support and whether it is framed. An image may show a ready work, an example for an order or a [sold original](/en/sold/) — these are different cases. The price of the painting and the cost of [delivery](/en/delivery/) are considered separately. If the page lacks information, ask for it before deciding."
        ),
        "button_ru": "Обсудить выбор картины", "button_en": "Discuss your choice",
        "seo_title_ru": "Как выбрать картину для интерьера", "seo_title_en": "How to choose a painting for an interior",
        "seo_description_ru": "Выбор картины для интерьера: оценка пространства, формата, цвета и композиции. Какие характеристики проверить до покупки или индивидуального заказа.",
        "seo_description_en": "Choosing a painting for an interior: assessing space, format, colour and composition. Which details to check before buying or commissioning.",
    },
    {
        "slug_ru": "готовая-или-на-заказ", "slug_en": "ready-work-or-commission",
        "title_ru": "Готовая картина и индивидуальный заказ: различия условий выбора",
        "title_en": "A ready painting or a commission: how the terms differ",
        "excerpt_ru": "В каталоге используются три статуса. Они определяют предмет обращения и помогают не смешивать покупку существующей работы с обсуждением новой.",
        "excerpt_en": "The catalogue uses three statuses. They define what an inquiry is about and help keep buying an existing work separate from discussing a new one.",
        "body_ru": (
            "## Покупка работы из наличия\n"
            "В этом случае обсуждается конкретная [готовая картина](/каталог/), представленная в карточке. До оформления уточняются актуальность наличия, характеристики, оформление и условия получения. Выбор готовой работы позволяет оценить существующий результат, но не означает автоматического резервирования после просмотра или отправки формы.\n\n"
            "## Заказ новой работы\n"
            "[Индивидуальное исполнение](/картины-на-заказ/) рассматривается, когда нужны определенный сюжет, другой размер или согласованная цветовая гамма. На первом этапе передаются пожелания и изображения-ориентиры. Затем уточняются возможность выполнения, техника, основа, композиция, оформление, стоимость и сроки. Предварительный пример не заменяет согласование параметров новой картины.\n\n"
            "## Использование проданной картины как ориентира\n"
            "Статус «[Продана](/проданные-картины/)» означает, что представленный оригинал не предлагается как находящийся в наличии. Действие «Заказать похожую» относится к новой работе. Возможность близкого исполнения, допустимые изменения и цена рассматриваются отдельно. Ссылка на исходный пример сохраняется в обращении, чтобы предмет обсуждения был однозначным.\n\n"
            "## Общие вопросы перед оформлением\n"
            "Для обоих сценариев следует уточнить состав заказа и характеристики работы, условия оформления и способ получения. Для индивидуального исполнения дополнительно фиксируются сюжет и срок изготовления. [Доставка](/доставка/) оплачивается отдельно; транспортная компания и маршрут согласуются с Заказчиком. Дату получения необходимо отличать от даты готовности картины.\n\n"
            "## Роль заявки на сайте\n"
            "Форма используется для передачи запроса и контактных данных. Она не является оплатой, подтверждением изготовления или автоматическим резервом. После обращения стороны уточняют условия применительно к выбранной работе. Один удобный способ связи позволяет начать этот процесс без регистрации личного кабинета."
        ),
        "body_en": (
            "## Buying a work from stock\n"
            "Here the subject is a specific [ready painting](/en/catalog/) shown on its page. Before purchase we confirm it is still available, its details, framing and how it will be received. Choosing a ready work lets you assess an existing result, but viewing it or sending the form does not reserve it automatically.\n\n"
            "## Ordering a new work\n"
            "A [custom commission](/en/custom-paintings/) is considered when you need a particular subject, a different size or an agreed colour range. First you send your requirements and reference images. Then we clarify feasibility, technique, support, composition, framing, price and timing. A preliminary example does not replace agreement on the new painting’s parameters.\n\n"
            "## Using a sold painting as a reference\n"
            "The “[Sold](/en/sold/)” status means the original shown is not offered as available. “Order a similar one” refers to a new work. Whether a close execution is possible, acceptable changes and the price are considered separately. The link to the original example is kept in the request so that the subject of discussion is unambiguous.\n\n"
            "## Questions to settle before ordering\n"
            "In both cases, clarify what the order includes and the work’s details, framing and how you will receive it. For a commission, the subject and production time are also recorded. [Delivery](/en/delivery/) is paid separately; the carrier and route are agreed with the customer. The delivery date should be distinguished from the date the painting is finished.\n\n"
            "## What the site request does\n"
            "The form is used to send your request and contact details. It is not a payment, a production confirmation or an automatic reservation. After the inquiry, both sides clarify the terms for the selected work. One convenient contact method is enough to start, with no account registration."
        ),
        "button_ru": "Выбрать работу в каталоге", "button_en": "Choose a work in the catalogue",
        "seo_title_ru": "Готовая картина или индивидуальный заказ", "seo_title_en": "A ready painting or a commission",
        "seo_description_ru": "Различия покупки готовой картины, индивидуального исполнения и заказа по мотивам проданной работы. Статусы, параметры и вопросы для согласования.",
        "seo_description_en": "How buying a ready painting differs from a commission and from ordering based on a sold work. Statuses, parameters and questions to agree.",
    },
    {
        "slug_ru": "что-подготовить-для-заказа", "slug_en": "preparing-a-painting-commission",
        "title_ru": "Какие сведения подготовить для заказа картины: сюжет, размер и срок",
        "title_en": "What information to prepare when commissioning a painting: subject, size and timing",
        "excerpt_ru": "Для предварительного обсуждения достаточно основных ориентиров. Подробные параметры уточняются после оценки задачи.",
        "excerpt_en": "Basic pointers are enough for a preliminary discussion. Detailed parameters are clarified after the task has been assessed.",
        "body_ru": (
            "## Назначение и сюжет\n"
            "Укажите, для какого пространства или события предназначена работа. Опишите сюжет в одной-двух фразах: природный вид, городской мотив, абстрактная композиция, портрет или другой вариант. Если изображение связано с конкретным местом или человеком, обозначьте это сразу.\n\n"
            "## Изображения-ориентиры\n"
            "Приложите подходящие примеры — например, из раздела [«Проданные картины»](/проданные-картины/) — и поясните назначение каждого. Один может иллюстрировать палитру, другой — композицию, третий — характер исполнения. Фотография помещения помогает оценить окружение и предполагаемый размер. Сам факт передачи примера не означает согласие на точное воспроизведение или окончательное утверждение результата.\n\n"
            "## Обязательные параметры\n"
            "Отдельно перечислите ограничения: допустимый формат, конкретные объекты, нужные оттенки и элементы, которые не должны присутствовать. Укажите, какие решения допускают обсуждение. Это позволяет отличить требования к результату от предварительных предпочтений.\n\n"
            "## Размер, сроки и бюджетный ориентир\n"
            "Если точный размер не выбран, укажите диапазон или размеры доступного места. Для [заказа](/картины-на-заказ/) к событию важна дата получения, а не только окончания работы. Изготовление и [перевозка](/доставка/) согласуются раздельно. Бюджетный ориентир можно передать в комментарии; он не заменяет согласованную стоимость и не является обязательным условием первого запроса.\n\n"
            "## Контакт и дальнейшее согласование\n"
            "Оставьте имя и один доступный способ связи. При обращении из [карточки работы](/каталог/) выбранная работа уже включается в контекст заявки. После рассмотрения уточняются возможность исполнения, параметры, оформление, стоимость и сроки. До их согласования исходные пожелания остаются предварительными."
        ),
        "body_en": (
            "## Purpose and subject\n"
            "State the space or occasion the work is for. Describe the subject in one or two sentences: a natural view, a city motif, an abstract composition, a portrait or something else. If the image relates to a particular place or person, say so from the start.\n\n"
            "## Reference images\n"
            "Attach suitable examples — for instance, from the [“Sold paintings”](/en/sold/) section — and explain the purpose of each. One may illustrate the palette, another the composition, a third the style of execution. A photo of the room helps assess the surroundings and the likely size. Sending an example does not in itself mean agreement to an exact reproduction or final approval of the result.\n\n"
            "## Mandatory parameters\n"
            "List the constraints separately: acceptable format, specific objects, required colours and elements that must not appear. Indicate which decisions are open to discussion. This distinguishes requirements for the result from preliminary preferences.\n\n"
            "## Size, timing and budget guide\n"
            "If the exact size is not chosen, give a range or the dimensions of the available space. For an [order](/en/custom-paintings/) tied to an event, the date of receipt matters, not just the completion date. Production and [shipping](/en/delivery/) are agreed separately. A budget guide can be given in the comment; it does not replace the agreed price and is not required for a first request.\n\n"
            "## Contact and further agreement\n"
            "Leave your name and one available contact method. When you write from a [work’s page](/en/catalog/), that work is already included in the request. After review we clarify feasibility, parameters, framing, price and timing. Until these are agreed, your initial wishes remain preliminary."
        ),
        "button_ru": "Направить пожелания к заказу", "button_en": "Send your order requirements",
        "seo_title_ru": "Что подготовить для заказа картины", "seo_title_en": "What to prepare for a painting commission",
        "seo_description_ru": "Какие сведения нужны для индивидуального заказа: назначение, сюжет, примеры, размеры, сроки и контакт. Порядок предварительного согласования.",
        "seo_description_en": "What information a commission needs: purpose, subject, examples, size, timing and contact. How preliminary agreement works.",
    },
    {
        "slug_ru": "расчет-размера-картины", "slug_en": "calculating-painting-size",
        "title_ru": "Расчет размера картины для стены",
        "title_en": "Calculating the right painting size for a wall",
        "excerpt_ru": "Практическая последовательность: замер свободной площади, соотношение с мебелью, проверка шаблоном. Размеры указываются для самой работы, без внешней рамы.",
        "excerpt_en": "A practical sequence: measuring the free area, relating it to furniture, checking with a template. Sizes refer to the work itself, without an outer frame.",
        "body_ru": (
            "## Замер свободной площади\n"
            "Измерьте ширину и высоту участка стены, который может занять картина, с учетом соседних предметов: окон, дверей, светильников, выключателей. Зафиксируйте минимальные отступы, которые нужно сохранить до края стены и до мебели.\n\n"
            "## Соотношение с мебелью\n"
            "Если картина размещается над мебелью, ее ширину обычно соотносят с шириной предмета под ней. Распространенный ориентир — примерно от половины до двух третей ширины дивана, кровати или комода. Для отдельно стоящей стены определяющим фактором становится расстояние, с которого картину будут рассматривать.\n\n"
            "## Расстояние обзора\n"
            "Чем дальше основная точка обзора, тем крупнее может быть формат. В узком коридоре большая работа воспринимается фрагментарно; в просторной гостиной небольшая картина может потеряться. Оцените обычные точки, откуда картину будут видеть: вход в комнату, диван, обеденный стол.\n\n"
            "## Проверка шаблоном\n"
            "Вырежьте прямоугольник из бумаги или картона нужного размера и закрепите на стене безопасным для отделки способом. Проверьте несколько вариантов, если сомневаетесь между соседними форматами. Шаблон также помогает определить высоту размещения и место крепления.\n\n"
            "## Как указать размер в заявке\n"
            "Размер фиксируется в порядке «ширина × высота» в сантиметрах, для самой работы без внешней рамы. В форме можно выбрать стандартный формат из списка с горизонтальным или вертикальным расположением либо указать собственные значения. Размер — пожелание для согласования: возможность исполнения и стоимость подтверждаются отдельно."
        ),
        "body_en": (
            "## Measure the free area\n"
            "Measure the width and height of the wall area the painting may occupy, taking into account nearby items: windows, doors, lights, switches. Note the minimum clearances you want to keep to the edge of the wall and to furniture.\n\n"
            "## Relate it to furniture\n"
            "If the painting hangs above furniture, its width is usually related to the width of the item below. A common guide is about half to two thirds of the width of the sofa, bed or chest of drawers. On a free-standing wall, the distance from which the painting will be viewed is the deciding factor.\n\n"
            "## Viewing distance\n"
            "The further away the main viewing point, the larger the format can be. In a narrow corridor a large work is seen only in parts; in a spacious living room a small painting may get lost. Consider the usual viewing points: the doorway, the sofa, the dining table.\n\n"
            "## Check with a template\n"
            "Cut a rectangle of paper or card to the required size and fix it to the wall in a way that is safe for the finish. Try several options if you are torn between adjacent formats. The template also helps determine the hanging height and fixing point.\n\n"
            "## How to state the size in a request\n"
            "Size is given as width × height in centimetres, for the work itself without an outer frame. In the form you can choose a standard format from the list in landscape or portrait orientation, or enter your own values. The size is a wish to be agreed: feasibility and price are confirmed separately."
        ),
        "button_ru": "Указать размер в заявке", "button_en": "Specify the size in a request",
        "seo_title_ru": "Как рассчитать размер картины для стены", "seo_title_en": "How to calculate painting size for a wall",
        "seo_description_ru": "Расчет размера картины: замер стены, соотношение с шириной мебели, расстояние обзора и проверка бумажным шаблоном. Как указать размер в заявке.",
        "seo_description_en": "Calculating painting size: measuring the wall, relating it to furniture width, viewing distance and checking with a paper template.",
    },
    {
        "slug_ru": "картины-для-офиса", "slug_en": "paintings-for-offices",
        "title_ru": "Картины для офиса и переговорной: критерии выбора",
        "title_en": "Paintings for offices and meeting rooms: selection criteria",
        "excerpt_ru": "В рабочем пространстве картина решает функциональные задачи: формирует впечатление, зонирует помещение, поддерживает стиль компании. Перечень критериев для выбора.",
        "excerpt_en": "In a workspace a painting has functional tasks: shaping impressions, zoning the room, supporting the company’s style. A list of selection criteria.",
        "body_ru": (
            "## Назначение помещения\n"
            "Для приемной и переговорной важны нейтральность и узнаваемость стиля: работа не должна отвлекать от разговора. В рабочих зонах уместны спокойные сюжеты, в зонах отдыха — более выразительные цветовые решения.\n\n"
            "## Сюжеты и стилистика\n"
            "Чаще всего в деловых интерьерах используют абстракцию, пейзажи, городские и архитектурные мотивы. Такие сюжеты воспринимаются нейтрально широкой аудиторией. Портреты и сюжеты с выраженной личной историей обычно оставляют для частных пространств.\n\n"
            "## Формат и количество\n"
            "Длинные стены переговорных хорошо поддерживает одна крупная горизонтальная работа или серия одного размера. Для коридоров подходит ряд одинаковых форматов с равными интервалами. Заранее определите количество мест и их размеры — это упрощает подбор и согласование.\n\n"
            "## Эксплуатационные требования\n"
            "Учитывайте освещение (прямое солнце, яркие лампы), близость кондиционеров и обогревателей, проходимость. В местах, где картину могут задеть, рекомендуется надежное крепление и защитное оформление.\n\n"
            "## Согласование и документы\n"
            "Для организаций заранее определите, кто утверждает выбор, какие сведения о работе нужны для внутреннего учета и как будет организована доставка. Эти вопросы уточняются в переписке до оформления заказа."
        ),
        "body_en": (
            "## Purpose of the room\n"
            "For a reception area or meeting room, neutrality and a recognisable style matter: the work should not distract from conversation. Calm subjects suit work areas; more expressive colours suit break areas.\n\n"
            "## Subjects and style\n"
            "Business interiors most often use abstracts, landscapes, city and architectural motifs. These subjects are perceived neutrally by a wide audience. Portraits and subjects with a strong personal story are usually kept for private spaces.\n\n"
            "## Format and quantity\n"
            "A long meeting-room wall is well supported by one large horizontal work or a series of the same size. Corridors suit a row of identical formats at equal intervals. Decide the number of places and their sizes in advance — it simplifies selection and approval.\n\n"
            "## Operating conditions\n"
            "Consider lighting (direct sun, bright lamps), proximity to air conditioners and heaters, and foot traffic. Where the painting could be knocked, secure fixing and protective framing are recommended.\n\n"
            "## Approval and paperwork\n"
            "For organisations, decide in advance who approves the choice, what information about the work is needed for internal records and how delivery will be arranged. These questions are clarified by correspondence before the order is placed."
        ),
        "button_ru": "Обсудить подбор для офиса", "button_en": "Discuss office selection",
        "seo_title_ru": "Картины для офиса и переговорной", "seo_title_en": "Paintings for offices and meeting rooms",
        "seo_description_ru": "Как выбрать картины для офиса: назначение помещения, сюжеты для делового интерьера, формат и количество, освещение и порядок согласования.",
        "seo_description_en": "How to choose paintings for an office: room purpose, subjects for business interiors, format and quantity, lighting and approval.",
        "categories": ["абстракция", "город-и-архитектура"],
    },
    {
        "slug_ru": "техники-живописи", "slug_en": "painting-techniques-compared",
        "title_ru": "Техники живописи: сравнение характеристик",
        "title_en": "Painting techniques: comparing their characteristics",
        "excerpt_ru": "Техника указывается в характеристиках каждой работы. Краткое сравнение масла, акрила, акварели и смешанных техник по внешнему виду и условиям эксплуатации.",
        "excerpt_en": "The technique is listed for every work. A brief comparison of oil, acrylic, watercolour and mixed media by appearance and care requirements.",
        "body_ru": (
            "## Масляная живопись\n"
            "Внешний вид: глубокие цвета, мягкие переходы, характерный блеск. Основа: как правило, холст на подрамнике или картон. Особенности: полное высыхание красочного слоя занимает длительное время; работа требует защиты от прямого солнца и резких перепадов температуры и влажности.\n\n"
            "## Акрил\n"
            "Внешний вид: насыщенные, чистые цвета, возможна выраженная фактура мазка. Основа: холст, картон, дерево. Особенности: краска высыхает быстро; готовые работы, как правило, устойчивы в обычных бытовых условиях.\n\n"
            "## Акварель\n"
            "Внешний вид: прозрачность, легкость, тонкие переливы. Основа: бумага. Особенности: чувствительна к влаге и свету, поэтому обычно оформляется в раму со стеклом и паспарту.\n\n"
            "## Жидкий акрил\n"
            "Внешний вид: плавные переливы и органичные формы, каждая работа неповторима. Особенности: точное повторение композиции невозможно; при заказе похожей работы согласуются палитра, размер и общий характер.\n\n"
            "## Кофе и вино\n"
            "Внешний вид: монохромные теплые изображения. Особенности: условия хранения и оформление уточняются для конкретной работы.\n\n"
            "## Как использовать сравнение\n"
            "Техника влияет на внешний вид, оформление и уход, но не определяет ценность работы сама по себе. Если для выбора важен какой-либо параметр — фактура, блеск, необходимость стекла, — уточните его в заявке по конкретной картине."
        ),
        "body_en": (
            "## Oil painting\n"
            "Appearance: deep colours, soft transitions, a characteristic sheen. Support: usually canvas on a stretcher or board. Specifics: the paint layer takes a long time to dry completely; the work needs protection from direct sun and sharp changes in temperature and humidity.\n\n"
            "## Acrylic\n"
            "Appearance: rich, clean colours; pronounced brushstroke texture is possible. Support: canvas, board, wood. Specifics: the paint dries quickly; finished works are generally stable in normal household conditions.\n\n"
            "## Watercolour\n"
            "Appearance: transparency, lightness, delicate colour shifts. Support: paper. Specifics: sensitive to moisture and light, so usually framed behind glass with a mount.\n\n"
            "## Fluid acrylic\n"
            "Appearance: smooth flows and organic shapes; every work is unique. Specifics: an exact repeat of a composition is impossible; when ordering a similar work, the palette, size and general character are agreed.\n\n"
            "## Coffee and wine\n"
            "Appearance: warm monochrome images. Specifics: storage conditions and framing are clarified for each specific work.\n\n"
            "## How to use this comparison\n"
            "Technique affects appearance, framing and care, but does not in itself determine a work’s value. If a particular parameter matters to your choice — texture, sheen, the need for glass — ask about it in a request for the specific painting."
        ),
        "button_ru": "Уточнить характеристики работы", "button_en": "Ask about a work’s details",
        "seo_title_ru": "Техники живописи: масло, акрил, акварель", "seo_title_en": "Painting techniques: oil, acrylic, watercolour",
        "seo_description_ru": "Сравнение техник живописи: масло, акрил, акварель, жидкий акрил, кофе и вино. Внешний вид, основа, оформление и условия эксплуатации.",
        "seo_description_en": "Comparing painting techniques: oil, acrylic, watercolour, fluid acrylic, coffee and wine. Appearance, support, framing and care.",
    },
    {
        "slug_ru": "основа-картины", "slug_en": "painting-supports",
        "title_ru": "Основа картины: холст, картон, бумага, дерево",
        "title_en": "Painting supports: canvas, board, paper, wood",
        "excerpt_ru": "Поле «Основа» в характеристиках показывает, на чем выполнена работа. От основы зависят вес, оформление, способ крепления и условия перевозки.",
        "excerpt_en": "The “Support” field shows what a work is painted on. The support affects weight, framing, hanging and shipping conditions.",
        "body_ru": (
            "## Холст на подрамнике\n"
            "Наиболее распространенный вариант для масла и акрила. Холст натянут на деревянную раму — подрамник. Работу можно разместить без рамы, если торцы оформлены. Для крупных форматов важно надежное крепление.\n\n"
            "## Холст на картоне\n"
            "Холст наклеен на жесткий картон. Такая основа тоньше и легче подрамника, обычно используется для небольших и средних форматов и, как правило, оформляется в раму.\n\n"
            "## Картон и бумага\n"
            "Бумага применяется для акварели, графики и ряда смешанных техник. Работы на бумаге чувствительны к влаге, свету и механическим повреждениям, поэтому их оформляют под стекло с паспарту.\n\n"
            "## Дерево и другие жесткие основы\n"
            "Жесткая основа устойчива к деформации и позволяет создавать выраженную фактуру. Такие работы тяжелее, что учитывается при выборе крепления и упаковки.\n\n"
            "## Что это значит для заказа\n"
            "Для готовой работы основа указывается в карточке. Для индивидуального заказа она согласуется вместе с техникой, размером и оформлением. При расчете доставки учитываются габариты и вес упакованной работы, которые зависят в том числе от основы."
        ),
        "body_en": (
            "## Canvas on a stretcher\n"
            "The most common option for oil and acrylic. The canvas is stretched over a wooden frame — the stretcher. The work can be hung unframed if the edges are finished. Large formats need secure fixing.\n\n"
            "## Canvas board\n"
            "Canvas glued onto rigid board. This support is thinner and lighter than a stretcher, is typically used for small and medium formats and is usually framed.\n\n"
            "## Board and paper\n"
            "Paper is used for watercolour, drawing and some mixed media. Works on paper are sensitive to moisture, light and mechanical damage, so they are framed behind glass with a mount.\n\n"
            "## Wood and other rigid supports\n"
            "A rigid support resists warping and allows pronounced texture. Such works are heavier, which is taken into account when choosing fixings and packaging.\n\n"
            "## What this means for ordering\n"
            "For a ready work, the support is shown on its page. For a commission it is agreed together with technique, size and framing. Delivery costs take into account the dimensions and weight of the packed work, which depend partly on the support."
        ),
        "button_ru": "Задать вопрос об основе", "button_en": "Ask about the support",
        "seo_title_ru": "Основа картины: холст, картон, бумага", "seo_title_en": "Painting supports: canvas, board, paper",
        "seo_description_ru": "Чем отличаются основы картин: холст на подрамнике, холст на картоне, бумага, дерево. Как основа влияет на оформление, крепление и доставку.",
        "seo_description_en": "How painting supports differ: canvas on a stretcher, canvas board, paper, wood. How the support affects framing, hanging and delivery.",
    },
    {
        "slug_ru": "оформление-картины", "slug_en": "framing-options",
        "title_ru": "Оформление картины: рама, паспарту, стекло",
        "title_en": "Framing a painting: frame, mount, glass",
        "excerpt_ru": "Оформление влияет на восприятие, защиту и размеры работы. Критерии выбора и порядок согласования.",
        "excerpt_en": "Framing affects how a work is perceived, how it is protected and its overall size. Selection criteria and how it is agreed.",
        "body_ru": (
            "## Рама\n"
            "Рама отделяет изображение от стены, защищает края и задает стилистику. Тонкий нейтральный профиль подходит большинству работ и интерьеров. Выразительные рамы подбираются под конкретное произведение. Холст на подрамнике с оформленными торцами допускает размещение без рамы.\n\n"
            "## Паспарту\n"
            "Паспарту — картонное окно вокруг изображения. Оно применяется преимущественно для работ на бумаге: отделяет изображение от стекла и визуально увеличивает формат.\n\n"
            "## Стекло\n"
            "Стекло защищает работы на бумаге от пыли и прикосновений. При выборе учитывайте блики: при ярком освещении или окне напротив может потребоваться другое размещение.\n\n"
            "## Влияние на размеры\n"
            "Размеры в характеристиках и в списке форматов указываются для самой работы, без внешней рамы. Если пространство ограничено, прибавьте ширину профиля рамы и паспарту.\n\n"
            "## Как согласуется оформление\n"
            "Для готовой работы текущее оформление указывается в поле «Оформление». Если поле не заполнено или требуется иной вариант, уточните это до принятия решения. Для индивидуального заказа оформление согласуется вместе с остальными параметрами и влияет на стоимость и условия перевозки."
        ),
        "body_en": (
            "## Frame\n"
            "A frame separates the image from the wall, protects the edges and sets the style. A thin neutral profile suits most works and interiors. Expressive frames are chosen for a specific work. A canvas on a stretcher with finished edges can be hung without a frame.\n\n"
            "## Mount\n"
            "A mount is a card window around the image. It is used mainly for works on paper: it separates the image from the glass and visually enlarges the format.\n\n"
            "## Glass\n"
            "Glass protects works on paper from dust and touch. Consider reflections: with bright lighting or a window opposite, a different placement may be needed.\n\n"
            "## Effect on dimensions\n"
            "Dimensions in the details and in the list of formats refer to the work itself, without an outer frame. If space is limited, add the width of the frame profile and mount.\n\n"
            "## How framing is agreed\n"
            "For a ready work, the current framing is shown in the “Framing” field. If the field is empty or you need a different option, clarify it before deciding. For a commission, framing is agreed with the other parameters and affects the price and shipping conditions."
        ),
        "button_ru": "Уточнить оформление", "button_en": "Ask about framing",
        "seo_title_ru": "Оформление картины: рама, паспарту, стекло", "seo_title_en": "Framing a painting: frame, mount, glass",
        "seo_description_ru": "Как выбрать оформление картины: рама, паспарту и стекло, влияние на размеры и порядок согласования для готовой работы и заказа.",
        "seo_description_en": "How to choose framing: frame, mount and glass, the effect on dimensions and how framing is agreed for ready works and commissions.",
    },
    {
        "slug_ru": "картина-корпоративный-подарок", "slug_en": "a-painting-as-a-corporate-gift",
        "title_ru": "Картина как корпоративный или официальный подарок",
        "title_en": "A painting as a corporate or formal gift",
        "excerpt_ru": "Картина подходит для подарка партнеру, руководителю или коллективу. Какие вопросы решить заранее, чтобы подарок был уместен и прибыл вовремя.",
        "excerpt_en": "A painting makes a suitable gift for a partner, a manager or a team. The questions to settle in advance so the gift is appropriate and arrives on time.",
        "body_ru": (
            "## Уместность сюжета\n"
            "Для официального подарка обычно выбирают нейтральные сюжеты: пейзажи, города, архитектуру, абстракцию. Если известны интересы получателя или есть символичное место — город компании, объект, связанный с совместным проектом, — это может стать основой для индивидуального заказа.\n\n"
            "## Формат\n"
            "Получатель не всегда может сразу разместить крупную работу. Средний формат универсальнее. Если подарок предназначен для офиса, уточните возможное место размещения у представителей компании.\n\n"
            "## Сроки\n"
            "Дату вручения указывайте при первом обращении. Для работы из наличия нужно предусмотреть время на согласование и доставку, для индивидуального заказа — дополнительно время на выполнение.\n\n"
            "## Альтернатива — сертификат\n"
            "Если выбор сюжета лучше оставить получателю, рассмотрите подарочный сертификат. Номинал, формат, срок действия и условия использования согласуются до оформления.\n\n"
            "## Организационные вопросы\n"
            "Для организаций заранее уточните, какие сведения о работе и документы понадобятся, кто принимает решение и на какой адрес организуется доставка."
        ),
        "body_en": (
            "## Appropriateness of the subject\n"
            "Formal gifts usually feature neutral subjects: landscapes, cities, architecture, abstracts. If you know the recipient’s interests or there is a symbolic place — the company’s city, a site linked to a joint project — it can become the basis for a commission.\n\n"
            "## Format\n"
            "The recipient cannot always hang a large work straight away. A medium format is more versatile. If the gift is meant for an office, check the possible placement with the company’s representatives.\n\n"
            "## Timing\n"
            "State the presentation date in your first inquiry. For a work from stock, allow time for agreement and delivery; for a commission, also allow time for production.\n\n"
            "## Alternative: a certificate\n"
            "If the choice of subject is better left to the recipient, consider a gift certificate. Amount, format, validity and terms of use are agreed before it is issued.\n\n"
            "## Organisational questions\n"
            "For organisations, clarify in advance what information about the work and what documents will be needed, who makes the decision and where delivery should go."
        ),
        "button_ru": "Обсудить подарок", "button_en": "Discuss a gift",
        "seo_title_ru": "Картина в подарок партнеру или коллеге", "seo_title_en": "A painting as a gift for a partner or colleague",
        "seo_description_ru": "Картина как корпоративный подарок: выбор сюжета и формата, сроки вручения, подарочный сертификат и организационные вопросы.",
        "seo_description_en": "A painting as a corporate gift: choosing subject and format, presentation timing, gift certificates and organisational questions.",
    },
] + ARTICLES_MORE
