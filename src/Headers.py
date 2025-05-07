from fastapi import Header

async def headers(
        accept:str = Header(None),
        content_type:str = Header(None),
        User_Agent:str = Header(None),
        Host:str = Header(None)

):
    request