import asyncio
import aiohttp
import sys

print(r"""
 _   _       ____                 
| | | | __ _|___ \  ___ ___ _ __  
| |_| |/ _` | __) |/ __/ _ \ '__| 
|  _  | (_| |/ __/| (_|  __/ |    
|_| |_|\__,_|_____|\___\___|_|    
""")
print("="*50)
print("DEV BY 3zF | SHADOW MODE V99 | TURBO ASYNC")
print("="*50)

token = input("[+] User Token: ")
channel_id = int(input("[+] Channel ID: "))
message = input("[+] Message: ")
count = int(input("[+] Send Count: "))
concurrent = int(input("[+] Concurrent sends (1-50) [20]: ") or "20")

confirm = input("[+] Type 'yes' to confirm: ")
if confirm.lower() != 'yes':
    print("[!] Cancelled.")
    sys.exit()

headers = {
    "Authorization": token,
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

url = f"https://discord.com/api/v9/channels/{channel_id}/messages"
payload = {"content": message}

sent = 0
sem = asyncio.Semaphore(int(concurrent))

async def send_one(session):
    global sent
    async with sem:
        try:
            async with session.post(url, json=payload) as resp:
                if resp.status in [200, 201]:
                    sent += 1
                    print(f"[✓] {sent}/{count}")
                elif resp.status == 429:
                    data = await resp.json()
                    await asyncio.sleep(data.get("retry_after", 2))
                else:
                    print(f"[✗] {resp.status}")
        except:
            pass

async def main():
    global sent
    connector = aiohttp.TCPConnector(limit=0, force_close=True)
    async with aiohttp.ClientSession(headers=headers, connector=connector) as session:
        tasks = []
        for _ in range(count):
            tasks.append(send_one(session))
        await asyncio.gather(*tasks)
    print(f"[+] Done. Sent: {sent}")

asyncio.run(main())
