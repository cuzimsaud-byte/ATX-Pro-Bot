import discord
from discord.ext import commands

class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lock")
    @commands.has_permissions(manage_channels=True)
    async def lock(self, ctx):
        """قفل القناة الحالية للأعضاء"""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        
        embed = discord.Embed(
            title="🔒 تم قفل القناة",
            description="تم منع الأعضاء من إرسال الرسائل في هذه القناة.",
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

    @commands.command(name="unlock")
    @commands.has_permissions(manage_channels=True)
    async def unlock(self, ctx):
        """فتح القناة للأعضاء"""
        overwrite = ctx.channel.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = None # يعيدها للوضع الافتراضي
        await ctx.channel.set_permissions(ctx.guild.default_role, overwrite=overwrite)
        
        embed = discord.Embed(
            title="🔓 تم فتح القناة",
            description="يمكن للأعضاء الآن إرسال الرسائل مرة أخرى.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    @commands.command(name="clear")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """مسح عدد محدد من الرسائل"""
        if amount < 1:
            return await ctx.send("❌ يرجى تحديد عدد أكبر من 0.")
        
        deleted = await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f"✅ تم مسح {len(deleted)-1} رسالة.", delete_after=5)

    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """طرد عضو من السيرفر"""
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("❌ لا يمكنك طرد عضو لديه رتبة أعلى منك أو مساوية لك.")
        
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="👢 تم الطرد",
            description=f"تم طرد {member.mention} من السيرفر.\n**السبب:** {reason or 'غير محدد'}",
            color=discord.Color.orange()
        )
        await ctx.send(embed=embed)

    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """حظر عضو من السيرفر"""
        if member.top_role >= ctx.author.top_role:
            return await ctx.send("❌ لا يمكنك حظر عضو لديه رتبة أعلى منك أو مساوية لك.")
        
        await member.ban(reason=reason)
        embed = discord.Embed(
            title="🔨 تم الحظر",
            description=f"تم حظر {member.mention} من السيرفر.\n**السبب:** {reason or 'غير محدد'}",
            color=discord.Color.dark_red()
        )
        await ctx.send(embed=embed)

    # معالجة الأخطاء الخاصة بـ Cog الإدارة
    @lock.error
    @unlock.error
    @clear.error
    @kick.error
    @ban.error
    async def admin_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ ليس لديك الصلاحيات الكافية لتنفيذ هذا الأمر الإداري.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ يرجى التأكد من ذكر العضو بشكل صحيح أو إدخال رقم صحيح.")

    @commands.command(name='help')
    async def help_command(self, ctx):
        """عرض قائمة الأوامر المتاحة"""
        embed = discord.Embed(
            title="📚 قائمة الأوامر المتاحة",
            description="جميع الأوامر المتوفرة في البوت ATX Pro",
            color=discord.Color.purple()
        )
        
        embed.add_field(
            name="🔴 أوامر التنبيهات",
            value="`!add_streamer <platform> <username>` - إضافة ستريمر\n"
                  "`!set_alert_channel #channel` - تعيين قناة التنبيهات",
            inline=False
        )
        
        embed.add_field(
            name="🛡️ أوامر الإدارة",
            value="`!lock` - قفل القناة\n"
                  "`!unlock` - فتح القناة\n"
                  "`!clear <number>` - مسح الرسائل\n"
                  "`!kick <member> [reason]` - طرد عضو\n"
                  "`!ban <member> [reason]` - حظر عضو",
            inline=False
        )
        
        embed.add_field(
            name="🎶 أوامر الموسيقى",
            value="`!join` - دخول الروم الصوتي\n"
                  "`!play <url/search>` - تشغيل أغنية\n"
                  "`!skip` - تخطي الأغنية\n"
                  "`!stop` - إيقاف والخروج\n"
                  "`!queue` - عرض قائمة الانتظار",
            inline=False
        )
        
        embed.set_footer(text="ATX Pro Bot v1.0.0")
        await ctx.send(embed=embed)


    @commands.command(name='reload')
    @commands.is_owner()
    async def reload_cogs(self, ctx):
        """إعادة تحميل جميع الـ Cogs بدون إيقاف البوت"""
        try:
            # إعادة تحميل التنبيهات
            await ctx.bot.reload_extension('cogs.notifications')
            # إعادة تحميل الإدارة
            await ctx.bot.reload_extension('cogs.admin')
            # إعادة تحميل الموسيقى
            await ctx.bot.reload_extension('cogs.music')
            
            embed = discord.Embed(
                title="✅ تم إعادة التحميل",
                description="تم إعادة تحميل جميع الـ Cogs بنجاح!",
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = discord.Embed(
                title="❌ خطأ في إعادة التحميل",
                description=f"حدث خطأ: {str(e)}",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Admin(bot))

