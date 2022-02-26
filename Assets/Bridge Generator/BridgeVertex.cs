using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class BridgeVertex : MonoBehaviour
{
    public int id;
    public string model;
    public List<BridgeEdge> edges;
    public List<BridgeVertex> neighborVertices;
    public BridgeGenerator bridgeBuilder;

    public List<GameObject> nearWaypoints;
    public List<GameObject> farWaypoints;


    private void Awake()
    {
        edges = new List<BridgeEdge>();
        neighborVertices = new List<BridgeVertex>();
        nearWaypoints = new List<GameObject>();
        farWaypoints = new List<GameObject>();
    }

    public Vector2 Get2DPos()
    {
        float x = transform.position.x;
        // y pos is the magnitude from top center of bridge
        float y = transform.position.z * (new Vector3(x, bridgeBuilder.bridgeHeight, 0) - transform.position).magnitude;
        Vector2 twoDPos = new Vector2(x, y);
        return twoDPos;
    }
}
