from flask_login import current_user

from backend.logger import logger
from backend.utils import load_schema_file


PRETTY_JURISDICTION_MAP = {
    'boone': 'Boone County',
    'saltlake': 'Salt Lake County',
    'clark': 'Clark County',
    'mclean': 'McLean County',
    'test': 'Test County',
}


def get_jurisdiction_roles():
    jurisdiction_roles = []
    for role in current_user.roles:
        if not role.name:
            logger.warning("User Role %s has no name", role)
            continue
        parts = role.name.split('_', maxsplit=1)
        if len(parts) != 2:
            logger.warning(
                "User role %s does not have two parts,"
                "cannot process into jurisdiction and event type",
                role.name
            )
            continue
        jurisdiction, event_type = parts
        try:
            schema_file = load_schema_file(event_type)
        except FileNotFoundError:
            logger.warning('User belongs to event_type %s that has no schema file', event_type)
            continue
        jurisdiction_roles.append({
            'jurisdictionSlug': jurisdiction,
            'jurisdiction': PRETTY_JURISDICTION_MAP.get(jurisdiction, jurisdiction),
            'eventTypeSlug': event_type,
            'eventType': schema_file.get('name')
        })
    return jurisdiction_roles


def can_upload_file(file_jurisdiction, file_event_type):
    return any(
        role['jurisdictionSlug'] == file_jurisdiction and role['eventTypeSlug'] == file_event_type
        for role in get_jurisdiction_roles()
    )
