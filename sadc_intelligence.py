import os

def send_to_bridge(number, message):
    pipe_path = "/data/data/com.termux/files/usr/tmp/imperial_pipe"
    payload = f"{number}|{message}"
    try:
        with open(pipe_path, "w") as pipe:
            pipe.write(payload)
        print(f"Successfully pushed to Imperial Pipe: {number}")
    except Exception as e:
        print(f"Pipe Failure: {e}")

# Example usage for your SADC report
if __name__ == "__main__":
    # Your trade intelligence logic here...
    report = "SADC Intelligence: Trade Volume Verified - Lithium/Gold Status: 55/55"
    send_to_bridge("27794658481", report)
