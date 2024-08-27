# FlashForge Printer Preview

This is a simple tool that allows you to see your printer stats in OrcaSlicer as the printer is printing. I made this since OrcaSlicer does not have a built-in feature to show the printer stats for FlashForge printers (Connection refused error in OrcaSlicer 2.1.1)

> ⚠️ This is not nearly as finished so expect bugs

## Installation

1. Download the latest release from the [release folder](https://github.com/JMcrafter26/flashforge-printer-preview/tree/main/api/release/program)
1. Windows: Run backend.exe | Other OS: Run backend.py
1. Open localhost:8899 in your browser

## Detailed installation

From [reddit](https://www.reddit.com/r/FlashForge/comments/1el5xeq/comment/lk64gw1/)

**A. For windows:** Download `backend.exe` and `index.html` from [here](https://github.com/JMcrafter26/flashforge-printer-preview/tree/main/api/release/program) and put them in the same folder.  
Then run `backend.exe`. (*Note:* Your antivirus may detect the file as a virus, which is not true. I used pyinstaller which converts the .py file into an EXE which does not require having Python installed. If you don't trust it, you can follow Step B)

**B. For all OS:** Download [`backend.py`](http://backend.py)  and `index.html` from [here](https://github.com/JMcrafter26/flashforge-printer-preview/tree/main/api/release/program) and put them in the same folder. Second, you need to install Python (if you haven't already). I would recommend Python 3.11 because I used and tested it with this version. You can find tutorials on how to install Python online. Then open the file in a terminal and run `python3` [`backend.py`](http://backend.py) in the folder where the file is located.

**NEXT:** This should give you a URL, which you will need to open in your browser. The URL should look something like this: [http://192.168.2.216:8899](http://192.168.2.216:8899)

You are greeted with a page that prompts you to enter your printer IP. You can get the IP from the info page on your printer or via your routers settings. After entering, click on save and reload the page. (Make sure your printer is on.) Then you should see a dashboard with information. (Do not expect everything to work, this is just a proof of concept).


## License and Credits

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Parts of the API by <https://github.com/01F0/flashforge-finder-api/>
