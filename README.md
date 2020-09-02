# 遺伝的アルゴリズムを使ったSwitchのパラメータ検討

## switch_t
### 目的
Tableパラメータ(corner, c, a1, a2, b, o, x)をより強くするパラメータ値を求める。
かつゲームの進行に合わせて5段階に切り替える。

### 条件
ランダムなパラメータ値の個体から開始し、既存パラメータの個体と1手読み同士で対戦させ勝率の高いものを次の世代に入れ替える。

```JSON
{
    "max_generations": 1000,
    "population_num": 24,
    "offspring_num": 12,
    "mutation_chance": 0.1,
    "mutation_value": 6,
    "large_mutation": 100,
    "large_mutation_value": 25,
    "turns": [12, 24, 36, 48, 60],
    "board_size": 8,
    "matches": 250,
    "threshold": 85,
    "random_opening": 6,
    "processes": 2
}
```

### 結果
3回目の試行の1500世代あたりで79%程度の勝率となる個体が現れたが
複数手を読む戦略にパラメータを適用したところ弱くなったため中断。<br>

![switch_t](https://raw.githubusercontent.com/y-tetsu/reversi/images/switch_t.png)

## switch2_tw
### 目的
Tableパラメータ(corner, c, a1, a2, b, o, x)+勝敗パラメータ(ww)をより強くするパラメータ値を求める。
かつゲームの進行に合わせて5段階に切り替える。

### 条件
ランダムなパラメータ値の個体から開始し、既存パラメータの個体と2手読み同士で対戦させ勝率の高いものを次の世代に入れ替える。

```JSON
{
    "max_generations": 200,
    "population_num": 24,
    "offspring_num": 12,
    "mutation_chance": 0.1,
    "mutation_value": 6,
    "large_mutation": 100,
    "large_mutation_value": 25,
    "turns": [12, 24, 36, 48, 60],
    "board_size": 8,
    "matches": 100,
    "threshold": 85,
    "random_opening": 8,
    "processes": 2
}
```

### 結果
200世代ほど繰り返すも勝率が20%からあがる気配がなく中断。<br>

![switch2_tw](https://raw.githubusercontent.com/y-tetsu/reversi/images/switch2_tw.png)

## switch2f9j_tpwe(1)
### 目的
Tableパラメータ(corner, c, a1, a2, b1, b2, b3, x, o1, o2)+着手可能数パラメータ(wp)+勝敗パラメータ(ww)+エッジパラメータ(we)をより強くするパラメータ値を求める。
かつゲームの進行に合わせて5段階に切り替える。
定石打ちと終盤石差読み(残り9手)も適用する。

### 条件
1. ランダムなパラメータ値の個体から開始し、既存パラメータの個体と2手読み同士で対戦させ勝率の高いものを次の世代に入れ替える。
2. 1.を200世代進める。
3. 2.を6回分用意する。
4. 6回分の結果から勝率の割合に応じて12個体選び、これを6回分用意する。
5. 4.を200世代進める。
6. 4～5を繰り返す。

```JSON
{
    "max_generations": 200,
    "population_num": 12,
    "offspring_num": 6,
    "mutation_chance": 0.1,
    "mutation_value": 6,
    "large_mutation": 100,
    "large_mutation_value": 25,
    "turns": [12, 24, 36, 48, 60],
    "board_size": 8,
    "matches": 50,
    "threshold": 80,
    "random_opening": 8,
    "processes": 2
}
```

### 結果
1200世代分ほど繰り返すも勝率が40%程度からあがる気配がなく中断。<br>

![switch2f9j_tpwe1](https://raw.githubusercontent.com/y-tetsu/reversi/images/switch2f9j_tpwe1.png)

## switch2f9j_tpwe(2)
### 目的
Tableパラメータ(corner, c, a1, a2, b1, b2, b3, x, o1, o2)+着手可能数パラメータ(wp)+勝敗パラメータ(ww)+エッジパラメータ(we)をより強くするパラメータ値を求める。
かつゲームの進行に合わせて5段階に切り替える。
定石打ちと終盤石差読み(残り9手)も適用する。

### 条件
既存のパラメータ値の個体から開始し、既存パラメータの個体と2手読み同士で対戦させ勝率の高いものを次の世代に入れ替える。

```JSON
{
    "max_generations": 200,
    "population_num": 24,
    "offspring_num": 12,
    "mutation_chance": 0.3,
    "mutation_value": 3,
    "large_mutation": 50,
    "large_mutation_value": 10,
    "turns": [12, 24, 36, 48, 60],
    "board_size": 8,
    "matches": 300,
    "threshold": 80,
    "random_opening": 8,
    "processes": 2
}
```

### 結果
200世代ほどから勝率60%を超える個体が現れ、複数手読みの戦略にパラメータを適用しても既存より強かったため採用。<br>

![switch2f9j_tpwe2](https://raw.githubusercontent.com/y-tetsu/reversi/images/switch2f9j_tpwe2.png)
