using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class GameManager : MonoBehaviour
{
    public GameObject[] CubePrefabs; //作成したprefabを格納する配列を生成
    private float time; //オブジェクトを生成する時間の設定
    private int number; //オブジェクト番号の設定

    void Start()
    {
        WallGenerater();
    }

    public void WallGenerater()
    {
        number = Random.Range(0, CubePrefabs.Length);
        GameObject wall = Instantiate(CubePrefabs[number], new Vector3(0, 10, 20), Quaternion.identity);

        Movingwall wallscript = wall.GetComponent<Movingwall>();
        if (wallscript != null)
        {
            wallscript.generator = this;
        }
    }
}
