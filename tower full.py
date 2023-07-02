import dash,sqlite3,requests,json,pandas as pd
from dash import html, dcc
from dash.dependencies import Output, Input


app = dash.Dash(__name__, serve_locally=True)

def get_data():
    # API endpoints
    all_info_url = "http://127.0.0.1:5000/data1"
    team_info_url = "http://127.0.0.1:5000/data2"

    # Make API calls and parse the JSON responses
    all_info_response = requests.get(all_info_url)
    player_data = all_info_response.json()["allinfo"]["TotalPlayerList"]
    team_info_response = requests.get(team_info_url)
    team_data = team_info_response.json()["teamInfoList"]

    conn = sqlite3.connect("PATH TO SQL DB")
    cursor = conn.cursor()

    # Fetch the points from the "final_table" table
    select_statement = "SELECT team_name, total_points FROM final_table"
    cursor.execute(select_statement)
    rows = cursor.fetchall()

    # Create a dictionary to store the points for each team
    team_points = {team_name: total_points for team_name, total_points in rows}

    # Update killNum and rank for each team in teams dictionary
    teams = {}
    for team in team_data:
        teams[team["teamName"]] = {"killNum": team["killNum"], "rank": None, "liveState": [], "isOutsideBlueCircle": False}

    for player in player_data:
        teams[player["teamName"]]["liveState"].append(player["liveState"])
        teams[player["teamName"]]["rank"] = player["rank"]
        if player["isOutsideBlueCircle"]:
            teams[player["teamName"]]["isOutsideBlueCircle"] = True

    df = pd.DataFrame(teams)
    df = df.transpose()
    df["logo"] = df.index.map(lambda x: f"/assets/logos/{x}.png")
    df["liveStateCount"] = df["liveState"].map(lambda x: len([p for p in x if p in [0, 1, 2, 3]]))

    df["team_points"] = df.index.map(lambda x: team_points.get(x, 0))

    # Sort the DataFrame first by the number of players alive, then by team_points in descending order
    df = df.sort_values(by=["liveStateCount", "team_points"], ascending=[False, False])

    # Read the shortened team names from a local file
    with open("shortened_team_names.json", "r") as file:
        shortened_team_names = json.load(file)

    # Create a new column for the shortened team names
    df["shortened_team_name"] = df.index.map(lambda x: shortened_team_names.get(x, x))

    # Update the DataFrame with the team points
    df["team_points"] = df.index.map(lambda x: team_points.get(x, 0))

    df["background_image"] = df.apply(
        lambda row: ("assets/test.png", "assets/test.png")
        if row["isOutsideBlueCircle"]
        else ("assets/test.png", "assets/test.png"),
        axis=1
    )

    cursor.close()
    conn.close()
    return df


app.layout = html.Div(
    [
        html.Table(
            [
                html.Tbody(id="table-body"),
            ],
            className="custom-table"
        ),
        dcc.Interval(
            id='interval-component',
            interval=2 * 1000,  # update every 5 seconds
            n_intervals=0
        ),
    ],
    className="animate-bottom-container"
)


@app.callback(Output("table-body", "children"), [Input("interval-component", "n_intervals")])
def update_table(n):
    teams_sorted = get_data()
    rows = []
    dead_rows = []

    # Create the legend row
    legend_row = html.Tr(
        [
            html.Td("", className="legend-logo"),
            html.Td("teams", className="legend-name"),
            html.Td("alive", className="legend-status"),
            html.Td("pts", className="legend-pts"),
            html.Td("elim", className="legend-eliminations"),
        ],
        className="legend-row"
    )
    rows.append(legend_row)

    for team_name, team_data in teams_sorted.iterrows():
        if all(live_state > 3 for live_state in team_data["liveState"]):
            # The team is dead, so display the rank instead of the logo
            logo = html.Td(str(team_data["rank"]), className="team-rank")
        else:
            # The team is alive, so display the logo
            logo = html.Td(html.Img(src=team_data["logo"], style={"height": "35px"}), className="team-logo")

        team_name = html.Td(team_data["shortened_team_name"], className="team-name")

        live_states = team_data["liveState"]
        team_statuses = []
        for i, live_state in enumerate(live_states):
            if live_state == 0 or live_state == 1 or live_state == 2 or live_state == 3:
                icon = html.Img(src="assets/poze/alive.png", className="team-status")
            elif live_state == 4:
                icon = html.Img(src="assets/poze/knock.png", className="team-status")
            else:
                icon = html.Img(src="assets/poze/dead.png", className="team-status")

            team_statuses.append(html.Td(icon, className="team-status"))

            if (i + 1) % 2 == 0:
                # Insert an empty cell after every two team statuses to create a grid layout
                team_statuses.append(html.Td("", className="empty-cell"))

        team_points = html.Td(str(team_data["team_points"]), className="team-pts")
        eliminations = html.Td(str(team_data["killNum"]), className="team-eliminations")

        # Set the background image for the row based on the team name
        background_image = team_data['background_image'][0]
        if team_data['background_image'][1] == "pulsing":
            background_image = team_data['background_image'][2]
        row_style = {
            "background-image": f"url({background_image})",
            "background-size": "cover",
            "background-repeat": "no-repeat",
            "background-position": "center"
        }
        is_dead = all(live_state > 3 for live_state in team_data["liveState"])
        row_class_name = "team-row dead-row" if is_dead else "team-row" + " " + team_data["background_image"][1]
        row = html.Tr(
            [
                html.Td(logo, className="team-logo"),
                html.Td(team_name, className="team-name"),
                html.Td(
                    [
                        html.Div(team_statuses[:2], className="team-status-row"),
                        html.Div(team_statuses[2:], className="team-status-row")
                    ],
                    className="team-status-container"
                ),
                html.Td(team_points, className="team-pts"),
                html.Td(eliminations, className="team-eliminations"),
            ],
            className=row_class_name,
            id=f"row-{team_name}",
            style=row_style,
        )
        rows.append(row)
        if is_dead:
            dead_rows.append(row)

    # Move dead rows to the bottom of the table and add fade-in-down animation
    for i, row in enumerate(dead_rows):
        row_id = f"row-{teams_sorted.index[-(i + 1)]}"
        row.className = "animate__animated animate__fadeInDown team-row dead-row"
        if row_id != row.id:
            row.id = row_id
            rows.remove(row)
            rows.append(row)

    # Create the final row with a background image
    final_row = html.Tr(
        [
            html.Td(colSpan=6, children=[
                html.Div(
                    children=[
                        html.Img(src="assets/bottom.png", className="final-image"),
                    ],
                    className="final-row-container"
                )
            ])
        ],
        className="final-row"
    )
    rows.append(final_row)

    table_body = html.Tbody(rows, className="team-row")
    return table_body


if __name__ == "__main__":
    app.run_server(debug=False, port=8050, host="127.0.0.1")