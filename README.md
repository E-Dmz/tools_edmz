# ICM toolbox
Tools developed at the Renier Lab at the Paris Brain Institute (aka ICM)

This repo contains: 
- notebooks for analysis of experiments
- useful snippets of code
- insights into libraries, atlases, etc.
This toolbox is continuously developed, so you can expect deprecation of some 

I'm trying to keep track of what's deprecated, in a separate folder.

Testing data may or may not be provided.


## Installation
Currently, functionalities are implememted with a `tools_edmz` package but may later be done using the ClearMap 2.1 API
Install `ClearMapUi` (we may write a script to install minimal components required for analysis)

```bash
conda create --name icm_toolbox python=3.8
conda install -c conda-forge jupyter jupyter_contrib_nbextensions cached_property numpy pandas matplotlib seaborn

cd
mkdir -p code/doumazane
cd code/doumazane
git clone git@github.com:doumazane/icm_toolbox.git
cd icm_toolbox
pip install -e .

cd
mkdir -p code/ChristophKirst
cd code/ChristophKirst
git clone git@github.com:ChristophKirst/ClearMap2.git
git checkout gui
## write a script
```

Recommanded Jupyter notebooks extensions: 
- Collapsable headings
- Gist
- Execution time
- TraceBack Preview

## Recommanded aliases
Open .bash_aliases
`gedit ~/.bash_aliases`

```bash
alias ali="gedit ~/.bash_aliases"

alias cl="clear"
alias pm="python -m"

## various programs
alias fiji="~/programs/Fiji.app/ImageJ-linux64"
alias qpath="bash ~/programs/QuPath/bin/QuPath.sh"
alias pyc="/snap/pycharm-community/298/bin/pycharm.sh ./"

# jupyter
alias jn="jupyter notebook"
alias jl="jupyter lab"

## conda
alias cenvs="conda info --envs"
alias cact="conda activate"
alias cdeact="conda deactivate"
alias crev="conda list --revisions"
alias ccre="conda create --name"

## git
alias gst="git status"
alias gco="git checkout"
alias gcm="git commit -m"

## environments
alias cdtools="cd ~/code/doumazane/icm_toolbox"
alias catools="cact icm_toolbox"

alias caabba="cact abba-brainglobe-deepslice-itk"
alias cdabba="cd ~/code/NicoKiaru/ABBA-Python"

alias cacm="cact ClearMapUi"
alias cdcm="cd ~/code/ChristophKirst/ClearMap2"

alias cabggen="cact allen"
alias cdbggen="cd ~/code/brainglobe/bg-atlasgen"
```

## Cheat sheet `git`
```bash
pwd
git status
git add my_file
git rm --cached my_file
gedit .gitignore
# check this one echo "!**/*.ipynb" >> .gitignore
gh repo create
git remote -v
git remote set-url origin your_new_url
git branch 
git checkout -b branch_name
git checkout branch_name 

git switch remote_branch
```

## Cheat sheet `conda`
```bash
conda list
conda env remove -n your_env_name
conda create --clone
conda env export > env.yaml
conda env create -f env.yaml -n foo
```
https://stackoverflow.com/a/64384990/14908558

## Cheat sheet `gcloud`
