import discord
from discord.ext import commands, tasks
import aiohttp
import os
from twitchAPI.twitch import Twitch
from utils.data_manager import DataManager

class Notifications(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.twitch_client_id = os.getenv('TWITCH_CLIENT_ID')
        self.twitch_client_secret = os.getenv('TWITCH_CLIENT_SECRET')
        self.check_interval = int(os.getenv('CHECK_INTERVAL', 60))
        self.session = None
        self.twitch = None
        self.check_streams.start()

    async def cog_unload(self):
        self.check_streams.cancel()
        if self.session:
            await self.session.close()

    async def get_twitch_client(self):
        if not self.twitch:
            try:
                self.twitch = await Twitch(self.twitch_client_id, self.twitch_client_secret)
            except Exception as e:
                print(f"Twitch API Error: {e}")
        return self.twitch

    @tasks.loop(seconds=60)
    async def check_streams(self):
        if not self.session:
            self.session = aiohttp.ClientSession()
        
        data = DataManager.load_data()
        
        # فحص Twitch
        await self.check_twitch(data)
        # فحص Kick
        await self.check_kick(data)

    async def check_twitch(self, data):
        twitch = await self.get_twitch_client()
        if not twitch: return

        streamers = data["streamers"].get("twitch", [])
        for username in streamers:
            try:
                # الحصول على معلومات المستخدم
                user_gen = twitch.get_users(logins=[username])
                user = None
                async for u in user_gen:
                    user = u
                    break
                
                if not user: continue

                # الحصول على معلومات البث
                stream_gen = twitch.get_streams(user_id=[user.id])
                stream = None
                async for s in stream_gen:
                    stream = s
                    break

                is_live = stream is not None
                status_key = f"twitch:{username}"
                was_live = data["stream_status"].get(status_key, False)

                if is_live and not was_live:
                    await self.send_alert("Twitch", username, stream.title, stream.game_name, f"https://twitch.tv/{username}", user.profile_image_url, stream.thumbnail_url.replace("{width}", "1280").replace("{height}", "720"))
                    data["stream_status"][status_key] = True
                    DataManager.save_data(data)
                elif not is_live and was_live:
                    data["stream_status"][status_key] = False
                    DataManager.save_data(data)
            except Exception as e:
                print(f"Error checking Twitch {username}: {e}")

    async def check_kick(self, data):
        streamers = data["streamers"].get("kick", [])
        for username in streamers:
            try:
                async with self.session.get(f"https://kick.com/api/v2/channels/{username}") as resp:
                    if resp.status == 200:
                        res = await resp.json()
                        livestream = res.get("livestream")
                        is_live = livestream is not None
                        status_key = f"kick:{username}"
                        was_live = data["stream_status"].get(status_key, False)

                        if is_live and not was_live:
                            title = livestream.get("session_title", "No Title")
                            game = livestream.get("categories", [{}])[0].get("name", "Unknown")
                            pfp = res.get("user", {}).get("profile_pic")
                            thumb = livestream.get("thumbnail", {}).get("url")
                            await self.send_alert("Kick", username, title, game, f"https://kick.com/{username}", pfp, thumb)
                            data["stream_status"][status_key] = True
                            DataManager.save_data(data)
                        elif not is_live and was_live:
                            data["stream_status"][status_key] = False
                            DataManager.save_data(data)
            except Exception as e:
                print(f"Error checking Kick {username}: {e}")

    async def send_alert(self, platform, username, title, game, url, pfp, thumb):
        data = DataManager.load_data()
        for guild_id, config in data["guilds"].items():
            channel_id = config.get("alert_channel")
            if not channel_id: continue
            
            channel = self.bot.get_channel(int(channel_id))
            if not channel: continue

            embed = discord.Embed(
                title=f"🔴 {username} الآن مباشر على {platform}!",
                description=f"**{title}**",
                url=url,
                color=0x9146FF if platform == "Twitch" else 0x53FC18
            )
            embed.add_field(name="🎮 اللعبة", value=game, inline=True)
            embed.set_thumbnail(url=pfp)
            if thumb: embed.set_image(url=thumb)
            embed.set_footer(text="ATX Pro Notifications", icon_url=pfp)
            
            await channel.send(content="@everyone" if platform == "Twitch" else None, embed=embed)

    @commands.command(name="add_streamer")
    @commands.has_permissions(administrator=True)
    async def add_streamer(self, ctx, platform: str, username: str):
        """إضافة ستريمر للمراقبة (twitch/kick)"""
        platform = platform.lower()
        if platform not in ["twitch", "kick"]:
            return await ctx.send("❌ المنصات المدعومة فقط: twitch, kick")
        
        data = DataManager.load_data()
        if username not in data["streamers"][platform]:
            data["streamers"][platform].append(username)
            DataManager.save_data(data)
            await ctx.send(f"✅ تم إضافة **{username}** من منصة **{platform}**")
        else:
            await ctx.send("⚠️ هذا الستريمر موجود بالفعل في القائمة.")

    @commands.command(name="set_alert_channel")
    @commands.has_permissions(administrator=True)
    async def set_alert_channel(self, ctx, channel: discord.TextChannel):
        """تحديد قناة التنبيهات"""
        DataManager.update_guild_config(str(ctx.guild.id), "alert_channel", channel.id)
        await ctx.send(f"✅ تم تعيين قناة التنبيهات إلى {channel.mention}")

async def setup(bot):
    await bot.add_cog(Notifications(bot))
