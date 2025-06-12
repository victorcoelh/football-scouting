from web_client.gui.update import fetch_player_data, fetch_players


def main():
    player_data = fetch_player_data(0)
    print(player_data)


if __name__ == "__main__":
    main()
