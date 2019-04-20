# -*- coding: utf-8 -*-

import wx
import re
import sqlite3
import shutil
import os
import xml.dom.minidom

def boolchange(string):
    if string=='True':
        return 1
    if string=='False':
        return 0

# 存放性格
PerValue={}

# 存放进攻策略
AttackValue={}

# 存放每个性格的开场行为
OpeningDic={}

# 存放新添加的开场行为
NewOpenings=[]

# 存放每个性格的队伍策略
StraDic={}

# 存放新添加的队伍策略名称
NewStra=[]

# 存放每个性格的建造策略
BuildDic={}

# 存放新添加的建造策略名称
NewBuild=[]

# 存放每个性格的喜好单位
PreferDic={}

# 存放每个性格的喜好协议
PowerDic={}

# 存放每个性格的单位上限
CapDic={}

# 存放每个队伍策略的目标
TargetDic={}

# 存放新的已命名物体类型的目标
AddTarget={}

# AI性格信息
PerData=[u'继承自',u'作为遭遇战性格',u'头像',u'资源作弊倍率-简单',u'资源作弊倍率-中等',u'资源作弊倍率-困难',u'资源作弊倍率-凶残',u'开场行为',u'队伍策略',u'建造策略',u'单位喜好',u'协议喜好',u'单位上限']

# 队伍策略信息
AttackData=[u'最大目标数',u'flag',u'活跃时间',u'触发单位',u'目标',u'战术',u'最大活动距离',u'结束时的行为',u'队伍数目',u'排除的类型',u'允许的运动类型',u'优先权',u'总是招募',u'微操',u'生产单位']

# 父性格
FatherPer=['AlliedCoopBaseCampaignPersonality','AlliedCoopBaseSkirmishPersonality','JapanCoopBaseCampaignPersonality','JapanCoopBaseSkirmishPersonality',\
           'SovietCoopBaseCampaignPersonality','SovietCoopBaseSkirmishPersonality']

# 对应阵营性格必要的xml
NeededPer=['AlliedCoopBaseCampaignPersonality','AlliedCoopBaseSkirmishPersonality','JapanCoopBaseCampaignPersonality','JapanCoopBaseSkirmishPersonality',\
           'SovietCoopBaseCampaignPersonality','SovietCoopBaseSkirmishPersonality','CoopBasePersonality','BasePersonality','AlliedCoopBasePersonality','JapanCoopBasePersonality','SovietCoopBasePersonality']
# 头像
Portrait=['Warren','Lissette','Giles','Shinzo','Naomi','Kenji','Oleg','Moskvin','Zhana']

# 协议列表
SpecialPower={u'空军协议':'PlayerTech_Allied_AirPower',\
              u'精确打击':'PlayerTech_Allied_PrecisionStrike',\
              u'扫描侦查':'PlayerTech_Allied_SatelliteSweep',\
              u'高科技':'PlayerTech_Allied_HighTechnology',\
              u'交换物体':'PlayerTech_Allied_ChronoSwap',\
              u'自由贸易':'PlayerTech_Allied_FreeTrade',\
              u'时空炸弹一级':'PlayerTech_Allied_TimeBomb_Rank1',\
              u'时空炸弹二级':'PlayerTech_Allied_TimeBomb_Rank2',\
              u'时空炸弹三级':'PlayerTech_Allied_TimeBomb_Rank3',\
              u'冷冻一级':'PlayerTech_Allied_CryoSatellite_Rank1',\
              u'冷冻二级':'PlayerTech_Allied_CryoSatellite_Rank2',\
              u'冷冻三级':'PlayerTech_Allied_CryoSatellite_Rank3',\
              u'时空裂缝一级':'PlayerTech_Allied_ChronoRift_Rank1',\
              u'时空裂缝二级':'PlayerTech_Allied_ChronoRift_Rank2',\
              u'时空裂缝三级':'PlayerTech_Allied_ChronoRift_Rank3',\
              u'自杀式小飞机一级':'PlayerTech_Japan_FinalSquadron_Rank1',\
              u'自杀式小飞机二级':'PlayerTech_Japan_FinalSquadron_Rank2',\
              u'自杀式小飞机三级':'PlayerTech_Japan_FinalSquadron_Rank3',\
              u'天皇之怒一级':'PlayerTech_Japan_EmperorsRage_Rank1',\
              u'天皇之怒二级':'PlayerTech_Japan_EmperorsRage_Rank2',\
              u'天皇之怒三级':'PlayerTech_Japan_EmperorsRage_Rank3',\
              u'气球炸弹一级':'PlayerTech_Japan_BalloonAttack_Rank1',\
              u'气球炸弹二级':'PlayerTech_Japan_BalloonAttack_Rank2',\
              u'气球炸弹三级':'PlayerTech_Japan_BalloonAttack_Rank3',\
              u'套子':'PlayerTech_Japan_PointDefenseDrones',\
              u'自爆':'PlayerTech_Japan_EnhancedKamikaze',\
              u'海军强化':'PlayerTech_Japan_NavalPower',\
              u'先进火箭匣':'PlayerTech_Japan_AdvancedMissilePacks',\
              u'惊骇伏击':'PlayerTech_Japan_Ambush',\
              u'磁力卫星一级':'PlayerTech_Soviet_MagneticSatellite_Rank_1',\
              u'磁力卫星二级':'PlayerTech_Soviet_MagneticSatellite_Rank_2',\
              u'磁力卫星三级':'PlayerTech_Soviet_MagneticSatellite_Rank_3',\
              u'轨道卫星一级':'PlayerTech_Soviet_OrbitalRefuse_Rank1',\
              u'轨道卫星二级':'PlayerTech_Soviet_OrbitalRefuse_Rank2',\
              u'轨道卫星三级':'PlayerTech_Soviet_OrbitalRefuse_Rank3',\
              u'农药协议一级':'PlayerTech_Soviet_DesolatorBomb_Rank1',\
              u'农药协议二级':'PlayerTech_Soviet_DesolatorBomb_Rank2',\
              u'农药协议三级':'PlayerTech_Soviet_DesolatorBomb_Rank3',\
              u'毒素侵蚀':'PlayerTech_Soviet_IrradiateTarget',\
              u'钱套':'PlayerTech_Soviet_ProductionKickbacks',\
              u'碾压协议':'PlayerTech_Soviet_CrushPuppies',\
              u'磁力奇点':'PlayerTech_Soviet_MagneticSingularity',
              u'恐怖机器人袭击':'PlayerTech_Soviet_TerrorDroneEggs'}

# 协议选择列表
SpecialPowerkeys=[u'空军协议',u'精确打击',u'扫描侦查',u'高科技',u'交换物体',u'自由贸易',u'时空炸弹一级',u'时空炸弹二级',u'时空炸弹三级',u'冷冻一级',u'冷冻二级',u'冷冻三级',\
                  u'时空裂缝一级',u'时空裂缝二级',u'时空裂缝三级',u'自杀式小飞机一级',u'自杀式小飞机二级',u'自杀式小飞机三级',u'天皇之怒一级',u'天皇之怒二级',u'天皇之怒三级',\
                  u'气球炸弹一级',u'气球炸弹二级',u'气球炸弹三级',u'套子',u'自爆',u'海军强化',u'先进火箭匣',u'惊骇伏击',u'磁力卫星一级',u'磁力卫星二级',u'磁力卫星三级',\
                  u'轨道卫星一级',u'轨道卫星二级',u'轨道卫星三级',u'农药协议一级',u'农药协议二级',u'农药协议三级',u'毒素侵蚀',u'钱套',u'碾压协议',u'磁力奇点',u'恐怖机器人袭击']

# 攻击目标列表
Target=['SafestToGroundStructureHeuristic','SafestToGroundUnitHeuristic','SafestToAirUnitHeuristic','SafestToAirStructureHeuristic','SafestToWaterUnitHeuristic',\
              'SafestToWaterStructureHeuristic','ClosestStructureHeuristic','ClosestGroundStructureHeuristic','ClosestWaterStructureHeuristic','ClosestUnitHeuristic',\
              'ClosestGroundUnitHeuristic','ClosestWaterUnitHeuristic','SafestToSurfaceHarvesterHeuristic','SafestToSurfaceSurveyorHeuristic','ClosestAllyUnitHeuristic',\
        'ClosestAllyCombatUnitHeuristi','ClosestAllyWaterUnitHeuristic','ClosestHarvesterHeuristic']

# 微操列表
MicroManagerList=[u'StandardMicroManager', u'StandardMicroManager_MEDIUM', u'StandardMicroManager_EASY', u'CleanupMicroManager', u'FocusedMicroManager', u'FocusedMicroManager_MEDIUM',\
                  u'FearlessFocusedMicroManager', u'StandardFullAlphaStrikeMicroManager', u'GrowingAttacksMicroManager', u'GrowingAttacksMicroManager_MEDIUM',u'ReactiveDefenseMicroManager',\
                  u'FearlessMicroManager', u'FearlessMicroManager_MEDIUM', u'FearlessMicroManager_EASY', u'EmergencyDefenseMicroManager', u'EmergencyDefenseMicroManager_MEDIUM',\
                  u'EmergencyDefenseMicroManager_EASY', u'DefenseMicroManager', u'DefenseMicroManager_MEDIUM', u'DefenseMicroManager_EASY', u'ExpansionMicroManager', u'BaseDefenseMicroManager',\
                  u'FearlessDefenseMicroManager', u'FearlessDefenseMicroManager_MEDIUM', u'FearlessDefenseMicroManager_EASY',u'ScoutInfantryMicroManager', u'ScoutMicroManager', \
                  u'FighterAircraftMicroManager',u'BurstDroneHarassmentMicroManager', u'StealthDetectorMicroManager', u'HarrassmentMicroManager', u'HarrassmentMicroManager_MEDIUM',\
                  u'FighterAircraftMicroManager_MEDIUM', u'FearlessFighterAircraftMicroManager', u'AssaultAircraftMicroManager', u'TwinbladeMicroManager', u'TwinbladeMicroManager_EASY', \
                  u'VindicatorMicroManager',u'VindicatorMicroManager_MEDIUM', u'VindicatorMicroManager_EASY', u'FearlessVindicatorMicroManager', u'FearlessAssaultAircraftMicroManager', \
                  u'CenturyBomberMicroManager',u'FearlessCenturyBomberMicroManager', u'BomberAircraftMicroManager', u'FearlessBomberAircraftMicroManager', u'KirovMicroManager',\
                  u'FirstAssaultMicroManager', u'SpecialForcesMicroManager', u'HeavyArmorMicroManager', u'ShockSpecialistMicroManager', u'ShockSpecialistMicroManager_MEDIUM', u'AirMarshallMicroManager',\
                  u'FleetCommandMicroManager', u'AmbushDivisionMicroManager']
