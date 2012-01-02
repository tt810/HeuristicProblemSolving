import sys, math, socket, re, time
try:
  import myplot2
  graphics = True
except ImportError:
  graphics = False

time_steps = 0

if len(sys.argv) < 7:
  print "python evasion_game_server.py M N host1 port1 host2 port2"
  exit(0)

M = int(sys.argv[1])
N = int(sys.argv[2])

class wall:
  def __init__(self, x0, y0, x1, y1):
    self.x0 = x0
    self.y0 = y0
    self.x1 = x1
    self.y1 = y1
  
class Player(object):
  
  def __init__(self, x, y, board):
    self.x = x
    self.y = y
    self.board = board
  
  def BounceMove(self, delta_x, delta_y):
    new_x = self.x + delta_x
    new_y = self.y + delta_y
    wall = self.board.wall_gr[new_x][new_y]
    x_b = 1
    y_b = 1
    if wall:
      if wall[0] == 0:
        y_b = -1
        new_y = self.y
      else:
        x_b = -1
        new_x = self.x
    if self.board.wall_gr[new_x][new_y]:
      if x_b == -1:
        y_b, x_b = -1, 1
        new_x = self.x + delta_x
        new_y = self.y
      else:
        x_b, y_b = -1, 1
        new_y = self.y + delta_y
        new_x = self.x
      if self.board.wall_gr[new_x][new_y]:
        x_b, y_b = -1, -1
        new_x = self.x
        new_y = self.y
    delta_y *= y_b
    delta_x *= x_b
    self.x = new_x
    self.y = new_y
    return delta_x, delta_y

class Prey(Player):

  def __init__(self, x, y, board):
    Player.__init__(self, x, y, board)
  
  def Move(self, delta_x, delta_y):
    max_delta = max(abs(delta_x),abs(delta_y))
    if max_delta > 1:
      return
    self.BounceMove(delta_x, delta_y)
    if self.board.wall_gr[self.x][self.y]:
      self.board.RemoveWall(self.board.hunter.last_build_wall_i)
      self.board.hunter.last_built = N
      self.BounceMove(delta_x, delta_y)

  def __str__(self):
    return "Prey:  " + str(self.x) + " " + str(self.y) + "\n"

class Hunter(Player):

  def __init__(self, x, y, board):
    Player.__init__(self, x, y, board)
    self.delta_x = 1
    self.delta_y = 1
    self.last_built = N
    self.last_build_wall_i = -1
  
  def Move(self):
    global time_steps
    time_steps += 1
    self.last_built += 1
    self.delta_x, self.delta_y = self.BounceMove(self.delta_x, self.delta_y)
    if self.board.wall_gr[self.x][self.y]:
      self.board.RemoveWall(self.last_build_wall_i)
      self.last_built = N
      self.delta_x *= -1
      self.delta_y *= -1
      self.BounceMove(self.delta_x, self.delta_y)

  def BuildWall(self, dir, min_coord, max_coord):
    if self.last_built < N:
      return
    if min_coord >= max_coord:
      min_coord, max_coord = max_coord, min_coord
    if dir == 0:
      if self.x < min_coord or self.x > max_coord:
        return
      self.last_build_wall_i = self.board.AddWall(dir, min_coord, max_coord, self.y)
    else:
      if self.y < min_coord or self.y > max_coord:
        return
      self.last_build_wall_i = self.board.AddWall(dir, min_coord, max_coord, self.x)
    self.last_built = 0

  def DestroyWall(self, wall_index):
    self.board.RemoveWall(wall_index)

  def __str__(self):
    return "Hunter:" + str(self.x) + " " + str(self.y) + " " + str(self.delta_x) + " " + str(self.delta_y) + "\n"

