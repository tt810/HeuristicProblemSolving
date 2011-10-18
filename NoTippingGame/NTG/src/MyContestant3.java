
import java.io.*;
import java.util.*;

class MyContestant3 extends NoTippingPlayer {
	private static BufferedReader br;
  private static String my_color;

	MyContestant3(int port) {
		super(port);
    //System.out.println(-1 + " " + 10);
	}

  private void init(List<String> command)
  {
    boolean allEmpty = true;
    for (String s: command) {
      System.out.println(s);
      List<String> myCommands = new ArrayList<String>(Arrays.asList((s.split(" "))));
      int position = Integer.valueOf(myCommands.get(1));
      String color = myCommands.get(2);
      if (color.equals("Red") || color.equals("Blue"))
        if (position != 0)
          allEmpty = false;
    }
    if (allEmpty) { my_color = "Red";} else {my_color = "Blue";}
  }

	protected String process(String command) {
		System.out.println(command);
		System.out.println("Enter move (position weight): ");

    if (my_color == null) {
      List<String> theirCommands = new LinkedList<String>(Arrays.asList((command.split("\n"))));
      theirCommands.remove(0);
      init(theirCommands);
    }

    int[] bar = new int[31];
    for (int i = 0; i < bar.length; i++) {
      bar[i] = 0;
    }
    String move = "";
	int def_pos = 0;
	int def_weight = 0;
    Scanner in = new Scanner(command);
    String phase = in.next();
    //int choices = 0;
    if (phase.equals("ADDING")) {
      int choices = 0;
      int[] avail = new int[11];
      int[] avail2 = new int[11];
      for (int i = 0; i < 11; i++) {
        avail[i] = 0;
        avail2[i] = 0;
      }
      int left_balance = -9;
      int right_balance = -3;
      for (int i = 0; i < 21; i++) {
        int on = in.nextInt();
        int location = in.nextInt();
        String player = in.next();
        int weight = in.nextInt();
        if (on == 1) {
          bar[location + 15] = weight;
          left_balance += weight*(-3-location);
          right_balance += weight*(-1-location);

        }
        else if (player.equals(my_color)) {
          avail[weight] = 1;
          choices++;
          //System.out.println(weight + " is available for red");
        }
        else {
          avail2[weight] = 1;
          choices++;
        }
      }
      
      //int[] l = pruneA(bar, avail, avail2, 0, choices, 
      //               left_balance, right_balance, 0);
    //move = l[0] + " " + l[1];

     
      //      System.out.println(left_balance + " " + right_balance);
      //Read all the input :D
	 if (my_color.equals("Red")) {  
      int min_right = right_balance;
      int delta_weight = 0;
      
      for (int i = 1; i < 11; i++) {
        if (avail[i] == 1) {
			def_weight = i;
          for (int j = 0; j < 16; j++) {
            if (bar[j+15] == 0) {
				def_pos = j;
              delta_weight = i*(-1-j);
              if (-1*delta_weight <= right_balance) {
                if (min_right > right_balance+delta_weight) {
                  min_right = right_balance + delta_weight;
                  move = j + " " + i;
                }
              }
              else {
                break;
              }
            }
          }
        }
      }
      min_right = left_balance;
      if (move.equals("")) {
        for (int i = 1; i < 11; i++) {
          if (avail[i] == 1) {
            for (int j = -1; j > -16; j--) {
              if (bar[j+15] == 0) {
                delta_weight = i*(-3-j);
                if (-1*delta_weight >= left_balance) {
                  if (min_right < left_balance + delta_weight) {
                    min_right = left_balance + delta_weight;
                    move = j + " " + i;
                  }
                }
                else {
                  break;
                }
              }
            }
          }
        }
      }
     }
     else {
		 for (int i = 10; i > 0; i--) {
			 if (avail[i] == 1) {
				 def_weight = i;
				 for (int j = -2; j < 16; j++) {
					 if (bar[j+15] == 0) {
						 def_pos = j;
						 int delta_left = i*(-3-j);
						 int delta_right = i*(-1-j);
						 if (-1*delta_left >= left_balance && -1*delta_right <= right_balance) {
							 move = j + " " + i;
							 break;
						 }
					 }
					 if (j <= 11) {
						 if (bar[-2-j+15] == 0) {
							 int delta_left = i*(-3-(-2-j));
							 int delta_right = i*(-1-(-2-j));
							 if (-1*delta_left >= left_balance && -1*delta_right <= right_balance) {
								 move = (-2-j) + " " + i;
								 break;
							 }
						 }
					 }
				 }
				 if (!move.equals("")) {
					 break;
				 }				 
			 }
		 }
	 }
	 if (move.equals("")) {
//        System.out.println("I'm broked");
		 return def_pos + " " + def_weight;
//        return ":(";
      }
      
      //We want right_balance to be as small as possible
    }
    else {
      //Remove the smallest (relative) weights
      int choices = 0;
      int left_balance = -9;
      int right_balance = -3;
      for (int i = 0; i < 21; i++) {
        int on = in.nextInt();
        int location = in.nextInt();
        String player = in.next();
        int weight = in.nextInt();        
                
        if (on == 1) {
			def_pos = location;
			def_weight = weight;
          choices++;
          left_balance += weight*(-3-location);
          right_balance += weight*(-1-location);
          bar[location + 15] = weight;
          /*
          if (location == -2) {
            return "-2 " + weight;
          }
          if (location == -1) {
            return "-1 " + weight;
          }
          if (location == -3) {
            return "-3 " + weight;
          }
          */
          //System.out.println(location + " " + weight);
        }
      }
      
      int l = pruneR(bar, 0, choices, choices, left_balance, right_balance);
      if (bar[l+15] == 0) {
		  return def_pos + " " + def_weight;
//        System.out.println("i lose  "+l);
      }
      move = l + " " + bar[l + 15];

      /*
      in = new Scanner(command);
      in.next();
      int min_rel = 10000;
      for (int i = 0; i < 21; i++) {
        int on = in.nextInt();
        int location = in.nextInt();
        String player = in.next();
        int weight = in.nextInt();
        int rel_weight = 0;
        if (on == 1) {
          rel_weight = weight*(-2-location);
          if (Math.abs(rel_weight) < Math.abs(min_rel)) {
            if (right_balance - weight*(-1-location) >= 0 && 
                left_balance-weight*(-3-location) <= 0) {
              min_rel = rel_weight;
              move = location + " " + weight;
            }
          }
        }
      }
      */
      
      if (move.equals("")) {
//        System.out.println("I lose :((((((");
		  return def_pos + " " + def_weight;
      }
    }
    
    
    
    /*		try {
			br.readLine();
		} catch (Exception ev) {
			System.out.println(ev.getMessage());
      }*/
    
    
    System.out.println(move);
		return move;			
	}

