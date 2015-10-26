#download_stuff.py

##requirements:
 * python3

##usage:
 * download the download_stuff.py file to any place you like, e.g. ~/scripts_n_stuff
 * create a main folder for the homepage you want to download stuff from (e.g. string_theory)
 * create a text file download_stuff.conf, which contains one line for every "subpage" you want to download from, this line needs to contain the url of the subpage and the folder name the downloads are supposed to go, seperated by a whitespace (i.e. csv format)
    ```
    http://www.physik.lmu.de/lehre/vorlesungen/wise_15_16/TVI_TMP-TD1_-String-Theory-I/Tutorials/index.html tutorials
    ```
 * call the download_stuff.py script from the main folder:
    ```bash
    ~/scripts_n_stuff/download_stuff.py
    ```
 * if authentication is required, specify username and password as extra arguments:
    ```bash
    ~/scripts_n_stuff/download_stuff.py user passwd
    ```
 * generally, download_stuff tries to determine which files are already present and avoids redownloading these. If you wish to overwrite such files, use the *force* flag `-f`
    ```bash
    ~/scripts_n_stuff/download_stuff.py -f
    ```

