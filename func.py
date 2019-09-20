from bs4 import BeautifulSoup
import requests
import time

links_to_check = []

def get_html(url):
    try:
        r = requests.get(url)
        return r.text
    except Exception as e:
        print(e,2)


def get_all_url_line(html,links_to_check_line,driver):
    try:
        soup = BeautifulSoup(html,'lxml')
        all_matches = soup.find_all('div',class_ = 'c-events__item c-events__item_col')
        
        for match in all_matches:
            link_of_match_soup = match.find('a',class_ = 'c-events__name')
            link_of_match = link_of_match_soup.get('href')
            teams = link_of_match_soup.find_all('span',class_ = 'c-events__item')
            if link_of_match not in links_to_check:
                links_to_check_line[link_of_match] = [teams,get_total(link_of_match,driver)]
    except Exception as e:
        print(e,6)
    
    

def get_all_url_live(html,links_to_check_line,driver):
    try:
        all_matches = driver.find_elements_by_xpath('//div[@class="c-events__item c-events__item_col"]')

        for match in range(len(all_matches)):
            team1 = driver.find_elements_by_xpath('//div[@class="c-events__item c-events__item_col"][{0}]/div[@class="c-events-scoreboard"]/div[@class="c-events__team"][1]'.format(str(match+1))).text
            team2 = driver.find_elements_by_xpath('//div[@class="c-events__item c-events__item_col"][{0}]/div[@class="c-events-scoreboard"]/div[@class="c-events__team"][2]'.format(str(match+1))).text
            teams = [team1,team2]
            overtime = driver.find_element_by_xpath('//div[@class="c-events__item c-events__item_col"][{0}]/span[@class="c-events__overtime"]'.format(str(match+1))).text
            time = driver.find_element_by_xpath('//div[@class="c-events__item c-events__item_col"][{0}]/span[@class="c-events__time"]'.format(str(match+1))).text
            time_min = driver.find_element_by_xpath('//div[@class="c-events__item c-events__item_col"][{0}]/span'.format(str(match+1))).text
            if teams in dict.values() and time == '1-й Тайм' and time_min == '30:00':
                for k in dict.keys():

                    if dict[k][0] == teams:
                        cf = dict[k][1]
                        del dict[k]
                open_and_check(match.find('a',class_='c-events__name').get('href'),cf,time)  #url coef
    except Exception as e:
        print(e,3)

#//div[@class='bet_group_col cols2']/div[1]/div[@class='bet_group']/

def get_total(url,driver):
    try:
        urls = url.split('/')
        url = ''
        for i in urls[0:-1]:
            url += i + '/'
        time.sleep(30)
        driver.get('https://1xstavka.ru/'+url)
        driver.find_element_by_xpath("//button[@data-type='1']").click()
        try:
            FIRST=driver.find_element_by_xpath("//div[@class='bets betCols2']/div[1]/span[@class='bet_type']").text
            LAST=driver.find_element_by_xpath("//div[@class='bets betCols2']/div[last()]/span[@class='bet_type']").text
        except Exception:
            FIRST=driver.find_element_by_xpath("//div[@class='bet_group_col cols2']/div[1]/div[@class='bet_group']/div[@class='bets betCols2']/div[1]/span[@class='bet_type']").text
            LAST=driver.find_element_by_xpath("//div[@class='bet_group_col cols2']/div[1]/div[@class='bet_group']/div[@class='bets betCols2']/div[last()]/span[@class='bet_type']").text
        try:
            FIRST_KF=driver.find_element_by_xpath("//div[@class='bet_group_col cols2']/div[1]/div[@class='bet_group']/div[@class='bets betCols2']/div[1]/span[@class='koeff']").text
            LAST_KF=driver.find_element_by_xpath("//div[@class='bet_group_col cols2']/div[1]/div[@class='bet_group']/div[@class='bets betCols2']/div[last()]/span[@class='koeff']").text
        except Exception:
            FIRST_KF=driver.find_element_by_xpath("//div[@class='bet_group_col cols1']/div[1]/div[@class='bet_group']/div[@class='bets betCols2']/div[1]/span[@class='koeff']").text
            LAST_KF=driver.find_element_by_xpath("//div[@class='bet_group_col cols1']/div[1]/div[@class='bet_group']/div[@class='bets betCols2']/div[last()]/span[@class='koeff']").text
        driver.back()
        l=[[FIRST,LAST],{FIRST:FIRST_KF,LAST:LAST_KF}]
        return l
    except Exception as e:
        print(url)
        print(e,4)





def open_and_check(url,coef,time,driver):
    try:
        split_time=time.split(':')
        #time.sleep(30*60-int(split_time[0])*60-int(split_time[1]))
        driver.get(url)
        total_score_1=int(driver.find_element_by_xpath("//div[@class='tablo_dual_board']/div[@class='db__sport']/div[@class='db-sport__center']/div[@class='db-sport__score']/div[@class='db-sport__score-con']/span[1]").text)
        total_score_2=int(driver.find_element_by_xpath("//div[@class='tablo_dual_board']/div[@class='db__sport']/div[@class='db-sport__center']/div[@class='db-sport__score']/div[@class='db-sport__score-con']/span[last()]").text)
        team1=driver.find_element_by_xpath("//div[@class='tablo_dual_board']/div[@class='db__sport']/div[@class='db-sport__center']/div[@class='db-sport__team'][1]").text
        team2=driver.find_element_by_xpath("//div[@class='tablo_dual_board']/div[@class='db__sport']/div[@class='db-sport__center']/div[@class='db-sport__team'][2]").text
        total_score=total_score_1+total_score_2
        teams=team1+' - '+team2
        text=teams+'\n'
        kf=get_total(url,driver)
        coef_1=coef[0][0].split()
        coef_2=coef[0][1].split()
        if total_score < int(coef_1[0])*0.7:
            text += 'Рекомендуемые параметры\n'+str(kf[0][0])+' '+str(kf[1][kf[0][0]])
        elif total_score > int(coef_1[1])*1.3:
            text += 'Рекомендуемые параметры\n'+str(kf[0][1])+' '+str(kf[1][kf[0][1]])
        r = requests.post('https://api.telegram.org/bot902794685:AAHtVVCBJ6JoUZfEqxebRJ5vzmUZzG_v5c8/sendMessage?chat_id=690965187&text='+text)
        driver.get('https://1xstavka.ru/live/Handball')
    except Exception as e:
        print(e,5)





