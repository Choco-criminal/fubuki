#
# Copyright (C) 2024 by Moonshining1@Github, < https://github.com/Moonshining1 >.
#
# This file is part of < https://github.com/Moonshining1/ANNIE-MUSIC > project,
# and is released under the MIT License.
# Please see < https://github.com/Moonshining1/ANNIE-MUSIC/blob/master/LICENSE >
#
# All rights reserved.
#

from pyrogram import filters
from pyrogram.types import Message

from config import BANNED_USERS
from ANNIEMUSIC import app
from ANNIEMUSIC.misc import db
from ANNIEMUSIC.utils.decorators import AdminRightsCheck


@app.on_message(
    filters.command(["cplayer", "playing", "cplaying", "player"])
    & filters.group
    & ~BANNED_USERS
)
@AdminRightsCheck
async def pause_admin(cli, message: Message, _, chat_id):
    check = db.get(chat_id)
    reply_markup, thumbs, caption = (
        next(
            (
                item["mystic"].reply_markup
                for item in check
                if isinstance(item, dict)
                and "mystic" in item
                and hasattr(item["mystic"], "reply_markup")
            ),
            None,
        ),
        (
            next(
                (
                    item["mystic"].photo.thumbs
                    for item in check
                    if isinstance(item, dict)
                    and "mystic" in item
                    and hasattr(item["mystic"].photo, "thumbs")
                ),
                None,
            )
        )[0].file_id,
        next(
            (
                item["mystic"].caption
                for item in check
                if isinstance(item, dict)
                and "mystic" in item
                and hasattr(item["mystic"], "caption")
            ),
            None,
        ),
    )

    await message.reply_photo(photo=thumbs, caption=caption, reply_markup=reply_markup)
