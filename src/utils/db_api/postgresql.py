from datetime import datetime, timedelta
from typing import Union
import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool
from src.data import config
class Database:

    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME
        )

    async def execute(self, command, *args,
                      fetch: bool = False,
                      fetchval: bool = False,
                      fetchrow: bool = False,
                      execute: bool = False
                      ):
        result = None
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username VARCHAR(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE,
        gender   VARCHAR(10) NULL,
        interests VARCHAR(255) NULL,
        age_group VARCHAR(20) NULL,
        status BOOLEAN DEFAULT FALSE,
        current_state VARCHAR(255) NULL,
        invited_users INTEGER DEFAULT 0,
        premium_expiration TIMESTAMPTZ DEFAULT NULL,
        created_at TIMESTAMPTZ DEFAULT NOW()
        );
        """
        await self.execute(sql, execute=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num}" for num, item in enumerate(parameters.keys(),
                                                          start=1)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO Users (full_name, username, telegram_id, created_at) VALUES($1, $2, $3, $4) returning *"
        created_at = datetime.now()
        return await self.execute(sql, full_name, username, telegram_id, created_at, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_all_ids(self):
        sql = "SELECT telegram_id FROM Users"
        return await self.execute(sql, fetch=True)


    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE TRUE"
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def select_user_telegram_id(self, telegram_id):
        sql = "SELECT * FROM Users WHERE telegram_id = $1"
        params = telegram_id

        return await self.execute(sql, params, fetchrow=True)

    async def update_user_premium_status(self, telegram_id, status):
        sql = "UPDATE Users SET status = $1 WHERE telegram_id = $2"
        await self.execute(sql, status, telegram_id, execute=True)

    async def get_user_premium_status(self, telegram_id):
        sql = "SELECT status FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def update_user_invited_users(self, telegram_id):
        sql = "UPDATE Users SET invited_users = invited_users + 1 WHERE telegram_id = $1"
        await self.execute(sql, telegram_id, execute=True)

    async def update_user_premium_expiration(self, telegram_id, expiration_time):
        sql = "UPDATE Users SET premium_expiration = $1 WHERE telegram_id = $2"
        await self.execute(sql, expiration_time, telegram_id, execute=True)

    async def get_invited_users_count(self, telegram_id):
        sql = "SELECT invited_users FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def get_user_premium_expiration(self, telegram_id):
        sql = "SELECT premium_expiration FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def count_new_users(self):
        current_time = datetime.now()
        start_time = current_time - timedelta(hours=24)
        sql = "SELECT COUNT(*) FROM Users WHERE created_at > $1"
        return await self.execute(sql, start_time, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def update_user_gender(self, gender, telegram_id):
        sql = "UPDATE Users SET gender=$1 WHERE telegram_id=$2"
        return await self.execute(sql, gender, telegram_id, execute=True)

    async def count_men(self):
        sql = "SELECT COUNT(*) FROM Users WHERE gender = 'man'"
        return await self.execute(sql, fetchval=True)

    async def count_women(self):
        sql = "SELECT COUNT(*) FROM Users WHERE gender = 'woman'"
        return await self.execute(sql, fetchval=True)

    async def get_female_users(self):
        sql = "SELECT * FROM Users WHERE gender='woman'"
        return await self.execute(sql, fetch=True)

    async def get_male_users(self):
        sql = "SELECT * FROM Users WHERE gender='man'"
        return await self.execute(sql, fetch=True)
    async def update_user_interests(self, interests, telegram_id):
        sql = "UPDATE Users SET interests=$1 WHERE telegram_id=$2"
        return await self.execute(sql, interests, telegram_id, execute=True)

    # async def clear_user_interests(self, telegram_id):
    #     sql = "UPDATE Users SET interests=NULL WHERE telegram_id=$1"
    #     return await self.execute(sql, telegram_id, execute=True)

    async def update_user_age_group(self, age_group, telegram_id):
        sql = "UPDATE Users SET age_group=$1 WHERE telegram_id=$2"
        return await self.execute(sql, age_group, telegram_id, execute=True)

    async def get_user_gender(self, telegram_id):
        sql = "SELECT gender FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def get_user_interests(self, telegram_id):
        sql = "SELECT interests FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def get_user_age_group(self, telegram_id):
        sql = "SELECT age_group FROM Users WHERE telegram_id = $1"
        return await self.execute(sql, telegram_id, fetchval=True)

    async def check_current_state(self, telegram_id):
        sql = """
        SELECT current_state
        FROM Users
        WHERE telegram_id = $1;
        """
        record = await self.execute(sql, telegram_id, fetchval=True)
        return record

    async def update_user_current_state(self, telegram_id, current_state):
        sql = """
        UPDATE Users
        SET current_state = $1
        WHERE telegram_id = $2;
        """
        await self.execute(sql, current_state, telegram_id, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)

# TABLE Conversations

    async def create_conversation(self):
        sql = """
        CREATE TABLE IF NOT EXISTS conversations (
            user_id BIGINT PRIMARY KEY,
            companion_id BIGINT
        );
        """
        await self.execute(sql, execute=True)

    async def get_companion_id(self, user_id):
        async with self.pool.acquire() as connection:
            sql = """
            SELECT companion_id
            FROM conversations
            WHERE user_id = $1
              AND user_id NOT IN (SELECT companion_id FROM conversations WHERE companion_id = $1);
            """
            row = await connection.fetchrow(sql, user_id)

        if row:
            return row["companion_id"]
        else:
            return None

    async def add_user_to_conversations(self, user_id):
        async with self.pool.acquire() as connection:
            sql = "INSERT INTO conversations (user_id) VALUES ($1);"
            await connection.execute(sql, user_id)

    async def get_available_companion_id(self, user_id):
        async with self.pool.acquire() as connection:
            sql = """
            SELECT user_id
            FROM conversations
            WHERE user_id != $1
              AND companion_id IS NULL
              AND user_id NOT IN (
                  SELECT companion_id FROM conversations WHERE companion_id IS NOT NULL
              )
              AND user_id NOT IN (
                  SELECT companion_id FROM conversations WHERE user_id = $1
              )
            LIMIT 1;
            """
            row = await connection.fetchrow(sql, user_id)
        if row:
            return row["user_id"]
        else:
            return None

    async def is_in_conversation(self, user_id):
        async with self.pool.acquire() as connection:
            sql = "SELECT user_id FROM conversations WHERE (user_id = $1 OR companion_id = $1) AND companion_id IS NOT NULL;"
            row = await connection.fetchrow(sql, user_id)

        if row:
            return True
        else:
            return False

    async def remove_user_from_conversations(self, user_id):
        async with self.pool.acquire() as connection:
            sql = """
            DELETE FROM conversations 
            WHERE user_id = $1 
               OR companion_id = $1;
            """
            await connection.execute(sql, user_id)

    async def set_companion_id(self, user_id, companion_id):
        async with self.pool.acquire() as connection:
            sql = "UPDATE conversations SET companion_id = $1 WHERE user_id = $2;"
            await connection.execute(sql, companion_id, user_id)

    async def get_chat_info(self, chat_id):
        async with self.pool.acquire() as connection:
            sql = "SELECT * FROM conversations WHERE user_id = $1 OR companion_id = $1;"
            row = await connection.fetchrow(sql, chat_id)
            if row:
                return dict(row)
            else:
                return None

    async def drop_conversations(self):
        await self.execute("DROP TABLE conversations", execute=True)





