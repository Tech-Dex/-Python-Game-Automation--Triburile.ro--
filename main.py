from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time


class Triburile_Login(): # Basic Login into your account
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def logIn(self):
        self.browser = webdriver.Firefox()
        self.browser.get("https://www.triburile.ro/")
        time.sleep(1)
        usernameToLog = self.browser.find_element_by_id('user')
        usernameToLog.send_keys(self.username)
        passwordToLog = self.browser.find_element_by_name('password')
        passwordToLog.send_keys(self.password)
        self.browser.find_element_by_class_name('btn-login').click()
        time.sleep(1)
        self.browser.find_element_by_class_name('world_button_active').click()
        self.browser.current_url

    def startPopUp(self):
        try:
            dailyQuestExist = self.browser.find_element_by_xpath('//*[@id="popup_box_daily_bonus"]')
            if dailyQuestExist != None:
                self.browser.find_element_by_class_name('btn-default').click()
                time.sleep(2)
                self.browser.find_element_by_class_name('popup_box_close').click()
        except Exception:
            pass

class Data_Village(Triburile_Login): # Get important data from your village
    def __init__(self, login_class ):
        self.browser = login_class.browser

    def getResourceInfo(self):
        self.wood = int(self.browser.find_element_by_id('wood').text)
        self.stone = int(self.browser.find_element_by_id('stone').text)
        self.iron = int(self.browser.find_element_by_id('iron').text)

        #production per hour
        #element css selector can be different from world to world. You can take CSS_Selector link from Insepct Element
        self.browser.find_element_by_class_name('visual-label-wood').click()
        self.woodPerHour = int (self.browser.find_element_by_css_selector('.vis > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > b:nth-child(1)').text)
        self.browser.find_element_by_class_name("village").click()

        self.moveTo = self.browser.find_element_by_class_name('visual-label-stone')
        self.browser.execute_script('arguments[0].scrollIntoView();',self.moveTo)
        self.browser.find_element_by_class_name('visual-label-stone').click()
        self.stonePerHour = int (self.browser.find_element_by_css_selector('.vis > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > b:nth-child(1)').text)
        self.browser.find_element_by_class_name("village").click()

        self.browser.find_element_by_class_name('visual-label-iron').click()
        self.ironPerHour = int (self.browser.find_element_by_css_selector('.vis > tbody:nth-child(1) > tr:nth-child(5) > td:nth-child(2) > b:nth-child(1)').text)
        self.browser.find_element_by_class_name("village").click()

        print ('Current wood ' + str(self.wood))
        print ('Current stone ' + str(self.stone))
        print ('Current iron ' + str(self.iron))

        print ('Wood per hour ' + str(self.woodPerHour))
        print ('Stone per hour ' + str(self.stonePerHour))
        print ('Iron per hour ' + str(self.ironPerHour))

    def getGeneralInfo(self):
        self.currentPopulation = int(self.browser.find_element_by_id('pop_current_label').text)
        self.maxPopulation = int(self.browser.find_element_by_id('pop_max_label').text)
        self.maxStorage = int(self.browser.find_element_by_id('storage').text)
        print ('Current population ' + str(self.currentPopulation))
        print ('Max population ' + str(self.maxPopulation))
        print ('Storage Capacity ' + str(self.maxStorage))

