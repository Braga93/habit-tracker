from dataclasses import dataclass


@dataclass(frozen=True)
class Badge:
    code: str
    name: str
    description: str
    icon: str
    kind: str
    threshold: int
    xp_bonus: int


BADGES: tuple[Badge, ...] = (
    Badge("arquiteto", "Arquiteto", "Crie o seu primeiro hábito", "🧱", "habits", 1, 25),
    Badge("primeiro_passo", "Primeiro Passo", "Faça o seu primeiro check-in", "👣", "checkins", 1, 25),
    Badge("aquecendo", "Aquecendo", "Mantenha 3 dias seguidos", "🔥", "streak", 3, 50),
    Badge("semana_de_ferro", "Semana de Ferro", "Mantenha 7 dias seguidos", "⚡", "streak", 7, 100),
    Badge("inabalavel", "Inabalável", "Mantenha 30 dias seguidos", "🌟", "streak", 30, 300),
    Badge("centenario", "Centenário", "Complete 100 check-ins", "💯", "checkins", 100, 200),
    Badge("veterano", "Veterano", "Alcance o nível 5", "🎖️", "level", 5, 150),
    Badge("mestre", "Mestre dos Hábitos", "Complete 500 check-ins", "🏆", "checkins", 500, 500),
)

BADGES_BY_CODE = {badge.code: badge for badge in BADGES}


@dataclass(frozen=True)
class BadgeStats:
    habits_created: int
    checkins: int
    streak: int
    level: int


def is_unlocked(badge: Badge, stats: BadgeStats) -> bool:
    value = {
        "habits": stats.habits_created,
        "checkins": stats.checkins,
        "streak": stats.streak,
        "level": stats.level,
    }[badge.kind]
    return value >= badge.threshold


def newly_unlocked(stats: BadgeStats, earned: set[str]) -> list[Badge]:
    return [badge for badge in BADGES if badge.code not in earned and is_unlocked(badge, stats)]
