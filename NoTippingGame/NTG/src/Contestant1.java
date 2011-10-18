import java.io.BufferedReader;
import java.io.InputStreamReader;

/**
 * 
 */

/**
 * @author ting
 *
 */
public class Contestant1 extends NoTippingPlayer {
	Contestant1(int port) {
		super(port);
		
	}

	private static BufferedReader br;
	
	private String add(String command){
		try {
			return br.readLine();
		} catch (Exception ev) {
			System.out.println(ev.getMessage());
		}
		return "";
	}
	
	protected String process(String command) {
		System.out.println(command);
		System.out.println("Enter move (position weight): ");
		String move = add(command);
		return move;			
	}

	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		Contestant1 con = new Contestant1(Integer.parseInt(args[0]));
		
	}
}