class Village_Quest(Data_Village):
    def __init__(self, data_class ):
        self.browser = data_class.browser
        self.wood = data_class.wood
        self.stone = data_class.stone
        self.iron = data_class.iron
        self.woodPerHour = data_class.woodPerHour
        self.stonePerHour = data_class.stonePerHour
        self.ironPerHour = data_class.ironPerHour
        self.currentPopulation = data_class.currentPopulation
        self.maxPopulation = data_class.maxPopulation
        self.maxStorage = data_class.maxStorage

    def questPrioritize(self): #He is trying to prioritize quest for getting rewards
        self.browser.find_element_by_class_name('visual-label-main').click()
        questBot.popUp_Event()
        try:
            find_quest = self.browser.find_element_by_class_name('current-quest')
            while find_quest != None:
                find_quest.click()
                time.sleep(2)
                find_quest = self.browser.find_element_by_class_name('current-quest')
        except Exception:
            print ("No current Quest running")
            self.browser.find_element_by_class_name("village").click()
            pass

    def popUp_Event(self): #closing popUp dialoge box
        try:
            popup = self.browser.find_element_by_id('popup_box_quest')
            if popup != None:
                self.browser.find_element_by_class_name('btn').click()
        except Exception:
            pass

    def noSpaceDep(self): # When you have to take a reward from quest but not enough space
        self.browser.find_element_by_class_name('visual-label-main').click()
        self.request_wood = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(2)').text)
        self.request_stone = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(3)').text)
        self.request_iron = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(4)').text)
        self.timeToFinish = self.browser.find_element_by_css_selector("#main_buildrow_storage > td:nth-child(5)").text
        self.timeToWaitInSeconds = sum( x * int(t) for x, t in zip([3600, 60, 1], self.timeToFinish.split(':')))

        print (self.request_wood)
        print (self.request_stone)
        print (self.request_iron)
        if self.request_wood <= self.wood and self.request_stone <= self.stone and self.request_iron <= self.iron:
                print ("Storage Upgraded... we need space for storing")
                self.level = self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(1) > span:nth-child(4)').text
                self.level_nr = int(self.level[-1:]) + 1
                self.moveTo = self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(1) > span:nth-child(4)')
                self.browser.execute_script('arguments[0].scrollIntoView();',self.moveTo)
                self.browser.find_element_by_css_selector('#main_buildlink_storage_' + str(self.level_nr) ).click()
                print ('Time until finish in seconds: ' + str(self.timeToWaitInSeconds) )
                time.sleep(self.timeToWaitInSeconds + 2)
                print ('Finished, go to village')
                self.moveTo = self.browser.find_element_by_class_name("village")
                self.browser.execute_script('arguments[0].scrollIntoView();',self.moveTo)
                self.moveTo.click();
                questBot.questFinished()

    def questFinished(self): # Checking Dialog Box Quest for taking reward
        try:
            self.browser.find_element_by_class_name('finished').click()
            time.sleep(2)
            try:
                warn = self.browser.find_element_by_class_name('warn')
                print ("Warning Not Enough Capacity")
                self.browser.find_element_by_class_name('popup_box_close').click()
                questBot.noSpaceDep()
            except Exception:
                print ("Quest Finished")
                self.browser.find_element_by_css_selector('.btn-confirm-yes').click()
                time.sleep(2)

        except Exception:
            pass

