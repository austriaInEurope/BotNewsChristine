import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio

TOKEN = "8440806883:AAFswE9RyDdHYmTBPxKm36KtM8u6rqbgZlk"

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_news():
    url = "https://lenta.ru"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    links = soup.find_all("a")[:5]

    news = []
    for item in links:
        title = item.get_text(strip=True)
        link = item.get("href")

        if title and link:
            if not link.startswith("http"):
                link = "https://lenta.ru" + link
            news.append(f"{title}\n{link}")

    return news[:5]

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет 💛 Напиши тему: спорт / ИИ / крипта")

@dp.message(Command("update"))
async def update(message: types.Message):
    await message.answer("База новостей обновлена")

@dp.message()
async def send_news(message: types.Message):
    news = get_news()
    await message.answer("\n\n".join(news))

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())