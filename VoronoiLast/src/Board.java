import java.util.ArrayList;
import java.util.Collection;
import java.util.HashMap;
import java.util.Iterator;
import java.util.Map;


public class Board {

	private double[][] board = new double[1000][1000];
	private Map<Integer, ArrayList<Position>> owners;
	private ArrayList<Position> positions = new ArrayList<Position>();
	private int me;
	
	public Board(Map<Integer, ArrayList<Position>> owners, int me){
		this.me = me;
		for(int y=0; y<1000; y++){
			for(int x=0; x<1000; x++){
				board[y][x] = -1;
			}
		}
		this.owners = owners;
		getPositions();
	}
	
	Map<Position, ArrayList<Position>> polygons = new HashMap<Position, ArrayList<Position>>();
	public void assignPolygon(){
		for(int y=0; y<1000; y++){
			for(int x=0; x<1000; x++){
				Position point = new Position(x, y);
				Position owner = smallestDis(point);
				if(polygons.containsKey(owner)){
					polygons.get(owner).add(point);
				}else{
					ArrayList<Position> points = new ArrayList<Position>();
					points.add(point);
					polygons.put(owner, points);
				}
			}
		}
	}
	
	public Position getresult(){
		assignPolygon();
		Position biggestPolygon = new Position();
		int biggestsize = Integer.MIN_VALUE;
		Iterator<Position> keys = polygons.keySet().iterator();
		while(keys.hasNext()){
			Position polygon = keys.next();			
			int o = own(polygon);
			System.out.println("score: "+polygons.get(polygon).size()+ " owner: "+o);
			if(o != me){
				int size = polygons.get(polygon).size();
				if(size > biggestsize){
					biggestsize = size;
					biggestPolygon = polygon;
				}
			}
		}
		Position farPoint = far(biggestPolygon, polygons.get(biggestPolygon));
		Position result = biggestPolygon.percent(farPoint, 1.618);
		System.out.println("farPoint: "+farPoint+" result: "+result);
		return result;
	}
	
	private int getRate(){
		int rate = 2;
		if(positions.size() <= 3){
			rate = 4;
		}else if(positions.size() <= 15){
			rate = 3;
		}
		return rate;
	}
	
	private Position far(Position center, ArrayList<Position> points){
		Position farPoint = new Position();
		double longest = Integer.MIN_VALUE;
		for(Position point : points){
			double dis = center.distance(point);
			if(longest < dis){
				longest = dis;
				farPoint = point;
			}
		}
		return farPoint;
	}
	
	private int own(Position position){
		int owner = -1;
		Iterator<Integer> keys = owners.keySet().iterator();
		while(keys.hasNext()){
			Integer own = keys.next();
			ArrayList<Position> pos = owners.get(own);
			for(Position p : pos){
				if(p.equals(position)){return own;}
			}
		}
		return owner;
	}
	
	private void getPositions(){
		Collection<ArrayList<Position>> posLists = owners.values();
		System.out.println("all positions: "+ posLists.size());
		for(ArrayList<Position> poslist : posLists){
			for(int i=0; i<poslist.size(); i++){
				System.out.println("position: "+ poslist.get(i)+"&&&&& i "+i);
				positions.add(poslist.get(i));
			}
		}
		System.out.println("position number: "+positions.size());
	}
	
	private Position smallestDis(Position point){
		double smallest = Integer.MAX_VALUE;
		Position owner = new Position();
		for(int i=0; i<positions.size(); i++){
			double dis = positions.get(i).distance(point);
			if(dis < smallest){
				smallest = dis;
				owner = positions.get(i);
			}
		}
		return owner;
	}
	
	public static void main(String[] args) {
		// TODO Auto-generated method stub

	}

}
