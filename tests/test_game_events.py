import pytest
import asyncio
from src.events.game import (
    CombatEvent,
    GameEvent,
    IfEvent,
    DamageEvent,
    MenuEvent,
    ConversationEvent,
    ChangeLevelEvent,
    eventFromDict,
)
from src.common.event_queue import loop, pushEvent, registerHandler, unregisterHandler
from src.globals import player


@pytest.mark.asyncio
async def test_game_event():
    task = asyncio.create_task(loop())
    """Test the base GameEvent functionality."""
    results = []
    
    async def event_start_handler(params):
        results.append(f"start: {params['event'].eventId}")

    async def event_end_handler(params):
        results.append(f"end: {params['event'].eventId}")

    registerHandler("event_start", event_start_handler)
    registerHandler("event_end", event_end_handler)

    event = GameEvent("test_event", {"nextEvent": "next_test"})
    result = await event()
    await asyncio.sleep(0.1)
    assert result == "next_test"
    assert results == ["start: test_event", "end: test_event"]

    unregisterHandler("event_start", event_start_handler)
    unregisterHandler("event_end", event_end_handler)

    task.cancel()

@pytest.mark.asyncio
async def test_if_event():
    """Test the IfEvent functionality."""
    event = IfEvent("if_event", {"condition": "{{player.health > 50}}", "eventIdTrue": "eventA", "eventIdFalse": "eventB"})
    player.loadSave("pytest")

    player.player["health"] = 60
    assert(player.player["health"] == 60)
    result = await event()
    assert result == "eventA"

    player.player["health"] = 40
    result = await event()
    assert result == "eventB"


# @pytest.mark.asyncio
# async def test_damage_event():
#     """Test the DamageEvent functionality."""
#     results = []

#     async def gameover_handler(params):
#         results.append("gameover_triggered")

#     registerHandler("gameover", gameover_handler)

#     player.player["health"] = 100
#     damage_event = DamageEvent("damage_event", {"hp": 20})
#     await damage_event()

#     assert player.player["health"] == 80
#     assert "gameover_triggered" not in results

#     damage_event = DamageEvent("damage_event", {"hp": 100})
#     await damage_event()

#     assert player.player["health"] == 0
#     assert "gameover_triggered" in results

#     unregisterHandler("gameover", gameover_handler)


@pytest.mark.asyncio
async def test_menu_event():
    """Test the MenuEvent functionality."""
    menu = MenuEvent(
        "menu_event",
        {"entryList": ["Option1", "Option2"], "eventList": ["event1", "event2"]},
    )

    menu.select(1)  # Simulate selecting the second option
    result = await menu()

    assert result == "event2"


@pytest.mark.asyncio
async def test_conversation_event():
    """Test the ConversationEvent functionality."""
    convo = ConversationEvent("conversation_event", {"dialogue": [("NPC", "Hello!"), ("Player", "Hi!")]})

    assert convo.currentLine() == ("NPC", "Hello!")
    convo.nextLine()
    assert convo.currentLine() == ("Player", "Hi!")
    convo.nextLine()

    result = await convo()
    assert result == convo.nextEvent


# @pytest.mark.asyncio
# async def test_event_from_dict():
#     """Test dynamic event creation from a dictionary."""
#     event = eventFromDict("DamageEvent", "dynamic_event", {"hp": 10})
#     assert isinstance(event, DamageEvent)

#     result = await event()
#     assert player.player["health"] == player.player["health"] - 10


@pytest.fixture
def setup_player():
    """Fixture to reset player stats before each test."""
    player.loadSave("pytest")
    player.player.set_value('health', 80)
    player.player.set_value('attack', 10)
    player.player.set_value('armor', 5)


@pytest.mark.asyncio
async def test_combat_event_attack(setup_player):
    """Test the player's attack action in CombatEvent."""
    combat = CombatEvent("combat1", {
        "opponentHealth": 50,
        "opponentAttack": 10,
        "opponentDefense": 3,
        "nextEvent": "postCombat"
    })

    # Player attacks opponent
    combat.player_attack()
    assert combat.opponentHealth < 50  # Health should decrease
    assert combat.opponentHealth >= 0  # Health should not drop below zero


@pytest.mark.asyncio
async def test_combat_event_brace(setup_player):
    """Test the player's brace action in CombatEvent."""
    combat = CombatEvent("combat1", {
        "opponentHealth": 50,
        "opponentAttack": 10,
        "opponentDefense": 3,
        "playerHealAmount": 10,
        "nextEvent": "postCombat"
    })

    # Player braces
    initial_health = player.player['health']
    message = combat.player_brace()
    assert player.player['health'] > initial_health  # Health should increase
    assert "healing" in message.lower()  # Message should indicate healing

async def asyncRepeat(function, arg):
    while True:
        await asyncio.sleep(0.1)
        function(arg)

@pytest.mark.asyncio
async def test_combat_event_flee(setup_player):
    """Test the player's flee action in CombatEvent."""
    combat = CombatEvent("combat1", {
        "opponentHealth": 50,
        "opponentAttack": 10,
        "opponentDefense": 3,
        "nextEvent": "postCombat",
        "eventFlee" : "eventFlee"
    })

    # Player flees
    task = asyncio.create_task( asyncRepeat(combat.action, 'flee'))
    res = await combat()
    task.cancel()
    assert combat.fled is True  # Player should have fled
    assert (res == "eventFlee")

@pytest.mark.asyncio
async def test_combat_event_completion(setup_player):
    """Test the completion of CombatEvent."""
    combat = CombatEvent("combat1", {
        "opponentHealth": 10,
        "opponentAttack": 0,
        "opponentDefense": 3,
        "nextEvent": "postCombat"
    })

    # Simulate a full combat loop
    tsk = asyncio.create_task( asyncRepeat(combat.action, 'attack'))
    res = await combat()
    tsk.cancel()
    assert res == "postCombat"
    assert combat.opponentHealth <= 0 
