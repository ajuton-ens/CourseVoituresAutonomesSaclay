# Document recensant les expériences Lidar

## Slamtec RpLidar A2M8
115200 bauds, 10 tours/seconde, 200 points par tour en mode express scan avec le module python rplidar-roboticia
Juste 80 points par tour en mode scan normal.
Attention, le lidar envoyant en continu, il faut recevoir en continu, sous peine de laisser le buffer de réception déborder.

## Slamtec RpLidar A2M12
256000 bauds, 10 tours/seconde, 300 points par tour en mode express scan avec le module python rplidar-roboticia

## Slamtec RpLidar A3M12
tourne plus vite, pas testé

## Slamtec RpLidar S2
1 Mbit/s trop de données pour être utilisé en python. Résultats prometteurs avec le noeud ROS2 associé (écrit en C/C++ certainement).

## Slamtec RpLidar S3
tourne plus vite, pas testé
