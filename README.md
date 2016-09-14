# これは何

タイムアウト付き関数の実装テスト。テスト対象は以下のとおり

* Python 2.6.6 (CentOS 6)
* Python 2.7.12 (現行の 2.7系最新)
* Python 3.5.2 (現行の 3系最新)

諸事情で 2.6.6 から動作するかも見たかった。
結論としては、本範囲では何ら障害になるような話はない。


# 動作概要

デコレータ `@timeout(5)` がついた `run_with_timeout(100)` は要するに
`timeout(5)(run_with_timeout)(100)`と同じ。

実体は`new_function(100)`で、クロージャ内に `seconds=5` が含まれてるので、
肝心の`time_consuming_function()`が呼ばれる前に
`signal.setitimer(signal.ITIMER_REAL, 5)`でタイムアウト時に`SIGALRM`が送出される。
その直前の行で
`old = signal.signal(signal.SIGALRM, handler)`が実行されており`SIGALRM`の
ハンドラが登録されている。ここで`old`はそれ以前のシグナルハンドラ。
もし他のシグナルハンドラが事前に設定されていたら困るので、
実行終了後に復元する意味も込めて`signal.signal(signal.SIGALRM, old)`としている。
このあたりはトイプログラム実装ならば省略して良いと思う。


* http://docs.python.jp/2/library/signal.html
* http://docs.python.jp/3.5/library/signal.html

signalモジュールはPython 2系とPython 3系 (3.5.2 時点) で詳細部分で結構差がある様子。
ただ、本実装の範囲では同じように書ける。
