from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from src.database import db
from src.config import settings
from src.utils.texts import TEXTS

router = Router()

@router.callback_query(F.data == "deposit")
async def deposit_handler(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    link = settings.LINK_BR_AFILIADO if lang == 'pt' else settings.LINK_EN_AFILIADO
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TEXTS[lang]['btn_play_official'], url=link)],
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    await callback.message.edit_text(TEXTS[lang]['deposit_msg'], reply_markup=keyboard)

@router.callback_query(F.data == "withdraw")
async def withdraw_handler(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    link = settings.LINK_BR_AFILIADO if lang == 'pt' else settings.LINK_EN_AFILIADO
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=TEXTS[lang]['btn_withdraw_official'], url=link)],
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    await callback.message.edit_text(TEXTS[lang]['withdraw_msg'], reply_markup=keyboard)

@router.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    
    text = TEXTS[lang]['profile'].format(
        user_id=user['user_id'],
        balance=user['balance'],
        total_won=user['total_won']
    )
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard)

@router.message(F.text == "/perfil")
async def cmd_profile(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    lang = user['language']
    text = TEXTS[lang]['profile'].format(
        user_id=user['user_id'],
        balance=user['balance'],
        total_won=user['total_won']
    )
    await message.answer(text)

@router.callback_query(F.data == "ranking")
async def ranking_handler(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    top_players = await db.get_top_players()
    
    text = f"<b>{TEXTS[lang]['ranking_title']}</b>\n\n"
    for i, player in enumerate(top_players, 1):
        username = player['username'] or "Usuário"
        text += f"{i}. {username} - {player['balance']:.2f} SM\n"
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode="HTML")

@router.message(F.text == "/ranking")
async def cmd_ranking(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return
    lang = user['language']
    top_players = await db.get_top_players()
    text = f"<b>{TEXTS[lang]['ranking_title']}</b>\n\n"
    for i, player in enumerate(top_players, 1):
        username = player['username'] or "Usuário"
        text += f"{i}. {username} - {player['balance']:.2f} SM\n"
    await message.answer(text, parse_mode="HTML")
