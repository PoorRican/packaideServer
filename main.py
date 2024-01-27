from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from utils import combine_svg, generate_sheet, perform_pack

app = FastAPI()


class NestingRequest(BaseModel):
    """ A request to the Packaide server.

    Each field is required. The `tolerance`, `offset`, and `rotations` fields *must* be passed
    from the client.
    """
    height: float
    width: float
    shapes: list[str]
    tolerance: float
    offset: float
    rotations: int


@app.post('/pack')
def pack(request: NestingRequest):
    # create a template sheet
    sheet = generate_sheet(width=request.width, height=request.height)

    # combine all shapes into one SVG
    shapes = combine_svg(request.shapes)

    # perform the packing operation
    try:
        packed_sheets: list[str] = perform_pack(shapes, sheet,
                                                tolerance=request.tolerance,
                                                offset=request.offset,
                                                rotations=request.rotations)

        return packed_sheets

    # return status code 400 if an error occurs
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
