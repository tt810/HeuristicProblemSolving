import java.io.InputStream;
import java.util.Properties;
import java.util.Enumeration;

/**
 * Created by IntelliJ IDEA.
 * User: prasad
 * Date: Sep 24, 2003
 * Time: 9:52:33 AM
 * Gets the list of players and their assigned port numbers
 */
public class Player {

    private static String filename = "PlayerInfo.txt";
    // A list of the players
    private static String[] playerNames;
    // A list of the player ports corresponding to the names above
    private static int[] playerPorts;
    private static boolean initialized = false;
    private static String hostname = "localhost";
    private static boolean noDelay = false;

    public static void initialize (String fileName) {
        Properties players = null;
        try {
            players = new Properties();
            InputStream stream = Player.class.getResourceAsStream((fileName==null)?filename:fileName);
            players.load(stream);
            stream.close();
        } catch (Exception ev) {
            System.out.println(ev.getMessage());
        }
        playerNames = new String[players.size()];
        playerPorts = new int[playerNames.length];
        Enumeration playerEnum = players.keys();
        int i = 0;
        String name;
        while (playerEnum.hasMoreElements()) {
            name = (String)playerEnum.nextElement();
            playerNames[i] = name;
            playerPorts[i] = Integer.parseInt(players.getProperty(name));
            i++;
        }
        initialized = true;
    }

    public static int getPort(String name) {
        if (!initialized)
            initialize(filename);
        for (int i=0; i<playerNames.length; i++)
             if (playerNames[i].equals(name))
                 return playerPorts[i];
        return -1;
    }

    public static String[] getPlayers() {
        if (!initialized)
            initialize(filename);
        return playerNames;
    }

    public static String getHostname() {
        if (!initialized)
            initialize(filename);
        return hostname;
    }

    public static void setProperties(NoTippingAppletStub noTippingAppletStub) {
        hostname = noTippingAppletStub.getParameter("hostname");
        String noDelayString = noTippingAppletStub.getParameter("nodelay");
        if (noDelayString != null && noDelayString.equals("true"))
            noDelay = true;
    }

    public static boolean noDelay() {
        return noDelay;
    }
}
