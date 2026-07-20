"""Static dev server for the Innoculated Farms — Gold & Black site.

Sends no-cache headers so the browser always revalidates — avoids the
stale-JS/CSS problem where edits don't show up without a hard refresh.
Serves the folder this file lives in, on $PORT (default 8642).
"""
import functools
import http.server
import os


class NoCacheHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()


if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    port = int(os.environ.get("PORT", "8642"))
    handler = functools.partial(NoCacheHandler, directory=directory)
    http.server.test(HandlerClass=handler, port=port, bind="127.0.0.1")
