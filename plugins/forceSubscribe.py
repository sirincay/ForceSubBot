import time
import logging
from config import Config
from pyrogram import Client, filters
from sql_helpers import forceSubscribe_sql as sql
from pyrogram.types import ChatPermissions, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, UsernameNotOccupied, ChatAdminRequired, PeerIdInvalid

logging.basicConfig(level=logging.INFO)

static_data_filter = filters.create(lambda _, __, query: query.data == "onUnMuteRequest")
@Client.on_callback_query(static_data_filter)
def _onUnMuteRequest(client, cb):
  user_id = cb.from_user.id
  chat_id = cb.message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    channel = chat_db.channel
    chat_member = client.get_chat_member(chat_id, user_id)
    if chat_member.restricted_by:
      if chat_member.restricted_by.id == (client.get_me()).id:
          try:
            client.get_chat_member(channel, user_id)
            client.unban_chat_member(chat_id, user_id)
            if cb.message.reply_to_message.from_user.id == user_id:
              cb.message.delete()
          except UserNotParticipant:
            client.answer_callback_query(cb.id, text="❕ Sözü gedən 'Kanala' qoşulun və yenidən 'Səsimi Aç' düyməsini basın.", show_alert=True)
      else:
        client.answer_callback_query(cb.id, text="❕ Başqa səbəblərə görə adminlər tərəfindən səssiz qalmısınız", show_alert=True)
    else:
      if not client.get_chat_member(chat_id, (client.get_me()).id).status == 'administrator':
        client.send_message(chat_id, f"❕ **{cb.from_user.mention} səssizləşdirə bilmirəm, çünki mən bu söhbətdə admin deyiləm məni yenidən admin olaraq əlavə edin.**\n__#Leaving this chat...__")
        client.leave_chat(chat_id)
      else:
        client.answer_callback_query(cb.id, text="❕ Xəbərdarlıq: Sərbəst danışa bilsəniz düyməni vurmayın", show_alert=True)



@Client.on_message(filters.text & ~filters.private & ~filters.edited, group=1)
def _check_member(client, message):
  chat_id = message.chat.id
  chat_db = sql.fs_settings(chat_id)
  if chat_db:
    user_id = message.from_user.id
    if not client.get_chat_member(chat_id, user_id).status in ("administrator", "creator") and not user_id in Config.SUDO_USERS:
      channel = chat_db.channel
      try:
        client.get_chat_member(channel, user_id)
      except UserNotParticipant:
        try:
          sent_message = message.reply_text(
              "**Salam** {}, **Siz Bizim Kanala Abunə Deyilsiz, Zəhmət Olmasa** [Bura Klik Edərək Kanala Qatılın](https://t.me/{}) 🔍 Və **Aşağıdakı düyməyə basaraq ⬇️ Səssizdən Çıx**".format(message.from_user.mention, channel, channel),
              disable_web_page_preview=True,
              reply_markup=InlineKeyboardMarkup(
                  [[InlineKeyboardButton("👤 Səsimi Aç 🗣", callback_data="onUnMuteRequest")]]
              )
          )
          client.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=False))
        except ChatAdminRequired:
          sent_message.edit("❕ **Mən burada admin deyiləm.**\n__İstifadəçi Qadağa icazəsi ilə məni admin edin.\n#Leaving this chat...__")
          client.leave_chat(chat_id)
      except ChatAdminRequired:
        client.send_message(chat_id, text=f"❕ **Mən adminlik hüququna malik deyiləm @{channel}**\n__Məni kanalda admin et və məni yenidən qrupa əlavə et.\n#Leaving this chat...__")
        client.leave_chat(chat_id)


@Client.on_message(filters.command(["forcesubscribe", "fsub"]) & ~filters.private)
def fsub(client, message):
  user = client.get_chat_member(message.chat.id, message.from_user.id)
  if user.status is "creator" or user.user.id in Config.SUDO_USERS:
    chat_id = message.chat.id
    if len(message.command) > 1:
      input_str = message.command[1]
      input_str = input_str.replace("@", "")
      if input_str.lower() in ("off", "no", "disable"):
        sql.disapprove(chat_id)
        message.reply_text("❌ **Məcburi Abunə Olma Uğurla Deaktiv edildi.**")
      elif input_str.lower() in ('clear'):
        sent_message = message.reply_text('**Mənim tərfimdən Səsizdə olan istifadəçinin səsini açıram:)**')
        try:
          for chat_member in client.get_chat_members(message.chat.id, filter="restricted"):
            if chat_member.restricted_by.id == (client.get_me()).id:
                client.unban_chat_member(chat_id, chat_member.user.id)
                time.sleep(1)
          sent_message.edit('✅ **Hərkəsin səsini açdım**')
        except ChatAdminRequired:
          sent_message.edit('❕ **Mən bu söhbətdə admin deyiləm**\n__Üzvləri səsdən çıxara bilmirəm, çünki bu söhbətdə admin deyiləm, qadağan istifadəçi icazəsi ilə məni admin edir.__')
      else:
        try:
          client.get_chat_member(input_str, "me")
          sql.add_channel(chat_id, input_str)
          message.reply_text(f"**Məcburi Abunə Olma Aktivdir**\n__Bütün qrup üzvləri bu [Kanala](https://t.me/{input_str}) abunə olmalıdırki bu qrupa mesaj göndərə bilsin🔥__", disable_web_page_preview=True)
        except UserNotParticipant:
          message.reply_text(f"❕ **Kanalda Admin deyiləm**\n__[Kanalda](https://t.me/{input_str}) adminlik huququ verin. Məcburi Abunə'yi aktivləşdirmək üçün məni admin olaraq əlavə edin.__", disable_web_page_preview=True)
        except (UsernameNotOccupied, PeerIdInvalid):
          message.reply_text(f"❕ **Yanlış Kanal  Adı.**")
        except Exception as err:
          message.reply_text(f"❗ **ERROR:** ```{err}```")
    else:
      if sql.fs_settings(chat_id):
        message.reply_text(f"✅ **Məcburi Abunə olmaq bu söhbətdə aktivdir.**\n__Bu [Kanal](https://t.me/{sql.fs_settings(chat_id).channel})__", disable_web_page_preview=True)
      else:
        message.reply_text("❌ **Məcburi Abunə olmaq bu söhbətdə deaktivdir.**")
  else:
      message.reply_text("❕ **Qrup sahibi tələb olunur**\n__Bunu etmək üçün qrup sahibi olmalısan.__")
