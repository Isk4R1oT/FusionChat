import os
from backend.services.llm import MistralLLM
from backend.services.stock_quotes import StockQuoteService
from langchain.agents import Tool, initialize_agent
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from langchain_community.utilities import DuckDuckGoSearchAPIWrapper


load_dotenv()


def calculator(query: str) -> str:
    """
    Простой калькулятор для вычисления математических выражений.
    """
    try:
        result = eval(query, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Ошибка при вычислении: {e}"


search_client = DuckDuckGoSearchAPIWrapper()


def search_dds(query: str) -> str:
    """
    Поиск информации через DuckDuckGo.
    """
    try:
        return search_client.run(query)
    except Exception as e:
        return f"Ошибка при поиске: {e}"


class ChatBot:
    def __init__(self, api_key: str = None):

        if api_key is None:
            api_key = os.getenv("MISTRAL_API_KEY")
        if not api_key:
            raise ValueError("API ключ не предоставлен")

        self.stock_service = StockQuoteService()

        system_prompt = """
        Ты — опытный, дружелюбный инвестиционный консультант. 
        Твои ответы должны быть подробными, понятными и наполненными аналитикой, прогнозами и сравнительным анализом. 
        Объясняй сложные концепции простым языком и используй живой, разговорный стиль. 
        Если необходимо, задавай уточняющие вопросы для лучшего понимания запроса.
        """

        self.llm = MistralLLM(
            api_key=api_key,
            temperature=0.6,
            system_prompt=system_prompt
        )

        stock_quote_tool = Tool(
            name="Stock Quote Lookup",
            func=self.stock_service.get_stock_quote,
            description=(
                "Используй этот инструмент для получения текущей котировки акции по заданному тикеру. "
                "При необходимости, добавь свои комментарии и аналитические замечания о движении цены."
            )
        )

        stock_news_tool = Tool(
            name="Stock News Lookup",
            func=self.stock_service.get_stock_news,
            description=(
                "Используй этот инструмент для получения последних новостей, связанных с заданным тикером. "
                "Если необходимо, предоставь свой анализ и комментарии к новостям."
            )
        )

        stock_info_tool = Tool(
            name="Stock Info Lookup",
            func=self.stock_service.get_stock_info,
            description=(
                "Используй этот инструмент для получения общей информации о компании по заданному тикеру. "
                "Если уместно, сравни компанию с другими или добавь аналитические комментарии."
            )
        )

        calculator_tool = Tool(
            name="Calculator",
            func=calculator,
            description="Используй этот инструмент для вычисления математических выражений. Например: '2+2*3'."
        )

        search_dds_tool = Tool(
            name="DuckDuckGo Search",
            func=search_dds,
            description="Используй этот инструмент для поиска информации в интернете по заданному запросу. Например: 'последние новости о Tesla'."
        )

        self.agent = initialize_agent(
            tools=[
                stock_quote_tool,
                stock_news_tool,
                stock_info_tool,
                calculator_tool,
                search_dds_tool
            ],
            llm=self.llm,
            agent="chat-conversational-react-description",
            memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True),
            verbose=True
        )

    def process_query(self, query: str) -> str:
        return self.agent.run(input=query)