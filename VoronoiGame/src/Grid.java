/**
 * 
 */

/**
 * @author ting
 *
 */
public class Grid {
	
	 Point center;
	 Point a;
	 Point b;
	 Point c;
	 Point d;
	int id;
	boolean taken ;
	
	public Grid(Point a, Point b, Point c, Point d){
		this.a = a;
		this.b = b;
		this.c = c;
		this.d = d;
		this.center.x = (a.x + b.x) / 2;
		this.center.y = (a.y + d.y) / 2;
	}
	public Grid(){	}
	public void set(Point a, Point b, Point c, Point d){
		this.a = a;
		this.b = b;
		this.c = c;
		this.d = d;
		this.center.x = (a.x + b.x) / 2;
		this.center.y = (a.y + d.y) / 2;
	}

	public double centerTo(Point p){
		return Math.pow((center.x - p.x), 2.0) + 
			   Math.pow((center.y - p.y), 2.0);
	}
	
	public Point beachy(Point p){
		Point ctr = this.center;
		for(int i=0; i<5; i++){
			ctr.x = (ctr.x + p.x)/2;
			ctr.y = (ctr.y + p.y)/2;
			
		}
		return ctr;
	}
	/**
	 * @param args
	 */
	public static void main(String[] args) {
		Grid grid = new Grid();
		grid.center = new Point(1024, 1024);
		System.out.println(grid.beachy(new Point(2048,2048)));
	}

}
