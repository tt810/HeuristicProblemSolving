import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.UnknownHostException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;

/**
 * 
 */

/**
 * @author ting
 *
 */
public class Client {
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
		System.out.println(info);
		String[] lines = info.split("\n");
		if(totalTurn == 0){
			totalTurn = Integer.parseInt(lines[1].split(" ")[2]);
			totalPlayer = Integer.parseInt(lines[2].split(" ")[2]);
			me = Integer.parseInt(lines[3].split(" ")[3]);
		}
		int playerScoresFrom = 0;
		int boardStateFrom = 0;
		int boardStateEnd = 0;
		for(int i=0; i<lines.length; i++){
			
			if(lines[i].equals("PLAYER SCORES")){
				System.out.println("****"+lines[i]+"*********");
				playerScoresFrom = i;
			}
			if(lines[i].equals("BOARD STATE")){
				System.out.println("****"+lines[i]+"*********");
				boardStateFrom = i + 1;
			}
			if(lines[i].equals("Enter new position \"X Y\":")){
				System.out.println("****"+lines[i]+"*********");
				boardStateEnd = i-1;
			}
		}
		
		if (boardStateFrom == boardStateEnd){ return "500 500";}
		Map<Integer, ArrayList<Position>> owners = new HashMap<Integer, ArrayList<Position>>();
		for (int i = boardStateFrom; i < boardStateEnd; i++){
			String[] playerInfo = lines[i].split(" ");
			double x = Integer.parseInt(playerInfo[1]);
			double y = Integer.parseInt(playerInfo[2]);
			Integer owner = Integer.parseInt(playerInfo[0].substring(0, playerInfo[0].length()-1));			
			if(owners.containsKey(owner)){
				owners.get(owner).add(new Position(x, y));
			}else{
				ArrayList<Position> pos = new ArrayList<Position>();
				pos.add(new Position(x, y));
				owners.put(owner, pos);
			}
		}
		System.out.println("now owners size: "+owners.size());
		Board board = new Board(owners, me);
		Position p = board.getresult();
		return p.toString();
	}
	
	public static void main(String[] args) {
		stdIn = new BufferedReader(new InputStreamReader(System.in));
		String host = "localhost";
		int port = Integer.parseInt(args[0]);
		Client client = new Client(host, port);
	}

}
