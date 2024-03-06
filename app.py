
import os
from pathlib import Path
from fastapi import FastAPI, Body, Request, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from process import generate_response
from process import file_generated
import aiofiles
import sys
from pydantic import BaseModel

app = FastAPI()
sys.setrecursionlimit(15000)

@app.get("/")
async def main():
    # async with aiofiles.open('templates/index.html', mode='r') as f:
    #     content = await f.read()
    # return HTMLResponse(content)
    return HTMLResponse("Hello world")

class Req(BaseModel):
    userImg: str
    userAnim: str

@app.post("/animate/")
async def animate(req: Req):
    
    response = generate_response(req.userImg,req.userAnim)

    if(file_generated): 
        print(print(f'{Path.cwd()}/generated.mp4'))
        return HTMLResponse(response)
    else:
        return {"message": "There was an error generating the animation"}


@app.post("/uploadfile/{userid}")
async def create_upload_file(file: UploadFile, userid: str):
    try:
        contents = file.file.read()
        extension = file.filename.split(".")[1]
        newpath = r'uploads' 
        if not os.path.exists(newpath):
            os.mkdir(newpath)
       
        file_name = os.getcwd()+f"/uploads/{userid}."+extension.replace(" ", "-")
        with open(file_name, 'wb') as f:
            f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
    
    response = {
        "code": 200,
        "message": "Successfully uploaded",
        "filename": f"{userid}.{extension}"
    }

    return response

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)