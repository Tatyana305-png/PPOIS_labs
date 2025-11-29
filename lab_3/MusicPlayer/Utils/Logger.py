from datetime import datetime

class Logger:
    def __init__(self):
        self.log_file = "music_player.log"

    def log(self, message: str, level: str = "INFO"):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}\n"
        print(log_entry)
        try:
            with open(self.log_file, "a", encoding='utf-8') as f:
                f.write(log_entry)
        except UnicodeEncodeError:
            safe_message = message.encode('ascii', 'ignore').decode('ascii')
            log_entry = f"[{timestamp}] [{level}] {safe_message}\n"
            with open(self.log_file, "a", encoding='utf-8') as f:
                f.write(log_entry)