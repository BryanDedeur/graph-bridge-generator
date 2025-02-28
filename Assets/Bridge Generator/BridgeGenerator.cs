﻿using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using System.IO;
using System;
using SFB; // Standalone file browser package

// Bridge generator constructs verious bridges with various parameters

[Serializable]
public class BridgeGenerator : MonoBehaviour
{
    public bool arched = false;

    public GameObject defaultVertex;
    public GameObject defaultEdge;

    public float totalCost = 0;
    public List<BridgeVertex> vertices;
    public List<BridgeEdge> edges;

    public BridgeVertex deploymentVertex;

    // bridge generation variables
    public int numSegments = 4;
    public float segmentSpacing = 4;
    private float surfaceWidth = 4f;
    public float bridgeHeight = 7;
    public float bridgeLength = 0;
    public float bridgeWidth = 7.4f;
    private float trussWidth = 0.3f;
    
    [Serializable]
    public enum BridgeType {Pratt, Howe, Warren, KTruss};
    public BridgeType bridgeType = BridgeType.Pratt;

    public bool mirrorZ = true;
    public bool mirrorX = true;

    // private members variables
    public string bridgeName = "";
    public GameObject rootObject;

    public void Awake()
    {
        rootObject = new GameObject();
        rootObject.name = "Bridge";
        SetBridgeType(((int)bridgeType));
        Generate();
    }

    public void Clear()
    {
        foreach (BridgeVertex bv in vertices)
        {
            Destroy(bv.gameObject);
        }
        vertices.Clear();
        foreach (BridgeEdge be in edges)
        {
            Destroy(be.gameObject);
        }
        edges.Clear();
    }

    public void SaveToObj()
    {
        var path = StandaloneFileBrowser.SaveFilePanel("Save File", "", bridgeName, "obj");

        string output = "";
        foreach(BridgeVertex vertex in vertices)
        {
            Vector2 vec2 = vertex.Get2DPos();
            output += "v " + vec2.x + " " + vec2.y + " 0" + "\n";
        }
        File.WriteAllText(path, output);
    }
    public void LoadFromOBJ(string file_path)
    {
        StreamReader istream = new StreamReader(file_path);
        // todo verify files exists and all that jazz
        while (!istream.EndOfStream)
        {
            string ln = istream.ReadLine();
            string[] tokens = ln.Split(' ');
            if (tokens[0] == "v")
            {
                // todo verify tokens are all valid floats
                CreateVertex(new Vector3(float.Parse(tokens[1]), float.Parse(tokens[2]), float.Parse(tokens[3])));
            }
            else if (tokens[0] == "l")
            {
                // todo verify tokens are all valid floats
                CreateEdge(vertices[Convert.ToInt32(tokens[1]) - 1], vertices[Convert.ToInt32(tokens[2]) - 1]);
            }
        }

        istream.Close();
    }

    public void SetNumSegments(string segments)
    {
        numSegments = Int32.Parse(segments);
    }

    public void SetBridgeHeight(string height)
    {
        bridgeHeight = float.Parse(height);
    }

    public void SetBridgeWidth(string width)
    {
        surfaceWidth = float.Parse(width);
    }

    public void SetSegmentLength(string len)
    {
        segmentSpacing = float.Parse(len);
    }

    public float GetLength()
    {
        return bridgeLength;
    }

    public void SetBridgeType(int type)
    {
        switch(type)
        {
            case 0:
                bridgeType = BridgeType.Pratt;
                bridgeName = "pratt-l";
                break;
            case 1:
                bridgeType = BridgeType.Howe;
                bridgeName = "howe-l";
                break;
            case 2:
                bridgeType = BridgeType.Warren;
                bridgeName = "warren-l";
                break;
            case 3:
                bridgeType = BridgeType.KTruss;
                bridgeName = "ktruss-l";
                break;
        }
    }

    // ------------------------------------------- GENERATING BRIDGES ----------------------------------- //

