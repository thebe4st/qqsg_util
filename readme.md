卡键、自动回复
========

**自动帮您回复生命值与法力、卡键等**

注意事项
---------

* 需要以管理员身份运行python解释器。
* 游戏客户端为32位，所以需要运行在32位python解释器之上。
* 在使用过程中，需要把生命回复药品放在```E```技能栏上，法力回复药品放在`R`技能栏上。

安装与使用
---------

```
cd $project-base-dir
```

```
pip install -r requirement.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```
python main.py
```

打包二进制
----------

```
pip install pyinstaller -i https://pypi.tuna.tsinghua.edu.cn/simple
```

```
cd $project-base-dir
```

```
pyinstaller -F main.py
```

结构与实现
-----
* 自动回复采用读内存方式实现，基址保存在 ```const.py```中
* 卡键：module/pressa.py
* 自动回复：module/auto_blood.py