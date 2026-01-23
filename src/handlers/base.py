from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from src.database import db
from src.config import settings
from src.utils.texts import TEXTS

router = Router()

def get_main_keyboard(lang):
    keyboard = [
        [InlineKeyboardButton(text=TEXTS[lang]['btn_tiger'], callback_data="game_tiger"),
         InlineKeyboardButton(text=TEXTS[lang]['btn_aviator'], callback_data="game_aviator")],
        [InlineKeyboardButton(text=TEXTS[lang]['btn_roleta'], callback_data="game_roleta")],
        [InlineKeyboardButton(text=TEXTS[lang]['btn_deposit'], callback_data="deposit"),
         InlineKeyboardButton(text=TEXTS[lang]['btn_withdraw'], callback_data="withdraw")],
        [InlineKeyboardButton(text=TEXTS[lang]['btn_perfil'], callback_data="profile"),
         InlineKeyboardButton(text=TEXTS[lang]['btn_ranking'], callback_data="ranking")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇧🇷 PT-BR", callback_data="set_lang_pt"),
         InlineKeyboardButton(text="🇺🇸 EN", callback_data="set_lang_en")]
    ])
    await message.answer("Escolha seu idioma / Choose your language:", reply_markup=keyboard)

@router.callback_query(F.data.startswith("set_lang_"))
async def set_language(callback: CallbackQuery):
    lang = callback.data.split("_")[-1]
    user = await db.get_user(callback.from_user.id)
    
    if not user:
        await db.create_user(
            callback.from_user.id, 
            callback.from_user.full_name, 
            lang, 
            settings.INITIAL_BONUS
        )
        welcome_text = TEXTS[lang]['welcome_bonus'].format(bonus=settings.INITIAL_BONUS)
        await callback.message.answer(welcome_text)
    else:
        await db.set_language(callback.from_user.id, lang)
    
    user = await db.get_user(callback.from_user.id)
    await callback.message.edit_text(
        TEXTS[lang]['main_menu'].format(balance=user['balance']),
        reply_markup=get_main_keyboard(lang)
    )

@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    await callback.message.edit_text(
        TEXTS[lang]['main_menu'].format(balance=user['balance']),
        reply_markup=get_main_keyboard(lang)
    )
