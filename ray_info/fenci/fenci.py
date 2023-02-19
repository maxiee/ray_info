import jieba
import peewee

from ray_info.db import UserDict


def load_user_dict_from_db():
    user_dict = []
    for word in UserDict.select():
        user_dict.append((word.word, word.freq, word.tag))
    return user_dict


def init_jieba():
    jieba.initialize()
    for w in load_user_dict_from_db():
        word = w[0]
        freq = None
        tag = None

        if w[1] >= 1:
            freq = w[1]

        if w[2]:
            tag = w[2]

        jieba.add_word(word, freq, tag)


def add_word(word: str, freq: int = 1, tag: str = "n"):
    try:
        d = UserDict.get(UserDict.word == word)
        d.freq = d.freq + 1
        d.save()
        return d
    except peewee.DoesNotExist:
        d = UserDict.create(word=word, freq=freq, tag=tag, like=1)
        return d

def like_word(word: str):
    w = add_word(word)
    w.like = w.like + 1
    w.save()
