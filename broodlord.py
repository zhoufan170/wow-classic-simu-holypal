# -*- coding: utf-8 -*
import random
import time

# 单次击退仇恨减少比例
THREAT_REDUCE_RATE = 0.3
# 当前boss坦克在两次击退间隔期间输出仇恨
TANK_THREAT = 10000.0
# 非当前boss坦克在两次击退期间输出仇恨
# 由于目前观察了几份wcl，只要第一次击退打中mt，副t必然能接手（不考虑副t手法问题）
# 所以设定副t在非坦克阶段是可以超过主t仇恨的70%，按照110% ot理论，设定为8000
UNTANK_THREAT = 8000.0

# 坦克配装两种模型，第一种高三围，第二种低三围，下面是两种模型击退的miss几率
KNOCK_MISS_RATE_HIGH = 33
KNOCK_MISS_RATE_LOW = 25

# 最大击退施放次数
MAX_KNOCK_TIMES = 5


# 判断是否击退
def check_knock(high_rate):
    if random.random() * 100 < (KNOCK_MISS_RATE_HIGH if high_rate else KNOCK_MISS_RATE_LOW):
        return False
    else:
        return True


def battle(high_rate):
    # 单次模拟高三围仇恨
    knock_times = 0
    mt_flag = True
    mt_threat = 0.0
    st_threat = 0.0
    knock_list = list()
    while knock_times < MAX_KNOCK_TIMES:
        # 这一段解释一下，以当前t为mt为例
        # 在击退之前，mt（当前boss t）增加了10000仇恨，非boss t增加了8000仇恨
        # 击退开始，计算概率，如果命中，mt仇恨降低30%
        # 此时判断非当前t是否超过当前t仇恨110%，超过换t
        if mt_flag:
            mt_threat = mt_threat + TANK_THREAT
            st_threat = st_threat + UNTANK_THREAT
            if check_knock(high_rate):
                print("第%d次击退，mt被击退，仇恨减少百分之30" % (knock_times + 1))
                knock_list.append(1)
                mt_threat = mt_threat * (1 - THREAT_REDUCE_RATE)
            else:
                print("第%d次击退，mt击退miss" % (knock_times + 1))
                knock_list.append(0)
            print("第%d次击退后，mt仇恨%.2f, st仇恨%.2f" % (knock_times + 1, mt_threat, st_threat))
            if st_threat > mt_threat * 1.1:
                mt_flag = False
                print("st ot，当前boss坦为st")
        else:
            mt_threat = mt_threat + UNTANK_THREAT
            st_threat = st_threat + TANK_THREAT
            if check_knock(high_rate):
                print("第%d次击退，st被击退，仇恨减少百分之30" % (knock_times + 1))
                knock_list.append(1)
                st_threat = st_threat * (1 - THREAT_REDUCE_RATE)
            else:
                print("第%d次击退，st击退miss" % (knock_times + 1))
                knock_list.append(0)
            print("第%d次击退后，mt仇恨%.2f, st仇恨%.2f" % (knock_times + 1, mt_threat, st_threat))
            if mt_threat > st_threat * 1.1:
                mt_flag = True
                print("mt ot，当前boss坦为mt")

        knock_times = knock_times + 1
        distribute = ""
    for knock_hit in knock_list:
        distribute = distribute + str(knock_hit)
    print("五次击退分布：" + distribute)
    return mt_threat + st_threat, distribute


def simulation():
    high_list = list()
    low_list = list()
    simulation_times = 10000
    simu = 0
    high_distribute = dict()
    low_distribute = dict()
    while simu < simulation_times:
        high_threat, high_knock_distribute = battle(True)
        low_threat, low_knock_distribute = battle(False)
        high_list.append(high_threat)
        low_list.append(low_threat)
        count = high_distribute.get(high_knock_distribute)
        high_distribute[high_knock_distribute] = 1 if not isinstance(count, int) else count + 1
        count = low_distribute.get(low_knock_distribute)
        low_distribute[low_knock_distribute] = 1 if not isinstance(count, int) else count + 1
        simu = simu + 1
        print("=============================================================================================")
    index = 0
    high = 0.0
    low = 0.0
    while index < 10000:
        high = high + high_list[index]
        low = low + low_list[index]
        index = index + 1
    print("全部样本：")
    print("高三围坦克组总体仇恨值%s" % str(round(high / 10000.0, 2)))
    print("低三围坦克组总体仇恨值%s" % str(round(low / 10000.0, 2)))
    up = str(round((high - low) * 100.0 / low, 3))
    print("全部样本，高三围提高仇恨百分之%s" % up)

    high_list.sort()
    low_list.sort()
    start = 9000
    end = 10000
    top_10_high = 0.0
    top_10_low = 0.0
    while start < end:
        top_10_high = top_10_high + high_list[start]
        top_10_low = top_10_low + low_list[start]
        start = start + 1
    print("前10%样本下：")
    print("高三围坦克组总体仇恨值%s" % str(round(top_10_high / 1000.0, 2)))
    print("低三围坦克组总体仇恨值%s" % str(round(top_10_low / 1000.0, 2)))
    up = str(round((top_10_high - top_10_low) * 100.0 / top_10_low, 3))
    print("仇恨最高的极限样本（前百分之10）下，高三围仇恨提升了百分之%s" % up)
    high_keys = list()
    for key in high_distribute.keys():
        high_keys.append(key)
    high_keys.sort()
    for key in high_keys:
        print(high_distribute[key])
    print("========================================================================")
    low_keys = list()
    for low_key in low_distribute.keys():
        low_keys.append(low_key)
    low_keys.sort()
    for low_key in low_keys:
        print(low_distribute[low_key])
    print(low_distribute)

if __name__ == '__main__':
    simulation()




