# ESJ-novel-backup
ESJZone 小說的備份工具

## Python 版本
Python 2.x 對應 esjbackup.py  
Python 3.x 對應 esjbackup3.py

## 使用方法

### 單部小說（從小說主頁備份）  

範例：https://www.esjzone.cc/detail/1599746513.html

`pyhon esjbackup.py https://www.esjzone.cc/detail/1599746513.html`

讀取該小說的章節頁面，依序將該頁面內所有的「站內連結」來做備份，並把它寫成一個 txt 文字檔，檔案名為該小說的名稱。   
  
　  
  
### 單部小說（從小說論壇備份）

範例：https://www.esjzone.cc/forum/1584679807/1599746513/

`pyhon esjbackup.py https://www.esjzone.cc/forum/1584679807/1599746513/`

生成該小說名稱的目錄，該目錄內有所有論壇內文章的 txt 文字檔，檔案名為該文章的標題名稱。

　  

### 單篇文章

範例：https://www.esjzone.cc/forum/1599746513/121688.html

`pyhon esjbackup.py https://www.esjzone.cc/forum/1599746513/121688.html`

僅保存該單篇的  txt 文字檔。
