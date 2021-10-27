from fastapi import APIRouter, File, UploadFile
from config.settings import UPLOAD_TO
from requests_toolbelt.multipart.encoder import MultipartEncoder
import http3

client = http3.AsyncClient()

router = APIRouter()


@router.post('/api/uploadfile')
async def create_upload_file(file: UploadFile = File(...)):
    m = MultipartEncoder(fields={'file': (file.filename, file.file, file.content_type)})
    file_response = await client.post(UPLOAD_TO, data=m.to_string(), headers={'Content-Type': m.content_type})
    return file_response.json()
