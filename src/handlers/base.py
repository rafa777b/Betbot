from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from src.database import db
from src.config import settings
from src.utils.texts import TEXTS

router = Router()

def get_main_keyboard(lang):
    keyboard = [
        [InlineKeyboardButton(text="🐯 JOGAR TIGRINHO", callback_data="game_tiger"),
         InlineKeyboardButton(text="✈️ JOGAR AVIATOR", callback_data="game_aviator")],
        [InlineKeyboardButton(text="🎯 ROLETA LUXO", callback_data="game_roleta")],
        [InlineKeyboardButton(text="💰 DEPOSITAR", callback_data="deposit"),
         InlineKeyboardButton(text="🏧 SACAR AGORA", callback_data="withdraw")],
        [InlineKeyboardButton(text="👤 MEU PERFIL", callback_data="profile"),
         InlineKeyboardButton(text="🏆 RANKING VIP", callback_data="ranking")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

@router.message(CommandStart())
async def cmd_start(message: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇧🇷 PORTUGUÊS", callback_data="set_lang_pt"),
         InlineKeyboardButton(text="🇺🇸 ENGLISH", callback_data="set_lang_en")]
    ])
    await message.answer_photo(
        photo=settings.IMG_MAIN,
        caption="<b>BEM-VINDO AO CASSINO VIP</b>\n\nEscolha seu idioma para receber seu bônus exclusivo!\n\n<i>Choose your language to receive your exclusive bonus!</i>",
        reply_markup=keyboard,
        parse_mode="HTML"
    )

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
        await callback.message.answer_photo(
            photo=settings.IMG_WIN,
            caption=f"🔥 <b>BÔNUS ATIVADO!</b>\n\n{welcome_text}",
            parse_mode="HTML"
        )
    else:
        await db.set_language(callback.from_user.id, lang)
    
    user = await db.get_user(callback.from_user.id)
    await callback.message.answer_photo(
        photo=settings.IMG_MAIN,
        caption=TEXTS[lang]['main_menu'].format(balance=user['balance']),
        reply_markup=get_main_keyboard(lang),
        parse_mode="HTML"
    )
    await callback.message.delete()

@router.callback_query(F.data == "main_menu")
async def main_menu(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=settings.IMG_MAIN,
            caption=TEXTS[lang]['main_menu'].format(balance=user['balance']),
            parse_mode="HTML"
        ),
        reply_markup=get_main_keyboard(lang)
    )
