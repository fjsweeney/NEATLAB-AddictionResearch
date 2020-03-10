#Clustering practice:
clusters.py expects location data to be in ./locs and smoking reports to be in ./sm_reports subdirectories.

clusters.py can run 3 clustering algorithms:
- k-means
- Mean shift
- HDBSCAN

Mean shift is the more successful in clustering our types of data than the other ones, but it is possible to make k-means better by implementing the "elbow method".


###Stuff to look into:
Spatial KZ filter - remove sparse data? - https://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Zurbenko_filter
Smoothing - https://en.wikipedia.org/wiki/Smoothing

###Works on my machine:
.<br />
├── clusters.py<br />
├── gmplot_practice.py<br />
├── locs<br />
│   ├── location_1.csv<br />
│   ├── location_2.csv<br />
│   ├── location_3.csv<br />
│   ├── location_4.csv<br />
│   ├── location_5.csv<br />
│   └── location_6.csv<br />
├── mymap.html<br />
├── README.md<br />
└── sm_reports<br />
    ├── smoking_reports_1.csv<br />
    ├── smoking_reports_2.csv<br />
    ├── smoking_reports_3.csv<br />
    ├── smoking_reports_4.csv<br />
    ├── smoking_reports_5.csv<br />
    └── smoking_reports_6.csv<br />

