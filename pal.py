#!/usr/local/bin/python3
# -*- coding: utf-8 -*

import random
import time
MAX_MANA = 4800
FLASH_MANA = 140
CRI_RATE = 24
MP5 = 25 + 36
BASIC_HEAL = (343 + 384) / 2
HEAL_POWER = 578
INCREASE = 0.12


def main():
    clock = 0
    flash_count = 0
    heal_per = (1 + INCREASE) * (BASIC_HEAL + HEAL_POWER * (1.5/3.5))
    print(heal_per)
    casting = False
    mana = MAX_MANA
    total_heal = 0
    total_mp5 = 0
    total_crit_restore = 0
    crit_count = 0
    
    print("begin to cast flash of light")
    while True:
        if int(10 * clock) % 50 == 0:
            mana = mana + MP5
            mp5 = MP5
            if mana > MAX_MANA:
                mp5 = mp5 - (mana - MAX_MANA)
                mana = MAX_MANA
            print ("第%.1f秒，通过5回回复了%d法力" % (clock, mp5))
            total_mp5 = total_mp5 + mp5
        if int(10 * clock) % 15 == 0:
            if casting:
                mana = mana - FLASH_MANA
                crit = random.random()
                heal = int((random.randrange(343, 384) + HEAL_POWER * (1.5/3.5)) * (1 + INCREASE))
                if crit * 100 < CRI_RATE:
                    mana = mana + FLASH_MANA
                    crit_restore = FLASH_MANA
                    if mana > MAX_MANA:
                        crit_restore = crit_restore - (mana - MAX_MANA)
                    print ("第%.1f秒，通过暴击回蓝回复了%d法力" % (clock, crit_restore))
                    total_crit_restore = total_crit_restore + crit_restore
                    heal = int(heal * 1.5)
                    crit_count = crit_count + 1
                if flash_count > 0:
                    total_heal = total_heal + heal 
                    hps = int(total_heal / clock)
                    print ("第%.1f秒，第%d次圣光闪现施法完成, 治疗%d点伤害, 当前法力值%d, 当前总治疗量%d, 当前hps %d" % (clock, flash_count, heal, mana, total_heal, hps))
                casting = False

            if not casting:
                if mana < FLASH_MANA:
                    print("oom了，总治疗时间%.1f秒，总治疗量%d，施放圣光闪现%d次，暴击%d次，通过5回回复%d法力，通过暴击回复%d法力" % (clock, total_heal, flash_count, crit_count, total_mp5, total_crit_restore))
                    return
                flash_count = flash_count + 1
                print ("第%.1f秒，开始施放第%d次圣光闪现" % (clock, flash_count))
                casting = True
        time.sleep(0.01)
        clock = clock + 0.5
            



if __name__ == '__main__':
   main()
