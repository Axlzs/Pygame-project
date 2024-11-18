import math

max_xp = 4
enemies_killed_for_lvl = 0
level = 1

for i in range(1000):
    enemies_killed_for_lvl +=1
    if enemies_killed_for_lvl >= max_xp:
        print("level: ",level,"xp_needed: ",max_xp)
        enemies_killed_for_lvl = 0
        level+=1
        max_xp += int(math.log(max_xp,2))


# for i in range(1000):
#     enemies_killed_for_lvl +=1
#     if enemies_killed_for_lvl >= max_xp:
#         print("level: ",level,"xp_needed: ",max_xp)
#         enemies_killed_for_lvl = 0
#         level+=1
#         max_xp = int(max_xp*1.25)
