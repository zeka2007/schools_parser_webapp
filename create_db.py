import asyncio
from db import init_models, diary, virtual_diary, student, mark, lesson

def db_init_models():
    asyncio.run(init_models())
    print("Done")


if __name__ == "__main__":
    db_init_models()