//using System.Collections;
//using System.Collections.Generic;
//using Unity.VisualScripting;
//using UnityEngine;

//public class Wall_Generater : MonoBehaviour
//{
//    public GameObject[] CubePrefabs;
//    public StartManager manager;
//    private float time;
//    private int number;

//    //If(!gameStarted) return;

//     void Start()
//      {
//        //GenerateWall();
//      }
//    //public void GameStart()
//    //{
//    //    GenerateWall();
//    //}

//    public void GenerateWall()
//    {
//        number = Random.Range(0, CubePrefabs.Length);
//        GameObject wall = Instantiate(CubePrefabs[number], new Vector3(0, 10, 20), Quaternion.identity);

//        Moving_Wall wallscript = wall.GetComponent<Moving_Wall>();
//        if (wallscript != null)
//        {
//            wallscript.generator = this;
//        }
//        //wall.GetComponent<Moving_Wall>().generater = this;
//    }
//}
using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.SceneManagement;

public class Wall_Generater : MonoBehaviour
{
    public GameObject[] CubePrefabs;
    public StartManager manager;
    private int number;

    public static int generatedCount = 1;

    void Start()
    {
        //GenerateWall(); // Start????????
        // StartManager?????????????????
    }

    public void GenerateWall()
    {

        if (generatedCount > 10)
        {
            SceneManager.LoadScene("ResultScene");
        }
        if (CubePrefabs == null || CubePrefabs.Length == 0)
        {
            Debug.LogWarning("CubePrefabs???????????");
            return;
        }

        number = Random.Range(0, CubePrefabs.Length);
        GameObject wall = Instantiate(CubePrefabs[number], new Vector3(0, 10, 20), Quaternion.identity);

        Moving_Wall wallscript = wall.GetComponent<Moving_Wall>();
        if (wallscript != null)
        {
            wallscript.generator = this;
        }
        generatedCount++;
    }
}