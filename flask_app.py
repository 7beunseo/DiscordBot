import discord
import asyncio
import time
from config import CHANNEL_ID, TOKEN
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.presences = True
intents.members = True

client = discord.Client(intents=intents)

# 음성 채널 입장 시간 저장할 딕셔너리
join_times = {}

# 유저별 음성 채팅 시간 저장할 딕셔너리
user_voice_times = {}

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    await client.change_presence(status=discord.Status.online,
                                 activity=discord.Game("밤새 코딩"))

@client.event
async def on_voice_state_update(member, before, after):
    # 음성 채널에서 입장
    if before.channel is None and after.channel is not None:
        join_times[member.id] = time.time()

    # 음성 채널에서 퇴장
    elif before.channel is not None and after.channel is None:
        if member.id in join_times:
            join_time = join_times.pop(member.id)
            duration = time.time() - join_time
            # 시간 누적
            if member.id in user_voice_times:
                user_voice_times[member.id] += duration
            else:
                user_voice_times[member.id] = duration
            channel = client.get_channel(CHANNEL_ID)

            hours = int(duration // 3600)
            minutes = int((duration % 3600) // 60)
            seconds = int(duration % 60)
            if channel is not None:
                await channel.send(
                    f'{member.mention}님이 음성 채팅에서 {hours}시간 {minutes}분 {seconds}초를 보냈습니다.'
                )
                await print_voice_statistics(channel)

async def print_voice_statistics(channel):
    # 통계 출력
    voice_statistics = "음성 채팅 통계\n"
    for user_id, voice_time in user_voice_times.items():
        hours = int(voice_time // 3600)
        minutes = int((voice_time % 3600) // 60)
        seconds = int(voice_time % 60)
        voice_statistics += f"<@{user_id}>: {hours}시간 {minutes}분 {seconds}초\n"
    await channel.send(voice_statistics)

keep_alive()
client.run(TOKEN)