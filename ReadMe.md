# Events

标签（空格分隔）： 未分类

---
## 概述
Events是一个使用Python实现的简单的支持文件事件和事件事件的时间驱动库。

## 分支
>* master：普通模式，性能表现一般
>* mul_thread：使用线程池实现了文件事件处理
>* alone_proc：简化事件结构，性能接近于直接使用Python下的Epoll

## 测试数据

---
## 100Mb/s网卡测试：
|Python 原始Epoll|Events|Redis AE|
|------|------|------|
| 3200/s  |  2800/s | 3800/s  |
附注：
>* 本次测试为初步测试，仅仅记录下大概结果，详细信息未记录
>* 单位为连接/每秒，每次连接包含client向server发送的100bytes数据和server回应client的数据，数据容量同样为100bytes
>* 经过line_profiler显示，主要耗时操作为recv，send，register，modify，unregister，close等操作，此类操作由Python提供底层支持，不作为优化对象

## 线程池100Mb/s网卡测试：
>* 速度：800/s 

附注：
>* Events poll出socket后，使用线程池中的线程执行所有文件事件
>* line_profiler显示，每一次锁操作耗时约为send操作的1/4，为了保证并发同步，在多处使用了锁，这应该是使用线程池后性能不升反降的主要原因
>* 使用线程池后，由于每次并发需要等待最慢线程执行完毕，故而性能仍然受到个体最长阻塞时间影响
>* recv，send操作阻塞已经较小，阻塞占用时间比可能较低，比普通recv，send更偏向于cpu计算，使用线程池并不合适
>* Event 每次只poll出少量的socket，测试中大部分情况下poll出1-3个socket，也使得线程池的意义进一步降低

## 连接合并（0.1s）100Mb/s测试：
>* 速度：80/s

附注：
>* 经测试，延时不会带来连接合并，在延长的时间中，poll会维持已经抛出的socket，不会增加新的socket

## 统一proc 测试：

### 测试环境：
网卡：
>* Speed: 1000Mb/s
>* Duplex: Full

CPU:
>* Intel(R) Core(TM) i3-3220 CPU @ 3.30GHz
>* 单CPU 四核

内存：
>* 3895024 kB

原始Epoll
``` 
{'complete': 6960000, 'timespan': 345.9557659626007, 'start time': 1457873821.45116, 'connections': 6960002, 'end time': 1457874167.406926, 'speed': 20118.178925661858}
```

未使用统一proc Events：
```
{'complete': 2796201, 'timespan': 213.3290979862213, 'start time': 1457878038.713266, 'connections': 2796204, 'end time': 1457878252.042364, 'speed': 13107.45241223775}
```

使用统一proc Events:
```
{'complete': 1841263, 'timespan': 101.5847761631012, 'start time': 1457874398.415248, 'connections': 1841265, 'end time': 1457874500.000024, 'speed': 18125.383246833448}
{'complete': 1895690, 'timespan': 104.58472299575806, 'start time': 1457874398.415248, 'connections': 1895692, 'end time': 1457874502.999971, 'speed': 18125.878672326635}
{'complete': 1949934, 'timespan': 107.58474111557007, 'start time': 1457874398.415248, 'connections': 1949936, 'end time': 1457874505.999989, 'speed': 18124.633472932142}
{'complete': 6000000, 'timespan': 333.00359416007996, 'start time': 1457874398.415248, 'connections': 6000000, 'end time': 1457874731.418842, 'speed': 18017.823546720363}
```

Redis AE:
```
start:1457875796, end:1457875832
complete:1361379, speed:37816.082031
```

```
start:1457875567, end:1457875753
complete:6000000, speed:32258.064453
```

```
start:1457875263, end:1457875522
complete:5091596, speed:19658.671875
start:1457875263, end:1457875529
complete:5094438, speed:19152.023438
```

附注：
>* 使用统一proc后的事件驱动的性能得到了一定增长，几乎接近于原始Epoll的性能了
>* Redis AE性能表现最好，但是性能表现不稳定，且存在明显的连接丢失




