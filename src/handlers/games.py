import random
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message
from src.database import db
from src.config import settings
from src.utils.texts import TEXTS

router = Router()

async def check_win_limit(callback_or_message, user):
    lang = user['language']
    if user['balance'] >= settings.MAX_BALANCE:
        link = settings.LINK_BR_AFILIADO if lang == 'pt' else settings.LINK_EN_AFILIADO
        text = TEXTS[lang]['win_limit_reached'].format(balance=user['balance'])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]['btn_play_official'], url=link)]
        ])
        
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.edit_text(text, reply_markup=keyboard)
        else:
            await callback_or_message.answer(text, reply_markup=keyboard)
        return True
    return False

@router.callback_query(F.data.startswith("game_"))
async def play_game_callback(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    
    if await check_win_limit(callback, user):
        return

    game_type = callback.data.split("_")[1]
    win = random.random() < settings.WIN_RATE
    
    if win:
        amount = random.uniform(10, 30)
        await db.update_balance(user['user_id'], amount)
        text_key = f"{game_type}_win"
    else:
        amount = random.uniform(5, 15)
        if user['balance'] - amount < 0:
            amount = user['balance']
        await db.update_balance(user['user_id'], -amount)
        text_key = f"{game_type}_loss"

    updated_user = await db.get_user(user['user_id'])
    
    if updated_user['balance'] >= settings.MAX_BALANCE:
        await check_win_limit(callback, updated_user)
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Jogar Novamente" if lang == 'pt' else "🔄 Play Again", callback_data=callback.data)],
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    
    result_text = TEXTS[lang][text_key].format(amount=amount)
    result_text += f"\n\n💰 Saldo Atual: {updated_user['balance']:.2f} SM"
    
    await callback.message.edit_text(result_text, reply_markup=keyboard)

@router.message(F.text.in_({"/tiger", "/tigrinho", "/aviator", "/fly", "/roleta", "/spin"}))
async def cmd_games(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        return await message.answer("Use /start primeiro!")
    
    if await check_win_limit(message, user):
        return

    lang = user['language']
    cmd = message.text.lower()
    
    game_map = {
        "/tiger": "tiger", "/tigrinho": "tiger",
        "/aviator": "aviator", "/fly": "aviator",
        "/roleta": "roleta", "/spin": "roleta"
    }
    
    game_type = game_map.get(cmd)
    win = random.random() < settings.WIN_RATE
    
    if win:
        amount = random.uniform(10, 30)
        await db.update_balance(user['user_id'], amount)
        text_key = f"{game_type}_win"
    else:
        amount = random.uniform(5, 15)
        if user['balance'] - amount < 0:
            amount = user['balance']
        await db.update_balance(user['user_id'], -amount)
        text_key = f"{game_type}_loss"

    updated_user = await db.get_user(user['user_id'])
    
    if updated_user['balance'] >= settings.MAX_BALANCE:
        await check_win_limit(message, updated_user)
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Jogar Novamente" if lang == 'pt' else "🔄 Play Again", callback_data=f"game_{game_type}")],
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    
    result_text = TEXTS[lang][text_key].format(amount=amount)
    result_text += f"\n\n💰 Saldo Atual: {updated_user['balance']:.2f} SM"
    
    await message.answer(result_text, reply_markup=keyboard)
