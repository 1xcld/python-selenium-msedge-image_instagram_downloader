import requests

def downloadFile(path):
    response = requests.get(path)

    file = open("./image/image.png", "wb")
    file.write(response.content)
    file.close()
