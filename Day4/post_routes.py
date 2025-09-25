from flask import request, jsonify
from flask_smorest import Blueprint, abort

def create_posts_blueprint(mysql):
    posts_blp = Blueprint('posts', __name__, description='posts api', url_prefix='/posts/')

    @posts_blp.route('/', methods=['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()
        try:
            # GET: 전체 조회
            if request.method == 'GET':
                sql = "SELECT id, title, content FROM posts ORDER BY id DESC"
                cursor.execute(sql)

                rows = cursor.fetchall()
                cursor.close()

                post_list = []

                for row in rows:
                    post_list.append({
                        'id': row[0],
                        'title': row[1],
                        'content': row[2],
                    })
                return jsonify(post_list)
                print(post_list)

            # POST: 생성
            body = request.get_json() or {}
            title = (body.get('title') or '').strip()
            content = (body.get('content') or '').strip()

            if not title or not content:
                abort(400, message="Title and content cannot be empty.")

            sql = "INSERT INTO posts (title, content) VALUES (%s, %s)"
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            new_id = cursor.lastrowid
            return jsonify({
                'message': 'Post created successfully.',
                'id': new_id,
                'title': title,
                'content': content
            }), 201
        finally:
            cursor.close()

    # 상세 조회/수정/삭제 — 일관된 파라미터 이름(post_id) 사용
    @posts_blp.route('/<int:post_id>', methods=['GET', 'PUT', 'DELETE'])
    def post(post_id):
        cursor = mysql.connection.cursor()
        try:
            # GET: 단건 조회 (파라미터 바인딩 사용)
            if request.method == 'GET':
                sql = "SELECT id, title, content FROM posts WHERE id = %s"
                cursor.execute(sql, (post_id,))
                row = cursor.fetchone()
                if not row:
                    abort(404, message="Post not found.")
                return jsonify({"id": row[0], "title": row[1], "content": row[2]})

            # PUT: 수정
            elif request.method == 'PUT':
                body = request.get_json() or {}
                title = (body.get('title') or '').strip()
                content = (body.get('content') or '').strip()

                if not title or not content:
                    abort(400, message="Title and content cannot be empty.")

                # 존재 여부 확인
                cursor.execute("SELECT id FROM posts WHERE id = %s", (post_id,))
                if not cursor.fetchone():
                    abort(404, message="Post not found.")

                sql = "UPDATE posts SET title = %s, content = %s WHERE id = %s"
                cursor.execute(sql, (title, content, post_id))
                mysql.connection.commit()

                return jsonify({'message': 'Post updated successfully.', 'id': post_id, 'title': title, 'content': content})

            # DELETE: 삭제
            elif request.method == 'DELETE':
                # 삭제 시도 후 적용된 행 수로 존재 여부 판단
                sql = "DELETE FROM posts WHERE id = %s"
                cursor.execute(sql, (post_id,))
                mysql.connection.commit()

                if cursor.rowcount == 0:
                    abort(404, message="Post not found.")
                return jsonify({'message': 'Post deleted successfully.'})
        finally:
            cursor.close()

    return posts_blp
