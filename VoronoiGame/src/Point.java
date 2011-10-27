
/**
 * 
 */

/**
 * @author ting
 *
 */
public class Point implements Comparable<Point>{
	double x, y;
	
	public Point(double x, double y){
		this.x = x;
		this.y = y;
	}
	
	public Point(){ }
	
	@Override
	public boolean equals(Object o){
		if(o == null ) return false;
		if(this == o) return true;
		if(!(o instanceof Point)) return false;
		Point p = (Point)o;
		return this.x == p.x && this.y == p.y;
	}
	@Override
	public String toString(){
		return ((int)x+" "+(int)y);
	}

	@Override
	public int compareTo(Point o) {
		if(this == o) return 0;
		if(this.x < o.x) return -1;
		if(this.x > o.x) return 1;
		return (int)(this.y-o.y);
	}
}
