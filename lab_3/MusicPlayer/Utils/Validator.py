class Validator:
    def validate_email(email: str) -> bool:
        if not email or not isinstance(email, str):
            return False
        email = email.strip()
        return "@" in email and "." in email and len(email) > 3

    def validate_audio_file(file_path: str) -> bool:
        if not file_path or not isinstance(file_path, str):
            return False
        supported_formats = ('.mp3', '.wav', '.flac', '.aac')
        return file_path.lower().endswith(supported_formats)

    def validate_playlist_name(name: str) -> bool:
        if not name or not isinstance(name, str):
            return False
        name_stripped = name.strip()
        return len(name_stripped) >= 1 and len(name_stripped) <= 100