    public void Generate()
    {
        numSegments = (int) Mathf.Ceil(numSegments / 2) * 2;
        surfaceWidth = bridgeWidth + trussWidth;
        bridgeLength = numSegments * segmentSpacing;

        // get positive z position on one side of road
        float zPos = surfaceWidth / 2.0f;

        // make prev vertices list to assist segment creation
        List<BridgeVertex> prevVertices = new List<BridgeVertex>();

        if (bridgeType == BridgeType.Warren)
        {
            // create starting triangle
            prevVertices.Add(CreateVertex(new Vector3(segmentSpacing /2.0f, 0, zPos), true, true));
            prevVertices.Add(CreateVertex(new Vector3(0, bridgeHeight, zPos), false, true));
            CreateEdge(prevVertices[0], prevVertices[1], true, true);
            CreateEdge(prevVertices[0], GetVertex(new Vector3(-segmentSpacing / 2.0f, 0, zPos)), false, true);
            // create top edge
            CreateEdge(GetVertex(new Vector3(0, bridgeHeight, -zPos)), prevVertices[1], false, true);
        }
        else
        {
            // create center vertical vertices and edge
            prevVertices.Add(CreateVertex(new Vector3(0, 0, zPos), false, true));
            prevVertices.Add(CreateVertex(new Vector3(0, bridgeHeight, zPos), false, true));
            CreateEdge(prevVertices[0], prevVertices[1], false, true);
            CreateEdge(GetVertex(new Vector3(0, bridgeHeight, -zPos)), prevVertices[1], false, true);
        }


        // make middle segments starting from the center out
        float xPos = segmentSpacing;
        float heightReduction = 0;
        //BridgeVertex prev_v2 = v2;
        int i;
        for (i = 1; i < numSegments / 2; ++i)
        {
            //prev_v2 = v2;
            switch(bridgeType) {
                case BridgeType.Pratt:
                    prevVertices = MakePrattSegement(prevVertices, xPos, zPos, bridgeHeight - heightReduction);
                    break;
                case BridgeType.Howe:
                    prevVertices = MakeHoweSegement(prevVertices, xPos, zPos, bridgeHeight - heightReduction);
                    break;
                case BridgeType.KTruss:
                    prevVertices = MakeKTrussSegement(prevVertices, xPos, zPos, bridgeHeight - heightReduction);
                    break;
                case BridgeType.Warren:
                    prevVertices = MakeWarrenSegement(prevVertices, i, xPos, zPos, bridgeHeight - heightReduction);
                    break;
            }
            //MakeUpperXSegment(v2, prev_v2, xPos, zPos);
            xPos += segmentSpacing;
            //heightReduction += (1 - Mathf.Cos(i / (float) Math.PI))/2.0f;
        }

        // make end segment
        BridgeVertex endv;
        if (bridgeType == BridgeType.Warren)
        {
            // add one more triangle
            prevVertices = MakeWarrenSegement(prevVertices, i, xPos, zPos, bridgeHeight - heightReduction);
            bridgeLength = (numSegments + 1) * segmentSpacing;
            //endv = CreateVertex(new Vector3(xPos - segmentSpacing / 2.0f, 0, zPos), true, true);
            endv = prevVertices[0];
        } else {
            endv = CreateVertex(new Vector3(xPos, 0, zPos), true, true);
            CreateEdge(prevVertices[0], endv, true, true);
            CreateEdge(prevVertices[1], endv, true, true);
        }


        deploymentVertex = endv;

    }

    public List<BridgeVertex> MakeHoweSegement(List<BridgeVertex> prev, float xPos, float zPos, float height)
    {
        // make vertices
        List<BridgeVertex> newV = new List<BridgeVertex>();
        newV.Add(CreateVertex(new Vector3(xPos, 0, zPos), true, true));
        newV.Add(CreateVertex(new Vector3(xPos, height, zPos), true, true));

        // horizontal
        CreateEdge(newV[0], prev[0], true, true);
        CreateEdge(newV[1], prev[1], true, true);
        // vertical
        CreateEdge(newV[0], newV[1], true, true);
        // diagonal
        CreateEdge(newV[0], prev[1], true, true);
        // top
        if (mirrorZ)
        {
            newV.Add(CreateVertex(new Vector3(xPos - segmentSpacing / 2.0f, newV[1].transform.position.y, 0), true, false));

            CreateEdge(newV[2], prev[1], true, true);
            CreateEdge(newV[2], newV[1], true, true);
            CreateEdge(GetVertex(new Vector3(xPos, newV[1].transform.position.y, -zPos)), newV[1], true, false);
        }


        return newV;
    }

