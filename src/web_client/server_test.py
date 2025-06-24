from web_client.gui.controller.update import fetch_player_data


def main():
    player_data = fetch_player_data(0)
    print(player_data)


if __name__ == "__main__":
    main()
