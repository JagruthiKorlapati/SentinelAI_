import time
import threading

from agents import ALL_AGENTS
from orchestrator import analyse_incident

# Make each agent take 1 second to simulate slow work (e.g. LLM call)
for agent in ALL_AGENTS:
    original = agent.analyse

    def slow(incident, _orig=original, _name=agent.name):
        print(f"  start: {_name} (thread {threading.current_thread().name})")
        time.sleep(1)
        return _orig(incident)

    agent.analyse = slow

start = time.time()
analyse_incident("Ransomware detected on payment server", use_llm=False)
print(f"\nTotal time: {time.time() - start:.1f}s")