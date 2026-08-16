from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.settings.enums.settings_key import SettingsCode
from app.features.settings.enums.settings_type import SettingsType
from app.features.settings.models.setting import Setting


async def seed_settings(session: AsyncSession) -> None:
    settings_seed = (
        {
            "code": SettingsCode.MAINTENANCE_MODE,
            "bool_value": False,
            "description": "Maintenance Mode",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.MAINTENANCE_MESSAGE,
            "string_value": "MartelPop is currently undergoing maintenance. We'll be back shortly.",
            "description": "Maintenance Message",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.APPLICATION_URL,
            "string_value": "http://localhost/",
            "description": "Site URL",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.REPLY_TO_EMAIL,
            "string_value": "",
            "description": "Reply To Email",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.SUPPORT_EMAIL,
            "string_value": "",
            "description": "Support Email",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.CONTACT_EMAIL,
            "string_value": "",
            "description": "Contact Email",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.APPLICATION_NAME,
            "string_value": "Martel'Pop",
            "description": "Site Name",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.APPLICATION_LOGO,
            "string_value": "",
            "description": "Application Logo",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.APPLICATION_FAVICON,
            "string_value": "",
            "description": "Application Favicon",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.FOOTER_TEXT,
            "string_value": "",
            "description": "Footer Text",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.DEFAULT_PAGE_SIZE,
            "int_value": 50,
            "description": "Default Page Size",
            "value_type": SettingsType.INTEGER
        },
        {
            "code": SettingsCode.MAX_PAGE_SIZE,
            "int_value": 200,
            "description": "Max Page Size",
            "value_type": SettingsType.INTEGER
        },
        {
            "code": SettingsCode.DEFAULT_EVENT_LOCATION,
            "string_value": "Maison de Village de Martelange",
            "description": "Default Event Location",
            "value_type": SettingsType.STRING
        },
        {
            "code": SettingsCode.DEFAULT_EVENT_CAPACITY,
            "int_value": 30,
            "description": "Default Event Capacity",
            "value_type": SettingsType.INTEGER
        },
        {
            "code": SettingsCode.DEFAULT_EVENT_DURATION,
            "int_value": 240,
            "description": "Default Event Duration in minutes",
            "value_type": SettingsType.INTEGER
        },
        {
            "code": SettingsCode.REGISTRATIONS_ENABLED,
            "bool_value": True,
            "description": "Enable registrations",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.WAITLIST_ENABLED,
            "bool_value": True,
            "description": "Enable waitlist",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.OPEN_DAYS_BEFORE,
            "int_value": 14,
            "description": "Open registration X days before event start date",
            "value_type": SettingsType.INTEGER
        },
        {
            "code": SettingsCode.CLOSE_MINUTES_BEFORE,
            "int_value": 0,
            "description": "Close registration X minutes before event start date",
            "value_type": SettingsType.INTEGER
        },
        {
            "code": SettingsCode.EMAIL_ENABLE,
            "bool_value": False,
            "description": "Enable email notifications",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.EMAIL_SEND_REGISTRATION_CONFIRMATION,
            "bool_value": True,
            "description": "Send registration confirmation email",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.EMAIL_SEND_CANCELLATION_CONFIRMATION,
            "bool_value": True,
            "description": "Send cancellation confirmation email",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.EMAIL_SEND_EVENT_REMINDERS,
            "bool_value": True,
            "description": "Send event reminders",
            "value_type": SettingsType.BOOLEAN
        },
        {
            "code": SettingsCode.EMAIL_REMINDER_DAYS_BEFORE,
            "int_value": 1,
            "description": "Send event reminders X days before event start date",
            "value_type": SettingsType.INTEGER
        },
    )

    for data in settings_seed:
        exists = await session.scalar(
            select(Setting).where(Setting.code == data["code"])
        )

        if exists is None:
            session.add(Setting(**data))
        # else:
        #     exists.name = data["name"]
        #     exists.description = data["description"]
        #     exists.is_default = data["is_default"]
