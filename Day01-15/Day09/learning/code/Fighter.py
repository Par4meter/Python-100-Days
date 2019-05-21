from abc import abstractmethod, ABCMeta
from random import randint


class Fighter(object, metaclass=ABCMeta):
    """斗士"""
    __slots__ = ('_name', '_hp')

    def __init__(self, name, hp):
        """
        初始化斗士
        :param name:    斗士的名字
        :param hp:      斗士的生命值
        """
        self._name = name
        self._hp = hp

    @property
    def name(self):
        return self._name

    @property
    def hp(self):
        return self._hp

    @name.setter
    def name(self, name):
        self._name = name

    @hp.setter
    def hp(self, hp):
        self._hp = hp

    @abstractmethod
    def attack(self, target):
        """
        对目标进行普通攻击
        :param target: 目标
        :return:
        """
        pass


class Avenger(Fighter):
    """复仇者"""

    __slots__ = ('_name', '_hp', '_mp')

    def __init__(self, name, hp, mp):
        """
        初始化复仇者
        :param name: 复仇者名字
        :param hp: 复仇者血量
        :param mp: 复仇者魔法值
        """
        self._name = name
        self._hp = hp
        self._mp = mp

    def attack(self, target):
        target.hp -= randint(10, 30)

    def execute_attack(self, target):
        """
        处决攻击，需要mp大于50,否则执行普通攻击
        :param target:目标
        :return:成功：True；失败：False
        """
        if self._mp >= 50:
            target.hp = 0
            return True
        else:
            self.attack(self, target)
            return target.hp == 0

    def magic_attack(self, target):
        """
        魔法攻击，需要mp>20
        :param target:目标
        """
        if self._mp >= 20:
            target.hp -= randint(30, 60)
        else:
            self.attack(self, target)

    def resume(self):
        """回复生命与魔法"""
        self.hp += randint(1, 10)
        self.mp += randint(1, 10)

    def __str__(self):
        return '~~~复仇者-%s~~~\n' % self._name \
               + '生命值：%d\n' % self._hp \
               + '魔法值:%d\n' % self._mp


def main():
    a = Avenger('钢铁侠', 100, 100)
    print(a)

    a1 = Avenger('蜘蛛侠', 50, 50)

    a.attack(a1)

    print(a1)


if __name__ == '__main__':
    main()
