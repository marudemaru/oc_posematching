using System.Collections;
using System.Collections.Generic;
using Unity.VisualScripting.ReorderableList;
using UnityEngine;

public class Moving_Wall : MonoBehaviour
{
    public Wall_Generater generator;
    public float speed = 50.0f; //????

    private void Update()
    {
        Vector3 direction = new Vector3(0f, 0f, -1f);
        transform.Translate(direction * speed * Time.deltaTime, Space.World);

        if (transform.position.z < -30f)
        {
            generator.GenerateWall();
            Destroy(this.gameObject);
        }
    }

}
