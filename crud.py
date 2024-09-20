from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from models import *
from schemas import *
from datetime import datetime
from typing import List
# CRUD cho Keyword

async def create_keyword(db: AsyncSession, keyword_name: str):
        try:
            async with db.begin():
                new_keyword = Keyword(keyword_name=keyword_name)
                db.add(new_keyword)
                await db.commit()
                return KeywordResponse.model_validate(new_keyword)
        except IntegrityError:
            await db.rollback()
            raise ValueError(f"Keyword '{keyword_name}' already exists")
        
async def create_list_keywords(db: AsyncSession, keywords: List[KeywordBase]):
    created_keywords = []
    try:
        async with db.begin():
            for keyword_data in keywords:
                new_keyword = Keyword(keyword_name=keyword_data.keyword_name)
                db.add(new_keyword)
                created_keywords.append(new_keyword)
            await db.commit()
        return created_keywords
    except IntegrityError:
        await db.rollback()
        raise HTTPException(status_code=400, detail="One or more keywords already exist")


async def get_keyword(db: AsyncSession, keyword_id: int):
    async with db.begin():
        result = await db.execute(select(Keyword).filter(Keyword.keyword_id == keyword_id))
        keyword = result.scalars().first()
        if keyword:
            await db.refresh(keyword)
        return KeywordResponse.model_validate(keyword)
    
async def get_all_keywords(db: AsyncSession):
    async with db.begin():
        result = await db.execute(select(Keyword))
        keywords = result.scalars().all()
        return keywords
    
async def update_keyword(db: AsyncSession, keyword_id: int, keyword_name: str):
    async with db.begin():
        result = await db.execute(select(Keyword).filter(Keyword.keyword_id == keyword_id))
        keyword = result.scalars().first()
        if keyword:
            keyword.keyword_name = keyword_name
            await db.flush()
        return KeywordResponse.model_validate(keyword)

async def delete_keyword(db: AsyncSession, keyword_id: int):
    async with db.begin():
        result = await db.execute(select(Keyword).filter(Keyword.keyword_id == keyword_id))
        keyword = result.scalars().first()
        if keyword:
            await db.delete(keyword)
            await db.flush()
        return KeywordResponse.model_validate(keyword)

# CRUD cho KeywordSearchVolume

async def create_keyword_search_volume(db: AsyncSession, keyword_id: int, created_datetime: datetime, search_volume: int):
    async with db.begin():
        search_volume_record = KeywordSearchVolume(
            keyword_id=keyword_id,
            created_datetime=created_datetime,
            search_volume=search_volume
        )
        db.add(search_volume_record)
        await db.flush()
        return KeywordSearchVolumeResponse.model_validate(search_volume_record)

async def get_keyword_search_volume(db: AsyncSession, keyword_id: int, start_time: datetime, end_time: datetime):
    async with db.begin():
        result = await db.execute(
            select(KeywordSearchVolume)
            .filter(KeywordSearchVolume.keyword_id == keyword_id)
            .filter(KeywordSearchVolume.created_datetime.between(start_time, end_time))
        )
        search_volumes = result.scalars().all()
        if len(search_volumes) == 0:
            return []
        return [KeywordSearchVolumeResponse.model_validate(volume) for volume in search_volumes]


async def update_keyword_search_volume(db: AsyncSession, keyword_id: int, created_datetime: datetime, search_volume: int):
    async with db.begin():
        result = await db.execute(select(KeywordSearchVolume).filter(
            KeywordSearchVolume.keyword_id == keyword_id,
            KeywordSearchVolume.created_datetime == created_datetime
        ))
        search_volume_record = result.scalars().first()
        if search_volume_record:
            search_volume_record.search_volume = search_volume
            await db.flush()
        return KeywordSearchVolumeResponse.model_validate(search_volume_record)

