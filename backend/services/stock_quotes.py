import time
import yfinance as yf


class StockQuoteService:
    def get_stock_quote(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            time.sleep(1)  # задержка в 1 секунду
            if data.empty:
                return f"Нет данных по тикеру {ticker}."
            price = data['Close'].iloc[-1]
            return f"Текущая цена акции {ticker}: {price:.2f} USD"
        except Exception as e:
            return f"Ошибка при получении котировки для {ticker}: {str(e)}"

    def get_stock_news(self, ticker: str, max_articles: int = 3) -> str:
        try:
            stock = yf.Ticker(ticker)

            news_items = stock.get_news()
            time.sleep(1)

            if not news_items:
                return f"Нет последних новостей для {ticker}."

            return news_items
        except Exception as e:
            return f"Ошибка при получении новостей для {ticker}: {str(e)}"

    def get_stock_info(self, ticker: str) -> str:
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            time.sleep(1)

            if not info:
                return f"Нет информации по тикеру {ticker}."
            company_name = info.get("longName", "Неизвестно")
            sector = info.get("sector", "Неизвестно")
            return f"Тикер {ticker} представляет компанию {company_name}, сектор: {sector}."
        except Exception as e:
            return f"Ошибка при получении информации для {ticker}: {str(e)}"