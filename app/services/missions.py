from sqlmodel import Session

from app.models.missions import Mission


def create_mission(session: Session, **kwargs) -> Mission:
    mission = Mission(**kwargs)
    # session.add(mission)
    # session.commit()
    # session.refresh(mission)
    return mission
