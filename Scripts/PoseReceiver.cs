using UnityEngine;
using WebSocketSharp;
using System.Collections.Generic;

public class PoseReceiver : MonoBehaviour
{
    [System.Serializable]
    public class JointSetting
    {
        public string jointName;
        public Transform jointObject;
    }

    public List<JointSetting> joints; // Inspectorで12個分設定

    private Dictionary<string, Transform> jointDict;
    private Dictionary<string, Vector3> basePositions;

    private WebSocket ws;

    private PoseDataWrapper latestPoseData = null;
    private readonly object poseLock = new object();

    void Start()
    {
        jointDict = new Dictionary<string, Transform>();
        basePositions = new Dictionary<string, Vector3>();

        foreach (var joint in joints)
        {
            jointDict[joint.jointName] = joint.jointObject;
            basePositions[joint.jointName] = joint.jointObject.position;
        }

        ws = new WebSocket("ws://localhost:3000/");

        ws.OnOpen += (sender, e) =>
        {
            Debug.Log("WebSocket Open");
        };
        ws.OnError += (sender, e) =>
        {
            Debug.LogError("WebSocket Error: " + e.Message);
        };
        ws.OnClose += (sender, e) =>
        {
            Debug.Log("WebSocket Close");
        };

        ws.OnMessage += (sender, e) =>
        {
            try
            {
                var poseData = JsonUtility.FromJson<PoseDataWrapper>(e.Data);
                lock (poseLock)
                {
                    latestPoseData = poseData;
                }
            }
            catch (System.Exception ex)
            {
                Debug.LogError("JSON parse error: " + ex.Message);
            }
        };

        ws.Connect();
    }

    void Update()
    {
        PoseDataWrapper poseData = null;
        lock (poseLock)
        {
            if (latestPoseData != null)
            {
                poseData = latestPoseData;
            }
        }
        if (poseData != null)
        {
            foreach (var joint in joints)
            {
                if (jointDict.TryGetValue(joint.jointName, out Transform obj))
                {
                    Vector3 offset = Vector3.zero;
                    switch (joint.jointName)
                    {
                        case "head":           offset = poseData.head.ToVector3(); break;
                        case "shoulder_left":  offset = poseData.shoulder_left.ToVector3(); break;
                        case "shoulder_right": offset = poseData.shoulder_right.ToVector3(); break;
                        case "elbow_left":     offset = poseData.elbow_left.ToVector3(); break;
                        case "elbow_right":    offset = poseData.elbow_right.ToVector3(); break;
                        case "wrist_left":     offset = poseData.wrist_left.ToVector3(); break;
                        case "wrist_right":    offset = poseData.wrist_right.ToVector3(); break;
                        case "pelvis":         offset = poseData.pelvis.ToVector3(); break;
                        case "knee_left":      offset = poseData.knee_left.ToVector3(); break;
                        case "knee_right":     offset = poseData.knee_right.ToVector3(); break;
                        case "ankle_left":     offset = poseData.ankle_left.ToVector3(); break;
                        case "ankle_right":    offset = poseData.ankle_right.ToVector3(); break;
                    }
                    // XY平面のみ移動（Zは初期値を維持）
                    Vector3 newPos = basePositions[joint.jointName];
                    newPos.x += offset.x;
                    newPos.y += offset.y;
                    // newPos.zは初期値のまま
                    obj.position = newPos;
                }
            }
        }
    }

    void OnDestroy()
    {
        if (ws != null)
        {
            ws.Close();
            ws = null;
        }
    }

    public void StartGame() // 追加: ゲーム開始時に呼ばれる
    {
        if (ws != null && !ws.IsAlive)
        {
            ws.Connect();
        }
    }

    [System.Serializable]
    public class Offset
    {
        public float x, y, z;
        public Vector3 ToVector3() => new Vector3(x, y, z);
    }

    [System.Serializable]
    public class PoseDataWrapper
    {
        public Offset head;
        public Offset shoulder_left;
        public Offset shoulder_right;
        public Offset elbow_left;
        public Offset elbow_right;
        public Offset wrist_left;
        public Offset wrist_right;
        public Offset pelvis;
        public Offset knee_left;
        public Offset knee_right;
        public Offset ankle_left;
        public Offset ankle_right;
    }
}
