import packaide
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class NestingRequest(BaseModel):
    height: float
    width: float
    shapes: str


@app.post('/pack')
def pack(request: NestingRequest):
    sheet = """<svg
       viewBox="0 0 {height} {width}"
       version="1.1"
       xmlns="http://www.w3.org/2000/svg"
       xmlns:svg="http://www.w3.org/2000/svg" ></svg>""".format(height=request.height, width=request.width)

    results, _, _ = packaide.pack(
        [sheet],
        request.shapes,
        tolerance=0.1,
        offset=5,
        partial_solution=True,
        rotations=4,
        persist=True
    )

    sheets: list[str] = []
    for _, out in results:
        sheets.append(out)

    return sheets
