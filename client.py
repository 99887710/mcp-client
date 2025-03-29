import asyncio
from mcp import ClientSession
from contextlib import AsyncExitStack

class MCPClient:
    def __init__(self):
        """Initialise MCP Client"""
        self.session =None
        self.exit_stack = AsyncExitStack()

    async def connect_to_mock_server(self):
        """Mock MCP server connection"""
        print("✅ MCP client initialised")

    async def chat_loop(self):
        """start chat loop"""
        print("\n📢 MCP client started, input 'quit' to exit! \n")

        while True:
            try:
                query = input("📝 input your question: ").strip()
                if query.lower() =='quit':
                    print("\n👋 exit chat...")
                    break

                response =f"🤖 [Mock Response] your question is：{query}"
                print(response)
            except Exception as e:
                print(f"\n⚠️ error happens:{str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    client = MCPClient()
    try:
        await client.connect_to_mock_server()
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    asyncio.run(main())