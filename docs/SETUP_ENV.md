## Create new enviornment 👨🏻‍💻

### Table of contents

- [Create new enviornment](#create-new-env)
  * [Via mamba](#new-env-mamba)
  * [Via conda](#new-env-conda)
  * [Via virtualenv](#new-env-virtualenv)

#

<a id="create-new-env" />

### 1. Create new enviornment

<a id="new-env-mamba" />

#### 1.1. Via mamba

```bash
brew install mambaforge
```

And then later install `mamba` via

```bash
conda install mamba -n base -c conda-forge
```

Now, you can create a new env via

```bash
mamba env create -n nutri-score -f docs/config/nutri-score_env.yaml
```

<a id="new-env-conda" />

#### 1.2. Via conda

Before starting further, make sure that you have `conda` (Anaconda) installed (otherwise, create a new env via [virutalenv](#new-env-virtualenv)). We will create a new enviornment for the purpose of our labs:

```bash
conda create -n nutri-score -f docs/config/nutri-score_env.yaml -y
```

and activate it

```bash
conda activate nutri-score
```

<a id="new-env-virtualenv" />

#### 1.3. Via virtualenv

You can create your virtual enviornment without conda as well. In order to do that, make sure that you have [`virtualenv`](https://pypi.org/project/virtualenv/) installed or else, you can install it via:


```bash
pip install virtualenv
```

Now, create your new enviornment called `nutri-score`

```bash
virtualenv -p python3 nutri-score
```

and then activate it via

```bash
source nutri-score/bin/activate
```
