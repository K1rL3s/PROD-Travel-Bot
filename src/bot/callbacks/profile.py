from aiogram.filters.callback_data import CallbackData


class ProfileData(CallbackData, prefix="profile"):
    action: str


class EditProfileData(CallbackData, prefix="edit_profile"):
    field: str
