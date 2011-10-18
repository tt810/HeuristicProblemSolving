/**
 * 
 */

/**
 * @author ting
 *
 */
public class PWPairs {
	
	private int position;
	private int weight;
	
	public PWPairs(int position, int weight){
		this.position = position;
		this.weight = weight;
	}
	public PWPairs(){
		
	}
	public void setP(int p){
		this.position = p;
	}
	public void setW(int w){
		this.weight = w;
	}
	public int get(int index){
		if (index == 0)
			return position;
		else
			return weight; 
	}
	
	public int getPosition(){
		return position;
	}
	
	public int getWeight(){
		return weight;
	}
	@Override
	public boolean equals(Object o){
		if(this == o)
			return true;
		if(!(o instanceof PWPairs))
			return false;
		final PWPairs po = (PWPairs) o;
		return po.position == this.position &&
				po.weight == this.weight;
				
		
	}
	
	@Override
	public String toString(){
		StringBuilder sb = new StringBuilder();
		sb.append(position+" ");
		return sb.append(weight).toString();
	}
}
