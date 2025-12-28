# Tool that extracts usernames and user IDs from reactions on specific Discord messages

## Key Features

* **Deep Scraping:** Fetches all users even if the reaction count is in the thousands
* **Auto-Save:** Automatically generates a text file named after the message ID containing the results
* **Duplicate Removal:** If a user reacted with multiple emojis, they are only listed once

## Prerequisites

To use this software, you need three pieces of information:

```text
User Token
```

```text
Channel ID
```

```text
Message ID
```

### How to find your User Token

1. Open Discord in your browser (Chrome, Firefox, etc.)
2. Press F12 to open Developer Tools and go to the "Network" tab
3. Click on any text channel in Discord to trigger a network request
4. In the Network filter box, search for "messages" or "science"
5. Click on one of the requests and look at the "Request Headers" section
6. Copy the text next to "authorization". This is your token
7. **Do not share this token with anyone**

### How to find IDs

First, enable Developer Mode in Discord (User Settings > Advanced > Developer Mode)

* **Channel ID:** Right-click the channel name and select "Copy Channel ID"
* **Message ID:** Right-click the specific message and select "Copy Message ID"

## Installation and Usage

### Option 1: Download the Application (Windows)

Go to the "Releases" section on the right side of this page and download the RAR archive. You can run it directly without installing Python.

### Option 2: Run from Source

If you prefer to run the raw Python code:

1. Clone this repository.
2. Install the required specific library (DO NOT use the standard discord.py):
   ```bash
   pip install discord.py-self
   ```
3. Run the script:
   ```bash
   python main.py
   ```

## Output Format

The software produces a clean text file for every scrape. It looks like this:

```text
-- MADE BY THENOTFUEL -- Discord: @face.punch

Username1 | ID: 123456789012345678
Username2 | ID: 987654321098765432
UserThree | ID: 112233445566778899
```

## Disclaimer

This tool functions as a "self-bot," meaning it automates actions on a user account. This is technically against Discord's Terms of Service. Use it responsibly and avoid scraping massive amounts of data in a short period to prevent temporary account restrictions

## Credits

Developed by **TheNotFuel**
Discord: **@face.punch**
