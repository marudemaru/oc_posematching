using UnityEngine;
using UnityEngine.UI;

public class StartManager : MonoBehaviour
{
    public GameObject startCanvas; // スタート画面全体(Canvas)
    public RectTransform startButtonArea; // スタートボタンエリアのRectTransform
    public Transform rightWrist; // PoseReceiverで受信している右手首のTransform
    public float requiredTime = 2.0f; // 必要な滞在秒数

    public Wall_Generater wallGenerator; // 壁生成用のスクリプト
    public PoseReceiver poseReceiver;     // ポーズ合わせゲーム用スクリプト

    private float timer = 0f;
    public static bool gameStarted = false;

    void Start()
    {
        // ゲーム開始前はスタート画面を表示
        if (startCanvas != null)
            startCanvas.SetActive(true);

        gameStarted = false;
    }

    void Update()
    {
        if (gameStarted) return;

        // 右手のワールド座標→画面座標に変換
        Vector3 wristScreenPos = Camera.main.WorldToScreenPoint(rightWrist.position);

        // スタートボタンエリア内か判定
        if (RectTransformUtility.RectangleContainsScreenPoint(startButtonArea, wristScreenPos, null))
        {
            timer += Time.deltaTime;
            if (timer >= requiredTime)
            {
                StartGame();
            }
        }
        else
        {
            timer = 0f;
        }
    }

    void StartGame()
    {
        gameStarted = true;
        if (startCanvas != null)
            startCanvas.SetActive(false); // スタート画面を非表示

        // ポーズ合わせゲーム開始
        if (poseReceiver != null)
            poseReceiver.StartGame();

        // 壁生成
        if (wallGenerator != null)
            wallGenerator.GenerateWall();
    }
}
