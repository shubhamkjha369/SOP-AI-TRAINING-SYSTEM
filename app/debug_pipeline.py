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
    text = "How to reset password: Step 1: Click forgot password. Step 2: Enter email. Step 3: Check email for link. Step 4: Enter new password."

    print("Running pipeline on dummy file...")
    res = run_pipeline(MockFile(text))
    print("\nFINAL PIPELINE JSON RESULT:")
    print(json.dumps(res, indent=2))
except Exception as e:
    print("FATAL ERROR:")
    traceback.print_exc()
