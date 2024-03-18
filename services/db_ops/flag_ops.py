from models.db.models import db
from models.db.models import Flag


def add_new_flag(flag_value: bool):
    new_flag = Flag(allow_connections=flag_value)
    db.add(new_flag)
    db.commit()


def create_or_update_flag(flag_value: bool):
    # Fetch the first row from the flags table
    first_flag = db.query(Flag).first()

    if first_flag:
        # If a flag exists, update it
        first_flag.allow_connections = flag_value  # type: ignore
        # Update the attribute with the correct data type
        db.commit()
        return {"message": "Flag updated successfully"}
    else:
        # If no flag exists, insert a new one
        add_new_flag(flag_value=flag_value)


def read_flag() -> bool:
    # Fetch the first row from the flags table
    first_flag = db.query(Flag).first()
    if not first_flag:
        add_new_flag(True)
        return db.query(Flag).first().allow_connections  # type: ignore
    else:
        return first_flag.allow_connections  # type: ignore
