async def pagination_params(limit: int = 100, offset: int = 0) -> dict[str, int]:
    return {"limit": limit, "offset": offset}
