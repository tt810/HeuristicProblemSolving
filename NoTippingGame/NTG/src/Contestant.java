
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.Map;
import java.util.Random;
import java.util.TreeMap;


/**
 * 
 */
 


class Contestant extends NoTippingPlayer {
	
	Contestant(int port) {
		super(port);
		
	}
	//private static BufferedReader br;
	private static Map<Integer, Integer> pwPairs = new TreeMap<Integer, Integer>();
	private static int[] place = new int[21];
	private static boolean adding = true;
	private static boolean removing = false;
	private static Integer[] torque = {-9, -3};
	private static ArrayList<Integer> myweights = new ArrayList<Integer>();
	private static Integer[][] totalTorque = new Integer[10][31];
	private static String flag;
	
	private void updateInfo(String command){	
		
		String[] line = command.split("\n");
		
		for(int i=1; i<line.length; i++){
			String[] el = line[i].split(" ");
			if(Integer.parseInt(el[0]) != place[i-1]){
				place[i-1] = Integer.parseInt(el[0]);
				int p = Integer.parseInt(el[1]);
				int w = Integer.parseInt(el[3]);
				pwPairs.put(p, w);
				computeTorque(p, w);
				updatePosition(p);
			}
		}
		
		if(line[0].equals("ADDING")){
			adding = true;
			removing = false;
		}else{
			removing = true;
			adding = false;
		}
	}
	private String updateTotalTorque(){
		int left = -torque[0];
		int right = -torque[1];
		boolean isMatch = false;
		ArrayList<PWPairs> solutions =new ArrayList<PWPairs>();
		ArrayList<PWPairs> mins = new ArrayList<PWPairs>();
		Integer[][] lefts = new Integer[10][2];
		Integer[][] rights = new Integer[10][2];
		int min = 1000;
		
		for(int i=0; i<myweights.size(); i++){
			lefts[i][0] = -1; 
			lefts[i][1] = 1000;
			rights[i][0] = -1; 
			rights[i][1] = 1000; 
			for (int j=0; j<31; j++)
			{
				System.out.print (totalTorque[i][j]+"  ");
			}System.out.println("");
		}
		for(int w=0; w<myweights.size(); w++){
			for(int j=w; j<totalTorque[w].length; j++){
				
				if (totalTorque[w][j] == -right)
				{
					rights[w][0] = j;
					rights[w][1] = 0; 
					solutions.add(new PWPairs(j-15, w+1));
					isMatch = true; 
					break; 
				}
				if (totalTorque[w][j] != -right && !isMatch)	
				{	if (Math.abs(totalTorque[w][j]+right) <=rights[w][1] && w>=1){
					rights[w][0] = j;
					rights[w][1] = Math.abs(totalTorque[w][j]+right);
					if (rights[w][1]<min){
						min=rights[w][1];
						mins.clear();
						mins.add(new PWPairs(j-15, w+1));
						}
					else if (rights[w][1]==min)
						mins.add(new PWPairs(j-15, w+1));	
				}

				}
				if (totalTorque[w][j] == left)
				{
					lefts[w][0] = j;
					lefts[w][1] = 0; 
					solutions.add(new PWPairs(j-15, w+1));
					isMatch = true; 
					break; 
				}
				if (totalTorque[w][j] != left && !isMatch)	
				{	if (Math.abs(totalTorque[w][j]-left) <=lefts[w][1] && w>=1){
					lefts[w][0] = j;
					lefts[w][1] = Math.abs(totalTorque[w][j]-left);
					if (lefts[w][1]<min){
						min=j;
						mins.clear();
						mins.add(new PWPairs(j-15, w+1));
						}
					else if (lefts[w][1]==min)
						mins.add(new PWPairs(j-15, w+1));	
					}
				}
			}
		}
		int index; 
		PWPairs move; 
		Random random = new Random();
		if (isMatch){
			index = random.nextInt(solutions.size()); 	
			System.out.println(solutions.get(index));
			move = solutions.get(index);}
		
		//case 2: if no exact match was found:
		else{
			System.out.println("nomatch");
			index = random.nextInt(mins.size()); 
			System.out.println(mins.get(index));
			move = mins.get(index);}
		
		System.out.println ("Our move is "+move);
		updateWeight(move.getWeight()); 
		updatePosition(move.getPosition()); 
		System.out.println("torque: "+torque[0]+"  "+torque[1]);
		return move.toString();
	}
	private String add(String command){
		if(flag == null){
			flag = " ";
			init();
		}
		updateInfo(command);
		String move = updateTotalTorque();
		return move;
	}
	private String remove(String command){
		return "";
	}
	protected String process(String command) {
		
		//System.out.println(command);
		System.out.println("Enter move (position weight): ");
		String move;
		if(adding){
			move = add(command);
		}else{			
			move = remove(command);
		}
		return move;			
	}
	private void updateWeight(int w){
	
		for(int p=0; p<31; p++){
			totalTorque[w-1][p] = Integer.MAX_VALUE;
		}
	}
	private void updatePosition(int p){
		for(int w=0; w<10;w++){
			totalTorque[w][p+15] = Integer.MAX_VALUE;
		}
	}
	private void computeTorque(int p, int w){
		torque[0] += ((-3) - p) * w;
		torque[1] += ((-1) - p) * w;
	}
	private static void init(){
		for(int i=0; i<21; i++){
			place[i] = 0;
		}
		for(int i=0; i<10; i++){
			myweights.add(i+1);
		}
		for(int w=0; w<10; w++){
			for(int p=-15; p<16; p++){
				if(p<-3){
					totalTorque[w][p+15] = (w+1)*(-3-p);
				}
				if(p>-4 && p <=-1){
					totalTorque[w][p+15] = 0;
				}
				if(p>-1){
					totalTorque[w][p+15] = (w+1)*(-1-p);
				}
			}
		}
	}
	public static void main(String[] args) throws Exception {
		//br = new BufferedReader(new InputStreamReader(System.in));
		Contestant con = new Contestant(Integer.parseInt(args[0]));
		
	}
}