    public List<BridgeVertex> MakePrattSegement(List<BridgeVertex> prev, float xPos, float zPos, float height)
    {
        // make vertices
        List<BridgeVertex> newV = new List<BridgeVertex>();
        newV.Add(CreateVertex(new Vector3(xPos, 0, zPos), true, true));
        newV.Add(CreateVertex(new Vector3(xPos, height, zPos), true, true));

        // horizontal
        CreateEdge(newV[0], prev[0], true, true);
        CreateEdge(newV[1], prev[1], true, true);
        // vertical
        CreateEdge(newV[0], newV[1], true, true);
        // diagonal
        CreateEdge(newV[1], prev[0], true, true);
        // top
        if (mirrorZ)
        {
            newV.Add(CreateVertex(new Vector3(xPos - segmentSpacing / 2.0f, newV[1].transform.position.y, 0), true, false));
            CreateEdge(newV[2], prev[1], true, true);
            CreateEdge(newV[2], newV[1], true, true);
            CreateEdge(GetVertex(new Vector3(xPos, newV[1].transform.position.y, -zPos)), newV[1], true, false);
        }

        return newV;
    }

    public List<BridgeVertex> MakeWarrenSegement(List<BridgeVertex> prev, int seg, float xPos, float zPos, float height)
    {
        // make vertices in a triangle
        List<BridgeVertex> newV = new List<BridgeVertex>();
        newV.Add(CreateVertex(new Vector3(xPos + segmentSpacing * .5f, 0, zPos), true, true));
        newV.Add(CreateVertex(new Vector3(xPos, height, zPos), true, true));
       
        // horizontal
        CreateEdge(newV[0], prev[0], true, true);
        CreateEdge(newV[1], prev[1], true, true);

        // diagonal
        CreateEdge(newV[1], prev[0], true, true);
        CreateEdge(newV[0], newV[1], true, true);

        // top
        if (mirrorZ)
        {
            newV.Add(CreateVertex(new Vector3(xPos - segmentSpacing * .5f, newV[1].transform.position.y, 0), true, false));

            CreateEdge(newV[2], newV[1], true, true);
            CreateEdge(newV[2], prev[1], true, true);
            CreateEdge(GetVertex(new Vector3(xPos, newV[1].transform.position.y, -zPos)), newV[1], true, false);
        }

        return newV;
    }

    public List<BridgeVertex> MakeKTrussSegement(List<BridgeVertex> prev, float xPos, float zPos, float height)
    {
        // make vertices
        List<BridgeVertex> newV = new List<BridgeVertex>();
        newV.Add(CreateVertex(new Vector3(xPos, 0, zPos), true, true));
        newV.Add(CreateVertex(new Vector3(xPos, height, zPos), true, true));
        newV.Add(CreateVertex(new Vector3(xPos, height / 2, zPos), true, true));

        // make edges along x axis
        // horizontal
        CreateEdge(newV[0], prev[0], true, true);
        CreateEdge(newV[1], prev[1], true, true);
        // vertical
        CreateEdge(newV[0], newV[2], true, true);
        CreateEdge(newV[1], newV[2], true, true);
        // diagonal
        CreateEdge(prev[0], newV[2], true, true);
        CreateEdge(prev[1], newV[2], true, true);

        // top
        if (mirrorZ)
        {
            newV.Add(CreateVertex(new Vector3(xPos - segmentSpacing / 2.0f, newV[1].transform.position.y, 0), true, false));
            CreateEdge(newV[3], prev[1], true, true);
            CreateEdge(newV[3], newV[1], true, true);
            CreateEdge(GetVertex(new Vector3(xPos, newV[1].transform.position.y, -zPos)), newV[1], true, false);
        }

        return newV;
    }

    public void MakeUpperXSegment(BridgeVertex new_v2, BridgeVertex prev_v2, float xPos, float zPos)
    {
        // create upper edges
        CreateEdge(GetVertex(new Vector3(xPos, new_v2.transform.position.y, -zPos)), new_v2, true, false);

        BridgeVertex centerv = CreateVertex(new Vector3(xPos - segmentSpacing / 2.0f, new_v2.transform.position.y, 0), true, false);
        CreateEdge(centerv, prev_v2, true, true);
        CreateEdge(centerv, new_v2, true, true);
    }


    // ------------------------------------------------- VERTICES --------------------------------------- //

    public BridgeVertex GetVertex(Vector3 coordinate)
    {
        foreach (BridgeVertex otherbv in vertices)
            if (otherbv.transform.position.x == coordinate.x && otherbv.transform.position.y == coordinate.y && otherbv.transform.position.z == coordinate.z)
                return otherbv;
        return null;
    }

    public BridgeVertex CreateVertex(Vector3 coordinate)
    {
        // make sure vertex does not already exist
        if (GetVertex(coordinate) != null)
            return null;

        // create vertex object
        GameObject go = Instantiate(defaultVertex);
        go.name = "V" + vertices.Count.ToString();
        go.transform.position = coordinate;
        go.transform.parent = rootObject.transform;

        // create vertex component
        BridgeVertex bv = go.AddComponent<BridgeVertex>();
        bv.bridgeBuilder = this;
        bv.id = vertices.Count;
        vertices.Add(bv);

        return bv;
    }

