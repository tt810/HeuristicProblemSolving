
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.util.ArrayList;


/**
 * @author ting
 */
 


class Contestant2 extends NoTippingPlayer {
	
	Contestant2(int port) {
		super(port);
		
	}
	private static BufferedReader br;
	private static int[] place = new int[21];
	private static int[] replace = new int[21];
	private static boolean adding = true;
	private static boolean removing = false;
	private static Integer[] torque = {-9, -3};
	private static Integer[] myweights = new Integer[10];
	private static Integer[][] totalTorque = new Integer[10][31];
	private static String flag;
	
	private void updateInfo(String command){	
		
		String[] line = command.split("\n");
		
		for(int i=1; i<line.length; i++){
			String[] el = line[i].split(" ");
			if( Integer.parseInt(el[0]) == 1 && Integer.parseInt(el[0]) != place[i-1]){
				place[i-1] = Integer.parseInt(el[0]);
				int p = Integer.parseInt(el[1]);
				int w = Integer.parseInt(el[3]);
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
		int left = torque[0];
		int right = torque[1];
		Integer[][] sub = new Integer[10][31];
		for(int w=0; w<10; w++){
			if(myweights[w] != 0){
				for(int p=-15; p<16; p++){
					if(totalTorque[w][p+15]!= 0 && totalTorque[w][p+15] != Integer.MAX_VALUE){
						if(p<-4){
							int s = totalTorque[w][p+15] + left;
							if(s<=0)
								sub[w][p+15] = s;
						}
						if(p>-1){
							int s = totalTorque[w][p+15] + right;
							if(s>=0)
								sub[w][p+15] = s;
						}
					}
				}
			}
		}
		
		PWPairs pw = new PWPairs();
		int min = Integer.MAX_VALUE;
		for(int w=0; w<10; w++){
			
			if(myweights[w] != 0){
				
				
				for(int p=-15; p<16; p++){
					if(sub[w][p+15]!=null){
						if(min>=Math.abs(sub[w][p+15])){
							min = Math.abs(sub[w][p+15]);
							pw.setP(p);
							pw.setW(w+1);
						}
					}
				}
			}
		}
		myweights[pw.getWeight()-1] = 0;
		return pw.toString();
	}
	private String add(String command){
		
		String move = updateTotalTorque();
		return move;
	}
	private boolean isTip(Integer[] torque, PWPairs pw){
		int left = torque[0] - (-3 - pw.getPosition())*pw.getWeight();
		int right = torque[1] - (-1 - pw.getPosition())*pw.getWeight();
		return (left > 0 || right < 0);
	}
	
	private String remove(String command){
		Integer[] rTorque = {-9, -3};
		ArrayList<PWPairs> myPairs = new ArrayList<PWPairs>();
		ArrayList<PWPairs> hePairs = new ArrayList<PWPairs>();
		String[] line = command.split("\n");
		
		for(int i=1; i<line.length; i++){
			String[] el = line[i].split(" ");
			if(Integer.parseInt(el[0]) == 1){
				int p = Integer.parseInt(el[1]);
				int w = Integer.parseInt(el[3]);
				rTorque[0] += (-3 -p)*w;
				rTorque[1] += (-1 -p) *w;
				myPairs.add(new PWPairs(p, w));
				hePairs.add(new PWPairs(p,w));
			}
			
		}
		ArrayList<PWPairs> noTips = new ArrayList<PWPairs>();
		for(int i=0; i<myPairs.size(); i++){
			PWPairs myChoice = myPairs.get(i);
			if(!isTip(rTorque, myChoice)){
				noTips.add(myChoice);
			}
		}
		
		PWPairs myPick = new PWPairs();
		
		if(noTips.isEmpty()){
			myPick = myPairs.get(0);
			return myPick.toString();
		}
		int max = 0;
		int badMax = 0;
		PWPairs badBestOne = new PWPairs();
		PWPairs bestOne = new PWPairs();
		for(int i =0; i<noTips.size(); i++){
			int finalDecision = 0;
			myPick = noTips.get(i); 
			Integer[] cTorque = getTorque(rTorque, myPick);
			int heTipTime = 0;
			for(int j=0; j<hePairs.size(); j++){
				PWPairs hisPick = hePairs.get(j);
				Integer[] hTorque = getTorque(cTorque, hisPick);
				if(!hisPick.equals(myPick)){
					if(isTip(cTorque, hisPick)){
						heTipTime++;
						finalDecision++;
					}else{
						for(int k=0; k<myPairs.size(); k++){
							PWPairs my2Pick = myPairs.get(k);
							if((!my2Pick.equals(myPick))&& (!my2Pick.equals(hisPick))){
								if(!isTip(hTorque, my2Pick)){
									finalDecision++;
									break;
								}
							}
						}
					}
				}
			}
			if(heTipTime==(myPairs.size()-1)){
				return myPick.toString();
			}else if(finalDecision==(myPairs.size()-1)){
				if(heTipTime > max){
					max = heTipTime;
					bestOne = myPick;
				}
			}else{
				if(finalDecision>badMax){
					badMax = finalDecision;
					badBestOne = myPick;
				}
			}
		}
		if(bestOne.equals(new PWPairs(0,0))){
			return badBestOne.toString();
		}
		return bestOne.toString();
	}
	private Integer[] getTorque(Integer[] rTorque, PWPairs pw){
		Integer[] t = {rTorque[0], rTorque[1]};
		t[0] -= (-3 -pw.getPosition())*pw.getWeight();
		t[1] -= (-1 -pw.getPosition())*pw.getWeight();
		return t;
	}
	protected String process(String command) {
		if(flag == null){
			flag = " ";
			init();
		}
		updateInfo(command);
		String move;
		if(adding){
			
			move = add(command);
		}else{			
			move = remove(command);
		}
		return move;			
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
			replace[i] = 1;
		}
		for(int i=0; i<10; i++){
			myweights[i] = i+1;
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
		br = new BufferedReader(new InputStreamReader(System.in));
		Contestant2 con = new Contestant2(Integer.parseInt(args[0]));
		
	}
}
