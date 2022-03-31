from time import sleep
import clr
import os
import sys

from cv2 import resize

class AIVoiceCtrl:
    def __init__(self, debug: bool = False) -> None:
        self.retained_text = ""
        self.__debug = debug
        self.__vpNames = []
        self.__init_aivoice()
    
    def __del__(self):
        try:
            self.__ttsControl.Disconnect()
            self.__debug_print(f"AIVOICEの接続を終了しました。")
        except Exception as e:
            print(f"AIVOICEへの接続終了処理失敗: {e}")
    
    @property
    def vpName(self) -> list[str]:
        """
        ボイスプリセット名を取得
        """
        return self.__vpNames

    def __init_aivoice(self) -> None:
        """
        AIVOICEのAPI初期化処理
        """
        # dllがあるかチェック
        _editor_dir = os.environ['ProgramW6432'] + '\\AI\\AIVoice\\AIVoiceEditor\\'
        if not os.path.isfile(_editor_dir + 'AI.Talk.Editor.Api.dll'):
            print("A.I.VOICE Editor (v1.3.0以降) がインストールされていません。")
            exit()
        
        # pythonnet DLLの読み込み
        clr.AddReference(_editor_dir + "AI.Talk.Editor.Api")
        from AI.Talk.Editor.Api import TtsControl, HostStatus
        self.__ttsControl = TtsControl()
        self.__HostStatus = HostStatus

        host = self.__ttsControl.GetAvailableHostNames()
        if len(host) == 0:
            print("接続可能なAIVOICEが存在しません。")
            exit()
        
        try:
            # APIを初期化する
            self.__ttsControl.Initialize(host[0])
        except Exception as e:
            print(f"APIの初期化に失敗: {e}")
            exit()

        try:
            if self.__ttsControl.Status == self.__HostStatus.NotRunning:
                # AIVOICEが起動していなければ起動する
                self.__ttsControl.StartHost()
            
            # AIVOICEに接続
            self.__ttsControl.Connect()

            self.__debug_print(f"AIVOICEへの接続が完了しました。 Ver.{self.__ttsControl.Version}")
        except Exception as e:
            print(f"AIVOICEへの接続に失敗: {e}")
            exit()

        # 登録されているボイスプリセット名を取得
        for vp in self.__ttsControl.VoicePresetNames:
            self.__vpNames.append(vp)

    def change_voicepreset(self, name: str):
        """
        ボイスプリセットを変更
        """
        self.__ttsControl.CurrentVoicePresetName = name
        
    def playTalk(self, text: str):
        """
        AIVOICEにテキストを読み上げ
        """
        if self.__ttsControl.Status == self.__HostStatus.Busy:
            # 処理中であれば一旦停止
            self.__ttsControl.Stop()
        elif not self.__ttsControl.Status == self.__HostStatus.Idle:
            print("AIVOICEに再接続します。")
            self.__init_aivoice()

        # 現在のテキストを保持
        self.retained_text = self.__ttsControl.Text
        # テキストをセット
        self.__ttsControl.Text = text
        self.__ttsControl.SelectionStart = 0
        # 再生時間取得
        playTime = (self.__ttsControl.GetPlayTime() / 1000) + 0.15
        self.__debug_print(f"読み上げ中... (再生時間: {playTime}秒)")
        # 再生
        self.__ttsControl.Play()
        # 読み上げが完了するまで処理を止める
        sleep(playTime)

        # 読み上げが完了しているかチェック
        if self.__ttsControl.Status == self.__HostStatus.Busy:
            self.__debug_print("取得した再生時間を超えても処理中の為、再度処理を一時停止します。")
            sleep(0.1)
            count = 0
            while self.__ttsControl.Status == self.__HostStatus.Busy:
                # 再度待つ
                sleep(0.1)
                count += 1
                if count == 50:
                    raise Exception("タイムアウトしました。読み上げが完了しません。")

        self.__debug_print("読み上げ完了")
        # テキストを元に戻す
        self.__ttsControl.Text = self.retained_text
    
    def __debug_print(self, msg: str):
        if self.__debug == True:
            print(msg)

def main():
    avc = AIVoiceCtrl(True)
    avc.playTalk(sys.argv[1])

if __name__ == '__main__':
    main()