    // public methods
    public BridgeVertex CreateVertex(Vector3 coordinate, bool mirrorAlongX, bool mirrorAlongZ)
    {
        mirrorAlongX = mirrorAlongX && mirrorX;
        mirrorAlongZ = mirrorAlongZ && mirrorZ;

        // mirroring
        if (mirrorAlongX)
            CreateVertex(new Vector3(-coordinate.x, coordinate.y, coordinate.z));

        if (mirrorAlongZ)
            CreateVertex(new Vector3(coordinate.x, coordinate.y, -coordinate.z));

        if (mirrorAlongX && mirrorAlongZ)
            CreateVertex(new Vector3(-coordinate.x, coordinate.y, -coordinate.z));

        return CreateVertex(coordinate);
    }

    // ------------------------------------------------- EDGES --------------------------------------- //


    public BridgeEdge GetEdge(BridgeVertex vertex1, BridgeVertex vertex2)
    {
        foreach (BridgeEdge otherbe in edges)
            if ((otherbe.v1 == vertex1 && otherbe.v2 == vertex2) || (otherbe.v1 == vertex2 && otherbe.v2 == vertex1))
                return otherbe;
        return null;
    }

    public BridgeEdge CreateEdge(BridgeVertex vertex1, BridgeVertex vertex2)
    {
        if (vertex1 == null || vertex2 == null)
            return null;
        // check if edge exists
        if (GetEdge(vertex1, vertex2) != null)
            return null;

        // create edge object
        GameObject go = Instantiate(defaultEdge);
        go.name = "E" + edges.Count.ToString();
        go.transform.parent = rootObject.transform;
        Vector3 dir = (vertex2.transform.position - vertex1.transform.position);
        go.transform.position = vertex1.transform.position + (dir / 2);
        go.transform.LookAt(vertex2.transform);
        float length = dir.magnitude;
        go.transform.localScale = new Vector3(go.transform.localScale.x, go.transform.localScale.y, length);

        // create edge component
        BridgeEdge be = go.AddComponent<BridgeEdge>();
        be.bridgeBuilder = this;
        be.id = edges.Count;
        be.v1 = vertex1;
        be.v2 = vertex2;
        be.cost = length;
        edges.Add(be);
        totalCost += be.cost;

        // update vertices
        vertex1.edges.Add(be);
        vertex1.neighborVertices.Add(vertex2);

        vertex2.edges.Add(be);
        vertex2.neighborVertices.Add(vertex1);

        return be;
    }

    public BridgeEdge CreateEdge(BridgeVertex vertex1, BridgeVertex vertex2, bool mirrorAlongX, bool mirrorAlongZ)
    {
        mirrorAlongX = mirrorAlongX && mirrorX;
        mirrorAlongZ = mirrorAlongZ && mirrorZ;

        // mirroring
        if (mirrorAlongX)
        {
            BridgeVertex v1 = GetVertex(new Vector3(-vertex1.transform.position.x, vertex1.transform.position.y, vertex1.transform.position.z));
            BridgeVertex v2 = GetVertex(new Vector3(-vertex2.transform.position.x, vertex2.transform.position.y, vertex2.transform.position.z));
            if (v1 != null && v2 != null)
                CreateEdge(v1, v2);
            else
                print("must create vertices fist to mirror an edge");
        }

        if (mirrorAlongZ)
        {
            BridgeVertex v1 = GetVertex(new Vector3(vertex1.transform.position.x, vertex1.transform.position.y, -vertex1.transform.position.z));
            BridgeVertex v2 = GetVertex(new Vector3(vertex2.transform.position.x, vertex2.transform.position.y, -vertex2.transform.position.z));
            if (v1 != null && v2 != null)
                CreateEdge(v1, v2);
            else
                print("must create vertices fist to mirror an edge");
        }

        if (mirrorAlongX && mirrorAlongZ)
        {
            BridgeVertex v1 = GetVertex(new Vector3(-vertex1.transform.position.x, vertex1.transform.position.y, -vertex1.transform.position.z));
            BridgeVertex v2 = GetVertex(new Vector3(-vertex2.transform.position.x, vertex2.transform.position.y, -vertex2.transform.position.z));
            if (v1 != null && v2 != null)
                CreateEdge(v1, v2);
            else
                print("must create vertices fist to mirror an edge");
        }

        return CreateEdge(vertex1, vertex2);
    }
}
