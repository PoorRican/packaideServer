from fastapi import FastAPI
from pydantic import BaseModel

from utils import combine_svg, generate_sheet, perform_packing

app = FastAPI()


class NestingRequest(BaseModel):
    height: float
    width: float
    shapes: list[str]


@app.post('/pack')
def pack(request: NestingRequest):
    # create a template sheet
    sheet = generate_sheet(width=request.width, height=request.height)

    # combine all shapes into one SVG
    shapes = combine_svg(request.shapes)

    # perform the packing operation
    packed_sheets: list[str] = perform_packing(shapes, sheet)

    return packed_sheets
