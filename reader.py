from urllib.request import urlopen, Request
url = "http://192.168.1.5:5000"
request = Request(url)
response = urlopen(request)
html = response.read()
print(html)
response.close()