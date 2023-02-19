from queue import PriorityQueue
import time
import heapq
import datetime
class Task:
    def __init__(self, name, ts, repeat=False, repeat_period=0) -> None:
        """
        repeat: 是否重复
        repeat_period: 重复周期（单位 秒）
        """
        self.name = name
        self.ts = ts
        self.repeat = repeat
        self.repeat_period = repeat_period
    
    def run(self):
        pass
    
    def clone(self):
        return Task(
            name=self.name,
            ts=self.ts,
            repeat=self.repeat,
            repeat_period=self.repeat_period
        )
    
    def __str__(self) -> str:
        return f"任务: {self.name}"

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
                self.addTask(t_new)            
            return task
        else:
            # 时间未到
            self.addTask(task)
            return None
    
    def __str__(self) -> str:
        items = heapq.nsmallest(self.tasks.qsize(), self.tasks.queue)
        ret = '任务调度队列：\n'
        for i in items:
            ret += f'\t[{datetime.datetime.fromtimestamp(i[0]).strftime("%Y-%m-%d %H:%M:%S")}]\t[{i[1]}]'
        return ret
