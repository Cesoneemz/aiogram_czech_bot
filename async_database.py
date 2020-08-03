import asyncio
import asyncpg


class AsyncDataBase(object):

    @classmethod
    async def connect(cls):
        self = AsyncDataBase()
        self.pool = await asyncpg.create_pool(host='localhost', user='postgres', database='users')
        return self

    def conn(func):
        async def decorator(self, *args, **kwargs):
            async with self.pool.acquire() as conn:
                async with conn.transaction():
                    return await func(self, conn=conn, *args, **kwargs)

        return decorator

    @conn
    async def async_get_user(self, conn, user_id):
        return bool(await conn.fetchrow('SELECT * FROM users WHERE user_id = $1', user_id))

    @conn
    async def async_get_words_count(self, conn):
        return str(await conn.fetchval('SELECT COUNT(*) FROM words'))

    @conn
    async def async_get_word(self, conn, word):
        return bool(await conn.fetchrow('SELECT * FROM words WHERE word = $1', word))

    @conn
    async def async_add_user_to_database(self, conn, user_id):
        await conn.execute('INSERT INTO users (user_id) VALUES ($1);', user_id)

    @conn
    async def async_add_new_word(self, conn, category, word, translate, user_id):
        await conn.execute('INSERT INTO words (category, word, translate, user_id) VALUES ($1, $2, $3, $4);',
                           category, word, translate, user_id)

    @conn
    async def async_testing_easy_difficult(self, conn, category='all'):
        if category == 'all':
            return await conn.fetch('SELECT (word, translate) FROM words ORDER by random() LIMIT 4')
        else:
            return await conn.fetch('SELECT (word, translate) FROM words WHERE category = $1 ORDER BY random() LIMIT 4',
                                    category)

    @conn
    async def async_testing_hard_difficult(self, conn, category='all'):
        if category == 'all':
            return await conn.fetchval('SELECT (word, translate) FROM words ORDER by random() LIMIT 1')
        else:
            return await conn.fetchval('SELECT (word, translate) FROM words WHERE category = $1 ORDER BY random() '
                                       'LIMIT 1',
                                       category)


loop = asyncio.get_event_loop()
db = loop.run_until_complete(AsyncDataBase.connect())
