using UnityEngine;

public class Collision2 : MonoBehaviour
{
    // インスペクターから設定する効果音のオーディオクリップ
    public AudioClip pickupSound;
    // 効果音の音量
    [Range(0f, 1f)] // 0から1の範囲でスライダー表示
    public float soundVolume = 1.0f;


    // OnTriggerEnter: 何らかのColliderがこのトリガー領域に入ったときに一度だけ呼び出される
    void OnTriggerEnter(Collider other)
    {
        // 衝突した相手が「Player」タグを持っているか確認
        if (other.CompareTag("Wall"))
        {
            // 1. 効果音を鳴らす
            // PlayClipAtPointは、指定した位置でAudioClipを一度だけ再生する便利なメソッド
            // 再生後、自動的にAudioSourceオブジェクトが破棄される
            if (pickupSound != null)
            {
                // 音を鳴らす
                AudioSource.PlayClipAtPoint(pickupSound, transform.position, soundVolume);
            }
        }
    }
}
