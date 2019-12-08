from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import WebDriverException

MAX_WAIT = 10

# Clean up after FT runs(LiveServerTestCase)
class NewVisitorTest(LiveServerTestCase):
    def setUp(self):
        # https://codedragon.tistory.com/6114
        # C:\Users\sdrlu\Anaconda\Library\bin
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    # Remove time.sleeps
    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException):
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def test_can_start_a_list_and_retrieve_it_later(self):
        # 영애씨는 온라인 일정관리 앱을 알게 되어 홈페이지에 방문한다.
        self.browser.get(self.live_server_url)

        # 홈페이지에 방문해 보니 제목이 "일정관리"인 것을 보고 홈페이지에 올바르게 방문한 것을 확인한다.
        self.assertIn('일정관리', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('일정목록', header_text)

        # 일정을 입력할 수 있는 페이지로 바로 이동한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(inputbox.get_attribute('placeholder'), '할일을 입력하세요')

        # 영애씨는 생일날 미역국을 끓이기 위해 텍스트박스에 "시장에서 미역 사기"를 입력한다.
        inputbox.send_keys('시장에서 미역 사기')

        # 영애씨가 엔터를 입력하면 페이지를 새로고침해서 모든 일정 목록을 보여준다.
        # "1: 시장에서 미역 사기"가 첫 번째 할일로 일정 목록에서 보여진다.
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 시장에서 미역 사기')

        # 영애씨는 추가로 할일 텍스트박스에 입력할 수 있고
        # "미역을 물에 불리기"라고 입력한다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('미역을 물에 불리기')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # 다시 페이지를 새로고침해서 입력한 일정 두 가지 모두 목록에 표시한다.
        self.wait_for_row_in_list_table('1: 시장에서 미역 사기')
        self.wait_for_row_in_list_table('2: 미역을 물에 불리기')
        self.fail('Finish the test!')

        # 영애씨는 일정 목록이 사이트에 올바로 저장되었는지 궁금해서
        # 고유 URL 생성을 확인한다.

        # 영애씨는 URL을 방문하고 일정 목록이 올바르게 있음을 확인한다.

        # 영애씨는 이제 만족하고 잠을 자러간다.

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Edith는 새로운 일정 목록을 시작한다.
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('시장에서 미역 사기')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 시장에서 미역 사기')

        # 그녀는 유일한 URL을 가지는 그녀의 목록을 확인한다.
        edith_list_url = self.browser.current_url
        self.assertRegex(edith_list_url, '/lists/.+')

        # 이제 Francis가 이 사이트로 들어온다.
        # 우리는 Edith의 쿠키등으로 들어온 정보가 없는 걸 보장하기
        # 위해 새로운 브라주어를 사용한다
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # Francis가 홈페이지를 방문한다. Edith의 목록은 없다.
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('시장에서 미역 사기', page_text)

        # Francis는 새로운 아이템을 엔터로 넣기 시작한다.
        # 그는 Edith보다 관심이 적다.
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys("우유 사기")
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: 우유 사기')

        # Francis는 그의 고유의 유일한 URL을 얻습니다.
        francis_list_url = self.browser.current_url
        self.assertRegex(francis_list_url, '/lists/.+')
        self.assertNotEqual(francis_list_url, edith_list_url)

        # 다시, Edith의 목록이 흔적이 없음을 확인한다.
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('시장에서 미역 사기', page_text)
        self.assertIn('우유 사기', page_text)

        # 만족하고 둘다 자러 간다.

        


if __name__ == '__main__':
    unittest.main(warnings='ignore')