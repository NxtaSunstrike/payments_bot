import json
import hashlib
import base64
from typing import Any

from aiohttp import ClientSession


def generate_headers(data: str) -> dict[str, str]:
    
    sign = hashlib.md5(
        base64.b64encode(
        data.encode('ascii')) + API_KEY.encode('ascii')
        ).hexdigest()
    
    return {
        'merchant': MERCHANT_UUID,
        'sign':sign,
        'content-type':'application/json'
        }


async def create_invoice(user_id:int,currency:int)->Any:
    async with ClientSession() as session:
        
        json_dumps = json.dumps(
            {
            'amount':f'{currency}',
            'order_id': f'{user_id}',
            'currency':'USDT',
            'network':'tron',
            'lifetime':900
        }
        )
        responce = await session.post(
            url = END_POINT,
            data = json_dumps,
            headers = generate_headers(json_dumps)
        )
        return await responce.json()
    

async def get_invoice(uuid:str)->Any:
    async with ClientSession() as session:
        json_dumps = json.dumps({'uuid': uuid})
        responce = await session.post(
            url = PAYMENT_INFO,
            data = json_dumps,
            headers = generate_headers(json_dumps)
        )
        return await responce.json()