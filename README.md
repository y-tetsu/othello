# othello
Pythonで作るオセロゲーム

## GUI版
```
$ python othello.py
```
![gui](https://github.com/y-tetsu/othello/blob/master/image/gui.gif?raw=true)

## コンソール版
```
$ python othelloc.py
```
![console](https://github.com/y-tetsu/othello/blob/master/image/console.gif?raw=true)

## 対戦相手紹介
選択可能な対戦相手(AI戦略)の一覧です。<br>
難易度は8x8サイズの場合の目安となっております。<br>
CPUの持ち時間は0.5秒までとしています。

 |対戦相手|特徴|難易度|
 |:---|:---|:---:|
 |User1, User2 |人が操作します。 | ？ |
 |Unselfish |なるべく少なく取ろうとします。 | ★ |
 |Random |ランダムに手を選びます。 | ★ |
 |Greedy |なるべく多く取ろうとします。 | ★ |
 |SlowStarter |残り手数が15%未満の場合はUnselfish戦略、<br>15%以上の場合はGreedy戦略を取ります。 | ★ |
 |Table |評価テーブルにより盤面を評価して手を選びます。<br>なるべく少なく取り、角を狙い、角のそばは避けます。 | ★ |
 |MinMax |ミニマックス法で2手先を読んで手を選びます。<br>Table戦略に加えて、配置可能数と勝敗を盤面評価の考慮に入れます。 | ★★ |
 |MonteCarlo |モンテカルロ法で手を選びます。| ★★ |
 |NegaMax |ネガマックス法で3手先を読んで手を選びます。| ★★ |
 |AlphaBeta |アルファベータ法で4手先を読んで手を選びます。| ★★ |
 |Iterative |反復深化法で手を選びます。 | ★★★ |
 |FullReading |終盤残り11手から石差を読んで手を選びます。 | ★★★ |
 |Joseki |序盤は定石通りに手を選びます。 | ★★★ |

## 動作確認環境
- Windows10<br>
- Python 3.7.0<br>
    - numpy 1.15.1<br>
    - pyinstaller 3.4<br>
    - cython 0.28.5<br>
- Microsoft Visual C++ 2019<br>

## 参考書籍
- 「実践Python3」Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン [ISBN978-4-87311-739-3](https://www.oreilly.co.jp/books/9784873117393/)
- 「Java言語で学ぶデザインパターン入門」結城 浩著 ソフトバンククリエイティブ株式会社 [ISBN4-7973-2703-0](https://www.hyuki.com/dp/)
- 「日経ソフトウェア2019年11月号」 日経BP [ISSN1347-4685](https://books.google.co.jp/books?id=qhCxDwAAQBAJ&pg=PA146&lpg=PA146&dq=ISSN1347-4685&source=bl&ots=_3Z0k4Y_WE&sig=ACfU3U1urxBdw_srrg62Kr5UJD1sXLEQbQ&hl=ja&sa=X&ved=2ahUKEwjlkqzArY_nAhVTc3AKHXlBA6YQ6AEwAHoECAkQAQ#v=onepage&q=ISSN1347-4685&f=false)

## 参考サイト
- 「オセロ・リバーシプログラミング講座 ～勝ち方・考え方～」https://uguisu.skr.jp/othello/
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70
