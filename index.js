const TelegramBot = require('node-telegram-bot-api');
const axios = require('axios');

const token = process.env.TELEGRAM_TOKEN;
const bot = new TelegramBot(token, { polling: true });

let currentCoefficient = null;

async function updateCoefficient() {
  try {
    const response = await axios.get('https://drgns8.casino/srv/api/v1/crash/state');
    const data = response.data;

    if (data && data.game_state === 'crashed') {
      currentCoefficient = data.coef;
    } else {
      currentCoefficient = null;
    }
  } catch (error) {
    console.error('Ошибка при получении коэффициента:', error.message);
  }
}

setInterval(updateCoefficient, 5000);

bot.onText(/\/коэффициент/, (msg) => {
  const text = currentCoefficient
    ? `Последний коэффициент: ${currentCoefficient}x`
    : 'Коэффициент пока недоступен.';
  bot.sendMessage(msg.chat.id, text);
});

bot.onText(/\/прогноз/, (msg) => {
  const prediction = Math.random() < 0.5 ? 'Будет выше 2x' : 'Будет меньше 2x';
  bot.sendMessage(msg.chat.id, `Прогноз: ${prediction}`);
});

console.log('Бот запущен...');
