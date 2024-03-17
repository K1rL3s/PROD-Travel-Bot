from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks.profile import EditProfileData, ProfileData
from bot.callbacks.state import InStateData
from bot.keyboards.profile import edit_profile_fields_keyboard
from bot.keyboards.universal import back_cancel_keyboard
from bot.utils.enums import Action
from bot.utils.states import ProfileState
from bot.utils.tg import delete_last_message
from core.models import User
from core.service.user import UserService, get_user_field_validator
from core.utils.enums import ProfileField

from .funcs import format_user_profile
from .phrases import error_text_by_field

router = Router(name=__name__)


@router.callback_query(ProfileData.filter(F.action == Action.EDIT))
@router.callback_query(
    InStateData.filter(F.action == Action.BACK),
    ProfileState.editing,
)
async def edit_profile(callback: CallbackQuery, user: User) -> None:
    text = "Что вы хотите изменить?\n\n" + format_user_profile(user)
    keyboard = edit_profile_fields_keyboard
    await callback.message.edit_text(text=text, reply_markup=keyboard)


for field in ProfileField.values():

    @router.callback_query(EditProfileData.filter(F.field == field))
    async def edit_profile_field(
        callback: CallbackQuery,
        callback_data: EditProfileData,
        state: FSMContext,
        user: User,
    ) -> None:
        text = "Введите новое значение.\nТекущее: " + str(
            getattr(user, callback_data.field)
        )
        await callback.message.edit_text(text=text, reply_markup=back_cancel_keyboard)
        await state.set_data(
            {
                "last_id": callback.message.message_id,
                "field": callback_data.field,
            },
        )
        await state.set_state(ProfileState.editing)


@router.message(F.text, ProfileState.editing)
async def edit_profile_field_enter(
    message: Message,
    bot: Bot,
    state: FSMContext,
    user: User,
    user_service: UserService,
) -> None:
    data = await state.get_data()
    edit_field: str = data["field"]
    validator = get_user_field_validator(edit_field)
    error_text = error_text_by_field[edit_field]

    if not validator(message.text):
        await message.reply(text=error_text, reply_markup=back_cancel_keyboard)
        await delete_last_message(bot, state, message)
        return

    setattr(user, edit_field, message.text)
    await user_service.update(user.id, user)
    await message.answer(
        text=format_user_profile(user),
        reply_markup=edit_profile_fields_keyboard,
    )
    await delete_last_message(bot, state, message)
