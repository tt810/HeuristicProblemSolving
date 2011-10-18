/**
 * 
 */


import java.util.Map;
import java.util.TreeMap;

/**
 * @author ting
 *
 */
public final class Support {
	
	private Map<Integer, Integer> pwPairs = new TreeMap<Integer, Integer>();
	private Integer[] score = {0, 0}; 
	private int lPosition = -3;
	private int rPosition = -1;
	/**
	 * initialize the two supports, add the original weight 3kg to position -4, 
	 * This weight can be removed during the remove period.
	 */
	public Support(){
		init();
	}
	/**
	 * set the <position, weight> pairs to zero, if add put weight, if remove set back 
	 * weight to zero, in order to reduce the execution time.
	 */
	public void init(){
		//the board weights 3kg, gravity center at position: 0
		//so, left init score = (-3 - 0) * 3 = -9;
		//right init score = (-1 - 0) * 3 = -3;
		this.score[0] = -9;
		this.score[1] = -3;
		for(int i=-15; i<16; i++){
			this.pwPairs.put(i, 0);
		}
		add(-4, 3);
	}
	/**
	 * add weight to a certain position
	 * @param position
	 * @param weight
	 */
	public void add(int position, int weight){
		if(this.pwPairs.get(position) != 0)
			throw new
				IllegalArgumentException("position taken!");
		
		this.score[0] += (this.lPosition - position) * weight;
		this.score[1] += (this.rPosition - position) * weight;
		this.pwPairs.put(position, weight);
	}
	/**
	 * remove weight from a specified position
	 * @param position
	 */
	public void remove(int position){
		if(this.pwPairs.get(position) == 0)
			throw new
				IllegalArgumentException("empty position!");
		int weight = this.pwPairs.get(position);
		this.score[0] -= (this.lPosition - position) * weight;
		this.score[1] -= (this.rPosition - position) * weight;
		this.pwPairs.put(position, 0);
	}
	/**
	 * get score of each support
	 * @return an array of score, leftSupport = getScore[0], rightSupport = getScore[1]
	 */
	public Integer[] getScore(){
		return this.score;
	}
	/**
	 * if left support score is grater than zero, 
	 * or right support score is less than zero, tip; 
	 * @return true if tip, else false
	 */
	public boolean isTip(){
		return (this.score[0] > 0 || this.score[1] < 0);
	}
	
	public static void main(String[] args){
		Support s = new Support();
		System.out.println(s.getScore()[0] + " "+ s.getScore()[1]);
		System.out.println(s.isTip());
		s.add(1, 3);
		System.out.println(s.getScore()[0] + " "+ s.getScore()[1]);
		System.out.println(s.isTip());
		
		s.remove(1);
		s.remove(-4);
		System.out.println(s.getScore()[0] + " "+ s.getScore()[1]);
		System.out.println(s.isTip());
	}
}
