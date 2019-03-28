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

class Data_Village(Triburile_Login): # Get important data from your village
    def __init__(self, login_class ):
        self.browser = login_class.browser

    def getResourceInfo(self):
        self.wood = int(self.browser.find_element_by_id('wood').text)
        self.stone = int(self.browser.find_element_by_id('stone').text)
        self.iron = int(self.browser.find_element_by_id('iron').text)
        #self.wood_per_hour = int(self.browser.find_element_by_css_selector('tr.nowrap:nth-child(1) > td:nth-child(2) > strong:nth-child(1)').text)
        #self.stone_per_hour = int(self.browser.find_element_by_css_selector('tr.nowrap:nth-child(2) > td:nth-child(2) > strong:nth-child(1)').text)
        #self.iron_per_hour = int(self.browser.find_element_by_css_selector('tr.nowrap:nth-child(3) > td:nth-child(2) > strong:nth-child(1)').text)
        print ('Current wood ' + str(self.wood))
        print ('Current stone ' + str(self.stone))
        print ('Current iron ' + str(self.iron))
        #print ('Wood production per hour ' + str(self.wood))
        #print ('Stone production per hour ' + str(self.stone))
        #print ('Iron production per hour ' + str(self.iron))

    def getGeneralInfo(self):
        self.currentPopulation = int(self.browser.find_element_by_id('pop_current_label').text)
        self.maxPopulation = int(self.browser.find_element_by_id('pop_max_label').text)
        self.maxStorage = int(self.browser.find_element_by_id('storage').text)
        print ('Current population ' + str(self.currentPopulation))
        print ('Max population ' + str(self.maxPopulation))
        print ('Storage Capacity ' + str(self.maxStorage))

class Upgrade_Village_Quest(Data_Village):
    def __init__(self, data_class ):
        self.browser = data_class.browser
        self.wood = data_class.wood
        self.stone = data_class.stone
        self.iron = data_class.iron
        self.currentPopulation = data_class.currentPopulation
        self.maxPopulation = data_class.maxPopulation

    def questPrioritize(self): #He is trying to prioritize quest for getting rewards
        self.browser.find_element_by_class_name('visual-label-main').click()
        upgradeBot.popUp_Event()
        try:
            find_quest = self.browser.find_element_by_class_name('quest-arrow-target')
            while find_quest != None:
                find_quest.click()
                time.sleep(2)
                find_quest = self.browser.find_element_by_class_name('quest-arrow-target')
        except Exception:
            print ("No current Quest")
            self.browser.find_element_by_class_name("village").click()
            pass

    def popUp_Event(self): #closing popUp dialoge box
        try:
            popup = self.browser.find_element_by_id('popup_box_quest')
            if popup != None:
                self.browser.find_element_by_class_name('btn')
        except Exception:
            pass

    def noSpaceDep(self): # When you have to take a reward from quest but not enough space
        self.browser.find_element_by_class_name('visual-label-main').click()
        self.request_wood = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(2)').text)
        self.request_stone = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(3)').text)
        self.request_iron = int(self.browser.find_element_by_css_selector('#main_buildrow_storage > td:nth-child(4)').text)
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

    def questFinished(self): # Checking Dialog Box Quest for taking reward
        try:
            self.browser.find_element_by_class_name('finished').click()
            time.sleep(2)
            try:
                warn = self.browser.find_element_by_class_name('warn')
                print ("Warning Not Enough Capacity")
                self.browser.find_element_by_class_name('popup_box_close').click()
                upgradeBot.noSpaceDep()
            except Exception:
                print ("Quest Finished")
                self.browser.find_element_by_css_selector('.btn-confirm-yes').click()
                time.sleep(2)

        except Exception:
            pass

loginBot = Triburile_Login('username','password') # change it
loginBot.logIn()

dataBot = Data_Village(loginBot)
dataBot.getResourceInfo()
dataBot.getGeneralInfo()

<<<<<<< HEAD
# Skip when you have a mission with minimap, to hard to automatize for attacking a village, i have to find a way to import full map from game
questBot = Village_Quest(dataBot)
questBot.questPrioritize()
questBot.questFinished()

stage = 2;
resourceUpgradeBot = Resource_Upgrade(dataBot)
while True:
    resourceUpgradeBot.compareLevels()
    print ("\n")
    print ("\n")
    print ("Stage " + k )
    print ("\n")
<<<<<<< HEAD
    k = k + 1
=======
    ++k
>>>>>>> master
    dataBot.getResourceInfo()
    dataBot.getGeneralInfo()

#This game is based on resource development and/or army development
#The problem is you have to wait time until a building is Upgraded
#And you can chose only 2 building at a time... play it a little and you will got how it works
#So when you set wood resource to upgrade you have to wait 'X' time to wait
#And stone resource to upgrade and you have a 'Y' time to wait.
#In total you have to wait X minute to set another command, or X+Y for 2 new commands
#When you set 2 command on a day night you will waste a couple of hours doing nothing
#So you can use this bot to take care of your village when you aren't in front of computer
#You can chose to upgrade resource on night time on equal level, or modify a little bit code for what u want to prioritize
# If you  don't have enough resource to upgrade a building, bot will wait exact time for upgrade it
#The same problem is on army development too.
=======
upgradeBot = Upgrade_Village_Quest(dataBot)
upgradeBot.popUp_Event()
upgradeBot.questPrioritize()
upgradeBot.questFinished()
>>>>>>> parent of 5a5bbc5... New Feature
