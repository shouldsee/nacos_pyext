__doc__ = '''
Author: Feng Geng <shouldsee@qq.com>
Ref: https://nacos.io/en-us/docs/open-api.html
License Apache2.0
'''
__version__ = 'v0.0.1'
from nacos import NacosClient
from nacos.client import logger
from datetime import datetime
from multiprocessing import Queue
from threading import Thread
import time
import traceback

class NacosClientService(object):
    '''
    Thinly wrapped object for simpler service registery
    '''
    def __init__(self, urls, service_name, ip, port, ephemeral= True,**kw):
        # super().__init__(urls, **kw)
        self.client = NacosClient(urls,**kw)
        self.service_name = service_name
        self.ip = ip
        self.port = port
        self.ephemeral = ephemeral
        self.heartbeat_thread = None
        self.q_rec = Queue()
        self.last_exes = {}
        self.last_beat_good = False
        self.last_beat_good_ts = None

    def safe_send_heartbeat(self,**kw):
        ret = False
        try:            
            ret= self.client.send_heartbeat(self.service_name, self.ip, self.port, 
            ephemeral = self.ephemeral,
         **kw)
        except Exception as e:
            self.last_exes['heartbeat'] = es = traceback.format_exc()
            # logger.warning(es)
            time.sleep(1)
        self.last_beat_good = ret
        if self.last_beat_good:
            self.last_beat_good_ts = datetime.now().isoformat()
        return ret

    def cycle_send_heartbeat(self, wait_sec, **kw):
        while True:
            suc = self.safe_send_heartbeat(**kw)
            if suc is False:
                # None:
                #  suc:
                self.q_rec.put(1)
            time.sleep(wait_sec)



    def start_register_thread(self, **kw):
        def inner():
            while True:
                _ = self.q_rec.get()
                self.add_naming_instance(**kw)
        t = Thread(target=inner,daemon=True)
        t.start()
        self.t_register = t
        self.q_rec.put(1)


    def start_heartbeat_thread(self,wait_sec=10):
        t = Thread(target=self.cycle_send_heartbeat,args=(wait_sec,),daemon=True)
        t.start()
        self.heartbeat_thread = t

    def add_naming_instance(self,**kw):
        ret = False
        try:            
            ret = self.client.add_naming_instance(self.service_name, self.ip, self.port,
            ephemeral = self.ephemeral,
            **kw)
        except Exception as e:
            self.last_exes['register'] = es = traceback.format_exc()
            # logger.warning(es)
            time.sleep(1)
        return ret

    def register(self,**kw):
        return self.add_naming_instance(**kw)

    def remove_naming_instance(self,**kw):
        return self.client.remove_naming_instance(self.service_name, self.ip, self.port,
        ephemeral = self.ephemeral,
        **kw)
        
    def deregister(self,**kw):
        return self.remove_naming_instance(**kw)
