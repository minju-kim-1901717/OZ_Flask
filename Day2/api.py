# - 책 목록을 보여주는 GET 엔드포인트를 만듭니다.
# - 새 책을 추가하는 POST 엔드포인트를 만듭니다.
# - 특정 책의 정보를 업데이트하는 PUT 엔드포인트를 만듭니다.
# - 특정 책을 삭제하는 DELETE 엔드포인트를 만듭니다.

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

book_blp = Blueprint('books', 'books', url_prefix='/books', description='Operations on books')

# 데이터 저장소
books = []

# 엔드포인트 구현...
@book_blp.route('/')
class Books(MethodView):
    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return books

    @book_blp.arguments(BookSchema)
    @book_blp.response(201, BookSchema)
    def post(self, new_book):
        new_book['id'] = len(books) + 1
        books.append(new_book)
        return new_book

@book_blp.route('/<int:book_id>')
class Book(MethodView):
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        return book
    
    @book_blp.arguments(BookSchema)
    @book_blp.response(200, BookSchema)
    def put(self, updated_book, book_id):
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        book.update(updated_book)
        return book

    @book_blp.response(204)
    def delete(self, book_id):
        global books
        book = next((book for book in books if book['id'] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        books = [book for book in books if book['id'] != book_id]
        return ''
    