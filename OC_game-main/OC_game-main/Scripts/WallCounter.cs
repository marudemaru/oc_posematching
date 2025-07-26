using UnityEngine;
using TMPro; // TextMeshProを扱うために必要

public class WallCounter : MonoBehaviour
{
    public static int count;
    // Inspectorから設定するUIテキスト
    public TextMeshProUGUI wallCount;

    // 毎フレーム呼ばれる
    void Update()
    {
        count = Wall_Generater.generatedCount - 1;
        // scoreTextが設定されていなければ何もしない
        if (wallCount == null)
        {
            return;
        }

        // Collisionスクリプトのcount変数をテキストに表示する
        // "static"な変数なので、直接「クラス名.変数名」でアクセスできる
        wallCount.text = "Wall: " + count + "/10";
    }
}