  public static int[] pruneA(int[] bar, int[] avail, int[] avail2, int depth, 
                             int choices, int left, int right, int turn) {
    if (choices == 0) { 
      int[] x = {1,0};
      return x;
    }
   
    if (depth == 4) { // this is not happening right now
      int[] x = {2,0};
      return x;
    }
    
    int max = 0;
    int num = 0;
    int location = 0;
    int position = -16;
    int weight = 0;
    if (turn % 2 == 0) { // red turn
      for (int i = 1; i < avail.length; i++) {        
        if (avail[i] == 1) { // weight is available
          for (int j = 0; j < bar.length; j++) {
            num = 0;
            if (bar[j] == 0) { // bar is empty
              location = j - 15;
              int nLeft = left + i * (-3 - location);
              int nRight = right + i * (-1 - location);
              if (nLeft <= 0 && nRight >= 0) {
                int[] tempBar = new int[31];
                int[] tempAvail = new int[11];
                for (int k = 0; k < bar.length; k++) {
                  tempBar[k] = bar[k];
                }
                tempBar[j] = i;
                for (int k = 1; k < avail.length; k++) {
                  tempAvail[k] = avail[k];
                }
                tempAvail[i] = 0;
                int[] p = pruneA(tempBar, tempAvail, avail2, depth+1,
                                 choices-1, nLeft, nRight, turn+1);
                num += p[0]; //Change for alpha-beta
              }
            }
            //if (num > 2)
            //  System.out.println(num);
            if (num > max) {
              max = num;
              position = j - 15;
              weight = i;              
            }
          }      
        }
      }
    }
    else { // blue turn
      for (int i = 1; i < avail.length; i++) {        
        if (avail2[i] == 1) { // weight is available
          for (int j = 0; j < bar.length; j++) {
            num = 0;
            if (bar[j] == 0) { // bar is empty
              location = j - 15;
              int nLeft = left + i * (-3 - location);
              int nRight = right + i * (-1 - location);
              if (nLeft <= 0 && nRight >= 0) {
                //System.out.println("hello");
                int[] tempBar = new int[31];
                int[] tempAvail = new int[11];
                for (int k = 0; k < bar.length; k++) {
                  tempBar[k] = bar[k];
                }
                tempBar[j] = i;
                for (int k = 1; k < avail2.length; k++) {
                  tempAvail[k] = avail2[k];
                }
                tempAvail[i] = 0;
                int[] p = pruneA(tempBar, tempAvail, avail2, depth+1,
                                 choices-1, nLeft, nRight, turn+1);
                num += p[0]; // Change for alpha beta
              }
            }
            if (num > max) {
              max = num;
              position = j - 15;
              weight = i;
            }
          }
        }
      }
    }

    if (depth != 0) {
      int[] x = { max, 0 };
      return x;
    }
    else {
      int[] x = { position, weight };
      return x;
    }
  }
  
