import os
import json
import asyncio
import numpy as np
from datetime import datetime, time, timedelta
import nextcord
from PIL import Image
from io import BytesIO
import re

GME_TICKER = 'GME'
intents = nextcord.Intents.all()
intents.members = True
client = nextcord.Client(intents=intents)
mutex = asyncio.Lock()
JuwuL_channel_id = 
transcript_channel_id = 
summary_channel_id = 

REQUESTS_COUNT = 0

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    await run_simplysummary()

async def run_simplysummary():
    while True:
        global REQUESTS_COUNT
        REQUESTS_COUNT += 1
        print("Running SimplySummary")
        # Calculate the start and end times for the past hour
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=3)
        end_time = current_time

        # Get the channel object to read messages from
        transcript_channel = client.get_channel(transcript_channel_id)

        # Fetch messages within the time range
        messages = await transcript_channel.history(limit=None, after=start_time, before=end_time).flatten()
        num_messages = len(messages)
        
        if num_messages > 10:
            # Prepare the command to trigger the summary
            command = f"SimplySummary <#{transcript_channel_id}> {num_messages}"
            # Send the command to the summary channel
            summary_channel = client.get_channel(summary_channel_id)
            await summary_channel.send(command)

        # Delay for 3 hour before running the next summary
        count = 0
        for i in range(360 * 3):
            await asyncio.sleep(10)
            count += 10
            print(f"Waiting for {3600 * 3 - count} seconds")

@client.event
async def on_message(message):
    global REQUESTS_COUNT
    async with mutex:
        try:
            if message.content.lower().startswith('simplysummary'):

                # React with loading emoji
                await message.add_reaction('⏳')

                # Split the message content into different arguments
                command, channel_tag, num_messages_str = message.content.split(' ')
                num_messages = int(num_messages_str)

                # Get the channel object based on the mentioned channel tag
                channel_id = int(channel_tag.strip('<#>'))
                channel = message.guild.get_channel(channel_id)
                print(channel.name)

                # Fetch the specified number of messages from the channel
                messages = await channel.history(limit=num_messages).flatten()
                # Sort messages by timestamp
                messages.sort(key=lambda x: x.created_at)
                
                # Get start and end times
                start_time = messages[-1].created_at if messages else datetime.now()
                end_time = messages[0].created_at if messages else datetime.now()
                
                message_texts = []
                last_timestamp = None
                
                for msg in messages:
                    if not msg.content.startswith('https://tenor.com'):
                        current_time = msg.created_at
                        
                        # Add timestamp every 15 minutes
                        if last_timestamp is None or (current_time - last_timestamp).total_seconds() >= 900:  # 900 seconds = 15 minutes
                            message_texts.append(f"\n[{current_time.strftime('%Y-%m-%d %H:%M:%S')}]\n")
                            last_timestamp = current_time
                        
                        author_name = msg.author.nick if msg.author.nick else msg.author.name
                        content = re.sub(r'<@!\d+>', '', msg.content)
                        message_texts.append(f"{author_name}: {content}")

                print(len(message_texts))

                # Concatenate the messages into a single string
                message_text = '\n'.join(message_texts)

                # Remove unicode characters
                message_text = message_text.encode('ascii', 'ignore').decode('ascii')

                # Send message_text to transcript channel as a text attachment
                with open('Transcript.txt', 'w') as f:
                    f.write(message_text)

                await client.get_channel(JuwuL_channel_id).send(
                    'Summarize this finance stock trader chatlog. '
                    'Sections include: Top mentioned tickers, including prices and targets, future expectations and sentiment. Include quotes where it provides more context. Describe the overall sentiment of the chatlog. Include any notable events or news that may have influenced the chatlog. Provide a summary of the chatlog. At the end, provide a TLDR that is fun and uses emojis and motivation',
                    file=nextcord.File('Transcript.txt'))

                # Await reply from user id 1079502852126417077
                def check(m):
                    return m.author.id == 1079502852126417077 # Juwul

                summary_parts = []
                for _ in range(3):  # Check for up to 3 messages (original + 2 more)
                    try:
                        msg = await client.wait_for('message', check=check, timeout=30.0)
                        if msg.content.strip() == "":
                            print("Empty message received. Trying again.")
                            msg = await client.wait_for('message', check=check, timeout=30.0)
                            continue
                        summary_parts.append(msg.content)
                        print(f"Received message: {msg.content}")
                    except asyncio.TimeoutError:
                        print("No message received. Continuing.")
                        continue  # Stop waiting if no message received within 30 seconds

                # Combine all parts of the summary
                full_summary = "\n".join(summary_parts)

                # Prepare the summary text with embedded timezone
                summary_text = (
                    f"**Time Range:** From: <t:{int(start_time.timestamp())}:F> To: <t:{int(end_time.timestamp())}:F>\n\n"
                    f"{full_summary}"
                )

                # Split the summary if it's too long
                max_length = 4000  # Maximum length for embed description
                summary_parts = [summary_text[i:i+max_length] for i in range(0, len(summary_text), max_length)]
                total_parts = len(summary_parts)

                # Send each part as a separate embed
                summary_channel = client.get_channel(summary_channel_id)
                for i, part in enumerate(summary_parts, 1):
                    embed = nextcord.Embed(
                        title=f"Chat Summary: {channel.name} ({i} of {total_parts})" if total_parts > 1 else f"Chat Summary: {channel.name}",
                        description=part,
                        color=0xFFFF00
                    )
                    embed.set_footer(text=f"SimplySummary generated at {datetime.now().timestamp()})")
                    await summary_channel.send(embed=embed)
                    
                    
                if REQUESTS_COUNT % 3 == 0:
                    request = "!!SUMMON!! 1,Sonnet,assets\\prompts\\no_prompt.txt,https://www.claude.ai/new"
                    await client.get_channel(JuwuL_channel_id).send(request)
                    await asyncio.sleep(30)
        except Exception as e:
            tb = e.__traceback__
            while tb.tb_next:
                tb = tb.tb_next
            print(f"Error: {e} at line {tb.tb_lineno}")

client.run('YOUR_BOT_TOKEN_HERE')
