"""Record Perseus Dashboard demo video for H0 Hackathon submission."""
import os, sys, time, threading
import http.server, socketserver
from playwright.sync_api import sync_playwright

DEMO_DIR = '/opt/data/webui/minions/.minions-data/workspace/perseus-dashboard/demo'
VIDEO_DIR = os.path.join(DEMO_DIR, 'video_output')
HTML_FILE = 'demo_terminal.html'

os.makedirs(VIDEO_DIR, exist_ok=True)
os.chdir(DEMO_DIR)

# Start local HTTP server
httpd = socketserver.TCPServer(("", 9876), http.server.SimpleHTTPRequestHandler)
t = threading.Thread(target=httpd.serve_forever, daemon=True)
t.start()
print("HTTP server started on :9876")

# Total animation duration from the HTML: ~160 seconds
# Scene 1: ~9.3s, Scene 2: ~7s, Scene 3: ~8.7s, Scene 4: ~4.5s, Scene 5: ~8.5s = ~38s + gaps
# Let's use 165s for safety with the HTML timing
TOTAL_DURATION = 170

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        record_video_dir=VIDEO_DIR,
        record_video_size={'width': 1280, 'height': 720},
    )
    page = context.new_page()
    
    # Navigate to the local HTTP server
    page.goto(f'http://localhost:9876/{HTML_FILE}',
              wait_until='domcontentloaded', timeout=15000)
    
    # Verify JS is running
    time.sleep(3)
    screen_text = page.inner_text('#screen')
    if len(screen_text.strip()) == 0:
        print(f"WARNING: Screen empty! JS may not have executed.")
        errors = []
        page.on('pageerror', lambda err: errors.append(str(err)))
        time.sleep(2)
        if errors:
            print(f"JS errors: {errors}")
    else:
        print(f"Screen has content ({len(screen_text)} chars) — JS running")
    
    # Wait for animation to complete
    print(f"Recording for {TOTAL_DURATION}s...")
    time.sleep(TOTAL_DURATION)
    
    # Close context to save video
    context.close()
    browser.close()
    httpd.shutdown()
    print("Recording complete!")

# Find the output webm
webm_files = [f for f in os.listdir(VIDEO_DIR) if f.endswith('.webm')]
if webm_files:
    webm_path = os.path.join(VIDEO_DIR, webm_files[0])
    print(f"Video saved: {webm_path}")
    print(f"Size: {os.path.getsize(webm_path) / 1024:.1f} KB")
else:
    print("ERROR: No webm file found in video_output/")
    sys.exit(1)
