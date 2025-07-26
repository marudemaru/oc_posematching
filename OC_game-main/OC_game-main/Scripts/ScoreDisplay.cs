using UnityEngine;
using TMPro; // TextMeshProを扱うために必要

public class ScoreDisplay : MonoBehaviour
{
    // Inspectorから設定するUIテキスト
    public TextMeshProUGUI scoreText;

    // 毎フレーム呼ばれる
    void Update()
    {
        // scoreTextが設定されていなければ何もしない
        if (scoreText == null)
        {
            return;
        }

        // Collisionスクリプトのcount変数をテキストに表示する
        // "static"な変数なので、直接「クラス名.変数名」でアクセスできる
        scoreText.text = "Count: " + Collision.count;
    }
}
