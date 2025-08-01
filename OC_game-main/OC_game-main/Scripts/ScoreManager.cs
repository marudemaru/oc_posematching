/*using System.Net.Sockets;
using UnityEngine;
using UnityEngine.UI;

public class ScoreManager : MonoBehaviour
{
   public int score = 0;
   //public Text scoreText; //UI?????????????????

   private void Start()
   {
       UpdateScoreText();
   }

   public void AddScore(int amount)
   {
       score += amount;
       UpdateScoreText();
   }

   void UpdateScoreText()
   {
       if(scoreText != null)
       {
           UpdateScoreText().text = "Score:" + score.ToString();
       }
   }

   public void ResetScore()
   {
       score = 0;
       UpdateScoreText();
   }

}
*/