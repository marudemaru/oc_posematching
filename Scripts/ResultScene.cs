using UnityEngine;
using TMPro;
using UnityEngine.SceneManagement;

public class ResultManager : MonoBehaviour
{
    public TMP_Text resultText;
    public TMP_Text hitText;
    public TMP_Text rankText;
    public GameObject returnButton;

    private float rightHandTouchTime = 0f;
    public float waitTime = 2f;

    private void Start()
    {
        resultText.text = "RESULT";
        hitText.text = "HIT: " + Collision.count.ToString();
        rankText.text = "RANK: " + GetRank(Collision.count);
        returnButton.SetActive(false);
    }

    private void Update()
    {
        if (IsRightHandTouchingButton())
        {
            rightHandTouchTime += Time.deltaTime;

            if (rightHandTouchTime >= waitTime)
            {
                returnButton.SetActive(true);
            }
        }
        else
        {
            rightHandTouchTime = 0f;
            returnButton.SetActive(false);
        }
    }
    string GetRank(int count)
    {
        if (count == 0) return "SSS";
        else if (count < 2) return "S";
        else if (count < 4) return "A";
        else if (count < 6) return "B";
        else if (count < 8) return "C";
        else return "D";
    }

    bool IsRightHandTouchingButton()
    {
        return false;
    }

    public void OnReturnButton()
    {
        Collision.count = 0; // Reset the count for the next game
        SceneManager.LoadScene("StartScene"); // Load the StartScene
    }
}