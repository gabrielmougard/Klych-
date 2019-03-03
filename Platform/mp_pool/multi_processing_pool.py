######################
#    Writter Plawn   #
######################

import multiprocessing as mp
import threading


class Task:
    __slots__ = ['func', 'return_id', 'args']

    def __init__(self, func, return_id, args):
        self.func = func
        self.return_id = return_id
        self.args = args

    def __call__(self):
        return self.func(*self.args)


class Pool:
    MAX_PROCESS_ID = 65535

    def __init__(self, processes):
        self.processes = processes
        self.workers = []
        self.manager = mp.Manager()
        self.manager_d = self.manager.dict()
        self.manager_d['free_worker'] = []
        self.queue = mp.Queue()
        self.lock = threading.Lock()
        self.process_id = 0
        self.event = mp.Event()
        self.events = []
        self.id_worker = -1
        # init the pool
        for _ in range(self.processes):
            self._new_worker()
        for worker in self.workers:
            worker.start()
        # print(self.manager_d)

    def _new_worker(self):
        event = mp.Event()
        queue = mp.Queue()
        w = Worker(self, queue, self.manager_d, event, self.get_id_worker())
        self.workers.append(w)
        self.manager_d['free_worker'] = list(range(len(self.workers)))
        # print(self.manager_d['free_worker'])

    def get_id_worker(self):
        with self.lock:
            if self.id_worker < self.MAX_PROCESS_ID:
                self.id_worker += 1
            else:
                self.id_worker = 0
            return self.id_worker

    def get_return_id(self):
        with self.lock:
            if self.process_id < self.MAX_PROCESS_ID:
                self.process_id += 1
            else:
                self.process_id = 0
            return self.process_id

    def get_worker(self):
        import time
        while True:
            with self.lock:
                if len(self.manager_d['free_worker']) > 0:
                    l = self.manager_d['free_worker']
                    i = l.pop(0)
                    self.manager_d['free_worker'] = l
                    self.event.clear()
                    return self.workers[i]
                # else:
                #     print('no worker', self.manager_d['free_worker'])
            # time.sleep(1)
            self.event.wait()
            # <opti>pre-chache event and then give them</opti>

    def map_one(self, func, args):
        return_id = self.get_return_id()
        worker = self.get_worker()
        task = Task(func, return_id, args)
        worker.queue.put(task)
        worker.event.wait()
        worker.event.clear()
        res = self.manager_d[return_id]
        del self.manager_d[return_id]
        return res

    def stop(self):
        for worker in self.workers:
            worker.stop()
            worker.terminate()

    def reset_worker(self, idx):
        old = self.manager_d['free_worker']
        old.append(idx)
        self.manager_d['free_worker'] = old
        self.event.set()


class Worker(mp.Process):
    def __init__(self, pool, queue, manager_d, event, idx):
        mp.Process.__init__(self)
        self.queue = queue
        self.event = event
        self.stopped = False
        self.manager_d = manager_d
        self.pool = pool
        self.idx = idx

    def run(self):
        while not self.stopped:
            task = self.queue.get()
            result = None
            try :
                result = task()
                self.manager_d[task.return_id] = result                
            # except Exception as e:
            #     print('HEY', e)
            finally :
                self.pool.reset_worker(self.idx)
                self.event.set()

    def stop(self):
        self.stopped = True
