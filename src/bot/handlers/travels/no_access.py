from aiogram import Bot, Router
from aiogram.filters import or_f
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.callbacks import DeleteTravelData, EditTravelData, GetTravelData
from bot.filters import TravelCallbackAccess, TravelStateAccess
from bot.keyboards import back_to_travels_keyboard
from bot.utils.states import TravelState
from bot.utils.tg import delete_last_message

router = Router(name=__name__)


@router.callback_query(
    or_f(GetTravelData.filter(), DeleteTravelData.filter(), EditTravelData.filter()),
    ~TravelCallbackAccess(),
)
async def no_travel_access(
    callback: CallbackQuery,
    callback_data: GetTravelData | DeleteTravelData | EditTravelData,
) -> None:
    text = "Путешествие не найдено или у вас нет к нему доступа :("
    keyboard = back_to_travels_keyboard(callback_data.page)
    await callback.message.edit_text(text=text, reply_markup=keyboard)


@router.message(TravelState.editing, ~TravelStateAccess())
async def edit_travel_no_access(
    message: Message,
    bot: Bot,
    state: FSMContext,
) -> None:
    data = await state.get_data()
    page: int = data["page"]

    text = "😵‍💫 Путешествие не найдено или у вас нет к нему доступа :("
    keyboard = back_to_travels_keyboard(page)
    await message.answer(text=text, reply_markup=keyboard)

    await delete_last_message(bot, state, message)
    await state.clear()
