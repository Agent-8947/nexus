---
tags: [nexus-vault, hardware, robotics, urdf, sdf, physics-sim]
category: Hardware / Robotics Modeling
language: URDF / SDF / Collada (DAE)
github: https://github.com/robotology/awesome-robot-descriptions
---

# AWSOME-ROBOT-DESCRIPTIONS — Robotics Models & Sim Base

## Описание
**Awesome Robot Descriptions** — это курируемый список **описаний роботов (Robot Description Files)**. Он содержит ссылки на файлы в форматах **URDF (Unified Robot Description Format)** и **SDF (Simulation Description Format)** для сотен моделей: от манипуляторов (UR5, KUKA) и гуманоидов (Atlas, iCub) до дронов и колесных платформ. Это основа для любой физической симуляции роботов.

## Форматы Описания
1. **URDF (XML)** — стандарт в **ROS** (Robot Operating System), описывает связи (links) и суставы (joints) робота.
2. **SDF (XML)** — стандарт в симуляторе **Gazebo**, более мощный формат для сложных сред и физики.
3. **Collada (DAE) / STL** — 3D-сетки (meshes), которые определяют внешний вид робота.
4. **MJCF** — формат для физического движка **MuJoCo** (быстрый и точный симулятор).

## Почему это важно
- **Simulation**— прежде чем строить робота в жизни, его запускают в Gazebo/PyBullet/MuJoCo. Без URDF-файла это невозможно.
- **Kinematics**— описание длин сегментов и углов поворота нужно для расчета движений (Forward/Inverse Kinematics).
- **Physical Integration**— содержит данные о массе, центре тяжести и моментах инерции каждого сегмента робота.

## Архитектурная Ценность для NEXUS
- **Паттерн:** Цифровой Двойник Робота (Digital Twin). Знание структуры робота — основа для его автономного управления.
- **Интеграция:** Модуль NEXUS Robotics — автоматическая загрузка нужной модели в симулятор при обнаружении нового физического агента.
- **Ключевое:** Содержит "скелеты" (URDF) для почти всех промышленных роботов мира.

## Пример фрагмента URDF (Nexus Robot)
```xml
<link name="base_link">
  <visual>
    <geometry><box size="0.6 0.4 0.2"/></geometry>
    <material name="NEXUS_Blue"/>
  </visual>
</link>
<joint name="wheel_joint" type="continuous">
  <parent link="base_link"/><child link="wheel"/>
  <axis xyz="0 1 0"/>
</joint>
```

## Связанные Репозитории
- [[BULLET3]] — самый мощный физический движок
- [[ARDUPILOT]] — автопилот для управления дронами
- [[ARDUINO-FOC]] — низкоуровневое управление суставами
- [[AWSOME-WEEKLY-ROBOTICS]] — новости роботов
- [[AGIBOT_X1_INFER]] — инференс-модель для роботов
