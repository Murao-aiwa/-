図版元（構想図の作図元）
対象：提案資料 1ページ目（全体構想図）と 2ページ目（ナカニシ回転部の構想図）の画像部分。

・fig1.svg / fig2.svg … 構想図の本体（ベクター。Inkscape・Illustrator等で編集可）。文字は含まない。
・iso.py / fig1.py / fig2.py … SVGを生成するPythonスクリプト（立体風の模式図。寸法は実物と無関係）。
　再生成：python3 fig1.py fig1.svg ／ python3 fig2.py fig2.svg（ラベル位置用の *_anchors.json も出力）
・render.js … SVGをPNG化する補助スクリプト（Node.js＋Playwright）。
　例：node render.js "<絶対パス>/fig1.svg" fig1.png 2850 1250 1.2 ／ node render.js "<絶対パス>/fig2.svg" fig2.png 2850 1240 1.2

注意
・図中の部品名・番号・注記・凡例はPowerPoint側の図形（文字・引出線）で、PPTX上で直接編集できます。
・構想図は模式図です。IH-300の内部構造・接続ねじ・軸受・専用継手・取付寸法は表現しておらず、
　橙色の破線部（接続適合 要確認）と青破線の保持金具（形状・固定方法 未定）は未確認・未定の箇所です。
