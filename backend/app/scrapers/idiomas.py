"""
Scraper curado de plataformas gratuitas de idiomas.

En lugar de scraping dinámico, devuelve una lista mantenida manualmente
de las mejores plataformas gratuitas de aprendizaje de idiomas para
hispanohablantes. Actualizar esta lista cuando cambien las URLs o aparezcan
nuevas plataformas de calidad.
"""

from app.schemas import Opportunity, OpportunityType


class IdiomaScraper:
    """Curated list of free language learning platforms."""

    source_name = "Idiomas Gratuitos"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def scrape(self) -> list[Opportunity]:
        return [o for o in _COURSES if o is not None]


def _c(
    title: str,
    description: str,
    provider: str,
    url: str,
    tags: list[str],
) -> Opportunity:
    return Opportunity(
        title=title,
        description=description,
        opportunity_type=OpportunityType.COURSE,
        provider=provider,
        source_url=url,
        location="Online",
        is_free=True,
        tags=["idiomas", "gratuito", "online"] + tags,
    )


_COURSES: list[Opportunity] = [
    # ── INGLÉS ────────────────────────────────────────────────────────────────
    _c(
        title="BBC Learning English — Inglés completo y gratuito",
        description=(
            "Plataforma completa del grupo BBC para aprender inglés: gramática, "
            "pronunciación, vocabulario, comprensión auditiva y noticias en inglés "
            "sencillo. Todos los recursos son 100 % gratuitos y accesibles sin registro."
        ),
        provider="BBC Learning English",
        url="https://www.bbc.co.uk/learningenglish/",
        tags=["inglés", "bbc", "listening", "gramática"],
    ),
    _c(
        title="British Council — Learn English (Gramática y habilidades)",
        description=(
            "Ejercicios interactivos de gramática, vocabulario, comprensión lectora y "
            "auditiva del British Council. Incluye lecciones para todos los niveles "
            "(A1–C1) y juegos de idiomas. Completamente gratuito."
        ),
        provider="British Council",
        url="https://learnenglish.britishcouncil.org/",
        tags=["inglés", "british council", "gramática", "certificación"],
    ),
    _c(
        title="USA Learns — Inglés gratis para adultos hispanohablantes",
        description=(
            "Curso de inglés en línea diseñado especialmente para adultos "
            "hispanohablantes. Cubre conversación, lectura, escritura y pronunciación "
            "desde nivel básico hasta intermedio. Totalmente gratuito y sin anuncios."
        ),
        provider="USA Learns",
        url="https://www.usalearns.org/",
        tags=["inglés", "hispanohablantes", "adultos", "conversación"],
    ),
    _c(
        title="VOA Learning English — Noticias y lecciones de inglés",
        description=(
            "Voice of America ofrece noticias en inglés sencillo, lecciones de "
            "vocabulario y pronunciación, y podcasts didácticos. Ideal para practicar "
            "inglés con contenido del mundo real. Totalmente gratuito."
        ),
        provider="VOA Learning English",
        url="https://learningenglish.voanews.com/",
        tags=["inglés", "voa", "noticias", "escucha"],
    ),
    _c(
        title="Cambridge English — Recursos gratuitos para aprender inglés",
        description=(
            "Materiales de práctica gratuitos de Cambridge: tests de nivel, ejercicios "
            "de gramática y vocabulario, y recursos para preparar exámenes Cambridge "
            "(B1, B2, C1). Algunos recursos requieren registro gratuito."
        ),
        provider="Cambridge English",
        url="https://www.cambridgeenglish.org/learning-english/",
        tags=["inglés", "cambridge", "examen", "certificación"],
    ),
    _c(
        title="Duolingo — Inglés para hispanohablantes",
        description=(
            "Aprende inglés de forma gratuita con el método de Duolingo: lecciones "
            "cortas, gamificación y práctica diaria. Cubre vocabulario, gramática y "
            "comprensión auditiva. La versión básica es completamente gratuita."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/enroll/en/es/English-for-Spanish-speakers",
        tags=["inglés", "duolingo", "app", "principiantes"],
    ),
    # ── FRANCÉS ───────────────────────────────────────────────────────────────
    _c(
        title="TV5Monde — Apprendre le français (Francés para hispanohablantes)",
        description=(
            "Plataforma oficial de TV5Monde con más de 800 actividades gratuitas para "
            "aprender francés en todos los niveles. Incluye ejercicios basados en "
            "programas de televisión, noticias y documentales reales."
        ),
        provider="TV5Monde",
        url="https://apprendre.tv5monde.com/",
        tags=["francés", "tv5monde", "cultura", "ejercicios"],
    ),
    _c(
        title="Duolingo — Francés para hispanohablantes",
        description=(
            "Curso gratuito de francés de Duolingo con lecciones interactivas de "
            "vocabulario, gramática y pronunciación. Desde cero hasta nivel intermedio. "
            "Disponible en web y app móvil sin costo."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/fr/es/Learn-French-Online",
        tags=["francés", "duolingo", "principiantes", "app"],
    ),
    _c(
        title="Alliance Française — Recursos digitales gratuitos de francés",
        description=(
            "La Alliance Française ofrece recursos en línea gratuitos para aprender "
            "y practicar el francés: podcasts, ejercicios de gramática, lecturas y "
            "materiales culturales. Complemento ideal para cualquier nivel."
        ),
        provider="Alliance Française",
        url="https://www.alliancefr.org/",
        tags=["francés", "alliance française", "cultura", "gramática"],
    ),
    # ── ALEMÁN ────────────────────────────────────────────────────────────────
    _c(
        title="Deutsche Welle — Aprende alemán gratis (A1 a C1)",
        description=(
            "DW ofrece cursos gratuitos de alemán para todos los niveles (A1–C1) en "
            "español. Incluye cursos en video, ejercicios interactivos, podcasts y "
            "material descargable. Es la plataforma más completa para aprender alemán "
            "de forma gratuita."
        ),
        provider="Deutsche Welle (DW)",
        url="https://learngerman.dw.com/es/overview",
        tags=["alemán", "deutsche welle", "todos los niveles", "certificación"],
    ),
    _c(
        title="Duolingo — Alemán para hispanohablantes",
        description=(
            "Aprende alemán desde cero con las lecciones cortas y gamificadas de "
            "Duolingo. Cubre vocabulario cotidiano, gramática básica y frases esenciales. "
            "Completamente gratuito."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/de/es/Learn-German-Online",
        tags=["alemán", "duolingo", "principiantes", "app"],
    ),
    _c(
        title="Goethe-Institut — Deutsch Lernen Online (Alemán nivel A1–A2)",
        description=(
            "El Goethe-Institut ofrece materiales gratuitos en línea para aprender "
            "alemán: ejercicios de gramática, vocabulario, escucha y lectura para "
            "los niveles A1 y A2. Ideal como complemento a un curso formal."
        ),
        provider="Goethe-Institut",
        url="https://www.goethe.de/en/spr/ueb.html",
        tags=["alemán", "goethe", "a1", "a2"],
    ),
    # ── ITALIANO ──────────────────────────────────────────────────────────────
    _c(
        title="Duolingo — Italiano para hispanohablantes",
        description=(
            "Curso gratuito de italiano en Duolingo con lecciones de vocabulario, "
            "gramática y pronunciación. Desde nivel cero hasta conversación cotidiana. "
            "App y versión web disponibles sin costo."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/it/es/Learn-Italian-Online",
        tags=["italiano", "duolingo", "principiantes", "app"],
    ),
    _c(
        title="RAI — Italiano facile (Italiano para extranjeros)",
        description=(
            "RAI ofrece recursos gratuitos para aprender italiano a través de sus "
            "programas de televisión y radio. Incluye ejercicios de escucha, "
            "vocabulario y comprensión de textos auténticos en italiano."
        ),
        provider="RAI",
        url="https://www.rainews.it/tgr/sardegna/lingua/italiano",
        tags=["italiano", "rai", "escucha", "cultura"],
    ),
    # ── PORTUGUÉS ─────────────────────────────────────────────────────────────
    _c(
        title="Duolingo — Portugués brasileño para hispanohablantes",
        description=(
            "Aprende portugués brasileño gratis con Duolingo: vocabulario, frases del "
            "día a día, gramática básica y pronunciación. Enfocado en el portugués de "
            "Brasil. Totalmente gratuito en web y app."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/pt/es/Learn-Portuguese-Online",
        tags=["portugués", "duolingo", "brasil", "principiantes"],
    ),
    _c(
        title="Português para Estrangeiros — USP",
        description=(
            "La Universidad de São Paulo ofrece materiales gratuitos de portugués para "
            "extranjeros: gramática, ejercicios escritos, textos auténticos y recursos "
            "de comprensión lectora. Ideal para hispanohablantes que quieren aprender "
            "portugués desde la academia."
        ),
        provider="Universidade de São Paulo (USP)",
        url="https://www.fflch.usp.br/dlcv/lport/pfol/",
        tags=["portugués", "usp", "academia", "gramática"],
    ),
    # ── JAPONÉS ───────────────────────────────────────────────────────────────
    _c(
        title="NHK World — Easy Japanese (Japonés básico gratuito)",
        description=(
            "NHK World ofrece un curso gratuito de japonés básico con lecciones en "
            "video, audio y ejercicios interactivos. Cubre los fundamentos del japonés "
            "cotidiano con explicaciones en español."
        ),
        provider="NHK World",
        url="https://www3.nhk.or.jp/nhkworld/en/learnjapanese/",
        tags=["japonés", "nhk", "principiantes", "video"],
    ),
    _c(
        title="Duolingo — Japonés para hispanohablantes",
        description=(
            "Aprende japonés gratis con Duolingo: hiragana, katakana, vocabulario "
            "básico y frases esenciales. Sistema de lecciones cortas y progresivas "
            "ideal para principiantes absolutos."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/ja/es/Learn-Japanese-Online",
        tags=["japonés", "duolingo", "principiantes", "escritura"],
    ),
    # ── CHINO ─────────────────────────────────────────────────────────────────
    _c(
        title="Duolingo — Chino Mandarín para hispanohablantes",
        description=(
            "Aprende chino mandarín desde cero con Duolingo: pinyin, vocabulario "
            "cotidiano, frases básicas y escritura de caracteres. Lecciones breves y "
            "gamificadas, completamente gratuitas."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/zh-CN/es/Learn-Chinese-Online",
        tags=["chino", "mandarín", "duolingo", "principiantes"],
    ),
    _c(
        title="Chinese for Beginners — Universidad de Pekín (Coursera)",
        description=(
            "Curso de chino mandarín para principiantes absolutos impartido por la "
            "Universidad de Pekín en Coursera. Cubre pronunciación, vocabulario básico "
            "y expresiones cotidianas. Auditar el curso es completamente gratuito."
        ),
        provider="Universidad de Pekín / Coursera",
        url="https://www.coursera.org/learn/learn-chinese",
        tags=["chino", "mandarín", "coursera", "universidad"],
    ),
    # ── COREANO ───────────────────────────────────────────────────────────────
    _c(
        title="Duolingo — Coreano para hispanohablantes",
        description=(
            "Aprende coreano con Duolingo: Hangul (el alfabeto coreano), vocabulario "
            "básico y frases del día a día. Comienza desde cero con lecciones breves "
            "y progresivas. Completamente gratuito."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/ko/es/Learn-Korean-Online",
        tags=["coreano", "duolingo", "principiantes", "hangul"],
    ),
    _c(
        title="Talk To Me In Korean — Coreano gratuito (niveles 1–3)",
        description=(
            "Talk To Me In Korean es una de las plataformas más populares para "
            "aprender coreano. Los primeros tres niveles (Hangeul + básico) son "
            "completamente gratuitos en PDF y audio, ideales para construir una base sólida."
        ),
        provider="Talk To Me In Korean",
        url="https://talktomeinkorean.com/curriculum/",
        tags=["coreano", "ttmik", "pdf", "audio"],
    ),
    # ── ÁRABE ─────────────────────────────────────────────────────────────────
    _c(
        title="Duolingo — Árabe para hispanohablantes",
        description=(
            "Aprende árabe moderno estándar con Duolingo: el alfabeto árabe, "
            "pronunciación, vocabulario básico y frases esenciales. Lecciones "
            "gamificadas totalmente gratuitas."
        ),
        provider="Duolingo",
        url="https://www.duolingo.com/course/ar/es/Learn-Arabic-Online",
        tags=["árabe", "duolingo", "principiantes", "escritura"],
    ),
]
