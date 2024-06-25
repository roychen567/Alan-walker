#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) @AlbertEinsteinTG

import motor.motor_asyncio
from info import REQ_CHANNEL1, REQ_CHANNEL2

class JoinReqs:

    def __init__(self):
        from info import JOIN_REQS_DB
        if JOIN_REQS_DB:
            self.client = motor.motor_asyncio.AsyncIOMotorClient(JOIN_REQS_DB)
            self.db = self.client["JoinReqs"]
            self.col1 = self.db[str(REQ_CHANNEL1)]
            self.col2 = self.db[str(REQ_CHANNEL2)]
            self.chat_col1 = self.db["ChatId1"]
            self.chat_col2 = self.db["ChatId2"]
        else:
            self.client = None
            self.db = None
            self.col = None

    def isActive(self):
        if self.client is not None:
            return True
        else:
            return False

    ##############################################
    async def add_user1(self, user_id, first_name, username, date):
        try:
            await self.col1.insert_one({"_id": int(user_id),"user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
        except:
            pass

    async def get_user1(self, user_id):
        return await self.col1.find_one({"user_id": int(user_id)})

    async def get_all_users1(self):
        return await self.col1.find().to_list(None)

    async def delete_user1(self, user_id):
        await self.col1.delete_one({"user_id": int(user_id)})

    async def delete_all_users1(self):
        await self.col1.delete_many({})

    async def get_all_users_count1(self):
        return await self.col1.count_documents({})
   
    ##############################################
    async def add_user2(self, user_id, first_name, username, date):
        try:
            await self.col2.insert_one({"_id": int(user_id),"user_id": int(user_id), "first_name": first_name, "username": username, "date": date})
        except:
            pass

    async def get_user2(self, user_id):
        return await self.col2.find_one({"user_id": int(user_id)})

    async def get_all_users2(self):
        return await self.col2.find().to_list(None)

    async def delete_user2(self, user_id):
        await self.col2.delete_one({"user_id": int(user_id)})

    async def delete_all_users2(self):
        await self.col2.delete_many({})

    async def get_all_users_count2(self):
        return await self.col2.count_documents({})

    ##############################################
    async def add_fsub_chat1(self, chat_id):
        try:
            await self.chat_col1.delete_many({})
            await self.chat_col1.insert_one({"chat_id": chat_id})
        except:
            pass

    async def get_fsub_chat1(self):
        return await self.chat_col1.find_one({})

    async def delete_fsub_chat1(self, chat_id):
        await self.chat_col1.delete_one({"chat_id": chat_id})

    ##############################################
    async def add_fsub_chat2(self, chat_id):
        try:
            await self.chat_col2.delete_many({})
            await self.chat_col2.insert_one({"chat_id": chat_id})
        except:
            pass

    async def get_fsub_chat2(self):
        return await self.chat_col2.find_one({})

    async def delete_fsub_chat2(self, chat_id):
        await self.chat_col2.delete_one({"chat_id": chat_id})
    ##############################################
