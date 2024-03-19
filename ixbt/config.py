from get_user_agent import get_random_user_agent
from datetime import datetime

URL_IXBT = "https://www.ixbt.com/news/?show=tape"

KEYWORDS = [
    "AMOLED", "iPhone", "Huawei", "OnePlus", "Oppo", "Realme", "Vivo", "Motorola", "Nokia",
    "Sony Xperia", "Google Pixel", "ASUS Zenfone", "ZTE", "Honor", "BlackBerry",
    "HTC", "LG", "Meizu", "Alcatel", "Tecno", "Infinix", "Micromax", "Lenovo",
    "Razor Phone", "Fairphone", "Palm", "Vsmart", "Sharp", "Kyocera", "Panasonic",
    "Turing", "Poco", "Nubia", "Red Magic", "ROG Phone", "Cat Phones", "Ulefone",
    "dual SIM", "eSIM", "USB Type-C", "Doogee", "Blackview", "AGM", "Energizer",
    "Poco", "Nubia", "IP68","NFC", "смартфон", "AI camera"
    ]

HEADERS = {
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    "user-agent": get_random_user_agent()
}

BOT_TOKEN = '6230573565:AAGro7qOktJvU_4hzvIFazZkT9UUDug1r8g'
CHANNEL_ID = '@texm_by'

# KEYWORDS = ["Audi", "Ford", "Great Wall", "Changan", "Chery", "Chevrolet", "GAC", "Geely", "Hyundai", "Honda",
#             "Lada", "Land Rover", "Lexus", "Lynk & Co", "Mercedes", "Peugeot", "Porsche",
#             "Suzuki", "Toyota", "Subaru", "Skoda", "Volkswagen", "Tesla", "кроссовер", "Нива"]