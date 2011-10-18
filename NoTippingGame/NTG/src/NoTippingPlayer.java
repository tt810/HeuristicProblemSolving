/**
 * 
 */


import java.net.ServerSocket;
import java.net.Socket;
import java.io.*;

/**
 * Created by IntelliJ IDEA.
 * User: Sri Prasad Tadimalla
 * Date: Sep 24, 2003
 * Time: 2:32:35 PM
 * This class is the skeleton which much be modified to be run as a player
 */
public abstract class NoTippingPlayer {

    /**
     * Pass the port with which you registered yourselves
     * @param port
     */
    NoTippingPlayer(int port) {
        ServerSocket server = null;
        Socket socket = null;
        PrintWriter out = null;
        BufferedReader in = null;
        try {
            server = new ServerSocket(port);
            socket = server.accept();
            socket.setTcpNoDelay(true);
            out = new PrintWriter(socket.getOutputStream(), true);
            in = new BufferedReader(new InputStreamReader(socket.getInputStream()));

        } catch (IOException ev) {
            System.err.println(ev.getMessage());
        }
        String command;
        StringBuffer state = new StringBuffer();
        try {
            while ((command = in.readLine())!= null) {
                if (command.equals("STATE END")) {
                    out.println(process(state.toString()));
                    state.delete(0, state.length());
                    continue;
                }
                state.append(command+"\n");
            }
        }
        catch (IOException io) {
            System.err.println(io.getMessage());
        }
        out.close();
        try {
            in.close();
            socket.close();
            server.close();
        } catch (IOException io) {
            System.err.println(io.getMessage());
        }
    }

    /**
     * This function must be overridden to process each command that is recieved from the
     * client
     * @param command
     * @return
     */
    protected abstract String process(String command);

}
