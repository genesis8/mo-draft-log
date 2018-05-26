#####################################################################################
#
#	ログと画像を受け取って、以下のようなHTMLを生成します。
#
#	生成されるHTMLファイル名は [画像のbasename].html になります。
#	例えば画像が 20180524_1000_2-1.png の場合は、
#	HTMLファイル名は 20180524_1000_2-1.html となります。
#
#	このツールではブラウザオートメーションツールであるseleniumを利用しています。
#	Chromeドライバのパスはハードコーディングされているので適宜書き換えて下さい。
#
#	環境要件：
#			1. pythonのインストール
#			2. seleniumのインストール
#			3. ChromeDriverの導入およびコード内でのパス指定
#
#	引数:
#			1. ログ
#			2. 画像
#
#####################################################################################

import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#------------------------------------------------------------------------------------
# 環境設定
#------------------------------------------------------------------------------------

# Chromeドライバのパス
chrome_driver_path = "webdriver/chromedriver.exe"

#------------------------------------------------------------------------------------
# インプット
#------------------------------------------------------------------------------------

# 引数を取得
args = sys.argv
if len(args) != 3:
	print("引数は2個指定してください")
	exit()
print("ログ",args[1])
print("画像",args[2])
pic_log_file_name = args[1]
pic_pic_file_name = args[2]

#------------------------------------------------------------------------------------
# HTML生成
#------------------------------------------------------------------------------------

# ピック譜を読み込み
print("ピック譜を読み込み中・・・")
pic_log_file = open(pic_log_file_name, 'r')
pic_log = pic_log_file.read()
pic_log_file.close()
print(pic_log)


# エキスパンション名を修正
pic_log = pic_log.replace(" DAR "," DOM ")
print(pic_log)

# ヘッドレスモードでChromeドライバを作成
print("Chromeドライバ起動中・・・")
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome(chrome_driver_path, chrome_options=options)

# ドラフトコンバータにアクセス
driver.get("http://www.zizibaloob.com/convert_images.html")

# ピック譜をHTMLにコンバート
print("ドラフトコンバータで処理中・・・")
elem_search_word = driver.find_element_by_id("draft_in")
elem_search_word.send_keys(pic_log)
elem_search_btn = driver.find_element_by_xpath('//*[@id="main"]/tbody/tr[2]/td[2]/table/tbody/tr/td[1]/input')
elem_search_btn.click()
elem_result_box = driver.find_element_by_id("draft_out")
cvt_text = elem_result_box.get_attribute("value")

# ドラフトコンバータを閉じる
#driver.close()

# 結果の取得
print(cvt_text)

# 最後に画像を追加
image_tag = '<br><img src="' + pic_pic_file_name + '">'
cvt_text = cvt_text + "\n" + image_tag

# HTMLファイルを出力
print("HTLMLファイル出力中・・・")
basename = os.path.splitext(os.path.basename(pic_pic_file_name))[0]
html_file_name = basename + ".html"
print( html_file_name )
html_file = open(html_file_name, 'w')
html_file.write(cvt_text)
html_file.close()

print(html_file_name + "を出力")