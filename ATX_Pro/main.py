import discord
from discord.ext import commands
import os
import asyncio
from dotenv import load_dotenv
import logging

# إعداد التسجيل (Logging) لمراقبة أداء البوت
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s:%(levelname)s:%(name)s: %(message)s'
)
logger = logging.getLogger('ATX_Bot')

# تحميل متغيرات البيئة
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
PREFIX = os.getenv('BOT_PREFIX', '!')

class ATXBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.voice_states = True
        intents.guilds = True
        
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None,
            case_insensitive=True
        )

    async def setup_hook(self):
        """تحميل الـ Cogs تلقائياً عند بدء التشغيل"""
        logger.info("--- جاري تحميل الإضافات (Cogs) ---")
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    logger.info(f'✅ تم تحميل الإضافة: {filename}')
                except Exception as e:
                    logger.error(f'❌ فشل تحميل الإضافة {filename}: {e}')
        logger.info("--- اكتمل تحميل الإضافات ---")

    async def on_ready(self):
        logger.info(f'🚀 تم تسجيل الدخول كـ {self.user.name} (ID: {self.user.id})')
        logger.info(f'🌐 متصل بـ {len(self.guilds)} سيرفرات')
        
        # تعيين حالة البوت
        activity = discord.Activity(type=discord.ActivityType.listening, name=f"{PREFIX}help | ATX Pro")
        await self.change_presence(status=discord.Status.online, activity=activity)

    async def on_command_error(self, ctx, error):
        """معالجة أخطاء الأوامر بشكل مركزي"""
        if isinstance(error, commands.CommandNotFound):
            return
        
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(title="❌ خطأ في الصلاحيات", description="ليس لديك الصلاحيات الكافية لتنفيذ هذا الأمر.", color=discord.Color.red())
            return await ctx.send(embed=embed)
        
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="❌ معامل مفقود", description=f"يرجى التأكد من كتابة جميع المعاملات المطلوبة. استخدم `{PREFIX}help` للمساعدة.", color=discord.Color.orange())
            return await ctx.send(embed=embed)

        if isinstance(error, commands.CheckFailure):
            return # تم التعامل معه في الـ Cog نفسه غالباً

        logger.error(f"حدث خطأ غير متوقع: {error}")
        # await ctx.send(f"⚠️ حدث خطأ داخلي: {error}")

async def run_bot():
    bot = ATXBot()
    async with bot:
        await bot.start(TOKEN)

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        logger.info("⏹️ تم إيقاف البوت يدوياً.")
    except Exception as e:
        logger.critical(f"💥 فشل تشغيل البوت: {e}")
