import discord
import asyncio
import sys
import time

print(r"""
 _   _       ____                 
| | | | __ _|___ \  ___ ___ _ __  
| |_| |/ _` | __) |/ __/ _ \ '__| 
|  _  | (_| |/ __/| (_|  __/ |    
|_| |_|\__,_|_____|\___\___|_|    
""")
print("="*50)
print("DEV BY 3zF | SHADOW MODE V99")
print("="*50)

token = input("[+] Bot Token: ")
channel_id = int(input("[+] Channel ID: "))
message = input("[+] Message: "))
count = int(input("[+] Send Count: "))
delay = float(input("[+] Delay (seconds): "))

confirm = input("[+] Type 'yes' to confirm: ")

if confirm.lower() != 'yes':
    print("[!] Cancelled.")
    sys.exit()

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"[+] Logged in as {client.user}")
    channel = client.get_channel(channel_id)
    
    if not channel:
        print("[✗] Channel not found or no permission")
        await client.close()
        return
    
    print(f"[+] Sending to {channel.name}")
    
    for i in range(1, count + 1):
        try:
            await channel.send(message)
            print(f"[✓] {i}/{count}")
            await asyncio.sleep(delay)
        except Exception as e:
            print(f"[✗] Error: {e}")
            break
    
    print("[+] Mission Complete.")
    await client.close()

client.run(token)
