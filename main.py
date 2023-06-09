from typing import Any, List, Annotated

from fastapi import FastAPI, File, UploadFile, Request, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates

from controller.gis_convert import GisConvertController
from web.response import ResponseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5500",
    "http://localhost:28080",
    "http://192.168.1.110",
    "http://192.168.1.110:3000",
    "http://192.168.1.110:5500",
    "http://192.168.1.110:28080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 파라메터를 받아 DB에 저장
@app.put("/api/v1/geoInfo", response_model=ResponseModel)
async def update_geoInfo(request: Request) -> Any:
    data = await request.json()
    return ResponseModel(code=200, message="Hello World", data=[{"name": "John Doe"}])

@app.get("/api/v1/hello", response_model=ResponseModel)
def read_root() -> Any:
    return ResponseModel(code=200, message="Hello World", data=[{"name": "John Doe"}])


# Excel 업로드 기능
@app.post("/api/v1/gisinfo/addr")
async def address_convert(file: UploadFile = File(...), column: str = Form(...)) -> Any:
    return GisConvertController(file=file, target=[column]).address_based_method()

@app.post("/api/v1/gisinfo/coord")
async def coordinate_convert(file: UploadFile = File(...), x: str = Form(...), y: str = Form(...)) -> Any:
    return GisConvertController(file=file, target=[x, y]).coordinate_based_method()

@app.get("/")
async def read_upload_file():
    request = {"request": "Hello"}
    return templates.TemplateResponse("upload_excel.html", {"request": request})

# print(RetrieveNaverMap().address_based("서구 배재로 128"))
