using UnityEngine;
using UnityEngine.UI;

public class StartManager : MonoBehaviour
{
    public GameObject startCanvas; // ????????(Canvas)
    public RectTransform startButtonArea; // ???????????RectTransform
    public Transform rightWrist; // PoseReceiver???????????Transform
    public float requiredTime = 2.0f; // ???????

    public Wall_Generater wallGenerator; // ??????????
    public PoseReceiver poseReceiver;     // ???????????????

    private float timer = 0f;
    public static bool gameStarted = false;

    void Start()
    {
        // ????????????????
        if (startCanvas != null)
            startCanvas.SetActive(true);

        gameStarted = false;
    }

    void Update()
    {
        if (gameStarted) return;

        // ?????????????????
        Vector3 wristScreenPos = Camera.main.WorldToScreenPoint(rightWrist.position);

        // ??????????????
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
            startCanvas.SetActive(false); // ??????????

        // ???????????
        if (poseReceiver != null)
            poseReceiver.StartGame();

        // ???
        if (wallGenerator != null)
            wallGenerator.GenerateWall();
    }
}
