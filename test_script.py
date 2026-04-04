import traceback
from agent.graph import process_chat

try:
    process_chat("Met test.", {"hcp_name": "", "date": "", "product": "", "notes": "", "sentiment": "", "follow_up": ""})
    print("SUCCESS")
except BaseException as e:
    traceback.print_exc()