  public static int Fitness(int left, int right, int[] bar) {
    int diff = right - left;
    // Want big smallest rel. weight
    // Want board to be even.
    int min_rel_weight = 10000;
    int max_rel_weight = 0;
    for (int i = 0; i < 31; i++) {
      if (bar[i] != 0) {
        min_rel_weight = Math.min(min_rel_weight, Math.abs((i-13)*bar[i]));
        max_rel_weight = Math.max(max_rel_weight, Math.abs((i-13)*bar[i]));
      }
    }
    int unbalance = Math.max(diff-right, diff-Math.abs(left));
    // Want min_rel_weight to be big, unbalance to be small
    // The more weights on the board, the more min_rel_weight should matter, and also the bigger unbalance is.
    //int fitness = 80/unbalance + min_rel_weight;
    //if (fitness > 0) {
    //System.out.println(fitness);
    //}

    if (my_color.equals("Red")) {
      return 3000/unbalance/diff + min_rel_weight;
    }
    else {
      return 2000-max_rel_weight;
    }
 }

  public static int pruneR(int[] bar, int depth, int choices, 
                           int choices2, int left, int right) {
    
    if (choices == 0) {
      if (my_color.equals("Red"))
        return 0;
      return 1000000000;
    }
//    if (choices2 > 15) {
      if (depth == 15-2*((choices2+2)/4)) {
        return Fitness(left, right, bar);
      }
//    }
    //else if (choices2 > 13) {
    //  if (depth == 7) {
    //    return Fitness(left, right, bar);
    //  }
    //}
//    else {
  //    if (depth == 7) {
    //    return Fitness(left, right, bar);
      //}
    //}
    
    int num = 0;
    int max = 0;
    int min = 1000000000;
    int minIndex, maxIndex;
    minIndex = maxIndex = -1;
    int smallest_rel = 1000000;
    int rel = 0;
    
    if (depth%2 == 0) {
      max = 0;
      for (int i = 0; i < bar.length; i++) {
        num = 0;
        int location = i - 15;
        int weight = bar[i];
        if (bar[i] != 0) {
          int tempL = left - weight*(-3-location);
          int tempR = right - weight*(-1-location);
          if (tempL <= 0 && tempR >= 0) { // move is okay
            int[] temp = new int[31];
            for (int j = 0; j < 31; j++) {
              temp[j] = bar[j];
            }
            temp[i]--;
            //int nLeft = left;
            //int nRight = right;
            //num += pruneR(bar, depth+1, choices-1, tempL, tempR); //Change for alpha beta
            num = pruneR(bar, depth+1, choices-1, choices2, tempL, tempR);
            rel = Math.abs(weight*(-2-location));
            if (my_color.equals("Red")) {
              if (num > max) {
                max = num;
                maxIndex = location;
              }
              else if (num == max && rel <= smallest_rel) {
                smallest_rel = rel;
                maxIndex = location;
              }
            }
            else {
              if (num > max) {
                max = num;
                maxIndex = location;
              }
              else if (num == max && rel >= smallest_rel) {
                smallest_rel = rel;
                maxIndex = location;
              }
            }  
          }
        }
      }
    }

    else {
      max = 1000000000;
      for (int i = 0; i < bar.length; i++) {
        //num = 1000000;
        int location = i - 15;
        int weight = bar[i];
        if (bar[i] != 0) {
          int tempL = left - weight*(-3-location);
          int tempR = right - weight*(-1-location);
          if (tempL <= 0 && tempR >= 0) { // move is okay
            int[] temp = new int[31];
            for (int j = 0; j < 31; j++) {
              temp[j] = bar[j];
            }
            temp[i]--;
            //int nLeft = left;
            //int nRight = right;
            //num += pruneR(bar, depth+1, choices-1, tempL, tempR); //Change for alpha beta
            num = pruneR(bar, depth+1, choices-1, choices2, tempL, tempR);
            if (num <= max) {
              max = num;
              maxIndex = location;
            }
          }
        }
      }
    }
   
    if (depth == 0) {      
      //return minIndex;      
      return maxIndex;
    }
    
    if (depth % 2 == 0) { 
      //return min;      
      return max;
    }
    
    else {       
      return max;
    }    
  }
  
	public static void main(String[] args) throws Exception {
		br = new BufferedReader(new InputStreamReader(System.in));
		new MyContestant3(Integer.parseInt(args[0]));

    //System.out.println(-1 + " " + 10);
	}  
}
