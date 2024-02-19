from selenium import webdriver
from bs4 import BeautifulSoup
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from tqdm import tqdm
import pandas as pd
import argparse
import os

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url",type=str,required=True)
    parser.add_argument("--id",type=str,required=True)
    parser.add_argument("--password",type=str,required=True)
    parser.add_argument("--key1",type=str,required=True)
    parser.add_argument("--key2",type=str,required=True)
    parser.add_argument("--save_path", type=str,required=True)
    return parser.parse_args()

def get_url(driver, url, id, password):
    # 사람인 get6
    driver.get(url)
    time.sleep(10)

    btn= driver.find_element(By.CSS_SELECTOR, '#utility > li.member_menu > a')
    btn.click()
    time.sleep(1)

    ID = driver.find_element(By.CSS_SELECTOR, '#id')
    ID.send_keys(id)
    time.sleep(1)

    PASSWORD = driver.find_element(By.CSS_SELECTOR, '#password')
    PASSWORD.send_keys(password)
    time.sleep(1)

    login= driver.find_element(By.CSS_SELECTOR, '#login_frm > div > div > div.cm_login_box > button')
    login.click()
    time.sleep(1)

    menu= driver.find_element(By.CSS_SELECTOR, '#gnb_position_manage')
    menu.click()
    time.sleep(1)

    check_2= driver.find_element(By.CSS_SELECTOR, '#content > div > div.certification_dispatch_wrap > div:nth-child(1) > div.wrap_btn > button')
    check_2.click()
    time.sleep(1)

def second_check(driver, number):
    check_number = driver.find_element(By.CSS_SELECTOR, '#cert_code')
    check_number.send_keys(number)

    check= driver.find_element(By.CSS_SELECTOR, '#validate_cert_code')
    check.click()
    time.sleep(1)

    not_look= driver.find_element(By.CSS_SELECTOR, '#app > div.ModalBox.modal_minimum_wage.Show.modal_join_benefit.modal_talent_pool > div.ModalCont > button')
    not_look.click()
    time.sleep(1)

def keyword(driver, key1, key2):
    keyword1 = driver.find_element(By.CSS_SELECTOR, '#app > div.talent_header > div > div > div.search_form_wrap > div.search_default > input')
    keyword1.click()
    time.sleep(1) 
    
    keyword11 = driver.find_element(By.CSS_SELECTOR, "#app > div.talent_header > div > div > div.search_form_wrap > div.search_default > div.search_detail > div.search_input_top > div > div > input")
    keyword11.send_keys(key1)
    time.sleep(1)
    
    keyword11.send_keys(Keys.ENTER)
    time.sleep(1)

    keyword2 = driver.find_element(By.CSS_SELECTOR, '#app > div.talent_header > div > div > div.search_form_wrap > div.search_word_include > input')
    keyword2.click()
    time.sleep(1)

    keyword22 = driver.find_element(By.CSS_SELECTOR, "#app > div.talent_header > div > div > div.search_form_wrap > div.search_word_include > div.search_detail > div.search_input_top > div > div > input")
    keyword22.send_keys(key2)

    time.sleep(1)
    keyword22.send_keys(Keys.ENTER)
    time.sleep(1)

