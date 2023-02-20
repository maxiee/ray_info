from fastapi import FastAPI
import uvicorn
from ray_info.db import Info
from playhouse.shortcuts import model_to_dict
import jieba

from ray_info.fenci.fenci import add_word, get_word, like_word

def server_main():
    app = FastAPI()

    @app.get("/")
    async def hello():
        return "Hello, world!"

    @app.get("/info/list")
    async def info_list(skip: int = 0, limit: int = 20):
        query = Info.select().order_by(Info.updated.desc()).offset(skip).limit(limit)
        ret = []
        for info in query:
            cut_ret = jieba.cut(info.title)
            like_score = 0
            for fc in cut_ret:
                w = get_word(fc)
                if w != None:
                    like_score += w.like
            info.like = like_score
            info.save()
            d = model_to_dict(info)
            d['title_fc'] = jieba.cut(info.title)
            ret.append(d)
        return ret
    
    @app.get('/add_word')
    async def api_add_word(word: str):
        d = add_word(word)
        jieba.add_word(d.word, d.freq, d.tag)
        return 'ok'
    
    @app.get('/like_word')
    async def api_like_word(word: str):
        like_word(word)
        return 'ok'
    
    @app.get('/cut')
    async def cut(words: str):
        return jieba.cut(words)

    uvicorn.run(app, host="127.0.0.1", port=1127)
