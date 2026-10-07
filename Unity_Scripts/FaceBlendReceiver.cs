using UnityEngine;
using System.IO.Ports; // シリアル通信を使うために必要

public class FaceBlendReceiver : MonoBehaviour
{
    [SerializeField] private Renderer targetRenderer;
    [SerializeField] private Texture2D[] faceTextures; // Lv01~Lv04の4枚

    [Header("[ Arduino Settings ]")]
    [SerializeField] private string portName = "COM4"; // Arduinoが接続されているポート名（※環境に合わせて変更）
    [SerializeField] private int baudRate = 9600;      // Arduino側の Serial.begin(9600); と合わせる

    // 0.0 (Lv01) ～ 3.0 (Lv04) まで連続して動く変数
    [Range(0f, 3f)] public float currentLevelProgress = 0f;

    private SerialPort serialPort;

    void Start()
    {
        // ゲーム開始時にシリアルポートを開く
        if (!string.IsNullOrEmpty(portName))
        {
            try
            {
                serialPort = new SerialPort(portName, baudRate);
                serialPort.ReadTimeout = 50; // 読み込み待ちでフリーズするのを防ぐ
                serialPort.Open();
                Debug.Log($"[Serial] {portName} を開きました。");
            }
            catch (System.Exception e)
            {
                Debug.LogError($"[Serial] ポートを開けませんでした: {e.Message}");
            }
        }
    }

    void Update()
    {
        // Arduinoからデータが届いているか確認
        if (serialPort != null && serialPort.IsOpen)
        {
            try
            {
                string message = serialPort.ReadLine(); // Arduinoから1行（Serial.println）読み込む

                // 届いたテキストを数値（float）に変換
                if (float.TryParse(message, out float sensorValue))
                {
                    // 【重要】Arduinoのセンサー値（例: 0 ～ 1023）を、Unityの進行度（0.0 ～ 3.0）に変換する
                    // ※お使いのセンサーの最小値・最大値に合わせて「0f, 1023f」の部分を調整してください
                    currentLevelProgress = Map(sensorValue, 400f, 900f, 0f, (float)(faceTextures.Length - 1));
                }
            }
            catch (System.TimeoutException)
            {
                // データが届いていない時間はタイムアウトしますが、無視して大丈夫です
            }
        }

        ApplyFaceBlend();
    }

    // 数値の範囲を変換する便利な関数（Arduinoの map関数 と同じ働きをします）
    private float Map(float value, float fromSource, float toSource, float fromTarget, float toTarget)
    {
        float result = (value - fromSource) / (toSource - fromSource) * (toTarget - fromTarget) + fromTarget;
        return Mathf.Clamp(result, fromTarget, toTarget); // 範囲を超えないように安全ガード
    }

    void OnDestroy()
    {
        // ゲーム終了時にポートを安全に閉じる
        if (serialPort != null && serialPort.IsOpen)
        {
            serialPort.Close();
            Debug.Log("[Serial] ポートを閉じました。");
        }
    }

    void ApplyFaceBlend()
    {
        if (targetRenderer == null || faceTextures == null || faceTextures.Length < 2) return;

        int indexA = Mathf.FloorToInt(currentLevelProgress);
        int indexB = Mathf.CeilToInt(currentLevelProgress);
        float blend = currentLevelProgress - indexA;

        indexA = Mathf.Clamp(indexA, 0, faceTextures.Length - 1);
        indexB = Mathf.Clamp(indexB, 0, faceTextures.Length - 1);

        Material mat = Application.isPlaying ? targetRenderer.material : targetRenderer.sharedMaterial;

        if (mat != null)
        {
            mat.SetTexture("_TextureA", faceTextures[indexA]);
            mat.SetTexture("_TextureB", faceTextures[indexB]);
            mat.SetFloat("_Blend", blend);
        }
    }
}
