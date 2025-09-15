# Paris-Saclay Autonomous Car Race Rules (CoVAPSy)

These rules evolve from year to year; feel free to send your comments and suggestions.

## The Vehicle

The vehicle must use a Tamiya TT02 chassis/motor kit and, for propulsion, a NiMH 7.2V battery with a maximum capacity of 5000 mAh. A secondary battery, of any type, is allowed to power the electronics. Powering the motor with a voltage higher than the battery voltage is not allowed. The car must have a body covering more than 80% of it (estimated by the jury in a non-scientific way...).
The vehicle, with all its sensors and actuators, must fit within the dimensions below:

![car dimensions diagram](images/dimensions_voiture.png)

The car must be visible to vehicles following it: the car must have at least one opaque rectangle at the rear, 150 mm wide and 110 mm high. Only a small gap (< 10 mm high) for ground clearance is allowed.
Transparent bodies or those with green, red, or gray as the main color are not allowed. Guides for painting the car are available on YouTube (e.g., https://www.youtube.com/watch?v=MO5J6AqEpbs). A test with an RP-Lidar A2M12 or A2M8 validates the rear visibility of the car. If not detected (some black paints absorb infrared), off-white tape will be added to the rear of the car.

It is possible to remove the front-wheel drive to improve turning radius.

The car must be able to operate in both forward and reverse.

To improve steering mechanics, some plastic parts may be replaced with commercially available aluminum parts (Yeah Racing TATT-S03BU available at Rcmart.com or Tamiya kit 54574 sold at Conrad).
Any major modification to the chassis (beyond a few drillings) must be requested and approved by the other institutions participating in the race. The request must include references or plans of the intended modifications.

Team communication with the vehicle must be limited to sending a start signal and a stop signal. The vehicle may send information to the team (telemetry). Sending commands that modify the vehicle's behavior will result in team disqualification. As with mechanical modifications, it is possible to request permission from other institutions to use a trackside computer for offboard computation.

A standard car kit is available (see *Standard Car* menu) from the Ménagerie Technologique.

## The Track

The track layout is not known before the day of the competition. Providing the car with information about the track layout is prohibited. Referees may check this, for example, on an auxiliary track. The car may learn the track by completing up to 3 setup laps.

The track consists of 200 mm high borders, green on the right in the direction of travel and red on the left. These borders are made of straight elements and arcs with a curvature radius R = 400 mm or more. The floor is gray linoleum. The track is at all points wider than 800 mm but may contain obstacles inside.

Color references:

* GREEN: RAL 6037
* RED: RAL 3020
* FLOOR: PVC GERFLOR concrete effect leone anthracite l.4 m Ref 83309786 (Leroy Merlin)

Color references are approximate, and the track edges may be marked by impacts.

Here is an example of one of the 2023 tracks:

![example track layout](images/piste_2023.png)

A track kit is available from the Ménagerie Technologique.

## Homologation

Homologation is done in 4 steps:

* validation of vehicle elements (dimensions, battery, chassis, lidar-detectable color, etc.),
* validation of remote start and stop,
* verification of the vehicle's ability to move along a straight track section plus a curve without touching the borders,
* verification of the vehicle's ability to reverse in case of blockage against an obstacle and in the absence of a vehicle behind.

The referees may consider homologation with a penalty for minor rule violations: for example, a vehicle that does not stop or reverse properly.

For both races and qualifications, a car using SLAM may complete up to 3 setup laps, without obstacles. Obstacles or opponent cars are added afterward, once the car is on the starting grid.

## Qualifications 1 – Time Trial

The first qualification phase consists of 2 runs with a single car on track A, which includes fixed obstacles similar in size to a car.
For each run, the car completes 2 laps. The best of the 2 times is kept, to compensate for any technical issue during the first run.

If both runs fail to complete 2 laps, a time of 120 s is recorded.

At the end of the first qualification phase, the first car gets 25 points, the second 24 points, and so on down to a minimum of 5 points for any car with less than 120 s. Cars that do not complete a single 2-lap run get 0 points.

## Qualifications 2 – Races

The second qualification phase consists of 2 group races with 4 to 8 cars over 3 laps on track B and 3 laps on track C. The method for forming the N groups is based on the qualification ranking (group n is composed of cars ranked n%N, where n is the group number and N is the number of groups). In each race, the car accumulates points for the overall qualification ranking: 10 points for first place, 6 for second, 4 for third, and 2 points for cars that finish the race. A car that does not complete all 3 laps gets no points.

For each race (including the final):

* Teams have 3 minutes to set up their vehicle on the track.
* All vehicles in the group are positioned on the starting grid according to qualification results.
* Once all teams have declared they are ready, it is forbidden to touch the vehicles. The referee gives the start signal orally.
* The finishing order is recorded after a predefined number of laps (3 by default for qualification, 5 for finals).
* A car that does not complete the required number of laps is not ranked.

The referee and race marshals ensure the proper conduct of the races:

* A vehicle displaying clearly aggressive behavior towards opponents is disqualified and removed from the track, as is a car deliberately preventing another from overtaking.
* A vehicle immobilized on the track for more than 10 seconds, without being blocked by another car, is removed from the track.
* A vehicle that travels more than 2 m in the wrong direction is removed from the track.

## Final Phases – Races, in 2 Rounds

After the qualifications, each car receives 2 scores:

* the total coursesQualif (sum of points earned in the 2 qualification races)
* the total CLM+courseQualif (the previous score plus the points earned in the time trial qualification).

2 rounds are each composed of 3 races.

The top 2 of each group (by coursesQualif score, with CLM+courseQualif used to break ties) compete in race 1 of each round, the 3rd and 4th in race 2, and the others in race 3. The qualification ranking (by coursesQualif, with CLM+courseQualif as a tiebreaker) determines the starting grid, with the car with the most points starting at the front.

Referees record the finishing order after a predefined number of laps (5 by default) and award points as follows: 25 pts for 1st, 18 pts for 2nd, 15 pts for 3rd, 12 pts for 4th; 10 pts for 5th, 8 pts for 6th; 6 pts for 7th, 4 pts for 8th; 2 pts for 9th and 1 pt for 10th. A car that does not complete the required number of laps gets 0 points. Once the cars in the first race are ranked, points are then awarded to the cars in the second race, and so on.

The final ranking is based only on the points from the 2 final races. In case of a tie, the CLM+courseQualif score is used for the final ranking. If there is still a tie, the coursesQualif score is used.

Prizes are awarded to the 1st, 2nd, and 3rd in the overall ranking. There is also an innovation prize and a prize for the top license teams.