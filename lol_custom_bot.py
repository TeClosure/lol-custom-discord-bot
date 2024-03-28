import discord
import os
import requests

from discord.ext import commands
from dotenv import load_dotenv

load_dotenv(".env")

BOT_TOKEN = os.getenv("BOT_TOKEN")
REGION = "jp1"
RIOT_API_KEY = os.getenv("RIOT_API_KEY")


intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", case_insensitive=True, intents=intents)

client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)


@client.event
async def on_ready():
    print("Bot is ready.")
    await tree.sync()


@tree.command(
    name="register",
    description="サモナーネームを登録し、その人の直近のランク情報を取得します。",
)
async def register(ctx: discord.Interaction, summoner_name: str, tag_line: str) -> None:
    """
    サモナーネームを登録し、その人の直近のランク情報を取得します。
    Riot APIを叩いてランク情報を取得し、その情報をローカルサーバーに保存します。
    使用方法: /register <サモナーネーム>
    """
    # Riot APIを叩いてランク情報を取得
    print("register start")

    account_info_url = f"https://asia.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{summoner_name}/{tag_line}?api_key={RIOT_API_KEY}"

    account_info_response = requests.get(account_info_url)

    account_info = account_info_response.json()
    puu_id = account_info["puuid"]

    summoner_info_url = f"https://jp1.api.riotgames.com/lol/summoner/v4/summoners/by-puuid/{puu_id}?api_key={RIOT_API_KEY}"

    summoner_info_response = requests.get(summoner_info_url)
    print(summoner_info_response.json())

    summoner_info = summoner_info_response.json()
    encrypted_summoner_id = summoner_info["id"]

    rank_stats_url = f"https://{REGION}.api.riotgames.com/lol/league/v4/entries/by-summoner/{encrypted_summoner_id}?api_key={RIOT_API_KEY}"

    rank_stats_response = requests.get(rank_stats_url)
    print(rank_stats_response.json())

    # await ctx.response.send_message(ranked_stats)

    # rank_info = response.json()

    # # ランク情報をローカルサーバーに保存
    # with open("rank_info.txt", "a") as f:
    #     f.write(f"{summoner_name}: {rank_info}\n")

    # await ctx.send(f"{summoner_name}さんのランク情報を登録しました。")


client.run(BOT_TOKEN)
