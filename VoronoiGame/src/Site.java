/**
 * 
 */

/**
 * @author ting
 *
 */
public class Site {
	Point p;
	int owner;
	
	

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		
	}



	@Override
	public boolean equals(Object o){
		if(o == null) return false;
		if(this == o) return true;
		if(!(o instanceof Site)) return false;
		Site s = (Site)o;
		return this.p == s.p && this.owner == s.owner;
	}

}
