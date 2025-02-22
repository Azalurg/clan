from sqlmodel import select, Session

from app.models import Resource


def get_resources(session: Session, limit: int = 20):
    resources = session.exec(select(Resource)).all()
    return resources