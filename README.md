# reversi
Pythonで作るリバーシ

## ゲーム紹介
### GUI版
![gui](https://github.com/y-tetsu/reversi/blob/master/image/gui4.gif?raw=true)
#### 実行方法
```
$ python reversi.py
```

上記の他、Windows版は下記よりexe(ダブルクリックで起動)をダウンロード可能です。<br>
[ダウンロード](https://github.com/y-tetsu/reversi/releases)

### コンソール版
![gui](https://github.com/y-tetsu/reversi/blob/master/image/console2.gif?raw=true)
#### 実行方法
```
$ python reversic.py
```

## 対戦相手紹介
選択可能な対戦相手(CPUの戦略)の一覧です。<br>
難易度は8x8サイズの場合の目安となっております。<br>
CPUの持ち時間のデフォルトは大体0.5秒までとしています。(GUI版では設定変更可)<br>

 |対戦相手|特徴|難易度|
 |:---|:---|:---:|
 |User1, User2 |人が操作します。 | ？ |
 |Unselfish |なるべく少なく取ろうとします。 | ★ |
 |Random |ランダムに手を選びます。 | ★ |
 |Greedy |なるべく多く取ろうとします。 | ★ |
 |SlowStarter |残り手数が15%未満の場合はUnselfish戦略、<br>15%以上の場合はGreedy戦略を取ります。 | ★ |
 |Table |マス目の位置に重みをつけた評価テーブルにより盤面の形勢を判断して手を選びます。<br>なるべく少なく取り、角を狙い、角のそばは避けるよう心掛けます。 | ★★ |
 |MinMax |ミニマックス法で2手先を読んで手を選びます。<br>Table戦略に加えて、配置可能数と勝敗を考慮に入れます。 | ★★ |
 |MonteCarlo |モンテカルロ法で手を選びます。持ち時間の限りプレイアウトを繰り返し、最も勝率の高い手を選びます。| ★★ |
 |NegaMax |ネガマックス法で持ち時間の限り3手先を読んで手を選びます。| ★★★ |
 |AlphaBeta |アルファベータ法(ネガアルファ法)で持ち時間の限り4手先を読んで手を選びます。| ★★★ |
 |FullReading |AlphaBeta戦略に加えて、終盤残り9手からは最終局面の石差を読んで手を選びます。| ★★★ |
 |Joseki |FullReading戦略に加えて、序盤は定石通りに手を選びます。| ★★★ |
 |Iterative |Joseki戦略に反復深化法を適用して持ち時間の限り徐々に深く手を読みます。<br>読む手の深さを増やす際は前回の深さで最も評価が高かった手を最初に調べます。<br>それにより不要な探索をカットし、より深く手を読む場合があります。| ★★★★ |
 |NegaScout |Iterative戦略の探索手法にネガスカウト法を用いて手を読みます。<br>Null Window Searchを行うことで局面によってはアルファベータ法より深く手を読む場合があります。| ★★★★ |

## 自作AI参戦機能
### 概要
本プログラム(**reversi**)はお好きなプログラミング言語で作成したAIをゲームに参加させて遊ぶことができます。<br>
ただし、自作したAIの入出力は所定のフォーマット(後述)に従う必要があります。

### 実行の流れ
自作したAIは、**reversi**に登録する事で外部プログラムとして実行されるようになります。<br>
以下に処理の流れを示します。

1. ゲーム開始後、自作AIの手番になると**reversi**は外部プログラム(自作AI)を実行します。<br>その際、標準入力に盤面の情報を渡しプログラムからの応答を待ちます。
2. 自作AIは標準入力から盤面の情報を受け取り次の手を決めて、その結果を標準出力します。<br>(そのようなプログラムを書いてください)
3. **reversi**は外部プログラムからの標準出力(次の手)を受け取るとゲームを再開します。<br>一定時間応答がない場合は外部プログラムを強制終了し、反則負けとして扱います。

### 標準入力フォーマット
自作AIが受け取る標準入力の情報です。
```
手番の色(黒:1、白:-1)
盤面のサイズ(4～26までの偶数)
盤面の石の2次元配置(空き:0、黒:1、白:-1をスペース区切り)
```

下記に白の手番、盤面サイズ8x8の例を示します。
```
-1
8
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 1 1 1 0 0
0 0 0 -1 1 0 0 0
0 0 -1 -1 1 -1 0 0
0 0 0 0 1 -1 0 0
0 0 0 0 1 -1 0 0
0 0 0 0 0 0 0 0
```

### 標準出力フォーマット
自作AIの実行結果(次の手)を下記に従って標準出力してください。
```
盤面の座標(左上を起点(0,0)としてxとyをスペース区切り)
```

下記にc5へ打つ場合の例を示します。
```
2 4
```

### 登録ファイル
自作したAIを**reversi**に登録するために登録ファイルを作成する必要があります。<br>
登録ファイルは下記のフォーマット(JSON形式)に従って`stratgies/ex/`以下に作成してください。
```
{
    "name": "AIの名前",
    "cmd": "AIの実行コマンド",
    "timeouttime": AIからの応答待ち時間(秒) ※起動に時間がかかる場合があるため、余裕を持った設定を推奨します
}
```

下記にサンプルのpythonで作ったTopLeftの例を示します。
```
{
    "name": "TopLeft",
    "cmd": "python ./strategies/ex/python/topleft.py",
    "timeouttime": 60
}
```

### 手順
自作AI登録までの手順を以下に示します。

1. お好きなプログラミング言語の実行環境を準備して下さい。
2. AIのプログラムを書いて下さい。
3. 登録ファイルを準備して下さい。
4. **reversi**を起動して下さい。
5. Externalメニューより登録ファイルを読み込ませて下さい。

### 外部プログラム一覧
動作環境を別途準備する事で対戦可能となる外部プログラムのAI一覧です。

 |対戦相手|特徴|難易度|
 |:---|:---|:---:|
 |TopLeft |打てる手の中から一番上の左端を選びます。 | ★ |

 |対戦相手|動作環境|実行方法|
 |:---|:---|:---|
 |TopLeft |Python 3.7.0 |`python ./strategies/ex/python/topleft.py` |

---
## 動作確認環境
- Windows10 64bit<br>
- ディスプレイサイズ 1366x768 以上
- プロセッサ 1.6GHz 以上
- メモリ 4.00GB 以上
- Python 3.7.0<br>
    - numpy 1.15.1<br>
    - cython 0.28.5<br>
    - pyinstaller 3.4<br>
- Microsoft Visual C++ 2019<br>

## 参考書籍
- 「実践Python3」Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン [ISBN978-4-87311-739-3](https://www.oreilly.co.jp/books/9784873117393/)
- 「Java言語で学ぶデザインパターン入門」結城 浩著 ソフトバンククリエイティブ株式会社 [ISBN4-7973-2703-0](https://www.hyuki.com/dp/)
- 「日経ソフトウェア2019年11月号」 日経BP [ISSN1347-4685](https://books.google.co.jp/books?id=qhCxDwAAQBAJ&pg=PA146&lpg=PA146&dq=ISSN1347-4685&source=bl&ots=_3Z0k4Y_WE&sig=ACfU3U1urxBdw_srrg62Kr5UJD1sXLEQbQ&hl=ja&sa=X&ved=2ahUKEwjlkqzArY_nAhVTc3AKHXlBA6YQ6AEwAHoECAkQAQ#v=onepage&q=ISSN1347-4685&f=false)

## 参考サイト
- 「オセロ・リバーシプログラミング講座 ～勝ち方・考え方～」https://uguisu.skr.jp/othello/
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「強いオセロプログラムの内部動作」http://www.amy.hi-ho.ne.jp/okuhara/howtoj.htm
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70
