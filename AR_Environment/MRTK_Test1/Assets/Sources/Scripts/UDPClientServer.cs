using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.Net;
using System.Net.Sockets;
using System.Text;

public class UDPClientServer : MonoBehaviour
{
    public static UDPClientServer Instance;
    private UdpClient udpClient;
    private IPEndPoint pcEndPoint;
    private const int PORT_HOLOLENS = 8080;

    void Awake()
    {
        Instance = this;
    }
    private void Start()
    {
        // Creation of the UDP client and start listening
        udpClient = new UdpClient(PORT_HOLOLENS);
        Debug.Log("UDP client created on port " + PORT_HOLOLENS);
        Debug.Log("Waiting for messages...");
        udpClient.BeginReceive(ReceiveCallback, null);
        Debug.Log("UDP client started listening");
    }

    private void ReceiveCallback(System.IAsyncResult ar)
    {
        Debug.Log("Message received");
        // Reception of data from the PC 
        IPEndPoint remoteEndPoint = new IPEndPoint(IPAddress.Any, 0);

        pcEndPoint = remoteEndPoint;
        byte[] receivedData = udpClient.EndReceive(ar, ref remoteEndPoint);

        // show the IP address and port number from which the message was sent
        Debug.Log("Message received from " + remoteEndPoint.Address.ToString() + " : " +remoteEndPoint.Port.ToString());

        //  Convert the data to a string
        string message = Encoding.ASCII.GetString(receivedData);
        Debug.Log("Message reçu : " + message);
        EyeTrackingManager.Instance.command = message;

        // Restart listening
        udpClient.BeginReceive(ReceiveCallback, null);
    }
    public void udpClose(){
        // Close the UDP client when the application is closed
        udpClient.Close();
    }
    void OnApplicationQuit(){
        // Close the UDP client when the application is closed
        udpClient.Close();
    }
}