class AIEdit(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self,None,-1,u'AI编辑器',size=(760,560))
        self.SetMaxSize((760,560))
        panel=wx.Panel(self)
        self.createMenuBar()
        
        sizer=wx.BoxSizer(wx.HORIZONTAL)
        self.tree=wx.TreeCtrl(panel,-1,size=(250,500),style=wx.TR_EDIT_LABELS|wx.TR_DEFAULT_STYLE)
        sizer.Add(self.tree,1,wx.ALL)
        self.list=wx.ListCtrl(panel,-1,size=(500,500),style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        sizer.Add(self.list,3,wx.ALL)
        panel.SetSizer(sizer)
        panel.Fit()
        
        self.createTree()
        self.createList()

        self.ModName=''
        self.TreeTextEdit=''

    def menuData(self):
        return((u'文件',(u'新建',self.OnNew),(u'打开',self.OnOpen),(u'保存',self.OnSave),('',''),(u'退出',self.OnQuit)),
               (u'编辑',(u'新增AI性格',self.OnNewPerson),(u'新增AI队伍策略',self.NewStra),(u'新增AI建造策略',self.NewBuild),(u'新增AI开场行为',self.NewOpening),('',''),(u'删除项目',self.OnDelete),(u'重命名项目',self.EnableTreeEdit)))

    def createMenuBar(self):
        menuBar=wx.MenuBar()
        for eachMenuData in self.menuData():
            menuLabel=eachMenuData[0]
            menuItems=eachMenuData[1:]
            menuBar.Append(self.createMenu(menuItems),menuLabel)
        self.SetMenuBar(menuBar)

    def createMenu(self,menuData):
        menu=wx.Menu()
        for eachLabel,eachHandler in menuData:
            if not eachLabel:
                menu.AppendSeparator()
                continue
            menuItem=menu.Append(-1,eachLabel)
            self.Bind(wx.EVT_MENU,eachHandler,menuItem)
        return menu

    def createTree(self):
        self.root=self.tree.AddRoot(u'AI')
        self.Person=self.tree.AppendItem(self.root,u'性格')
        self.Stra=self.tree.AppendItem(self.root,u'策略')
        self.Opening=self.tree.AppendItem(self.root,u'开场行为')

        self.AttackStra=self.tree.AppendItem(self.Stra,u'队伍策略')
        self.BuildStra=self.tree.AppendItem(self.Stra,u'建造策略')

        self.tree.SelectItem(self.Person)

        self.Bind(wx.EVT_TREE_SEL_CHANGING, self.OnClickTree, self.tree)
        self.Bind(wx.EVT_TREE_BEGIN_LABEL_EDIT,self.OnBeginEditTree,self.tree)
        self.Bind(wx.EVT_TREE_END_LABEL_EDIT,self.OnEndEditTree,self.tree)

    def createList(self):
        self.list.InsertColumn(0,u'名字')
        self.list.InsertColumn(1,u'值')
        self.list.SetColumnWidth(0,130)
        self.list.SetColumnWidth(1,370)

        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED,self.OnItemActivated,self.list)

    def OnNew(self,event):
        NameDialog=wx.TextEntryDialog(None,u'mod名称',u'新建',style=wx.OK|wx.CANCEL)
        if NameDialog.ShowModal()==wx.ID_OK:
            if re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$',NameDialog.GetValue())==None:
                warning=wx.MessageDialog(None,u'名称不正确',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                NameDialog.Destroy()
                return
            
            # 路径名称，以后也许需要修改
            pathname='Mods\\'+NameDialog.GetValue()
            if os.path.exists(pathname):
                warning=wx.MessageDialog(None,u'Mod名称已存在',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                NameDialog.Destroy()
                return
            self.ModName=NameDialog.GetValue()
            title=self.ModName+u' - AI编辑器'
            self.SetTitle(title)
        NameDialog.Destroy()

    def OnOpen(self,event):
        
        ModList=os.listdir('Mods')
        for i in ModList:
            if re.match(r'^[a-zA-Z]+$',i)==None:
                ModList.remove(i)
        ModChoice=wx.SingleChoiceDialog(None,u'选择一个mod',u'打开',ModList)
        if ModChoice.ShowModal()==wx.ID_OK:
            # 清空存放的数据
            PerValue.clear()
            OpeningDic.clear()
            StraDic.clear()
            BuildDic.clear()
            PreferDic.clear()
            PowerDic.clear()
            CapDic.clear()
            AddTarget.clear()

            del NewOpenings[:]
            del NewStra[:]
            del NewBuild[:]

            self.tree.DeleteChildren(self.Person)
            self.tree.DeleteChildren(self.AttackStra)
            self.tree.DeleteChildren(self.BuildStra)
            self.tree.DeleteChildren(self.Opening)

            self.ModName=ModChoice.GetStringSelection()
            title=self.ModName+u' - AI编辑器'
            self.SetTitle(title)
            
            pathname='Mods\\'+ModList[ModChoice.GetSelection()]
            for root,dirs,files in os.walk(pathname):
                for xmlfile in files:
                    if xmlfile.endswith('.xml'):
                        if xmlfile.rstrip('.xml') in NeededPer:
                            continue
                        dom=xml.dom.minidom.parse(os.path.join(root,xmlfile))
                        root=dom.documentElement
                        if root.getElementsByTagName('AIPersonalityDefinition'):
                            NewRoot=root.getElementsByTagName('AIPersonalityDefinition')[0]
                            name=NewRoot.getAttribute('id')
                            if re.match(r'^[0-9]',name)!=None:
                                name=name[1:]
                            self.tree.AppendItem(self.Person,name)
                            PerValue[name]=[]
                            NewPerValue=PerValue[name]
                            for i in range(len(PerData)):
                                NewPerValue.append('')
                            OpeningDic[name]={}
                            StraDic[name]={}
                            BuildDic[name]={}
                            PreferDic[name]={}
                            PowerDic[name]={}
                            CapDic[name]={}
                            
                            NewPerValue[0]=NewRoot.getAttribute('inheritFrom')
                            NewPerValue[1]=NewRoot.getAttribute('SkirmishPersonality').capitalize()
                            NewPerValue[2]=NewRoot.getAttribute('CommanderPortrait')

                            CheatNodes=root.getElementsByTagName('ResourceMultiplierCheat')
                            for Nodes in CheatNodes:
                                print '1'
                                if Nodes.getAttribute('Difficulty')!='':
                                    DifficultyStr=Nodes.getAttribute('Difficulty')
                                    if re.search(r'EASY',DifficultyStr)!=None:
                                        NewPerValue[3]=Nodes.getAttribute('Percentage')
                                    if re.search(r'MEDIUM',DifficultyStr)!=None:
                                        NewPerValue[4]=Nodes.getAttribute('Percentage')
                                    if re.search(r'HARD',DifficultyStr)!=None:
                                        NewPerValue[5]=Nodes.getAttribute('Percentage')
                                    if re.search(r'BRUTAL',DifficultyStr)!=None:
                                        NewPerValue[6]=Nodes.getAttribute('Percentage')
                            
                            OpeningNodes=root.getElementsByTagName('OpeningMove')
                            Openings=OpeningDic[name]
                            for Nodes in OpeningNodes:
                                OpeningName=Nodes.getAttribute('Name')
                                NewPerValue[7]+=OpeningName+','
                                Openings[OpeningName]=[]
                                Openings[OpeningName].append(Nodes.getAttribute('Weight').rstrip('%'))
                                DifficultyStr=Nodes.getAttribute('Difficulty')
                                if re.search(r'EASY',DifficultyStr)!=None:
                                    Openings[OpeningName].append('True')
                                else:
                                    Openings[OpeningName].append('False')
                                if re.search(r'MEDIUM',DifficultyStr)!=None:
                                    Openings[OpeningName].append('True')
                                else:
                                    Openings[OpeningName].append('False')
                                if re.search(r'HARD',DifficultyStr)!=None:
                                    Openings[OpeningName].append('True')
                                else:
                                    Openings[OpeningName].append('False')
                                if re.search(r'BRUTAL',DifficultyStr)!=None:
                                    Openings[OpeningName].append('True')
                                else:
                                    Openings[OpeningName].append('False')
                            NewPerValue[7]=NewPerValue[7].rstrip(',')

                            StraNodes=root.getElementsByTagName('StrategicState')
                            Stra=StraDic[name]
                            for Nodes in StraNodes:
                                if Nodes.getAttribute('xai:joinAction')!='':
                                    continue
                                StraName=Nodes.getAttribute('id')
                                NewPerValue[8]+=StraName+','
                                Stra[StraName]=[]
                                DifficultyStr=Nodes.getAttribute('Difficulty')
                                if re.search(r'EASY',DifficultyStr)!=None:
                                    Stra[StraName].append('True')
                                else:
                                    Stra[StraName].append('False')
                                if re.search(r'MEDIUM',DifficultyStr)!=None:
                                    Stra[StraName].append('True')
                                else:
                                    Stra[StraName].append('False')
                                if re.search(r'HARD',DifficultyStr)!=None:
                                    Stra[StraName].append('True')
                                else:
                                    Stra[StraName].append('False')
                                if re.search(r'BRUTAL',DifficultyStr)!=None:
                                    Stra[StraName].append('True')
                                else:
                                    Stra[StraName].append('False')
                            NewPerValue[8]=NewPerValue[8].rstrip(',')

                            BuildNodes=root.getElementsByTagName('BuildState')
                            Build=BuildDic[name]
                            for Nodes in BuildNodes:
                                if Nodes.getAttribute('xai:joinAction')!='':
                                    continue
                                BuildName=Nodes.getAttribute('id')
                                NewPerValue[9]+=BuildName+','
                                Build[BuildName]=[]
                                DifficultyStr=Nodes.getAttribute('Difficulty')
                                if re.search(r'EASY',DifficultyStr)!=None:
                                    Build[BuildName].append('True')
                                else:
                                    Build[BuildName].append('False')
                                if re.search(r'MEDIUM',DifficultyStr)!=None:
                                    Build[BuildName].append('True')
                                else:
                                    Build[BuildName].append('False')
                                if re.search(r'HARD',DifficultyStr)!=None:
                                    Build[BuildName].append('True')
                                else:
                                    Build[BuildName].append('False')
                                if re.search(r'BRUTAL',DifficultyStr)!=None:
                                    Build[BuildName].append('True')
                                else:
                                    Build[BuildName].append('False')
                            NewPerValue[9]=NewPerValue[9].rstrip(',')

                            conn=sqlite3.connect('UnitList.db')
                            cur=conn.cursor()

                            PreferNodes=root.getElementsByTagName('UnitModifier')
                            Prefer=PreferDic[name]
                            for Nodes in PreferNodes:
                                PreferName=Nodes.getAttribute('Unit')
                                cur.execute("select * from Unitname WHERE name1=(?)",(PreferName,))
                                res=cur.fetchall()
                                if res!=[]:
                                    NewPerValue[10]+=res[0][0]+','
                                    Prefer[PreferName]=[]
                                    Prefer[PreferName].append(Nodes.getAttribute('OffensiveModifier'))
                                    Prefer[PreferName].append(Nodes.getAttribute('DefensiveModifier'))
                            NewPerValue[10]=NewPerValue[10].rstrip(',')

                            Dic=dict((value,key) for key,value in SpecialPower.items())

                            PowerNodes=root.getElementsByTagName('PowerChoice')
                            Power=PowerDic[name]
                            for Nodes in PowerNodes:
                                PowerName=Nodes.getAttribute('PlayerPower')
                                if Dic.has_key(PowerName):
                                    NewPerValue[11]+=Dic[PowerName]+','
                                    Power[PowerName]=Nodes.getAttribute('Weight').rstrip('%')
                            NewPerValue[11]=NewPerValue[11].rstrip(',')

                            CapNodes=root.getElementsByTagName('SpecificUnitCap')
                            Cap=CapDic[name]
                            for Nodes in CapNodes:
                                CapName=Nodes.getAttribute('Unit')
                                cur.execute("select * from Unitname WHERE name1=(?)",(CapName,))
                                res=cur.fetchall()
                                if res!=[]:
                                    NewPerValue[12]+=res[0][0]+','
                                    Cap[CapName]=Nodes.getAttribute('Cap')
                            NewPerValue[12]=NewPerValue[12].rstrip(',')
                            cur.close()
                            conn.close()
                        if root.getElementsByTagName('AIStrategicStateDefinition'):
                            for NewRoot in root.getElementsByTagName('AIStrategicStateDefinition'):
                                name=NewRoot.getAttribute('id')
                                self.tree.AppendItem(self.AttackStra,name)
                                AttackValue[name]=[]
                                NewAttackValue=AttackValue[name]
                                for i in range(len(AttackData)):
                                    NewAttackValue.append('')
                                TargetDic[name]={}
                                NewStra.append(name)

                                NewAttackValue[0]=NewRoot.getAttribute('MaxTargets')

                                if NewRoot.getElementsByTagName('ScriptedFlagHeuristic'):
                                    NewAttackValue[1]=NewRoot.getElementsByTagName('ScriptedFlagHeuristic')[0].getAttribute('FlagName')

                                if NewRoot.getElementsByTagName('IntervalHeuristic'):
                                    NewAttackValue[2]=NewRoot.getElementsByTagName('IntervalHeuristic')[0].getAttribute('IntervalTime')+','+NewRoot.getElementsByTagName('IntervalHeuristic')[0].getAttribute('ActiveTime')

                                conn=sqlite3.connect('UnitList.db')
                                cur=conn.cursor()
                                if NewRoot.getElementsByTagName('ObjectOfTypeExistsHeuristic'):
                                    Node=NewRoot.getElementsByTagName('ObjectOfTypeExistsHeuristic')[0]
                                    NewAttackValue[3]=Node.getElementsByTagName('ObjectFilter')[0].getAttribute('Relationship')
                                    index=1
                                    for i in Node.getElementsByTagName('IncludeThing'):
                                        if index==4:
                                            break
                                        NewAttackValue[3]+=','+i.firstChild.data
                                        index=index+1
                                    for i in range(4-len(NewAttackValue[3].split(','))):
                                        NewAttackValue[3]+=u',无'

                                if NewRoot.getElementsByTagName('TargetHeuristic'):
                                    for i in NewRoot.getElementsByTagName('TargetHeuristic'):
                                        NewAttackValue[4]+=i.getAttribute('TargetHeuristic')+','
                                        Target=TargetDic[name]
                                        Target[i.getAttribute('TargetHeuristic')]=i.getAttribute('Priority')
                                    NewAttackValue[4]=NewAttackValue[4].rstrip(',')

                                if NewRoot.getElementsByTagName('Tactic'):
                                    NewAttackValue[5]=NewRoot.getElementsByTagName('Tactic')[0].getAttribute('Tactic')
                                    NewAttackValue[6]=NewRoot.getElementsByTagName('Tactic')[0].getAttribute('Distance')
                                    NewAttackValue[7]=NewRoot.getElementsByTagName('Tactic')[0].getAttribute('EndBehavior')

                                if NewRoot.getElementsByTagName('TeamTemplate'):
                                    NewAttackValue[8]=NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('MinUnits')+','+NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('MaxUnits')
                                    NewAttackValue[9]=NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('ExcludeKindOf')
                                    NewAttackValue[10]=NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('AllowedLocomotorTypes')
                                    NewAttackValue[11]=NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('Priority')
                                    NewAttackValue[12]=NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('AlwaysRecruit').capitalize()
                                    NewAttackValue[13]=NewRoot.getElementsByTagName('TeamTemplate')[0].getAttribute('MicroManager')
                                    Node=NewRoot.getElementsByTagName('TeamTemplate')[0]
                                    if Node.getElementsByTagName('CreateUnits'):
                                        NewAttackValue[14]=Node.getElementsByTagName('CreateUnits')[0].getAttribute('UnitName')+','+Node.getElementsByTagName('CreateUnits')[0].getAttribute('MinUnits')+','+Node.getElementsByTagName('CreateUnits')[0].getAttribute('MaxUnits')
                                cur.close()
                                conn.close()
        
        ModChoice.Destroy()
        self.tree.SelectItem(self.Person)
        self.list.DeleteAllItems()


    def OnSave(self,event):
        if PerValue=={} and NewStra=={}:
            warning=wx.MessageDialog(None,u'没有添加新项目',u'警告')
            warning.ShowModal()
            warning.Destroy()
            return
        if self.ModName=='':
            NameDialog=wx.TextEntryDialog(None,u'Mod名称',u'输入名称',style=wx.OK|wx.CANCEL)
            if NameDialog.ShowModal()==wx.ID_OK:
                if re.match(r'^[a-zA-Z][a-zA-Z0-9_]+$',NameDialog.GetValue())==None:
                    warning=wx.MessageDialog(None,u'名称不正确',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    NameDialog.Destroy()
                    return
                pathname='Mods\\'+NameDialog.GetValue()
                if os.path.exists(pathname):
                    warning=wx.MessageDialog(None,u'Mod名称已存在,是否覆盖？',u'警告',style=wx.OK|wx.CANCEL)
                    if warning.ShowModal()!=wx.ID_OK:
                        warning.Destroy()
                        NameDialog.Destroy()
                        return
                    shutil.rmtree(pathname)
                self.ModName=NameDialog.GetValue()
                title=self.ModName+u' - AI编辑器'
                self.SetTitle(title)
            else:
                return
            NameDialog.Destroy()

        if os.path.exists('Mods\\'+self.ModName):
            shutil.rmtree('Mods\\'+self.ModName)
        Data='Mods\\'+self.ModName+'\\Data'
        os.makedirs(Data)
        FileModXml=Data+'\\mod.xml'
        ModXml=open(FileModXml,'w+')
        ModXml.write('''<?xml version="1.0" encoding="UTF-8"?>
<AssetDeclaration xmlns="uri:ea.com:eala:asset" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
	<Tags></Tags>
	<Includes>
		<Include type="reference" source="DATA:static.xml" />
		<Include type="reference" source="DATA:global.xml" />    
		<Include type="reference" source="DATA:audio.xml" />\n''')

        os.makedirs('Mods\\'+self.ModName+'\\Additional\\Data')
        ModStr=open('Mods\\'+self.ModName+'\\Additional\\Data\\mod.str','w+')
        
        if PerValue!={}:
            Person=Data+'\\Personalities'
            os.makedirs(Person)
            ModXml.write('''\n		<Include type="all" source="DATA:%s/data/Personalities/CoopBasePersonality.xml" />
		<Include type="all" source="DATA:%s/data/Personalities/BasePersonality.xml" />'''%(self.ModName,self.ModName))
            
            shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\CoopBasePersonality.xml',Person+'\\CoopBasePersonality.xml')
            shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\BasePersonality.xml',Person+'\\BasePersonality.xml')
            
            parentlist=[]
            for Per in PerValue.keys():
                parentlist.append(PerValue[Per][0])
            if ('AlliedCoopBaseCampaignPersonality' in parentlist) or ('AlliedCoopBaseSkirmishPersonality' in parentlist):
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/AlliedCoopBasePersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\AlliedCoopBasePersonality.xml',Person+'\\AlliedCoopBasePersonality.xml')
            if 'AlliedCoopBaseCampaignPersonality' in parentlist:
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/AlliedCoopBaseCampaignPersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\AlliedCoopBaseCampaignPersonality.xml',Person+'\\AlliedCoopBaseCampaignPersonality.xml')
            if 'AlliedCoopBaseSkirmishPersonality' in parentlist:
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/AlliedCoopBaseSkirmishPersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\AlliedCoopBaseSkirmishPersonality.xml',Person+'\\AlliedCoopBaseSkirmishPersonality.xml')
            if ('JapanCoopBaseCampaignPersonality' in parentlist) or ('JapanCoopBaseSkirmishPersonality' in parentlist):
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/JapanCoopBasePersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\JapanCoopBasePersonality.xml',Person+'\\JapanCoopBasePersonality.xml')
            if 'JapanCoopBaseCampaignPersonality' in parentlist:
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/JapanCoopBaseCampaignPersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\JapanCoopBaseCampaignPersonality.xml',Person+'\\JapanCoopBaseCampaignPersonality.xml')
            if 'JapanCoopBaseSkirmishPersonality' in parentlist:
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/JapanCoopBaseSkirmishPersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\JapanCoopBaseSkirmishPersonality.xml',Person+'\\JapanCoopBaseSkirmishPersonality.xml')
            if ('SovietCoopBaseCampaignPersonality' in parentlist) or ('SovietCoopBaseSkirmishPersonality' in parentlist):
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/SovietCoopBasePersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\SovietCoopBasePersonality.xml',Person+'\\SovietCoopBasePersonality.xml')
            if 'SovietCoopBaseCampaignPersonality' in parentlist:
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/SovietCoopBaseCampaignPersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\SovietCoopBaseCampaignPersonality.xml',Person+'\\SovietCoopBaseCampaignPersonality.xml')
            if 'SovietCoopBaseSkirmishPersonality' in parentlist:
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/SovietCoopBaseSkirmishPersonality.xml" />''')
                shutil.copyfile('SageXml\\SkirmishAI\\Personalities\\SovietCoopBaseSkirmishPersonality.xml',Person+'\\SovietCoopBaseSkirmishPersonality.xml')

            index=4
            for name,value in PerValue.items():
                PerXml=open(Person+'\\'+name+'.xml','w+')

                ModStr.write('''Personality:%s
"%s"
END\n'''%(name,name))
                if value[0]=='':
                    warning=wx.MessageDialog(None,name+u'没有继承一个父类',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                if value[1]=='':
                    warning=wx.MessageDialog(None,name+u'是否为遭遇战性格不明确',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                PerXml.write('''<?xml version="1.0" encoding="utf-8"?>
<AssetDeclaration xmlns="uri:ea.com:eala:asset" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Tags></Tags>
  <Includes>
    <Include type="instance" source="%s" />
  </Includes>
  <AIPersonalityDefinition
		id="%s"
    PersonalityType="%s"
    inheritFrom="%s"
    SkirmishPersonality="%s"
    PersonalityUIName="Personality:%s"'''%(value[0]+'.xml',str(index)+name,str(index)+name,value[0],value[1].lower(),name))
                if value[2]!='':
                    PerXml.write('''\n    CommanderPortrait="%s"'''%(value[2],))
                PerXml.write('''\n           >\n''')
                
                if value[3]!='':
                    PerXml.write('''\n    <ResourceMultiplierCheat Percentage="%s" Difficulty="EASY"/>'''%(value[3]+'%',))
                if value[4]!='':
                    PerXml.write('''\n    <ResourceMultiplierCheat Percentage="%s" Difficulty="MEDIUM"/>'''%(value[4]+'%',))
                if value[5]!='':
                    PerXml.write('''\n    <ResourceMultiplierCheat Percentage="%s" Difficulty="HARD"/>'''%(value[5]+'%',))
                if value[6]!='':
                    PerXml.write('''\n    <ResourceMultiplierCheat Percentage="%s" Difficulty="BRUTAL"/>'''%(value[6]+'%',))

                PerXml.write('''\n''')

                if value[7]!='':
                    for openingname,Difficulty in OpeningDic[name].items():
                        weight=Difficulty[0]+'%'
                        DifficultyStr=''
                        if Difficulty[1]=='True':
                            DifficultyStr+='EASY '
                        if Difficulty[2]=='True':
                            DifficultyStr+='MEDIUM '
                        if Difficulty[3]=='True':
                            DifficultyStr+='HARD '
                        if Difficulty[4]=='True':
                            DifficultyStr+='BRUTAL'
                        if DifficultyStr.endswith(' '):
                            DifficultyStr=DifficultyStr.rstrip(' ')
                        PerXml.write('''\n    <OpeningMove Name="%s" Weight="%s" Difficulty="%s"/>'''%(weight,DifficultyStr))
                    PerXml.write('''\n''')

                if value[8]!='':
                    for straName,Difficulty in StraDic[name].items():
                        DifficultyStr=''
                        if Difficulty[0]=='True':
                            DifficultyStr+='EASY '
                        if Difficulty[1]=='True':
                            DifficultyStr+='MEDIUM '
                        if Difficulty[2]=='True':
                            DifficultyStr+='HARD '
                        if Difficulty[3]=='True':
                            DifficultyStr+='BRUTAL'
                        if DifficultyStr.endswith(' '):
                            DifficultyStr=DifficultyStr.rstrip(' ')
                        PerXml.write('''\n    <StrategicState id="%s" State="%s" Difficulty="%s"/>'''%(straName,straName,DifficultyStr))
                    PerXml.write('''\n''')

                if value[9]!='':
                    for buildName,Difficulty in BuildDic[name].items():
                        DifficultyStr=''
                        if Difficulty[0]=='True':
                            DifficultyStr+='EASY '
                        if Difficulty[1]=='True':
                            DifficultyStr+='MEDIUM '
                        if Difficulty[2]=='True':
                            DifficultyStr+='HARD '
                        if Difficulty[3]=='True':
                            DifficultyStr+='BRUTAL'
                        if DifficultyStr.endswith(' '):
                            DifficultyStr=DifficultyStr.rstrip(' ')
                        PerXml.write('''\n    <BuildState id="%s" State="%s" Difficulty="%s"/>'''%(buildName,buildName,DifficultyStr))
                    PerXml.write('''\n''')

                if value[10]!='':
                    for preferName,count in PreferDic[name].items():
                        PerXml.write('''\n    <UnitModifier Unit="%s" OffensiveModifier="%s" DefensiveModifier="%s"/>'''%(preferName,count[0],count[1]))
                    PerXml.write('''\n''')

                if value[11]!='':
                    for powerName,weight in PowerDic[name].items():
                        PerXml.write('''\n    <PowerChoice PlayerPower="%s" Weight="%s"/>'''%(powerName,weight+'%'))
                    PerXml.write('''\n''')

                if value[12]!='':
                    for capName,cap in CapDic[name].items():
                        PerXml.write('''\n    <SpecificUnitCap Unit="%s" Cap="%s" Difficulty="EASY MEDIUM HARD BRUTAL"/>'''%(capName,cap))
                    PerXml.write('''\n''')
                PerXml.write('''\n   </AIPersonalityDefinition>
</AssetDeclaration>''')
                PerXml.close()
                index+=1
                ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Personalities/%s.xml" />'''%(name,))

        ModStr.close()

        if AttackValue!={}:
            ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/Strategic/NewStrategic.xml" />''')
            
            Strategic=Data+'\\Strategic'
            os.makedirs(Strategic)
            
            StrategicXml=open(Strategic+'\\NewStrategic.xml','w+')

            StrategicXml.write('''<?xml version="1.0" encoding="utf-8" ?>
<AssetDeclaration xmlns="uri:ea.com:eala:asset" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Tags></Tags>
  <Includes></Includes>\n''')

            for name,value in AttackValue.items():
                if value[0]=='':
                    warning=wx.MessageDialog(None,name+u'没有最大目标数',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write('''\n   <AIStrategicStateDefinition
    id="%s"
    MaxTargets="%s">
    <Heuristic>'''%(name,value[0]))

                if value[1]!='':
                    StrategicXml.write('''\n    <ScriptedFlagHeuristic FlagName="%s"/>'''%(value[1],))
                if value[2]!='':
                    StrategicXml.write('''\n    <IntervalHeuristic IntervalTime="%s" ActiveTime="%s" CountFrom="AI_START"/>'''%(value[2].split(',')[0],value[2].split(',')[1]))
                if value[3]!='':
                    triggerlist=value[3].split(',')
                    print triggerlist
                    StrategicXml.write('''\n    <ObjectOfTypeExistsHeuristic
        PassIfExists="true">
        <ObjectFilter
					Relationship="%s"
					Rule="ANY" >'''%(triggerlist[0],))
                    if triggerlist[1]!=u'无':
                        StrategicXml.write('''\n          <IncludeThing>%s</IncludeThing>'''%(triggerlist[1],))
                    if triggerlist[2]!=u'无':
                        StrategicXml.write('''\n          <IncludeThing>%s</IncludeThing>'''%(triggerlist[2],))
                    if triggerlist[3]!=u'无':
                        StrategicXml.write('''\n          <IncludeThing>%s</IncludeThing>'''%(triggerlist[3],))
                    StrategicXml.write('''\n        </ObjectFilter>
      </ObjectOfTypeExistsHeuristic>''')
                if value[1]=='' and value[2]=='' and value[3]=='':
                    StrategicXml.write('''\n      <ConstantHeuristic/>''')
                StrategicXml.write('''\n    </Heuristic>''')
                if value[4]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写目标',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                for TargetName,Pro in TargetDic[name].items():
                    StrategicXml.write('''\n    <TargetHeuristic TargetHeuristic="%s" Priority="%s"/>'''%(TargetName,Pro))

                if value[5]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写战术',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                if value[5]=='DefenseAvoidanceAttack' or value[5]=='SimpleAttack' or value[5]=='SimpleExpansion':
                    StrategicXml.write('''\n    <Tactic id="Attack" Tactic="%s"'''%(value[5],))
                if value[5]=='StaticDefense':
                    StrategicXml.write('''\n    <Tactic id="Defend" Tactic="%s"'''%(value[5],))
                
                if value[6]!='':
                    StrategicXml.write(''' Distance="%s"'''%(value[6],))

                if value[7]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写结束行为',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write(''' EndBehavior="%s">'''%(value[7],))

                if value[8]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写队伍数目',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write('''\n      <TeamTemplate MinUnits="%s" MaxUnits="%s"'''%(value[8].split(',')[0],value[8].split(',')[1]))

                StrategicXml.write('''\n                    IncludeKindOf="CAN_ATTACK" ExcludeKindOf="%s"'''%(value[9],))

                if value[10]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写允许运动类型',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write('''\n                    AllowedLocomotorTypes="%s"'''%(value[10],))

                if value[11]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写优先权',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write('''\n                    Priority="%s"'''%(value[11],))

                if value[12]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写是否招募',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write('''\n                    AlwaysRecruit="%s"'''%(value[12].lower(),))

                if value[13]=='':
                    warning=wx.MessageDialog(None,name+u'没有填写微操',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    shutil.rmtree('Mods\\'+self.ModName)
                    return
                StrategicXml.write('''\n                    MicroManager="%s">'''%(value[13],))

                if value[14]!='':
                    StrategicXml.write('''\n      <CreateUnits UnitName="%s" MinUnits="%s" MaxUnits="%s"/>'''%(value[14].split(',')[0],value[14].split(',')[1],value[14].split(',')[2]))

                StrategicXml.write('''\n</TeamTemplate>
    </Tactic>
  </AIStrategicStateDefinition>''')
                
                StrategicXml.write('''\n''')
            StrategicXml.write('''\n</AssetDeclaration>''')
            StrategicXml.close()

        if AddTarget!={}:
            ModXml.write('''\n		<Include type="all" source="DATA:'''+self.ModName+'''/data/AITargetHeuristicLibrary1.xml" />''')
            AITarget=open(Data+'\\AITargetHeuristicLibrary1.xml','w+')
            AITarget.write('''<?xml version="1.0" encoding="utf-8"?>
<AssetDeclaration xmlns="uri:ea.com:eala:asset" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
  <Tags></Tags>
  <Includes>
  </Includes>\n''')
            for name,value in AddTarget.items():
                AITarget.write('''\n  <AITargetingHeuristic
   id="%s"
   HeuristicType="NamedObject"
   Name="%s"
  />\n'''%(name,value))
            AITarget.write('''\n</AssetDeclaration>''')

        ModXml.write('''\n	  </Includes>

</AssetDeclaration>''')
        ModXml.close()

    def OnQuit(self,event):
        self.Close()
    
    def OnNewPerson(self,event):
        NewPersonDialog=wx.TextEntryDialog(None,u'AI性格名称',u'新建AI性格')
        if NewPersonDialog.ShowModal()==wx.ID_OK:
            if re.match(r'[a-zA-Z][a-zA-Z0-9_]+',NewPersonDialog.GetValue())==None:
                WarningDialog=wx.MessageDialog(None,u'名称不正确',u'警告',style=wx.OK)
                WarningDialog.ShowModal()
                WarningDialog.Destroy()
                NewPersonDialog.Destroy()
                return
            self.tree.AppendItem(self.Person,NewPersonDialog.GetValue())
            PerValue[NewPersonDialog.GetValue()]=[]
            NewPerValue=PerValue[NewPersonDialog.GetValue()]
            for i in range(len(PerData)):
                NewPerValue.append('')
            OpeningDic[NewPersonDialog.GetValue()]={}
            StraDic[NewPersonDialog.GetValue()]={}
            BuildDic[NewPersonDialog.GetValue()]={}
            PreferDic[NewPersonDialog.GetValue()]={}
            PowerDic[NewPersonDialog.GetValue()]={}
            CapDic[NewPersonDialog.GetValue()]={}
        NewPersonDialog.Destroy()

    def NewStra(self,event):
        NewAttackDialog=wx.TextEntryDialog(None,u'队伍策略名称',u'新建队伍策略')
        if NewAttackDialog.ShowModal()==wx.ID_OK:
            if re.match(r'[a-zA-Z][a-zA-Z0-9_]+',NewAttackDialog.GetValue())==None:
                WarningDialog=wx.MessageDialog(None,u'名称不正确',u'警告',style=wx.OK)
                WarningDialog.ShowModal()
                WarningDialog.Destroy()
                NewAttackDialog.Destroy()
                return
            self.tree.AppendItem(self.AttackStra,NewAttackDialog.GetValue())
            AttackValue[NewAttackDialog.GetValue()]=[]
            NewAttackValue=AttackValue[NewAttackDialog.GetValue()]
            for i in range(len(AttackData)):
                NewAttackValue.append('')
            TargetDic[NewAttackDialog.GetValue()]={}
            NewStra.append(NewAttackDialog.GetValue())
        NewAttackDialog.Destroy()

    def NewBuild(self,event):
        pass

    def NewOpening(self,event):
        pass

    def OnDelete(self,event):
        item=self.tree.GetSelection()
        treeText=self.tree.GetItemText(item)
        if treeText=='AI'or treeText==u'性格' or treeText==u'队伍策略' or treeText==u'开场行为' or treeText==u'建造策略':
            return
        if self.tree.GetItemText(self.tree.GetItemParent(item))==u'性格':
            warning=wx.MessageDialog(None,u'确认删除这个AI性格？',u'提示',style=wx.OK|wx.CANCEL)
            if warning.ShowModal()==wx.ID_OK:
                self.tree.Delete(item)
                self.tree.SelectItem(self.Person)
                self.list.DeleteAllItems()
                del PerValue[treeText]
                del OpeningDic[treeText]
                del StraDic[treeText]
                del PreferDic[treeText]
                del PowerDic[treeText]
                del CapDic[treeText]
            warning.Destroy()
            return

        if self.tree.GetItemText(self.tree.GetItemParent(item))==u'队伍策略':
            warning=wx.MessageDialog(None,u'确认删除这个队伍策略？',u'提示',style=wx.OK|wx.CANCEL)
            if warning.ShowModal()==wx.ID_OK:
                self.tree.Delete(item)
                self.tree.SelectItem(self.AttackStra)
                self.list.DeleteAllItems()
                del AttackValue[treeText]
                del TargetDic[treeText]
            warning.Destroy()
            return

    def EnableTreeEdit(self,event):
        item=self.tree.GetSelection()
        self.tree.EditLabel(item)

    def OnItemActivated(self,event):
        item=event.GetItem()
        treeItem=self.tree.GetSelection()
        if item.GetText()==u'继承自':
            inheritDialog=wx.Dialog(None,-1,u'继承自')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(inheritDialog,-1,u'选择一个父类')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            Choice=wx.Choice(inheritDialog,-1,choices=FatherPer)
            if self.list.GetItem(event.GetIndex(),1).GetText()=='':
                Choice.SetSelection(0)
            else:
                Choice.SetSelection(FatherPer.index(self.list.GetItem(event.GetIndex(),1).GetText()))
            box.Add(Choice,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.StaticBox(inheritDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(inheritDialog,-1,u'父类决定这个ai性格属于哪个阵营,\nAllied开头的为盟军,\nJapan开头德威帝国,\nSoviet开头的为苏联')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(inheritDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(inheritDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            inheritDialog.SetSizer(sizer)
            inheritDialog.Fit()

            if inheritDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,Choice.GetStringSelection())
                PerValue[self.tree.GetItemText(treeItem)][0]=Choice.GetStringSelection()
            inheritDialog.Destroy()
            return
        
        if item.GetText()==u'作为遭遇战性格':
            boolDialog=wx.Dialog(None,-1,u'编辑布尔值')
            sizer=wx.BoxSizer(wx.VERTICAL)
            Choice=wx.CheckBox(boolDialog,-1,u'作为遭遇战性格   :',style=wx.ALIGN_RIGHT)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                Choice.SetValue(boolchange(PerValue[self.tree.GetItemText(treeItem)][1]))
            sizer.Add(Choice,0,wx.ALIGN_CENTER|wx.ALL,10)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(boolDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(boolDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            boolDialog.SetSizer(sizer)
            boolDialog.Fit()
            if boolDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(Choice.GetValue()))
                PerValue[self.tree.GetItemText(treeItem)][1]=str(Choice.GetValue())
            boolDialog.Destroy()
            return

        if item.GetText()==u'头像':
            PortraitDialog=wx.Dialog(None,-1,u'头像')
            sizer=wx.BoxSizer(wx.VERTICAL)
                        
            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(PortraitDialog,-1,u'选择一个头像  :')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,5)
            Choice=wx.Choice(PortraitDialog,-1,choices=Portrait)
            if self.list.GetItem(event.GetIndex(),1).GetText()=='':
                Choice.SetSelection(0)
            else:
                Choice.SetSelection(Portrait.index(self.list.GetItem(event.GetIndex(),1).GetText()))                        
            box.Add(Choice,0,wx.ALIGN_CENTER|wx.ALL,5)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(PortraitDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(PortraitDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            PortraitDialog.SetSizer(sizer)
            PortraitDialog.Fit()

            if PortraitDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,Choice.GetStringSelection())
                PerValue[self.tree.GetItemText(treeItem)][2]=Choice.GetStringSelection()
            PortraitDialog.Destroy()
            return

        if item.GetText()==u'资源作弊倍率-简单':
            percentDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)
            Number=wx.SpinCtrl(percentDialog,-1)
            Number.SetRange(1,999)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                Number.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText()))
            sizer.Add(Number,0,wx.ALIGN_CENTER|wx.ALL,10)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(percentDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(percentDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            percentDialog.SetSizer(sizer)
            percentDialog.Fit()
            if percentDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(Number.GetValue()))
                PerValue[self.tree.GetItemText(treeItem)][3]=str(Number.GetValue())
            percentDialog.Destroy()
            return

        if item.GetText()==u'资源作弊倍率-中等':
            percentDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)
            Number=wx.SpinCtrl(percentDialog,-1)
            Number.SetRange(1,999)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                Number.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText()))
            sizer.Add(Number,0,wx.ALIGN_CENTER|wx.ALL,10)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(percentDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(percentDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            percentDialog.SetSizer(sizer)
            percentDialog.Fit()
            if percentDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(Number.GetValue()))
                PerValue[self.tree.GetItemText(treeItem)][4]=str(Number.GetValue())
            percentDialog.Destroy()
            return

        if item.GetText()==u'资源作弊倍率-困难':
            percentDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)
            Number=wx.SpinCtrl(percentDialog,-1)
            Number.SetRange(1,999)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                Number.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText()))
            sizer.Add(Number,0,wx.ALIGN_CENTER|wx.ALL,10)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(percentDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(percentDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            percentDialog.SetSizer(sizer)
            percentDialog.Fit()
            if percentDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(Number.GetValue()))
                PerValue[self.tree.GetItemText(treeItem)][5]=str(Number.GetValue())
            percentDialog.Destroy()
            return

        if item.GetText()==u'资源作弊倍率-凶残':
            percentDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)
            Number=wx.SpinCtrl(percentDialog,-1)
            Number.SetRange(1,999)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                Number.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText()))
            sizer.Add(Number,0,wx.ALIGN_CENTER|wx.ALL,10)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(percentDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(percentDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            percentDialog.SetSizer(sizer)
            percentDialog.Fit()
            if percentDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(Number.GetValue()))
                PerValue[self.tree.GetItemText(treeItem)][6]=str(Number.GetValue())
            percentDialog.Destroy()
            return

        if item.GetText()==u'开场行为':
            OpeningDialog=wx.Dialog(None,-1,u'开场行为')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(OpeningDialog,-1,u'列表-开场行为')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            openinglist=PerValue[self.tree.GetItemText(treeItem)][7].split(',')
            if '' in openinglist:
                openinglist.remove('')
            self.Openings=wx.ListBox(OpeningDialog,-1,size=(300,250),choices=openinglist)
            sizer.Add(self.Openings,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            NewOpen=wx.Button(OpeningDialog,-1,u'添加开场行为',size=(-1,25))
            box.Add(NewOpen,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.EditOpen=wx.Button(OpeningDialog,-1,u'编辑开场行为',size=(-1,25))
            box.Add(self.EditOpen,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)

            self.DelOpen=wx.Button(OpeningDialog,-1,u'删除开场行为',size=(-1,25))
            self.DelOpen.Enable(False)
            self.EditOpen.Enable(False)
            sizer.Add(self.DelOpen,0,wx.ALIGN_CENTER|wx.ALL,1)

            OpeningDialog.Bind(wx.EVT_LISTBOX,self.OnOpenings,self.Openings)
            OpeningDialog.Bind(wx.EVT_LISTBOX_DCLICK,self.OnEditOpen,self.Openings)

            OpeningDialog.Bind(wx.EVT_BUTTON,self.OnNewOpen,NewOpen)
            OpeningDialog.Bind(wx.EVT_BUTTON,self.OnEditOpen,self.EditOpen)
            OpeningDialog.Bind(wx.EVT_BUTTON,self.OnDelOpen,self.DelOpen)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(OpeningDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(OpeningDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            OpeningDialog.SetSizer(sizer)
            OpeningDialog.Fit()

            if OpeningDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PerValue[self.tree.GetItemText(treeItem)][7])
            OpeningDialog.Destroy()
            return
        
        if item.GetText()==u'进攻策略':
            StraDialog=wx.Dialog(None,-1,u'进攻策略')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(StraDialog,-1,u'列表-进攻策略')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            stralist=PerValue[self.tree.GetItemText(treeItem)][8].split(',')
            if '' in stralist:
                stralist.remove('')
            self.stra=wx.ListBox(StraDialog,-1,size=(300,250),choices=stralist)
            sizer.Add(self.stra,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            NewStra=wx.Button(StraDialog,-1,u'添加进攻策略',size=(-1,25))
            box.Add(NewStra,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.EditStra=wx.Button(StraDialog,-1,u'编辑进攻策略',size=(-1,25))
            self.EditStra.Enable(False)
            box.Add(self.EditStra,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)

            self.DelStra=wx.Button(StraDialog,-1,u'删除进攻策略',size=(-1,25))
            self.DelStra.Enable(False)
            sizer.Add(self.DelStra,0,wx.ALIGN_CENTER|wx.ALL,5)
          
            StraDialog.Bind(wx.EVT_LISTBOX,self.OnStra,self.stra)
            StraDialog.Bind(wx.EVT_LISTBOX_DCLICK,self.OnEditStra,self.stra)

            StraDialog.Bind(wx.EVT_BUTTON,self.OnNewStra,NewStra)
            StraDialog.Bind(wx.EVT_BUTTON,self.OnEditStra,self.EditStra)
            StraDialog.Bind(wx.EVT_BUTTON,self.OnDelStra,self.DelStra)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(StraDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(StraDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            StraDialog.SetSizer(sizer)
            StraDialog.Fit()

            if StraDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PerValue[self.tree.GetItemText(treeItem)][8])
            StraDialog.Destroy()
            return
            
        if item.GetText()==u'建造策略':
            BuildDialog=wx.Dialog(None,-1,u'建造策略')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(BuildDialog,-1,u'列表-建造策略')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            buildlist=PerValue[self.tree.GetItemText(treeItem)][9].split(',')
            if '' in buildlist:
                buildlist.remove('')
            self.build=wx.ListBox(BuildDialog,-1,size=(300,250),choices=buildlist)
            sizer.Add(self.build,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            NewBuild=wx.Button(BuildDialog,-1,u'添加建造策略',size=(-1,25))
            box.Add(NewBuild,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.EditBuild=wx.Button(BuildDialog,-1,u'编辑建造策略',size=(-1,25))
            self.EditBuild.Enable(False)
            box.Add(self.EditBuild,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)

            self.DelBuild=wx.Button(BuildDialog,-1,u'删除建造策略',size=(-1,25))
            self.DelBuild.Enable(False)
            sizer.Add(self.DelBuild,0,wx.ALIGN_CENTER|wx.ALL,5)
          
            BuildDialog.Bind(wx.EVT_LISTBOX,self.OnBuild,self.build)
            BuildDialog.Bind(wx.EVT_LISTBOX_DCLICK,self.OnEditBuild,self.build)

            BuildDialog.Bind(wx.EVT_BUTTON,self.OnNewBuild,NewBuild)
            BuildDialog.Bind(wx.EVT_BUTTON,self.OnEditBuild,self.EditBuild)
            BuildDialog.Bind(wx.EVT_BUTTON,self.OnDelBuild,self.DelBuild)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(BuildDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(BuildDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            BuildDialog.SetSizer(sizer)
            BuildDialog.Fit()

            if BuildDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PerValue[self.tree.GetItemText(treeItem)][9])
            BuildDialog.Destroy()
            return

        if item.GetText()==u'单位喜好':
            PreferDialog=wx.Dialog(None,-1,u'单位喜好')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(PreferDialog,-1,u'列表-喜好单位')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            preferlist=PerValue[self.tree.GetItemText(treeItem)][10].split(',')
            if '' in preferlist:
                preferlist.remove('')
            self.prefer=wx.ListBox(PreferDialog,-1,size=(300,250),choices=preferlist)
            sizer.Add(self.prefer,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            NewPrefer=wx.Button(PreferDialog,-1,u'添加喜好单位',size=(-1,25))
            box.Add(NewPrefer,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.DelPrefer=wx.Button(PreferDialog,-1,u'删除喜好单位',size=(-1,25))
            self.DelPrefer.Enable(False)
            box.Add(self.DelPrefer,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)
          
            PreferDialog.Bind(wx.EVT_LISTBOX,self.OnPrefer,self.prefer)

            PreferDialog.Bind(wx.EVT_BUTTON,self.OnNewPrefer,NewPrefer)
            PreferDialog.Bind(wx.EVT_BUTTON,self.OnDelPrefer,self.DelPrefer)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(PreferDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(PreferDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            PreferDialog.SetSizer(sizer)
            PreferDialog.Fit()

            if PreferDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PerValue[self.tree.GetItemText(treeItem)][10])
            PreferDialog.Destroy()
            return

        if item.GetText()==u'协议喜好':
            PowerDialog=wx.Dialog(None,-1,u'协议喜好')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(PowerDialog,-1,u'列表-喜好协议')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            powerlist=PerValue[self.tree.GetItemText(treeItem)][11].split(',')
            if '' in powerlist:
                powerlist.remove('')
            self.power=wx.ListBox(PowerDialog,-1,size=(300,250),choices=powerlist)
            sizer.Add(self.power,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            NewPower=wx.Button(PowerDialog,-1,u'添加喜好协议',size=(-1,25))
            box.Add(NewPower,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.DelPower=wx.Button(PowerDialog,-1,u'删除喜好协议',size=(-1,25))
            self.DelPower.Enable(False)
            box.Add(self.DelPower,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)
          
            PowerDialog.Bind(wx.EVT_LISTBOX,self.OnPower,self.power)

            PowerDialog.Bind(wx.EVT_BUTTON,self.OnNewPower,NewPower)
            PowerDialog.Bind(wx.EVT_BUTTON,self.OnDelPower,self.DelPower)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(PowerDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(PowerDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            PowerDialog.SetSizer(sizer)
            PowerDialog.Fit()

            if PowerDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PerValue[self.tree.GetItemText(treeItem)][11])
            PowerDialog.Destroy()
            return

        if item.GetText()==u'单位上限':
            CapDialog=wx.Dialog(None,-1,u'单位上限')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(CapDialog,-1,u'列表-单位')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            caplist=PerValue[self.tree.GetItemText(treeItem)][12].split(',')
            if '' in caplist:
                caplist.remove('')
            self.cap=wx.ListBox(CapDialog,-1,size=(300,250),choices=caplist)
            sizer.Add(self.cap,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            NewCap=wx.Button(CapDialog,-1,u'添加单位',size=(-1,25))
            box.Add(NewCap,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.DelCap=wx.Button(CapDialog,-1,u'删除单位',size=(-1,25))
            self.DelCap.Enable(False)
            box.Add(self.DelCap,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)
          
            CapDialog.Bind(wx.EVT_LISTBOX,self.OnCap,self.cap)

            CapDialog.Bind(wx.EVT_BUTTON,self.OnNewCap,NewCap)
            CapDialog.Bind(wx.EVT_BUTTON,self.OnDelCap,self.DelCap)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(CapDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(CapDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            CapDialog.SetSizer(sizer)
            CapDialog.Fit()

            if CapDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PerValue[self.tree.GetItemText(treeItem)][12])
            CapDialog.Destroy()
            return
        if item.GetText()==u'最大目标数':
            MaxTargetDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)
            
            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(MaxTargetDialog,-1,u'最大目标数  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            spin=wx.SpinCtrl(MaxTargetDialog,-1,'')
            spin.SetRange(1,20)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                spin.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText()))
            else:
                spin.SetValue(2)
            box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(MaxTargetDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(MaxTargetDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            MaxTargetDialog.SetSizer(sizer)
            MaxTargetDialog.Fit()

            if MaxTargetDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(spin.GetValue()))
                AttackValue[self.tree.GetItemText(treeItem)][0]=str(spin.GetValue())
            MaxTargetDialog.Destroy()
            return

        if item.GetText()==u'flag':
            flagDialog=wx.Dialog(None,-1,u'编辑字符串')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(flagDialog,-1,u'玩家名称  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            self.playerName=wx.TextCtrl(flagDialog,-1,size=(100,-1))
            box.Add(self.playerName,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)
            
            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(flagDialog,-1,u'flag名称  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            self.flag=wx.TextCtrl(flagDialog,-1,size=(100,-1))
            box.Add(self.flag,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)
            
            NoFlag=wx.CheckBox(flagDialog,-1,u'不设置flag ：',style=wx.ALIGN_RIGHT)
            NoFlag.SetValue(False)
            sizer.Add(NoFlag,0,wx.ALIGN_CENTER|wx.ALL,5)

            flagDialog.Bind(wx.EVT_CHECKBOX,self.OnNoFlag,NoFlag)

            box=wx.StaticBox(flagDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(flagDialog,-1,u'通过在地图里设置flag的值来激活或抑制\n此策略，在地图里选flag时这个flag选项为\n玩家名称/flag名称\n如 Japan01/Mission_Completed')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(flagDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(flagDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            flagDialog.SetSizer(sizer)
            flagDialog.Fit()

            if flagDialog.ShowModal()==wx.ID_OK:
                if NoFlag.GetValue():
                    self.list.SetStringItem(event.GetIndex(),1,'')
                    AttackValue[self.tree.GetItemText(treeItem)][1]=''
                    return
                if self.playerName.GetValue()=='' or self.flag.GetValue()=='':
                    return
                self.list.SetStringItem(event.GetIndex(),1,self.playerName.GetValue()+'/'+self.flag.GetValue())
                AttackValue[self.tree.GetItemText(treeItem)][1]=self.playerName.GetValue()+'/'+self.flag.GetValue()
            flagDialog.Destroy()
            return

        if item.GetText()==u'活跃时间':
            ActiveTimeDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(ActiveTimeDialog,-1,u'时间间隔  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            self.IntervalTime=wx.SpinCtrl(ActiveTimeDialog,-1,'')
            self.IntervalTime.SetRange(0,360)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                self.IntervalTime.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText().split(',')[0]))
            else:
                self.IntervalTime.SetValue(60)
            box.Add(self.IntervalTime,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)
            
            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(ActiveTimeDialog,-1,u'活跃时续时间  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            self.ActiveTime=wx.SpinCtrl(ActiveTimeDialog,-1,'')
            self.ActiveTime.SetRange(0,360)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                self.ActiveTime.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText().split(',')[1]))
            else:
                self.ActiveTime.SetValue(60)
            box.Add(self.ActiveTime,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            NoTime=wx.CheckBox(ActiveTimeDialog,-1,u'不设置时间 ：',style=wx.ALIGN_RIGHT)
            NoTime.SetValue(False)
            sizer.Add(NoTime,0,wx.ALIGN_CENTER|wx.ALL,5)

            ActiveTimeDialog.Bind(wx.EVT_CHECKBOX,self.NoTime,NoTime)

            box=wx.StaticBox(ActiveTimeDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(ActiveTimeDialog,-1,u'AI将从被激活（能自主行动）开始计时\n单位为秒')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(ActiveTimeDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(ActiveTimeDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            ActiveTimeDialog.SetSizer(sizer)
            ActiveTimeDialog.Fit()

            if ActiveTimeDialog.ShowModal()==wx.ID_OK:
                if NoTime.GetValue():
                    self.list.SetStringItem(event.GetIndex(),1,'')
                    AttackValue[self.tree.GetItemText(treeItem)][2]=''
                    return
                self.list.SetStringItem(event.GetIndex(),1,str(self.IntervalTime.GetValue())+','+str(self.ActiveTime.GetValue()))
                AttackValue[self.tree.GetItemText(treeItem)][2]=str(self.IntervalTime.GetValue())+','+str(self.ActiveTime.GetValue())
            ActiveTimeDialog.Destroy()
            return

        if item.GetText()==u'触发单位':
            trigUnitDialog=wx.Dialog(None,-1,u'编辑触发单位')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(trigUnitDialog,-1,u'----关系----')
            sizer.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            RelationList={u'敌人':'ENEMIES',u'同一玩家':'SAME_PLAYER'}
            self.Relation=wx.Choice(trigUnitDialog,-1,size=(100,-1),choices=RelationList.keys())
            self.Relation.SetSelection(0)
            sizer.Add(self.Relation,0,wx.ALIGN_CENTER|wx.ALL,3)

            
            label=wx.StaticText(trigUnitDialog,-1,u'----单位----')
            sizer.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            
            conn=sqlite3.connect('UnitList.db')
            cur=conn.cursor()
            cur.execute("select * from Unitname")
            res=cur.fetchall()
            namelist=[u'无']
            for name in res:
                namelist.append(name[0])
                
            self.UnitChoice1=wx.Choice(trigUnitDialog,-1,size=(100,-1),choices=namelist)
            self.UnitChoice1.SetSelection(0)
            sizer.Add(self.UnitChoice1,0,wx.ALIGN_CENTER|wx.ALL,3)
            self.UnitChoice2=wx.Choice(trigUnitDialog,-1,size=(100,-1),choices=namelist)
            self.UnitChoice2.SetSelection(0)
            sizer.Add(self.UnitChoice2,0,wx.ALIGN_CENTER|wx.ALL,6)
            self.UnitChoice3=wx.Choice(trigUnitDialog,-1,size=(100,-1),choices=namelist)
            self.UnitChoice3.SetSelection(0)
            sizer.Add(self.UnitChoice3,0,wx.ALIGN_CENTER|wx.ALL,6)

            NoTrigUnit=wx.CheckBox(trigUnitDialog,-1,u'不设置触发单位 ：',style=wx.ALIGN_RIGHT)
            NoTrigUnit.SetValue(False)
            sizer.Add(NoTrigUnit,0,wx.ALIGN_CENTER|wx.ALL,5)

            trigUnitDialog.Bind(wx.EVT_CHECKBOX,self.NoTrigUnit,NoTrigUnit)

            box=wx.StaticBox(trigUnitDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(trigUnitDialog,-1,u'AI探测到这些单位时将启发策略\n并且单位与AI要符合这个关系')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(trigUnitDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(trigUnitDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            trigUnitDialog.SetSizer(sizer)
            trigUnitDialog.Fit()

            if trigUnitDialog.ShowModal()==wx.ID_OK:
                if NoTrigUnit.GetValue():
                    self.list.SetStringItem(event.GetIndex(),1,'')
                    AttackValue[self.tree.GetItemText(treeItem)][3]=''
                    return
                if self.UnitChoice1.GetStringSelection()==u'无' and self.UnitChoice2.GetStringSelection()==u'无' and self.UnitChoice3.GetStringSelection()==u'无':
                    warning=wx.MessageDialog(None,u'至少选择一个触发单位',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    trigUnitDialog.Destroy()
                    return
                trigUnitStr1=self.Relation.GetStringSelection()+','
                trigUnitStr2=RelationList[self.Relation.GetStringSelection()]+','
                if self.UnitChoice1.GetStringSelection()!=u'无':
                    trigUnitStr1+=self.UnitChoice1.GetStringSelection()+','
                    cur.execute("select * from Unitname WHERE name=(?)",(self.UnitChoice1.GetStringSelection(),))
                    res=cur.fetchall()
                    trigUnitStr2+=res[0][1]+','
                else:
                    trigUnitStr2+=self.UnitChoice1.GetStringSelection()+','
                if self.UnitChoice2.GetStringSelection()!=u'无':
                    trigUnitStr1+=self.UnitChoice2.GetStringSelection()+','
                    cur.execute("select * from Unitname WHERE name=(?)",(self.UnitChoice2.GetStringSelection(),))
                    res=cur.fetchall()
                    trigUnitStr2+=res[0][1]+','
                else:
                    trigUnitStr2+=self.UnitChoice2.GetStringSelection()+','
                if self.UnitChoice3.GetStringSelection()!=u'无':
                    trigUnitStr1+=self.UnitChoice3.GetStringSelection()+','
                    cur.execute("select * from Unitname WHERE name=(?)",(self.UnitChoice3.GetStringSelection(),))
                    res=cur.fetchall()
                    trigUnitStr2+=res[0][1]+','
                else:
                    trigUnitStr2+=self.UnitChoice3.GetStringSelection()+','
                if trigUnitStr1.endswith(','):
                    trigUnitStr1=trigUnitStr1.rstrip(',')
                if trigUnitStr2.endswith(','):
                    trigUnitStr2=trigUnitStr2.rstrip(',')
                self.list.SetStringItem(event.GetIndex(),1,trigUnitStr1)
                AttackValue[self.tree.GetItemText(treeItem)][3]=trigUnitStr2
            trigUnitDialog.Destroy()
            cur.close()
            conn.close()
            return

        if item.GetText()==u'目标':
            TargetDialog=wx.Dialog(None,-1,u'编辑目标')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(TargetDialog,-1,u'列表-目标')
            sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

            targetlist=AttackValue[self.tree.GetItemText(treeItem)][4].split(',')
            if '' in targetlist:
                targetlist.remove('')
            self.target=wx.ListBox(TargetDialog,-1,size=(300,250),choices=targetlist)
            sizer.Add(self.target,0,wx.ALIGN_CENTER|wx.ALL,5)

            box=wx.BoxSizer(wx.HORIZONTAL)
            AddTarget=wx.Button(TargetDialog,-1,u'添加目标',size=(-1,25))
            box.Add(AddTarget,0,wx.ALIGN_CENTER|wx.ALL,2)
            self.DelTarget=wx.Button(TargetDialog,-1,u'删除目标',size=(-1,25))
            self.DelTarget.Enable(False)
            box.Add(self.DelTarget,0,wx.ALIGN_CENTER|wx.ALL,2)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,5)

            AddNewTarget=wx.Button(TargetDialog,-1,u'添加自定目标',size=(-1,25))
            sizer.Add(AddNewTarget,0,wx.ALIGN_CENTER|wx.ALL,2)
          
            TargetDialog.Bind(wx.EVT_LISTBOX,self.OnTarget,self.target)

            TargetDialog.Bind(wx.EVT_BUTTON,self.OnAddTarget,AddTarget)
            TargetDialog.Bind(wx.EVT_BUTTON,self.OnDelTarget,self.DelTarget)
            TargetDialog.Bind(wx.EVT_BUTTON,self.OnAddNewTarget,AddNewTarget)
                        
            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(TargetDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(TargetDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            TargetDialog.SetSizer(sizer)
            TargetDialog.Fit()

            if TargetDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,AttackValue[self.tree.GetItemText(treeItem)][4])
            TargetDialog.Destroy()
            return
        
        if item.GetText()==u'战术':
            TacticDialog=wx.Dialog(None,-1,u'编辑战术')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(TacticDialog,-1,u'选择一个战术 :')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            TacticList=['DefenseAvoidanceAttack','SimpleAttack','StaticDefense','SimpleExpansion']
            TacticChoice=wx.Choice(TacticDialog,-1,size=(170,-1),choices=TacticList)
            if AttackValue[self.tree.GetItemText(treeItem)][5]=='':
                TacticChoice.SetSelection(0)
            else:
                TacticChoice.SetStringSelection(AttackValue[self.tree.GetItemText(treeItem)][5])
            box.Add(TacticChoice,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.StaticBox(TacticDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(TacticDialog,-1,u'战术决定了该队伍是要进攻，防守,\n还是拓展')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(TacticDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(TacticDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            TacticDialog.SetSizer(sizer)
            TacticDialog.Fit()

            if TacticDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,TacticChoice.GetStringSelection())
                AttackValue[self.tree.GetItemText(treeItem)][5]=TacticChoice.GetStringSelection()
            TacticDialog.Destroy()
            return

        if item.GetText()==u'最大活动距离':
            DistanceDialog=wx.Dialog(None,-1,u'编辑数值')
            sizer=wx.BoxSizer(wx.VERTICAL)
            
            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(DistanceDialog,-1,u'最大活动距离:')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            self.Distance=wx.SpinCtrlDouble(DistanceDialog,value='100.0',min=0,max=1000,inc=0.5)
            self.Distance.SetDigits(1)
            box.Add(self.Distance,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            NoDistance=wx.CheckBox(DistanceDialog,-1,u'不设置活动距离 ：',style=wx.ALIGN_RIGHT)
            NoDistance.SetValue(False)
            sizer.Add(NoDistance,0,wx.ALIGN_CENTER|wx.ALL,5)

            DistanceDialog.Bind(wx.EVT_CHECKBOX,self.NoDistance,NoDistance)

            box=wx.StaticBox(DistanceDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(DistanceDialog,-1,u'大概是指离目标的距离,当目标为\n友军时，将保持与友军在这个距离内')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(DistanceDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(DistanceDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            DistanceDialog.SetSizer(sizer)
            DistanceDialog.Fit()

            if DistanceDialog.ShowModal()==wx.ID_OK:
                if NoDistance.GetValue():
                    self.list.SetStringItem(event.GetIndex(),1,'')
                    AttackValue[self.tree.GetItemText(treeItem)][6]=''
                    return
                self.list.SetStringItem(event.GetIndex(),1,str(self.Distance.GetValue()))
                AttackValue[self.tree.GetItemText(treeItem)][6]=str(self.Distance.GetValue())
            DistanceDialog.Destroy()
            return

        if item.GetText()==u'结束时的行为':
            EndBehavDialog=wx.Dialog(None,-1,u'编辑行为')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(EndBehavDialog,-1,u'选择一个行为 :')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            EndBehavList=['RAMPAGE','DISBAND','RETURN_HOME_AND_DISBAND']
            EndBehavChoice=wx.Choice(EndBehavDialog,-1,size=(170,-1),choices=EndBehavList)
            if AttackValue[self.tree.GetItemText(treeItem)][7]=='':
                EndBehavChoice.SetSelection(0)
            else:
                EndBehavChoice.SetStringSelection(AttackValue[self.tree.GetItemText(treeItem)][7])
            box.Add(EndBehavChoice,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.StaticBox(EndBehavDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(EndBehavDialog,-1,u'当结此策略时队伍的行为')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(EndBehavDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(EndBehavDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            EndBehavDialog.SetSizer(sizer)
            EndBehavDialog.Fit()

            if EndBehavDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,EndBehavChoice.GetStringSelection())
                AttackValue[self.tree.GetItemText(treeItem)][7]=EndBehavChoice.GetStringSelection()
            EndBehavDialog.Destroy()
            return

        if item.GetText()==u'队伍数目':
            TeamNumberDialog=wx.Dialog(None,-1,u'编辑整数')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(TeamNumberDialog,-1,u'最大数目  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            MaxNumber=wx.SpinCtrl(TeamNumberDialog,-1,'')
            MaxNumber.SetRange(2,999)
            box.Add(MaxNumber,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(TeamNumberDialog,-1,u'最小数目  ：')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            MinNumber=wx.SpinCtrl(TeamNumberDialog,-1,'')
            MinNumber.SetRange(1,50)
            box.Add(MinNumber,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            if self.list.GetItem(event.GetIndex(),1).GetText().split(',')!=['']:
                MinNumber.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText().split(',')[0]))
                MaxNumber.SetValue(int(self.list.GetItem(event.GetIndex(),1).GetText().split(',')[1]))
            else:
                MinNumber.SetValue(6)
                MaxNumber.SetValue(15)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(TeamNumberDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(TeamNumberDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            TeamNumberDialog.SetSizer(sizer)
            TeamNumberDialog.Fit()

            if TeamNumberDialog.ShowModal()==wx.ID_OK:
                if MinNumber.GetValue()>MaxNumber.GetValue():
                    warning=wx.MessageDialog(None,u'最小数目不能大于最大数目',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    TeamNumberDialog.Destroy()
                self.list.SetStringItem(event.GetIndex(),1,','.join([str(MinNumber.GetValue()),str(MaxNumber.GetValue())]))
                AttackValue[self.tree.GetItemText(treeItem)][8]=','.join([str(MinNumber.GetValue()),str(MaxNumber.GetValue())])
            TeamNumberDialog.Destroy()
            return

        if item.GetText()==u'排除的类型':
            ExcluKindDialog=wx.Dialog(None,-1,u'选择排除类型')
            sizer=wx.BoxSizer(wx.VERTICAL)

            ExcluKindList=['IGNORES_SELECT_ALL','AIRCRAFT','BOMBER_AIRCRAFT','HARVESTER','ASSAULT_AIRCRAFT','FIGHTER_AIRCRAFT']

            box1=wx.BoxSizer(wx.HORIZONTAL)
            
            box=wx.BoxSizer(wx.VERTICAL)
            Exclu1=wx.CheckBox(ExcluKindDialog,-1,ExcluKindList[0])
            box.Add(Exclu1,0,wx.LEFT)
            Exclu2=wx.CheckBox(ExcluKindDialog,-1,ExcluKindList[1])
            box.Add(Exclu2,0,wx.LEFT)
            Exclu3=wx.CheckBox(ExcluKindDialog,-1,ExcluKindList[2])
            box.Add(Exclu3,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.BoxSizer(wx.VERTICAL)
            Exclu4=wx.CheckBox(ExcluKindDialog,-1,ExcluKindList[3])
            box.Add(Exclu4,0,wx.LEFT)
            Exclu5=wx.CheckBox(ExcluKindDialog,-1,ExcluKindList[4])
            box.Add(Exclu5,0,wx.LEFT)
            Exclu6=wx.CheckBox(ExcluKindDialog,-1,ExcluKindList[5])
            box.Add(Exclu6,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)
            
            sizer.Add(box1,0,wx.ALIGN_CENTER|wx.ALL,3)

            strlist=self.list.GetItem(event.GetIndex(),1).GetText().split(' ')
            if ExcluKindList[0] in strlist:
                Exclu1.SetValue(True)
            else:
                Exclu1.SetValue(False)
            if ExcluKindList[1] in strlist:
                Exclu2.SetValue(True)
            else:
                Exclu2.SetValue(False)
            if ExcluKindList[2] in strlist:
                Exclu3.SetValue(True)
            else:
                Exclu3.SetValue(False)
            if ExcluKindList[3] in strlist:
                Exclu4.SetValue(True)
            else:
                Exclu4.SetValue(False)
            if ExcluKindList[4] in strlist:
                Exclu5.SetValue(True)
            else:
                Exclu5.SetValue(False)
            if ExcluKindList[5] in strlist:
                Exclu6.SetValue(True)
            else:
                Exclu6.SetValue(False)

            box=wx.StaticBox(ExcluKindDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(ExcluKindDialog,-1,u'AI使用此策略时排除的单位类型,\n一般只用勾选第一排的,\n对于骚扰策略则只勾第一个')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(ExcluKindDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(ExcluKindDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            ExcluKindDialog.SetSizer(sizer)
            ExcluKindDialog.Fit()

            if ExcluKindDialog.ShowModal()==wx.ID_OK:
                strlist=[]
                if Exclu1.GetValue():
                    strlist.append(ExcluKindList[0])
                if Exclu2.GetValue():
                    strlist.append(ExcluKindList[1])
                if Exclu3.GetValue():
                    strlist.append(ExcluKindList[2])
                if Exclu4.GetValue():
                    strlist.append(ExcluKindList[3])
                if Exclu5.GetValue():
                    strlist.append(ExcluKindList[4])
                if Exclu6.GetValue():
                    strlist.append(ExcluKindList[5])
                
                self.list.SetStringItem(event.GetIndex(),1,' '.join(strlist))
                AttackValue[self.tree.GetItemText(treeItem)][9]=' '.join(strlist)
            ExcluKindDialog.Destroy()
            return

        if item.GetText()==u'允许的运动类型':
            LocomotorDialog=wx.Dialog(None,-1,u'选择允许的运动类型')
            sizer=wx.BoxSizer(wx.VERTICAL)

            LocomotorList=['AMPHIBIOUS','LAND','AIRCRAFT','AIR','WATER','FIGHTER_AIRCRAFT']

            box1=wx.BoxSizer(wx.HORIZONTAL)
            
            box=wx.BoxSizer(wx.VERTICAL)
            Locomotor1=wx.CheckBox(LocomotorDialog,-1,LocomotorList[0])
            box.Add(Locomotor1,0,wx.LEFT)
            Locomotor2=wx.CheckBox(LocomotorDialog,-1,LocomotorList[1])
            box.Add(Locomotor2,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.BoxSizer(wx.VERTICAL)
            Locomotor3=wx.CheckBox(LocomotorDialog,-1,LocomotorList[2])
            box.Add(Locomotor3,0,wx.LEFT)
            Locomotor4=wx.CheckBox(LocomotorDialog,-1,LocomotorList[3])
            box.Add(Locomotor4,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)
            
            sizer.Add(box1,0,wx.ALIGN_CENTER|wx.ALL,3)

            strlist=self.list.GetItem(event.GetIndex(),1).GetText().split(',')
            if LocomotorList[0] in strlist:
                Locomotor1.SetValue(True)
            else:
                Locomotor1.SetValue(False)
            if LocomotorList[1] in strlist:
                Locomotor2.SetValue(True)
            else:
                Locomotor2.SetValue(False)
            if LocomotorList[2] in strlist:
                Locomotor3.SetValue(True)
            else:
                Locomotor3.SetValue(False)
            if LocomotorList[3] in strlist:
                Locomotor4.SetValue(True)
            else:
                Locomotor4.SetValue(False)

            box=wx.StaticBox(LocomotorDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(LocomotorDialog,-1,u'AI将根据单位运动类型筛选\n是否加入此策略的队伍')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(LocomotorDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(LocomotorDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            LocomotorDialog.SetSizer(sizer)
            LocomotorDialog.Fit()

            if LocomotorDialog.ShowModal()==wx.ID_OK:
                strlist=[]
                if Locomotor1.GetValue():
                    strlist.append(LocomotorList[0])
                if Locomotor2.GetValue():
                    strlist.append(LocomotorList[1])
                if Locomotor3.GetValue():
                    strlist.append(LocomotorList[2])
                if Locomotor4.GetValue():
                    strlist.append(LocomotorList[3])
                
                self.list.SetStringItem(event.GetIndex(),1,','.join(strlist))
                AttackValue[self.tree.GetItemText(treeItem)][10]=','.join(strlist)
            LocomotorDialog.Destroy()
            return

        if item.GetText()==u'优先权':
            PriorityDialog=wx.Dialog(None,-1,u'选择优先权')
            sizer=wx.BoxSizer(wx.VERTICAL)

            box=wx.BoxSizer(wx.HORIZONTAL)
            label=wx.StaticText(PriorityDialog,-1,u'选择一个优先权 :')
            box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            PriorityList=['STANDARD','HIGH','LOW','DEFENSE']
            PriorityChoice=wx.Choice(PriorityDialog,-1,size=(170,-1),choices=PriorityList)
            if AttackValue[self.tree.GetItemText(treeItem)][11]=='':
                PriorityChoice.SetSelection(0)
            else:
                PriorityChoice.SetStringSelection(AttackValue[self.tree.GetItemText(treeItem)][11])
            box.Add(PriorityChoice,0,wx.ALIGN_CENTER|wx.ALL,3)
            sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.StaticBox(PriorityDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(PriorityDialog,-1,u'优先权决定AI先考虑哪个策略')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(PriorityDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(PriorityDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            PriorityDialog.SetSizer(sizer)
            PriorityDialog.Fit()

            if PriorityDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,PriorityChoice.GetStringSelection())
                AttackValue[self.tree.GetItemText(treeItem)][11]=PriorityChoice.GetStringSelection()
            PriorityDialog.Destroy()
            return

        if item.GetText()==u'总是招募':
            RecruitDialog=wx.Dialog(None,-1,u'编辑布尔值')
            sizer=wx.BoxSizer(wx.VERTICAL)
            Recruit=wx.CheckBox(RecruitDialog,-1,u'总是招募   :',style=wx.ALIGN_RIGHT)
            if self.list.GetItem(event.GetIndex(),1).GetText()!='':
                Recruit.SetValue(boolchange(AttackValue[self.tree.GetItemText(treeItem)][12]))
            sizer.Add(Recruit,0,wx.ALIGN_CENTER|wx.ALL,10)

            box=wx.StaticBox(RecruitDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(RecruitDialog,-1,u'AI是否总是使用此策略')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(RecruitDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(RecruitDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            RecruitDialog.SetSizer(sizer)
            RecruitDialog.Fit()
            if RecruitDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,str(Recruit.GetValue()))
                AttackValue[self.tree.GetItemText(treeItem)][12]=str(Recruit.GetValue())
            RecruitDialog.Destroy()
            return

        if item.GetText()==u'生产单位':
            CreateUnitDialog=wx.Dialog(None,-1,u'选择允许的运动类型')
            sizer=wx.BoxSizer(wx.VERTICAL)

            LocomotorList=['AMPHIBIOUS','LAND','AIRCRAFT','AIR','WATER','FIGHTER_AIRCRAFT']

            box1=wx.BoxSizer(wx.HORIZONTAL)

            box=wx.BoxSizer(wx.VERTICAL)
            conn=sqlite3.connect('UnitList.db')
            cur=conn.cursor()
            cur.execute("select * from Unitname")
            res=cur.fetchall()
            namelist=[]
            for name in res:
                namelist.append(name[0])

            label=wx.StaticBox(CreateUnitDialog,-1,u'单位')
            box.Add(label,0,wx.LEFT)
            self.CreateChoice1=wx.Choice(CreateUnitDialog,-1,size=(130,-1),choices=namelist)
            self.CreateChoice1.SetSelection(0)
            box.Add(self.CreateChoice1,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.BoxSizer(wx.VERTICAL)
            label=wx.StaticBox(CreateUnitDialog,-1,u'最小数目')
            box.Add(label,0,wx.LEFT)
            self.MinNumber1=wx.SpinCtrl(CreateUnitDialog,-1,'')
            self.MinNumber1.SetRange(1,20)
            box.Add(self.MinNumber1,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            box=wx.BoxSizer(wx.VERTICAL)
            label=wx.StaticBox(CreateUnitDialog,-1,u'最大数目')
            box.Add(label,0,wx.LEFT)
            self.MaxNumber1=wx.SpinCtrl(CreateUnitDialog,-1,'')
            self.MaxNumber1.SetRange(2,40)
            box.Add(self.MaxNumber1,0,wx.LEFT)
            box1.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

            if self.list.GetItem(event.GetIndex(),1).GetText().split(',')!=['']:
                CreateUnitStr=self.list.GetItem(event.GetIndex(),1).GetText().split(',')
                self.CreateChoice1.SetStringSelection(CreateUnitStr[0])
                self.MinNumber1.SetValue(int(CreateUnitStr[1]))
                self.MaxNumber1.SetValue(int(CreateUnitStr[2]))
            else:
                self.CreateChoice1.SetSelection(0)
                self.MinNumber1.SetValue(1)
                self.MaxNumber1.SetValue(2)
            
            sizer.Add(box1,0,wx.ALIGN_CENTER|wx.ALL,3)

            NoCreateUnit=wx.CheckBox(CreateUnitDialog,-1,u'不生产单位       ：',style=wx.ALIGN_RIGHT)
            NoCreateUnit.SetValue(False)
            sizer.Add(NoCreateUnit,0,wx.ALIGN_CENTER|wx.ALL,8)

            CreateUnitDialog.Bind(wx.EVT_CHECKBOX,self.NoCreateUnit,NoCreateUnit)
            
            box=wx.StaticBox(CreateUnitDialog,-1,'')
            bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

            label=wx.StaticText(CreateUnitDialog,-1,u'AI在使用此策略时被强制生产的单位')
            label.SetForegroundColour('DIM GREY')
            bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
            sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(CreateUnitDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(CreateUnitDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            CreateUnitDialog.SetSizer(sizer)
            CreateUnitDialog.Fit()

            if CreateUnitDialog.ShowModal()==wx.ID_OK:
                if NoCreateUnit.GetValue():
                    self.list.SetStringItem(event.GetIndex(),1,'')
                    AttackValue[self.tree.GetItemText(treeItem)][14]=''
                    return
                if self.MinNumber1.GetValue()>self.MaxNumber1.GetValue():
                    warning=wx.MessageDialog(None,u'最小数目不能大于最大数目',u'警告',style=wx.OK)
                    warning.ShowModal()
                    warning.Destroy()
                    CreateUnitDialogDialog.Destroy()
                else:
                    CreateUnitStr1=','.join([self.CreateChoice1.GetStringSelection(),str(self.MinNumber1.GetValue()),str(self.MaxNumber1.GetValue())])
                    cur.execute("select * from Unitname WHERE name=(?)",(self.CreateChoice1.GetStringSelection(),))
                    res=cur.fetchall()
                    CreateUnitStr2=','.join([res[0][1],str(self.MinNumber1.GetValue()),str(self.MaxNumber1.GetValue())])
                self.list.SetStringItem(event.GetIndex(),1,CreateUnitStr1)
                AttackValue[self.tree.GetItemText(treeItem)][14]=CreateUnitStr2
            cur.close()
            conn.close()
            CreateUnitDialog.Destroy()
            return

        if item.GetText()==u'微操':
            MicroManagerDialog=wx.Dialog(None,-1,u'选择微操')
            sizer=wx.BoxSizer(wx.VERTICAL)

            label=wx.StaticText(MicroManagerDialog,-1,u'选择一个微操 :')
            sizer.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
            MicroManagerChoice=wx.ListBox(MicroManagerDialog,-1,size=(280,320),choices=MicroManagerList)
            if AttackValue[self.tree.GetItemText(treeItem)][13]=='':
                MicroManagerChoice.SetSelection(0)
            else:
                MicroManagerChoice.SetStringSelection(AttackValue[self.tree.GetItemText(treeItem)][14])
            sizer.Add(MicroManagerChoice,0,wx.ALIGN_CENTER|wx.ALL,6)

            btnsizer=wx.StdDialogButtonSizer()
            btn=wx.Button(MicroManagerDialog,wx.ID_OK,size=(-1,25))
            btnsizer.AddButton(btn)
            btn=wx.Button(MicroManagerDialog,wx.ID_CANCEL,size=(-1,25))
            btnsizer.AddButton(btn)
            btnsizer.Realize()
            sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

            MicroManagerDialog.SetSizer(sizer)
            MicroManagerDialog.Fit()

            if MicroManagerDialog.ShowModal()==wx.ID_OK:
                self.list.SetStringItem(event.GetIndex(),1,MicroManagerChoice.GetStringSelection())
                AttackValue[self.tree.GetItemText(treeItem)][13]=MicroManagerChoice.GetStringSelection()
            MicroManagerDialog.Destroy()
            return
            
    def OnNoFlag(self,event):
        if event.IsChecked():
            self.playerName.Clear()
            self.flag.Clear()
            self.playerName.Enable(False)
            self.flag.Enable(False)
        else:
            self.playerName.Enable(True)
            self.flag.Enable(True)

    def NoTime(self,event):
        if event.IsChecked():
            self.IntervalTime.Enable(False)
            self.ActiveTime.Enable(False)
        else:
            self.IntervalTime.Enable(True)
            self.ActiveTime.Enable(True)

    def NoTrigUnit(self,event):
        if event.IsChecked():
            self.Relation.Enable(False)
            self.UnitChoice1.Enable(False)
            self.UnitChoice2.Enable(False)
            self.UnitChoice3.Enable(False)
        else:
            self.Relation.Enable(True)
            self.UnitChoice1.Enable(True)
            self.UnitChoice2.Enable(True)
            self.UnitChoice3.Enable(True)

    def NoDistance(self,event):
        if event.IsChecked():
            self.Distance.Enable(False)
        else:
            self.Distance.Enable(True)

    def NoCreateUnit(self,event):
        if event.IsChecked():
            self.CreateChoice1.Enable(False)
            self.MinNumber1.Enable(False)
            self.MaxNumber1.Enable(False)
        else:
            self.CreateChoice1.Enable(True) 
            self.MinNumber1.Enable(True)
            self.MaxNumber1.Enable(True)
           

    def OnOpenings(self,event):
        if self.Openings.GetStringSelection()=='':
            self.DelOpen.Enable(False)
            self.EditOpen.Enable(False)
        else:
            self.DelOpen.Enable(True)
            self.EditOpen.Enable(True)

    def OnNewOpen(self,event):
        OpeningList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(OpeningList,-1,u'选择一个开场行为')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceOpen=wx.ListBox(OpeningList,-1,size=(250,350),choices=NewOpenings)
        sizer.Add(self.ChoiceOpen,0,wx.ALIGN_CENTER|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(OpeningList,-1,u'权重  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin=wx.SpinCtrl(OpeningList,-1,'')
        spin.SetRange(10,100)
        spin.SetValue(100)
        box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        label=wx.StaticText(OpeningList,-1,u'何种难度使用')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        Easy=wx.CheckBox(OpeningList,-1,u'简单',style=wx.ALIGN_RIGHT)
        Easy.SetValue(True)
        box.Add(Easy,0,wx.ALIGN_CENTER|wx.ALL,2)
        Medium=wx.CheckBox(OpeningList,-1,u'中等',style=wx.ALIGN_RIGHT)
        Medium.SetValue(True)
        box.Add(Medium,0,wx.ALIGN_CENTER|wx.ALL,2)
        Hard=wx.CheckBox(OpeningList,-1,u'困难',style=wx.ALIGN_RIGHT)
        Hard.SetValue(True)
        box.Add(Hard,0,wx.ALIGN_CENTER|wx.ALL,2)
        Brutal=wx.CheckBox(OpeningList,-1,u'凶残',style=wx.ALIGN_RIGHT)
        Brutal.SetValue(True)
        box.Add(Brutal,0,wx.ALIGN_CENTER|wx.ALL,2)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,2)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(OpeningList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(OpeningList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        OpeningList.SetSizer(sizer)
        OpeningList.Fit()

        treeItem=self.tree.GetSelection()
        if OpeningList.ShowModal()==wx.ID_OK:
            if self.ChoiceOpen.GetStringSelection()=='':
                OpeningList.Destroy()
                return
            if self.Openings.FindString(self.ChoiceOpen.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                OpeningList.Destroy()
                return
            self.Openings.Append(self.ChoiceOpen.GetStringSelection())
            if PerValue[self.tree.GetItemText(treeItem)][7]=='':
                PerValue[self.tree.GetItemText(treeItem)][7]+=self.ChoiceOpen.GetStringSelection()
            else:
                PerValue[self.tree.GetItemText(treeItem)][7]+=','+self.ChoiceOpen.GetStringSelection()
            OpeningItem=OpeningDic[self.tree.GetItemText(treeItem)]
            OpeningItem[self.ChoiceOpen.GetStringSelection()]=[]
            DifficultList=OpeningItem[self.ChoiceOpen.GetStringSelection()]
            DifficultList.append(str(spin.GetValue()))
            DifficultList.append(str(Easy.GetValue()))
            DifficultList.append(str(Medium.GetValue()))
            DifficultList.append(str(Hard.GetValue()))
            DifficultList.append(str(Brutal.GetValue()))
        OpeningList.Destroy()

    def OnEditOpen(self,event):
        treeItem=self.tree.GetSelection()
        
        OpeningList=wx.Dialog(None,-1,u'编辑')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(OpeningList,-1,u'选择一个开场行为')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceOpen=wx.ListBox(OpeningList,-1,size=(250,350),choices=NewOpenings)
        self.ChoiceOpen.SetStringSelection(self.Openings.GetStringSelection())
        sizer.Add(self.ChoiceOpen,0,wx.ALIGN_CENTER|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(OpeningList,-1,u'权重  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin=wx.SpinCtrl(OpeningList,-1,'')
        spin.SetRange(10,100)
        spin.SetValue(int(OpeningDic[self.tree.GetItemText(treeItem)][self.Openings.GetStringSelection()][0]))
        box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        label=wx.StaticText(OpeningList,-1,u'何种难度使用')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        Easy=wx.CheckBox(OpeningList,-1,u'简单',style=wx.ALIGN_RIGHT)
        Easy.SetValue(boolchange(OpeningDic[self.tree.GetItemText(treeItem)][self.Openings.GetStringSelection()][1]))
        box.Add(Easy,0,wx.ALIGN_CENTER|wx.ALL,2)
        Medium=wx.CheckBox(OpeningList,-1,u'中等',style=wx.ALIGN_RIGHT)
        Medium.SetValue(boolchange(OpeningDic[self.tree.GetItemText(treeItem)][self.Openings.GetStringSelection()][2]))
        box.Add(Medium,0,wx.ALIGN_CENTER|wx.ALL,2)
        Hard=wx.CheckBox(OpeningList,-1,u'困难',style=wx.ALIGN_RIGHT)
        Hard.SetValue(boolchange(OpeningDic[self.tree.GetItemText(treeItem)][self.Openings.GetStringSelection()][3]))
        box.Add(Hard,0,wx.ALIGN_CENTER|wx.ALL,2)
        Brutal=wx.CheckBox(OpeningList,-1,u'凶残',style=wx.ALIGN_RIGHT)
        Brutal.SetValue(boolchange(OpeningDic[self.tree.GetItemText(treeItem)][self.Openings.GetStringSelection()][4]))
        box.Add(Brutal,0,wx.ALIGN_CENTER|wx.ALL,2)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,2)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(OpeningList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(OpeningList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        OpeningList.SetSizer(sizer)
        OpeningList.Fit()

        
        if OpeningList.ShowModal()==wx.ID_OK:
            if self.ChoiceOpen.GetStringSelection()=='':
                OpeningList.Destroy()
                return
            if self.Openings.FindString(self.ChoiceOpen.GetStringSelection())!=-1 and self.ChoiceOpen.GetStringSelection()!=self.Openings.GetStringSelection():
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                OpeningList.Destroy()
                return
            PerValue[self.tree.GetItemText(treeItem)][7]=PerValue[self.tree.GetItemText(treeItem)][7].replace(self.Openings.GetStringSelection(),self.ChoiceOpen.GetStringSelection())

            OpeningItem=OpeningDic[self.tree.GetItemText(treeItem)]
            del OpeningItem[self.Openings.GetStringSelection()]
            OpeningItem[self.ChoiceOpen.GetStringSelection()]=[]
            DifficultList=OpeningItem[self.ChoiceOpen.GetStringSelection()]
            DifficultList.append(str(spin.GetValue()))
            DifficultList.append(str(Easy.GetValue()))
            DifficultList.append(str(Medium.GetValue()))
            DifficultList.append(str(Hard.GetValue()))
            DifficultList.append(str(Brutal.GetValue()))
            
            self.Openings.SetString(self.Openings.GetSelection(),self.ChoiceOpen.GetStringSelection())
        OpeningList.Destroy()

    def OnDelOpen(self,event):
        treeItem=self.tree.GetSelection()

        PerValue[self.tree.GetItemText(treeItem)][7]=PerValue[self.tree.GetItemText(treeItem)][7].rstrip(self.Openings.GetStringSelection())
        if PerValue[self.tree.GetItemText(treeItem)][7].endswith(','):
            PerValue[self.tree.GetItemText(treeItem)][7]=PerValue[self.tree.GetItemText(treeItem)][7].rstrip(',')
        del OpeningDic[self.tree.GetItemText(treeItem)][self.Openings.GetStringSelection()]
        self.DelOpen.Enable(False)
        self.EditOpen.Enable(False)
        self.Openings.Delete(self.Openings.GetSelection())

    def OnStra(self,event):
        if self.stra.GetStringSelection()=='':
            self.DelStra.Enable(False)
            self.EditStra.Enable(False)
        else:
            self.DelStra.Enable(True)
            self.EditStra.Enable(True)

    def OnNewStra(self,event):
        StraList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(StraList,-1,u'选择一个进攻策略')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceStra=wx.ListBox(StraList,-1,size=(250,350),choices=NewStra)
        sizer.Add(self.ChoiceStra,0,wx.ALIGN_CENTER|wx.ALL,5)

        label=wx.StaticText(StraList,-1,u'何种难度使用')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        Easy=wx.CheckBox(StraList,-1,u'简单',style=wx.ALIGN_RIGHT)
        Easy.SetValue(True)
        box.Add(Easy,0,wx.ALIGN_CENTER|wx.ALL,2)
        Medium=wx.CheckBox(StraList,-1,u'中等',style=wx.ALIGN_RIGHT)
        Medium.SetValue(True)
        box.Add(Medium,0,wx.ALIGN_CENTER|wx.ALL,2)
        Hard=wx.CheckBox(StraList,-1,u'困难',style=wx.ALIGN_RIGHT)
        Hard.SetValue(True)
        box.Add(Hard,0,wx.ALIGN_CENTER|wx.ALL,2)
        Brutal=wx.CheckBox(StraList,-1,u'凶残',style=wx.ALIGN_RIGHT)
        Brutal.SetValue(True)
        box.Add(Brutal,0,wx.ALIGN_CENTER|wx.ALL,2)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,2)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(StraList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(StraList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        StraList.SetSizer(sizer)
        StraList.Fit()

        treeItem=self.tree.GetSelection()
        if StraList.ShowModal()==wx.ID_OK:
            if self.ChoiceStra.GetStringSelection()=='':
                StraList.Destroy()
                return
            if self.stra.FindString(self.ChoiceStra.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                StraList.Destroy()
                return
            self.stra.Append(self.ChoiceStra.GetStringSelection())
            if PerValue[self.tree.GetItemText(treeItem)][8]=='':
                PerValue[self.tree.GetItemText(treeItem)][8]+=self.ChoiceStra.GetStringSelection()
            else:
                PerValue[self.tree.GetItemText(treeItem)][8]+=','+self.ChoiceStra.GetStringSelection()
            StraItem=StraDic[self.tree.GetItemText(treeItem)]
            StraItem[self.ChoiceStra.GetStringSelection()]=[]
            DifficultList=StraItem[self.ChoiceStra.GetStringSelection()]
            DifficultList.append(str(Easy.GetValue()))
            DifficultList.append(str(Medium.GetValue()))
            DifficultList.append(str(Hard.GetValue()))
            DifficultList.append(str(Brutal.GetValue()))
        StraList.Destroy()

    def OnEditStra(self,event):
        treeItem=self.tree.GetSelection()
        
        StraList=wx.Dialog(None,-1,u'编辑')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(StraList,-1,u'选择一个进攻策略')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceStra=wx.ListBox(StraList,-1,size=(250,350),choices=NewStra)
        self.ChoiceStra.SetStringSelection(self.stra.GetStringSelection())
        sizer.Add(self.ChoiceStra,0,wx.ALIGN_CENTER|wx.ALL,5)

        label=wx.StaticText(StraList,-1,u'何种难度使用')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        Easy=wx.CheckBox(StraList,-1,u'简单',style=wx.ALIGN_RIGHT)
        Easy.SetValue(boolchange(StraDic[self.tree.GetItemText(treeItem)][self.stra.GetStringSelection()][0]))
        box.Add(Easy,0,wx.ALIGN_CENTER|wx.ALL,2)
        Medium=wx.CheckBox(StraList,-1,u'中等',style=wx.ALIGN_RIGHT)
        Medium.SetValue(boolchange(StraDic[self.tree.GetItemText(treeItem)][self.stra.GetStringSelection()][1]))
        box.Add(Medium,0,wx.ALIGN_CENTER|wx.ALL,2)
        Hard=wx.CheckBox(StraList,-1,u'困难',style=wx.ALIGN_RIGHT)
        Hard.SetValue(boolchange(StraDic[self.tree.GetItemText(treeItem)][self.stra.GetStringSelection()][2]))
        box.Add(Hard,0,wx.ALIGN_CENTER|wx.ALL,2)
        Brutal=wx.CheckBox(StraList,-1,u'凶残',style=wx.ALIGN_RIGHT)
        Brutal.SetValue(boolchange(StraDic[self.tree.GetItemText(treeItem)][self.stra.GetStringSelection()][3]))
        box.Add(Brutal,0,wx.ALIGN_CENTER|wx.ALL,2)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,2)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(StraList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(StraList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        StraList.SetSizer(sizer)
        StraList.Fit()

        if StraList.ShowModal()==wx.ID_OK:
            if self.ChoiceStra.GetStringSelection()=='':
                StraList.Destroy()
                return
            if self.stra.FindString(self.ChoiceStra.GetStringSelection())!=-1 and self.ChoiceStra.GetStringSelection()!=self.stra.GetStringSelection():
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                StraList.Destroy()
                return
            
            PerValue[self.tree.GetItemText(treeItem)][8]=PerValue[self.tree.GetItemText(treeItem)][8].replace(self.stra.GetStringSelection(),self.ChoiceStra.GetStringSelection())
            
            
            StraItem=StraDic[self.tree.GetItemText(treeItem)]
            del StraItem[self.stra.GetStringSelection()]
            StraItem[self.ChoiceStra.GetStringSelection()]=[]
            DifficultList=StraItem[self.ChoiceStra.GetStringSelection()]
            DifficultList.append(str(Easy.GetValue()))
            DifficultList.append(str(Medium.GetValue()))
            DifficultList.append(str(Hard.GetValue()))
            DifficultList.append(str(Brutal.GetValue()))

            self.stra.SetString(self.stra.GetSelection(),self.ChoiceStra.GetStringSelection())
        StraList.Destroy()

    def OnDelStra(self,event):
        treeItem=self.tree.GetSelection()

        PerValue[self.tree.GetItemText(treeItem)][8]=PerValue[self.tree.GetItemText(treeItem)][8].rstrip(self.stra.GetStringSelection())
        if PerValue[self.tree.GetItemText(treeItem)][8].endswith(','):
            PerValue[self.tree.GetItemText(treeItem)][8]=PerValue[self.tree.GetItemText(treeItem)][8].rstrip(',')
        del StraDic[self.tree.GetItemText(treeItem)][self.stra.GetStringSelection()]
        self.DelStra.Enable(False)
        self.stra.Delete(self.stra.GetSelection())

    def OnBuild(self,event):
        if self.build.GetStringSelection()=='':
            self.DelBuild.Enable(False)
            self.EditBuild.Enable(False)
        else:
            self.DelBuild.Enable(True)
            self.EditBuild.Enable(True)

    def OnNewBuild(self,event):
        BuildList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(BuildList,-1,u'选择一个建造策略')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceBuild=wx.ListBox(BuildList,-1,size=(250,350),choices=NewBuild)
        sizer.Add(self.ChoiceBuild,0,wx.ALIGN_CENTER|wx.ALL,5)

        label=wx.StaticText(BuildList,-1,u'何种难度使用')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        Easy=wx.CheckBox(BuildList,-1,u'简单',style=wx.ALIGN_RIGHT)
        Easy.SetValue(True)
        box.Add(Easy,0,wx.ALIGN_CENTER|wx.ALL,2)
        Medium=wx.CheckBox(BuildList,-1,u'中等',style=wx.ALIGN_RIGHT)
        Medium.SetValue(True)
        box.Add(Medium,0,wx.ALIGN_CENTER|wx.ALL,2)
        Hard=wx.CheckBox(BuildList,-1,u'困难',style=wx.ALIGN_RIGHT)
        Hard.SetValue(True)
        box.Add(Hard,0,wx.ALIGN_CENTER|wx.ALL,2)
        Brutal=wx.CheckBox(BuildList,-1,u'凶残',style=wx.ALIGN_RIGHT)
        Brutal.SetValue(True)
        box.Add(Brutal,0,wx.ALIGN_CENTER|wx.ALL,2)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,2)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(BuildList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(BuildList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        BuildList.SetSizer(sizer)
        BuildList.Fit()

        treeItem=self.tree.GetSelection()
        if BuildList.ShowModal()==wx.ID_OK:
            if self.ChoiceBuild.GetStringSelection()=='':
                BuildList.Destroy()
                return
            if self.build.FindString(self.ChoiceBuild.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                BuildList.Destroy()
                return
            self.build.Append(self.ChoiceBuild.GetStringSelection())
            if PerValue[self.tree.GetItemText(treeItem)][9]=='':
                PerValue[self.tree.GetItemText(treeItem)][9]+=self.ChoiceBuild.GetStringSelection()
            else:
                PerValue[self.tree.GetItemText(treeItem)][9]+=','+self.ChoiceBuild.GetStringSelection()
            BuildItem=BuildDic[self.tree.GetItemText(treeItem)]
            BuildItem[self.ChoiceBuild.GetStringSelection()]=[]
            DifficultList=BuildItem[self.ChoiceBuild.GetStringSelection()]
            DifficultList.append(str(Easy.GetValue()))
            DifficultList.append(str(Medium.GetValue()))
            DifficultList.append(str(Hard.GetValue()))
            DifficultList.append(str(Brutal.GetValue()))
        BuildList.Destroy()

    def OnEditBuild(self,event):
        treeItem=self.tree.GetSelection()
        
        BuildList=wx.Dialog(None,-1,u'编辑')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(BuildList,-1,u'选择一个建造策略')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceBuild=wx.ListBox(BuildList,-1,size=(250,350),choices=NewBuild)
        self.ChoiceBuild.SetStringSelection(self.build.GetStringSelection())
        sizer.Add(self.ChoiceBuild,0,wx.ALIGN_CENTER|wx.ALL,5)

        label=wx.StaticText(BuildList,-1,u'何种难度使用')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        Easy=wx.CheckBox(BuildList,-1,u'简单',style=wx.ALIGN_RIGHT)
        Easy.SetValue(boolchange(BuildDic[self.tree.GetItemText(treeItem)][self.build.GetStringSelection()][0]))
        box.Add(Easy,0,wx.ALIGN_CENTER|wx.ALL,2)
        Medium=wx.CheckBox(BuildList,-1,u'中等',style=wx.ALIGN_RIGHT)
        Medium.SetValue(boolchange(BuildDic[self.tree.GetItemText(treeItem)][self.build.GetStringSelection()][1]))
        box.Add(Medium,0,wx.ALIGN_CENTER|wx.ALL,2)
        Hard=wx.CheckBox(BuildList,-1,u'困难',style=wx.ALIGN_RIGHT)
        Hard.SetValue(boolchange(BuildDic[self.tree.GetItemText(treeItem)][self.build.GetStringSelection()][2]))
        box.Add(Hard,0,wx.ALIGN_CENTER|wx.ALL,2)
        Brutal=wx.CheckBox(BuildList,-1,u'凶残',style=wx.ALIGN_RIGHT)
        Brutal.SetValue(boolchange(BuildDic[self.tree.GetItemText(treeItem)][self.build.GetStringSelection()][3]))
        box.Add(Brutal,0,wx.ALIGN_CENTER|wx.ALL,2)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,2)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(BuildList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(BuildList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        BuildList.SetSizer(sizer)
        BuildList.Fit()

        if BuildList.ShowModal()==wx.ID_OK:
            if self.ChoiceBuild.GetStringSelection()=='':
                BuildList.Destroy()
                return
            if self.build.FindString(self.ChoiceBuild.GetStringSelection())!=-1 and self.ChoiceBuild.GetStringSelection()!=self.build.GetStringSelection():
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                BuildList.Destroy()
                return
            
            PerValue[self.tree.GetItemText(treeItem)][9]=PerValue[self.tree.GetItemText(treeItem)][9].replace(self.build.GetStringSelection(),self.ChoiceBuild.GetStringSelection())
            
            BuildItem=BuildDic[self.tree.GetItemText(treeItem)]
            del BuildItem[self.build.GetStringSelection()]
            BuildItem[self.ChoiceBuild.GetStringSelection()]=[]
            DifficultList=BuildItem[self.ChoiceBuild.GetStringSelection()]
            DifficultList.append(str(Easy.GetValue()))
            DifficultList.append(str(Medium.GetValue()))
            DifficultList.append(str(Hard.GetValue()))
            DifficultList.append(str(Brutal.GetValue()))

            self.build.SetString(self.build.GetSelection(),self.ChoiceBuild.GetStringSelection())
        BuildList.Destroy()

    def OnDelBuild(self,event):
        treeItem=self.tree.GetSelection()

        PerValue[self.tree.GetItemText(treeItem)][9]=PerValue[self.tree.GetItemText(treeItem)][9].rstrip(self.build.GetStringSelection())
        if PerValue[self.tree.GetItemText(treeItem)][9].endswith(','):
            PerValue[self.tree.GetItemText(treeItem)][9]=PerValue[self.tree.GetItemText(treeItem)][9].rstrip(',')
        del BuildDic[self.tree.GetItemText(treeItem)][self.build.GetStringSelection()]
        self.DelBuild.Enable(False)
        self.EditBuild.Enable(False)
        self.build.Delete(self.build.GetSelection())

    def OnPrefer(self,event):
        if self.prefer.GetStringSelection()=='':
            self.DelPrefer.Enable(False)
        else:
            self.DelPrefer.Enable(True)

    def OnNewPrefer(self,event):
        PreferList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(PreferList,-1,u'选择一个单位')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        conn=sqlite3.connect('UnitList.db')
        cur=conn.cursor()
        cur.execute("select * from Unitname")
        res=cur.fetchall()
        namelist=[]
        for name in res:
            namelist.append(name[0])

        self.ChoicePrefer=wx.ListBox(PreferList,-1,size=(250,350),choices=namelist)
        sizer.Add(self.ChoicePrefer,0,wx.ALIGN_CENTER|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(PreferList,-1,u'进攻指数  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin1=wx.SpinCtrlDouble(PreferList,value='2.00',min=0.50,max=5.00,inc=0.25)
        spin1.SetDigits(2)
        box.Add(spin1,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(PreferList,-1,u'防御指数  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin2=wx.SpinCtrlDouble(PreferList,value='2.00',min=0.50,max=5.00,inc=0.25)
        spin2.SetDigits(2)
        box.Add(spin2,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.StaticBox(PreferList,-1,'')
        bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

        label=wx.StaticText(PreferList,-1,u'这里的单位和数值似乎对AI\n影响不大,进攻指数和防御指数\n一般是相等的')
        label.SetForegroundColour('DIM GREY')
        bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
        sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(PreferList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(PreferList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        PreferList.SetSizer(sizer)
        PreferList.Fit()

        treeItem=self.tree.GetSelection()
        if PreferList.ShowModal()==wx.ID_OK:
            if self.ChoicePrefer.GetStringSelection()=='':
                PreferList.Destroy()
                return
            if self.prefer.FindString(self.ChoicePrefer.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                PreferList.Destroy()
                return
            self.prefer.Append(self.ChoicePrefer.GetStringSelection())
            if PerValue[self.tree.GetItemText(treeItem)][10]=='':
                PerValue[self.tree.GetItemText(treeItem)][10]+=self.ChoicePrefer.GetStringSelection()
            else:
                PerValue[self.tree.GetItemText(treeItem)][10]+=','+self.ChoicePrefer.GetStringSelection()
            PreferItem=PreferDic[self.tree.GetItemText(treeItem)]
            cur.execute("select * from Unitname WHERE name=(?)",(self.ChoicePrefer.GetStringSelection(),))
            name=cur.fetchall()[0][1]
            PreferItem[name]=[]
            Acount=PreferItem[name]
            Acount.append(str(spin1.GetValue()))
            Acount.append(str(spin2.GetValue()))
        cur.close()
        conn.close()
        PreferList.Destroy()

    def OnDelPrefer(self,event):
        treeItem=self.tree.GetSelection()

        PerValue[self.tree.GetItemText(treeItem)][10]=PerValue[self.tree.GetItemText(treeItem)][10].rstrip(self.prefer.GetStringSelection())
        if PerValue[self.tree.GetItemText(treeItem)][10].endswith(','):
            PerValue[self.tree.GetItemText(treeItem)][10]=PerValue[self.tree.GetItemText(treeItem)][10].rstrip(',')
        conn=sqlite3.connect('UnitList.db')
        cur=conn.cursor()
        cur.execute("select * from Unitname WHERE name=(?)",(self.prefer.GetStringSelection(),))
        name=cur.fetchall()[0][1]
        del PreferDic[self.tree.GetItemText(treeItem)][name]
        cur.close()
        conn.close()
        self.DelPrefer.Enable(False)
        self.prefer.Delete(self.prefer.GetSelection())

    def OnPower(self,event):
        if self.power.GetStringSelection()=='':
            self.DelPower.Enable(False)
        else:
            self.DelPower.Enable(True)

    def OnNewPower(self,event):
        PowerList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(PowerList,-1,u'选择一个协议')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoicePower=wx.ListBox(PowerList,-1,size=(250,350),choices=SpecialPowerkeys)
        sizer.Add(self.ChoicePower,0,wx.ALIGN_CENTER|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(PowerList,-1,u'权重  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin=wx.SpinCtrl(PowerList,-1,'')
        spin.SetRange(100,500)
        spin.SetValue(200)
        box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.StaticBox(PowerList,-1,'')
        bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

        label=wx.StaticText(PowerList,-1,u'这里的调节似乎不太\n有用,我也没有研究透')
        label.SetForegroundColour('DIM GREY')
        bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
        sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(PowerList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(PowerList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        PowerList.SetSizer(sizer)
        PowerList.Fit()

        treeItem=self.tree.GetSelection()
        if PowerList.ShowModal()==wx.ID_OK:
            if self.ChoicePower.GetStringSelection()=='':
                PowerList.Destroy()
                return
            if self.power.FindString(self.ChoicePower.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                PowerList.Destroy()
                return
            self.power.Append(self.ChoicePower.GetStringSelection())
            if PerValue[self.tree.GetItemText(treeItem)][11]=='':
                PerValue[self.tree.GetItemText(treeItem)][11]+=self.ChoicePower.GetStringSelection()
            else:
                PerValue[self.tree.GetItemText(treeItem)][11]+=','+self.ChoicePower.GetStringSelection()
            PowerItem=PowerDic[self.tree.GetItemText(treeItem)]
            PowerItem[SpecialPower[self.ChoicePower.GetStringSelection()]]=str(spin.GetValue())
        PowerList.Destroy()

    def OnDelPower(self,event):
        treeItem=self.tree.GetSelection()

        PerValue[self.tree.GetItemText(treeItem)][11]=PerValue[self.tree.GetItemText(treeItem)][11].rstrip(self.power.GetStringSelection())
        if PerValue[self.tree.GetItemText(treeItem)][11].endswith(','):
            PerValue[self.tree.GetItemText(treeItem)][11]=PerValue[self.tree.GetItemText(treeItem)][11].rstrip(',')
        del PowerDic[self.tree.GetItemText(treeItem)][SpecialPower[self.power.GetStringSelection()]]
        self.DelPower.Enable(False)
        self.power.Delete(self.power.GetSelection())

    def OnCap(self,event):
        if self.cap.GetStringSelection()=='':
            self.DelCap.Enable(False)
        else:
            self.DelCap.Enable(True)

    def OnNewCap(self,event):
        CapList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(CapList,-1,u'选择一个单位')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        conn=sqlite3.connect('UnitList.db')
        cur=conn.cursor()
        cur.execute("select * from Unitname")
        res=cur.fetchall()
        namelist=[]
        for name in res:
            namelist.append(name[0])

        self.ChoiceCap=wx.ListBox(CapList,-1,size=(250,350),choices=namelist)
        sizer.Add(self.ChoiceCap,0,wx.ALIGN_CENTER|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(CapList,-1,u'最大数目  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin=wx.SpinCtrl(CapList,-1,'')
        spin.SetRange(0,100)
        spin.SetValue(10)
        box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.StaticBox(CapList,-1,'')
        bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

        label=wx.StaticText(CapList,-1,u'这里的最大数目不是绝对\n有用的,AI钱足够多的情况下,\n仍然会超过这个数目')
        label.SetForegroundColour('DIM GREY')
        bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
        sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(CapList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(CapList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        CapList.SetSizer(sizer)
        CapList.Fit()

        treeItem=self.tree.GetSelection()
        if CapList.ShowModal()==wx.ID_OK:
            if self.ChoiceCap.GetStringSelection()=='':
                CapList.Destroy()
                return
            if self.cap.FindString(self.ChoiceCap.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此项目',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                CapList.Destroy()
                return
            self.cap.Append(self.ChoiceCap.GetStringSelection())
            if PerValue[self.tree.GetItemText(treeItem)][12]=='':
                PerValue[self.tree.GetItemText(treeItem)][12]+=self.ChoiceCap.GetStringSelection()
            else:
                PerValue[self.tree.GetItemText(treeItem)][12]+=','+self.ChoiceCap.GetStringSelection()
            CapItem=CapDic[self.tree.GetItemText(treeItem)]
            cur.execute("select * from Unitname WHERE name=(?)",(self.ChoiceCap.GetStringSelection(),))
            name=cur.fetchall()[0][1]
            CapItem[name]=str(spin.GetValue())
        CapList.Destroy()

    def OnDelCap(self,event):
        treeItem=self.tree.GetSelection()

        PerValue[self.tree.GetItemText(treeItem)][12]=PerValue[self.tree.GetItemText(treeItem)][12].rstrip(self.cap.GetStringSelection())
        if PerValue[self.tree.GetItemText(treeItem)][12].endswith(','):
            PerValue[self.tree.GetItemText(treeItem)][12]=PerValue[self.tree.GetItemText(treeItem)][12].rstrip(',')
        conn=sqlite3.connect('UnitList.db')
        cur=conn.cursor()
        cur.execute("select * from Unitname WHERE name=(?)",(self.cap.GetStringSelection(),))
        name=cur.fetchall()[0][1]
        del CapDic[self.tree.GetItemText(treeItem)][name]
        cur.close()
        conn.close()
        self.DelCap.Enable(False)
        self.cap.Delete(self.cap.GetSelection())

    def OnTarget(self,event):
        if self.target.GetStringSelection()=='':
            self.DelTarget.Enable(False)
        else:
            self.DelTarget.Enable(True)

    def OnAddTarget(self,event):
        TargetList=wx.Dialog(None,-1,u'添加')
        sizer=wx.BoxSizer(wx.VERTICAL)

        label=wx.StaticText(TargetList,-1,u'选择目标')
        sizer.Add(label,0,wx.ALIGN_LEFT|wx.ALL,3)

        self.ChoiceTarget=wx.ListBox(TargetList,-1,size=(250,350),choices=Target)
        sizer.Add(self.ChoiceTarget,0,wx.ALIGN_CENTER|wx.ALL,5)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(TargetList,-1,u'优先权  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin=wx.SpinCtrl(TargetList,-1,'')
        spin.SetRange(10,100)
        spin.SetValue(10)
        box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.StaticBox(TargetList,-1,'')
        bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

        label=wx.StaticText(TargetList,-1,u'这里的目标描述了一类单位或建筑,\n把单词拆开就能大致看懂意思,\n目标并不意味着就是被攻击的,\n若描述的目标为友军单位,则会\n去靠近或保护这些单位')
        label.SetForegroundColour('DIM GREY')
        bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
        sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(TargetList,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(TargetList,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        TargetList.SetSizer(sizer)
        TargetList.Fit()

        treeItem=self.tree.GetSelection()
        if TargetList.ShowModal()==wx.ID_OK:
            if self.ChoiceTarget.GetStringSelection()=='':
                TargetList.Destroy()
                return
            if self.target.FindString(self.ChoiceTarget.GetStringSelection())!=-1:
                warning=wx.MessageDialog(None,u'已存在此目标',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                TargetList.Destroy()
                return
            self.target.Append(self.ChoiceTarget.GetStringSelection())
            if AttackValue[self.tree.GetItemText(treeItem)][4]=='':
                AttackValue[self.tree.GetItemText(treeItem)][4]+=self.ChoiceTarget.GetStringSelection()
            else:
                AttackValue[self.tree.GetItemText(treeItem)][4]+=','+self.ChoiceTarget.GetStringSelection()
            TargetItem=TargetDic[self.tree.GetItemText(treeItem)]
            TargetItem[self.ChoiceTarget.GetStringSelection()]=str(spin.GetValue())
        TargetList.Destroy()

    def OnDelTarget(self,event):
        treeItem=self.tree.GetSelection()

        AttackValue[self.tree.GetItemText(treeItem)][4]=AttackValue[self.tree.GetItemText(treeItem)][4].rstrip(self.target.GetStringSelection())
        if AttackValue[self.tree.GetItemText(treeItem)][4].endswith(','):
            AttackValue[self.tree.GetItemText(treeItem)][4]=AttackValue[self.tree.GetItemText(treeItem)][4].rstrip(',')
        del TargetDic[self.tree.GetItemText(treeItem)][self.target.GetStringSelection()]
        if AddTarget.has_key(self.target.GetSelection()):
            del AddTarget[self.target.GetSelection()]
        self.DelTarget.Enable(False)
        self.target.Delete(self.target.GetSelection())

    def OnAddNewTarget(self,evnet):
        NewTargetDialog=wx.Dialog(None,-1,u'添加自定目标')
        sizer=wx.BoxSizer(wx.VERTICAL)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(NewTargetDialog,-1,u'目标名称')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        TargetID=wx.TextCtrl(NewTargetDialog,-1,size=(100,-1))
        box.Add(TargetID,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(NewTargetDialog,-1,u'物体名称')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        ObjectName=wx.TextCtrl(NewTargetDialog,-1,size=(100,-1))
        box.Add(ObjectName,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.BoxSizer(wx.HORIZONTAL)
        label=wx.StaticText(NewTargetDialog,-1,u'优先权  :')
        box.Add(label,0,wx.ALIGN_CENTER|wx.ALL,3)
        spin=wx.SpinCtrl(NewTargetDialog,-1,'')
        spin.SetRange(10,100)
        spin.SetValue(10)
        box.Add(spin,0,wx.ALIGN_CENTER|wx.ALL,3)
        sizer.Add(box,0,wx.ALIGN_CENTER|wx.ALL,3)

        box=wx.StaticBox(NewTargetDialog,-1,'')
        bsizer=wx.StaticBoxSizer(box,wx.VERTICAL)

        label=wx.StaticText(NewTargetDialog,-1,u'这里的新定义目标为地图上已命名\n物体的目标，物体名称即为已命名物体的\n名称')
        label.SetForegroundColour('DIM GREY')
        bsizer.Add(label,0,wx.TOP|wx.LEFT,6)
        sizer.Add(bsizer,0,wx.ALIGN_CENTER|wx.ALL,5)

        btnsizer=wx.StdDialogButtonSizer()
        btn=wx.Button(NewTargetDialog,wx.ID_OK,size=(-1,25))
        btnsizer.AddButton(btn)
        btn=wx.Button(NewTargetDialog,wx.ID_CANCEL,size=(-1,25))
        btnsizer.AddButton(btn)
        btnsizer.Realize()
        sizer.Add(btnsizer,0,wx.ALIGN_CENTER|wx.ALL,10)

        NewTargetDialog.SetSizer(sizer)
        NewTargetDialog.Fit()

        treeItem=self.tree.GetSelection()
        if NewTargetDialog.ShowModal()==wx.ID_OK:
            if TargetID.GetValue()=='' or ObjectName.GetValue()=='':
                warning=wx.MessageDialog(None,u'未填写完整',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                NewTargetDialog.Destroy()
                return
            if self.target.FindString(TargetID.GetValue())!=-1:
                warning=wx.MessageDialog(None,u'已存在此目标',u'警告',style=wx.OK)
                warning.ShowModal()
                warning.Destroy()
                NewTargetDialog.Destroy()
                return
            self.target.Append(TargetID.GetValue())
            if AttackValue[self.tree.GetItemText(treeItem)][4]=='':
                AttackValue[self.tree.GetItemText(treeItem)][4]+=TargetID.GetValue()
            else:
                AttackValue[self.tree.GetItemText(treeItem)][4]+=','+TargetID.GetValue()
            TargetItem=TargetDic[self.tree.GetItemText(treeItem)]
            TargetItem[TargetID.GetValue()]=str(spin.GetValue())

            AddTarget[TargetID.GetValue()]=ObjectName.GetValue()
        NewTargetDialog.Destroy()

    def OnClickTree(self,event):
        item=event.GetItem()
        treeText=self.tree.GetItemText(item)
        if treeText=='AI'or treeText==u'性格' or treeText==u'队伍策略' or treeText==u'开场行为' or treeText==u'建造策略':
            self.list.DeleteAllItems()
            return
        if self.tree.GetItemText(self.tree.GetItemParent(item))==u'性格':
            self.list.DeleteAllItems()
            for i in range(len(PerData)):
                self.list.InsertStringItem(i,PerData[i])
                self.list.SetStringItem(i,1,PerValue[treeText][i])

        if self.tree.GetItemText(self.tree.GetItemParent(item))==u'队伍策略':
            self.list.DeleteAllItems()
            for i in range(len(AttackData)):
                self.list.InsertStringItem(i,AttackData[i])
                self.list.SetStringItem(i,1,AttackValue[treeText][i])
            conn=sqlite3.connect('UnitList.db')
            cur=conn.cursor()
            triggerList=AttackValue[treeText][3].split(',')
            if triggerList!=['']:
                if triggerList[1]!=u'无':
                    cur.execute("select * from Unitname WHERE name1=(?)",(triggerList[1],))
                    res=cur.fetchall()
                    triggerList[1]=res[0][0]
                else:
                    del triggerList[1]
                if triggerList[2]!=u'无':
                    cur.execute("select * from Unitname WHERE name1=(?)",(triggerList[2],))
                    res=cur.fetchall()
                    triggerList[2]=res[0][0]
                else:
                    del triggerList[2]
                if triggerList[3]!=u'无':
                    cur.execute("select * from Unitname WHERE name1=(?)",(triggerList[3],))
                    res=cur.fetchall()
                    triggerList[3]=res[0][0]
                else:
                    del triggerList[3]
                self.list.SetStringItem(3,1,','.join(triggerList))

            creatUnitList=AttackValue[treeText][14].split(',')
            if creatUnitList!=['']:
                cur.execute("select * from Unitname WHERE name1=(?)",(creatUnitList[0],))
                res=cur.fetchall()
                creatUnitList[0]=res[0][0]
                self.list.SetStringItem(14,1,','.join(creatUnitList))
            

    def OnBeginEditTree(self,event):
        item=event.GetItem()
        treeText=self.tree.GetItemText(item)
        if treeText=='AI'or treeText==u'性格' or treeText==u'队伍策略' or treeText==u'开场行为' or treeText==u'建造策略':
            event.Veto()
        self.TreeTextEdit=event.GetLabel()

    def OnEndEditTree(self,event):
        if event.IsEditCancelled():
            return
        if self.tree.GetItemText(self.tree.GetItemParent(item))==u'性格':
            PerValue[event.GetLabel()]=PerValue[self.TreeTextEdit]
            OpeningDic[event.GetLabel()]=OpeningDic[self.TreeTextEdit]
            StraDic[event.GetLabel()]=StraDic[self.TreeTextEdit]
            BuildDic[event.GetLabel()]=BuildDic[self.TreeTextEdit]
            PreferDic[event.GetLabel()]=PreferDic[self.TreeTextEdit]
            PowerDic[event.GetLabel()]=PowerDic[self.TreeTextEdit]
            CapDic[event.GetLabel()]=CapDic[self.TreeTextEdit]

            del PerValue[self.TreeTextEdit]
            del OpeningDic[self.TreeTextEdit]
            del StraDic[self.TreeTextEdit]
            del BuildDic[self.TreeTextEdit]
            del PreferDic[self.TreeTextEdit]
            del PowerDic[self.TreeTextEdit]
            del CapDic[self.TreeTextEdit]

        if self.tree.GetItemText(self.tree.GetItemParent(item))==u'队伍策略':
            AttackValue[event.GetLabel()]=AttackValue[self.TreeTextEdit]
            TargetDic[event.GetLabel()]=TargetDic[self.TreeTextEdit]

            del AttackValue[self.TreeTextEdit]
            del TargetDic[self.TreeTextEdit]

if __name__=='__main__':
    app=wx.App()
    aiEdit=AIEdit()
    aiEdit.Show()
    app.MainLoop()
