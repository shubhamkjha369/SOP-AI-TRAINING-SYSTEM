import sys
import json
import traceback

from pipeline import run_pipeline

class MockFile:
    def __init__(self, content):
        self.content = content
        self.type = "text/plain"
        self.pointer = 0
        self.name = "sample_sop.txt"
    def read(self):
        return self.content.encode("utf-8")
    def seek(self, pos):
        self.pointer = pos

try:
    with open(r"C:\Users\SAM\.gemini\antigravity\brain\d6144864-0ea7-4252-9515-825a217305a6\sample_sop.txt", "r", encoding="utf-8") as f:
        text = f.read()

    print("Running pipeline on dummy file...")
    res = run_pipeline(MockFile(text))
    print("\nFINAL PIPELINE JSON RESULT:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print("FATAL ERROR:")
    traceback.print_exc()
