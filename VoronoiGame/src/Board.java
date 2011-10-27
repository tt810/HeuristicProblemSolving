import java.util.Set;

/**
 * 
 */

/**
 * @author ting
 *
 */
public class Board {
	
	static double l = 1000;
	static double h = 1000;
	static int me;
	static int gridNum;
	static Grid[] grids;
	Set<Site> sites;
	Set<Point> sPoints;
	
	public Board(int totals, int me){
		this.me = me;
		int number = (int)Math.sqrt(totals);
		if(Math.pow(number, 2)<totals) 
			gridNum = number + 1;
		else 
			gridNum = number;
		//gridNum = 10;
		grids = new Grid[gridNum * gridNum];
		for(int i=0; i<grids.length; i++) {
			grids[i] = new Grid();
		}
		assignGrids();
	}
	
	static void assignGrids(){
		double gridl = l / gridNum;
		double gridh = h / gridNum;
		int num = 0;
		System.out.println(gridl + " "+gridh);
		for(double y=0; y<=(h-gridh); y+=gridh){
			for(double x=0; x<=(l-gridl); x+=gridl){					
				Point a = new Point(x,y);
				Point b = new Point((x+gridl), y);
				Point c = new Point((x+gridl),(y+gridh));
				Point d = new Point(x,(gridh+y));					
				grids[num].a = a;
				grids[num].b = b;
				grids[num].c = c;
				grids[num].d = d;
				grids[num].id = num;
				Point center = new Point();
				center.x = (a.x + b.x) / 2;
				center.y = (a.y + d.y) / 2;
				grids[num].center = center;
				System.out.println("("+a+") ("+b+") ("+c+") ("+d+") ("+center+")("+grids[num].center+")");
				num++;
			}
		}
	}
	private Point selectMaxMin(){
		double max = Double.MIN_NORMAL;
		int id = 0;
		if(sites.isEmpty()) id = 0;		
		for(Grid grid : grids){
			System.out.println(grid.a);
		}
		for(Grid grid : grids){
			System.out.println(sPoints.size() + " "+grid.center);
			for(Point sPoint : sPoints){
				System.out.println(sPoint+" site point ");
				if(sPoint.equals(grid.center)){
					System.out.println(grid.center+" taken");
					grid.taken = true;
				}
			}
		}
		for(Grid grid : grids){
			if(!grid.taken){
				System.out.println("not taken grid "+grid.center);
				double min = Double.MAX_VALUE;
				for(Site site : sites){
					double len = grid.centerTo(site.p);
					if(min > len){
						min = len;
					}
					
				}
				if(max < min){
					max = min;
					id = grid.id;
				}
			}
		}
		return grids[id].center;
	}
	
	public String getMyStep(){
		return selectMaxMin().toString();
	}
	static void print(){
		int nums = gridNum*gridNum;
		for(int i=0; i<nums; i++){
			System.out.println(grids[i].center);
		}
	}
	
	public String beachyMove(){
		double max = Double.MIN_NORMAL;
		int id = 0;
		for(Grid grid : grids){
			System.out.println(sPoints.size() + " "+grid.center);
			for(Point sPoint : sPoints){
				System.out.println(sPoint+" site point ");
				if(sPoint.equals(grid.center)){
					System.out.println(grid.center+" taken");
					grid.taken = true;
				}
			}
		}
		Site opSite = new Site();
		for(Grid grid : grids){
			if(!grid.taken){
				System.out.println("grid: "+grid.id);
				double min = Double.MAX_VALUE;				
				for(Site site : sites){
						double len = grid.centerTo(site.p);
						if(min > len ){
							min = len;
							opSite = site;
						}
					
				}
				if(opSite.owner != me){
					System.out.println(opSite.p + " " + id);
					if(max < min){
						max = min;
						id = grid.id;
					}
				}
			}
		}
		System.out.println(opSite.p);
		return grids[id].beachy(opSite.p).toString();
	}
	
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Board board = new Board(15, 0);
		board.print();
	}

}
