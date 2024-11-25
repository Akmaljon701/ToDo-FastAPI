import redis.asyncio as redis
from app import config


async def get_redis():
    return await redis.from_url(
        config.REDIS_URL,
        encoding="utf-8",
        decode_responses=True,
    )


async def get_cache():
    return await redis.from_url(
        config.REDIS_URL,
        decode_responses=False,
    )

# redis = await get_redis()
#
# await redis.set("key", "value")
# print("Ma'lumot saqlandi!")
#
# value = await redis.get("key")
# print(f"Saqlangan qiymat: {value}")
#
# await redis.delete("key")
# print("Ma'lumot o'chirildi!")
