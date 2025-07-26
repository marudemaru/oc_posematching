using UnityEngine;

public class WallCollisionDetector : MonoBehaviour
{
    // 画面揺らしのスクリプトへの参照
    // InspectorからメインカメラにアタッチされているCameraShakeスクリプトをドラッグ＆ドロップで設定
    public CameraShake cameraShake;

    void OnTriggerEnter(Collider other)
    {
        // 衝突した相手が「Wall」タグを持っているか確認
        if (other.CompareTag("Wall"))
        {
            // CameraShakeスクリプトが設定されていれば、揺らしを開始
            if (cameraShake != null)
            {
                cameraShake.StartShake();
            }
        }
    }
}
