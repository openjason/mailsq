# TradeWeb测试脚本
import threading, time, http.client, urllib.request, os
#import matplotlib.pyplot as plt

URL = 'http://127.0.0.1:8888/XXXXXXXXX/httpXmlServlet' # 在配置文件中读取，此处将无效

TOTAL       = 0;    # 总数
SUCC        = 0;    # 响应成功数量
FAIL        = 0;    # 响应失败数量
EXCEPT      = 0     # 响应异常数
MAXTIME     = 0     # 最大响应时间
MINTIME     = 100   # 最小响应时间，初始值为100秒
COUNT_TIME   = 0    # 总时间
THREAD_COUNT = 0    # 记录线程数量
CODE_MAP = {200:0, 301:0, 302:0, 304:0}     # 状态码信息(部分)
RESULT_FILE = 'tradeWebResult.xml'          # 输出结果文件
REQUEST_DATA_FILE = 'requestData.config'         # 数据文件

DATA = '''请在tradeWebRequestData.config文件中配置'''

TIME_LIST = []  # 记录访问时间

#创建一个threading.Thread的派生类
class RequestThread(threading.Thread):
    #构造函数
    def __init__(self, thread_name):
        threading.Thread.__init__(self)
        self.test_count = 0;

    #线程运行的入口函数
    def run(self):
        global THREAD_COUNT
        THREAD_COUNT += 1
        #print("Start the count of thread:%d" %(THREAD_COUNT))
        self.testPerformace()

    #测试性能方法
    def testPerformace(self):
        global TOTAL
        global SUCC
        global FAIL
        global EXCEPT
        global DATA
        global COUNT_TIME
        global CODE_MAP
        global URL
        try:
            st = time.time()    #记录开始时间

            start_time
            cookies = urllib.request.HTTPCookieProcessor()
            opener = urllib.request.build_opener(cookies)

            resp = urllib.request.Request(url=URL,
                                      headers={'Content-Type':'text/xml', 'Connection':'Keep-Alive'},
                                      data=DATA.encode('gbk'))

            respResult = opener.open(resp)

            # 记录状态码 START
            code = respResult.getcode()
            if code == 200:
                SUCC += 1
            else:
                FAIL += 1

            if code in CODE_MAP.keys():
                CODE_MAP[code] += 1
            else:
                CODE_MAP[code] = 1

            # print(request.status)
            # 记录状态码 END

            html = respResult.read().decode('gbk')
            print(html)

            time_span = time.time() - st    # 计算访问时间

             # 记录访问时间
            TIME_LIST.append(round(time_span * 1000))

            # print('%-13s: %f ' %(self.name, time_span))

            self.maxtime(time_span)
            self.mintime(time_span)

            self.writeToFile(html)

            # info = respResult.info()   # 响应头信息
            # url = respResult.geturl()  # URL地址
            # print(info);
            # print(url)

            COUNT_TIME += time_span
            TOTAL += 1
        except Exception as e:
            print(e)
            TOTAL += 1
            EXCEPT += 1

    # 设置最大时间，如果传入的时间大于当前最大时间
    def maxtime(self, ts):
        global MAXTIME
        #print("time:%f" %(ts))
        if ts > MAXTIME:
            MAXTIME = ts

    # 设置最小时间，如果传入的时间小于当前最小时间
    def mintime(self, ts):
        global MINTIME
        #print("time:%f" %(ts))
        if ts < MINTIME and ts > 0.000000000000000001:
            MINTIME = ts

    # 写入文件
    def writeToFile(self, html):
        f = open(RESULT_FILE, 'w')
        f.write(html)
        f.write('\r\n')
        f.close();

# 读取XML数据信息
def loadData():
    global URL
    global DATA

    f = open(REQUEST_DATA_FILE, 'r')
    URL = "".join(f.readline())
    DATA = "".join(f.readlines())

    # print(DATA)

    f.close()


if __name__ == "__main__":
    # print("============测试开始============")
    print("")
    # 开始时间
    start_time = time.time()
    # 并发的线程数
    thread_count = 1

    loadData()     # 加载请求数据

    i = 0
    while i < thread_count:
        t = RequestThread("Thread" + str(i))
        t.start()
        i += 1

    t = 0
    while TOTAL < thread_count and t < 60:
        # print("total:%d, succ:%d, fail:%d, except:%d\n" %(TOTAL,SUCC,FAIL,EXCEPT))
        print("正在请求 ",URL)
        t += 1
        time.sleep(1)

    # 打印信息
    print()
    print("请求", URL, "的统计信息：")
    print("    总请求数 = %d，成功 = %d，失败 = %d，异常 = %d" %(TOTAL, SUCC, FAIL, EXCEPT))
    print()
    print("往返程的估计时间(以毫秒为单位)：")
    print("    合计 =", int(COUNT_TIME * 1000), "ms", end = '')
    print("    最大 =", round(MAXTIME * 1000), "ms", end = '')
    print("    最小 =", round(MINTIME * 1000), "ms", end = '')
    print("    平均 =", round((COUNT_TIME / thread_count) * 1000), "ms")
    print()
    print("响应的状态码与次数信息(状态码:次数)：")
    print("    ", CODE_MAP)
    print()
    print("输出页面请查看", RESULT_FILE, "文件(建议使用浏览器或XML专业工具打开)")
    print()
    # os.system("pause")

    print(TIME_LIST)
    input()