# en-lst-solver
Репозиторий с реализацией LST-eN метода. Создан по подобию solver_dummy. Всего в проекте фактически три солвер: `Temporal solver (TS)`, `Spatial solver (SS)` и `Amplification curves solver (ACS)`. TS решает задачу о поиске неустойчивых мод во временной постановке для задачи установившегося течения в канале, SS - в пространственной постановке для задачи Блазиуса. ACS решает задачу о поиске области ЛТП в пространсвтенной постановке для задачи Базиуса. Соответственно все методы для TS представлены в temporal_functions.py, для SS в `spatial_functions.py`, для ACS в `amplification_curves_functions.py`. Чтобы решать конкртеную задачу для конкретного солвера, надо воспользоваться следующими фукнциями (по сути точки входа): для TS - `temporal_solve(Re, alpha)`, для SS - `spatial_solve(N)`, для ACS - `amplfication_curves_solve(omega_min, omega_max, number_of_omegas)`, где в сигнатурах передаваемые пользователем параметры. Задачи для TS и SS считаются относительно быстро, ACS - не быстро. На выходе каждые солвер пользователю дает графики. 
Для TS график со всеми модами:

![Temporal spectrum](https://user-images.githubusercontent.com/11145647/143885599-c44b71e9-18a1-4937-a7bf-e411f5debcbc.jpg)

Для SS график со всеми модами и для сравнения данные для того же кейса из статьи:

![Spatial spectrum](https://user-images.githubusercontent.com/11145647/143885796-4608a2b0-a867-4e6c-b342-a4000544f931.png)

Для ACS график с наиболее неустойчивыми модами для каждого значения циклической частоты

![Unstable modes](https://user-images.githubusercontent.com/11145647/143885979-056e60fa-45ba-4bb9-a2e6-930d10c3aee4.jpg)

и график с кривыми усиления и сравнением с экспериментальными данными для каждого значения циклической частоты

![Amplification_curves](https://user-images.githubusercontent.com/11145647/143886068-a51dc489-ae11-4d3d-9235-ccf49e277261.jpg)

Опишем входные параметры для TS:

```
[
	{
          type: 'number',
          name: 'Re',
          label: 'Число Рейнольдса для набегающего потока',
          from: 1000,
          to: 20000,
          step: 1,
          example: 10000,
	},
	{
          type: 'number',
          name: 'alpha',
          label: 'Значение волнового числа \alpha',
          from: 0.1,
          to: 2.0,
          step: 0.01,
          example: 1.0,
	},
]    
```

Входные параметры для SS:

```
[
	{
          type: 'number',
          name: 'N',
          label: 'Число узлов сетки',
          from: 200,
          to: 2000,
          step: 10,
          example: 800,
	},
]    
```

Входные параметры для ACS:

```
[
	{
          type: 'number',
          name: 'omega_min',
          label: 'Минимальное значение циклической частоты',
          from: 500,
          to: 'omega_max',
          step: 100,
          example: 1000,
	},
	{
          type: 'number',
          name: 'omega_max',
          label: 'Максимальное значение циклической частоты',
          from: 'omega_min',
          to: 10000,
          step: 100,
          example: 7000,
	},
	{
          type: 'number',
          name: 'number_of_omegas',
          label: 'Число частот, взятое на равномерной сетке в указанном диапазоне',
          example: 8,
	},
]    
```

# Тестирование
Для тестирования солвера TS необходимо выполнить `python examples/temporal_run.py 10000 1.0`

Для тестирования солвера SS необходимо выполнить `python examples/spatial_run.py 800`

Для тестирования солвера ACS необходимо выполнить `python examples/amplification_curves_run.py 1000 7000 8`

Результаты сохраняются в папку out. Для TS это `Temporal spectrum.jpg`, для SS - `Spatial spectrum.jpg`, для ACS - `Unstable modes.jpg` и `Amplification_curves.jpg`

