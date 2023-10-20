import discord
import asyncio
import time
import requests

from discord.ext import commands
from discord import Interaction
from discord import app_commands

def embed(bot):
	embed=discord.Embed(title="Pong🏓", color=discord.Colour.green())
	embed.add_field(name="Latency:", value=int(bot.latency * 1000), inline=False)
	res = requests.get("https://api.country.is")
	c = res.json()["country"]
	embed.add_field(name="Server:", value=f"{c} :flag_{c.lower()}:", inline=False)
	embed.add_field(name="Extensions:", value=len(bot.extensions), inline=False)
	embed.add_field(name="Uptime:", value="From <t:{0}>(<t:{0}:R>)".format(timee), inline=False)
	return embed

class view(discord.ui.View):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
		super().__init__(timeout=None)
	
	@discord.ui.button(custom_id="ping_1", label="Extension list", style=discord.ButtonStyle.green)
	async def ping_1(self, ctx:Interaction, btn):
		await ctx.response.defer()
		e = discord.Embed(title="Extension list", color=discord.Color.green())
		n = 1
		for ext in self.bot.extensions:
			e.add_field(name=f"{n}- {ext}", value="", inline=False)
			n += 1
		await ctx.followup.send(embed=e)
	
	@discord.ui.button(custom_id="ping_2", label="Refresh", style=discord.ButtonStyle.green)
	async def ping_2(self, ctx:Interaction, btn):
		await ctx.message.edit(content=f"Last refresh: <t:{int(time.time())}:R>", embed=embed(self.bot), view=view(self.bot))
		await ctx.response.send_message("✅", ephemeral=True)
		await asyncio.sleep(1)
		await ctx.delete_original_response()

class Ping(commands.Cog):
	def __init__(self, bot:commands.Bot):
		self.bot = bot
	
	@commands.Cog.listener()
	async def on_ready(self):
		global timee
		timee = int(time.time())
	
	@app_commands.command(name = "ping", description = "Show QoqnusBot ping🏓")
	async def ping(self, ctx: Interaction):
		await ctx.response.defer()
		await ctx.followup.send(embed=embed(self.bot), view=view(self.bot))

async def setup(bot:commands.Bot):
    await bot.add_cog(Ping(bot))
    bot.add_view(view(bot))
