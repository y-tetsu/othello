<p align="center">
<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/reversi.png" width="800px">
</p>

# reversi
[ [English](https://github.com/y-tetsu/reversi/blob/master/README.md) | [日本語](https://github.com/y-tetsu/reversi/blob/master/README.ja.md)]<br>
Pythonで使えるリバーシ(オセロ)のライブラリです。<br>
手軽にリバーシAIをプログラミングして遊ぶ事ができます。<br>
[![MIT License](http://img.shields.io/badge/license-MIT-blue.svg?style=flat)](LICENSE)
<br>

## ダウンロード
本ライブラリで作ったWindows版のアプリケーション(exe)を下記よりダウンロードできます。<br>
[reversi.zip](https://github.com/y-tetsu/reversi/releases)(リンク先でAssetsをクリックしてください)

## 動作環境
- Windows10 64bit<br>
- Display size 1366x768
- Processor 1.6GHz
- Memory 4.00GB
- [Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>
    - cython 0.29.15<br>
    - numpy 1.18.1<br>
    - pyinstaller 3.6<br>
- [Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)(When developing)<br>

## インストール方法
1. [Python 3.7.6](https://www.python.org/downloads/release/python-376/)をインストールしてください。<br>
2. 下記を実行して**reversi**ライブラリをインストールしてください。
```
$ py -3.7 -m pip install git+https://github.com/y-tetsu/reversi
```

## アンインストール方法
下記を実行して**reversi**ライブラリをアンインストールしてください。
```
$ py -3.7 -m pip uninstall reversi
```

## サンプル
任意のフォルダで下記コマンドを実行するとサンプルをコピーできます。
```
$ install_reversi_examples
```

コピーされるサンプルは下記のとおりです。

- [01_tkinter_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/01_tkinter_app.py) - tkinterでGUIを作ったアプリケーション
- [02_console_app.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/02_console_app.py) - コンソールで遊ぶアプリケーション
- [03_create_exe.bat](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/03_create_exe.bat) - GUIアプリケーションのexeファイルを作成するバッチファイル
- [04_reversi_simulator.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py) - AI同士を対戦させて結果を表示するシミュレータ
- [05_easy_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/05_easy_strategy.py) - 単純な戦略のAIを実装するサンプル
- [06_table_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/06_table_strategy.py) - テーブルによる重みづけで手を選ぶAIを実装するサンプル
- [07_minmax_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/07_minmax_strategy.py) - MinMax法で手を選ぶAIを実装するサンプル
- [08_alphabeta_strategy.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/08_alphabeta_strategy.py) - AlphaBeta法で手を選ぶAIを実装するサンプル
- [09_genetic_algorithm.py](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/09_genetic_algorithm.py) - 遺伝的アルゴリズムを使ってテーブルの重みを求めるサンプル

サンプルの実行方法はそれぞれ下記のとおりです。
```
$ cd reversi_examples
$ py -3.7 01_tkinter_app.py
$ py -3.7 02_console_app.py
$ 03_create_exe.bat
$ py -3.7 04_reversi_simulator.py
$ py -3.7 05_easy_strategy.py
$ py -3.7 06_table_strategy.py
$ py -3.7 07_minmax_strategy.py
$ py -3.7 08_alphabeta_strategy.py
$ py -3.7 09_genetic_algorithm.py
```

### デモ
[<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/tkinter_app_demo.gif" width="650px">](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/01_tkinter_app.py)
[<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/console_app_demo.gif" width="650px">](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/02_console_app.py)
[<img src="https://raw.githubusercontent.com/y-tetsu/reversi/images/simulator_demo.gif" width="650px">](https://github.com/y-tetsu/reversi/blob/master/reversi/examples/04_reversi_simulator.py)

---
## GUIアプリケーションの説明
### メニュー一覧
ゲームで選べるメニューの一覧です。<br>

 |名前|内容|
 |:---|:---|
 |Size |盤面のサイズ(4～26までの偶数)を選択します。 |
 |Black |黒(先手)のプレイヤーを選択します。 |
 |White |白(後手)のプレイヤーを選択します。 |
 |Cputime |CPUの持ち時間を設定します。デフォルトは0.5秒となっております。 |
 |Extra |外部プログラムのAIを追加します。Cputimeの持ち時間の設定は適用されません。 |
 |Assist |打てる手の候補をハイライト表示するかどうか選びます。 |
 |Language |言語設定を選びます。 |
 |Cancel |ゲームを中断します。 |

### プレイヤー紹介
選択可能なプレイヤーの一覧です。<br>
難易度は8x8サイズの場合の目安となっております。<br>

 |名前|特徴|難易度|
 |:---|:---|:---:|
 |User1, User2 |人が操作します。 | ？ |
 |Unselfish |なるべく少なく取ろうとします。 | ★ |
 |Random |ランダムに手を選びます。 | ★ |
 |Greedy |なるべく多く取ろうとします。 | ★ |
 |SlowStarter |残り手数が15%未満の場合はUnselfish、15%以上の場合はGreedyになります。 | ★ |
 |Table |マス目の位置に重みをつけたテーブルで盤面を評価し、自身の形勢が良くなるよう手を選びます。なるべく少なく取り、角を狙い、角のそばは避けるよう心掛けます。 | ★★ |
 |MonteCarlo |モンテカルロ法で手を選びます。持ち時間の限り、すべての手の候補についてゲーム終了までランダムな手を打ちあうプレイアウトを繰り返し、最も勝率が高かった手を選びます。| ★★ |
 |MinMax |ミニマックス法で2手先を読んで手を選びます。Tableの盤面評価に加えて、着手可能数と勝敗を考慮します。自身の置ける場所は増やし、相手の置ける場所は減らし、勝ちが見えた手を優先するよう手を読みます。 | ★★ |
 |NegaMax |MinMaxの探索手法をネガマックス法に替えて、持ち時間の限り3手先を読んで手を選びます。手を読む探索効率はミニマックス法と同じです。 | ★★★ |
 |AlphaBeta |NegaMaxの探索手法をアルファベータ法(ネガアルファ法)に替えて、持ち時間の限り4手先を読んで手を選びます。αβ値の枝刈りにより、ネガマックス法より効率良く手を読みます。 | ★★★ |
 |Joseki |AlphaBetaに加えて、序盤は定石通りに手を選びます。| ★★★ |
 |FullReading |Josekiに加えて、終盤残り9手からは最終局面までの石差を読んで手を選びます。| ★★★ |
 |Iterative |FullReadingに反復深化法を適用して持ち時間の限り徐々に深く手を読みます。読む手の深さを増やす際は前回の深さで最も評価が高かった手を最初に調べます。それにより、不要な探索を枝刈りしやすくし、4手よりも深く手を読む場合があります。| ★★★★ |
 |Edge |Iterativeの盤面評価に加えて、4辺のパターンを考慮し確定石を増やすよう手を選びます。| ★★★★ |

### プレイヤー追加機能
#### 概要
本プログラム(**reversi**)はお好きなプログラミング言語で作成したAI(追加プレイヤー)を<br>
ゲームに参加させて遊ぶことができます。<br>
また、あらかじめ用意された追加プレイヤーについても動作環境を準備する事で遊ぶ事ができます。<br>
なお、追加プレイヤーのプログラムを作成する際は入出力を後述のフォーマットに準拠させて下さい。<br>

#### 追加プレイヤー紹介
あらかじめ用意された追加プレイヤーの一覧です。<br>
動作環境を準備し、Extraメニューより登録ファイルを読み込ませると遊べるようになります。

 |名前|特徴|難易度|登録ファイル|開発言語|動作確認環境|
 |:---|:---|:---:|:---:|:---:|:---|
 |TopLeft |打てる手の中から一番上の左端を選びます。 | ★ | topleft.json | Python |Windows10 64bit<br>[Python 3.7.6](https://www.python.org/downloads/release/python-376/) |
 |BottomRight |打てる手の中から一番下の右端を選びます。 | ★ | bottomright.json | Perl |Windows10 64bit<br>[Strawberry Perl 5.30.1.1](http://strawberryperl.com/) |
 |RandomCorner |角が取れる時は必ず取ります。それ以外はランダムに手を選びます。 | ★ | randomcorner.json | VBScript |Windows10 64bit |

#### プレイヤー作成手順
プレイヤーを自作して遊ぶには、下記の手順でプレイヤーの作成と登録を行って下さい。

1. お好きなプログラミング言語の実行環境を準備する
2. [追加プレイヤー](#追加プレイヤーの実行)のプログラムを書く
3. [登録ファイル](#登録ファイル)を作成する
4. **reversi**を起動する
5. Extraメニューより登録ファイルを読み込ませる

![extra](https://raw.githubusercontent.com/y-tetsu/reversi/images/extra_ja.gif)

##### 追加プレイヤーの実行
追加プレイヤーを**reversi**に登録すると外部プログラムとして実行されるようになります。<br>
以下に処理の流れを示します。

![external](https://raw.githubusercontent.com/y-tetsu/reversi/images/external_ja.png)

1. ゲーム開始後、追加プレイヤーの手番になると**reversi**は対応するプログラムのコマンドを実行します。<br>その際、標準入力に盤面情報を渡し、追加プレイヤーのプログラムの応答を待ちます。

2. 追加プレイヤーは標準入力から盤面情報を受け取り、次の手を決め、その結果を標準出力します。<br>(そのようなプログラムを書いて下さい)

3. **reversi**は追加プレイヤーの標準出力(次の手)を受け取るとゲームを再開します。<br>一定時間応答がない場合は追加プレイヤーのプログラムを強制終了し、反則負けとして扱います。

##### 標準入力フォーマット
追加プレイヤーが受け取る標準入力の盤面の情報です。
```
手番の色(黒:1、白:-1)
盤面のサイズ(4～26までの偶数)
盤面の石の2次元配置(空き:0、黒:1、白:-1をスペース区切り)
```

下記に白の手番、盤面サイズ8x8の例を示します。<br>
![stdin](https://raw.githubusercontent.com/y-tetsu/reversi/images/stdin.png)
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

##### 標準出力フォーマット
追加プレイヤーが標準出力する次の手の情報です。
```
盤面の座標(左上を起点(0,0)としてxとyをスペース区切り)
```

下記にc5へ打つ場合の例を示します。<br>
![stdout](https://raw.githubusercontent.com/y-tetsu/reversi/images/stdout.png)
```
2 4
```

##### 登録ファイル
追加プレイヤーを**reversi**に登録するために本ファイルを作成する必要があります。<br>
登録ファイルは下記のフォーマット(JSON形式)に従って`extra/`以下に作成して下さい。<br>
作成後、Extraメニューより読み込む事でプレイヤーが追加されます。
```
{
    "name": "追加プレイヤーの名前",
    "cmd": "追加プレイヤー実行用のコマンド",
    "timeouttime": 追加プレイヤーからの応答待ち時間(秒) ※起動に時間がかかる場合があるため、余裕を持った設定を推奨します
}
```

下記に、Windows10上のPythonで動作するTopLeft(あらかじめ用意されたプレイヤー)の例を示します。
```
{
    "name": "TopLeft",
    "cmd": "py -3.7 ./extra/python/topleft/topleft.py",
    "timeouttime": 60
}
```

---
## インストールがうまくいかない場合
**reversi**のインストールがうまくいかない場合は
下記の手順(1～5)に従って環境を準備して下さい。

### 1. Pythonのインストール
下記よりPythonの64bit版インストーラのexeをダウンロード後、インストールして下さい。<br>
[Python 3.7.6](https://www.python.org/downloads/release/python-376/)<br>

インストール後、コマンドプロンプトを立ち上げて下記の'$'以降を入力してEnterを押し、同じ結果が出ればOKです。
```
$ py -3.7 --version
Python 3.7.6
```

### 2. pipの更新
**reversi**をPythonから実行するためにはいくつかの外部パッケージが必要となります。<br>
正しくインストールできるようにするために下記を実行してpipをアップデートして下さい。<br>
```
$ py -3.7 -m pip install --upgrade pip
 :
Successfully installed pip-20.0.2
```
※バージョンが異なる場合は上位であれば問題ないはずです

### 3. 関連パッケージのインストール
**reversi**の実行に必要なPythonのパッケージのインストールは下記で一括して行えます。<br>
事前にコマンドプロンプトにてreversiフォルダ以下に移動しておいてください。<br>
```
$ py -3.7 -m pip install -r requirements.txt
```
もしうまくいかない場合は、以降の"(パッケージインストールの補足)"を個別に実行してください。

### 4. Visual C++のインストール
本プログラムの実行にはC言語のコンパイル環境が必要となります。<br>
下記よりVisual C++をダウンロードして下さい。<br>
[Microsoft Visual C++ 2019](https://visualstudio.microsoft.com/downloads/?utm_medium=microsoft&utm_source=docs.microsoft.com&utm_campaign=button+cta&utm_content=download+vs2019+rc)<br>

### 5. reversiの実行
上記までの環境を準備した後、コマンドプロンプトにてexamplesフォルダ以下に移動し下記を実行すると**reversi**が起動します。
```
$ py -3.7 gui_app.py
```

### (パッケージインストールの補足)
#### cythonパッケージのインストール
**reversi**を実行するためにはcythonという外部パッケージが必要となります。<br>
下記を実行してインストールして下さい。
```
$ py -3.7 -m pip install cython
 :
Successfully installed cython-0.29.15
```

#### numpyパッケージのインストール
**reversi**を実行するためにはnumpyという外部パッケージが必要となります。<br>
下記を実行してインストールして下さい。
```
$ py -3.7 -m pip install numpy
 :
Successfully installed numpy-1.18.1
```

#### pyinstallerパッケージのインストール
**reversi**のexeを生成するためにはpyinstallerという外部パッケージが必要となります。<br>
下記を実行してインストールして下さい。不要な場合は省略しても構いません。
```
$ py -3.7 -m pip install pyinstaller
 :
Successfully installed altgraph-0.17 future-0.18.2 pefile-2019.4.18 pyinstaller-3.6 pywin32-ctypes-0.2.0
```

うまくいかない場合は下記を実行後に、再度上記を試してみて下さい。
```
$ py -3.7 -m pip install wheel
```

インストール完了後、pyinstallerを実行できるようにするために環境変数に下記を追加して下さい。
```
C:\Users\{あなたのユーザ名}\AppData\Local\Programs\Python\Python37\Scripts
```

---
## 参考書籍
- 「実践Python3」 Mark Summerfield著 斎藤 康毅訳 株式会社オライリー・ジャパン [ISBN978-4-87311-739-3](https://www.oreilly.co.jp/books/9784873117393/)
- 「Java言語で学ぶデザインパターン入門」 結城 浩著 ソフトバンククリエイティブ株式会社 [ISBN4-7973-2703-0](https://www.hyuki.com/dp/)
- 「日経ソフトウェア2019年11月号」 日経BP [ISSN1347-4685](https://books.google.co.jp/books?id=qhCxDwAAQBAJ&pg=PA146&lpg=PA146&dq=ISSN1347-4685&source=bl&ots=_3Z0k4Y_WE&sig=ACfU3U1urxBdw_srrg62Kr5UJD1sXLEQbQ&hl=ja&sa=X&ved=2ahUKEwjlkqzArY_nAhVTc3AKHXlBA6YQ6AEwAHoECAkQAQ#v=onepage&q=ISSN1347-4685&f=false)
- 「Python計算機科学新教本」 David Kopec著 黒川 利明訳 株式会社オライリー・ジャパン [ISBN978-4-87311-881-9](https://www.oreilly.co.jp/books/9784873118819/)

## 参考サイト
- 「オセロ・リバーシプログラミング講座 ～勝ち方・考え方～」https://uguisu.skr.jp/othello/
- 「オセロ･リバーシの勝ち方、必勝法」https://bassy84.net/
- 「強いオセロプログラムの内部動作」http://www.amy.hi-ho.ne.jp/okuhara/howtoj.htm
- 「オセロAI入門」https://qiita.com/na-o-ys/items/10d894635c2a6c07ac70
