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
message = input("[+] Message: ")
count = int(input("[+] Send Count: "))
delay = float(input("[+] Delay (seconds): "))

confirm = input("[+] Type 'yes' to confirm: ")

if confirm.lower() != 'yes':
    print("[!] Cancelled.")
    sys.exit()

intents = discord.Intents.default()
intents.message_content = True

class ShadowClient(discord.Client):
    async def on_ready(self):
        print(f"[+] Logged in as {self.user}")
        channel = self.get_channel(channel_id)

        if not channel:
            print("[✗] Channel not found or no permission")
            await self.close()
            return

        print(f"[+] Sending to #{channel.name}")

        sent = 0
        retries = 0
        max_retries = 5

        while sent < count:
            try:
                await channel.send(message)
                sent += 1
                retries = 0
                print(f"[✓] {sent}/{count}")
                if sent < count:
                    await asyncio.sleep(delay)
            except discord.HTTPException as e:
                if e.status == 429:
                    retries += 1
                    retry_after = float(e.response.headers.get("Retry-After", 5))
                    print(f"[!] Rate limited. Waiting {retry_after}s (attempt {retries}/{max_retries})")
                    if retries > max_retries:
                        print("[✗] Max retries exceeded. Stopping.")
                        break
                    await asyncio.sleep(retry_after + 0.5)
                else:
                    print(f"[✗] HTTP Error {e.status}: {e}")
                    break
            except Exception as e:
                print(f"[✗] Error: {e}")
                break

        print("[+] Mission Complete.")
        await self.close()

client = ShadowClient(intents=intents)
client.run(token)
