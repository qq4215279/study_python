# coding:utf-8
from enhance_gameserveruse import *
from request_wrapper import *
import time
import sched


def test():
    name_fmt = "auto_move_"

    for i in range(500):
        try:
            content = Content()
            task = Task(name_fmt + str(i), "1", ifCreateUser=True)

            # 获取编队信息
            task.addCommand("world@enter", {"id": "6"}, request_wrapper.TroopArrayWrapper(content))

            # 获取玩家城信息
            task.addCommand("world@getBirth", {}, PlayerCityReferencePointWrapper(content))

            # 行军
            task.addCommand("world@marchMultiple", {}, MoveWrapper(content))

            # 行军
            task.addCommand("world@marchMultiple", {}, MoveWrapper(content))

            # 行军
            task.addCommand("world@marchMultiple", {}, MoveWrapper(content))

            task.start()
        except ValueError:
            print 'ValueError'
        else:
            print 'success'


s = sched.scheduler(time.time, time.sleep)


def run(inc):
    s.enter(inc, 0, run, (inc,))
    test()


def my_main(inc=10):
    s.enter(inc, 0, run, (inc,))
    s.run()


if __name__ == '__main__':
    test()
    my_main()
