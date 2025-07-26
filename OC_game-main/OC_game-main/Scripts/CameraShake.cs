using System.Collections;
using UnityEngine;

public class CameraShake : MonoBehaviour
{
    // 揺れの強さ
    public float shakeMagnitude = 5.0f;
    // 揺れる時間
    public float shakeDuration = 0.5f;

    // カメラの元の位置を保存する変数
    private Vector3 originalPosition;

    void Awake()
    {
        // カメラの元の位置をAwakeで保存しておく
        originalPosition = transform.localPosition;
    }

    // 外部から呼び出すための画面揺らし開始メソッド
    public void StartShake()
    {
        StartCoroutine(Shake());
    }

    // 画面を揺らすコルーチン
    IEnumerator Shake()
    {
        float elapsed = 0f; // 経過時間

        while (elapsed < shakeDuration)
        {
            // ランダムな方向に揺らすオフセットを計算
            // Random.insideUnitSphere は半径1の球内のランダムな点を返す
            Vector3 randomOffset = Random.insideUnitSphere * shakeMagnitude;

            // カメラの位置を元の位置 + オフセットに設定
            transform.localPosition = originalPosition + randomOffset;

            elapsed += Time.deltaTime; // 経過時間を更新

            yield return null; // 1フレーム待つ
        }

        // 揺れが終わったら元の位置に戻す
        transform.localPosition = originalPosition;
    }
}
