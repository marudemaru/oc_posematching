using UnityEngine;

public class BoneConnector : MonoBehaviour
{
    public Transform jointA; // 始点関節(例えば肩)
    public Transform jointB; // 終点関節(例えば肘)

    void Update()
    {
        if (jointA == null || jointB == null) return;

        // 2点の真ん中に配置
        Vector3 posA = jointA.position;
        Vector3 posB = jointB.position;
        transform.position = (posA + posB) / 2f;

        // 円柱の向きをA→Bへ向ける
        Vector3 dir = posB - posA;
        transform.up = dir.normalized;

        // 円柱の長さ（yスケール）を2点間距離に合わせる
        Vector3 scale = transform.localScale;
        scale.y = dir.magnitude / 2f; // Cylinderの原点が中心なので半分
        transform.localScale = scale;
    }
}
