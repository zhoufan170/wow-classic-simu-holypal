# wow-classic-simu-holypal
魔兽世界经典怀旧服-奶骑模拟

目前只做了无限圣光闪现的模拟

MAX_MANA = 4800 最大法力值

FLASH_MANA = 140 圣光闪现消耗

CRI_RATE = 24 暴击几率

MP5 = 25 + 36 5回（依据了我自己装备的龙鳞+火蜥蜴，再加上智慧祝福）

BASIC_HEAL  圣光闪现基础治疗量 343-384

HEAL_POWER = 578 治疗效果

INCREASE = 0.12 天赋12%治疗量提高

单次治疗量计算：int((random.randrange(343, 384) + HEAL_POWER * (1.5/3.5)) * (1 + INCREASE))

模拟方法：clone仓库后，代码里将这些属性调整为自己所需要的，保存后输入python3 pal.py