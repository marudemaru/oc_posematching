using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class Movingwall : MonoBehaviour
{
    //public wallgenerater generator;
    public GameManager generator; //GameManagerのインスタンスを参照するための変数
    public float speed = 50.0f; //速度の設定

    void Update()
    {
        Vector3 direction = new Vector3(0f, 0f, -1f);
        transform.Translate(direction * speed * Time.deltaTime, Space.World); //ワールド座標で表す

        if (transform.position.z < -15f)
        {
            generator.WallGenerater(); //z座標が-10を下回ったら壁を生成
            Destroy(this.gameObject); //z座標が-10を下回ったらオブジェクトを削除
        }

    }
}