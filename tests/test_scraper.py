from utils.scraper import get_round_links
from bs4 import BeautifulSoup


def test_get_round_links():
    html = """
    <div class="flickity-slider" style="left: 0px; transform: translateX(0%);">
        <div class="post-event-watch-round-nav__item scroll-nav-item selected first is-selected" data-item-index="0"
            style="position: absolute; left: 0%;" id="jq-1715247203056-3">
            <a href="/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4446" data-no-scroll="1" title="Men's Heats"
                data-gtm-event=""
                class="ignore">
                <span class="round-name">Men's Heats</span>
                <span class="round-status">Completed</span>
            </a>
        </div>
        <div class="post-event-watch-round-nav__item scroll-nav-item last is-selected" data-item-index="1"
            style="position: absolute; left: 50%;"><a href="/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4447"
                data-no-scroll="1" title="Women's Heats"
                data-gtm-event=""
                class="ignore">
                <span class="round-name">Women's Heats</span>
                <span class="round-status">Completed</span>
            </a></div>
    </div>
    """
    soup = BeautifulSoup(html, "html.parser")

    round_links = get_round_links(soup)
    assert len(round_links) == 2
    assert round_links[0].sex == "men"
    assert (
        round_links[0].event_link
        == "/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4446"
    )
    assert round_links[1].sex == "women"
    assert (
        round_links[1].event_link
        == "/events/2024/ct/196/lexus-pipe-pro/results?statEventId=4447"
    )
