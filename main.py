from fastapi import FastAPI, HTTPException, Depends,status
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session
from crud import *
from schemas import *
from typing import List
from datetime import datetime,timedelta
from fastapi.security import OAuth2PasswordRequestForm
from oauth2 import *

app = FastAPI()

async def get_db():
    async with async_session() as session:
        yield session


@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}




@app.post("/keywords/", response_model=KeywordResponse,summary="Create 1 keyword")
async def create_keyword_endpoint(keyword: KeywordBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    return await create_keyword(db, keyword.keyword_name)


@app.post("/create-list-keywords", response_model=List[KeywordResponse],summary="Create list keywords")
async def create_keywords_endpoint(keywords: List[KeywordBase], db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    created_keywords = await create_list_keywords(db, keywords)
    return created_keywords

@app.get("/keywords/{keyword_id}", response_model=KeywordResponse)
async def read_keyword_endpoint(keyword_id: int, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_keyword = await get_keyword(db, keyword_id)
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@app.get("/get-all-keywords/", response_model=List[KeywordResponse],summary="Get all keywords")
async def read_keywords(db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    try:
        keywords = await get_all_keywords(db)
        return keywords
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/keywords/{keyword_id}", response_model=KeywordResponse)
async def update_keyword_endpoint(keyword_id: int, keyword: KeywordBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_keyword = await update_keyword(db, keyword_id, keyword.keyword_name)
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@app.delete("/keywords/{keyword_id}", response_model=KeywordResponse)
async def delete_keyword_endpoint(keyword_id: int, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_keyword = await delete_keyword(db, keyword_id)
    if db_keyword is None:
        raise HTTPException(status_code=404, detail="Keyword not found")
    return db_keyword

@app.post("/keyword_search_volume/", response_model=KeywordSearchVolumeResponse)
async def create_keyword_search_volume_endpoint(keyword_id: int, volume: KeywordSearchVolumeBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    return await create_keyword_search_volume(db, keyword_id, volume.created_datetime, volume.search_volume)

@app.get("/keyword_search_volume/{keyword_id}", response_model=List[KeywordSearchVolumeResponse])
async def get_keyword_search_volume_endpoint(keyword_id: int, start_time: datetime, end_time: datetime, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    search_volumes = await get_keyword_search_volume(db, keyword_id, start_time, end_time)
    return search_volumes

@app.put("/keyword_search_volume/", response_model=KeywordSearchVolumeResponse)
async def update_keyword_search_volume_endpoint(keyword_id: int, volume: KeywordSearchVolumeBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_volume = await update_keyword_search_volume(db, keyword_id, volume.created_datetime, volume.search_volume)
    if db_volume is None:
        raise HTTPException(status_code=404, detail="Search volume record not found")
    return db_volume

@app.delete("/keyword_search_volume/", response_model=KeywordSearchVolumeResponse)
async def delete_keyword_search_volume_endpoint(keyword_id: int, created_datetime: datetime, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    db_volume = await delete_keyword_search_volume(db, keyword_id, created_datetime)
    if db_volume is None:
        raise HTTPException(status_code=404, detail="Search volume record not found")
    return db_volume

@app.post("/user_subscription/", response_model=SubscriptionResponse)
async def create_user_subscription_endpoint(subscription: SubscriptionBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):

    return await create_user_subscription(
        db,
        subscription.user_id,
        subscription.keyword_id,
        subscription.timing,
        subscription.subscription_start,
        subscription.subscription_end
    )

@app.get("/user_subscription/{user_id}/{keyword_id}", response_model=SubscriptionResponse)
async def get_user_subscription_endpoint(user_id: int, keyword_id: int, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    subscription = await get_user_subscription(db, user_id, keyword_id)
    if subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

@app.get("/user_subscriptions/{user_id}", response_model=List[SubscriptionResponse])
async def get_user_subscriptions_endpoint(user_id: int, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    subscriptions = await get_user_subscriptions(db, user_id)
    return subscriptions

@app.put("/user_subscription/", response_model=SubscriptionResponse)
async def update_user_subscription_endpoint(subscription: SubscriptionBase, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    updated_subscription = await update_user_subscription(
        db,
        subscription.user_id,
        subscription.keyword_id,
        subscription.timing,
        subscription.subscription_start,
        subscription.subscription_end
    )
    if updated_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return updated_subscription

@app.delete("/user_subscription/{user_id}/{keyword_id}", response_model=SubscriptionResponse)
async def delete_user_subscription_endpoint(user_id: int, keyword_id: int, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    deleted_subscription = await delete_user_subscription(db, user_id, keyword_id)
    if deleted_subscription is None:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return deleted_subscription


@app.get("/user_subscriptions_list/{user_id}", response_model=List[SubscriptionResponse])
async def get_user_subscriptions_endpoint(user_id: int, db: AsyncSession = Depends(get_db),current_user: User = Depends(get_current_user)):
    subscriptions = await get_user_subscriptions(db, user_id)
    return subscriptions

@app.get("/user_keyword_subscriptions_list/", response_model=List[UserSubscriptionKeyWordResponse],summary="Get all user subscriptions by keyword")
async def read_keywords(userId: int,
                        keyword_name: str,
                        timing: str,
                        start_date: datetime,
                        end_date: datetime,
                        db: AsyncSession = Depends(get_db),
                        current_user: User = Depends(get_current_user)):
    try:
        volumes = await get_user_keyword_subscriptions_list(db, userId, keyword_name,timing,start_date,end_date)
        return volumes
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))