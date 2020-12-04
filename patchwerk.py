import random

SPELL_COST = 432
MP5 = 40
MANA_POISON_MANA = 2000
DARK_RUNE_MANA = 1000
MANA_POISON_CD = 120
DARK_RUNE_CD = 120
MAX_MANA = 10000
MANA_TOTEN_MANA = 1000
MISS_RATE = 0.33


def patchwerk():
    mana_left = MAX_MANA
    mana_poison_cd_flag = False
    dark_rune_cd_flag = False
    mana_poison_timing = 0.0
    dark_poison_timing = 0.0
    start = 3.0
    end = 3.0 + 3.6
    count = 0
    while True:
        count = count + 1
        print("第%d轮仇恨打击周期，开始时间:%.2f, 结束时间:%.2f,当前蓝量:%d" % (count, start, end, mana_left))
        # 判断大蓝cd是否转好
        if mana_poison_cd_flag:
            if start - mana_poison_timing > MANA_POISON_CD:
                mana_poison_cd_flag = False

        # 判断符文cd是否转好
        if dark_rune_cd_flag:
            if start - dark_poison_timing > DARK_RUNE_CD:
                dark_rune_cd_flag = False

        # mana_left = mana_left - SPELL_COST
        # 如果大蓝cd转好且蓝量下了2000，使用大蓝
        if MAX_MANA - mana_left > MANA_POISON_MANA and not mana_poison_cd_flag:
            mana_left = mana_left + MANA_POISON_MANA
            print("使用大蓝，回复%d法力" % MANA_POISON_MANA)
            mana_poison_cd_flag = True
            mana_poison_timing = start

        if MAX_MANA - mana_left > DARK_RUNE_MANA and not dark_rune_cd_flag:
            mana_left = mana_left + DARK_RUNE_MANA
            print("使用符文，回复%d法力" % DARK_RUNE_MANA)
            dark_rune_cd_flag = True
            dark_poison_timing = start

        # 计算5回，在这个区间内如果有5的倍数，回一次蓝
        if if_mp5(start, end):
            if MAX_MANA - mana_left > MP5:
                mana_left = mana_left + MP5
                print("该区间内触发一次5回，回复%d法力" % MP5)

        # 在这个start到end的3.6秒区间，释放一次N级治疗波
        if random.random() < MISS_RATE:
            print("本次仇恨打击miss")
        else:
            if mana_left > SPELL_COST:
                mana_left = mana_left - SPELL_COST
                print("释放一次治疗技能，消耗%d法力，剩余法力%d" % (SPELL_COST, mana_left))
            else:
                print("当前蓝量已无法支持继续治疗")
                break
        start = start + 3.6
        end = end + 3.6


def if_mp5(start, end):
    if int(start) == start:
        start_int = int(start)
    else:
        start_int = int(start + 1.0)
    result = False
    end_int = int(end)
    for i in range(start_int, end_int):
        if i % 5 == 0:
            result = True
            break

    return result


if __name__ == '__main__':
    patchwerk()