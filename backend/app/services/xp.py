from sqlmodel import Session

from app.models import User, XPEvent


def award(session: Session, user: User, amount: int, reason: str) -> None:
    if amount <= 0:
        return
    user.total_xp += amount
    session.add(user)
    session.add(XPEvent(user_id=user.id, amount=amount, reason=reason))


def revoke(session: Session, user: User, amount: int, reason: str) -> None:
    if amount <= 0:
        return
    removed = min(amount, user.total_xp)
    user.total_xp -= removed
    session.add(user)
    session.add(XPEvent(user_id=user.id, amount=-removed, reason=reason))
