import redis
import time

class redisproc:
    _instance = None

    @classmethod
    def _getInstance(cls):
        return cls._instance

    @classmethod
    def instance(cls, *args, **kargs):
        cls._instance = cls(*args, **kargs)
        cls.instance = cls._getInstance
        cls.connectRedis()
        return cls._instance

    @classmethod
    def connectRedis(cls):
        cls.r = redis.Redis(
            host='192.168.6.37',
            port=6379,
            password='mappers',
            db=0)
        return cls.r

    def is_redis_available(self, r):
        try:
            r.ping()
            print("Successfully connected to redis")
        except (redis.exceptions.ConnectionError, ConnectionRefusedError):
            print("Redis connection error!")
            return False
        return True

    def searchGrid(self):
        if not self.is_redis_available(self.r):
            raise Exception('db connection error')

        #result = r.geosearch('car-order', longitude=126.7981806, latitude=37.6175133, radius=10000,  unit="m", sort="ASC")
        start_time = time.process_time()
        counts = []
        for i in range(0,100):
            for j in range(0, 10):
                car_name = "car_%i_%i"% (i*10, j*10)
                result = self.r.geosearch('car-order', member=car_name , radius=5000,  unit='m', sort="ASC", withdist=True)
                #print(len(result))
                counts.append(len(result))
        end_time = time.process_time()
        print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")
        print(f"avg=%i, max=%i, min=%i"%(sum(counts)/len(counts), max(counts), min(counts)))

    def insertGrid(self):
        base_x = 126.7981806
        base_y = 37.6175133
        diff_x = 0.001
        diff_y = 0.001
        x =0.0
        y = 0.0
        counter =0
        isCar = False

        if not self.is_redis_available(self.r):
            raise Exception('db connection error')

        #result = r.geosearch('car-order', longitude=126.7981806, latitude=37.6175133, radius=10000,  unit="m", sort="ASC")
        start_time = time.process_time()
        counts = []
        for xi in range(0,1000):
            for yi in range(0, 1000):
                counter = counter + 1

                x = base_x + (diff_x * xi)
                y = base_y - (diff_y * yi)
                if xi % 10 == 0 and yi % 10 == 0:
                    isCar = True
                else:
                    isCar = False


                car_name = "car_%i_%i" % (xi, yi)
                result = self.r.geoadd('car-order', x, y, car_name )
                #print(len(result))

        end_time = time.process_time()
        print(f"time elapsed : {int(round((end_time - start_time) * 1000))}ms")
        print(f"avg=%i, max=%i, min=%i"%(sum(counts)/len(counts), max(counts), min(counts)))