class BoardState(object):

  def __init__(self):
    self.wall_gr = [[None for a in range(502)] for b in range(502)]
    #(dir, min_coord, max_coord, fixed_coord)
    self.walls = [() for i in range(M+4)]
    self.guiwalls = [() for i in range(M)]
    self.hunter = Hunter(0, 0, self)
    self.prey = Prey(330, 200, self)
    self.indices_avail = range(M)
    self.indices_avail[:0] = [M, M+1, M+2, M+3]
    self.AddWall(0, -1, 500, -1)
    self.AddWall(0, -1, 500, 500)
    self.AddWall(1, 0, 499, -1)
    self.AddWall(1, 0, 499, 500)

  def AddWall(self, dir, min_coord, max_coord, fixed_coord):
    print dir, min_coord, max_coord, fixed_coord
    if len(self.indices_avail) == 0:
      return -1
    wall_i = self.indices_avail[0]
    if dir == 0:
      self.walls[wall_i] = (dir, min_coord, max_coord, fixed_coord)
      if wall_i < M:
        self.guiwalls[wall_i] = wall(min_coord, fixed_coord, max_coord, fixed_coord)
      for i in range(max_coord - min_coord + 1):
        if self.wall_gr[min_coord+i][fixed_coord]:
          self.walls[wall_i] = ()
          self.guiwalls[wall_i] = ()
          for j in range(i):
            self.wall_gr[min_coord+j][fixed_coord] = None
          return -1
        self.wall_gr[min_coord+i][fixed_coord] = self.walls[wall_i]
    if dir == 1:
      self.walls[wall_i] = (dir, min_coord, max_coord, fixed_coord)
      if wall_i < M:
        self.guiwalls[wall_i] = wall(fixed_coord, min_coord, fixed_coord, max_coord)
      for i in range(max_coord - min_coord + 1):
        if self.wall_gr[fixed_coord][min_coord+i]:
          self.walls[wall_i] = ()
          self.guiwalls[wall_i] = ()
          for j in range(i):
            self.wall_gr[fixed_coord][min_coord+j] = None
          return -1
        self.wall_gr[fixed_coord][min_coord+i] = self.walls[wall_i]
    del self.indices_avail[0]
    if self.wall_gr[self.prey.x][self.prey.y]:
      self.RemoveWall(wall_i)
      return -1
    return wall_i

  def RemoveWall(self, wall_index):
    if wall_index in self.indices_avail or wall_index >= M or wall_index < 0:
      return
    if self.walls[wall_index][0] == 0:
      dir, x0, x1, y = self.walls[wall_index]
      for i in range(x1 - x0 + 1):
        self.wall_gr[x0+i][y] = None
    else:
      dir, y0, y1, x = self.walls[wall_index]
      for i in range(y1 - y0 + 1):
        self.wall_gr[x][y0+i] = None
    self.walls[wall_index] = ()
    self.guiwalls[wall_index] = ()
    self.indices_avail.append(wall_index)

  def Caught(self):
    if math.sqrt((self.hunter.x - self.prey.x) ** 2 + (self.hunter.y - self.prey.y) ** 2) <= 4:
      return True

  def __str__(self):
    out = str(self.hunter) + str(self.prey)
    out += "Walls: ["
    wall_strs = []
    for i, wall in enumerate(self.walls[:-4]):
      if wall:
        if wall[0] == 1:
          wall_strs.append("%d (%d, %d, %d, %d)" % (i, wall[3], wall[1], wall[3], wall[2]))
        else:
          wall_strs.append("%d (%d, %d, %d, %d)" % (i, wall[1], wall[3], wall[2], wall[3]))
    out += ", ".join(wall_strs) + "]\n"
    return out

board = BoardState()
if graphics:
  root, canvas = myplot2.main() 
  myplot2.update(root, canvas, board.guiwalls, board.hunter.x, board.hunter.y,
               board.prey.x, board.prey.y)

HOST1 = sys.argv[3]
PORT1 = int(sys.argv[4])
HOST2 = sys.argv[5]
PORT2 = int(sys.argv[6])
s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.bind((HOST1, PORT1))
s1.listen(1)
conn1, addr1 = s1.accept()
print 'Connected by', addr1

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind((HOST2, PORT2))
s2.listen(1)
conn2, addr2 = s2.accept()
print 'Connected by', addr2
p_t_left = 120
h_t_left = 120
while 1:
  conn1.send("You are Hunter\n" + str(board))
  t0 = time.time()
  print "Time left for Hunter:", h_t_left
  h_move = conn1.recv(1024)
  h_t_left -= (time.time()-t0)
  r = re.compile('Remove:\[(.*)\] Build:(.*) Remove:\[(.*)\] Build:(.*)')
  h_params = r.split(h_move)
  print h_params
  h_rem = h_params[1].split(',')
  for wall_in in h_rem:
    if wall_in:
      board.RemoveWall(int(wall_in))
  h_add = h_params[2]
  if h_add:
    h_add = h_add.split()
    print h_add
    board.hunter.BuildWall(int(h_add[0]), int(h_add[1]), int(h_add[2]))
  board.hunter.Move()
  if board.Caught():
    break 
  conn2.send("You are Prey\n" + str(board))
  print "Time left for Preay:", p_t_left
  t0 = time.time()
  p_move = conn2.recv(1024)
  p_t_left -= time.time()-t0

  h_rem = h_params[3].split(',')
  for wall_in in h_rem:
    if wall_in:
      board.RemoveWall(int(wall_in))
  h_add = h_params[4]
  if h_add:
    h_add = h_add.split()
    board.hunter.BuildWall(int(h_add[0]), int(h_add[1]), int(h_add[2]))
  board.hunter.Move()
  
  p_move = p_move.split()
  board.prey.Move(int(p_move[0]), int(p_move[1]))
  if board.Caught():
    break
  if graphics:
    myplot2.update(root, canvas, board.guiwalls, board.hunter.x, board.hunter.y,
                   board.prey.x, board.prey.y)
print "The prey was caught in %d time steps" % time_steps
conn1.send("END")
conn2.send("END")
s1.close()
s2.close()

"""
for i in range(2000):
  if (i == 30):
    board.hunter.BuildWall(0, 20, 100)
  if (i == 349):
    board.hunter.BuildWall(0, 300, 499)
  if (i == 449):
    board.hunter.BuildWall(1, 350, 499)
  board.hunter.Move()
  if (i%2 == 0):
    board.prey.Move(-1, -1)
    myplot2.update(root, canvas, board.guiwalls, board.hunter.x, board.hunter.y,
                   board.prey.x, board.prey.y)
  print board.Caught()
"""
