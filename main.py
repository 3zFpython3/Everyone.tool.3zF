import asyncio
import aiohttp
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

token = input("[+] User Token: ")
channel_id = int(input("[+] Channel ID: "))
message = input("[+] Message: ")
count = int(input("[+] Send Count: "))
delay = float(input("[+] Delay (seconds): "))

confirm = input("[+] Type 'yes' to confirm: ")
if confirm.lower() != 'yes':
    print("[!] Cancelled.")
    sys.exit()

headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

payload = {"content": message}
url = f"https://discord.com/api/v9/channels/{channel_id}/messages"

async def main():
    async with aiohttp.ClientSession(headers=headers) as session:
        print(f"[+] Sending to channel {channel_id}")
        sent = 0
        retries = 0

        while sent < count:
            try:
                async with session.post(url, json=payload) as resp:
                    if resp.status == 200 or resp.status == 201:
                        sent += 1
                        retries = 0
                        print(f"[✓] {sent}/{count}")
                        if sent < count and delay > 0:
                            await asyncio.sleep(delay)
                    elif resp.status == 429:
                        retries += 1
                        data = await resp.json()
                        retry_after = data.get("retry_after", 3)
                        print(f"[!] Rate limited. Waiting {retry_after}s ({retries}/5)")
                        if retries > 5:
                            print("[✗] Max retries. Stopping.")
                            break
                        await asyncio.sleep(retry_after + 0.3)
                    else:
                        text = await resp.text()
                        print(f"[✗] HTTP {resp.status}: {text}")
                        break
            except Exception as e:
                print(f"[✗] Error: {e}")
                break

        print("[+] Mission Complete.")

asyncio.run(main())
