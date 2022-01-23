import requests

API_URL = 'http://127.0.0.1:8000/api/'  #your api domain

#Test Case #1 - Create Book Record
url = API_URL + 'book-create/'
data = {
    "title":"Title of the book",
    "isbn_number":"2131",
    "genre": "ROMANCE",
    "author": "Author of the book",
    "description": "Description of the book"
}
response = requests.post(url,data=data)
response = response.json()
book = response.get('data','').get('book_id','')

#Test Case #2 - Create a library Record
url = API_URL + 'library-create/'
data = {
    "library_name":"Name of the Library",
    "email":"abclibrary@gmail.com",
    "password": "123",
}
response = requests.post(url,data=data)
response = response.json()
library = response.get('data','').get('library_id','')



#Test Case #3 - Create a library book Record
url = API_URL + 'library-book-create/'
data = {
    "book":book,
    "library":library,
    "quantity": 10,
}
response = requests.post(url,data=data)
response = response.json()
