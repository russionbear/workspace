#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @FileName  :politicsG.py
# @Time      :2022/1/9 15:07
# @Author    :russionbear

import random
import os
import pickle


PRI_MAP_PATH = r'./suitang_primary_path'
MAP_FILEPATH = r'./suitang_map'
SAVE_FILEPATH = r'./suitang_save'

MapMode = {
  "__tip for map": "sea = 1   river = 2   plain = 3   mountain = 4   beach = 5  tree = 6",
  "__tip for person1": "none = 0  sword = 1 arrow = 2 catapult = 3 mount = 4",
  "__tip for person2": "!!!warn:weapons <= troop <= 30000",
  "__tip for person3": {
    "__tip": "",
    "name" : "key",
    "loyal" : "",
    "wise" : "",
    "force" : "",
    "troop" : "",
    "weapons" : "",
    "weaponType" : "",
    "dsc" : ""
  },
  "__tip for persons": "",
  "__tip for city1": "max: Population = 200000  Money = 300000  Treasure = 100",
  "__tip for city2": {
    "__tip": "",
    "loc": "key",
    "header": "",
    "name": "",
    "population": "",
    "perTreasure": "",
    "tax": "",
    "growth": "",
    "natality": "",
    "officer": "",
    "prisoner": "",
    "restTroop": "",
    "weapons": "",
    "money":""
  },
  "__tip for force": {
    "__tip": "",
    "name":  "key",
    "header": "",
    "cities": "type:list"
  },
  # "map": [
  #   [4,3,1,2,5,5,3],
  #   [3,3,3,3,3,3,3],
  #   [3,3,3,3,3,3,3],
  #   [3,3,3,3,3,3,3],
  #   [3,3,3,3,3,3,3],
  #   [3,3,3,3,3,3,3]
  # ],
  "__run test": "load json",
  "personName": [
    "叶俊友",
    "方经国",
    "宋正真",
    "易志明",
    "廖阳辉",
    "石安澜",
    "熊宏阔",
    "郝子瑜",
    "万修文",
    "刘彭湃",
    "史雨石",
    "杨敏智",
    "丁志业",
    "钱修诚",
    "孟乐安",
    "谢子轩",
    "杨英勋",
    "汤正信",
    "顾俊智",
    "胡华荣",
    "高俊迈",
    "罗高阳",
    "赵敏智",
    "黄浩博",
    "段勇捷",
    "蔡伟志",
    "李俊楚",
    "苏雅懿",
    "卢乐天",
    "贾鹏涛",
    "姚嘉实",
    "萧博文",
    "潘才英",
    "贺阳德",
    "梁雅惠",
    "李泽语",
    "卢永思",
    "杨欣悦",
    "卢飞驰",
    "郝英光",
    "赖乐悦",
    "康博简",
    "邓明辉",
    "苏宏峻",
    "廖良翰",
    "马文乐",
    "郭学林",
    "夏意智",
    "夏咏思",
    "阎文成",
    "侯国兴",
    "朱文宣",
    "戴睿聪",
    "萧玉轩",
    "马绍元",
    "白自强",
    "郝涵衍",
    "杜峻熙",
    "周奇致",
    "白鹏鲸",
    "于雅逸",
    "韩安澜",
    "邱高阳",
    "李才艺",
    "余华晖",
    "马嘉祥",
    "江志行",
    "顾华晖",
    "王和裕",
    "武乐欣",
    "胡高旻",
    "石才良",
    "薛坚成",
    "周祺祥",
    "林景澄",
    "冯阳夏",
    "段志学",
    "潘天路",
    "乔弘方",
    "漕星辰",
    "叶巍然",
    "董光霁",
    "董温茂",
    "田志诚",
    "宋鸿朗",
    "潘文耀",
    "文乐天",
    "夏建安",
    "乔宏放",
    "漕和昶",
    "易彬彬",
    "宋滨海",
    "于修雅",
    "赵泰和",
    "罗向阳",
    "孟修然",
    "顾阳州",
    "许志行",
    "康俊民",
    "周和畅",
    "邓烨华",
    "贺德水",
    "韩嘉荣",
    "崔志新",
    "龚振海",
    "李高达",
    "何博涛",
    "江阳华",
    "李英奕",
    "徐承宣",
    "曹英博",
    "曹飞扬",
    "薛康盛",
    "苏和豫",
    "曹嘉玉",
    "方乐圣",
    "武烨磊",
    "江天工",
    "刘元正",
    "唐逸明",
    "万星华",
    "金鸿博",
    "孙高扬",
    "石乐人",
    "段弘致",
    "徐子瑜",
    "史凯风",
    "宋天和",
    "萧和豫",
    "赵乐水",
    "黄子真",
    "程修德",
    "龚鸿志",
    "朱良畴",
    "邵宏义",
    "谭经国",
    "白俊誉",
    "段宏富",
    "邹立轩",
    "彭心远",
    "易元化",
    "孔昊然",
    "朱越彬",
    "吕伟泽",
    "戴华彩",
    "叶高雅",
    "余经纶",
    "邱鹏鲲",
    "金经义",
    "江英资",
    "石承载",
    "叶鹤轩",
    "邵乐正",
    "傅鸿彩",
    "赖信然",
    "毛英叡",
    "常高歌",
    "范英毅",
    "梁永望",
    "邱季萌",
    "黄高远",
    "薛刚捷",
    "邱雪松",
    "万英逸",
    "袁雅志",
    "梁高畅",
    "王俊哲",
    "彭宏毅",
    "秦泰和",
    "谢雅志",
    "康凯复",
    "钟泰平",
    "赖元德",
    "叶弘方",
    "潘浩初",
    "朱凯歌",
    "蒋嘉茂",
    "谢阳飙",
    "叶鸿祯",
    "萧凯泽",
    "戴飞鸾",
    "阎阳晖",
    "陈子濯",
    "阎勇毅",
    "萧敏才",
    "阎安怡",
    "杜星津",
    "卢展鹏",
    "邵鹏涛",
    "卢飞飙",
    "田元德",
    "侯坚秉",
    "谭敏智",
    "吴涵畅",
    "易弘扬",
    "郑志新",
    "蔡和怡",
    "蔡阳飙",
    "萧祺瑞",
    "冯鸿达"
  ],
  "cityName": [
    "朐故道",
    "项嘉城",
    "化皋州",
    "大东乡",
    "首湖区",
    "淮陟崖",
    "饶华谷",
    "青临村",
    "川农郡",
    "蒙丘峰",
    "平大岛",
    "花河县",
    "定昌坡",
    "汉头镇",
    "泉洋庄",
    "林行堡",
    "棣城港",
    "上兴区",
    "安南港",
    "湖东坡",
    "大桥郡",
    "安鹤堡",
    "湖绥堡",
    "南沧道",
    "门作镇",
    "武新港",
    "镇清区",
    "三清郡",
    "大东堡",
    "安南庄"
  ],
  "forceName": [
    "幻燕联盟",
    "龙兽公国",
    "神翔帝国",
    "暗元国",
    "承赵联邦",
    "玄夏联盟",
    "魔魏联盟",
    "宙辉国",
    "龙兽公国",
    "神元联盟",
    "玄夏国",
    "宙辉国",
    "承赵帝国",
    "暗元公国",
    "魔魏国",
    "天澜公国",
    "承赵联盟",
    "玄夏联邦",
    "魔魏联盟",
    "魔魏公国",
    "玄夏帝国",
    "魔魏帝国",
    "神元国"
  ],
  "auto": False,
  "person": {
    "刘备": {
    "loyal" : 99,
    "wise" : 90,
    "force" : 90,
    "troop" : 20000,
    "weapons" : 20000,
    "weaponType" : 3,
    "dsc" : "奸雄"
    },
    "曹操": {
    "loyal" : 99,
    "wise" : 99,
    "force" : 80,
    "troop" : 2000,
    "weapons" : 2000,
    "weaponType" : 3,
    "dsc" : "英雄"
    },
    "张飞": {
    "loyal" : 99,
    "wise" : 0,
    "force" : 99,
    "troop" : 2000,
    "weapons" : 2000,
    "weaponType" : 3,
    "dsc" : "英雄"
    },
    "关羽": {
    "loyal" : 10,
    "wise" : 0,
    "force" : 99,
    "troop" : 2000,
    "weapons" : 2000,
    "weaponType" : 3,
    "dsc" : "英雄"
    },
    "诸葛亮": {
    "loyal" : 99,
    "wise" : 99,
    "force" : 0,
    "troop" : 2000,
    "weapons" : 2000,
    "weaponType" : 3,
    "dsc" : "英雄"
    }
  },
  "city": {
    "许昌": {
    "population": 200000,
    "perTreasure": 5.0,
    "officer": ["曹操", "关羽", "诸葛亮"],
    "prisoner": [],
    "restTroop": 0,
    "weapons": {},
    "money":100000
    },
    "邺城": {
    "population": 200000,
    "perTreasure": 5.0,
    "officer": ["张飞"],
    "prisoner": [],
    "restTroop": 0,
    "weapons": {},
    "money":1000
    },
    "成都": {
    "population": 200000,
    "perTreasure": 5.0,
    "officer": ["刘备"],
    "restTroop": 0,
    "weapons": {},
    "money":1000
    }
  },
  "force": {
    "魏国": {
    "cities": ["0-0", "1-0"]
    },
    "蜀国": {
    "cities": ["0-1"]
    }
  }
}



