class GoogleScope:
    BASE_URL = "https://www.googleapis.com/auth"

    def __class_getitem__(cls, key: str) -> str:
        return f"{cls.BASE_URL}/{key}"
