<h1 align="center">USGS-LIDAR Data</h1>
<div>
<a href="https://github.com/Abel-Blue/agriTech-USGS-LiDAR/network/members"><img src="https://img.shields.io/github/forks/Abel-Blue/agriTech-USGS-LiDAR" alt="Forks Badge"/></a>
<a href="https://github.com/Abel-Blue/agriTech-USGS-LiDAR/pulls"><img src="https://img.shields.io/github/issues-pr/Abel-Blue/agriTech-USGS-LiDAR" alt="Pull Requests Badge"/></a>
<a href="https://github.com/Abel-Blue/agriTech-USGS-LiDAR/issues"><img src="https://img.shields.io/github/issues/Abel-Blue/agriTech-USGS-LiDAR" alt="Issues Badge"/></a>
<a href="https://github.com/Abel-Blue/agriTech-USGS-LiDAR/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/Abel-Blue/agriTech-USGS-LiDAR?color=2b9348"></a>
<a href="https://github.com/Abel-Blue/agriTech-USGS-LiDAR/blob/main/LICENSE"><img src="https://img.shields.io/github/license/Abel-Blue/agriTech-USGS-LiDAR?color=2b9348" alt="License Badge"/></a>
</div>

</br>

![lidar-heatmap](https://www.geographyrealm.com/wp-content/uploads/2020/02/johnsons_reef_lidar.png)

<!-- ## Presentation Slide

- [Rossmann Pharmaceutical Sales prediction](https://www.canva.com/design/DAFBtdnLoKQ/hxJHGTgvoTwJMX9hXbbGVA/view?utm_content=DAFBtdnLoKQ&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

## Data visualization link

- [visualization link](https://share.streamlit.io/abel-blue/pharmaceutical-sales-prediction/main/app.py)

## Articles

- [Medium Article](https://medium.com/@Abel-Blue/pharmaceutical-sales-prediction-using-a-deep-learning-model-92d7d1e9626b) -->

## Table of Contents

- [Introduction](##Introduction)
- [Project Structure](#project-structure)
  - [data](#data)
  - [notebooks](#notebooks)
  - [scripts](#scripts)
  - [tests](#tests)
  - [logs](#logs)
  - [root folder](#root-folder)
- [Installation guide](#installation-guide)

## Introduction

<p>We are very interested in how water flows through a maize farm field. This knowledge will help us improve our research on new agricultural products being tested on farms.</p>

<p>How much maize a field produces is very spatially variable. Even if the same farming practices, seeds and fertilizer are applied exactly the same by machinery over a field, there can be a very large harvest at one corner and a low harvest at another corner. We would like to be able to better understand which parts of the farm are likely to produce more or less maize, so that if we try a new fertilizer on part of this farm, we have more confidence that any differences in the maize harvest are due mostly to the new fertilizer changes, and not just random effects due to other environmental factors.</p>

<p>We are tasked to produce an easy to use, reliable and well designed python module that domain experts and data scientists can use to fetch, visualise, and transform publicly available satellite and LIDAR data. In particular, our code should interface with USGS 3DEP and fetch data using their API.</p>

<!-- <img src="images/slide/3.png" name="">
<img src="images/slide/4.png" name=""> -->

## Project Structure

### [images](images):

- `images/` the folder where all snapshot for the project are stored.

### [logs](logs):

- `logs/` the folder where script logs are stored.

### [data](data):

- `data/` the folder where the dataset files are stored.

### [.github](.github):

- `.github/`: the folder where github actions and unit-tests are integrated.

### [.vscode](.vscode):

- `.vscode/`: the folder where local path are stored.
  stored.

### [notebooks](notebooks):

- `notebooks`: a jupyter notebook for preprocessing the data.

### [scripts](scripts):

- `scripts/`: folder where modules are stored.

### [tests](tests):

- `tests/`: the folder containing unit tests for the scripts.

### root folder

- `requirements.txt`: a text file lsiting the projet's dependancies.
- `.travis.yml`: a configuration file for Travis CI for unit test.
- `setup.py`: a configuration file for installing the scripts as a package.
- `README.md`: Markdown text with a brief explanation of the project and the repository structure.

# <a name='Installation guide'></a>Installation guide

### <a name='conda'></a>Conda Enviroment

```bash
conda create --name mlenv python==3.8.1
conda activate mlenv
```

then

```bash
git clone https://github.com/Abel-Blue/agriTech-USGS-LiDAR
cd agriTech-USGS-LiDAR
sudo python3 setup.py install
```

# <a name='license'></a>License

[MIT](https://github.com/Abel-Blue/agriTech-USGS-LiDAR/blob/main/LICENSE)
