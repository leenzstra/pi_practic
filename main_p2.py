import random
from requests import Session
from functools import reduce
from helpers import awaiter, read_json_data
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

client = Session()
base_url = "https://musicbrainz.org/ws/2"
client.headers["User-Agent"] = "Mozilla/5.0 (U; Linux x86_64; en-US) Gecko/20100101 Firefox/74.4"


# ----- avg length
def fetch_release_data(release_id):
    """Получение информации о релизе"""
    return client.get(
        base_url + f"/release/{release_id}",
        params={"inc": "recordings+release-groups+artists", "fmt": "json"}).json()


def merge_tracks(release):
    """Объекдинение треков из релиза в один массив"""
    return reduce(lambda x, y: x["tracks"] + y["tracks"], release["media"]) if len(release["media"]) > 1 else release["media"][0]['tracks']


def tracks_avg_length(tracks_lengths):
    return sum(filter(None, tracks_lengths)) / len(tracks_lengths) if len(tracks_lengths) != 0 else None


# ----- albums name
def fetch_artist_data(artist_id):
    return client.get(
        base_url + f"/artist/{artist_id}",
        params={"inc": "release-groups+releases", "fmt": "json"},
    ).json()


def filter_albums(releases):
    """Отбрасывание компиляций"""
    return list(filter(lambda release: "Compilation" not in release["secondary-types"]
                       and release["primary-type"] == 'Album', releases))


def task1_wrapper():
    """Returns: [ {name: str, avglen: float, cds: [ {name: str, avglen: float} ]} ]"""
    # release_data = fetch_release_data('a4864e94-6d75-4ade-bc93-0dabf3521453')
    # print('-'*25, release_data['artist-credit'][0]['name'], '-'*25)

    # # Средняя продолжительность треков релиза из примера
    # release_avg_len = tracks_avg_length([track["length"]for track in merge_tracks(release_data)])
    # print(f'Average release "{release_data['release-group']['title']}" length',release_avg_len)

    # # Средняя продолжительность треков для каждого диска релиза из примера
    # release_avg_len = [tracks_avg_length([track["length"]for track in cd["tracks"]]) for cd in release_data["media"]]
    # for avg, cd in zip(release_avg_len, release_data["media"]):
    #     print(f'Average CD {cd['title']} length ', avg)

    releases = []
    for i, release_id in enumerate(random.sample(read_json_data('release_ids.json')['releases'], 50)):
        release_data = awaiter(1, fetch_release_data, release_id)
        print(i+1, '-'*25, release_data['artist-credit'][0]['name'], '-'*25)

        avg_len = tracks_avg_length([track["length"]
                                    for track in merge_tracks(release_data)])
        print(f'Average release "{
              release_data['release-group']['title']}" length', avg_len)

        info = {'artist': release_data['artist-credit'][0]['name'],
                'name': release_data['release-group']['title'], 'avglen': avg_len, 'cds': []}

        cd_avg_len = [tracks_avg_length(
            [track["length"]for track in cd["tracks"]]) for cd in release_data["media"]]
        for avg, cd in zip(cd_avg_len, release_data["media"]):
            print(f'Average CD {cd['title']} length', avg)
            info['cds'].append({'name': cd['title'], 'avglen': avg})

        releases.append(info)

    return releases


def task2_wrapper():
    # Функции сортировки по дате
    def cond_by_date(alb): return alb["first-release-date"]
    def sort_by_date(albs): return sorted(albs, key=cond_by_date)

    def print_artist_name(artist_data): print(
        '\n', '-'*25, artist_data['name'], '-'*25)

    def print_album_info(album):
        print(f'{album['first-release-date']} - {album['title']}')

    # Обработка инфы об альбомах
    def process_albums(artist_id, callback):
        artist_data = fetch_artist_data(artist_id)
        if callback:
            callback(artist_data)
        return sort_by_date(filter_albums(artist_data["release-groups"]))

    # # из примера
    # for album in process_albums('83d91898-7763-47d7-b03b-b92132375c47', print_artist_name):
    #     print_album_info(album)

    artist_releases = []
    # 15 исполнителей
    for artist_data in read_json_data("artists.json")["artists"]:
        info = {'artist': artist_data['name'], 'albums': []}
        for album in awaiter(1, process_albums, artist_data["id"], print_artist_name):
            print_album_info(album)
            info['albums'].append(
                {'date': album['first-release-date'], 'name': album['title']})
        artist_releases.append(info)

    return artist_releases


def visualize_lens(release_lens):
    release_names = []
    lens = []

    for r in release_lens:
        release_names.append(f'{r['artist']} - {r['name']}')
        lens.append(r['avglen'])

    df = pd.DataFrame()
    df["Release"] = release_names
    df["Average length"] = lens

    sns.barplot(x="Average length", y="Release", data=df.sort_values(
        by='Average length', ascending=False))
    plt.show()


def visualize_artist(artist_releases):
    df = pd.DataFrame(columns=["Artist", "Year", "Release"])
    for ar in artist_releases:
        for alb in ar['albums']:
            df.loc[len(df)] = [ar['artist'],
                               alb['date'].split('-')[0], alb['name']]

    series = df.groupby(['Artist'])['Artist'].count()
    series = series.sort_values(ascending=False)

    df = pd.DataFrame(columns=["Artist", "Releases"])
    artists_without_releases = set(
        [art['artist'] for art in artist_releases]).difference(list(series.index))
    df['Artist'] = series.index
    df['Releases'] = series.values
    for awr in artists_without_releases:
        df.loc[len(df)] = [awr,0]

    sns.barplot(x='Releases', y='Artist', data=df)
    plt.show()


if __name__ == "__main__":
    release_lens = task1_wrapper()
    visualize_lens(release_lens)

    print('-'*100)

    artist_releases = task2_wrapper()
    visualize_artist(artist_releases)
