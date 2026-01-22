import random
import asyncio
from aiogram import Router, F
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, Message, InputMediaPhoto
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
            [InlineKeyboardButton(text="🎰 SACAR DINHEIRO REAL AGORA", url=link)],
            [InlineKeyboardButton(text="💎 ÁREA VIP (DINHEIRO REAL)", url=link)]
        ])
        
        caption = f"🔥 <b>LIMITE DE GANHO ATINGIDO!</b>\n\n{text}"
        
        if isinstance(callback_or_message, CallbackQuery):
            await callback_or_message.message.edit_media(
                media=InputMediaPhoto(media=settings.IMG_WIN, caption=caption, parse_mode="HTML"),
                reply_markup=keyboard
            )
        else:
            await callback_or_message.answer_photo(
                photo=settings.IMG_WIN, caption=caption, reply_markup=keyboard, parse_mode="HTML"
            )
        return True
    return False

@router.callback_query(F.data == "game_aviator")
async def aviator_menu(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    if await check_win_limit(callback, user): return
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚀 1.5x (Baixo Risco)", callback_data="play_aviator_1.5"),
         InlineKeyboardButton(text="🚀 2.0x (Médio Risco)", callback_data="play_aviator_2.0")],
        [InlineKeyboardButton(text="🚀 5.0x (ALTO RISCO)", callback_data="play_aviator_5.0")],
        [InlineKeyboardButton(text="🔙 MENU", callback_data="main_menu")]
    ])
    
    await callback.message.edit_media(
        media=InputMediaPhoto(media=settings.IMG_AVIATOR, caption="✈️ <b>AVIATOR VIP</b>\n\nEscolha seu multiplicador alvo para esta decolagem!\n\n<i>Quanto maior o alvo, maior o prêmio (e o risco)!</i>", parse_mode="HTML"),
        reply_markup=keyboard
    )

@router.callback_query(F.data.startswith("play_aviator_") | F.data.startswith("game_tiger") | F.data.startswith("game_roleta"))
async def play_game_callback(callback: CallbackQuery):
    user = await db.get_user(callback.from_user.id)
    lang = user['language']
    
    if await check_win_limit(callback, user): return

    data = callback.data
    game_type = "tiger" if "tiger" in data else ("roleta" if "roleta" in data else "aviator")
    
    # --- ANIMAÇÕES ---
    if game_type == "tiger":
        img = settings.IMG_TIGER
        icons = ["🐯", "💰", "💎", "🎰", "🔥", "✨"]
        for i in range(3):
            spin = f"{random.choice(icons)} | {random.choice(icons)} | {random.choice(icons)}"
            await callback.message.edit_media(
                media=InputMediaPhoto(media=img, caption=f"🐯 <b>TIGRINHO ESTÁ GIRANDO...</b>\n\n[ {spin} ]\n\n<i>Sorte vindo em {3-i}...</i>", parse_mode="HTML")
            )
            await asyncio.sleep(0.8)
            
    elif game_type == "aviator":
        target = float(data.split("_")[-1])
        img = settings.IMG_AVIATOR
        crash_point = random.uniform(1.1, 10.0)
        win = target <= crash_point
        
        limit = target if win else crash_point
        current = 1.0
        while current < limit:
            current += random.uniform(0.1, 0.4)
            if current > limit: current = limit
            await callback.message.edit_media(
                media=InputMediaPhoto(media=img, caption=f"✈️ <b>AVIATOR EM SUBIDA!</b>\n\n📈 MULTIPLICADOR: <b>{current:.2f}x</b>\n🎯 ALVO: <b>{target:.2f}x</b>\n\n🚀 <i>Subindo...</i>", parse_mode="HTML")
            )
            await asyncio.sleep(0.6)
        
        if not win:
            await callback.message.edit_media(
                media=InputMediaPhoto(media=img, caption=f"💥 <b>CRASH! O avião voou longe em {crash_point:.2f}x...</b>", parse_mode="HTML")
            )
            await asyncio.sleep(1)
            
    elif game_type == "roleta":
        img = settings.IMG_ROLETA
        frames = ["🔴 VERMELHO", "⚫ PRETO", "🔴 VERMELHO", "⚫ PRETO"]
        for frame in frames:
            await callback.message.edit_media(
                media=InputMediaPhoto(media=img, caption=f"🎯 <b>ROLETA GIRANDO...</b>\n\nGirando em: <b>{frame}</b>", parse_mode="HTML")
            )
            await asyncio.sleep(0.6)

    # --- LÓGICA DE RESULTADO ---
    if game_type != "aviator":
        win = random.random() < settings.WIN_RATE
        
    if win:
        if game_type == "aviator":
            target = float(data.split("_")[-1])
            amount = 10 * target
        else:
            amount = random.uniform(15, 45)
            
        await db.update_balance(user['user_id'], amount)
        text_key = f"{game_type}_win"
        final_img = settings.IMG_WIN
    else:
        amount = random.uniform(5, 15)
        if user['balance'] - amount < 0: amount = user['balance']
        await db.update_balance(user['user_id'], -amount)
        text_key = f"{game_type}_loss"
        final_img = settings.IMG_TIGER if game_type == "tiger" else (settings.IMG_AVIATOR if game_type == "aviator" else settings.IMG_ROLETA)

    updated_user = await db.get_user(user['user_id'])
    if updated_user['balance'] >= settings.MAX_BALANCE:
        await check_win_limit(callback, updated_user)
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔄 JOGAR NOVAMENTE", callback_data=f"game_{game_type}" if game_type != "aviator" else "game_aviator")],
        [InlineKeyboardButton(text="🔙 MENU PRINCIPAL", callback_data="main_menu")]
    ])
    
    result_text = TEXTS[lang][text_key].format(amount=amount)
    caption = f"<b>RESULTADO DA RODADA</b>\n\n{result_text}\n\n💰 <b>SALDO ATUAL: {updated_user['balance']:.2f} SM</b>"
    
    await callback.message.edit_media(
        media=InputMediaPhoto(media=final_img, caption=caption, parse_mode="HTML"),
        reply_markup=keyboard
    )

@router.message(F.text.in_({"/tiger", "/tigrinho", "/aviator", "/fly", "/roleta", "/spin"}))
async def cmd_games(message: Message):
    user = await db.get_user(message.from_user.id)
    if not user: return await message.answer("Use /start primeiro!")
    if await check_win_limit(message, user): return

    cmd = message.text.lower()
    if "aviator" in cmd or "fly" in cmd:
        class Dummy:
            def __init__(self, m, uid):
                self.message = m
                self.from_user = type('obj', (object,), {'id': uid})
        await aviator_menu(Dummy(message, message.from_user.id))
    else:
        game_map = {"/tiger": "game_tiger", "/tigrinho": "game_tiger", "/roleta": "game_roleta", "/spin": "game_roleta"}
        msg = await message.answer_photo(photo=settings.IMG_MAIN, caption="🎰 Iniciando jogo...", parse_mode="HTML")
        class Dummy:
            def __init__(self, m, uid, d):
                self.message = m
                self.from_user = type('obj', (object,), {'id': uid})
                self.data = d
        await play_game_callback(Dummy(msg, message.from_user.id, game_map.get(cmd)))
