from __future__ import annotations

from typing import Any, Awaitable, Callable, Dict, MutableMapping

Scope = Dict[str, Any]
Message = MutableMapping[str, Any]
Receive = Callable[[], Awaitable[Message]]
Send = Callable[[Message], Awaitable[None]]
ASGIApp = Callable[[Scope, Receive, Send], Awaitable[None]]
