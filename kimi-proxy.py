#!/usr/bin/env python3
"""
Math Garden — local server + KIMI (Moonshot) proxy.

WHY THIS EXISTS:
  A web page can't safely hold an API key (anyone could read it), and browsers
  usually block direct calls to the Moonshot API. This little server fixes both:
  it serves the game AND forwards KIMI requests, keeping your key on your own
  machine. The browser never sees the key.

HOW TO RUN (no installation needed — uses Python's built-in library):
  1. Open a terminal in this folder.
  2. Run:   python3 kimi-proxy.py
  3. In your browser, go to:   http://localhost:8000/math-garden.html
  4. Press Ctrl+C in the terminal to stop the server.

The key is read from kimi-key.txt (in this folder) or the KIMI_API_KEY env var.
Keep kimi-key.txt private — don't share or upload it.
"""
import http.server, socketserver, json, os, urllib.request, urllib.error
from urllib.parse import urlparse, parse_qs

PORT = 8000
HERE = os.path.dirname(os.path.abspath(__file__))
MOONSHOT_URL = "https://api.moonshot.cn/v1/chat/completions"
PROGRESS_FILE = os.path.join(HERE, "progress.json")  # all players' saved progress live here


def load_key():
    k = os.environ.get("KIMI_API_KEY")
    if k:
        return k.strip()
    p = os.path.join(HERE, "kimi-key.txt")
    if os.path.exists(p):
        with open(p) as f:
            return f.read().strip()
    return None


def read_all_progress():
    """Return {username: progress} for all players. Migrates the old
    single-profile format ({"coins":...}) into {"Sophie": {...}}."""
    if not os.path.exists(PROGRESS_FILE):
        return {}
    try:
        with open(PROGRESS_FILE) as f:
            data = json.load(f)
    except Exception:
        return {}
    if not isinstance(data, dict):
        return {}
    if "coins" in data:          # old flat format -> belongs to Sophie
        return {"Sophie": data}
    return data


def write_all_progress(allp):
    with open(PROGRESS_FILE, "w") as f:
        json.dump(allp, f)


def get_user(path):
    """Pull ?user=Name from a request path (defaults to 'Sophie')."""
    q = parse_qs(urlparse(path).query)
    return (q.get("user", ["Sophie"])[0]).strip() or "Sophie"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=HERE, **kwargs)

    def do_GET(self):
        # List of player names: GET /api/users
        if self.path.split("?")[0] == "/api/users":
            self._send_json(200, {"users": sorted(read_all_progress().keys())})
            return
        # One player's saved progress: GET /api/load?user=Name
        if self.path.split("?")[0] == "/api/load":
            user = get_user(self.path)
            self._send_json(200, read_all_progress().get(user, {}))
            return
        return super().do_GET()

    def do_POST(self):
        # Save one player's progress: POST /api/save?user=Name
        if self.path.split("?")[0] == "/api/save":
            user = get_user(self.path)
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                prog = json.loads(body)  # validate it's real JSON
                allp = read_all_progress()
                allp[user] = prog
                write_all_progress(allp)
                self._send_json(200, {"ok": True})
            except Exception as e:
                self._send_json(400, {"error": str(e)})
            return
        if self.path != "/api/kimi":
            self.send_error(404, "Not found")
            return
        key = load_key()
        if not key:
            self._send_json(500, {"error": "No API key found. Put it in kimi-key.txt."})
            return
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        req = urllib.request.Request(
            MOONSHOT_URL,
            data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": "Bearer " + key},
            method="POST",
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                self._send_raw(200, resp.read())
        except urllib.error.HTTPError as e:
            self._send_raw(e.code, e.read())
        except Exception as e:
            self._send_json(502, {"error": str(e)})

    def _send_json(self, code, obj):
        self._send_raw(code, json.dumps(obj).encode())

    def _send_raw(self, code, raw):
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass  # keep the terminal quiet


if __name__ == "__main__":
    if not load_key():
        print("WARNING: no key found in kimi-key.txt or KIMI_API_KEY environment variable.")
    print("=" * 56)
    print("  Math Garden is running!")
    print("  Open this in your browser:")
    print(f"     http://localhost:{PORT}/math-garden.html")
    print("  Press Ctrl+C here to stop.")
    print("=" * 56)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("127.0.0.1", PORT), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped. Bye!")
