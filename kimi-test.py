#!/usr/bin/env python3
"""
Quick check: is your KIMI (Moonshot) API key working?

Run from this folder:   python3 kimi-test.py

It reads the key from kimi-key.txt (or the KIMI_API_KEY environment variable),
makes one tiny request, and tells you plainly whether the key works.
"""
import os, json, urllib.request, urllib.error

# Moonshot has two regions. We try the global one first, then the China one.
HOSTS = ["https://api.moonshot.ai/v1/chat/completions",
         "https://api.moonshot.cn/v1/chat/completions"]


def load_key():
    k = os.environ.get("KIMI_API_KEY")
    if k:
        return k.strip()
    here = os.path.dirname(os.path.abspath(__file__))
    p = os.path.join(here, "kimi-key.txt")
    if os.path.exists(p):
        return open(p).read().strip()
    return None


def main():
    key = load_key()
    if not key:
        print("❌ No key found. Put it in kimi-key.txt or set KIMI_API_KEY.")
        return
    print(f"Using key: {key[:7]}...{key[-4:]}\n")

    body = json.dumps({
        "model": "moonshot-v1-8k",
        "messages": [{"role": "user", "content": "Reply with just the word: OK"}],
    }).encode()

    for url in HOSTS:
        print(f"Trying {url} ...")
        req = urllib.request.Request(
            url, data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + key},
            method="POST")
        try:
            with urllib.request.urlopen(req, timeout=25) as r:
                d = json.load(r)
                reply = d["choices"][0]["message"]["content"].strip()
                print(f"\n✅ SUCCESS — your key works! KIMI replied: {reply!r}")
                print(f"   (working endpoint: {url})")
                return
        except urllib.error.HTTPError as e:
            detail = e.read().decode(errors="replace")[:400]
            if e.code in (401, 403):
                print(f"   ❌ {e.code}: key rejected — invalid, expired, or no access.\n      {detail}")
            elif e.code == 429:
                print(f"   ⚠️ 429: key is valid but out of quota / rate-limited.\n      {detail}")
            else:
                print(f"   ⚠️ HTTP {e.code}: {detail}")
        except Exception as e:
            print(f"   ⚠️ Could not connect: {type(e).__name__}: {e}")

    print("\nFinished. If both endpoints failed with a connection error, check your "
          "internet; if they returned 401/403, the key itself is the problem.")


if __name__ == "__main__":
    main()