class Resource_Upgrade(Data_Village):
    def __init__(self, data_class ):
        self.browser = data_class.browser
        self.wood = data_class.wood
        self.stone = data_class.stone
        self.iron = data_class.iron
        self.woodPerHour = data_class.woodPerHour
        self.stonePerHour = data_class.stonePerHour
        self.ironPerHour = data_class.ironPerHour
        self.currentPopulation = data_class.currentPopulation
        self.maxPopulation = data_class.maxPopulation
        self.maxStorage = data_class.maxStorage

    def upgradeFarm(self):
        self.currentLevelFarm = self.browser.find_element_by_css_selector('#main_buildrow_farm > td:nth-child(1) > span:nth-child(4)').text
        self.levelFarm = int(self.currentLevelFarm[-1:]) + 1
        #activate execute_script when wood is out of window ( when u have more building it happens )
        self.browser.execute_script('arguments[0].scrollIntoView();',self.buttonUpgradeFarm)

        self.woodForFarm = int(self.browser.find_element_by_css_selector('#main_buildrow_farm > td:nth-child(2)').text)
        self.stoneForFarm = int(self.browser.find_element_by_css_selector('#main_buildrow_farm > td:nth-child(3)').text)
        self.ironForFarm =int(self.browser.find_element_by_css_selector('#main_buildrow_farm > td:nth-child(4)').text)
        self.upgradeFarmTimeText =self.browser.find_element_by_css_selector('#main_buildrow_farm > td:nth-child(2)').text
        self.upgradeFarmTimeSeconds = sum( x * int(t) for x, t in zip([3600, 60, 1], self.upgradeFarmTimeText.split(':')))

        if max(self.woodForFarm, self.stoneForFarm, self.ironForFarm) > self.maxStorage:
            resourceUpgradeBot.upgradeStorage()
        else:
            if self.woodForFarm <= self.wood and self.stoneForFarm <= self.stone and self.ironForFarm <= self.iron:
                self.buttonUpgradeFarm = self.browser.find_element_by_css_selector('#main_buildlink_farm' + str(self.levelFarm))
                self.buttonUpgradeFarm.click()
            else:
                self.needWoodFarm = self.woodForFarm - self.wood
                self.needIronFarm = self.stoneForFarm - self.iron
                self.needStoneFarm = self.ironForFarm - self.stone

                #Hour conversion
                self.timeForWood = (self.needWoodFarm/self.woodPerHour) * 3600 + 60
                self.timeForIron = (self.needIronFarm/self.ironPerHour) * 3600 + 60
                self.timeForStone = (self.needStoneFarm/self.stonePerHour) * 3600 + 60

                self.waitTime = max( self.timeForWood, self.timeForIron, self.timeForStone )
                print ("Time to get all resource that you need:" + str(self.waitTime) )
                time.sleep(self.waitTime + 2)
                self.browser.get(self.browser.getCurrentUrl())
                self.buttonUpgradeFarm = self.browser.find_element_by_css_selector('#main_buildlink_farm' + str(self.levelFarm))
                self.buttonUpgradeStorage.click()

            print ("Time Until Upgrade is ready: " + str(self.upgradeFarmTimeSeconds) )
            time.sleep(self.upgradeFarmTimeSeconds + 2)

    def upgradeStorage(self):
        self.currentLevelStorage = self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(1) > span:nth-child(4)').text
        self.levelStorage = int(self.currentLevelStorage[-1:]) + 1

        #activate execute_script when wood is out of window ( when u have more building it happens )
        self.browser.execute_script('arguments[0].scrollIntoView();',self.buttonUpgradeStorage)

        self.woodForStorage = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(2)').text)
        self.stoneForStorage = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(3)').text)
        self.ironForStorage = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(4)').text)
        self.upgradeStorageTimeText = self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(5)').text
        self.costPopulationStorage = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(6)').text)
        self.upgradeStorageTimeSeconds = sum( x * int(t) for x, t in zip([3600, 60, 1], self.upgradeStorageTimeText.split(':')))
        if self.costPopulationStorage > self.maxPopulation - self.currentPopulation:
            resourceUpgradeBot.upgradeFarm()
        else:
            if self.woodForStorage <= self.wood and self.stoneForStorage <= self.stone and self.ironForStorage <= self.iron:
                self.buttonUpgradeStorage = self.browser.find_element_by_css_selector("#main_buildlink_storage_" + str(self.levelStorage) )
                self.buttonUpgradeStorage.click()
            else:
                self.needWoodStorage = self.woodForStorage - self.wood
                self.needIronStorage = self.stoneForStorage - self.iron
                self.needStoneStorage = self.ironForStorage - self.stone

                #Hour conversion
                self.timeForWood = (self.needWoodStorage/self.woodPerHour) * 3600 + 60
                self.timeForIron = (self.needIronStorage/self.ironPerHour) * 3600 + 60
                self.timeForStone = (self.needStoneStorage/self.stonePerHour) * 3600 + 60

                self.waitTime = max( self.timeForWood, self.timeForIron, self.timeForStone )
                print ("Time to get all resource that you need:" + str(self.waitTime) )
                time.sleep(self.waitTime + 2)
                self.browser.get(self.browser.getCurrentUrl())
                self.buttonUpgradeStorage = self.browser.find_element_by_css_selector("#main_buildlink_storage_" + str(self.levelStorage) )
                self.buttonUpgradeStorage.click()

            print ("Time Until Upgrade is ready: " + str(self.upgradeStorageTimeSeconds) )
            time.sleep(self.upgradeStorageTimeSeconds + 2)

    def upgradeWood(self, levelWood):

        #activate execute_script when wood is out of window ( when u have more building it happens )

        #self.browser.execute_script('arguments[0].scrollIntoView();',self.buttonUpgrade)
        self.costWood = int(self.browser.find_element_by_css_selector('#main_buildrow_wood > td:nth-child(2)').text)
        self.costStone = int(self.browser.find_element_by_css_selector('#main_buildrow_wood > td:nth-child(3)').text)
        self.costIron = int(self.browser.find_element_by_css_selector('#main_buildrow_wood > td:nth-child(4)').text)
        self.upgradeTimeText = self.browser.find_element_by_css_selector('#main_buildrow_wood > td:nth-child(5)').text
        self.costPopulation = int(self.browser.find_element_by_css_selector('#main_buildrow_wood > td:nth-child(6)').text)
        self.upgradeTimeSeconds = sum( x * int(t) for x, t in zip([3600, 60, 1], self.upgradeTimeText.split(':')))
        if self.costPopulation > self.maxPopulation - self.currentPopulation:
            resourceUpgradeBot.upgradeFarm()
        else:
            if max(self.costWood, self.costStone, self.costIron) > self.maxStorage:
                resourceUpgradeBot.upgradeStorage()
            else:
                if self.wood >= self.costWood and self.iron >= self.costIron and self.stone >= self.costStone:
                    self.buttonUpgrade = self.browser.find_element_by_css_selector("#main_buildlink_wood_" + str(levelWood) )
                    self.buttonUpgrade.click()
                else:
                    self.needWood = self.costWood - self.wood
                    self.needIron = self.costIron - self.iron
                    self.needStone = self.costStone - self.stone
                    #Hour conversion
                    self.timeForWood = (self.needWood/self.woodPerHour) * 3600 + 60
                    self.timeForIron = (self.needIron/self.ironPerHour) * 3600 + 60
                    self.timeForStone = (self.needStone/self.stonePerHour) * 3600 + 60

                    self.waitTime = max( self.timeForWood, self.timeForIron, self.timeForStone )
                    print ("Time to get all resource that you need:" + str(self.waitTime) )
                    time.sleep(self.waitTime + 2)
                    self.browser.get(self.browser.getCurrentUrl())
                    self.buttonUpgrade = self.browser.find_element_by_css_selector("#main_buildlink_wood_" + str(levelWood) )
                    self.buttonUpgrade.click()

                print ("Time Until Upgrade is ready: " + str(self.upgradeTimeSeconds) )
                time.sleep(self.upgradeTimeSeconds + 2)

    def upgradeStone(self, levelStone):

        #activate execute_script when wood is out of window ( when u have more building it happens )

        #self.browser.execute_script('arguments[0].scrollIntoView();',self.buttonUpgrade)
        self.costWood = int(self.browser.find_element_by_css_selector('#main_buildrow_stone > td:nth-child(2)').text)
        self.costStone = int(self.browser.find_element_by_css_selector('#main_buildrow_stone > td:nth-child(3)').text)
        self.costIron = int(self.browser.find_element_by_css_selector('#main_buildrow_stone > td:nth-child(4)').text)
        self.upgradeTimeText = self.browser.find_element_by_css_selector('#main_buildrow_stone > td:nth-child(5)').text
        self.costPopulation = int(self.browser.find_element_by_css_selector('#main_buildrow_stone > td:nth-child(6)').text)
        self.upgradeTimeSeconds = sum( x * int(t) for x, t in zip([3600, 60, 1], self.upgradeTimeText.split(':')))
        if self.costPopulation > self.maxPopulation - self.currentPopulation:
            resourceUpgradeBot.upgradeFarm()
        else:
            if max(self.costWood, self.costStone, self.costIron) > self.maxStorage:
                resourceUpgradeBot.upgradeStorage()
            else:
                if self.wood > self.costWood and self.iron > self.costIron and self.stone > self.costStone:
                    self.buttonUpgrade = self.browser.find_element_by_css_selector("#main_buildlink_stone_" + str(levelStone) )
                    self.buttonUpgrade.click()
                else:
                    self.needWood = self.costWood - self.wood
                    self.needIron = self.costIron - self.iron
                    self.needStone = self.costStone - self.stone

                    #Hour conversion
                    self.timeForWood = (self.needWood/self.woodPerHour) * 3600 + 60
                    self.timeForIron = (self.needIron/self.ironPerHour) * 3600 + 60
                    self.timeForStone = (self.needStone/self.stonePerHour) * 3600 + 60

                    self.waitTime = max( self.timeForWood, self.timeForIron, self.timeForStone )
                    print ("Time to get all resource that you need:" + str(self.waitTime) )
                    time.sleep(self.waitTime + 2)
                    self.browser.get(self.browser.getCurrentUrl())
                    self.buttonUpgrade = self.browser.find_element_by_css_selector("#main_buildlink_stone_" + str(levelStone) )
                    self.buttonUpgrade.click()

                print ("Time Until Upgrade is ready: " + str(self.upgradeTimeSeconds) )
                time.sleep(self.upgradeTimeSeconds + 2)

    def upgradeIron(self, levelIron):

        #activate execute_script when wood is out of window ( when u have more building it happens )

        #self.browser.execute_script('arguments[0].scrollIntoView();',self.buttonUpgrade)
        self.costWood = int(self.browser.find_element_by_css_selector('#main_buildrow_iron > td:nth-child(2)').text)
        self.costStone = int(self.browser.find_element_by_css_selector('#main_buildrow_iron > td:nth-child(3)').text)
        self.costIron = int(self.browser.find_element_by_css_selector('#main_buildrow_iron > td:nth-child(4)').text)
        self.upgradeTimeText = self.browser.find_element_by_css_selector('#main_buildrow_iron > td:nth-child(5)').text
        self.costPopulation = int(self.browser.find_element_by_css_selector('#main_buildrow_iron > td:nth-child(6)').text)
        self.upgradeTimeSeconds = sum( x * int(t) for x, t in zip([3600, 60, 1], self.upgradeTimeText.split(':')))
        if self.costPopulation > self.maxPopulation - self.currentPopulation:
            resourceUpgradeBot.upgradeFarm()
        else:
            if max(self.costWood, self.costStone, self.costIron) > self.maxStorage:
                resourceUpgradeBot.upgradeStorage()
            else:
                if self.wood > self.costWood and self.iron > self.costIron and self.stone > self.costStone:
                    self.buttonUpgrade = self.browser.find_element_by_css_selector('#main_buildlink_iron_' + str(levelIron) )
                    self.buttonUpgrade.click()
                else:
                    self.needWood = self.costWood - self.wood
                    self.needIron = self.costIron - self.iron
                    self.needStone = self.costStone - self.stone

                    #Hour conversion
                    self.timeForWood = (self.needWood/self.woodPerHour) * 3600 + 60
                    self.timeForIron = (self.needIron/self.ironPerHour) * 3600 + 60
                    self.timeForStone = (self.needStone/self.stonePerHour) * 3600 + 60

                    self.waitTime = max( self.timeForWood, self.timeForIron, self.timeForStone )
                    print ("Time to get all resource that you need:" + str(self.waitTime) )
                    time.sleep(self.waitTime + 2)
                    self.browser.get(self.browser.getCurrentUrl())
                    self.buttonUpgrade = self.browser.find_element_by_css_selector('#main_buildlink_iron_' + str(levelIron) )
                    self.buttonUpgrade.click()

                print ("Time Until Upgrade is ready: " + str(self.upgradeTimeSeconds) )
                time.sleep(self.upgradeTimeSeconds + 2)

    def compareLevels(self):
        self.browser.find_element_by_class_name('visual-label-main').click()
        self.levelWoodText = self.browser.find_element_by_css_selector('#main_buildrow_wood > td:nth-child(1) > span:nth-child(4)').text
        self.levelStoneText = self.browser.find_element_by_css_selector('#main_buildrow_stone > td:nth-child(1) > span:nth-child(4)').text
        self.levelIronText = self.browser.find_element_by_css_selector('#main_buildrow_iron > td:nth-child(1) > span:nth-child(4)').text
        self.levelWood = int(self.levelWoodText[-1:]) + 1
        self.levelStone = int(self.levelStoneText[-1:]) + 1
        self.levelIron = int(self.levelIronText[-1:]) + 1
        self.homeButton = self.browser.find_element_by_class_name("village")
        #This can be chaned however you want to prioritize, presonal i like to have equal in... or in worst case more Wood
        if self.levelWood == self.levelIron == self.levelStone:
            resourceUpgradeBot.upgradeWood(self.levelWood)
            #Sometimes when you have more buldings is necesarry to activate it... game sucks sometimes with scroll Don't know why
            #self.browser.execute_script('arguments[0].scrollIntoView();',self.homeButton)
            self.homeButton.click()
            return

        if self.levelStone <= self.levelIron and self.levelStone < self.levelWood:
            resourceUpgradeBot.upgradeStone(self.levelStone)
            #Sometimes when you have more buldings is necesarry to activate it... game sucks sometimes with scroll Don't know why
            #self.browser.execute_script('arguments[0].scrollIntoView();',self.homeButton)
            self.homeButton.click()
            return

        if self.levelIron < self.levelStone and self.levelIron < self.levelWood:
            resourceUpgradeBot.upgradeIron(self.levelIron)
            #Sometimes when you have more buldings is necesarry to activate it... game sucks sometimes with scroll Don't know why
            #self.browser.execute_script('arguments[0].scrollIntoView();',self.homeButton)
            self.homeButton.click()
            return

        if self.levelWood < self.levelIron and self.levelWood < self.levelStone:
            resourceUpgradeBot.upgradeWood(self.levelWood)
            #self.browser.execute_script('arguments[0].scrollIntoView();',self.homeButton)
            self.homeButton.click()
            return
