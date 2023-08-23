/**
 *     dMMMMMP dMP     dMP dMMMMMMP .aMMMb  .aMMMb 
 *    dMP     dMP     amr    dMP   dMP"dMP dMP"VMP 
 *   dMMMP   dMP     dMP    dMP   dMMMMMP dMP      
 *  dMP     dMP     dMP    dMP   dMP dMP dMP.aMP   
 * dMMMMMP dMMMMMP dMP    dMP   dMP dMP  VMMMP"    
 * -------------------------------------------------
 * - Tactile Display Software
 * - Example UPD client application 
 * 
 * - For question or more information: www.elitac.nl
 * 
 * - Version 1.0
 * - 02/09/13
 */

package Tactile_example_UDP;

import java.awt.EventQueue;
import java.awt.event.ActionListener;
import java.awt.event.ActionEvent;
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.awt.Color;
import javax.swing.JFrame;
import javax.swing.JFormattedTextField;
import javax.swing.JButton;
import javax.swing.JFileChooser;
import javax.swing.JPanel;
import javax.swing.JTextPane;
import javax.swing.Timer;
import javax.swing.UnsupportedLookAndFeelException;
import javax.swing.border.TitledBorder;
import javax.swing.JSpinner;
import javax.swing.SpinnerNumberModel;
import javax.swing.UIManager;
import javax.swing.JComboBox;
import javax.swing.SwingConstants;

import net.miginfocom.swing.MigLayout;

import java.io.*;
import java.net.*;
import java.util.Arrays;
import java.util.Vector;

public class Tactile_example_UDP {

	private JFrame frmTactileExampleUsing;
	private boolean udp_connected = false;
	private DatagramSocket clientSocket;
	private int udpPort = 0;
	private String udpIP = "127.0.0.1";
	private String Selected_File_Name = null;
	Vector<String> comboBoxItems = new Vector<String>();
	int delayCounter = 0;
	
	/**
	 * 
	 * Launch the Tactile Example application.
	 * 
	 * This application uses the UPD connection of the UDP Tactile Server to 
	 * establish a connection between this client example and the Tactile Display
	 * 
	 * This application is only written as an example and a quick start.
	 * 
	 */
	
	public static void main(String[] args) {
		EventQueue.invokeLater(new Runnable() {
			public void run() {
				try {
					Tactile_example_UDP window = new Tactile_example_UDP();
					window.frmTactileExampleUsing.setVisible(true);
				} catch (Exception e) {
					e.printStackTrace();
				}
			}
		});
	}

	/**
	 * Create the application.
	 */
	public Tactile_example_UDP() {
		try {
			UIManager.setLookAndFeel(UIManager.getCrossPlatformLookAndFeelClassName());
		} catch (ClassNotFoundException | InstantiationException
				| IllegalAccessException | UnsupportedLookAndFeelException e) {
			e.printStackTrace();
		}
		initialize();
	}

	/**
	 * Initialize the contents of the frame.
	 */
	private void initialize() {
		frmTactileExampleUsing = new JFrame();
		frmTactileExampleUsing.setTitle("Tactile Example using UDP");
		frmTactileExampleUsing.setBounds(100, 100, 479, 560);
		frmTactileExampleUsing.setDefaultCloseOperation(JFrame.DO_NOTHING_ON_CLOSE);
		//frmTactileExampleUsing.dispatchEvent(new WindowEvent(frmTactileExampleUsing, WindowEvent.WINDOW_CLOSING));
		frmTactileExampleUsing.addWindowListener( new WindowAdapter() {
			public void windowClosing(WindowEvent e){
				System.out.println("Exiting...");
				frmTactileExampleUsing.dispose();
				closeUdpConnection();
				System.exit(0);
			}
		});
		frmTactileExampleUsing.getContentPane().setLayout(new MigLayout("fill", "[grow]", "[25%][25%][25%][25%]"));
		
		//Create a file chooser
		final JFileChooser fc = new JFileChooser();
		fc.setFileSelectionMode(JFileChooser.FILES_ONLY);  
		
		JPanel panel = new JPanel();
		panel.setBorder(new TitledBorder(null, "Load & Play file", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		frmTactileExampleUsing.getContentPane().add(panel, "cell 0 0,growx,aligny center");
		panel.setLayout(new MigLayout("fill", "[grow][]", "[23px,grow][20px][23px]"));
		
		JComboBox<String> comboBox = new JComboBox<String>(comboBoxItems);
		panel.add(comboBox, "cell 0 0,growx");
		comboBoxItems.add("test5");
		comboBoxItems.remove(0);		
		comboBox.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				System.out.println("Box selected!");
				@SuppressWarnings("unchecked")
				JComboBox<String> jcmbType = (JComboBox<String>) e.getSource();
				Selected_File_Name = (String) jcmbType.getSelectedItem();
				System.out.println(Selected_File_Name);
			}
		});		
		
