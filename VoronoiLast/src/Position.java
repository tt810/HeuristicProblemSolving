
public final class Position {
	double x;
	double y;
	
	public Position(){
		this.x = 0;
		this.y = 0;
	}
	
	public Position(double x, double y){
		this.x = x;
		this.y = y;
	}
	
	@Override
	public boolean equals(Object o){
		if(o == null ) return false;
		if(this == o) return true;
		if(!(o instanceof Position)) return false;
		Position p = (Position)o;
		return this.x == p.x && this.y == p.y;
	}
	
	public double distance(Position other){
		double otherX = other.x;
		double otherY = other.y;
		double power = Math.pow((x - otherX), 2.0) + 
		   			   Math.pow((y - otherY), 2.0);
		return Math.sqrt(power);
	}
	
	public Position percent(Position p, double ratio){
		Position newP = new Position();
		newP.x = (p.x + ratio*x)/(1 + ratio);
		newP.y = (p.y + ratio*y)/(1 + ratio);
		return newP;
	}
	
	@Override
	public String toString(){
		return ((int)x+" "+(int)y);
	}
}
