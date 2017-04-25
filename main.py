import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np

import config
from younet_rnd_infrastructure.tri.common import utils
from younet_rnd_infrastructure.tri.common import file_tool


def get_url_profile_by_age(age, size=500):
    time.sleep(np.random.randint(0, 1500)/1000.0)

    driver = webdriver.Chrome()
    driver.get("https://facebook.com/")
    email_input = driver.find_element_by_id("email")
    email_input.clear()
    email_input.send_keys(config.get_email())

    password_input = driver.find_element_by_id("pass")
    password_input.clear()
    password_input.send_keys(config.get_pass())
    password_input.send_keys(Keys.ENTER)

    try:
        # To ensure we have already loged in
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "q"))
        )
        driver.get('https://www.facebook.com/search/%s/users-age' % age)

        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_1uh-"))
        )

        for i in range(size):
            print 'Send page down %s/%s' % (i, size)
            time.sleep(2)
            element.send_keys(Keys.PAGE_DOWN)
            if len(driver.find_elements_by_xpath("//*[contains(text(), 'End of results')]")) != 0:
                print 'There are no more result.'
                break

        with open('./temp/age_%s.html' % age, 'w') as input:
            input.write(driver.page_source)

        users_href = driver.find_elements_by_css_selector('._gll a')
        users_url_profile = map(lambda x: x.get_attribute('href'), users_href)
        df = pd.DataFrame(users_url_profile)

        driver.quit()
        return df

    except Exception as e:
        print e
        return pd.DataFrame()


def get_url_profile_by_ages(ages, n_jobs=6):
    url_profile_by_ages = utils.run_paralell(get_url_profile_by_age, ages, n_jobs=n_jobs)
    return url_profile_by_ages


def count_result(ages):
    total = 0
    for age in ages:
        df = pd.read_csv('./output/profiles_by_age_%s.csv' % age)
        total += df.shape[0]
    return total


def aggregate_result(ages):
    list_csv_file = map(lambda x: './output/profiles_by_age_%s.csv' % x, ages)
    result_df = pd.DataFrame(columns=['url', 'age'])
    for i in range(len(list_csv_file)):
        df = pd.read_csv(list_csv_file[i])
        df['url'] = df.iloc[:, 0]
        df['age'] = int(ages[i])

        result_df = result_df.append(df, ignore_index=True)
    result_df[['age','url']].to_csv('./output/profile_by_ages.csv', index=None)


if __name__ == '__main__':
    ages = range(20, 50)
    # It will open 6 browser's window at the same time
    url_profile_by_ages = utils.time_measure(get_url_profile_by_ages, [ages, 6])
    for i in range(len(ages)):
        print 'Size df age %s: %s' % (ages[i], url_profile_by_ages[i].shape[0])
        url_profile_by_ages[i].to_csv('./output/profiles_by_age_%s.csv' % ages[i], index=None)

    aggregate_result(ages)