		final JTextPane txtpnNoFileLoaded = new JTextPane();
		txtpnNoFileLoaded.setBackground(UIManager.getColor("ComboBox.background"));
		txtpnNoFileLoaded.setText("- No file loaded - ");
		txtpnNoFileLoaded.setEditable(false);
		panel.add(txtpnNoFileLoaded, "cell 0 1,alignx center,growy");

		
		final JButton btnStop = new JButton("Stop");
		btnStop.setEnabled(false);
		panel.add(btnStop, "cell 1 0,alignx center,aligny center");
		btnStop.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
					String awnser = sendUDP("!stop");
					System.out.println("Stopped all actions: " + awnser);
			}
		});
						
		final JButton btnPlay = new JButton("Play");
		btnPlay.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent arg0) {
				// If a file is selected
				if(!Selected_File_Name.isEmpty()){
					// Give server the action to perform the selected pattern
					String awnser = sendUDP("!PlayPattern," + Selected_File_Name);
					System.out.println("Got length: " + awnser);
									
				}
			}
		});
		panel.add(btnPlay, "cell 1 1,alignx center,aligny center");
		
		JPanel panel_1 = new JPanel();
		panel_1.setBorder(new TitledBorder(null, "Information", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		frmTactileExampleUsing.getContentPane().add(panel_1, "cell 0 1,growx,aligny center");
		panel_1.setLayout(new MigLayout("fill", "[40%][60%]", "[grow][grow][grow][grow]"));
		
		JTextPane txtpnFirmwareVersion = new JTextPane();
		txtpnFirmwareVersion.setEditable(false);
		txtpnFirmwareVersion.setText("Firmware version");
		panel_1.add(txtpnFirmwareVersion, "cell 0 0,grow");
		
		final JTextPane textPane_2 = new JTextPane();
		textPane_2.setText("-");
		textPane_2.setEditable(false);
		panel_1.add(textPane_2, "cell 1 0,grow");
		
		JTextPane txtpnBattery = new JTextPane();
		txtpnBattery.setEditable(false);
		txtpnBattery.setText("Battery (%)");
		panel_1.add(txtpnBattery, "cell 0 1,grow");
		
		final JTextPane textPane_6 = new JTextPane();
		textPane_6.setText("-");
		textPane_6.setEditable(false);
		panel_1.add(textPane_6, "cell 1 1,grow");
		
		JTextPane txtpnVoltage = new JTextPane();
		txtpnVoltage.setText("Voltage");
		txtpnVoltage.setEditable(false);
		panel_1.add(txtpnVoltage, "cell 0 2,grow");
		
		final JTextPane txtpnVoltage_value = new JTextPane();
		txtpnVoltage_value.setText("-");
		txtpnVoltage_value.setEditable(false);
		panel_1.add(txtpnVoltage_value, "cell 1 2,grow");
		
		JTextPane txtpnConnectionTypeport = new JTextPane();
		txtpnConnectionTypeport.setEditable(false);
		txtpnConnectionTypeport.setText("Hardware version");
		panel_1.add(txtpnConnectionTypeport, "cell 0 3,grow");
		
		final JTextPane txtHardware_Version = new JTextPane();
		txtHardware_Version.setText("-");
		txtHardware_Version.setEditable(false);
		panel_1.add(txtHardware_Version, "cell 1 3,grow");
		
		JPanel panel_2 = new JPanel();
		panel_2.setBorder(new TitledBorder(null, "UDP Settings", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		frmTactileExampleUsing.getContentPane().add(panel_2, "cell 0 2,growx,aligny center");
		panel_2.setLayout(new MigLayout("fill", "[15%][30%][25%][30%]", "[23px,grow][grow]"));
		
		JTextPane txtpnPort = new JTextPane();
		txtpnPort.setEditable(false);
		txtpnPort.setBackground(UIManager.getColor("ComboBox.background"));
		txtpnPort.setText("Port:");
		panel_2.add(txtpnPort, "cell 0 0,alignx left,aligny center");
		
		final JSpinner udp_port_nr = new JSpinner();
		udp_port_nr.setModel(new SpinnerNumberModel(new Integer(50000), null, null, new Integer(1)));
		panel_2.add(udp_port_nr, "cell 1 0,growx,aligny center");
		udpPort = (int) udp_port_nr.getValue();
		
		JTextPane txtpnIp = new JTextPane();
		txtpnIp.setEditable(false);
		txtpnIp.setBackground(UIManager.getColor("ComboBox.background"));
		txtpnIp.setText("IP:");
		panel_2.add(txtpnIp, "cell 0 1,alignx left,aligny center");
		
		final JFormattedTextField udp_ip_nr = new JFormattedTextField();
		udp_ip_nr.setHorizontalAlignment(SwingConstants.CENTER);
		udp_ip_nr.setText("127.0.0.1");
		panel_2.add(udp_ip_nr, "cell 1 1,growx,aligny center");
		
		final JTextPane upd_status_txt = new JTextPane();
		upd_status_txt.setEditable(false);
		
		JPanel panel_3 = new JPanel();
		panel_3.setBorder(new TitledBorder(null, "Status", TitledBorder.LEADING, TitledBorder.TOP, null, null));
		frmTactileExampleUsing.getContentPane().add(panel_3, "cell 0 3,growx,aligny center");
		panel_3.setLayout(new MigLayout("fill", "[40%,grow][60%,grow]", "[20px,grow][grow][grow]"));
		
		JTextPane txtpnConnected = new JTextPane();
		txtpnConnected.setEditable(false);
		txtpnConnected.setBackground(UIManager.getColor("Label.background"));
		panel_3.add(txtpnConnected, "cell 0 0,alignx left,growy");
		txtpnConnected.setForeground(Color.BLACK);
		txtpnConnected.setText("UDP Connected: ");
		
		final JTextPane txtpnNotConnected = new JTextPane();
		txtpnNotConnected.setEditable(false);
		txtpnNotConnected.setBackground(UIManager.getColor("RadioButton.background"));
		txtpnNotConnected.setForeground(Color.RED);
		txtpnNotConnected.setText("Not connected");
		panel_3.add(txtpnNotConnected, "cell 1 2,alignx left,aligny center");
		
		final JButton btnConnect = new JButton("Connect");
		btnConnect.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				if(!udp_connected){				
					String test = new String (udpConnect(udp_ip_nr.getText(), (int) udp_port_nr.getValue()));
					if (test.toLowerCase().trim().equals("null")){
						udp_connected = false;
						upd_status_txt.setText("Not connected");
						upd_status_txt.setForeground(Color.RED);
					}else if (test.toLowerCase().trim().equals("timeout")){
						udp_connected = false;
						upd_status_txt.setText("Not connected (TimeOut)");
						upd_status_txt.setForeground(Color.RED);
					}else{
						// Connected through the UPD port.
						// Display info for multiple items
						// Enable and update buttons
						udp_connected = true;
						upd_status_txt.setText("Connected  -  " + test);
						upd_status_txt.setForeground(new Color(0, 128, 0));
						btnPlay.setEnabled(true);
						btnStop.setEnabled(true);
						udp_port_nr.setEnabled(false);
						udp_ip_nr.setEnabled(false);
						btnConnect.setText("Disconnect");
						
						// update the Connection status. 
						txtpnNotConnected.setForeground(Color.BLACK);
						txtpnNotConnected.setText(sendUDP("?isConnected"));
						
						udpPort = (int) udp_port_nr.getValue();
						udpIP = udp_ip_nr.getText().trim();
						
						// get Files loaded on server side
						populateDropdownBox();
					}
				} else {
					udp_connected = false;
					btnConnect.setText("Connect");
					udp_port_nr.setEnabled(true);
					udp_ip_nr.setEnabled(true);
					upd_status_txt.setText("Not connected");
					upd_status_txt.setForeground(Color.RED);
					closeUdpConnection();
				}
			}
		});
		
		panel_2.add(btnConnect, "cell 3 1,alignx right,aligny top");

		upd_status_txt.setBackground(UIManager.getColor("Label.background"));
		upd_status_txt.setText("Not connected");
		upd_status_txt.setForeground(Color.RED);
		panel_3.add(upd_status_txt, "cell 1 0,alignx left,growy");
		
		JTextPane txtpnUdpLatency = new JTextPane();
		txtpnUdpLatency.setEditable(false);
		txtpnUdpLatency.setBackground(UIManager.getColor("RadioButton.background"));
		txtpnUdpLatency.setText("UDP Latency:");
		panel_3.add(txtpnUdpLatency, "cell 0 1,grow");
		
		final JTextPane UDP_Latency_ms = new JTextPane();
		UDP_Latency_ms.setEditable(false);
		UDP_Latency_ms.setBackground(UIManager.getColor("RadioButton.background"));
		UDP_Latency_ms.setText("- ms");
		panel_3.add(UDP_Latency_ms, "cell 1 1,grow");
		
		JTextPane txtpnTactileConnected = new JTextPane();
		txtpnTactileConnected.setEditable(false);
		txtpnTactileConnected.setBackground(UIManager.getColor("RadioButton.background"));
		txtpnTactileConnected.setText("Tactile Connected:");
		panel_3.add(txtpnTactileConnected, "cell 0 2,alignx left,aligny center");
		
		// Create a timer
		// update handler
		ActionListener timedUpdater = new ActionListener() {
			public void actionPerformed(ActionEvent evt) {
					checkSerialConnected();
					if (udp_connected){
						// Update latency to the UDP server
						UDP_Latency_ms.setText(checkLatency() + " ms");
						// Update Battery status 
						textPane_6.setText(getBattery());
						textPane_2.setText(getFirmware());
						txtpnVoltage_value.setText(getVoltage());
						txtHardware_Version.setText(getHardware());

					} else {
						UDP_Latency_ms.setText("- ms");
						txtpnNotConnected.setForeground(Color.RED);
						txtpnNotConnected.setText("Not connected");
						btnPlay.setEnabled(false);
						btnStop.setEnabled(false);
						udp_port_nr.setEnabled(true);
						udp_ip_nr.setEnabled(true);
					}
			}
		};
		
		// start timer
		new Timer(1000, timedUpdater).start();
		
	}
	
	
	private void populateDropdownBox() {
		// check if connected with UDP ...
		if (udp_connected) {
			comboBoxItems.clear();
			String timeStamp = sendUDP("?getPatterns");
			String[] timeStamp1 = timeStamp.split(",");
			System.out.println("Dropdown Box popolated with: ");
			System.out.println(Arrays.toString(timeStamp1));
			for (int i = 0; i < timeStamp1.length; i++) {
				// check if the current pattern isn't empty
				if(!timeStamp1[i].isEmpty()) {
					comboBoxItems.add(timeStamp1[i]);
				}
			}
			System.out.println("........................");
		}
	}
	
	
	private String getFirmware() {
		return sendUDP("?GetFirmwareVersion");		
	}

	
	private String getBattery() {
		return sendUDP("?GetBatteryStatus");		
	}	
	
	private String getHardware() {
		return sendUDP("?GetHardwareVersion");
	}
	
	private String getVoltage() {
		return sendUDP("?GetBatteryVoltage");
	}
	
	// Try to make a UDP connection 
	private String udpConnect(String ip, int port){
		String teststring = "?getServerVersion";
		String modifiedSentence = "null";		
		try {
			clientSocket = new DatagramSocket( );
			clientSocket.setSoTimeout(500);
			InetAddress IPAddress = InetAddress.getByName(ip);
			
			byte[] receiveData = new byte[2048];
			byte[] sendData = teststring.trim().getBytes();
			
			DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, port);
			
			clientSocket.send(sendPacket);
			DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);
		//	System.out.println("x");
			try {
				clientSocket.receive(receivePacket);
				modifiedSentence = new String(receivePacket.getData());
				modifiedSentence = modifiedSentence.substring(0, receivePacket.getLength());
				modifiedSentence = modifiedSentence.split(",")[1];
			} catch (SocketTimeoutException e) {
				modifiedSentence = "timeOut";
			}
			udpIP = ip;
			clientSocket.close();
		} catch (SocketException e) {
			return modifiedSentence;
		} catch (UnknownHostException e) {
			return modifiedSentence;
		} catch (IOException e) {
			return modifiedSentence;
		}
		return modifiedSentence;
	}
	
	
	private String sendUDP(String command){
		String awnser = " ";
		if (udp_connected){
			byte[] receiveData = new byte[2048];
			try {
				clientSocket = new DatagramSocket();
				clientSocket.setSoTimeout(1000);
			} catch (SocketException e2) {
				e2.printStackTrace();
			}

			try {
				InetAddress IPAddress = InetAddress.getByName(udpIP);
				// Send command
				byte[] sendData = command.trim().getBytes();
				DatagramPacket sendPacket = new DatagramPacket(sendData, sendData.length, IPAddress, udpPort);
				clientSocket.send(sendPacket);
			} catch (UnknownHostException e1) {
				e1.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
			DatagramPacket receivePacket = new DatagramPacket(receiveData, receiveData.length);

			try {
				clientSocket.receive(receivePacket);
				awnser = new String(receivePacket.getData());
				awnser = awnser.substring(0,receivePacket.getLength());
			} catch (SocketTimeoutException e) {
				awnser = "timeOut";
			} catch (IOException e) {
				System.out.println("UDP error");
			}
		}
		clientSocket.close();
		// remove first argument
		return awnser.substring(awnser.indexOf(",") + 1, awnser.length());
	}
	
	// Check Latency between client and UPD server.
	// This is only needed if the server runs on a different computer
	// as the client. Long latency means the Tactile Display will not update instantly.
	// Latency is only displayed. No actions are taken with this value.
	private String checkLatency(){
		long latency = -1L;
		if(udp_connected){
			// send "!Time"
			String timeStamp = sendUDP("!Time," + System.currentTimeMillis());
			if(timeStamp != "timeOut"){
				latency =  System.currentTimeMillis() - Long.parseLong(timeStamp.trim());
			}
			// limit to zero
			if (latency <= 0){
				latency = 0L;
			}
		}
		return String.valueOf(latency);
	}
	
	// Check if a serial connection to the tactile display exists. 
	private String checkSerialConnected(){
		String serialConnected = " ";
		if(udp_connected){
			serialConnected = sendUDP("?isConnected");
		}
		return serialConnected;
	}
	
	// Close an open UDP connection socket
	private void closeUdpConnection(){
		try {
			clientSocket.close();
		} catch (Exception e) {
			System.out.println("No open connection");
		}
	}
}