async def delete_keyword_search_volume(db: AsyncSession, keyword_id: int, created_datetime: datetime):
    async with db.begin():
        result = await db.execute(select(KeywordSearchVolume).filter(
            KeywordSearchVolume.keyword_id == keyword_id,
            KeywordSearchVolume.created_datetime == created_datetime
        ))
        search_volume_record = result.scalars().first()
        if search_volume_record:
            await db.delete(search_volume_record)
            await db.flush()
        return KeywordSearchVolumeResponse.model_validate(search_volume_record)

# CRUD cho UserSubscription

async def create_user_subscription(db: AsyncSession, user_id: int, keyword_id: int,timing:str, start_time: datetime, end_time: datetime):
    async with db.begin():
        subscription = UserSubscription(
            user_id=user_id,
            keyword_id=keyword_id,
            timing = timing,
            subscription_start=start_time,
            subscription_end=end_time
        )
        db.add(subscription)
        await db.flush()
        return SubscriptionResponse.model_validate(subscription)

async def get_user_subscription(db: AsyncSession, user_id: int, keyword_id: int):
    async with db.begin():
        result = await db.execute(
            select(UserSubscription).filter(
                UserSubscription.user_id == user_id,
                UserSubscription.keyword_id == keyword_id
            )
        )
        subscription = result.scalars().first()
        return SubscriptionResponse.model_validate(subscription)

async def get_user_subscriptions(db: AsyncSession, user_id: int):
    async with db.begin():
        result = await db.execute(select(UserSubscription).filter(UserSubscription.user_id == user_id))
        subscriptions = result.scalars().all()
        if len(subscriptions) == 0:
            return []
        return [SubscriptionResponse.model_validate(item) for item in subscriptions]

async def update_user_subscription(db: AsyncSession, user_id: int, keyword_id: int, timing: str, start_time: datetime, end_time: datetime):
    async with db.begin():
        result = await db.execute(
            select(UserSubscription).filter(
                UserSubscription.user_id == user_id,
                UserSubscription.keyword_id == keyword_id
            )
        )
        subscription = result.scalars().first()
        if subscription:
            subscription.timing = timing
            subscription.subscription_start = start_time
            subscription.subscription_end = end_time
            await db.flush()
        return SubscriptionResponse.model_validate(subscription)

async def delete_user_subscription(db: AsyncSession, user_id: int, keyword_id: int):
    async with db.begin():
        result = await db.execute(
            select(UserSubscription).filter(
                UserSubscription.user_id == user_id,
                UserSubscription.keyword_id == keyword_id
            )
        )
        subscription = result.scalars().first()
        if subscription:
            await db.delete(subscription)
            await db.flush()
        return SubscriptionResponse.model_validate(subscription)


async def get_user_keyword_subscriptions_list(db: AsyncSession, 
                                            userId: int,
                                            keyword_name: str,
                                            timing: str,
                                            start_date: datetime,
                                            end_date: datetime):
    async with db.begin():
        results = await db.execute(
            select(KeywordSearchVolume.created_datetime, Keyword.keyword_name, KeywordSearchVolume.search_volume)\
            .join(Keyword, Keyword.keyword_id == KeywordSearchVolume.keyword_id)\
            .join(UserSubscription, UserSubscription.keyword_id == Keyword.keyword_id)\
            .filter(UserSubscription.user_id == userId)
            .filter(UserSubscription.timing == timing)\
            .filter(Keyword.keyword_name == keyword_name)\
            .filter(KeywordSearchVolume.created_datetime.between(start_date, end_date))\
        )
    
        search_volumes = results.fetchall()
        if len(search_volumes) == 0:
            raise HTTPException(status_code=404, detail="No search volumes found for the specified parameters.")
        return [UserSubscriptionKeyWordResponse(
                    time = item.created_datetime.strftime("%d/%m/%Y"),  # Convert datetime and hour to string
                    keyword_name = item.keyword_name,
                    search_volume = item.search_volume
                    ) for item in search_volumes
                ]