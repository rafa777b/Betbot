import random
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from src.database import db
from src.config import settings
from src.utils.texts import TEXTS

router = Router()

async def check_win_limit(callback: CallbackQuery, user):
    lang = user['language']
    if user['balance'] >= settings.MAX_BALANCE:
        link = settings.LINK_BR_AFILIADO if lang == 'pt' else settings.LINK_EN_AFILIADO
        text = TEXTS[lang]['win_limit_reached'].format(balance=user['balance'])
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=TEXTS[lang]['btn_play_official'], url=link)]
        ])
        await callback.message.edit_text(text, reply_markup=keyboard)
        return True
    return False

@router.callback_query(F.data.startswith("game_"))
async def play_game(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    
    if await check_win_limit(callback, user):
        return

    game_type = callback.data.split("_")[1]
    win = random.random() < settings.WIN_RATE
    
    # Lógica de ganho/perda simulada
    if win:
        amount = random.uniform(10, 30)
        await db.update_balance(user['user_id'], amount)
        text_key = f"{game_type}_win"
    else:
        amount = random.uniform(5, 15)
        # Não deixa o saldo ficar negativo
        if user['balance'] - amount < 0:
            amount = user['balance']
        await db.update_balance(user['user_id'], -amount)
        text_key = f"{game_type}_loss"

    updated_user = await db.get_user(user['user_id'])
    
    # Se atingiu o limite após essa jogada
    if updated_user['balance'] >= settings.MAX_BALANCE:
        await check_win_limit(callback, updated_user)
        return

    # Mostrar resultado e botão de voltar/jogar de novo
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 Jogar Novamente" if lang == 'pt' else "🔄 Play Again", callback_data=callback.data)],
        [InlineKeyboardButton(text="🔙 Menu", callback_data="main_menu")]
    ])
    
    result_text = TEXTS[lang][text_key].format(amount=amount)
    result_text += f"\n\n💰 Saldo Atual: {updated_user['balance']:.2f} SM"
    
    await callback.message.edit_text(result_text, reply_markup=keyboard)

# Handlers para comandos diretos
@router.message(F.text.in_({"/tiger", "/tigrinho", "/aviator", "/fly", "/roleta", "/spin"}))
async def cmd_games(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user:
        return await message.answer("Use /start primeiro!")
    
    lang = user['language']
    cmd = message.text.lower()
    
    game_map = {
        "/tiger": "game_tiger", "/tigrinho": "game_tiger",
        "/aviator": "game_aviator", "/fly": "game_aviator",
        "/roleta": "game_roleta", "/spin": "game_roleta"
    }
    
    # Simular o clique no botão do jogo
    callback_data = game_map.get(cmd)
    # Criar um objeto dummy para reutilizar a lógica
    class DummyCallback:
        def __init__(self, msg, user_id):
            self.message = msg
            self.from_user = type('obj', (object,), {'id': user_id})
            self.data = callback_data
    
    await play_game(DummyCallback(message, message.from_user.id))
