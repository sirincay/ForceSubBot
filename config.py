import os
from pyrogram import Client
from config import Config

class Config(object):
  BOT_TOKEN = os.environ.get("BOT_TOKEN")
  APP_ID = int(os.environ.get("APP_ID"))
  API_HASH = os.environ.get("API_HASH")
  DATABASE_URL = os.environ.get("DATABASE_URL")
  SUDO_USERS = list(set(int(x) for x in ''.split()))
  SUDO_USERS.append(1108583389)
  SUDO_USERS = list(set(SUDO_USERS))

class Messages():
      HELP_MSG = [
        ".",

        "[⚠️](https://telegra.ph/file/726e9af91d30fc6ef5d52.jpg) **Məcburi Kanala Qoşulmağ:**\n\n__Qrupda Mesaj Göndərməzdən Qrup Üzvlərini Xüsusi Bir Kanala Qoşulmağa Məcbur edin.İstifadəçi kanala qatılmayıbsa onu səsizə alacam və kanala qatılmasını tələb edəcək düymə göstərəcəm__👤ℹ️",
        
        "[ℹ️](https://telegra.ph/file/a97aa2c4eafa5381ab432.jpg) **Qurulum :**\n\n__Hər şeydən əvvəl Məni Qrupda Admin edib İstifadəçiləri qadağa etmək İcazəsi verin sonra Admin Olaraq İsitfadəçiləri Məcburi Abunə Olmasını İstədiyiniz Kanalda Admin Edin🎲\n**Qeyd:** Yalnız qrup sahibi məni qura bilir__",
        
        "[⚙️](https://telegra.ph/file/ea42ec3443dc0547e56b3.jpg) **Əmrlər :**\n\n/ForceSubscribe - __Mövcud Parametirləri əldə edin🕹\n\n/ForceSubscribe no/off/disable - Məcburi Abunə Olmağı Deaktiv etmək üçün⛔️\n\n/ForceSubscribe {Kanal Tağı} - Məcburi Abonə Kanalı Bağlamaq və Qurmaq üçün\n\n/ForceSubscribe clear - Mənim tərəfimdən səsi kəsilən bütün üzvləri səssizdən çıxarar📌\n\n● **Qeyd:** Əmirləri qısa olaraq /FSub ilədə istifadə edə bilərsiniz__",
       
        "👨‍💻 **Bot @SirinCayBoss tərəfindən hazırlanmışdır📌**"
      ]

      START_MSG = "**Hey! Salam 👋 [{}](tg://user?id={})**\n\n● __Mən Qrupda Yeni Gələn Üzvləri Mesaj Yazmazdan Əvvəl__\n__İstədiyiniz Bir Kanala Qoşulmağa Məcbur Edə Bilərəm__👮🏻‍♂️\n● /help __Əmrini istifadə edərək, daha çox məlumat əldə edin__🧏🏼"
