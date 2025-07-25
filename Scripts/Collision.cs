using UnityEngine;
using System.Collections;

public class Collision : MonoBehaviour
{
    public static int count;

    // 現在、壁に接触しているかどうかを管理するフラグ
    private static bool _isContactingWall = false;


    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        count = 0;
    }

    void OnTriggerEnter(Collider other)
    {
        // 衝突したオブジェクトが壁であるか判定
        // タグで判定する場合
        if (!_isContactingWall && other.gameObject.CompareTag("Wall"))
        {
            // ここに壁に当たっている間の処理を記述
            // 例: プレイヤーの移動速度を制限する、エフェクトを再生する
            count++;
            _isContactingWall = true;
            Debug.Log("壁に当たっている！ 回数" + count);
        }
    }

    // 衝突が終了した（オブジェクトが離れた）瞬間に呼ばれる
    void OnTriggerExit(Collider other)
    {
        // 「離れた相手が'Wall'」である場合
        if (other.gameObject.CompareTag("Wall"))
        {
            StartCoroutine(ResetContactFlagWithDelay());
        }
    }
    private IEnumerator ResetContactFlagWithDelay()
    {
        // 物理演算のフレームの終わりに実行することで、1フレーム内の連続ヒットを防ぐ
        yield return new WaitForSeconds(0.5f);

        // 壁から離れたので、フラグをリセットする
        _isContactingWall = false;

        Debug.Log("壁から離れました。次の衝突判定が可能です。");
        
    }
}
