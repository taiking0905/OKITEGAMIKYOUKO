import discord
import asyncio
from discord.ext import commands, tasks # Import tasks for continuous operation
import sys
import os

# 消したいチャンネルのIDを設定、掟上今日子
DISCORD_CHANNEL_ID = os.getenv("DISCORD_CHANNEL_ID")
# BOTのトークン
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")


# すべてのインテントを有効化
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"ログインしました: {bot.user}")
    # Start the message deletion task when the bot is ready
    delete_old_messages.start() # Call the task to start running

# Define a background task for message deletion
@tasks.loop(hours=24) # Example: run this task every 24 hours
async def delete_old_messages():
    try:
        # 特定のチャンネルを取得
        target_channel = bot.get_channel(DISCORD_CHANNEL_ID)

        if target_channel:
            print(f"チャンネル '{target_channel.name}' からメッセージを削除中...")
            # Delete messages. You might want to adjust the 'limit' or add 'before'/'after'
            # to delete messages older than a certain time.
            await target_channel.purge(limit=100) # Delete latest 100 messages
            print("メッセージ削除完了！")

            # ボットをシャットダウンしてからシステムを終了
            await bot.close() # <-- これが重要！
            sys.exit(0) # 成功時はcmdを閉じる
        else:
            print(f"チャンネルID {DISCORD_CHANNEL_ID} が見つかりませんでした。")
            await bot.close() # <-- これが重要！
            sys.exit(1) # チャンネルが見つからなければ終了コード1で失敗

    except Exception as e:
        print(f"メッセージ削除中にエラーが発生しました: {e}")
        # エラー発生時もボットをシャットダウンしてからシステムを終了
        await bot.close() # <-- これが重要！
        sys.exit(1) # エラー発生時も終了コード1で終了

bot.run(DISCORD_TOKEN)