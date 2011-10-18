import java.applet.AppletStub;
import java.applet.Applet;
import java.applet.AppletContext;
import java.util.Hashtable;
import java.util.StringTokenizer;
import java.util.NoSuchElementException;
import java.net.InetAddress;
import java.net.UnknownHostException;

/**
 * Created by IntelliJ IDEA.
 * User: prasad
 * Date: Sep 30, 2003
 * Time: 10:55:32 PM
 */
public class NoTippingAppletStub implements AppletStub {
    private Hashtable _properties;
    private Applet _applet;

    /*
     * @param argv[] Command line arguments passed to Main
     * @param an Applet instance.
     */
    public NoTippingAppletStub (String argv[], Applet a) {
      _applet = a;
      _properties = new Hashtable();
      for ( int i = 0; i < argv.length; i++ ) {
        try {
          StringTokenizer parser =
           new StringTokenizer (
            argv[i], "=");
          String name = parser.nextToken(
                          ).toString();
          String value = parser.nextToken(
             "\"").toString();
          value = value.substring(1);
          _properties.put (name, value);
        } catch (NoSuchElementException e) {
          e.printStackTrace();
        }
      }
    }

    /**
     * Calls the applet's resize
     * @param width
     * @param height
     */
    public void appletResize (
       int width, int height) {
      _applet.resize (width, height);
    }

    /**
     * Returns the applet's context, which is
     * null in this case. This is an area where more
     * creative programming
     * work can be done to try and provide a context
     * @return AppletContext Always null
     */
    public AppletContext getAppletContext () {
      return null;
    }

    /**
     * Returns the CodeBase. If a host parameter
     * isn't provided
     * in the command line arguments, the URL is based
     * on InetAddress.getLocalHost().
     * The protocol is "file:"
     * @return URL
     */
    public java.net.URL getCodeBase() {
      String host;
      if ( (host=getParameter (
        "host")) == null ) {
        try {
          host = InetAddress.getLocalHost(
                          ).getHostName();
        } catch (UnknownHostException e) {
          e.printStackTrace();
        }
      }

      java.net.URL u  = null;
      try {
        u = new java.net.URL (
         "file://"+host);
      } catch (Exception e) { }
      return u;
    }

    /**
     * Returns getCodeBase
     * @return URL
     */
    public java.net.URL getDocumentBase() {
      return getCodeBase();
    }

    /**
     * Returns the corresponding command line value
     * @return String
     */
    public String getParameter (
                      String p) {
      return (String)_properties.get (p);
    }

    /**
     * Applet is always true
     * @return boolean True
     */
    public boolean isActive () {
      return true;
    }

}
