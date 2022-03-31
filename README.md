# AIVoiceCtrl
A.I.VOICE EditorをPythonから読み上げ、ボイスプリセットの変更を行うスクリプト

## Requirement
- Windows10
- A.I.VOICE Editor Version 1.3.0.0
- Python 3.9.7
  - pythonnet 3.0.0.dev1

## Quick Start
```bash
cd aivoiceCtrl
python AIVoiceCtrl.py 読み上げテスト
```

## Usage
```python
from aivoiceCtrl import AIVoiceCtrl

# オブジェクト生成
avc = AIVoiceCtrl()
# デバッグ出力したい場合はdebug=True
#avc = AIVoiceCtrl(debug=True)

# vpNamesのボイスプリセット名を取得し、設定
avc.change_voicepreset(avc.vpName[0])

# 読み上げ
avc.playTalk(f"読み上げテスト {avc.vpName[0]}")

# 終了する場合はAIVoiceCtrlのオブジェクトを破棄すればデストラクタで後始末される
del avc
```
