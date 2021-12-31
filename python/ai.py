import numpy as np
import aiinpy as ai
from alive_progress import alive_bar

Board = 8
popsize = 1000
Score = np.zeros(popsize)
done = np.full(popsize, False)

Snake = [np.zeros((1, 2)) for _ in range(popsize)]
Apple = []
for _ in range(popsize):
  x = 0
  while np.sum(x) == 0:
    x = np.random.randint(Board, size=2)
  Apple.append(x)

model = ai.neuroevolution((8, 8), 4, popsize, [
  ai.nn(outshape=16, activation=ai.relu(), learningrate=0.1),
  ai.nn(outshape=16, activation=ai.relu(), learningrate=0.1),
  ai.nn(outshape=16, activation=ai.relu(), learningrate=0.1),
  ai.nn(outshape=4, activation=ai.stablesoftmax(), learningrate=0.1)
])

Turn = 0

NumOfGen = 1000
with alive_bar(NumOfGen) as bar:
  for gen in range(NumOfGen):
    while np.sum(done) != popsize:
      for player in range(popsize):
        if done[player] == False:
          input = np.zeros((Board, Board))
          input[Apple[0][0], Apple[0][1]] = 0.5
          for i in range(len(Snake[player])):
            if not np.array_equal(Snake[player][i], [8, 8]):
              input[int(Snake[player][i, 0]), int(Snake[player][i, 1])] = 1

          out = model.forwardsingle(input, player)

          # Detect key commands
          if np.max(out) == out[0]:
            Snake[player] = np.vstack(([Snake[player][0, 0], Snake[player][0, 1] - 1], Snake[player][:-1]))
          if np.max(out) == out[1]:
            Snake[player] = np.vstack(([Snake[player][0, 0] + 1, Snake[player][0, 1]], Snake[player][:-1]))
          if np.max(out) == out[2]:
            Snake[player] = np.vstack(([Snake[player][0, 0], Snake[player][0, 1] + 1], Snake[player][:-1]))
          if np.max(out) == out[3]:
            Snake[player] = np.vstack(([Snake[player][0, 0] - 1, Snake[player][0, 1]], Snake[player][:-1]))

          # Increase score
          if np.array_equal(Snake[player][0, :], Apple[player]):
            Score[player] += 1
            Snake[player] = np.vstack((Snake[player], [Board, Board]))

          # Check that new apple location is not on the snake
          i = 0
          while i < Snake[player].shape[0]:
            if Apple[player][0] == Snake[player][i, 0] and Apple[player][1] == Snake[player][i, 1]:
              Apple[player] = np.random.randint(Board, size=2)
              i = 0
            i += 1

          # Check out of bounds
          if Snake[player][0, 0] < 0 or Snake[player][0, 0] > Board - 1 or Snake[player][0, 1] < 0 or Snake[player][0, 1] > Board - 1:
            done[player] = True

          # Check intersecting with itself
          for i in range(1, Snake[player].shape[0]):
            if np.array_equal(Snake[player][0, :], Snake[player][i, :]):
              done[player] = True
      
      Turn += 1
      if Turn  == 100:
        done = np.full(popsize, True)
    
    print(np.sum(Score), np.max(Score))
    Score = np.zeros(popsize)
    done = np.full(popsize, False)

    Snake = [np.zeros((1, 2)) for _ in range(popsize)]
    Apple = []
    for _ in range(popsize):
      x = 0
      while np.sum(x) == 0:
        x = np.random.randint(Board, size=2)
      Apple.append(x)
    Turn = 0
    bar()