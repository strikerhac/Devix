
import ping3
import traceback

def ping(ip):
    try:
        response_time = ping3.ping(str(ip))
        if response_time is not None:
            return "Up", str(int(response_time*1000)), "0"
        else:
            return "Down", "NA", "100"
    except Exception as e:
        traceback.print_exc()
        return "Down", "NA", "100"


# ip = "192.168.30.186"


# def ping(ip):
    # from sys import platform
    # import subprocess
    # import re
#         status = None
#         if platform == "linux" or platform == "darwin":
#             command=["ping", "-c", "3", "-i", "0.2", ip]
#             timeout=2
#         else:
#             command=["ping", "-n", "1", ip]
#             timeout=2
        

#         proc=subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        


#         try:

#             [out, err]=proc.communicate(timeout=timeout)

#             if proc.returncode == 0:
#                 status = 0
#                 if platform == "linux" or platform == "darwin":
#                     # rtt min/avg/max/mdev = 578.263/917.875/1013.707/132.095 ms
#                     avgRTT=re.search("rtt min/avg/max/mdev = (\d+.\d+)/(\d+.\d+)/(\d+.\d+)/(\d+.\d+)", str(out)).group(2)
#                     return avgRTT,status
#                 else:
#                     # Approximate round trip times in milli-seconds: Minimum = 63ms, Maximum = 64ms, Average = 63ms
#                     print(out)
#                     packet_loss=re.search("Lost = (\d+)", str(out)).group()[-1]
#                     avgRTT=re.search("Average = (\d+)", str(out)).group()
#                     favg = re.search('\d+',avgRTT).group()
#                     return favg,status,packet_loss
#         except subprocess.TimeoutExpired:
#             proc.kill()


# res = ping(ip)

# print(res[0])