import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.HashSet;
import java.util.Set;

/**
 * 
 */

/**
 * @author ting
 *
 */
public class Client {

	/**
	 * @param args
	 */
	private static BufferedReader stdIn;
	private static int totalTurn = 0;
	private static int totalPlayer;
	private static int me;
	private static int currentTurn = 0;
	
	public Client(String host, int port){
		Socket socket = null;
		PrintWriter out = null;
		BufferedReader in = null;
		
		try{
			socket = new Socket(host, port);
			out = new PrintWriter(socket.getOutputStream(), true);
			in = new BufferedReader(new InputStreamReader(
										socket.getInputStream()));
			
		}catch(UnknownHostException e){
			System.err.println("unknown host: "+host);
		}catch(IOException e){
			System.exit(1);
		}
		Character boardInfo;
		StringBuffer state = new StringBuffer();
		try{
			while((boardInfo = (char)in.read()) != null){
				state.append(boardInfo);
				if(state.toString().endsWith("\":")){
					out.println(process(state.append("\n").toString()));
					state.delete(0, state.length());
					continue;
				}
			}
			out.close();
			in.close();
			stdIn.close();
			socket.close();
		}catch(IOException e){
			
		}
	}
	private String process(String info){
		System.out.print(info);
		String[] lines = info.split("\n");
		if(totalTurn == 0){
			totalTurn = Integer.parseInt(lines[1].split(" ")[2]);
			totalPlayer = Integer.parseInt(lines[2].split(" ")[2]);
			me = Integer.parseInt(lines[3].split(" ")[3]);
		}
		
		float[] playerScores = new float[totalPlayer];
		for(int i=0; i<totalPlayer; i++){
			playerScores[i] = Integer.parseInt(lines[6+i].split(" ")[1]);
		}
		
		int boardState = totalPlayer * currentTurn + me;
		currentTurn++;
//		System.out.println(totalTurn + " *** "+totalPlayer + " **** "+
//							me + " ***** "+boardState);
		Set<Site> sites = new HashSet<Site>();
		Set<Point> sPoints = new HashSet<Point>();
//		for(int i=0; i<boardState; i++){
//			sites[i] = new Site();
//		}
		int from = 8+totalPlayer;
//		System.out.println("BoardState: "+boardState);
		for(int i=0; i<boardState; i++){
			String[] strs = lines[from+i].split(" ");
			Site site = new Site();
			site.p = new Point(Integer.parseInt(strs[1]),
					Integer.parseInt(strs[2])); 
			String owner = strs[0].substring(0, strs[0].length()-1);
			site.owner = Integer.parseInt(owner);
			sites.add(site);
			sPoints.add(site.p);
		}
		Board board = new Board(totalTurn*totalPlayer, me);
		board.sites = sites;
		board.sPoints = sPoints;
		for(Site site:sites){
			System.out.println(site.p);
		}
		if(boardState == (totalTurn*totalPlayer-1)) return board.beachyMove();
		return board.getMyStep();

	}
	public static void main(String[] args) {
		stdIn = new BufferedReader(new InputStreamReader(System.in));
		String host = args[0];
		int port = Integer.parseInt(args[1]);		
		Client client = new Client(host, port);
		
	}

}
