import qrcode
from requests import Response

from fastApi.main import cur


async def QRCodeGeneratiFromArticle(article: str, response: Response):
    cur.execute(f"SELECT article FROM reviews ORDER BY RANDOM() LIMIT 1")
    data = cur.fetchall()
    # Generate the QR code
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4, )
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image()

    # Set the content type and send the image in the response body
    response.headers['Content-Type'] = 'image/png'
    img_bytes = img.getvalue()
    response.body = img_bytes

    # Redirect to another URL
    response.status_code = 307
    response.headers['Location'] = "/postamatQR/{article}"

