import asyncio

from src.components.app import App


async def main() -> None:
    app = App()

    query = "iphones that have good battery life"

    print("\n========================")
    print("USER QUERY:", query)
    print("========================\n")

    result = await app.run(query)

    print("\n========================")
    print("FINAL RESULT")
    print("========================\n")

    print(result)


if __name__ == "__main__":
    asyncio.run(main())