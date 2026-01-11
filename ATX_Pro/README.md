# 🤖 ATX Pro Discord Bot

**بوت Discord شامل (All-in-One) يوفر تنبيهات البث المباشر، أوامر الإدارة، وتشغيل الموسيقى.**

---

## 📋 المحتويات

- [المميزات](#-المميزات)
- [المتطلبات](#-المتطلبات)
- [التثبيت](#-التثبيت)
  - [تثبيت FFmpeg (ويندوز)](#تثبيت-ffmpeg-ويندوز)
- [الإعداد](#-الإعداد)
  - [الحصول على Discord Bot Token](#-الحصول-على-discord-bot-token)
  - [الحصول على Twitch API Keys](#-الحصول-على-twitch-api-keys)
- [التشغيل](#-التشغيل)
- [الأوامر](#-الأوامر)
- [هيكلية الملفات](#-هيكلية-الملفات)
- [استكشاف الأخطاء](#-استكشاف-الأخطاء)

---

## ✨ المميزات

- 🔴 **نظام تنبيهات البث المباشر**: يراقب Twitch و Kick ويرسل تنبيهات احترافية عند بدء البث.
- 🛡️ **أوامر إدارة السيرفر**: قفل/فتح القنوات، مسح الرسائل، طرد وحظر الأعضاء مع نظام صلاحيات صارم.
- 🎶 **تشغيل الموسيقى**: يدعم تشغيل الموسيقى من YouTube (روابط أو بحث) مع قائمة انتظار (Queue) وتحكم كامل.
- ⚙️ **هيكلية Cogs**: كود منظم ومقسم لسهولة التوسع والصيانة.
- 💾 **تخزين محلي**: يستخدم `data.json` لحفظ الإعدادات وقوائم الستريمرز.
- 🚀 **سهل الإعداد والتشغيل**.

---

## 📦 المتطلبات

- **Python 3.8+**
- **pip** (مدير حزم Python)
- **FFmpeg** (ضروري لتشغيل الموسيقى)
- **حساب Discord Developer** (للحصول على Bot Token)
- **Twitch Developer Account** (للحصول على API Keys)

---

## 🚀 التثبيت

### 1️⃣ تحميل المشروع

```bash
# استنساخ المشروع أو تحميله
git clone https://github.com/your-username/ATX_Pro.git
cd ATX_Pro
```

### 2️⃣ تثبيت المكتبات

```bash
# تثبيت المكتبات المطلوبة
pip install -r requirements.txt
```

أو يدوياً:

```bash
pip install discord.py python-dotenv requests aiohttp TwitchAPI yt-dlp PyNaCl
```

### تثبيت FFmpeg (ويندوز)

**FFmpeg** ضروري لتشغيل الموسيقى. اتبع الخطوات التالية لتثبيته على نظام Windows:

1.  **تحميل FFmpeg**: 
    - اذهب إلى الموقع الرسمي: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
    - اضغط على أيقونة Windows (عادةً ما تكون شعار ويندوز).
    - اختر رابط التحميل من [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) أو [BtbN](https://www.BtbN.com/ffmpeg-builds/). يفضل `gyan.dev`.
    - قم بتحميل ملف `ffmpeg-release-full.7z` (أو ما شابه).

2.  **فك الضغط**: 
    - استخدم برنامج مثل [7-Zip](https://www.7-zip.org/) لفك ضغط الملف الذي قمت بتحميله.
    - ستجد مجلداً باسم `ffmpeg-x.x-full_build` (حيث x.x هو رقم الإصدار).
    - انقل هذا المجلد إلى مكان يسهل الوصول إليه، مثل `C:\ffmpeg`.

3.  **إضافة FFmpeg إلى متغيرات البيئة (PATH)**:
    - ابحث في قائمة ابدأ عن `Edit the system environment variables` وافتحها.
    - اضغط على زر `Environment Variables...`.
    - في قسم `System variables`، ابحث عن المتغير `Path` وحدده، ثم اضغط `Edit...`.
    - اضغط `New` وأضف المسار إلى مجلد `bin` داخل مجلد FFmpeg. على سبيل المثال، إذا وضعت FFmpeg في `C:\ffmpeg`، فسيكون المسار هو `C:\ffmpeg\bin`.
    - اضغط `OK` في جميع النوافذ لإغلاقها.

4.  **التحقق من التثبيت**: 
    - افتح موجه الأوامر (Command Prompt) جديداً (أو PowerShell).
    - اكتب `ffmpeg -version` واضغط Enter.
    - إذا ظهرت معلومات إصدار FFmpeg، فهذا يعني أنه تم التثبيت بنجاح.

---

## ⚙️ الإعداد

### 📝 إعداد ملف البيئة (`.env`)

1.  انسخ ملف `.env.example` إلى `.env`:
    ```bash
    cp .env.example .env
    ```

2.  افتح ملف `.env` وأدخل المفاتيح الخاصة بك:
    ```env
    DISCORD_TOKEN=your_discord_bot_token_here
    BOT_PREFIX=!

    TWITCH_CLIENT_ID=your_twitch_client_id_here
    TWITCH_CLIENT_SECRET=your_twitch_client_secret_here

    CHECK_INTERVAL=60
    ```

### 🎮 الحصول على Discord Bot Token

#### الخطوات التفصيلية:

1.  **انتقل إلى Discord Developer Portal**
    - افتح الرابط: [https://discord.com/developers/applications](https://discord.com/developers/applications)
    - سجل الدخول بحساب Discord الخاص بك.

2.  **إنشاء تطبيق جديد**
    - اضغط على زر **"New Application"**.
    - أدخل اسم التطبيق: `ATX Pro`.
    - اضغط **"Create"**.

3.  **إعداد معلومات البوت**
    - من القائمة الجانبية، اختر **"Bot"**.
    - اضغط **"Add Bot"** ثم **"Yes, do it!"**.
    - يمكنك تغيير اسم البوت وإضافة صورة له.

4.  **الحصول على Token**
    - في قسم **"TOKEN"**، اضغط **"Reset Token"** ثم **"Yes, do it!"**.
    - اضغط **"Copy"** لنسخ التوكن.
    - ⚠️ **مهم جداً**: احفظ هذا التوكن في مكان آمن ولا تشاركه مع أحد!
    - الصق التوكن في ملف `.env` في حقل `DISCORD_TOKEN`.

5.  **تفعيل Privileged Gateway Intents**
    - في نفس صفحة **"Bot"**، انزل إلى قسم **"Privileged Gateway Intents"**.
    - فعّل الخيارات التالية:
        - ✅ **PRESENCE INTENT**
        - ✅ **SERVER MEMBERS INTENT**
        - ✅ **MESSAGE CONTENT INTENT**
        - ✅ **GUILD VOICE STATES** (ضروري للموسيقى)
    - اضغط **"Save Changes"**.

6.  **إنشاء رابط الدعوة**
    - من القائمة الجانبية، اختر **"OAuth2"** ثم **"URL Generator"**.
    - في **SCOPES**، اختر:
        - ✅ `bot`
        - ✅ `applications.commands`
    - في **BOT PERMISSIONS**، اختر:
        - ✅ `Administrator` (لتبسيط الصلاحيات، أو يمكنك اختيار الصلاحيات المطلوبة يدوياً: `Manage Channels`, `Kick Members`, `Ban Members`, `Send Messages`, `Embed Links`, `Attach Files`, `Read Message History`, `Mention Everyone`, `Connect`, `Speak`, `Use Voice Activity`)
    - انسخ الرابط من الأسفل **"GENERATED URL"**.

7.  **إضافة البوت للسيرفر**
    - افتح الرابط المنسوخ في المتصفح.
    - اختر السيرفر الذي تريد إضافة البوت إليه.
    - اضغط **"Authorize"**.
    - أكمل التحقق من CAPTCHA إذا ظهر.

### 🎬 الحصول على Twitch API Keys

1.  **انتقل إلى Twitch Developers**
    - افتح الرابط: [https://dev.twitch.tv/console](https://dev.twitch.tv/console)
    - سجل الدخول بحساب Twitch.

2.  **تسجيل تطبيق جديد**
    - اضغط **"Register Your Application"**.
    - أدخل المعلومات:
        - **Name**: `ATX Pro Bot`
        - **OAuth Redirect URLs**: `http://localhost`
        - **Category**: `Application Integration`
    - اضغط **"Create"**.

3.  **الحصول على Client ID و Client Secret**
    - اضغط **"Manage"** على التطبيق.
    - انسخ **Client ID** والصقه في `.env` في حقل `TWITCH_CLIENT_ID`.
    - اضغط **"New Secret"** لإنشاء Client Secret.
    - انسخ **Client Secret** والصقه في `.env` في حقل `TWITCH_CLIENT_SECRET`.
    - ⚠️ **لن تتمكن من رؤية Secret مرة أخرى!**

---

## 🎯 التشغيل

### تشغيل البوت

```bash
python main.py
```

أو:

```bash
python3 main.py
```

### التحقق من التشغيل

عند التشغيل الناجح، ستظهر رسائل في الطرفية (Terminal) تشير إلى تحميل الـ Cogs وتسجيل دخول البوت بنجاح.

---

## 📚 الأوامر

### 🔴 أوامر التنبيهات (`cogs/notifications.py`)

| الأمر | الوصف | مثال |
|------|-------|------|
| `!add_streamer <platform> <username>` | إضافة ستريمر للمراقبة | `!add_streamer twitch shroud` |
| `!set_alert_channel #channel` | تعيين قناة التنبيهات | `!set_alert_channel #stream-alerts` |

### 🛡️ أوامر الإدارة (`cogs/admin.py`)

| الأمر | الوصف | مثال |
|------|-------|------|
| `!lock` | قفل القناة الحالية | `!lock` |
| `!unlock` | فتح القناة الحالية | `!unlock` |
| `!clear <number>` | مسح عدد محدد من الرسائل | `!clear 10` |
| `!kick <member> [reason]` | طرد عضو من السيرفر | `!kick @user spamming` |
| `!ban <member> [reason]` | حظر عضو من السيرفر | `!ban @user rule-breaking` |

### 🎶 أوامر الموسيقى (`cogs/music.py`)

| الأمر | الوصف | مثال |
|------|-------|------|
| `!join` | يدخل البوت للروم الصوتي | `!join` |
| `!play <url/search>` | يشغل أغنية أو يبحث عنها | `!play despacito` / `!play https://youtu.be/dQw4w9WgXcQ` |
| `!skip` | يتخطى الأغنية الحالية | `!skip` |
| `!stop` | يوقف الموسيقى ويخرج | `!stop` |
| `!queue` | يعرض قائمة الانتظار | `!queue` |

---

## 📁 هيكلية الملفات

```
ATX_Pro/
├── main.py                 # الملف الرئيسي لتشغيل البوت وتحميل الـ Cogs
├── requirements.txt        # المكتبات المطلوبة
├── .env.example            # مثال لملف متغيرات البيئة
├── .gitignore              # ملفات Git المستبعدة
├── README.md               # هذا الملف (دليل التثبيت والتشغيل)
├── cogs/
│   ├── notifications.py    # كود تنبيهات البث المباشر (Twitch, Kick)
│   ├── admin.py            # كود أوامر الإدارة (lock, unlock, clear, kick, ban)
│   └── music.py            # كود تشغيل الموسيقى (join, play, skip, stop, queue)
├── data/
│   └── data.json           # ملف تخزين الإعدادات وقوائم الستريمرز
└── utils/
    └── data_manager.py     # مدير قراءة وكتابة ملف data.json
```

---

## 🔧 استكشاف الأخطاء

### ❌ البوت لا يستجيب للأوامر
- تأكد من تفعيل **MESSAGE CONTENT INTENT** في Discord Developer Portal.
- تحقق من أن البوت لديه صلاحيات القراءة والكتابة في القناة.
- تأكد من أن البادئة (`BOT_PREFIX`) في ملف `.env` صحيحة.

### ❌ الموسيقى لا تعمل / البوت لا يدخل الروم الصوتي
- تأكد من تثبيت **FFmpeg** بشكل صحيح وإضافته إلى متغيرات البيئة (PATH).
- تأكد من تفعيل **GUILD VOICE STATES** Intent في Discord Developer Portal.
- تأكد من أن البوت لديه صلاحيات `Connect` و `Speak` في الروم الصوتي.
- تأكد من أن مكتبة `PyNaCl` مثبتة (`pip install PyNaCl`).

### ❌ خطأ في الصلاحيات (`MissingPermissions`)
- تأكد من أن حسابك لديه الصلاحيات المطلوبة لتنفيذ الأمر (مثل `Administrator` أو `Manage Channels`).
- تأكد من أن البوت نفسه لديه الصلاحيات الكافية في السيرفر (يفضل إعطاءه صلاحية `Administrator` عند الدعوة).

### ❌ خطأ في Twitch API
- تحقق من صحة `TWITCH_CLIENT_ID` و `TWITCH_CLIENT_SECRET` في ملف `.env`.
- تأكد من أن تطبيقك نشط في Twitch Developer Console.

---

## 🤝 الدعم

إذا واجهت أي مشاكل أو لديك اقتراحات، لا تتردد في التواصل.

---

## 👨‍💻 المطور

**كبير مهندسي البرمجيات**

**الإصدار**: 1.0.0  
**تاريخ الإصدار**: 2024

---

**🌟 شكراً لاستخدامك ATX Pro Bot!**
