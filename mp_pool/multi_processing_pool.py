import multiprocessing as mp
import threading
import psutil

class Task:
    __slots__ = ['func', 'args']

    def __init__(self, func, args):
        self.func = func
        self.args = args

    def __call__(self):
        return self.func(*self.args)


class Pool:
    def __init__(self, processes):
        self.id_worker = -1
        self.process_id = 0
        self.processes = processes
        self.workers = []
        self.queue = mp.Queue()
        self.free_workers = mp.Queue()
        self.lock = mp.Lock()
        self.event = mp.Event()
        self.max_core = psutil.cpu_count() -1 
        self.current_affinity = -1
        # init the pool
        for _ in range(self.processes):
            self._new_worker()
        for worker in self.workers:
            worker.start()

    def _new_worker(self):
        idx = self.get_id_worker()
        affinity = self.get_affinity()
        d = d = dict(affinity=affinity)
        print('created worker with affinity {}'.format(affinity))
        w = Worker(self, mp.Queue(), mp.Queue(), mp.Event(), idx, mp.Lock(), kwargs=d)
        self.workers.append(w)
        self.free_workers.put(idx)
    def get_affinity(self):
        if self.current_affinity < self.max_core:
            self.current_affinity += 1
        else:
            self.current_affinity = 0
        return self.current_affinity


    def get_id_worker(self):
        self.lock.acquire()
        self.id_worker += 1
        self.lock.release()
        return self.id_worker

    def get_worker(self):
        self.lock.acquire()
        idx = self.free_workers.get()
        self.lock.release()
        return self.workers[idx]
        # <opti>pre-chache event and then give them</opti>

    def map_one(self, func, args=()):
        worker = self.get_worker()
        worker.lock.acquire()
        worker.queue.put(Task(func, args))
        res = worker.output_queue.get()
        worker.lock.release()
        return res

    def stop(self):
        for worker in self.workers:
            worker.stop()
            worker.terminate()

    def reset_worker(self, idx):
        self.free_workers.put(idx)


class Worker(mp.Process):
    def __init__(self, pool, in_queue, out_queue, event, idx, lock, **kwargs):
        mp.Process.__init__(self, **kwargs)
        self.queue = in_queue
        self.output_queue = out_queue
        self.event = event
        self.stopped = False
        self.pool = pool
        self.idx = idx
        self.lock = lock

    def run(self):
        while not self.stopped:
            task = self.queue.get()
            try:
                result = task()
                self.output_queue.put(result)
            finally:
                self.pool.reset_worker(self.idx)
                # self.event.set()

    def stop(self):
        self.stopped = True
