from utils.models import Tour, Heat
from bs4 import BeautifulSoup


def test_tour_create():
    tour = Tour(
        tour_code="MCT",
        sex="men",
        event_link=["/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4446"],
        round_links=[],
    )
    assert tour.tour_code == "MCT"
    assert tour.sex == "men"
    assert tour.event_link == [
        "/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4446"
    ]


def test_tour_create_from_soup():
    html = """
    <div class="post-event-watch-round-nav__item scroll-nav-item last is-selected" data-item-index="1"
        style="position: absolute; left: 50%;">
        <a href="/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4447"
            data-no-scroll="1" title="Women's Heats"
            data-gtm-event='[{"tour_code":"WCT","click_type":"heat details click"}]'
            class="ignore">
            <span class="round-name">Women's Heats</span>
            <span class="round-status">Completed</span>
        </a>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    tour = Tour.from_soup(soup)
    assert tour.tour_code == "WCT"
    assert tour.sex == "women"
    assert (
        tour.event_link == "/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4447"
    )


# correctly parses valid HTML with multiple athletes
def test_correctly_parses_valid_html_with_multiple_athletes():
    html = """
    <div data-heat-id="1" data-heat-number="2" data-round-number="3" data-event-id="4">
        <div class="hot-heat-athlete" data-athlete-id="101" data-athlete-singlet="red">
            <div class="hot-heat-athlete__name">Athlete One</div>
            <div class="hot-heat-athlete__score">9.5</div>
            <div class="hot-heat-athlete__counted-waves">3</div>
        </div>
        <div class="hot-heat-athlete" data-athlete-id="102" data-athlete-singlet="blue">
            <div class="hot-heat-athlete__name">Athlete Two</div>
            <div class="hot-heat-athlete__score">8.7</div>
            <div class="hot-heat-athlete__counted-waves">2</div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    # Get the outer div element from soup
    div = soup.find("div")
    heats = Heat.from_soup(div)

    assert len(heats) == 2
    assert heats[0].athlete_id == "101"
    assert heats[0].name == "Athlete One"
    assert heats[0].score == "9.5"
    assert heats[0].waves == "3"
    assert heats[1].athlete_id == "102"
    assert heats[1].name == "Athlete Two"
    assert heats[1].score == "8.7"
    assert heats[1].waves == "2"


# correctly parses valid HTML with multiple athletes
def test_correctly_parses_valid_html_with_multiple_athletes_no_wave_score():
    html = """
    <div data-heat-id="1" data-heat-number="2" data-round-number="3" data-event-id="4">
        <div class="hot-heat-athlete" data-athlete-id="101" data-athlete-singlet="red">
            <div class="hot-heat-athlete__name">Athlete One</div>
            <div class="hot-heat-athlete__score">9.5</div>
        </div>
        <div class="hot-heat-athlete" data-athlete-id="102" data-athlete-singlet="blue">
            <div class="hot-heat-athlete__name">Athlete Two</div>
            <div class="hot-heat-athlete__score">8.7</div>
        </div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")
    # Get the outer div element from soup
    div = soup.find("div")
    heats = Heat.from_soup(div)

    assert len(heats) == 2
    assert heats[0].athlete_id == "101"
    assert heats[0].name == "Athlete One"
    assert heats[0].score == "9.5"
    assert heats[0].waves == "0"
    assert heats[1].athlete_id == "102"
    assert heats[1].name == "Athlete Two"
    assert heats[1].score == "8.7"
    assert heats[1].waves == "0"
