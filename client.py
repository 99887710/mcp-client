import asyncio
import os
from openai import OpenAI
from mcp import ClientSession
from contextlib import AsyncExitStack
from dotenv import load_dotenv


load_dotenv()

class MCPClient:
    def __init__(self):
        """Initialise MCP Client"""
        self.session =None
        self.exit_stack = AsyncExitStack()
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        self.base_url = os.getenv("BASE_URL")
        self.model = os.getenv("MODEL")

        self.client = OpenAI(
            base_url = 'http://localhost:11434/v1',
            api_key='ollama', # required, but unused
        )
                    
        if not self.openai_api_key:
                    raise ValueError("❌ OpenAI API Key not found")

    async def process_query(self, query: str) -> str:
        """invoke OpenAI API to process user input"""
        messages = [{"role": "system", "content": "you are Ai assitant to help users answer their questions"},
                    {"role": "user", "content": query}]
                
        try:
            response =await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=messages
                )
                )
            return response.choices[0].message.content
        except Exception as e:
            return f"⚠️ error invoking OpenAI API:{str(e)}"

    # async def connect_to_mock_server(self):
    #     """Mock MCP server connection"""
    #     print("✅ MCP client initialised")


    async def chat_loop(self):
        """start chat loop"""
        print("\n📢 MCP client started, input 'quit' to exit! \n")

        while True:
            try:
                query = input("📝 input your question: ").strip()
                if query.lower() =='quit':
                    print("\n👋 exit chat...")
                    break

                # response =f"🤖 [Mock Response] your question is：{query}"
                response = await self.process_query(query)

                print(response)
            except Exception as e:
                print(f"\n⚠️ error happens:{str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        # await client.connect_to_mock_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())