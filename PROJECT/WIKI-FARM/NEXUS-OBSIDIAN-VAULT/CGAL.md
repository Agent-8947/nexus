---
tags: [nexus-vault, geometry, computational-geometry, mesh, robust]
category: CS / Computational Geometry (High Precision)
language: C++14+
github: https://github.com/CGAL/cgal
---

# CGAL — Computational Geometry Algorithms Library

## Описание
**CGAL** — это мощнейшая и наиболее академически точная библиотека в мире для выполнения **геометрических вычислений**. В отличие от простых библиотек графики, CGAL гарантирует **точный результат** (Exact Computation), предотвращая ошибки округления при пересечении плоскостей, триангуляции и булевых операциях над 3D-сетками.

## Технический Стек
| Компонент | Технология |
|-----------|------------|
| Язык | C++ 14+ (Template-based) |
| Architecture | Kernels (Exact, Inexact) |
| Dependencies | Boost, GMP (архимедова точность), MPFR |
| Bindings | Python (PyCGAL) |
| Modules | Triangulation, Meshing, Convex Hull, Voronoi |

## Математическая Мощь
1. **Delaunay Triangulation (2D/3D)** — идеальное разбиение пространства на треугольники/тетраэдры.
2. **Surface Mesh Processing** — восстановление поверхностей из облака точек, сглаживание, фильтрация.
3. **Boolean Operations** — сложение, вычитание и пересечение 3D тел без "дырок".
4. **Collision Detection** — сверхточное определение коллизий сложных объектов.
5. **Alpha Shapes** — выделение "формы" из набора точек (определение контура облака).

## Архитектурная Ценность для NEXUS
- **Паттерн:** Геометрическая Истина (Geometric Truth). Если NEXUS должен проектировать физические объекты или анализировать 3D-сканы OSINT-объектов — CGAL это единственный способ сделать это без ошибок.
- **Интеграция:** Использование CGAL для "сшивания" (stitching) 3D-карт из облака точек, полученных лидаром дрона [[ARDUPILOT]].
- **Ключевое:** Поддержка чисел произвольной точности (MPFR).

## Пример: Выпуклая Оболочка (Convex Hull) C++
```cpp
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/convex_hull_2.h>
#include <vector>

typedef CGAL::Exact_predicates_inexact_constructions_kernel K;
typedef K::Point_2 Point_2;

std::vector<Point_2> points, result;
points.push_back(Point_2(0,0)); points.push_back(Point_2(1,1));
// ...
CGAL::convex_hull_2(points.begin(), points.end(), std::back_inserter(result));
# (Результат - минимальный многоугольник, охватывающий все точки)
```

## Связанные Репозитории
- [[ALGS4]] — база общих алгоритмов
- [[BULLET3]] — физика в реальном времени (CGAL точнее, Bullet быстрее)
- [[AWSOME-ROBOT-DESCRIPTIONS]] — 3D модели роботов
- [[ANOMALIB]] — аномалии в картинках
- [[AMARANTH]] — синтез железа