class Geo:
    sea = 0x1
    mountain = 0x2
    river = 0x3
    plain = 0x4
    # beach = 0x5
    tree = 0x5
    ranges = 1, 6, 2
    color = {
        1: 44,
        2: 43,
        3: 46,
        4: 42,
        # 5: 46,
        5: 41
    }


"""
选择地图
"""


class Console:
    def __init__(self):
        colorama.init(True)
        self.map_ = []
        self.bg = []
        self.fg = 30
        self.width = 80
        self.height = 60
        self.indent = 0

    def set_bg(self, d0):
        self.bg = d0

    def set_map(self, map_):
        indent = 0
        self.map_ = map_
        for i in map_:
            for j in i:
                # k0 = 0
                # for k in j:
                #     if u'\u4e00' <= k <= u'\u9fa5':
                #         k0 += 2
                #     else:
                #         k0 += 1
                # indent = max(indent, k0)
                indent = max(indent, len(j))
        self.indent = indent + 2
        print(self.indent)

    @staticmethod
    def aligns(s0):
        new_string = ''
        for i in s0:
            codes = ord(i)
            if codes <= 126:
                new_string = new_string + chr(codes + 65248)
            else:
                new_string = new_string + i
        return new_string

    def print_map(self):
        # os.system('mode con cols=%d lines=%d' % (self.height, self.width))
        for i in range(len(self.map_[0])+1):
            # print(f'{str(i-1).center(self.indent)}', end='')
            # print(self.aligns(str(i-1)), end='')
            print(f'{self.aligns(str(i-1)).center(self.indent, "　")}', end='')
        print()
        for i, i1 in enumerate(self.map_):
            # print(f'{str(i).center(self.indent)}', end='')
            # print(self.aligns(str(i), self.indent), end='')
            print(f'{self.aligns(str(i)).center(self.indent, "　")}', end='')
            for j, j1 in enumerate(i1):
                # print(f'\033[1;{Geo.color[self.bg[i][j]]};{self.fg}m{j1.center(self.indent, " ")}', end='')
                # print(f'\033[1;{Geo.color[self.bg[i][j]]};{self.fg}m{self.aligns(j1, self.indent)}', end='')
                print(f'\033[1;{Geo.color[self.bg[i][j]]};{self.fg}m{self.aligns(j1).center(self.indent, "　")}', end='')
            print()

    @staticmethod
    def skim_files(path, rows=3, cols=4):
        gg0 = {'point': 0, 'end': False}
        files = os.listdir(path)
        if not files:
            print('empty')
            return
        length = len(files)
        step = rows * cols
        for i in range(0, length):
            if i and not i % cols:
                print()
            print(files[i], end='\t')
        print()
        print('a:turn left b:turn right esc:back')

        def run(e0: keyboard.KeyboardEvent):
            # global point, end
            # print(e0.name)
            if e0.event_type == 'down':
                if e0.name == 'd':
                    os.system('cls')
                    if gg0['point'] + step + 1 >= length:
                        return
                    gg0['point'] += step
                    os.system('cls')
                    top = gg0['point'] + 12
                    if top > length:
                        top = length
                    it = 0
                    for i in range(gg0['point'], top):
                        print(str(i)+'.'+files[i], end='')
                        it += 1
                        if not it % cols:
                            print()
                    print('page:%d' % ((gg0['point']+step-1)//step))
                elif e0.name == 'a':
                    os.system('cls')
                    if gg0['point'] - step < 0:
                        return
                    gg0['point'] -= step
                    os.system('cls')
                    top = gg0['point'] + 12
                    if top > length:
                        top = length
                    it = 0
                    for i in range(gg0['point'], top):
                        print(str(i)+'.'+files[i], end='')
                        it += 1
                        if not it % cols:
                            print()
                    print('page:%d' % ((gg0['point'] + step - 1) // step))
                elif e0.name == 'esc':
                    os.system('cls')
                    keyboard.unhook_all_hotkeys()
                    gg0['end'] = True

        keyboard.hook(run)
        while not gg0['end']:
            pass
        # keyboard.unhook_all_hotkeys()
        keyboard.unhook_all()

    @staticmethod
    def skim_data(data, step=3):
        if not data:
            print('empty')
            return
        gg0 = {'point': 0, 'end': False}
        keys = list(data.keys())
        length = len(keys)
        for i in keys[:step]:
            print('--' + i + '--')
            print(data[i])
            print()

        print('a:turn left b:turn right esc:back')

        def run(e0: keyboard.KeyboardEvent):
            if e0.event_type == 'down':
                if e0.name == 'd':
                    if gg0['point'] + step + 1 >= length:
                        return
                    os.system('cls')
                    gg0['point'] += step
                    os.system('cls')
                    top = gg0['point'] + step
                    if top > length:
                        top = length
                    for i in range(gg0['point'], top):
                        print('--'+keys[i]+'--')
                        print(data[keys[i]])
                        print()

                    print('page:%d' % ((gg0['point']+step-1)//step))
                elif e0.name == 'a':
                    if gg0['point'] - step < 0:
                        return
                    os.system('cls')
                    gg0['point'] -= step
                    os.system('cls')
                    top = gg0['point'] + step
                    if top > length:
                        top = length
                    for i in range(gg0['point'], top):
                        print('--'+keys[i]+'--')
                        print(data[keys[i]])
                        print()

                    print('page:%d' % ((gg0['point'] + step - 1) // step))
                elif e0.name == 'esc':
                    os.system('cls')
                    keyboard.unhook_all_hotkeys()
                    gg0['end'] = True

        keyboard.hook(run)
        while not gg0['end']:
            pass

        keyboard.unhook_all()


class Top:
    Troops = 20000
    Population = 400000
    Money = 200000
    Treasure = 10
    Loyal = 99
    Wise = 99
    Force = 99


class Weapon:
    none = 0
    sword = 1
    arrow = 2
    catapult = 3
    mount = 4
    ChineseName = {
        none: "徒手",
        sword: "剑",
        arrow: "弓",
        catapult: "攻城车",
        mount: "骑装"
    }
    price = {
        sword: 1,
        arrow: 1,
        catapult: 100,
        mount: 50
    }


class Person:
    def __init__(self):
        # self.id = None
        self.name = ''
        self.dsc = ''
        self.belong = 1

        self.loyal = random.randint(0, Top.Loyal)
        self.wise = random.randint(0, Top.Wise*2)
        self.force = random.randint(0, Top.Force*2)
        self.wise = self.wise // 2 if self.wise > Top.Wise else self.wise
        self.force = self.force // 2 if self.force > Top.Force else self.force

        self.troop = 0
        self.weapons = 0
        self.weaponType = 0

    @classmethod
    def load_obj(cls, d0):
        """
        no name
        :param d0:
        :return:
        """
        obj = cls()
        # int 1, float 2, str 3, list 4, dict 5
        keys = {
            "loyal": 1,
            "wise": 1,
            "force": 1,
            "troop": 1,
            "weapons": 1,
            "weaponType": 1,
            "dsc": 3
        }
        for k, v in keys.items():
            if k not in d0:
                continue

            setattr(obj, k, d0[k])

            if v == 1:
                if not isinstance(d0[k], int):
                    return False
            elif v == 2:
                if not isinstance(d0[k], float):
                    return False
            elif v == 3:
                if not isinstance(d0[k], str):
                    return False
            elif v == 4:
                if not isinstance(d0[k], list):
                    return False
                else:
                    setattr(obj, k, list(d0[k]))
            elif v == 5:
                if not isinstance(d0[k], dict):
                    return False

        return obj

    def obj_info(self):
        info = 'name:{}\tloyal:{}\twise:{}\tforce:{}\tbelong:{}\ntroop:{},weapon:{}-{}\ndsc:{}'
        return info.format(self.name, self.loyal, self.wise, self.force, self.belong, \
                           self.troop, Weapon.ChineseName[self.weaponType], self.weapons, self.dsc)


class City:
    def __init__(self):
        self.name = ''
        self.header = None

        self.population = random.randint(Top.Population//5, Top.Population//2)
        self.perTreasure = random.randint(1, 4)
        self.tax = 0.05
        self.growth = 0.03
        self.natality = 0.01

        self.officer = set()
        self.prisoner = set()
        self.restTroop = Top.Troops
        self.weapons = {}
        self.money = random.randint(1, Top.Money//10)

        self.convey = {}

    def update(self):
        # 控制度
        if self.header.wise > Top.Wise * 0.8:
            self.growth = 0.1
            self.natality = 0.05
            self.tax = 0.002
        elif self.header.wise > 0.6:
            self.growth = 0.5
            self.natality = 0.03
            self.tax = 0.001
        else:
            self.growth = 0.3
            self.natality = 0.02
            self.tax = 0.0005

        # 经济

        self.perTreasure += self.perTreasure * self.growth
        if self.perTreasure > Top.Treasure:
            self.perTreasure = Top.Treasure

        self.money += self.population * self.perTreasure * self.tax
        if self.money > Top.Money:
            self.money = Top.Money
        else:
            self.money = int(self.money)

        # 人口

        self.population += int(self.population * self.natality)
        if self.population > Top.Population:
            self.population = Top.Population

    @classmethod
    def load_obj(cls, d0):
        """
        no officer
        :param d0:
        :return:
        """
        obj = cls()
        # int 1, float 2, str 3, list 4, dict 5
        keys = {
            "header": 1,
            "population": 1,
            "perTreasure": 2,
            "officer": 4,
            "prisoner": 4,
            "restTroop": 1,
            "weapons": 5,
            "money": 1
        }
        if 'officer' not in d0:
            return False
        for k, v in keys.items():
            if k not in d0:
                continue

            setattr(obj, k, d0[k])

            if v == 1:
                if not isinstance(d0[k], int):
                    return False
            elif v == 2:
                if not isinstance(d0[k], float):
                    return False
            elif v == 3:
                if not isinstance(d0[k], str):
                    return False
            elif v == 4:
                if not isinstance(d0[k], list):
                    return False
                else:
                    setattr(obj, k, list(d0[k]))
            elif v == 5:
                if not isinstance(d0[k], dict):
                    return False

        return obj

    def obj_info(self, careful='whneop'):
        """

        :param careful: h:header, n:big number, e:economic, o:officer, p:prisoner
        :return:
        """
        if 'h' in careful:
            header = self.header.name
        else:
            header = "?"

        if 'n' in careful:
            troop = 0
            for i in self.officer:
                troop += i.troop
            population = self.population
            natality = self.natality
            restT = self.restTroop
        else:
            troop = '?'
            population = '?'
            natality = '?'
            restT = '?'

        if 'e' in careful:
            perTreaure = self.perTreasure
            tax = self.tax
            growth = self.growth
            money = self.money
        else:
            perTreaure = "?"
            tax = "?"
            growth = "?"
            money = "?"

        if 'w' in careful:
            weapons = ''
            for k, v in self.weapons.items():
                weapons += '\t' + Weapon.ChineseName[k]+':'+str(v)
        else:
            weapons = '?'

        if 'o' in careful:
            officers = ''
            for i in self.officer:
                officers += i.name + '\t'
        else:
            officers = '?'

        if 'p' in careful:
            conveyPerson = 0

        if 'p' in careful:
            prisoner = ''
            for i in self.prisoner:
                prisoner += i.name + '\t'
        else:
            prisoner = '?'

        info = "name:{}\theader:{}\ttroop:{}\trestTroop:{}\
        \tmoney:{}\nweapons:{}\nofficers:{}\nprisoner:{}\npopulation:{}\
        \tperTreasur:{}\tnatality:{}\ttax:{}\tgrowth:{}".\
            format(self.name, header, troop, restT, money, weapons, officers, prisoner, population, perTreaure, natality, tax, growth)
        return info

    def show_person(self):
        info1 = 'officer:'
        info2 = 'prisoner:'
        it = 1
        for i in self.officer:
            info1 += str(it) + '(' + i.name + ')\t'
            it += 1

        it = 1
        for i in self.prisoner:
            info2 += str(it) + '(' + i.name + ')\t'
            it += 1

        return info1, info2

    def show_convey(self):
        cities = {}
        # for k, v in self.conveyPerson.items():
        #     if k not in cities:
        #         cities[k] = {"officer":''}
        #         for i in v:
        #             cities[k]["officer"] += i.name + '\t'
        #
        # for k, v in self.conveyWeapon.items():
        #     if k not in cities:
        #         cities[k] = {"weapons":""}
        #         for i1, i in v.items():
        #             cities[k]["weapons"] += Weapon.ChineseName[i1] + str(i) + ', '
        # for k, v in self.conveyTroop.items():
        #     if k not in cities:
        #         cities[k] = {"troop": str(v)}
        #
        # for k, v in self.conveyMoney.items():
        #     if k not in cities:
        #         cities[k] = {"mongy": str(v)}

        for k, v in self.convey.items():
            tmp_d = str(k[0]) + '-' + str(k[1])
            cities[tmp_d] = {}
            if 'weapon' in v:
                cities[tmp_d] = {"weapons":""}
                for i1, i in v['weapon'].items():
                    cities[tmp_d]["weapons"] += Weapon.ChineseName[i1] + str(i) + ', '

            if 'officer' in v:
                cities[tmp_d] = {"officer": ''}
                for i in v['officer']:
                    cities[tmp_d]["officer"] += i.name + '\t'

            if 'troop' in v:
                cities[tmp_d]['troop'] = str(v['troop'])

            if 'money' in v:
                cities[tmp_d]['money'] = str(v['money'])

        info = ''
        for k, v in cities.items():
            # tmp_d = str(k[0]) + '-' +str(k[1])
            # info += tmp_d + '\n'
            info += k + '\n'
            for i1, i in v.items():
                info += i1 + ': ' + i + '\n'
            info += '\n'
        return info[:-1]

    def make_outbreak(self):
        for i in self.officer:
            i.troop = i.troop * 4 // 5
            i.weapons = i.weapons * 4 // 5


class Force:
    def __init__(self):
        self.header = 0
        self.cities = set()
        self.name = ""

    @classmethod
    def load_obj(cls, d0):
        """
        no name
        :param d0:
        :return:
        """
        obj = cls()
        # int 1, float 2, str 3, list 4, dict 5
        keys = {
            "header": 3,
            "cities": 4
        }
        for k, v in keys.items():
            if k not in d0:
                return False

            setattr(obj, k, d0[k])

            if v == 1:
                if not isinstance(d0[k], int):
                    return False
            elif v == 2:
                if not isinstance(d0[k], float):
                    return False
            elif v == 3:
                if not isinstance(d0[k], str):
                    return False
            elif v == 4:
                if not isinstance(d0[k], list):
                    return False
                else:
                    setattr(obj, k, list(d0[k]))
            elif v == 5:
                if not isinstance(d0[k], dict):
                    return False

        return obj


class ResManager:
    def __init__(self):
        # self.geoMapName = ''
        self.citiesNameMap = {}
        self.namesCityMap = {}
        self.roadsInfo = {}

        self.citiesInfo = {}
        self.personsInfo = {}
        self.forcesInfo = {}

        self.nameStorage = {
            "city": [],
            "person": [],
            "force": []
        }

        self.myForce = 0
        self.width = self.height = 0
        # self.isOk = False
        self.failed = {}

        self.groups = {}
        self.overed = set()
        self.turn = 1
        self.nowLocation = 1, 1
        self.userSave = {}

        self.attack = {}

    def init_map(self, filepath):
        # self.citiesInfo.clear()
        # self.forcesInfo.clear()
        # self.personsInfo.clear()
        # self.failed.clear()

        with open(filepath, 'r', encoding='utf-8') as f:
            top_map = json.load(f)

        with open(PRI_MAP_PATH+'/'+top_map['geo_map']+'/points', 'rb') as f:
            tmp = pickle.load(f)

            for i in tmp['roads']:
                if i[0] not in self.roadsInfo:
                    self.roadsInfo[i[0]] = set()
                if i[1] not in self.roadsInfo:
                    self.roadsInfo[i[1]] = set()

                self.roadsInfo[i[0]].add(i[1])
                self.roadsInfo[i[1]].add(i[0])

                # if tmp['cities'][i[0]] not in self.roadsInfo:
                #     self.roadsInfo[tmp['cities'][i[0]]] = set()
                # if tmp['cities'][i[1]] not in self.roadsInfo:
                #     self.roadsInfo[tmp['cities'][i[1]]] = set()
                # self.roadsInfo[tmp['cities'][i[0]]].add(tmp['cities'][i[1]])
                # self.roadsInfo[tmp['cities'][i[1]]].add(tmp['cities'][i[0]])

        # load name and check the repeat
        check_key_1 = ['person', 'city', 'force']
        for i in check_key_1:
            self.nameStorage[i] = list(set(top_map[i+"Name"]))

        if top_map['auto']:
            cities_name = random.sample(self.nameStorage['city'], len(list(self.roadsInfo.keys())))
            it = iter(cities_name)
            for i in list(self.roadsInfo.keys()):
                self.citiesNameMap[i] = next(it)
                self.namesCityMap[self.citiesNameMap[i]] = i

            person_name = random.sample(self.nameStorage['person'], len())

            persons = []
            # effective area
            # if len(self.nameStorage['city']) > len(e_area):
            #     self.nameStorage['city'] = self.nameStorage['city'][:e_area]
            # elif len(self.nameStorage['city']) < len(e_area):
            #     random.shuffle(e_area)
            #     e_area = e_area[0:len(self.nameStorage['city'])]
            # make city

            it = iter(random.shuffle(self.nameStorage['city']))
            should_d = []
            for i in list(self.citiesNameMap.keys()):
                obj = City()
                obj.name = it.__next__()
                self.citiesInfo[i] = obj
                should_d.append(i)

            for i in should_d:
                self.nameStorage['city'].remove(i)

            # self.nameStorage['city'] = []

            l_area = len(list(self.citiesNameMap.keys()))

            # make person
            if len(self.nameStorage['person']) < l_area:
                print("map's person aren't enough")
                return False

            bak_person = []
            if len(self.nameStorage['person']) > l_area * 4:
                bak_person = self.nameStorage['person'][l_area * 4:]
                self.nameStorage['person'] = self.nameStorage['person'][l_area * 4:]

            s0 = random.sample(range(0, len(self.nameStorage['person'])-1), l_area-1)
            s0.sort()
            s0.append(len(self.nameStorage['person'])-1)
            begin = 0
            for i1, i in enumerate(list(self.citiesNameMap.values())):
                # print(begin, s0[i1]+1)
                for j in self.nameStorage['person'][begin:s0[i1]+1]:
                    obj = Person()
                    obj.name = j
                    self.personsInfo[obj.name] = obj
                    self.citiesInfo[i].officer.add(obj)
                    self.citiesInfo[i].header = obj

                # begin = s0[i1] + 1
                # if not self.citiesInfo[i].officer:
                #     print(begin, s0)
                # for j in self.citiesInfo[i].officer:
                #     self.citiesInfo[i].header = j
                #     break
            self.nameStorage['person'] = bak_person

            # force
            bak_force = []
            if len(self.nameStorage['force']) > l_area:
                self.nameStorage['force'] = self.nameStorage['force'][:l_area]
                bak_force = self.nameStorage['force'][l_area:]
            s0 = random.sample(range(0, l_area-1), len(self.nameStorage['force'])-1)
            s0.sort()
            s0.append(l_area-1)
            begin = 0
            for i1, i in enumerate(self.nameStorage['force']):
                self.forcesInfo[i] = Force()
                self.forcesInfo[i].name = i
                top_city = None
                for j in list(self.citiesNameMap.keys())[begin:s0[i1]+1]:
                    # self.citiesInfo[j].header.belong = i
                    for k in self.citiesInfo[j].officer:
                        k.belong = i
                    top_city = j
                    # self.forcesInfo[i].cities.add(j)
                # else:
                obj = Person()
                obj.name = i + '首领'
                obj.belong = i
                if obj.name in self.personsInfo:
                    print("name shouldn't be country name added '首领'")
                    return False
                self.personsInfo[obj.name] = obj
                obj.loyal = Top.Loyal
                self.citiesInfo[top_city].header = obj
                self.citiesInfo[top_city].officer.add(obj)
                self.forcesInfo[i].header = obj
                begin = s0[i1] + 1
        #
        else:
            cities = []
            persons = []
            for i, j in top_map['force'].items():
                cities.extend(j['cities'])

            should_d = []
            for i, j in top_map['city'].items():
                if i not in cities:
                    should_d.append(i)
                    continue
                persons.extend(j['officer'])
                persons.extend(j['prisoner'])

            for i in should_d:
                del top_map['city'][i]

            for i in persons:
                if i not in top_map['person']:
                    del top_map['person'][i]

            for i in persons:
                self.nameStorage['person'].remove(i)

            if len(set(cities)) < len(cities):
                print('city repeat')
                raise OSError

            if len(set(persons)) < len(persons):
                print('person repeat')
                raise OSError

            if len(cities) > len(list(self.roadsInfo.keys())):
                print('no enough cities')
                raise OSError

            if len(cities) < len(list(top_map['city'].keys())):
                print('city lost')
                raise OSError

            if len(persons) < len(list(top_map['person'].keys())):
                print('person lost')
                raise OSError

            for k, v in top_map['person'].items():
                tmp_o = Person.load_obj(v)
                self.personsInfo[k] = tmp_o
                tmp_o.name = k

            for k, v in top_map['city'].items():
                tmp_o = City.load_obj(v)
                self.citiesInfo[k] = tmp_o
                tmp_o.name = k
                tmp_o.header = v['officer'][0]

            for k, v in top_map['force'].items():
                enemies = list(top_map['force'].keys())
                enemies.remove(k)
                tmp_o = Force.load_obj(v)
                self.forcesInfo[k] = tmp_o
                tmp_o.name = k
                tmp_o.header = self.citiesInfo[v['cities'][0]].header
                for i in tmp_o.cities:
                    for j in i.officer:
                        j.belong = k
                    for j in i.prisoner:
                        j.belong = random.sample(enemies, 1)[0]

        return True

    def get_person(self):
        if not self.nameStorage['person']:
           return None
        obj = Person()
        random.shuffle(self.nameStorage['person'])
        obj.name = self.nameStorage['person'][-1]
        self.nameStorage['person'].pop()
        return obj

    def search_force(self, yx):
        for k, v in self.forcesInfo.items():
            if yx in v.cities:
                return k

    def search_city(self, obj):
        for k, v in self.citiesInfo.items():
            if obj in v.officer:
                return v

    def auto_atk(self):
        force_1 = 0
        force_2 = 0
        troop_1 = 0
        troop_2 = 0
        city = self.citiesInfo[self.attack['def']]
        for i in self.attack['atk']:
            force_1 += i.weapons * Weapon.price[i.weaponType] * i.force // 100
            troop_1 += i.troop
        for i in city.officer:
            force_2 += i.weapons * Weapon.price[i.weaponType] * i.force // 100
            troop_2 += i.troop
        force_2 *= city.header.wise * 2.2 * city.header.loyal * 2.2 // Top.Wise // Top.Loyal
        if city.header.wise > 80 and self.attack['money'] < 100 * (city.header.wise-70):
            return 'failed, money is not enough'
        if force_1 < force_2:
            for i in self.attack['atk']:
                p0 = self.search_city(i)
                i.weaponType = 0
                i.weapons = 0
                i.troop = 0
                p0.officer.remove(i)
                city.prisoner.add(i)
            per = troop_1 * 0.4 / troop_2
            for i in city.officer:
                i.troop -= int(i.troop*per)
                if i.troop < 0:
                    i.troop = 0
            if self.forcesInfo[self.myForce].header in city.prisoner:
                self.ko(self.myForce, city.header.belong)
            return 'failed, the troop were over'
        else:
            for i in self.attack['atk']:
                i.troop -= int(i.troop*0.3)
                i.weapons = int(i.weapons*0.3)
            for i in city.officer:
                i.weaponType = 0
                i.weapons = 0
                i.troop = 0
            city.prisoner = city.prisoner.union(city.officer)
            city.officer = set(self.attack['atk'])

            for i in self.attack['atk']:
                p0 = self.search_city(i)
                p0.officer.remove(i)
                # i.header = self.attack['atk'][0]
            else:
                city.header = i

            force_3 = self.search_force(self.attack['def'])
            if self.forcesInfo[force_3].header in self.citiesInfo[self.attack['def']].prisoner:
                self.ko(force_3, self.myForce)

            return 'succeed, occupied the city'

    def update(self):
        for k, v in self.citiesInfo.items():
            v.update()
            for k1, v1 in v.convey.items():
                city = self.citiesInfo[k1]
                if 'money' in v1:
                    city.money += v1['money']
                if 'troop' in v1:
                    city.restTroop += v1['troop']
                if 'weapon' in v1:
                    for k2, v2 in v1['weapon'].items():
                        if k2 not in city.weapons:
                            city.weapons[k2] = 0
                        city.weapons[k2] += v2
                if 'officer' in v1:
                    if not v1['officer']:
                        continue
                    if v1['officer'][0].belong != city.header.belong:
                        city.prisoner = city.prisoner.union(set(v1['officer']))
                    else:
                        city.officer = city.officer.union(set(v1['officer']))
            v.convey = {}
        self.turn += 1
        self.overed.clear()

    def ko(self, force, who):
        for i in self.forcesInfo[force].cities:
            for j in self.citiesInfo[i].officer:
                j.belong = who
        self.forcesInfo[who].cities = self.forcesInfo[who].cities.union(self.forcesInfo[force].cities)
        self.failed[force] = self.forcesInfo[force]

        for k, v in self.personsInfo.items():
            if v.belong == force:
                v.belong = who

        del self.forcesInfo[force]
        print(force+'is game over!')
        if self.myForce == force:
            print('game is over!\n\t往兮一何盛\n\t今兮一何衰\n英雄不过是别人的嫁衣罢了...')
            time.sleep(1000000)
        print('壮士一去兮复不还...')

    @staticmethod
    def load_obj(filepath):
        with open('retention/'+filepath, 'rb') as f:
            return pickle.load(f)




if __name__ == "__main__":
    pass
