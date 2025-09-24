from flask import request, jsonify
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models import Board
 
board_blp = Blueprint('Boards', 'boards', description='Operations on boards', url_prefix='/board')


# APTI List
# /board/
# 전체 게시글 불러오기 (GET)
# 새로운 게시글 작성 (POST)
@board_blp.route('/', strict_slashes=False) 
class BoardList(MethodView):
    def get(self):
        boards = Board.query.all()
        return jsonify([{"user_id": board.user_id, 
                         "id": board.id,
                         "title": board.title,
                         "content": board.content,
                         "author_name": board.author.name,
                         "author_email": board.author.email
                         } for board in boards])

    def post(self):
        data = request.json
        new_board = Board(title=data['title'], 
                          content=data['content'], 
                          user_id=data['user_id'])
        db.session.add(new_board)
        db.session.commit()
        # 201 + JSON 본문 유지 (프런트가 json() 처리 가능)
        return jsonify({"msg": "succsess creatd board", "id": new_board.id}), 201
    

# /board/<int:board_id>
# 하나의 게시글 불러오기 (GET)
# 특정 게시글 수정 (PUT)
# 특정 게시글 삭제 (DELETE)
@board_blp.route('/<int:board_id>') 
class BoardResource(MethodView):
    def get(self, board_id):
        board = Board.query.get_or_404(board_id)
        return jsonify({"id": board.id,
                        "title": board.title, 
                        "content": board.content, 
                        "author": board.author.name})

    def put(self, board_id):
        board = Board.query.get_or_404(board_id)
        data = request.json
        board.title = data['title']
        board.content = data['content']
        db.session.commit()
        return jsonify({"msg": "succsess update board", "id": board.id}), 200

    def delete(self, board_id):
        board = Board.query.get_or_404(board_id)
        db.session.delete(board)
        db.session.commit()
        return jsonify({"message": "succsess delete board", "id": board_id}), 200
