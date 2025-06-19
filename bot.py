import os
import asyncio
from telegram import Bot
from dotenv import load_dotenv
from playwright.async_api import async_playwright
from sklearn.linear_model import LinearRegression
import numpy as np

load_dotenv()
bot = Bot(token=os.getenv("BOT_TOKEN"))
chat_id = os.getenv("CHAT_ID")
history = []

async def send_message(text):
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки: {e}")

def predict_next(data):
    if len(data) < 5:
        return "Недостаточно данных для прогноза."
    X = np.array(range(len(data))).reshape(-1, 1)
    y = np.array(data)
    model = LinearRegression().fit(X, y)
    next_x = np.array([[len(data)]])
    pred = model.predict(next_x)[0]
    return f"Прогноз следующего X: {pred:.2f}"

async def run():
    await send_message("🤖 Бот запущен. Ожидаю коэффициенты...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto("https://drgns8.casino/casino/game/crash")

        await page.wait_for_timeout(5000)  # подождем прогрузку

        while True:
            try:
                # Измените селектор на тот, который показывает текущий x (нужно уточнить вручную)
                x_elem = await page.query_selector(".game-info .multiplier")
                if x_elem:
                    x_text = await x_elem.inner_text()
                    if "x" in x_text:
                        value = float(x_text.replace("x", "").strip())
                        if not history or history[-1] != value:
                            history.append(value)
                            await send_message(f"🟢 Новый X: {value}")
                            pred = predict_next(history)
                            await send_message(pred)
                await asyncio.sleep(3)
            except Exception as e:
                print("Ошибка парсинга:", e)
                await asyncio.sleep(5)

asyncio.run(run())