def get_text(driver, cnt, page, save_path):
    html = driver.page_source
    soup = BeautifulSoup(html, 'lxml')
    # 이름
    try:
        name=soup.select('#resume_print_area > div > section.resume_basic > div > div.resume_top > h1')[0].text
    except:
        name=""
    # basic info
    try:
        basic_info=soup.select("#resume_print_area > div > section.resume_basic > div > p")[0].text
    except:
        basic_info=""
    
    try:
        # info
        info_1=soup.select("#resume_print_area > div > section.resume_basic > ul > li:nth-child(1)")[0].text
        info_2=soup.select("#resume_print_area > div > section.resume_basic > ul > li:nth-child(2)")[0].text
        info_3=soup.select("#resume_print_area > div > section.resume_basic > ul > li:nth-child(3)")[0].text
        info_4=soup.select("#resume_print_area > div > section.resume_basic > ul > li:nth-child(4)")[0].text
    except:
        info_1, info_2, info_3, info_4 = "None", "None", "None", "None"

    try:
        # 간략 소개, 없을 수 있음.
        content=soup.select("#resume_print_area > div > section.resume_letter")[0].text
    except:
        content=""
    try:
        # 경력
        experience=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(1) > div.box_tit")[0].text
        experience_text=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(1) > div.box_con")[0].text
    except:
        experience=""
        experience_text=""
    try:
        # 학력
        education=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(2) > div.box_tit")[0].text
        education_text=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(2) > div.box_con")[0].text
    except:
        education=""
        education_text=""
    try:
        # 자격/어학/수상
        award=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(3) > div.box_tit")[0].text
        award_text=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(3) > div.box_con")[0].text
    except:
        award=""
        award_text=""
    try:
        # 취업우대사항
        briefs=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(4) > div.box_tit")[0].text
        briefs_text=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(4) > div.box_con")[0].text
    except:
        briefs=""
        briefs_text=""
    try:
        # 경력기술서
        project=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(5) > div.box_tit")[0].text
        project_text=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(5) > div.box_con")[0].text
    except:
        project=""
        project_text=""
    try:
        # 자기소개서
        introduc=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(6) > div.box_tit")[0].text
        introduc_text=soup.select("#resume_print_area > div > div.resume_part > div:nth-child(6) > div.box_con")[0].text
    except:
        introduc=""
        introduc_text=""
    
    # 텍스트 템플릿
    text=f"""이력서
    성명:{name}
    {basic_info}
    {experience}{experience_text}
    {education}{education_text}
    {award}{award_text}
    {briefs}{briefs_text}
    {project}{project_text}
    {introduc}{introduc_text}
    """
    if not os.path.exists(save_path):
        os.makedirs(save_path)
    data_path=os.path.join(save_path, f"CV_{page}_{cnt}.txt")
    file = open(data_path, "w", encoding="utf-8") 
    file.write(text)
    file.close()
def main(args):
    print("-----------connect webdriver-----------")
    # 크롬 드라이버 불러오기
    driver = webdriver.Chrome()
    time.sleep(2)

    print("-----------connect url&login-----------")
    get_url(driver, args.url, args.id, args.password)

    print("-----------check second_certification-----------")
    number = int(input())
    second_check(driver, number)

    print("-----------keyword-----------")
    keyword(driver, args.key1, args.key2)

    print("-----------start crawling-----------")
    page=1
    while True:
        for i in range(1,21):
            try: 
                personal_info = driver.find_element(By.CSS_SELECTOR, f'#app > div.talent_container > div.talent_contents > div > div.talent_list > div:nth-child({i}) > div.summary_info > a > div.personal_info')
                personal_info.click()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)
                get_text(driver, i, page, args.save_path)
                time.sleep(1)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
            except:
                driver.find_element(By.CSS_SELECTOR, f"#app > div.talent_container > div.talent_contents > div > div.talent_list > div:nth-child({i}) > div.summary_info > a > div.personal_info").click()
                time.sleep(1)
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(1)
                get_text(driver, i, page, args.save_path)
                time.sleep(1)
                driver.close()
                driver.switch_to.window(driver.window_handles[0])
        page+=1
        # 페이지 넘어가기
        try:
            driver.find_element(By.CSS_SELECTOR, f"#app > div.talent_container > div.talent_contents > div > div.talent_list > div.PageBox > button:nth-child({page+1})").click() 
        except:
            driver.find_element(By.CSS_SELECTOR, f"#app > div.talent_container > div.talent_contents > div > div.talent_list > div.PageBox > button:nth-child({page+1})").click() 
        time.sleep(2)
if __name__=="__main__":
    args=parse_args()
    main(args)
    print(print("-----------end crawling-----------"))