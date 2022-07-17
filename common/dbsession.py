from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import event
import settings
from fastapi import Request
from common.globalFunctions import get_token
from BroadcastManager import broadcastManager
from sqlalchemy.util.concurrency import await_only
engine = create_async_engine(
    settings.DBURL,
    echo=settings.DEBUG,
)

async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session(request:Request,token: settings.UserTokenData=Depends(get_token)) -> AsyncSession:
    async with async_session() as session:
        setattr(session,"_createdArr",[])
        setattr(session, "_updateArr", [])

        @event.listens_for(session.sync_session, 'before_flush')
        def before_flush(tmpsession, flush_context,instances):
            await_only(broadcastManager.fireBeforeCreated(session.new,session,token))

        @event.listens_for(session.sync_session, 'after_flush')
        def after_flush(tmpsession, flush_context):
            await_only(broadcastManager.fireAfterCreated(session.new,session,token,background=False))
            await_only(broadcastManager.fireAfterUpdated(session.dirty,session,token,background=False))

            session._updateArr+=list(session.dirty)
            session._createdArr+=list(session.new)


        request.state.db_client=session
        yield session



