class Formatter:
    def format_duration(seconds: float) -> str:
        # Обработка отрицательного времени
        is_negative = seconds < 0
        seconds = abs(seconds)

        minutes = int(seconds // 60)
        seconds = int(seconds % 60)

        result = f"{minutes:02d}:{seconds:02d}"
        if is_negative:
            result = "-" + result
        return result

    def format_file_size(bytes: int) -> str:
        # Обработка отрицательного размера
        is_negative = bytes < 0
        bytes = abs(bytes)

        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes < 1024.0:
                result = f"{bytes:.1f} {unit}"
                if is_negative:
                    result = "-" + result
                return result
            bytes /= 1024.0
        result = f"{bytes:.1f} TB"
        if is_negative:
            result = "-" + result
        return result