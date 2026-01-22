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
    
    # --- ANIMAÇÕES DE SUSPENSE ---
    if game_type == "tiger":
        icons = ["🐯", "💰", "💎", "🎰", "🔥", "✨"]
        for _ in range(3):
            spin = f"{random.choice(icons)} | {random.choice(icons)} | {random.choice(icons)}"
            await callback.message.edit_text(f"🎰 GIRANDO O TIGRINHO... 🎰\n\n[ {spin} ]")
            await asyncio.sleep(0.6)
            
    elif game_type == "aviator":
        for i in range(1, 5):
            mult = 1.0 + (i * 0.3)
            await callback.message.edit_text(f"✈️ AVIATOR ✈️\n\n📈 Multiplicador: {mult:.2f}x\n🚀 O avião está subindo...")
            await asyncio.sleep(0.7)
            
    elif game_type == "roleta":
        frames = ["🔴", "⚫", "🔴", "⚫"]
        for frame in frames:
            await callback.message.edit_text(f"🎯 ROLETA GIRANDO... {frame}")
            await asyncio.sleep(0.5)

    # --- LÓGICA DE RESULTADO ---
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

    game_map = {
        "/tiger": "game_tiger", "/tigrinho": "game_tiger",
        "/aviator": "game_aviator", "/fly": "game_aviator",
        "/roleta": "game_roleta", "/spin": "game_roleta"
    }
    
    # Para comandos de texto, enviamos uma mensagem inicial e deixamos o callback_query lidar com a animação
    # Ou simplesmente simulamos o clique enviando a mensagem de "GIRANDO"
    msg = await message.answer("🎰 Iniciando jogo...")
    
    # Criar um objeto dummy de CallbackQuery para reutilizar a lógica de animação
    class DummyCallback:
        def __init__(self, msg, user_id, data):
            self.message = msg
            self.from_user = type('obj', (object,), {'id': user_id})
            self.data = data
    
    await play_game_callback(DummyCallback(msg, message.from_user.id, game_map.get(message.text.lower())))
