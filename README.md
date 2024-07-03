Here's a draft GitHub README for the provided code:

# SimplySummary Discord Bot

SimplySummary is a Discord bot that automatically summarizes chat conversations in specified channels. It uses natural language processing to generate concise summaries of chat logs, making it easier for users to catch up on discussions they may have missed.
Makes use of JuwuL AI Discord bot for LLM processing. 

## Features

- Automatically summarizes chat logs every 3 hours
- Can be manually triggered to summarize a specific number of messages
- Generates summaries that include:
  - Top mentioned stock tickers with prices and targets
  - Future expectations and sentiment
  - Notable events or news
  - Overall chat sentiment
  - TLDR with emojis for quick understanding
- Handles long summaries by splitting them into multiple Discord embeds
- Uses Discord's timestamp formatting for clear time ranges

## Setup

1. Clone this repository
2. Install the required dependencies:
   ```
   pip install nextcord pillow numpy
   ```
3. Set up a Discord bot and get your bot token
4. Replace the placeholder token at the bottom of the script with your actual bot token
5. Update the channel IDs in the script to match your Discord server's channels
6. Run the script:
   ```
   python bot.py
   ```

## Usage

The bot will automatically run summaries every 3 hours. To manually trigger a summary, use the following command in your Discord server:

```
SimplySummary #channel-name number_of_messages
```

For example:
```
SimplySummary #general 100
```

This will summarize the last 100 messages in the #general channel.

## Configuration

You can modify the following variables in the script to customize the bot's behavior:

- `JuwuL_channel_id`: ID of the channel used for processing summaries
- `transcript_channel_id`: ID of the main chat channel to be summarized
- `summary_channel_id`: ID of the channel where summaries will be posted

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This bot is designed for use in finance and stock trading Discord communities. Always do your own research and consult with a financial advisor before making investment decisions based on chat summaries.
