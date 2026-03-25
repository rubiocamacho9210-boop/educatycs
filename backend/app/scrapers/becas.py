"""
Lista curada de becas internacionales gratuitas para hispanohablantes.

Actualizar esta lista cuando cambien las convocatorias o aparezcan
nuevas becas de calidad. Las becas incluyen programas de posgrado,
intercambio y desarrollo profesional.
"""

from app.schemas import Opportunity, OpportunityType


class BecasScraper:
    """Curated list of free international scholarships."""

    source_name = "Becas Internacionales"

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass

    def scrape(self) -> list[Opportunity]:
        return list(_BECAS)


def _b(
    title: str,
    description: str,
    provider: str,
    url: str,
    tags: list[str],
) -> Opportunity:
    return Opportunity(
        title=title,
        description=description,
        opportunity_type=OpportunityType.SCHOLARSHIP,
        provider=provider,
        source_url=url,
        location="Internacional",
        is_free=True,
        tags=["beca", "gratuito", "internacional"] + tags,
    )


_BECAS: list[Opportunity] = [
    # ── BECAS PARA POSGRADO ───────────────────────────────────────────────────
    _b(
        title="Becas DAAD — Estudios de Posgrado en Alemania",
        description=(
            "El Servicio Alemán de Intercambio Académico (DAAD) ofrece becas completas "
            "para que estudiantes latinoamericanos realicen maestrías y doctorados en "
            "universidades alemanas. Cubre matrícula, manutención, seguro médico y vuelo. "
            "Convocatoria anual para diversas áreas del conocimiento."
        ),
        provider="DAAD — Servicio Alemán de Intercambio Académico",
        url="https://www.daad.de/es/estudiar-e-investigar-en-alemania/becas/",
        tags=["alemania", "posgrado", "maestría", "doctorado", "europa"],
    ),
    _b(
        title="Becas Fulbright — Posgrado en Estados Unidos",
        description=(
            "El programa Fulbright es uno de los más prestigiosos del mundo. Ofrece becas "
            "para realizar maestrías y doctorados en universidades de Estados Unidos. "
            "Incluye matrícula, gastos de vida, seguro médico y billete aéreo. "
            "Convocatoria anual en cada país latinoamericano."
        ),
        provider="Fulbright / Comisión Binacional",
        url="https://foreign.fulbrightonline.org/",
        tags=["estados unidos", "posgrado", "maestría", "doctorado", "fulbright"],
    ),
    _b(
        title="Erasmus+ — Becas de Movilidad y Posgrado en Europa",
        description=(
            "Erasmus+ financia estancias de estudio, prácticas y maestrías Erasmus Mundus "
            "en universidades europeas. Las becas Erasmus Mundus cubren matrícula completa, "
            "manutención mensual y gastos de viaje para estudiantes de todo el mundo, "
            "incluidos latinoamericanos."
        ),
        provider="Unión Europea — Erasmus+",
        url="https://erasmus-plus.ec.europa.eu/es",
        tags=["europa", "movilidad", "maestría", "erasmus", "posgrado"],
    ),
    _b(
        title="Becas OEA — Posgrado y Desarrollo Profesional",
        description=(
            "La Organización de los Estados Americanos (OEA) ofrece becas de posgrado y "
            "desarrollo profesional para ciudadanos de sus países miembros. Cubre estudios "
            "en universidades de países miembros de la OEA y en instituciones asociadas. "
            "Incluye maestrías, especializaciones y cursos de corta duración."
        ),
        provider="Organización de los Estados Americanos (OEA)",
        url="https://www.oas.org/es/becas/",
        tags=["oea", "latinoamerica", "posgrado", "desarrollo profesional"],
    ),
    _b(
        title="Becas Chevening — Posgrado en Reino Unido",
        description=(
            "Las becas Chevening del gobierno británico financian maestrías de un año en "
            "cualquier universidad del Reino Unido. Cubren matrícula, gastos de vida, "
            "viajes y otros costos. Dirigidas a profesionales con potencial de liderazgo "
            "de más de 160 países, incluidos todos los latinoamericanos."
        ),
        provider="Gobierno del Reino Unido — Chevening",
        url="https://www.chevening.org/es/",
        tags=["reino unido", "maestría", "liderazgo", "chevening", "europa"],
    ),
    _b(
        title="Becas Australia Awards — Posgrado en Australia",
        description=(
            "Las Australia Awards son becas del gobierno australiano para que estudiantes "
            "de países en desarrollo realicen estudios de posgrado en Australia. "
            "Cubren matrícula, gastos de vida, seguro médico y viajes. "
            "Disponibles para varios países latinoamericanos."
        ),
        provider="Gobierno de Australia — Study Australia",
        url="https://www.studyaustralia.gov.au/es/plan-your-studies/scholarships",
        tags=["australia", "posgrado", "maestría", "gobierno"],
    ),
    _b(
        title="Becas CONACYT — Posgrado Nacional e Internacional (México)",
        description=(
            "El CONAHCYT (antes CONACYT) financia estudios de maestría y doctorado en "
            "México y en el extranjero para ciudadanos mexicanos. Cubre matrícula, "
            "beca mensual y seguro médico. Convocatoria continua para programas en el "
            "Padrón Nacional de Posgrado."
        ),
        provider="CONAHCYT — México",
        url="https://conahcyt.mx/becas_posgrados/becas-al-extranjero/",
        tags=["méxico", "posgrado", "doctorado", "conahcyt", "nacional"],
    ),
    _b(
        title="Becas Santander — Movilidad y Emprendimiento",
        description=(
            "El Banco Santander ofrece becas de movilidad internacional, investigación, "
            "emprendimiento y acceso a formación para estudiantes y docentes universitarios "
            "de Iberoamérica. Convocatorias periódicas con distintos montos y requisitos "
            "según el programa y país."
        ),
        provider="Banco Santander — Becas Santander",
        url="https://www.becas-santander.com/es/index.html",
        tags=["santander", "movilidad", "iberoamerica", "emprendimiento"],
    ),
    _b(
        title="Becas AMEXCID — Cooperación Internacional (México)",
        description=(
            "La Agencia Mexicana de Cooperación Internacional para el Desarrollo "
            "(AMEXCID) ofrece becas de estudio en México para extranjeros y becas para "
            "mexicanos que quieran estudiar en el extranjero mediante convenios bilaterales. "
            "Cubre matrícula y manutención según el programa."
        ),
        provider="AMEXCID — Secretaría de Relaciones Exteriores",
        url="https://www.gob.mx/amexcid",
        tags=["méxico", "cooperación", "bilateral", "posgrado"],
    ),
    _b(
        title="Becas COLFUTURO — Posgrado en el Exterior (Colombia)",
        description=(
            "COLFUTURO ofrece financiación combinada (crédito-beca) para que colombianos "
            "realicen estudios de posgrado en las mejores universidades del mundo. "
            "Al regresar a Colombia y trabajar en el país, un porcentaje del crédito "
            "se convierte en beca. Convocatoria anual."
        ),
        provider="COLFUTURO — Colombia",
        url="https://www.colfuturo.org/",
        tags=["colombia", "posgrado", "maestría", "doctorado"],
    ),
    _b(
        title="Becas PRONABEC — Posgrado e Igualdad de Oportunidades (Perú)",
        description=(
            "El Programa Nacional de Becas e Inclusión Laboral (PRONABEC) del Perú "
            "ofrece becas de posgrado, pregrado y formación técnica para peruanos de "
            "escasos recursos y alto rendimiento académico. Incluye la Beca 18 y "
            "programas de maestría en el extranjero."
        ),
        provider="PRONABEC — Perú",
        url="https://www.pronabec.gob.pe/",
        tags=["perú", "posgrado", "pregrado", "inclusión"],
    ),
    _b(
        title="Becas FUNED — Posgrado en el Extranjero (México)",
        description=(
            "La Fundación Educación Superior Internacional A.C. (FUNED) otorga becas a "
            "profesionistas mexicanos sobresalientes para realizar estudios de posgrado en "
            "las mejores universidades del mundo. El programa ofrece financiamiento parcial "
            "o total, acompañamiento durante los estudios y una red de egresados comprometida "
            "con el desarrollo de México. Convocatoria anual."
        ),
        provider="FUNED — Fundación Educación Superior Internacional",
        url="https://www.funedmx.org/",
        tags=["méxico", "posgrado", "maestría", "doctorado", "fundación"],
    ),
    _b(
        title="Becas de la Fundación Carolina — España e Iberoamérica",
        description=(
            "La Fundación Carolina ofrece becas de posgrado, doctorado y estancias de "
            "investigación para ciudadanos iberoamericanos que quieran estudiar en España, "
            "y para españoles que quieran realizar estancias en Iberoamérica. "
            "Convocatoria anual con diversas modalidades."
        ),
        provider="Fundación Carolina — España",
        url="https://www.fundacioncarolina.es/becas/",
        tags=["españa", "posgrado", "investigación", "iberoamérica"],
    ),
]
