import http.client

conn = http.client.HTTPSConnection("firestore.googleapis.com")

headers = {
    'content-type': "application/json",
    'authorization': "Bearer ya29.GqQBkAbtSQvtpsOKEsGyXDBqeTjN9RkPy0J1YqvnOBTar0l7Cs8EuPQX7B6oDBJNtGZPRoeoMBZ3qkhlIgHtOtap2cVcplxbQzy0e2C9nMRLKtVlJ5f-d4Hw3MVaxa4eMLWnSqL4ZSH1n8o1JY0VMrkJ6CSEcnn1944BD3ej-Ov8n0Ya1fMMYicUCKdRINH72VvY9dmcrX6fgKLUGXEPuLHjYObTGyc",
    'cache-control': "no-cache",
    'postman-token': "00365fb2-9270-a53d-9856-20aa19611a01"
    }

conn.request("GET", "/v1beta1/projects/sandbox-khl/databases/%28default%29/documents/test/ncNyVdqKohl1Uj2flSui", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
