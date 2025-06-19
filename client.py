import asyncio
from fastmcp import Client

async def main():
    client = Client("http://localhost:8000/mcp")
    async with client:
        resp = await client.call_tool("store_memory", {
            "text": "I am strudying B tech on computer science at SMVITM Bantakal.",
            "id": "2",
            "metadata": {"tag": "education", "company": "SMVITM"}
        })
        print(resp)

        # resp2 = await client.call_tool("recall", {
        #     "query": "What did I build for Alatree?",
        #     "k": 2
        # })
        # print("Recall:", resp2)

if __name__ == "__main__":
    asyncio.run(main())
