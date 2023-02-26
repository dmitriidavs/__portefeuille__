import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

from utils import *
from includes.keyboards import *
from includes.finite_state_machines import *


# TODO: move answer msgs to db

async def cmd_start(message: types.Message) -> None:
    """/start command handler"""

    # check if user has a portfolio already
    if await user_is_active(message.from_user.id):
        msg = 'Hey, you already have a portfolio!\n' \
              'What would you like to do with it?'
        await message.answer(text=msg, reply_markup=kb_start_active)
    # if not
    else:
        msg = 'Hey, I\'m TrekB! Glad you\'re here!'
        await message.answer(text=msg)
        await asyncio.sleep(1)
        msg = 'I\'m your best friend when it comes to assets tracking. ' \
              'My data-driven insights will help you make the best out of your investment portfolio!'
        await message.answer(text=msg)
        await asyncio.sleep(1)
        msg = 'You can learn more about me by pressing /info. ' \
              'Or you can just go ahead and /join.'
        await message.answer(text=msg, reply_markup=kb_start)


async def cmd_info(message: types.Message) -> None:
    """/info command handler"""

    msg = 'Here is my repo: https://github.com/dmitriidavs/__portefeuille__/tree/main/assets_tracker_bot'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = '★ Don\'t forget to star the project ★'
    await message.answer(text=msg)


async def cmd_join(message: types.Message) -> None:
    """/join command handler"""

    msg = 'All right, let\'s set you up!'
    await message.answer(text=msg)
    await asyncio.sleep(1)
    msg = 'There are 2 ways to start configuring your portfolio. You can:\n' \
          '/manual - add assets by hand\n' \
          '/import - import crypto wallet balance'
    await message.answer(text=msg, reply_markup=kb_join)


async def cmd_manual_add(message: types.Message) -> None:
    """/manual & /add command handler: start FSMManualSetup"""

    await FSMManualSetup.asset_name.set()
    msg = 'OK. Send me the ticker symbol of an asset.\n' \
          'E.g.: BTC (Bitcoin) | MSFT (Microsoft)'
    await message.answer(text=msg)


async def add_asset_name(message: types.Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_name:
    Validating and saving name of an asset
    """

    async with state.proxy() as data:
        data["asset_name"] = message.text
    await FSMManualSetup.next()
    msg = 'Now send me the quantity.'
    await message.answer(text=msg)


async def add_asset_quantity(message: types.Message, state: FSMContext) -> None:
    """
    FSMManualSetup.asset_quantity:
    Validating and saving quantity of an asset
    """

    async with state.proxy() as data:
        data["asset_quantity"] = float(message.text)

    async with state.proxy() as data:
        msg = f'Added {data["asset_quantity"]} {data["asset_name"]} to your portfolio.'
        await message.answer(text=msg, reply_markup=kb_manual)

    await state.finish()


# async def cmd_portfolio(message: types.Message) -> None:


def register_handlers(disp: Dispatcher) -> None:
    """External handler registration for easy imports"""

    disp.register_message_handler(cmd_start, commands=['start'])
    disp.register_message_handler(cmd_info, commands=['info'])
    disp.register_message_handler(cmd_join, commands=['join'])
    disp.register_message_handler(cmd_manual_add, commands=['add'], state=None)
    disp.register_message_handler(add_asset_name, state=FSMManualSetup.asset_name)
    disp.register_message_handler(add_asset_quantity, state=FSMManualSetup.asset_quantity)
    # disp.register_message_handler(cmd_portfolio, commands=['portfolio'])