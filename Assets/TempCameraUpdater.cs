using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class TempCameraUpdater : MonoBehaviour
{
    public BridgeGenerator bg;
    public float timeBetweenUpdates = 10;
    public float timeRemaining = 0;
    public List<Vector3> positions;
    public int currentPos;

    public int resWidth = 2550;
    public int resHeight = 3300;

    private bool takeHiResShot = false;

    // Start is called before the first frame update
    void Start()
    {
        
    }

    // Update is called once per frame
    void Update()
    {
        timeRemaining -= Time.deltaTime;

        if (timeRemaining <= 0)
        {
            timeRemaining = timeBetweenUpdates;
            currentPos++;
            if (currentPos >= positions.Count)
            {
                currentPos = 0;
            }
            Camera.current.transform.position = positions[currentPos];
            Camera.current.transform.LookAt(new Vector3(0, 0, 0));
/*            ScreenCapture.CaptureScreenshot("SomeLevel");
            TakeHiResShot();*/

        }

    }

    public static string ScreenShotName(int width, int height)
    {
        return string.Format("{0}/screenshots/screen_{1}x{2}_{3}.png",
                             Application.dataPath,
                             width, height,
                             System.DateTime.Now.ToString("yyyy-MM-dd_HH-mm-ss"));
    }

    public void TakeHiResShot()
    {
        takeHiResShot = true;
    }

    void LateUpdate()
    {
        if (takeHiResShot)
        {
            RenderTexture rt = new RenderTexture(resWidth, resHeight, 24);
            Camera.current.targetTexture = rt;
            Texture2D screenShot = new Texture2D(resWidth, resHeight, TextureFormat.RGB24, false);
            Camera.current.Render();
            RenderTexture.active = rt;
            screenShot.ReadPixels(new Rect(0, 0, resWidth, resHeight), 0, 0);
            Camera.current.targetTexture = null;
            RenderTexture.active = null; // JC: added to avoid errors
            Destroy(rt);
            byte[] bytes = screenShot.EncodeToPNG();
            string filename = ScreenShotName(resWidth, resHeight);
            System.IO.File.WriteAllBytes(filename, bytes);
            Debug.Log(string.Format("Took screenshot to: {0}", filename));
            takeHiResShot = false;
        }
    }
}
