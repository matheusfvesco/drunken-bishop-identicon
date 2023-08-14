from lib.DrunkenBishop import DrunkenBishopIdenticon
from fastapi import FastAPI, Path, Request

app = FastAPI(
    title="Drunken Bishop Identicons",
    description="An API used for generating unique svg images based on a slug, using the drunken bishop algorithm",
    version="1.0.0",
)


@app.get("/")
async def root(request: Request) -> dict:
    """Returns a greeting message and some info.

    Args:
        request (Request): The incoming request object.

    Returns:
        dict: A dictionary containing the greeting message.
    """
    base_url = str(request.base_url)
    return {
        "Welcome": "Hello, welcome to the Drunken Bishop Identicon API! Use it to generate unique identicons for a slug.",
        "info": f"For more information on how to use the API, visit {base_url}doc!"
    }


@app.get("/svg/{slug}")
async def read_item(slug: str) -> dict:
    """Generates an HTML SVG identicon for the given slug.

    Args:
        slug (str): The input slug used to generate the identicon.

    Returns:
        dict: A dictionary containing the generated HTML SVG identicon. 300x300 SVG image, board size 7 and 3 iterations
    """
    return {"svg": DrunkenBishopIdenticon(slug, 7, 3).svg()}


@app.get("/svg/{slug}/{size}")
async def read_item(slug: str, size: int = Path(..., gt=0)) -> dict:
    """Generates an HTML SVG identicon for the given slug, returning it with the defined size for the HTML.

    Args:
        slug (str): The input slug used to generate the identicon.
        size (int): The size of the generated SVG image.

    Returns:
        dict: A dictionary containing the generated SVG identicon. Uses board size 7 and 3 iterations.
    """
    return {"svg": DrunkenBishopIdenticon(slug, 7, 3).svg(size)}


@app.get("/board/{slug}/{bsize}/{iter}/{size}")
async def read_item(
    slug: str,
    bsize: int = Path(..., gt=0),
    iter: int = Path(..., gt=0),
    size: int = Path(..., gt=0),
) -> dict:
    """Generates an HTML SVG identicon for the given parameters.

    Args:
        slug (str): The input slug used to generate the identicon.
        bsize (int): The size of the board used to generate the identicon.
        iter (int): The number of iterations to run the drunken bishop algorithm.
        size (int): The size of the generated SVG image.

    Returns:
        dict: A dictionary containing the generated SVG identicon.
    """
    return {"svg": DrunkenBishopIdenticon(slug, bsize, iter).svg(size)}


@app.get("/base64/{slug}")
async def read_item(slug: str) -> dict:
    """Generates an SVG identicon for the given slug and returns the base64 encoded string for it.

    Args:
        slug (str): The input slug used to generate the identicon.

    Returns:
        dict: A dictionary containing the generated base64 encoded SVG identicon. 300x300, board size 7 and 3 iterations.
    """
    return {"svg": DrunkenBishopIdenticon(slug, 7, 3).svg_base64()}


@app.get("/base64/{slug}/{size}")
async def read_item(slug: str, size: int = Path(..., gt=0)) -> dict:
    """Generates an SVG identicon for the given slug and returns the base64 encoded string for it.

    Args:
        slug (str): The input slug used to generate the identicon.
        size (int): The size of the generated SVG image.

    Returns:
        dict: A dictionary containing the generated base64 encoded SVG identicon. custom size, board size 7 and 3 iterations.
    """
    return {"svg": DrunkenBishopIdenticon(slug, 7, 3).svg_base64(size)}

@app.get("/base64board/{slug}/{bsize}/{iter}/{size}")
async def read_item(
    slug: str,
    bsize: int = Path(..., gt=0),
    iter: int = Path(..., gt=0),
    size: int = Path(..., gt=0),
) -> dict:
    """Generates an SVG identicon for the given parameters and returns the base64 encoded string for it.

    Args:
        slug (str): The input slug used to generate the identicon.
        bsize (int): The size of the board used to generate the identicon.
        iter (int): The number of iterations to run the drunken bishop algorithm.
        size (int): The size of the generated SVG image.

    Returns:
        dict: A dictionary containing the generated base64 encoded SVG identicon.
    """
    return {"svg": DrunkenBishopIdenticon(slug, bsize, iter).svg_base64(size)}

