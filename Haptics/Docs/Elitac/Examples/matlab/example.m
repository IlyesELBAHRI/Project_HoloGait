% This script shows how to control the Elitac tactile hardware
% This function calls java methods.
% Make sure that the PORTNUMBER corresponds with the port number in the
% tactile server and that it is running and connected with the Elitac hardware
% This example shows a selection of UDP messages that the Elitac hardware
% understands. For the full list, please consult the manual.
PORTNUMBER=50000;
TIMEOUT=1000;
ADDRESS='localhost';
MAXPACKETLENGTH=2048;

%% setup UDP connection
import java.io.*
import java.net.DatagramSocket
import java.net.DatagramPacket
import java.net.InetAddress
socket = DatagramSocket; % create UDP socket
socket.setReuseAddress(0);
socket.setSoTimeout(TIMEOUT); % reception of UDP package times out after TIMEOUT ms.
socket.setBroadcast(0);
socket.setSendBufferSize(MAXPACKETLENGTH);
socket.setReceiveBufferSize(MAXPACKETLENGTH);

try
    %% check if tactile display is connected
    sndmssg='?IsConnected';
    packet = DatagramPacket(int8(sndmssg), length(sndmssg), InetAddress.getByName(ADDRESS), PORTNUMBER); % make datagram package for sending
    socket.send(packet); % send message
    fprintf(1,'sent: %s\n',sndmssg);
    packet = DatagramPacket(zeros(1,MAXPACKETLENGTH,'int8'),MAXPACKETLENGTH); % make datagram package for receiving
    socket.receive(packet);
    mssg = packet.getData;
    mssg = char(mssg(1:packet.getLength));
    fprintf(1,'received: %s\n', char(mssg));

    %% get tactile patterns
    sndmssg='?GetPatterns';
    packet = DatagramPacket(int8(sndmssg), length(sndmssg), InetAddress.getByName(ADDRESS), PORTNUMBER); % make datagram package for sending
    socket.send(packet); % send message
    fprintf(1,'sent: %s\n',sndmssg);
    packet = DatagramPacket(zeros(1,MAXPACKETLENGTH,'int8'),MAXPACKETLENGTH); % make datagram package for receiving
    socket.receive(packet);
    mssg = packet.getData;
    mssg = char(mssg(1:packet.getLength));
    fprintf(1,'received: %s\n', char(mssg));
    
    %% play tactile pattern
    sndmssg='!PlayPattern,test_one_by_one';
    packet = DatagramPacket(int8(sndmssg), length(sndmssg), InetAddress.getByName(ADDRESS), PORTNUMBER); % make datagram package for sending
    socket.send(packet); % send message
    fprintf(1,'sent: %s\n',sndmssg);
    packet = DatagramPacket(zeros(1,MAXPACKETLENGTH,'int8'),MAXPACKETLENGTH); % make datagram package for receiving
    socket.receive(packet);
    mssg = packet.getData;
    mssg = char(mssg(1:packet.getLength));
    fprintf(1,'received: %s\n', char(mssg));

    %% close socket
    socket.close;

catch ME
    socket.close;
    rethrow(ME);
end



