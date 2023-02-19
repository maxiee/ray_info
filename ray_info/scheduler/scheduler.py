from queue import PriorityQueue
import time

class Task:
    def __init__(self, name, ts, callback, repeat=False, repeat_period=0) -> None:
        """
        repeat: 是否重复
        repeat_period: 重复周期（单位 秒）
        """
        self.name = name
        self.ts = ts
        self.callback = callback
        self.repeat = repeat
        self.repeat_period = repeat_period
    
    def clone(self):
        return Task(
            name=self.name,
            ts=self.ts,
            callback=self.callback,
            repeat=self.repeat,
            repeat_period=self.repeat_period
        )

class Scheduler:
    tasks = PriorityQueue()

    def addTask(self, task: Task):
        self.tasks.put((task.ts, task))

    def getOnTimeTask(self):
        now = time.time()
        ts, task = self.tasks.get()
        if now >= ts:
            # 时间已到
            if task.repeat is True:
                t_new = task.clone()
                t_new.ts = t_new.ts + t_new.repeat_period
                self.tasks.put(t_new.ts, t_new)            
            return task
        else:
            # 时间未到
            self.tasks.put(task)
            return None