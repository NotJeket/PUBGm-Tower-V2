## PUBGm-Tower-V2 ##

**Description**:

The Real-Time Damage Tracker is a web application built using the Dash framework. It fetches data from two API endpoints to get information about teams and players in a gaming competition. The application displays a table of the teams' real-time damage data. The table is periodically updated based on the live state data obtained from the APIs. The teams are sorted based on the number of players alive and their kill count. The application provides visual cues for the team's status, such as whether they are alive, knocked, or eliminated. The table includes team logos, team names, kill counts, and the status of each player.

**Features**:

- Display the live state of each player in a table that can be sorted by team and number of live players.

- For the teams populated with players the teams are sorted by the players alive.

- For the teams that are considered dead the sorting is based on the PTS.

- Can read data from a local mockup file or a URL.

- Each row of the table displays the logo of the team, the name of the team, and the live state of each player as well as the Points (SQL DB sorted and calculated) and Eliminations.

- The live state of each player is displayed using icons that represent whether the player is alive, knocked out, or dead.

- The table can be resized based on the content.

- The program uses dash for the user interface.

- The program is cross-platform and can be run on Windows, Linux, and macOS.

- The program updates the data every 1 second.

- Ability to customize fonts, backgrounds, and various visual modifications.
  
- Support for shortened Team Names with a .json file

**Installation**:

1\. Clone the repository.

2\. Install the required dependencies:

   pip install dash requests pandas

**Usage**:

1\. Make sure you have Python installed on your system.

2\. Open a terminal or command prompt.

3\. Navigate to the directory where the program is located.

4\. Run the program using the following command:

   python TOWER.py

5\. Access the application in your web browser by navigating to http://127.0.0.1:8050.

6\. The application will periodically fetch data from the API endpoints as well as a local SQL DB and update the table with the real-time damage data for each team. The table is sorted based on the number of players alive and their kill count.

**Customization**:

- Team Logos: Place the team logos in the assets/logos/ directory. The logos should be in PNG format and named after the respective team. For example, the logo for a team named "TeamA" should be named TeamA.png.

- Status Icons: The application uses different status icons for representing the player's status (alive, knocked, or dead). The icons are located in the assets/poze/ directory. You can customize or replace these icons as per your preference.

- Styling: The CSS styles for various elements of the application are defined in the assets/style.css file. You can modify this file to change the visual appearance of the application.

**Dependencies**:

- Dash

- Requests

- Pandas

**Screenshot**:

![image](https://github.com/NotJeket/PUBGm-Tower-V2/assets/37781149/aa377c89-ae26-4741-8551-7467eea5661a)


**Flowchart**:

![code2flow_fKQ1Ml (2)](https://github.com/NotJeket/PUBGm-Tower-V2/assets/37781149/8d7e1111-5982-4444-9cae-6a0cb5f0877b)


**License**:

This project is licensed under the MIT License. See the [LICENSE](https://github.com/NotJeket/PUBGm-Tower-V2/blob/main/LICENSE) file for details.