decison = int(input("1)Force Auto-Quest(experimental)\n2)Auto-Build Resource\n3)Auto-Recruitment Army(in-development)\nChoose what BOT to do: " ))
loginBot = Triburile_Login('username','password') # change it
loginBot.logIn()
loginBot.startPopUp()
print ("\n\t")
print ("Stage 1")
print ("\n")
dataBot = Data_Village(loginBot)
dataBot.getResourceInfo()
dataBot.getGeneralInfo()

# Skip when you have a mission with minimap, to hard to automatize for attacking a village, i have to find a way to import full map from game
if decison == 1 :
    while True:
        questBot = Village_Quest(dataBot)
        questBot.questPrioritize()
        questBot.questFinished()
        dataBot.getResourceInfo()
        dataBot.getGeneralInfo()

elif decison == 2:
    stage = 2
    resourceUpgradeBot = Resource_Upgrade(dataBot)
    while True:
        resourceUpgradeBot.compareLevels()
        print ("\n")
        print ("\n\t")
        print ("Stage " + str(stage) )
        print ("\n")
        stage = stage + 1
        dataBot.getResourceInfo()
        dataBot.getGeneralInfo()

#This game is based on resource development and/or army development
#The problem is you have to wait time until a building is Upgraded
#And you can choose only 2 building at a time... play it a little and you will got how it works
#So when you set wood resource to upgrade you have to wait 'X' time to wait
#And stone resource to upgrade and you have a 'Y' time to wait.
#In total you have to wait X minute to set another command, or X+Y for 2 new commands
#When you set 2 command on a day night you will waste a couple of hours doing nothing
#So you can use this bot to take care of your village when you aren't in front of computer
#You can choose to upgrade resource on night time on equal level, or modify a little bit code for what u want to prioritize
# If you  don't have enough resource to upgrade a building, bot will wait exact time for upgrade it
#The same problem is on army development too.
