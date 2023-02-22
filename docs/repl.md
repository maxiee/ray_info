PlayWright 如何拦截保存图片：https://stackoverflow.com/questions/74913951/how-to-asynchronizely-save-image-with-playwright-in-python

# 通过命令行发送一条微博

```
RayInfo REPL
> open_weibo
> send_weibo
输入微博内容>test
```

# REPL 调试方法

首先使用 poetry 进入 shell，进入内层的 ray_info 目录，执行 `python` 开启 repl：

```python
from u import *
```

其中，p 就是 Page，之后可以进行调试了。

调试完成后退出：

```python
done()
```
