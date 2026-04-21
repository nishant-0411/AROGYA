import os
from typing import Dict

from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_community.chat_message_histories import RedisChatMessageHistory

try:
    from langchain_community.chat_message_histories import RedisChatMessageHistory
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

_IN_MEMORY_STORE: Dict[str, BaseChatMessageHistory] = {}

def get_session_history(session_id: str) -> BaseChatMessageHistory:
    redis_url = os.getenv("REDIS_URL")
    
    if redis_url and REDIS_AVAILABLE:
        return RedisChatMessageHistory(session_id=session_id, url=redis_url)
    
    if session_id not in _IN_MEMORY_STORE:
        _IN_MEMORY_STORE[session_id] = InMemoryChatMessageHistory()
    
    return _IN_MEMORY_STORE[session_id]

def clear_session_history(session_id: str) -> None:
    redis_url = os.getenv("REDIS_URL")
    if redis_url and REDIS_AVAILABLE:
        history = RedisChatMessageHistory(session_id=session_id, url=redis_url)
        history.clear()
    elif session_id in _IN_MEMORY_STORE:
        _IN_MEMORY_STORE[session_id].clear()
        
def get_all_in_memory_sessions() -> Dict[str, BaseChatMessageHistory]:
    return _IN_MEMORY_STORE
