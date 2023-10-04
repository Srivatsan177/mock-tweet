import requests
files = {"upload_file": open('pyproject.toml', "rb")}
values = { 'DB': "photocat", "OUT": "csv", 'SHORT': "short" }
resp = requests.put("https://srivatsan-tweet.s3.amazonaws.com/images/6506a51bc3b71c5190d40171.txt?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIARAJWV2RPPON2ND4V%2F20230917%2Fap-south-1%2Fs3%2Faws4_request&X-Amz-Date=20230917T105451Z&X-Amz-Expires=300&X-Amz-SignedHeaders=host&X-Amz-Signature=30fafc71759225d46935cfa2953bbfdc35780fcb9fa8d1bc60d6e9a230da91de"
, files = files, data = values)
print(resp.text, resp)