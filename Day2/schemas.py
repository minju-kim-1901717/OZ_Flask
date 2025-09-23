# Marshmallow를 사용하여 책 정보를 위한 스키마를 정의합니다. 
# 책은 최소한 'title'(제목)과 'author'(저자) 필드를 가져야 합니다.

from marshmallow import Schema, fields

class BookSchema(Schema):
    id = fields.Int(dump_only=True) #관리
    title = fields.String(required=True) #필수
    author = fields.String(required=True) #필수