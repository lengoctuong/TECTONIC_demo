# Demo [TECTONIC](https://github.com/tsourolampis/Tectonic) for clustering amazon graph and analyze results

## Paper
- [Scalable Motif-Aware Graph Clustering](https://arxiv.org/abs/1606.06235)

## Authors
- [Charalampos E. Tsourakakis](https://tsourakakis.com/)
- [Jakub Pachocki](https://scholar.harvard.edu/meret/home)
- [Michael Mitzemacher](http://www.eecs.harvard.edu/~michaelm/)

## Clustering amazon graph with steps:

- **Set up**
```bash
cd '/content/drive/MyDrive/Colab-Notebooks/Tectonic-master/Amazon'
mkdir 'Output'
chmod +x ../mace222/mace
```

- **Step 1**
```python
python ../relabel-graph.py com-amazon.ungraph.txt com-amazon.top5000.cmty.txt amazon.mace amazon.communities
```

- **Step 2, 3**
```python
python ../mace-to-list.py amazon.mace amazon.edges
../mace222/mace C -l 3 amazon.mace _geq3_amazon.triangles
python ../_mace-u3.py _geq3_amazon.triangles amazon.triangles
```

- **Step 4, 5**
```python
python ../community-stats.py amazon.edges amazon.communities amazon.edges.stats
python ../community-stats.py amazon.triangles amazon.communities amazon.triangles.stats
```

- **Step 6, 7**
```python
python ../weighted-edges.py amazon.triangles amazon.edges amazon.out.graph amazon.out.mixed 667129
python ../normalized-edges.py amazon.out.mixed amazon.out.norm
```

- **Step 8**
```python
g++ -std=c++11 -o triangle_clusters ../triangle-clusters.cpp
chmod +x triangle_clusters
./triangle_clusters amazon.out.norm 334863 0.1 > amazon_clusters.txt
```

- **Step 9**
```python
python ../grade-clusters.py amazon.communities amazon_clusters.txt output.txt
```

## Analysis in ```CLUSTERING_AMAZON.ipynb``` file
- Clustering in many thresholds.
- Analyze amazon graph and top5000 communities.
- Analyze clustering results.

# BÀI TOÁN: phân cụm đồ thị amazon với TECTONIC.

### INPUT:
- File com-amazon.ungraph.txt: đồ thị amazon G(V, E) (với |E| dòng, mỗi dòng là một cạnh, với hai đỉnh cách nhau bởi space), với:
	- |V| = 334863
	- |E| = 925872
	- |T| = 667129 (số tam giác).
- File com-amazon.top5000.cmty.txt: top 5000 cộng đồng chất lượng nhất (theo Amazon) (với |C| dòng, mỗi dòng là bộ đỉnh, cách nhau bởi space), với |C| = 5000.
- Ngưỡng để loại bỏ cạnh (theta > 0).

### OUTPUT:
- Các cộng đồng được phân cụm theo TECTONIC.

==================================================
## Bước 1: run file relabel-graph.py.
- Chức năng: thay đổi nhãn đỉnh để được thứ tự tuần tự (từ 0 đến |V| - 1).
- Thực hiện:
	- Thay đổi nhãn đỉnh gốc thành thứ tự từ 0 đến |V| - 1.
	- Lưu vào 2 files: các láng giềng của từng đỉnh và các cộng đồng (với nhãn đỉnh mới).

**Input files:**
- com-amazon.ungraph.txt
- com-amazon.top5000.cmty.txt

**Output files:**
- amazon.mace: |V| dòng, dòng i là các láng giềng của đỉnh i mà không lặp lại.
- amazon.communities: |C| dòng, dòng i là cộng đồng với nhãn đỉnh mới.

==================================================
## Bước 2: run file mace-to-list.py.
- Chức năng: tìm các cạnh theo nhãn đỉnh đã thay đổi (ở bước 1) và lưu vào file.

**Input file:** mazon.mace

**Output file:**
- amazon.edges: |E| dòng, dòng i là bộ 2 dỉnh của một cạnh.

==================================================
## Bước 3: run mace.
- Chức năng: tìm các clique với ít nhất 3 đỉnh và nhiều nhất 3 đỉnh (tức các tam giác) và lưu vào file.

**Input file:** amazon.mace

**Ouput file:**
- amazon.triangles: |T| dòng, dòng i là bộ 3 đỉnh của một tam giác.

==================================================
## Bước 4: run file community-stats.py trên cạnh.
- Chức năng: thống kê số cạnh có lần lượt 0 (cạnh nằm ngoài hoàn toàn cộng đồng), 1 và 2 (cạnh thuộc hoàn toàn trong cộng đồng) đỉnh thuộc từng cộng đồng; thực hiện lưu kết quả vào file.

**Input files:**
- amazon.edges
- amazon.communities

**Output file:**
- amazon.edges.stats: |C| dòng, dòng i là bộ 3 chỉ số lần lượt là số cạnh có 0, 1 và 2 đỉnh thuộc cộng đồng i.

==================================================
## Bước 5: run file community-stats.py trên tam giác.
- Chức năng: thống kê số tam giác có lần lượt 0 (tam giác nằm ngoài hoàn toàn cộng đồng), 1, 2 và 3 (tam giác thuộc hoàn toàn trong cộng đồng) đỉnh thuộc từng cộng đồng; thực hiện lưu kết quả vào file.

**Input files:**
- amazon.triangles
- amazon.communities

**Output file:**
- amazon.triangles.stats: |C| dòng, dòng i là bộ 4 chỉ số lần lượt là số tam giác có 0, 1, 2 và 3 đỉnh thuộc cộng đồng i.

==================================================
## Bước 6: run file weighted-edges.py
- Chức năng: Thực hiện reweighting các cạnh theo số tam giác chứa nó của đồ thị và lưu kết quả vào file.

**Input files:**
- amazon.edges
- amazon.triangles

**Output files:**
- amazon.out.mixed : |V| dòng, dòng i chứa các cặp đỉnh tạo thành cạnh và số tam giác chứa nó (bao gồm các cạnh có trọng số bằng 0).
- amazon.out.graph: |V| dòng, dòng i chứa các cặp đỉnh tạo thành cạnh và số tam giác chứa nó (không bao gồm các cạnh có trọng số bằng 0)

==================================================
## Bước 7: normalized-edges.py
- Chức năng: Thực hiện chuẩn hóa các cạnh bằng cách chia trọng số cho tổng bậc 2 đỉnh của cạnh và lưu kết quả vào file.

**Input file:** amazon.out.mixed

**Output file:**
- amazon.out.norm |V| dòng, dòng i chứa các cặp đỉnh tạo thành cạnh và trọng số đã được chuẩn hóa.

==================================================
## Bước 8: compile file file triangle_clusters.cpp và run triangle_clusters
- Chức năng: thực hiện phân cụm đồ thị amazon với thuật toán TECTONIC và lưu kết quả các cộng đồng vào file.

**Input files:**
- amazon.out.norm
- numbers_of_nodes: số đỉnh của đồ thị, tức |V|.
- threshold_value: ngưỡng để loại bỏ cạnh, tức theta.

**Output file:**
- amazon_clusters.txt: các cộng đồng được phân theo TECTONIC, mỗi dòng là một cộng đồng với bộ đỉnh được cách nhau bằng space.

==================================================
## Bước 9: run file grade-clusters.py
- Chức năng: thực hiện định giá các cộng đồng vừa được phân dựa trên top 5000 cộng đồng.
- Thực hiện:
    - Định giá precision và recall theo top 5000 cộng đồng.
    - Lưu vào file kết quả định giá gồm: số đỉnh, precision và recall trên 5000 cộng đồng.

**Input files:**
- amazon.communities
- amazon_clusters.txt

**Output file:**
- output.txt: |C| dòng, dòng i là bộ 3 chỉ số: số đỉnh của cộng đồng, precision, recall được cách nhau bằng space.