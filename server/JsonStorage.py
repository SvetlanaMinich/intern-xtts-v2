import json
import aiofiles
import os
import base64
import logging

logging.basicConfig(format='%(asctime)s:%(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

class JsonStorage:
    def __init__(self, path_to_json_dir:str) -> None:
        self.json_dir = path_to_json_dir


    async def add_client_async(self, client_id:int, voice:bytes) -> None:
        new_file = self.json_dir + fr'/{client_id}.json'
        
        client_json_data = json.dumps({'voice': base64.b64encode(voice).decode('utf-8')})
        async with aiofiles.open(new_file, 'w') as f:
            await f.write(client_json_data)
        
        logger.debug(f'Client {client_id} added')

    
    async def update_client_async(self, client_id:int, voice:bytes) -> None:
        clients = os.listdir(path=self.json_dir)
        
        client_json_data = json.dumps({'voice': base64.b64encode(voice).decode('utf-8')})
        for client in clients:
            if client == f'{client_id}.json':
                file_path = self.json_dir + fr'/{client}'
                async with aiofiles.open(file_path, 'w') as f:
                    await f.write(client_json_data)
                    logger.debug(f'Client {client_id} voice updated')
                break


    async def client_exists_async(self, client_id:int) -> bool:
        clients = os.listdir(path=self.json_dir)

        for client in clients:
            if client == f'{client_id}.json':
                logger.debug(f'Client {client_id} exists')
                return True
        
        logger.debug(f'Client {client_id} does not exist')
        return False
    

    async def get_voice_by_client_id_async(self, client_id:int) -> bytes:
        clients = os.listdir(path=self.json_dir)

        for client in clients:
            if client == f'{client_id}.json':
                file_path = self.json_dir + fr'/{client}'
                async with aiofiles.open(file_path, 'r') as f:
                    json_data = await f.read()
                    data = json.loads(json_data)
                    logger.debug(f'Client {client_id} voice extracted')
                    return base64.b64decode(data['voice'])