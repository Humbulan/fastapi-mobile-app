import json
import sys

def sanitize_payload(raw_input):
    try:
        # Check if input is coming from command line argument
        data = json.loads(raw_input)
        return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": "Invalid JSON Input", "details": str(e)})

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Process the argument passed in the terminal
        print(sanitize_payload(sys.argv[1]))
    else:
        # Fallback for testing
        sample = {"village": "Thohoyandou", "status": "active"}
        print(json.dumps(sample, indent=2))
