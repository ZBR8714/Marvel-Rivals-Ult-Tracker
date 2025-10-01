# Step-by-Step Setup Guide for the Marvel Rivals Ultimate Tracker

Welcome! This guide will walk you through every step needed to get the ultimate tracker working on your computer. No coding experience is required!

### **Step 1: Download the Project**

1.  Go to the main page of this GitHub repository.
2.  Click the green **`< > Code`** button near the top.
3.  In the dropdown menu, click **`Download ZIP`**.
4.  Find the downloaded ZIP file (usually in your `Downloads` folder) and **unzip it**. You can right-click it and select "Extract All...". This will create a folder named something like `Marvel-Rivals-Tracker-main`.

### **Step 2: Install Python**

If you don't have Python, you'll need to install it.

1.  Go to the official Python website: [https://www.python.org/downloads/](https://www.python.org/downloads/)
2.  Click the "Download Python" button to get the latest version.
3.  Run the installer you downloaded.
4.  **VERY IMPORTANT:** On the first screen of the installer, check the box at the bottom that says **`Add Python to PATH`**. This is critical for the next steps.
5.  Click "Install Now" and complete the installation.

### **Step 3: Install the Required Libraries**

1.  Press the **Windows Key** and type `cmd`, then press Enter. This will open the Command Prompt.
2.  Now, we need to tell the Command Prompt to look inside the project folder you unzipped. Type `cd` followed by a space.
3.  Drag the project folder from your File Explorer and drop it directly into the Command Prompt window. It will paste the full path. Your command should look something like this: `cd C:\Users\YourName\Downloads\Marvel-Rivals-Tracker-main`
4.  Press **Enter**.
5.  Now that you're in the correct folder, copy and paste the following command into the Command Prompt and press **Enter**:
    ```
    pip install -r requirements.txt
    ```
    This will automatically install all the necessary libraries. Wait for it to finish.

### **Step 4: Create Your Ultimate Templates**

This is the most important step for making the tracker accurate!

1.  Launch *Marvel Rivals* and go into the Practice Range.
2.  As you use each of the four healer ultimates, press `Win + PrtScn` to take a screenshot the moment the subtitle appears.
3.  Go to your `Pictures/Screenshots` folder and open the screenshot in **MS Paint**.
4.  Use the **Select** tool to draw a very tight box around **only the subtitle text**.
5.  Click the **Crop** button.
6.  Go to `File > Save As > PNG picture`.
7.  Navigate to your project folder and save the image inside the **`ults`** folder.
8.  **You must use these exact filenames:**
    -   `luna_ult.png`
    -   `cloak_ult.png`
    -   `invisible_ult.png`
    -   `mantis_ult.png`

Repeat this process for all four ultimates.

### **Step 5: Configure the Subtitle Area**

The script needs to know where on *your* screen to look for subtitles.

1.  Open one of your full-sized screenshots in MS Paint again.
2.  Move your mouse cursor to the **top-left corner** of where the subtitle text can appear. In the bottom-left corner of MS Paint, you will see pixel coordinates (e.g., `123, 456`). The first number is the **X** (`left`) value, and the second is the **Y** (`top`) value.
3.  Now, figure out the `width` and `height` of this area.
4.  Open the `marvel_rivals_tracker.py` file with a text editor (like Notepad or VS Code).
5.  Find this section near the top and replace the numbers with your own:
    ```python
    # Example:
    SUBTITLE_MONITOR_AREA = {"top": 800, "left": 600, "width": 800, "height": 150}
    ```

### **Step 6: Run the Tracker!**

1.  Make sure *Marvel Rivals* is running in **Windowed Fullscreen** or **Windowed** mode.
2.  Go to your Command Prompt window (which should still be in the project folder).
3.  Type the following command and press **Enter**:
    ```
    python marvel_rivals_tracker.py
    ```
4.  The overlay is now running! Go into the game and test it. To stop the tracker, go back to the Command Prompt and press `Ctrl + C`.

You're all set! Enjoy the competitive edge.
