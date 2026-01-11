import discord
from discord.ext import commands
import yt_dlp
import asyncio
import functools

# إعدادات yt_dlp لضمان أفضل جودة وسرعة
YDL_OPTIONS = {
    'format': 'bestaudio/best',
    'extractaudio': True,
    'audioformat': 'mp3',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',
}

# إعدادات FFmpeg لتقليل التقطيع (Buffering)
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn',
}

ytdl = yt_dlp.YoutubeDL(YDL_OPTIONS)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        partial = functools.partial(ytdl.extract_info, url, download=not stream)
        data = await loop.run_in_executor(None, partial)

        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **FFMPEG_OPTIONS), data=data)

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.queue = {}

    def get_queue(self, ctx):
        if ctx.guild.id not in self.queue:
            self.queue[ctx.guild.id] = []
        return self.queue[ctx.guild.id]

    @commands.command(name="join")
    async def join(self, ctx):
        """دخول البوت للروم الصوتي"""
        if not ctx.author.voice:
            return await ctx.send("❌ يجب أن تكون في روم صوتي أولاً!")
        
        channel = ctx.author.voice.channel
        if ctx.voice_client:
            await ctx.voice_client.move_to(channel)
        else:
            await channel.connect()
        await ctx.send(f"✅ تم الدخول إلى {channel.mention}")

    @commands.command(name="play")
    async def play(self, ctx, *, search: str):
        """تشغيل أغنية من يوتيوب (رابط أو بحث)"""
        if not ctx.voice_client:
            await ctx.invoke(self.join)
        
        if not ctx.voice_client: return

        async with ctx.typing():
            try:
                player = await YTDLSource.from_url(search, loop=self.bot.loop, stream=True)
                queue = self.get_queue(ctx)
                queue.append(player)
                
                if not ctx.voice_client.is_playing():
                    self.play_next(ctx)
                    await ctx.send(f"🎶 جاري تشغيل: **{player.title}**")
                else:
                    await ctx.send(f"📝 تمت إضافة **{player.title}** إلى قائمة الانتظار.")
            except Exception as e:
                await ctx.send(f"❌ حدث خطأ أثناء محاولة التشغيل: {e}")

    def play_next(self, ctx):
        queue = self.get_queue(ctx)
        if len(queue) > 0:
            player = queue.pop(0)
            ctx.voice_client.play(player, after=lambda e: self.play_next(ctx))
        else:
            # يمكن إضافة مؤقت للخروج التلقائي هنا
            pass

    @commands.command(name="skip")
    async def skip(self, ctx):
        """تخطي الأغنية الحالية"""
        if ctx.voice_client and ctx.voice_client.is_playing():
            ctx.voice_client.stop()
            await ctx.send("⏭️ تم تخطي الأغنية.")
        else:
            await ctx.send("❌ لا توجد موسيقى تعمل حالياً لتخطيها.")

    @commands.command(name="stop")
    async def stop(self, ctx):
        """إيقاف الموسيقى والخروج من الروم"""
        if ctx.voice_client:
            self.queue[ctx.guild.id] = []
            await ctx.voice_client.disconnect()
            await ctx.send("⏹️ تم إيقاف الموسيقى والخروج.")
        else:
            await ctx.send("❌ البوت ليس في روم صوتي أصلاً.")

    @commands.command(name="queue")
    async def queue_list(self, ctx):
        """عرض قائمة الانتظار"""
        queue = self.get_queue(ctx)
        if not queue:
            return await ctx.send("📝 قائمة الانتظار فارغة حالياً.")
        
        description = ""
        for i, player in enumerate(queue):
            description += f"{i+1}. {player.title}\n"
        
        embed = discord.Embed(title="📝 قائمة الانتظار", description=description, color=discord.Color.blue())
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Music(bot))
